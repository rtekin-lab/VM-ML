# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.4. Aktivasyon Fonksiyonları: Ağa Doğrusal Olmayanlık Kazandırma › Kapsamlı Uygulama: MLP Mimarisi ve Aktivasyon Fonksiyonu Optimizasyonu
# Kitap  : Kod 10.4 (MLP mimarisi ve aktivasyon fonksiyonu seçimi)
# Dosya : bolum10/10_04_kapsamli-uygulama-mlp-mimarisi-ve-aktivasyon-fon.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================
import tensorflow as tf
from tensorflow import keras
import numpy as np

# ─────────────────────────────────────────────────────────
# Aktivasyon Fonksiyonu Seçimi ile MLP Kurma
# (MNIST Veri Seti Üzerinde)
# ─────────────────────────────────────────────────────────

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

# Normalizasyon: 0-255 → 0-1, düzleştirme: 28x28 → 784
X_train = X_train.reshape(-1, 784).astype("float32") / 255.0
X_test  = X_test.reshape(-1, 784).astype("float32") / 255.0

# ─── Model 1: Sigmoid (Kötü Örnek - Gizli Katmanlar) ────
model_sigmoid = keras.Sequential([
    keras.layers.Dense(256, activation="sigmoid", input_shape=(784,),
                       kernel_initializer="glorot_uniform"),
    keras.layers.Dense(128, activation="sigmoid"),
    keras.layers.Dense(10,  activation="softmax")
], name="sigmoid_model")

# ─── Model 2: ReLU + He Başlatması (İyi Örnek) ───────────
model_relu = keras.Sequential([
    keras.layers.Dense(256, activation="relu", input_shape=(784,),
                       kernel_initializer="he_normal"),
    keras.layers.Dense(128, activation="relu",
                       kernel_initializer="he_normal"),
    keras.layers.Dense(10,  activation="softmax")
], name="relu_model")

# ─── Model 3: Modern - ELU + BatchNorm ───────────────────
model_elu = keras.Sequential([
    keras.layers.Dense(256, activation="elu", input_shape=(784,),
                       kernel_initializer="lecun_normal"),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(128, activation="elu",
                       kernel_initializer="lecun_normal"),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(10,  activation="softmax")
], name="elu_batchnorm_model")

# Hepsini Derle ve Eğit
for model in [model_sigmoid, model_relu, model_elu]:
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    history = model.fit(
        X_train, y_train,
        epochs=15,
        batch_size=64,
        validation_split=0.1,
        verbose=0
    )
    _, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"{model.name:25s} → Test Doğruluğu: {test_acc:.4f}")

# Örnek çıktı (yaklaşık):
# sigmoid_model          → Test Doğruluğu: 0.9612
# relu_model             → Test Doğruluğu: 0.9781
# elu_batchnorm_model    → Test Doğruluğu: 0.9821
