# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.6. Üretici ve Temsili Modeller (Kısa Bir Bakış) › 11.6.1. Otokodlayıcılar (Autoencoders) › Python Uygulaması: Otokodlayıcı ile Anomali Tespiti
# Kitap  : Kod 11.10 (Otokodlayıcı ile anomali tespiti)
# Dosya : bolum11/11_06_01_python-uygulamasi-otokodlayici-ile-anomali-tespi.py
# Gerekli: pip install numpy scikit-learn tensorflow
# ==========================================================================
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import roc_auc_score, classification_report

# ============================================================
# 1. VERİ HAZIRLAMA — MNIST Anomali Senaryosu
# ============================================================
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32') / 255.0

# SENARYO: Yalnızca '0' rakamları normal; diğerleri anomali
X_normal_train = X_train[y_train == 0]
y_anomali_test = (y_test != 0).astype(int)   # 0=normal, 1=anomali

print(f'Normal eğitim: {len(X_normal_train)} örnek')
print(f'Test seti: {len(y_test)} örnek | Anomali oranı: {y_anomali_test.mean():.1%}')

# ============================================================
# 2. CNN OTOKODLAYıCı MİMARİSİ
# ============================================================
def otokodlayici_olustur(latent_dim=32):
    # --- KODLAYICI ---
    enc_in = keras.Input(shape=(28, 28, 1), name='encoder_giris')
    x = layers.Conv2D(32, 3, activation='relu', padding='same')(enc_in)
    x = layers.MaxPooling2D(2)(x)              # → 14×14×32
    x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
    x = layers.MaxPooling2D(2)(x)              # → 7×7×64
    x = layers.Flatten()(x)                    # → 3136
    gizli = layers.Dense(latent_dim, name='gizli_kod')(x)  # DARBOĞAZ
    encoder = keras.Model(enc_in, gizli, name='Encoder')

    # --- KOD ÇÖZÜCÜ ---
    dec_in = keras.Input(shape=(latent_dim,), name='decoder_giris')
    x = layers.Dense(7*7*64, activation='relu')(dec_in)
    x = layers.Reshape((7, 7, 64))(x)
    x = layers.Conv2DTranspose(64, 3, activation='relu', padding='same')(x)
    x = layers.UpSampling2D(2)(x)              # → 14×14×64
    x = layers.Conv2DTranspose(32, 3, activation='relu', padding='same')(x)
    x = layers.UpSampling2D(2)(x)              # → 28×28×32
    yeniden = layers.Conv2DTranspose(1, 3, activation='sigmoid',
                                      padding='same', name='cikis')(x)
    decoder = keras.Model(dec_in, yeniden, name='Decoder')

    # --- TAM OTOKODLAYıCı ---
    inp = encoder.input
    out = decoder(encoder(inp))
    oto = keras.Model(inp, out, name='Otokodlayici')
    return encoder, decoder, oto

encoder, decoder, oto = otokodlayici_olustur(latent_dim=32)
oto.summary()

# ============================================================
# 3. YALNIZCA NORMAL VERİYLE EĞİTİM
# ============================================================
oto.compile(optimizer=keras.optimizers.Adam(1e-3), loss='mse')

X_tr = X_normal_train.reshape(-1, 28, 28, 1)
X_te = X_test.reshape(-1, 28, 28, 1)

history = oto.fit(
    X_tr, X_tr,                     # Girdi = Hedef (self-supervised)
    epochs=30, batch_size=128,
    validation_split=0.1,
    callbacks=[keras.callbacks.EarlyStopping(patience=5,
                                              restore_best_weights=True)],
    verbose=0
)
print(f'Son eğitim kaybı: {history.history["loss"][-1]:.6f}')

# ============================================================
# 4. ANOMALİ TESPİTİ VE DEĞERLENDİRME
# ============================================================
X_hat = oto.predict(X_te, verbose=0)
recon_hatalari = np.mean((X_te - X_hat)**2, axis=(1,2,3))

auc = roc_auc_score(y_anomali_test, recon_hatalari)
print(f'\nAnomali Tespiti AUC-ROC: {auc:.4f}')

# Eşik: eğitim hatalarının 95. yüzdeliği
egitim_hatalari = np.mean(
    (X_tr - oto.predict(X_tr, verbose=0))**2, axis=(1,2,3))
esik = np.percentile(egitim_hatalari, 95)
y_tahmin = (recon_hatalari > esik).astype(int)

print(f'Eşik (θ = %95. yüzdelik): {esik:.6f}')
print('\n' + classification_report(y_anomali_test, y_tahmin,
      target_names=['Normal', 'Anomali']))

normal_ort  = recon_hatalari[y_anomali_test == 0].mean()
anomali_ort = recon_hatalari[y_anomali_test == 1].mean()
print(f'Normal ortalama hata :  {normal_ort:.6f}')
print(f'Anomali ortalama hata:  {anomali_ort:.6f}  ({anomali_ort/normal_ort:.1f}× daha yüksek)')
