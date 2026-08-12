# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.1. Derin Ağları Eğitmenin Zorlukları ve Modern Çözümler › 11.1.1. Gradyan Kaybolması ve Patlaması (Vanishing / Exploding Gradients) › Gradyan Akışı Analizi: Python Kodu
# Kitap  : Kod 11.1 (Katman katman gradyan normlarının izlenmesi)
# Dosya : bolum11/11_01_01_gradyan-akisi-analizi-python-kodu.py
# Gerekli: pip install matplotlib numpy tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────────────
# Gradyan Kaybolması Demonstrasyonu: Sigmoid vs ReLU
# ─────────────────────────────────────────────────────────────────────

def build_deep_network(activation, depth=10, units=64):
    """Aktivasyon fonksiyonuna göre derin ağ inşa et."""
    model = keras.Sequential(name=f"deep_{activation}")
    model.add(keras.layers.Input(shape=(20,)))
    for i in range(depth):
        model.add(keras.layers.Dense(
            units,
            activation=activation,
            kernel_initializer="glorot_uniform" if activation=="sigmoid"
                               else "he_normal",
            name=f"layer_{i+1}"
        ))
    model.add(keras.layers.Dense(1, activation="sigmoid"))
    return model

# Rastgele girdi verisi
np.random.seed(42)
X_dummy = np.random.randn(100, 20).astype("float32")
y_dummy = (np.random.rand(100) > 0.5).astype("float32")

gradient_norms = {}

for act in ["sigmoid", "relu", "elu"]:
    model = build_deep_network(act)
    model.compile(loss="binary_crossentropy", optimizer="adam")

    with tf.GradientTape() as tape:
        y_pred = model(X_dummy[:10], training=True)
        loss = keras.losses.binary_crossentropy(
            y_dummy[:10].reshape(-1,1), y_pred)
        loss = tf.reduce_mean(loss)

    # Tüm katmanlar için gradyanları hesapla
    grads = tape.gradient(loss, model.trainable_variables)
    norms = [tf.norm(g).numpy() for g in grads if g is not None]
    gradient_norms[act] = norms
    print(f"\n{act.upper():10s} aktivasyonu – Katman gradyan normları:")
    for i, n in enumerate(norms[::2]):   # Yalnızca ağırlık gradyanları
        print(f"  Katman {i+1:2d}: {n:.2e}")

# ─────────────────────────────────────────────────────────────────────
# Gradient Clipping Uygulaması
# ─────────────────────────────────────────────────────────────────────

model_clip = build_deep_network("relu")

# clipnorm: gradyan normu 1.0'ı aşarsa kırp
# clipvalue: her gradyan elemanını [-0.5, 0.5] aralığına sıkıştır
optimizer_clip = keras.optimizers.Adam(
    learning_rate=0.001,
    clipnorm=1.0          # Önerilen yöntem
    # clipvalue=0.5       # Alternatif yöntem
)

model_clip.compile(
    optimizer=optimizer_clip,
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
print("\nGradient clipping aktif Adam optimizer hazır.")

# ─────────────────────────────────────────────────────────────────────
# Residual Bağlantı: Sıfırdan Implementasyon
# ─────────────────────────────────────────────────────────────────────

def residual_block(inputs, units, name_prefix):
    """Temel residual blok: F(x) + x"""
    x = keras.layers.Dense(units, activation="relu",
                           kernel_initializer="he_normal",
                           name=f"{name_prefix}_dense1")(inputs)
    x = keras.layers.BatchNormalization(name=f"{name_prefix}_bn1")(x)
    x = keras.layers.Dense(units, activation=None,
                           kernel_initializer="he_normal",
                           name=f"{name_prefix}_dense2")(x)
    x = keras.layers.BatchNormalization(name=f"{name_prefix}_bn2")(x)
    # Skip connection: boyut eşleştirme gerekirse projection ekle
    if inputs.shape[-1] != units:
        inputs = keras.layers.Dense(units, use_bias=False,
                                    name=f"{name_prefix}_proj")(inputs)
    x = keras.layers.Add(name=f"{name_prefix}_add")([x, inputs])
    x = keras.layers.Activation("relu", name=f"{name_prefix}_relu")(x)
    return x

# Residual mimari
inputs = keras.Input(shape=(784,), name="giris")
x = keras.layers.Dense(256, activation="relu",
                        kernel_initializer="he_normal")(inputs)
x = residual_block(x, 256, "res1")
x = residual_block(x, 256, "res2")
x = residual_block(x, 128, "res3")   # boyut küçülür; projection eklenir
outputs = keras.layers.Dense(10, activation="softmax")(x)

res_model = keras.Model(inputs, outputs, name="ResidualMLP")
res_model.summary()
