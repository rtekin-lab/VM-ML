# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.2. Sıralı (Sequential) API ile Model İnşası, Derleme ve Eğitim › Adım 2: Modeli Derleme (model.compile)
# Kitap  : Kod 10.10 (model.compile(): iyileştirici, kayıp ve metr)
# Dosya : bolum10/10_06_02_adim-2-modeli-derleme.py
# Gerekli: pip install tensorflow
# ==========================================================================
# ─────────────────────────────────────────────────────────────────────
# model.compile(): Detaylı Kullanım
# ─────────────────────────────────────────────────────────────────────

# Yöntem 1: Kısa string isimler
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum10/10_06_02_adim-1-*
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 784).astype("float32") / 255.0
X_test  = X_test.reshape(-1, 784).astype("float32") / 255.0
model = keras.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(10, activation="softmax"),
])
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Yöntem 2: Obje olarak – hiperparametre kontrolü
model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=0.001,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-8,
        clipnorm=1.0        # Gradyan patlamasına karşı clipping
    ),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=[
        keras.metrics.SparseCategoricalAccuracy(name="accuracy"),
        keras.metrics.SparseTopKCategoricalAccuracy(k=3, name="top3_acc")
    ]
)

# Özel kayıp fonksiyonu tanımlama (örnek: Focal Loss)
def focal_loss(gamma=2.0, alpha=0.25):
    def loss_fn(y_true, y_pred):
        import tensorflow as tf
        ce = keras.losses.sparse_categorical_crossentropy(y_true, y_pred)
        p_t = tf.exp(-ce)
        focal = alpha * (1 - p_t)**gamma * ce
        return tf.reduce_mean(focal)
    return loss_fn

# model.compile(loss=focal_loss(gamma=2.0), optimizer="adam")
