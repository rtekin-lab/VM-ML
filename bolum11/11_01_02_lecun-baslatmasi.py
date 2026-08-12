# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.1. Derin Ağları Eğitmenin Zorlukları ve Modern Çözümler › 11.1.2. Ağırlık Başlatma Stratejileri › LeCun Başlatması
# Kitap  : Kod 11.2 (LeCun, Glorot ve He başlatmalarının karşılaş)
# Dosya : bolum11/11_01_02_lecun-baslatmasi.py
# Gerekli: pip install matplotlib numpy tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────────────
# Farklı Başlatma Stratejilerinin Aktivasyon Dağılımına Etkisi
# ─────────────────────────────────────────────────────────────────────

np.random.seed(42)
X_sample = np.random.randn(200, 784).astype("float32")

initializers = {
    "zeros":      keras.initializers.Zeros(),
    "random_normal(std=1)": keras.initializers.RandomNormal(stddev=1.0),
    "glorot_normal":        keras.initializers.GlorotNormal(),
    "he_normal":            keras.initializers.HeNormal(),
    "lecun_normal":         keras.initializers.LecunNormal(),
}

fig, axes = plt.subplots(1, len(initializers), figsize=(20, 4))

for ax, (name, init) in zip(axes, initializers.items()):
    # Tek katmanlı model
    layer = keras.layers.Dense(256, activation="relu",
                               kernel_initializer=init)
    out = layer(X_sample)
    ax.hist(out.numpy().flatten(), bins=50, color="steelblue", alpha=0.7)
    ax.set_title(name, fontsize=8)
    ax.set_xlabel("Aktivasyon değeri")
    mean_v = np.mean(np.abs(out.numpy()))
    ax.text(0.05, 0.95, f"Ort.|x|={mean_v:.3f}", transform=ax.transAxes,
            fontsize=8, va="top")

plt.suptitle("Başlatma Stratejisinin Aktivasyon Dağılımına Etkisi (ReLU)",
             fontweight="bold")
plt.tight_layout()
plt.savefig("initialization_comparison.png", dpi=150)
plt.show()

# ─────────────────────────────────────────────────────────────────────
# Model Karşılaştırması: Glorot vs He başlatması
# ─────────────────────────────────────────────────────────────────────

(X_tr, y_tr), (X_te, y_te) = keras.datasets.mnist.load_data()
X_tr = X_tr.reshape(-1, 784).astype("float32") / 255.0
X_te = X_te.reshape(-1, 784).astype("float32") / 255.0

def build_model_with_init(init_name, activation="relu"):
    return keras.Sequential([
        keras.layers.Dense(256, activation=activation,
                           kernel_initializer=init_name, input_shape=(784,)),
        keras.layers.Dense(128, activation=activation,
                           kernel_initializer=init_name),
        keras.layers.Dense(10, activation="softmax")
    ])

configs = [
    ("glorot_normal", "sigmoid"),
    ("glorot_normal", "relu"),
    ("he_normal",     "relu"),
    ("he_normal",     "elu"),
]

for init, act in configs:
    m = build_model_with_init(init, act)
    m.compile("adam", "sparse_categorical_crossentropy", ["accuracy"])
    h = m.fit(X_tr, y_tr, epochs=10, batch_size=128,
              validation_split=0.1, verbose=0)
    _, acc = m.evaluate(X_te, y_te, verbose=0)
    print(f"Init={init:15s}  Act={act:10s}  →  Test Acc: {acc:.4f}")
