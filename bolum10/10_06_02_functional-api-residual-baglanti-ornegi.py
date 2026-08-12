# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.2. Sıralı (Sequential) API ile Model İnşası, Derleme ve Eğitim › Functional API: Residual Bağlantı Örneği
# Kitap  : Kod 10.12 (Functional API ile atlamalı (residual) bağla)
# Dosya : bolum10/10_06_02_functional-api-residual-baglanti-ornegi.py
# ==========================================================================
# ─────────────────────────────────────────────────────────────────────
# Functional API: Residual (Skip) Bağlantı ile MLP
# ─────────────────────────────────────────────────────────────────────

# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum10/10_06_02_adim-1-*
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

inputs = keras.Input(shape=(784,), name="giris")

# Ana yol
x = layers.Dense(256, activation="relu", kernel_initializer="he_normal")(inputs)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)

# Residual blok: kısa yol (skip connection)
residual = layers.Dense(128)(x)           # boyut eşleştirmesi
x = layers.Dense(128, activation="relu", kernel_initializer="he_normal")(x)
x = layers.BatchNormalization()(x)
x = layers.Add()([x, residual])           # Ana yol + kısa yol
x = layers.Activation("relu")(x)

# İkinci residual blok
residual2 = x
x = layers.Dense(128, activation="relu")(x)
x = layers.Add()([x, residual2])
x = layers.Activation("relu")(x)

outputs = layers.Dense(10, activation="softmax")(x)

residual_model = keras.Model(inputs=inputs, outputs=outputs, name="residual_mlp")
residual_model.summary()
residual_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                       metrics=["accuracy"])
