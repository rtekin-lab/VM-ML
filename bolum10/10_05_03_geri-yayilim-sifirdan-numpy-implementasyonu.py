# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.5. Ağın Eğitilmesi: Geri Yayılım (Backpropagation) Algoritması › 10.5.3. Geri Yayılım Matematiği: Zincir Kuralı ile Gradyan Akışı › Geri Yayılım: Sıfırdan NumPy Implementasyonu
# Kitap  : Kod 10.7 (Geri yayılımın sıfırdan kodlanması: XOR prob)
# Dosya : bolum10/10_05_03_geri-yayilim-sifirdan-numpy-implementasyonu.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np

# ─────────────────────────────────────────────────────────────────────
# Tam Geri Yayılım: XOR Problemini Çözen 2-Katmanlı MLP
# ─────────────────────────────────────────────────────────────────────

np.random.seed(0)

# XOR veri seti
X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
y = np.array([[0],[1],[1],[0]], dtype=float)

# Ağırlık başlatma (He benzeri)
W1 = np.random.randn(2, 4) * 0.5
b1 = np.zeros((1, 4))
W2 = np.random.randn(4, 1) * 0.5
b2 = np.zeros((1, 1))

def sigmoid(z): return 1 / (1 + np.exp(-z))
def sig_deriv(z): s = sigmoid(z); return s * (1 - s)

lr = 0.5
loss_log = []

for epoch in range(5000):
    # ─── İLERİ YAYILIM ───────────────────────────────────────────────
    Z1   = X @ W1 + b1
    H1   = sigmoid(Z1)
    Z2   = H1 @ W2 + b2
    y_hat = sigmoid(Z2)

    # ─── KAYIP ───────────────────────────────────────────────────────
    loss = np.mean((y - y_hat) ** 2)
    loss_log.append(loss)

    # ─── GERİ YAYILIM ────────────────────────────────────────────────
    # Çıkış katmanı delta (∂L/∂z2)
    dL_dyhat = -2 * (y - y_hat) / len(y)        # ∂L/∂ŷ
    dyhat_dZ2 = sig_deriv(Z2)                    # ∂ŷ/∂z2
    delta2 = dL_dyhat * dyhat_dZ2               # [n x 1]

    # W2 ve b2 gradyanları
    dW2 = H1.T @ delta2                          # [4 x 1]
    db2 = delta2.sum(axis=0, keepdims=True)

    # Gizli katman delta (∂L/∂z1)
    dH1   = delta2 @ W2.T                        # [n x 4]
    delta1 = dH1 * sig_deriv(Z1)                 # [n x 4]

    # W1 ve b1 gradyanları
    dW1 = X.T @ delta1                           # [2 x 4]
    db1 = delta1.sum(axis=0, keepdims=True)

    # ─── AĞIRLIK GÜNCELLEMESİ ────────────────────────────────────────
    W2 -= lr * dW2;  b2 -= lr * db2
    W1 -= lr * dW1;  b1 -= lr * db1

    if epoch % 1000 == 0:
        print(f"Epoch {epoch:5d} | MSE Loss: {loss:.5f}")

print("\nTahminler:")
print(np.round(y_hat, 3))
# Beklenen: [[0],[1],[1],[0]]

# ─────────────────────────────────────────────────────────────────────
# TensorFlow GradientTape ile Aynı İşlem (Otomatik Türev)
# ─────────────────────────────────────────────────────────────────────

import tensorflow as tf

X_tf = tf.constant(X, dtype=tf.float32)
y_tf = tf.constant(y, dtype=tf.float32)

W1_tf = tf.Variable(tf.random.normal([2, 4], seed=0) * 0.5)
b1_tf = tf.Variable(tf.zeros([1, 4]))
W2_tf = tf.Variable(tf.random.normal([4, 1], seed=0) * 0.5)
b2_tf = tf.Variable(tf.zeros([1, 1]))

optimizer = tf.keras.optimizers.Adam(learning_rate=0.05)

for epoch in range(500):
    with tf.GradientTape() as tape:
        H1 = tf.sigmoid(X_tf @ W1_tf + b1_tf)
        yhat = tf.sigmoid(H1 @ W2_tf + b2_tf)
        loss = tf.reduce_mean((y_tf - yhat) ** 2)
    grads = tape.gradient(loss, [W1_tf, b1_tf, W2_tf, b2_tf])
    optimizer.apply_gradients(zip(grads, [W1_tf, b1_tf, W2_tf, b2_tf]))
    if epoch % 100 == 0:
        print(f"Epoch {epoch:4d} | Loss: {loss.numpy():.5f}")
