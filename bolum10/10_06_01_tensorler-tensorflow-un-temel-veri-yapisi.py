# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.1. Çerçevelere (Frameworks) Giriş: TensorFlow ve Keras Mimarisi › Tensörler: TensorFlow'un Temel Veri Yapısı
# Kitap  : Kod 10.8 (TensorFlow tensörleri ve otomatik türev)
# Dosya : bolum10/10_06_01_tensorler-tensorflow-un-temel-veri-yapisi.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import tensorflow as tf
import numpy as np

# ─────────────────────────────────────────────────────────────────────
# TensorFlow Temel Kavramları
# ─────────────────────────────────────────────────────────────────────

# Sabit Tensör
t1 = tf.constant([[1.0, 2.0], [3.0, 4.0]])
print(f"Şekil: {t1.shape}, Dtype: {t1.dtype}")

# Değişken Tensör (ağırlıklar için)
w = tf.Variable(tf.random.normal([3, 4], stddev=0.1))
print(f"Değişken: {w.shape}")

# Temel operasyonlar
a = tf.constant([1.0, 2.0, 3.0])
b = tf.constant([4.0, 5.0, 6.0])
print(tf.add(a, b))       # [5, 7, 9]
print(tf.reduce_mean(a))   # 2.0
print(tf.matmul(tf.reshape(a,[1,3]), tf.reshape(b,[3,1])))  # [32]

# GPU kullanılabilirliği kontrolü
gpus = tf.config.list_physical_devices("GPU")
print(f"GPU sayısı: {len(gpus)}")

# tf.function ile JIT derleme
@tf.function
def fast_matmul(x, y):
    return tf.matmul(x, y)

x = tf.random.normal([100, 100])
result = fast_matmul(x, tf.transpose(x))
print(f"JIT sonuç şekli: {result.shape}")
