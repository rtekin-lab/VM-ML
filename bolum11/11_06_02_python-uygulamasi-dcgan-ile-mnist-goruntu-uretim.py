# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.6. Üretici ve Temsili Modeller (Kısa Bir Bakış) › 11.6.2. Üretken Çekişmeli Ağlar (GAN — Generative Adversarial Networks) › Python Uygulaması: DCGAN ile MNIST Görüntü Üretimi
# Kitap  : Kod 11.11 (DCGAN ile MNIST görüntü üretimi) · Kod 11.12 (Üretilen görüntülerin niteliğinin değerlendi)
# Dosya : bolum11/11_06_02_python-uygulamasi-dcgan-ile-mnist-goruntu-uretim.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ============================================================
# 1. VERİ HAZIRLAMA
# ============================================================
(X_train, _), (_, _) = keras.datasets.mnist.load_data()
X_train = X_train.astype('float32')
# GAN için [-1, 1] normalizasyonu (Generator tanh çıkışıyla uyumlu)
X_train = (X_train - 127.5) / 127.5
X_train = X_train.reshape(-1, 28, 28, 1)
print(f'Veri: {X_train.shape}  Aralık: [{X_train.min():.1f}, {X_train.max():.1f}]')

# ============================================================
# 2. ÜRETİCİ (GENERATOR)
# ============================================================
def uretici_olustur(latent_dim=100):
    """
    z ~ N(0,I) → 28×28×1 sahte görüntü [-1, 1]
    Transposed convolution ile kademeli boyut büyütme
    """
    model = keras.Sequential([
        # Gürültü vektörünü 7×7×256'ya genişlet
        layers.Dense(7 * 7 * 256, input_dim=latent_dim),
        layers.BatchNormalization(),
        layers.LeakyReLU(0.2),
        layers.Reshape((7, 7, 256)),

        # 7×7×256 → 14×14×128
        layers.Conv2DTranspose(128, 4, strides=2, padding='same'),
        layers.BatchNormalization(),
        layers.LeakyReLU(0.2),

        # 14×14×128 → 28×28×64
        layers.Conv2DTranspose(64, 4, strides=2, padding='same'),
        layers.BatchNormalization(),
        layers.LeakyReLU(0.2),

        # 28×28×64 → 28×28×1 (son katman tanh ile [-1,1])
        layers.Conv2DTranspose(1, 4, strides=1, padding='same', activation='tanh'),
    ], name='Generator')
    return model

# ============================================================
# 3. AYIRT EDİCİ (DISCRIMINATOR)
# ============================================================
def ayirt_edici_olustur():
    """
    28×28×1 görüntü → gerçeklik skoru [0,1]
    NOT: D'de BatchNorm KULLANILMAZ (eğitim kararlılığı için)
    """
    model = keras.Sequential([
        # 28×28×1 → 14×14×64
        layers.Conv2D(64, 4, strides=2, padding='same', input_shape=(28,28,1)),
        layers.LeakyReLU(0.2),
        layers.Dropout(0.3),

        # 14×14×64 → 7×7×128
        layers.Conv2D(128, 4, strides=2, padding='same'),
        layers.LeakyReLU(0.2),
        layers.Dropout(0.3),

        layers.Flatten(),
        layers.Dense(1, activation='sigmoid'),  # Gerçek mi sahte mi?
    ], name='Discriminator')
    return model

# ============================================================
# 4. GAN SINIFI — ÖZEL EĞİTİM DÖNGÜSÜ
# ============================================================
class DCGAN(keras.Model):
    def __init__(self, latent_dim=100):
        super().__init__()
        self.latent_dim = latent_dim
        self.G = uretici_olustur(latent_dim)
        self.D = ayirt_edici_olustur()

    def compile(self, d_opt, g_opt, loss_fn):
        super().compile()
        self.d_opt = d_opt
        self.g_opt = g_opt
        self.loss_fn = loss_fn
        self.d_loss_m = keras.metrics.Mean('d_loss')
        self.g_loss_m = keras.metrics.Mean('g_loss')

    def train_step(self, gercek):
        bs = tf.shape(gercek)[0]

        # ---- ADIM 1: D Güncelle ----
        z = tf.random.normal([bs, self.latent_dim])
        sahte = self.G(z, training=False)
        tum   = tf.concat([gercek, sahte], axis=0)
        # Label smoothing: 1.0→0.9, 0.0→0.1
        etiket = tf.concat([
            tf.ones((bs,1)) * 0.9,   # Gerçek: smoothed
            tf.zeros((bs,1)) + 0.1,  # Sahte:  smoothed
        ], axis=0)

        with tf.GradientTape() as tape:
            tahmin = self.D(tum, training=True)
            d_loss = self.loss_fn(etiket, tahmin)
        grads = tape.gradient(d_loss, self.D.trainable_variables)
        self.d_opt.apply_gradients(zip(grads, self.D.trainable_variables))

        # ---- ADIM 2: G Güncelle ----
        z = tf.random.normal([bs, self.latent_dim])
        aldatici = tf.ones((bs, 1))  # G, D'nin 'gerçek' demesini istiyor

        with tf.GradientTape() as tape:
            sahte2 = self.G(z, training=True)
            pred   = self.D(sahte2, training=False)  # D donduruldu
            g_loss = self.loss_fn(aldatici, pred)
        grads = tape.gradient(g_loss, self.G.trainable_variables)
        self.g_opt.apply_gradients(zip(grads, self.G.trainable_variables))

        self.d_loss_m.update_state(d_loss)
        self.g_loss_m.update_state(g_loss)
        return {'d_loss': self.d_loss_m.result(),
                'g_loss': self.g_loss_m.result()}

# ============================================================
# 5. EĞİTİM VE GÖRÜNTÜ ÜRETME
# ============================================================
LATENT_DIM = 100
gan = DCGAN(latent_dim=LATENT_DIM)
gan.compile(

    g_opt  = keras.optimizers.Adam(2e-4, beta_1=0.5),
    loss_fn= keras.losses.BinaryCrossentropy(),
)

print(f'Generator parametresi    : {gan.G.count_params():,}')
print(f'Discriminator parametresi: {gan.D.count_params():,}')

# Eğitim (gerçek GPU ortamında çalıştırılır):
# history = gan.fit(X_train, epochs=50, batch_size=128)

# Eğitim sonrası yeni görüntü üretme:
# gurultu = np.random.normal(0, 1, (25, LATENT_DIM))
# uretilen = gan.G.predict(gurultu)
# uretilen = (uretilen * 127.5 + 127.5).astype(np.uint8)  # [-1,1] → [0,255]
print('\nGAN hazır. Eğitim tamamlandığında G.predict() ile görüntü üretilir.')
