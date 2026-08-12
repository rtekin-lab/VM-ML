# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.5. Derin Öğrenme Modellerini Ölçeklendirme ve Dağıtım (Deployment) › 12.5.1. Veri Paralelizmi vs. Model Paralelizmi › TensorFlow Dağıtık Eğitim: Kapsamlı Python Kodu
# Kitap  : Kod 12.11 (TensorFlow ile dağıtık eğitim stratejileri)
# Dosya : bolum12/12_05_01_tensorflow-dagitik-egitim-kapsamli-python-kodu.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================
import tensorflow as tf
import numpy as np
import os
import json
import time

# ─────────────────────────────────────────────────────────────────────
# 1. MirroredStrategy: Tek Makine, Çok GPU
# ─────────────────────────────────────────────────────────────────────

strategy = tf.distribute.MirroredStrategy()
print(f"Kullanılabilir GPU sayısı: {strategy.num_replicas_in_sync}")

# Model ve derleme MUTLAKA strategy.scope() içinde olmalı
with strategy.scope():
    base_model = tf.keras.applications.ResNet50(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )
    base_model.trainable = False  # Transfer learning: önce dondurup eğit

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(256, activation="relu",
                               kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation="softmax")
    ])

    # Doğrusal ölçekleme: n_gpu × base_lr
    n_gpu  = max(1, strategy.num_replicas_in_sync)
    base_lr = 0.001
    lr_schedule = tf.keras.optimizers.schedules.CosineDecayRestarts(
        initial_learning_rate=base_lr * n_gpu,
        first_decay_steps=1000,
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3)]
    )

model.summary()

# ─────────────────────────────────────────────────────────────────────
# 2. tf.data.Dataset ile Verimli Dağıtık Veri Yükleme
# ─────────────────────────────────────────────────────────────────────

BATCH_SIZE_PER_REPLICA = 32
GLOBAL_BATCH_SIZE      = BATCH_SIZE_PER_REPLICA * n_gpu
AUTOTUNE = tf.data.AUTOTUNE

def preprocess(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.image.resize(image, [224, 224])
    return image, label

def augment(image, label):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, 0.2)
    image = tf.image.random_contrast(image, 0.8, 1.2)
    return image, label

(X_tr, y_tr), (X_te, y_te) = tf.keras.datasets.cifar10.load_data()
y_tr, y_te = y_tr.squeeze(), y_te.squeeze()

train_dataset = (tf.data.Dataset.from_tensor_slices((X_tr, y_tr))
    .shuffle(50000, seed=42)
    .map(preprocess, num_parallel_calls=AUTOTUNE)
    .map(augment,    num_parallel_calls=AUTOTUNE)
    .batch(GLOBAL_BATCH_SIZE, drop_remainder=True)
    .prefetch(AUTOTUNE)             # GPU çalışırken CPU'da batch hazırla
    .cache()                        # İlk epoch'tan sonra RAM'de sakla
)

test_dataset = (tf.data.Dataset.from_tensor_slices((X_te, y_te))
    .map(preprocess, num_parallel_calls=AUTOTUNE)
    .batch(GLOBAL_BATCH_SIZE)
    .prefetch(AUTOTUNE)
)

# ─────────────────────────────────────────────────────────────────────
# 3. Callback Yapılandırması
# ─────────────────────────────────────────────────────────────────────

callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=10,
                                      restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint(
        "best_model.keras",
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6
    ),
    tf.keras.callbacks.TensorBoard(
        log_dir="./logs", histogram_freq=1, update_freq="epoch"
    ),
    tf.keras.callbacks.CSVLogger("training_log.csv"),
]

# ─────────────────────────────────────────────────────────────────────
# 4. Eğitim (feature extraction aşaması)
# ─────────────────────────────────────────────────────────────────────

print("\nAşama 1: Feature Extraction (base model dondurulmuş)")
history_fe = model.fit(
    train_dataset,
    epochs=10,
    validation_data=test_dataset,
    callbacks=callbacks,
    verbose=1
)

# Fine-tuning: En üst katmanları aç
with strategy.scope():
    base_model.trainable = True
    # Yalnızca son 50 katmanı eğit
    for layer in base_model.layers[:-50]:
        layer.trainable = False
    # Çok daha küçük LR ile fine-tune
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

print("\nAşama 2: Fine-Tuning (son 50 katman açık)")
history_ft = model.fit(
    train_dataset,
    epochs=20,
    validation_data=test_dataset,
    callbacks=callbacks,
    verbose=1
)

# ─────────────────────────────────────────────────────────────────────
# 5. MultiWorkerMirroredStrategy (Çok Makine)
# ─────────────────────────────────────────────────────────────────────

# Her makinede bu ortam değişkeni ayarlanmalı (YAML/JSON):
# TF_CONFIG = {
#   "cluster": {"worker": ["host1:12345", "host2:23456"]},
#   "task": {"type": "worker", "index": 0}   # host1 için 0, host2 için 1
# }
# os.environ["TF_CONFIG"] = json.dumps(TF_CONFIG)
# strategy = tf.distribute.MultiWorkerMirroredStrategy()

print("\nModel başarıyla eğitildi.")
