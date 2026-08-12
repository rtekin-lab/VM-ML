# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.2. Gelişmiş Optimizasyon ve Aşırı Öğrenmeyi (Overfitting) Önleme › 11.2.2. Düzenlileştirme (Regularization) Teknikleri › 5. Monte Carlo Dropout (MC Dropout)
# Kitap  : Kod 11.5 (Monte Carlo Dropout ile belirsizlik kestirim)
# Dosya : bolum11/11_02_02_monte-carlo-dropout.py
# Gerekli: pip install matplotlib numpy tensorflow
# ==========================================================================
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────────────
# L1, L2, Dropout ve Early Stopping: Kapsamlı Karşılaştırma
# ─────────────────────────────────────────────────────────────────────

(X_tr, y_tr), (X_te, y_te) = keras.datasets.mnist.load_data()
X_tr = X_tr.reshape(-1, 784).astype("float32") / 255.0
X_te = X_te.reshape(-1, 784).astype("float32") / 255.0

# Kasıtlı küçük veri seti (overfitting yaratmak için)
X_small, y_small = X_tr[:500], y_tr[:500]

def build_regularized_model(reg_type="none", dropout_rate=0.0):
    """Farklı regularization stratejileriyle model inşa et."""
    if reg_type == "l2":
        reg = keras.regularizers.L2(0.001)
    elif reg_type == "l1":
        reg = keras.regularizers.L1(0.001)
    elif reg_type == "l1_l2":
        reg = keras.regularizers.L1L2(l1=0.0001, l2=0.001)
    else:
        reg = None

    layers = [
        keras.layers.Dense(512, activation="relu",
                           kernel_initializer="he_normal",
                           kernel_regularizer=reg, input_shape=(784,)),
        keras.layers.Dense(256, activation="relu",
                           kernel_initializer="he_normal",
                           kernel_regularizer=reg),
    ]

    if dropout_rate > 0:
        layers.insert(1, keras.layers.Dropout(dropout_rate))
        layers.append(keras.layers.Dropout(dropout_rate))

    layers.append(keras.layers.Dense(10, activation="softmax"))
    return keras.Sequential(layers)

configs = [
    ("No Reg",             "none",  0.0),
    ("L2 (λ=0.001)",       "l2",    0.0),
    ("L1 (λ=0.001)",       "l1",    0.0),
    ("Dropout (p=0.3)",    "none",  0.3),
    ("Dropout (p=0.5)",    "none",  0.5),
    ("L2 + Dropout(0.3)",  "l2",    0.3),
]

results = {}
for name, reg, dr in configs:
    model = build_regularized_model(reg, dr)
    model.compile(
        optimizer=keras.optimizers.Adam(0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    h = model.fit(X_small, y_small, epochs=50, batch_size=32,
                  validation_data=(X_te, y_te), verbose=0)
    tr_acc  = max(h.history["accuracy"])
    val_acc = max(h.history["val_accuracy"])
    gap = tr_acc - val_acc
    results[name] = (tr_acc, val_acc, gap)
    print(f"{name:25s}  Train: {tr_acc:.3f}  Val: {val_acc:.3f}  Gap: {gap:.3f}")

# Karşılaştırma: En küçük gap = en az overfitting
print("\n→ Gap küçüldükçe overfitting azalıyor.")

# ─────────────────────────────────────────────────────────────────────
# Early Stopping: Detaylı Kullanım
# ─────────────────────────────────────────────────────────────────────

model_es = build_regularized_model("l2", 0.3)
model_es.compile("adam", "sparse_categorical_crossentropy", ["accuracy"])

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=10,
        min_delta=0.001,
        restore_best_weights=True,   # ← KRİTİK: En iyi ağırlıklara dön
        verbose=1
    ),
    keras.callbacks.ModelCheckpoint(
        "best_model.keras",
        monitor="val_accuracy",
        save_best_only=True
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1
    ),
]

history = model_es.fit(
    X_tr, y_tr,
    epochs=100,
    batch_size=64,
    validation_split=0.15,
    callbacks=callbacks,
    verbose=1
)

print(f"\nEğitim {len(history.history['loss'])} epoch'ta durdu.")
print(f"En iyi val_loss: {min(history.history['val_loss']):.4f}")

# ─────────────────────────────────────────────────────────────────────
# Veri Artırma (Data Augmentation) ile Eğitim
# ─────────────────────────────────────────────────────────────────────

(X_tr_img, y_tr_img), (X_te_img, y_te_img) = keras.datasets.cifar10.load_data()
X_tr_img = X_tr_img.astype("float32") / 255.0
X_te_img = X_te_img.astype("float32") / 255.0

# Keras Preprocessing katmanları ile gerçek zamanlı augmentation
data_augmentation = keras.Sequential([
    keras.layers.RandomFlip("horizontal"),
    keras.layers.RandomRotation(0.1),          # ±10% döndürme
    keras.layers.RandomZoom(0.1),              # ±10% zoom
    keras.layers.RandomTranslation(0.1, 0.1), # Kaydırma
    keras.layers.RandomBrightness(0.2),        # Parlaklık değişimi
    keras.layers.RandomContrast(0.1),          # Kontrast değişimi
], name="augmentation")

# CNN modeli (augmentation dahil)
cnn_inputs = keras.Input(shape=(32, 32, 3))
x = data_augmentation(cnn_inputs, training=True)  # Yalnızca eğitimde aktif
x = keras.layers.Conv2D(32, 3, padding="same", activation="relu")(x)
x = keras.layers.MaxPooling2D()(x)
x = keras.layers.Conv2D(64, 3, padding="same", activation="relu")(x)
x = keras.layers.MaxPooling2D()(x)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(0.5)(x)
cnn_outputs = keras.layers.Dense(10, activation="softmax")(x)

cnn_aug = keras.Model(cnn_inputs, cnn_outputs)
cnn_aug.compile("adam", "sparse_categorical_crossentropy", ["accuracy"])
print("CNN + Augmentation modeli hazır:", cnn_aug.input_shape)

# ─────────────────────────────────────────────────────────────────────
# Monte Carlo Dropout: Belirsizlik Tahmini
# ─────────────────────────────────────────────────────────────────────

# MC Dropout: Çıkarım sırasında Dropout aktif tut
model_mc = keras.Sequential([
    keras.layers.Dense(256, activation="relu", input_shape=(784,)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(10, activation="softmax")
])
model_mc.compile("adam", "sparse_categorical_crossentropy", ["accuracy"])
model_mc.fit(X_tr, y_tr, epochs=5, verbose=0)

# MC Dropout ile belirsizlik tahmini
test_sample = X_te[:1]
n_samples = 100

# training=True ile dropout aktif
mc_predictions = np.stack([
    model_mc(test_sample, training=True).numpy() for _ in range(n_samples)
])

mean_pred = mc_predictions.mean(axis=0)
std_pred  = mc_predictions.std(axis=0)

predicted_class = np.argmax(mean_pred)
confidence = mean_pred[0, predicted_class]
uncertainty = std_pred[0, predicted_class]

print(f"\nMC Dropout ({n_samples} örnek):")
print(f"  Tahmin edilen sınıf: {predicted_class}")
print(f"  Ortalama güven    : {confidence:.4f}")
print(f"  Belirsizlik (std) : {uncertainty:.4f}")
