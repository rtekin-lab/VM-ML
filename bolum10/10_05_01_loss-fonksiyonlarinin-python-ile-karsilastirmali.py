# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.5. Ağın Eğitilmesi: Geri Yayılım (Backpropagation) Algoritması › 10.5.1. Hata (Loss) Fonksiyonları › Loss Fonksiyonlarının Python ile Karşılaştırmalı Uygulaması
# Kitap  : Kod 10.5 (Kayıp fonksiyonlarının karşılaştırmalı uygul)
# Dosya : bolum10/10_05_01_loss-fonksiyonlarinin-python-ile-karsilastirmali.py
# Gerekli: pip install matplotlib numpy tensorflow
# ==========================================================================
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

# ─────────────────────────────────────────────────────────────────────
# 1. NumPy ile Kayıp Fonksiyonu Implementasyonu
# ─────────────────────────────────────────────────────────────────────

# Gerçek değerler ve tahminler (basit regresyon örneği)
y_true = np.array([3.0, -0.5, 2.0, 7.0])
y_pred = np.array([2.5,  0.0, 2.0, 8.0])

# MSE hesaplama
mse  = np.mean((y_true - y_pred) ** 2)
mae  = np.mean(np.abs(y_true - y_pred))
rmse = np.sqrt(mse)

print(f"MSE  : {mse:.4f}")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")

# Binary Cross-Entropy (sınıflandırma)
y_true_cls = np.array([1, 0, 1, 1])
y_pred_cls = np.array([0.9, 0.1, 0.8, 0.6])
eps = 1e-9   # log(0) hatası önlemek için
bce = -np.mean(y_true_cls * np.log(y_pred_cls + eps)
               + (1 - y_true_cls) * np.log(1 - y_pred_cls + eps))
print(f"Binary Cross-Entropy: {bce:.4f}")

# ─────────────────────────────────────────────────────────────────────
# 2. Keras ile Loss Karşılaştırması
# ─────────────────────────────────────────────────────────────────────

import tensorflow as tf

y_t = tf.constant([[1.0], [0.0], [1.0], [1.0]])
y_p = tf.constant([[0.9], [0.1], [0.8], [0.6]])

bce_keras = keras.losses.BinaryCrossentropy()(y_t, y_p)
mse_keras = keras.losses.MeanSquaredError()(y_t, y_p)
mae_keras = keras.losses.MeanAbsoluteError()(y_t, y_p)

print(f"Keras BCE : {bce_keras.numpy():.4f}")
print(f"Keras MSE : {mse_keras.numpy():.4f}")
print(f"Keras MAE : {mae_keras.numpy():.4f}")

# ─────────────────────────────────────────────────────────────────────
# 3. Loss Fonksiyonunun Görselleştirilmesi (MSE eğrisi)
# ─────────────────────────────────────────────────────────────────────

y_real = 3.0
predictions = np.linspace(-1, 7, 200)
mse_vals = (y_real - predictions) ** 2
mae_vals = np.abs(y_real - predictions)

plt.figure(figsize=(10, 4))
plt.plot(predictions, mse_vals, "b-", lw=2, label="MSE")
plt.plot(predictions, mae_vals, "r--", lw=2, label="MAE")
plt.axvline(y_real, color="green", ls=":", lw=1.5, label=f"Gerçek değer ({y_real})")
plt.xlabel("Tahmin Değeri"); plt.ylabel("Kayıp (Loss)")
plt.title("MSE vs MAE Kayıp Fonksiyonu Karşılaştırması")
plt.legend(); plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig("loss_comparison.png", dpi=150)
plt.show()
