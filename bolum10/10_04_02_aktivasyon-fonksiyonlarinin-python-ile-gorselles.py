# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.4. Aktivasyon Fonksiyonları: Ağa Doğrusal Olmayanlık Kazandırma › 10.4.2. Temel Aktivasyon Fonksiyonları: Denklemler, Türevler ve Kullanım Alanları › Aktivasyon Fonksiyonlarının Python ile Görselleştirilmesi ve Karşılaştırılması
# Kitap  : Kod 10.3 (Aktivasyon fonksiyonlarının ve türevlerinin )
# Dosya : bolum10/10_04_02_aktivasyon-fonksiyonlarinin-python-ile-gorselles.py
# Gerekli: pip install matplotlib numpy scikit-learn tensorflow
# ==========================================================================
import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────
# Aktivasyon Fonksiyonlarının NumPy Implementasyonu
# ─────────────────────────────────────────────────────────

z = np.linspace(-6, 6, 300)

# 1. Sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_deriv(z):
    s = sigmoid(z)
    return s * (1 - s)

# 2. Tanh
def tanh(z):
    return np.tanh(z)

def tanh_deriv(z):
    return 1 - np.tanh(z)**2

# 3. ReLU
def relu(z):
    return np.maximum(0, z)

def relu_deriv(z):
    return (z > 0).astype(float)

# 4. Leaky ReLU
def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

# 5. ELU
def elu(z, alpha=1.0):
    return np.where(z > 0, z, alpha * (np.exp(z) - 1))

# 6. Softmax (vektör için)
def softmax(z):
    exp_z = np.exp(z - np.max(z))  # sayısal kararlılık için
    return exp_z / exp_z.sum()

# ─────────────────────────────────────────────────────────
# Görselleştirme
# ─────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
fig.suptitle("Aktivasyon Fonksiyonları Karşılaştırması", fontsize=14, fontweight="bold")

functions = [
    ("Sigmoid", sigmoid, sigmoid_deriv, "blue"),
    ("Tanh", tanh, tanh_deriv, "green"),
    ("ReLU", relu, relu_deriv, "red"),
    ("Leaky ReLU (α=0.01)", leaky_relu, None, "orange"),
    ("ELU (α=1.0)", elu, None, "purple"),
]

for bos in axes.flat[len(functions):]:
    bos.set_visible(False)          # 5 fonksiyon, 6 panel: kullanilmayani gizle

for ax, (name, func, deriv, color) in zip(axes.flat, functions):
    ax.plot(z, func(z), color=color, lw=2, label=name)
    if deriv is not None:
        ax.plot(z, deriv(z), color=color, lw=1.5, ls="--", alpha=0.6, label=f"{name} Türev")
    ax.axhline(0, color="black", lw=0.5)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_title(name, fontweight="bold")
    ax.set_xlabel("z"); ax.set_ylabel("Aktivasyon")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("aktivasyon_fonksiyonlari.png", dpi=150)
plt.show()

# ─────────────────────────────────────────────────────────
# Keras'ta Aktivasyon Fonksiyonlarını Karşılaştırma
# ─────────────────────────────────────────────────────────

import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=2000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

results = {}

for activation in ["sigmoid", "tanh", "relu", "elu", "selu"]:
    model = keras.Sequential([
        keras.layers.Dense(64, activation=activation, input_shape=(20,)),
        keras.layers.Dense(32, activation=activation),
        keras.layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    history = model.fit(X_train, y_train, epochs=30, verbose=0,
                        validation_data=(X_test, y_test))
    val_acc = max(history.history["val_accuracy"])
    results[activation] = val_acc
    print(f"{activation:10s}  → En iyi doğrulama doğruluğu: {val_acc:.4f}")
