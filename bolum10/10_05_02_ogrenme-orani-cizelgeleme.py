# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.5. Ağın Eğitilmesi: Geri Yayılım (Backpropagation) Algoritması › 10.5.2. Gradyan İnişi (Gradient Descent): Hata Yüzeyinde Optimizasyon › Öğrenme Oranı Çizelgeleme (Learning Rate Scheduling)
# Kitap  : Kod 10.6 (Öğrenme oranı çizelgeleme stratejileri)
# Dosya : bolum10/10_05_02_ogrenme-orani-cizelgeleme.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras

# ─────────────────────────────────────────────────────────────────────
# Gradyan İnişi: NumPy ile El ile Lojistik Regresyon Eğitimi
# ─────────────────────────────────────────────────────────────────────

np.random.seed(42)
X = np.random.randn(100, 2)
y = (X[:, 0] + X[:, 1] > 0).astype(float)

# Parametreler
w = np.zeros(2)
b = 0.0
lr = 0.1
epochs = 50

def sigmoid(z): return 1 / (1 + np.exp(-z))

loss_history = []
for epoch in range(epochs):
    # İleri yayılım
    z = X @ w + b
    y_hat = sigmoid(z)
    loss = -np.mean(y * np.log(y_hat + 1e-9) + (1-y)*np.log(1-y_hat+1e-9))
    loss_history.append(loss)
    # Gradyanlar
    delta = y_hat - y
    dw = X.T @ delta / len(y)
    db = delta.mean()
    # Güncelleme
    w -= lr * dw
    b -= lr * db
    if epoch % 10 == 0:
        print(f"Epoch {epoch:3d} | Loss: {loss:.4f}")

# ─────────────────────────────────────────────────────────────────────
# Keras Optimizör Karşılaştırması
# ─────────────────────────────────────────────────────────────────────

(X_tr, y_tr), (X_te, y_te) = keras.datasets.mnist.load_data()
X_tr = X_tr.reshape(-1, 784).astype("float32") / 255.0
X_te = X_te.reshape(-1, 784).astype("float32") / 255.0

def build_model(optimizer):
    m = keras.Sequential([
        keras.layers.Dense(128, activation="relu", input_shape=(784,),
                           kernel_initializer="he_normal"),
        keras.layers.Dense(64, activation="relu",
                           kernel_initializer="he_normal"),
        keras.layers.Dense(10, activation="softmax")
    ])
    m.compile(optimizer=optimizer,
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
    return m

optimizers = {
    "SGD(lr=0.01)":           keras.optimizers.SGD(learning_rate=0.01),
    "SGD+Momentum":           keras.optimizers.SGD(learning_rate=0.01, momentum=0.9),
    "Adam(lr=0.001)":         keras.optimizers.Adam(learning_rate=0.001),
    "RMSprop":                keras.optimizers.RMSprop(learning_rate=0.001),
}

for name, opt in optimizers.items():
    model = build_model(opt)
    history = model.fit(X_tr, y_tr, epochs=10, batch_size=64,
                        validation_split=0.1, verbose=0)
    _, acc = model.evaluate(X_te, y_te, verbose=0)
    print(f"{name:30s} → Test Acc: {acc:.4f}")

# ─────────────────────────────────────────────────────────────────────
# Öğrenme Oranı Çizelgeleme (ReduceLROnPlateau)
# ─────────────────────────────────────────────────────────────────────

model = build_model(keras.optimizers.Adam(learning_rate=0.001))

lr_scheduler = keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,       # LR yi yarıya indir
    patience=3,       # 3 epoch ilerleme olmazsa tetikle
    min_lr=1e-6,
    verbose=1
)

history = model.fit(
    X_tr, y_tr,
    epochs=30,
    batch_size=64,
    validation_split=0.1,
    callbacks=[lr_scheduler],
    verbose=1
)
