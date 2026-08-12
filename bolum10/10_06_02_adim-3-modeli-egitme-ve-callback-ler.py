# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.2. Sıralı (Sequential) API ile Model İnşası, Derleme ve Eğitim › Adım 3: Modeli Eğitme (model.fit) ve Callback'ler
# Kitap  : Kod 10.11 (Geri çağrılarla (callback) eğitim sürecinin )
# Dosya : bolum10/10_06_02_adim-3-modeli-egitme-ve-callback-ler.py
# ==========================================================================
# ─────────────────────────────────────────────────────────────────────
# Callback'ler: Eğitim Sürecini Yönetme
# ─────────────────────────────────────────────────────────────────────
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum10/10_06_02_adim-2-*
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 784).astype("float32") / 255.0
X_test  = X_test.reshape(-1, 784).astype("float32") / 255.0
model = keras.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

import os

# 1. Early Stopping: Aşırı uyum başladığında eğitimi durdur
early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",   # Doğrulama kaybını izle
    patience=5,           # 5 epoch iyileşme yoksa dur
    restore_best_weights=True,  # En iyi ağırlıklara geri dön
    verbose=1
)

# 2. ModelCheckpoint: En iyi modeli diske kaydet
checkpoint = keras.callbacks.ModelCheckpoint(
    filepath="best_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

# 3. ReduceLROnPlateau: Öğrenme oranını otomatik azalt
reduce_lr = keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=3,
    min_lr=1e-6,
    verbose=1
)

# 4. TensorBoard: Eğitimi görselleştir
tensorboard = keras.callbacks.TensorBoard(
    log_dir="./logs",
    histogram_freq=1,     # Her epoch sonunda ağırlık histogramı
    write_graph=True
)

# 5. CSV Logger: Eğitim metriklerini dosyaya yaz
csv_logger = keras.callbacks.CSVLogger("training_log.csv")

# ─────────────────────────────────────────────────────────────────────
# model.fit(): Tüm Parametrelerle
# ─────────────────────────────────────────────────────────────────────

history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=64,
    validation_split=0.15,    # %15'i doğrulama için ayır
    # validation_data=(X_val, y_val),  # Alternatif: hazır val seti
    callbacks=[early_stop, checkpoint, reduce_lr, csv_logger],
    shuffle=True,             # Her epoch'ta veriyi karıştır
    verbose=1                 # 0=sessiz, 1=progress bar, 2=epoch özeti
)

print(f"Eğitim tamamlandı. Toplam epoch: {len(history.history['loss'])}")
