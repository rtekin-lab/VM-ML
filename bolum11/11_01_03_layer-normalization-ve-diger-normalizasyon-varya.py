# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.1. Derin Ağları Eğitmenin Zorlukları ve Modern Çözümler › 11.1.3. Toplu Normalleştirme (Batch Normalization) › Layer Normalization ve Diğer Normalizasyon Varyantları
# Kitap  : Kod 11.3 (Layer Normalization ve diğer normalleştirme )
# Dosya : bolum11/11_01_03_layer-normalization-ve-diger-normalizasyon-varya.py
# Gerekli: pip install tensorflow
# ==========================================================================
import tensorflow as tf
from tensorflow import keras

# ─────────────────────────────────────────────────────────────────────
# Batch Normalization Uygulaması: Doğru Kullanım
# ─────────────────────────────────────────────────────────────────────

# Yöntem 1: Orijinal kağıt sırası (Dense → BN → Activation)
model_bn = keras.Sequential([
    keras.layers.Input(shape=(784,)),
    # BN kullandığında Dense'de bias gerekmez (BN beta parametresi bias görevi görür)
    keras.layers.Dense(300, use_bias=False, kernel_initializer="he_normal"),
    keras.layers.BatchNormalization(),
    keras.layers.Activation("relu"),

    keras.layers.Dense(200, use_bias=False, kernel_initializer="he_normal"),
    keras.layers.BatchNormalization(),
    keras.layers.Activation("relu"),

    keras.layers.Dense(100, use_bias=False, kernel_initializer="he_normal"),
    keras.layers.BatchNormalization(),
    keras.layers.Activation("relu"),

    keras.layers.Dense(10, activation="softmax")
], name="BN_Model")

model_bn.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),  # BN ile daha yüksek LR
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# BN parametrelerini incele
bn_layer = model_bn.layers[2]   # İlk BN katmanı
print(f"BN parametreleri: {bn_layer.count_params()}")
print(f"  gamma (ölçek) : {bn_layer.gamma.shape}")
print(f"  beta (kaydırma): {bn_layer.beta.shape}")
print(f"  moving_mean    : {bn_layer.moving_mean.shape}")
print(f"  moving_variance: {bn_layer.moving_variance.shape}")

# ─────────────────────────────────────────────────────────────────────
# Layer Normalization (Transformer için)
# ─────────────────────────────────────────────────────────────────────

model_ln = keras.Sequential([
    keras.layers.Input(shape=(784,)),
    keras.layers.Dense(300, kernel_initializer="he_normal"),
    keras.layers.LayerNormalization(),   # batch boyutundan bağımsız
    keras.layers.Activation("relu"),
    keras.layers.Dense(100, kernel_initializer="he_normal"),
    keras.layers.LayerNormalization(),
    keras.layers.Activation("relu"),
    keras.layers.Dense(10, activation="softmax")
], name="LN_Model")

# ─────────────────────────────────────────────────────────────────────
# BN vs BN-yok karşılaştırması
# ─────────────────────────────────────────────────────────────────────

(X_tr, y_tr), (X_te, y_te) = keras.datasets.mnist.load_data()
X_tr = X_tr.reshape(-1, 784).astype("float32") / 255.0
X_te = X_te.reshape(-1, 784).astype("float32") / 255.0

for name, model in [("BN_Model", model_bn), ("LN_Model", model_ln)]:
    h = model.fit(X_tr, y_tr, epochs=10, batch_size=64,
                  validation_split=0.1, verbose=0)
    _, acc = model.evaluate(X_te, y_te, verbose=0)
    init_loss = h.history["loss"][0]
    final_loss = h.history["loss"][-1]
    print(f"{name}: Başlangıç loss={init_loss:.3f} → Final loss={final_loss:.3f}  |  Test acc={acc:.4f}")
