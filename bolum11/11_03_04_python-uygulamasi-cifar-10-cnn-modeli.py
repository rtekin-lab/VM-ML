# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.3. Evrişimsel Sinir Ağları (Convolutional Neural Networks — CNN) › 11.3.4. Modern CNN Mimarileri › Python Uygulaması: CIFAR-10 CNN Modeli
# Kitap  : Kod 11.6 (CIFAR-10 için evrişimsel ağ mimarisi)
# Dosya : bolum11/11_03_04_python-uygulamasi-cifar-10-cnn-modeli.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ============================================================
# 1. VERİ YÜKLEME VE ÖN İŞLEME
# ============================================================
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# Normalizasyon: [0,255] → [0,1]
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32') / 255.0

# CIFAR-10 sınıf etiketleri
sinif_adlari = ['uçak','otomobil','kuş','kedi','geyik',
                'köpek','kurbağa','at','gemi','kamyon']

print(f'Eğitim: {X_train.shape}, Test: {X_test.shape}')
print(f'Görüntü boyutu: {X_train.shape[1:]}  (32×32×3 RGB)')

# ============================================================
# 2. CNN MİMARİSİ: VGG-STYLE KÜÇÜK MODEL
# ============================================================
def cnn_modeli_olustur():
    model = keras.Sequential([
        # --- BLOK 1 ---
        layers.Conv2D(32, (3,3), padding='same', activation='relu',
                      input_shape=(32,32,3)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3,3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(0.25),

        # --- BLOK 2 ---
        layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(0.30),

        # --- BLOK 3 ---
        layers.Conv2D(128, (3,3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3,3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.GlobalAveragePooling2D(),  # Flatten yerine GAP
        layers.Dropout(0.40),

        # --- SINIFLANDIRICI ---
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.50),
        layers.Dense(10, activation='softmax'),
    ], name='VGGStyle_CIFAR10')
    return model

model = cnn_modeli_olustur()
model.summary()

# ============================================================
# 3. VERİ ARTIRIMI (DATA AUGMENTATION)
# ============================================================
datagen = ImageDataGenerator(
    rotation_range=15,         # ±15° döndürme
    width_shift_range=0.1,     # Yatay kaydırma
    height_shift_range=0.1,    # Dikey kaydırma
    horizontal_flip=True,      # Yatay çevirme
    zoom_range=0.1,            # Yakınlaştırma
    fill_mode='nearest'
)
datagen.fit(X_train)

# ============================================================
# 4. DERLEME VE EĞİTİM
# ============================================================
lr_schedule = keras.optimizers.schedules.CosineDecay(
    initial_learning_rate=0.001, decay_steps=50*390)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=lr_schedule),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
    keras.callbacks.ModelCheckpoint('cifar10_best.h5', save_best_only=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5, min_lr=1e-6),
]

history = model.fit(
    datagen.flow(X_train, y_train, batch_size=64),
    epochs=50,
    validation_data=(X_test, y_test),
    callbacks=callbacks,
    verbose=1
)

# ============================================================
# 5. RESNET-STYLE SKIP CONNECTION (FUNCTIONAL API)
# ============================================================
def residual_blok(x, filters, stride=1):
    """Temel ResNet artık bloku — F(x) + x"""
    shortcut = x

    # Ana yol
    x = layers.Conv2D(filters, 3, stride, padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.Conv2D(filters, 3, padding='same')(x)
    x = layers.BatchNormalization()(x)

    # Boyut eşleştirme (stride > 1 ise shortcut boyutu değişir)
    if stride != 1 or shortcut.shape[-1] != filters:
        shortcut = layers.Conv2D(filters, 1, stride)(shortcut)
        shortcut = layers.BatchNormalization()(shortcut)

    # Skip connection: F(x) + x
    x = layers.Add()([x, shortcut])
    x = layers.ReLU()(x)
    return x

def kucuk_resnet():
    giris = keras.Input(shape=(32, 32, 3))
    x = layers.Conv2D(32, 3, padding='same')(giris)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = residual_blok(x, 32)
    x = residual_blok(x, 64, stride=2)
    x = residual_blok(x, 64)
    x = residual_blok(x, 128, stride=2)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(10, activation='softmax')(x)
    return keras.Model(giris, x, name='KucukResNet')

resnet = kucuk_resnet()
resnet.summary()
print(f'\nResNet parametre sayısı: {resnet.count_params():,}')
