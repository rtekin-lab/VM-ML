# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.2. Gelişmiş Optimizasyon ve Aşırı Öğrenmeyi (Overfitting) Önleme › 11.2.1. Hızlı Optimizörler: Momentum'dan Adam'a › Adam Varyantları
# Kitap  : Kod 11.4 (Adam varyantlarının karşılaştırması)
# Dosya : bolum11/11_02_01_adam-varyantlari.py
# Gerekli: pip install matplotlib numpy tensorflow
# ==========================================================================
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────────────
# Optimizör Karşılaştırması: SGD, Momentum, Adam, AdamW
# ─────────────────────────────────────────────────────────────────────

(X_tr, y_tr), (X_te, y_te) = keras.datasets.mnist.load_data()
X_tr = X_tr.reshape(-1, 784).astype("float32") / 255.0
X_te = X_te.reshape(-1, 784).astype("float32") / 255.0

def build_model():
    return keras.Sequential([
        keras.layers.Dense(256, activation="relu",
                           kernel_initializer="he_normal", input_shape=(784,)),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(128, activation="relu",
                           kernel_initializer="he_normal"),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(10, activation="softmax")
    ])

optimizers = {
    "SGD(lr=0.01)":           keras.optimizers.SGD(learning_rate=0.01),
    "SGD+Momentum(0.9)":      keras.optimizers.SGD(learning_rate=0.01, momentum=0.9),
    "SGD+Nesterov":           keras.optimizers.SGD(learning_rate=0.01, momentum=0.9,
                                                   nesterov=True),
    "RMSprop(lr=0.001)":      keras.optimizers.RMSprop(learning_rate=0.001),
    "Adam(lr=0.001)":         keras.optimizers.Adam(learning_rate=0.001),
    "AdamW(lr=0.001)":        keras.optimizers.AdamW(learning_rate=0.001,
                                                      weight_decay=0.01),
    "Nadam(lr=0.001)":        keras.optimizers.Nadam(learning_rate=0.001),
}

histories = {}
for name, opt in optimizers.items():
    model = build_model()
    model.compile(optimizer=opt,
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    h = model.fit(X_tr, y_tr, epochs=15, batch_size=128,
                  validation_split=0.1, verbose=0)
    _, test_acc = model.evaluate(X_te, y_te, verbose=0)
    histories[name] = h.history["val_accuracy"]
    print(f"{name:30s} → Test Acc: {test_acc:.4f}")

# Yakınsama grafikleri
plt.figure(figsize=(12, 5))
for name, val_acc in histories.items():
    plt.plot(val_acc, label=name, lw=2)
plt.xlabel("Epoch"); plt.ylabel("Doğrulama Doğruluğu")
plt.title("Optimizör Karşılaştırması (MNIST)", fontweight="bold")
plt.legend(fontsize=8); plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig("optimizer_comparison.png", dpi=150)
plt.show()

# ─────────────────────────────────────────────────────────────────────
# Öğrenme Oranı Bulucu (LR Range Test)
# ─────────────────────────────────────────────────────────────────────

# LR Range Test: En uygun learning rate aralığını bul
model = build_model()

# Üstel LR zamanlayıcı: 0.00001'den 1.0'a kadar
import math
lr_finder_epochs = 30
lr_start, lr_end = 1e-5, 1.0

lr_schedule = keras.callbacks.LearningRateScheduler(
    lambda epoch: lr_start * (lr_end/lr_start) ** (epoch/lr_finder_epochs)
)

model.compile(
    optimizer=keras.optimizers.SGD(learning_rate=lr_start),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history_lr = model.fit(
    X_tr[:10000], y_tr[:10000],
    epochs=lr_finder_epochs,
    batch_size=128,
    callbacks=[lr_schedule],
    verbose=0
)

# Loss'un en hızlı düştüğü LR değeri optimal öğrenme oranına işaret eder
lrs = [lr_start * (lr_end/lr_start)**(e/lr_finder_epochs)
       for e in range(lr_finder_epochs)]
plt.figure(figsize=(8,4))
plt.semilogx(lrs, history_lr.history["loss"], lw=2)
plt.xlabel("Öğrenme Oranı (log ölçek)"); plt.ylabel("Loss")
plt.title("LR Range Test", fontweight="bold")
plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()
