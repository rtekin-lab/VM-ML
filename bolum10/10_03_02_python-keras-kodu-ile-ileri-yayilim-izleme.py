# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.3. Çok Katmanlı Algılayıcılar (Multi-Layer Perceptrons – MLP) › 10.3.2. İleri Yayılım (Forward Propagation): Matris Çarpımı ile Verimli Hesaplama › Python / Keras Kodu ile İleri Yayılım İzleme
# Kitap  : Kod 10.2 (Keras ile ileri yayılımın katman katman izle)
# Dosya : bolum10/10_03_02_python-keras-kodu-ile-ileri-yayilim-izleme.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras

# ─────────────────────────────────────────────────────────
# İleri Yayılım: NumPy ile El ile Hesaplama
# ─────────────────────────────────────────────────────────

# ReLU aktivasyon fonksiyonu
def relu(z):
    return np.maximum(0, z)

# Softmax aktivasyon fonksiyonu (sayısal kararlılık için)
def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / exp_z.sum(axis=1, keepdims=True)

# Örnek veri: 3 örnek, 4 öznitelik
X = np.random.randn(3, 4)

# Ağırlık matrisleri ve bias vektörleri (rastgele başlatma)
W1 = np.random.randn(4, 5) * 0.01   # Gizli katman: 5 nöron
b1 = np.zeros((1, 5))
W2 = np.random.randn(5, 3) * 0.01   # Çıkış katmanı: 3 sınıf
b2 = np.zeros((1, 3))

# İleri yayılım (Forward Propagation)
Z1 = X @ W1 + b1          # Doğrusal dönüşüm: [3x4] @ [4x5] = [3x5]
H1 = relu(Z1)              # ReLU aktivasyonu
print(f"Gizli katman çıktısı: {H1.shape}")   # (3, 5)

Z2 = H1 @ W2 + b2          # Çıkış katmanı: [3x5] @ [5x3] = [3x3]
y_hat = softmax(Z2)        # Softmax ile olasılık dağılımı
print(f"Çıkış (olasılık): {y_hat.shape}")     # (3, 3)
print(f"Her örnek için sınıf olasılıkları:\n{np.round(y_hat, 3)}")

# ─────────────────────────────────────────────────────────
# Keras ile Aynı Mimari: Model Özeti ve Boyut Analizi
# ─────────────────────────────────────────────────────────

model = keras.Sequential([
    keras.layers.Dense(5, activation="relu", input_shape=(4,)),
    keras.layers.Dense(3, activation="softmax")
])

model.summary()

# Keras ile ileri yayılım (predict)
sample = np.random.randn(1, 4)
prediction = model.predict(sample)
print(f"\nModel tahmini: {prediction}")
