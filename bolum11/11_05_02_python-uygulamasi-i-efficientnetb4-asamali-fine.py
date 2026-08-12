# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.5. Transfer Öğrenimi (Transfer Learning) › 11.5.2. Özellik Çıkarımı ve İnce Ayarlama › Python Uygulaması I: EfficientNetB4 Aşamalı Fine-Tuning
# Kitap  : Kod 11.8 (EfficientNet ile aşamalı ince ayar)
# Dosya : bolum11/11_05_02_python-uygulamasi-i-efficientnetb4-asamali-fine.py
# Gerekli: pip install numpy tensorflow
# ==========================================================================
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB4, ResNet50V2
from tensorflow.keras.applications.efficientnet import preprocess_input as eff_prep
from tensorflow.keras.applications.resnet_v2 import preprocess_input as res_prep

# ============================================================
# 1. ÖZELLIK ÇIKARIMI — ResNet50V2
# ============================================================
def ozellik_cikarici_model(n_sinif, base='resnet50v2', img_size=224):
    """
    Önceden eğitilmiş modelin tüm ağırlıkları dondurulur.
    Yalnızca yeni sınıflandırma başlığı eğitilir.
    """
    input_shape = (img_size, img_size, 3)

    if base == 'resnet50v2':
        base_model = ResNet50V2(weights='imagenet', include_top=False,
                                input_shape=input_shape)
    else:
        base_model = EfficientNetB4(weights='imagenet', include_top=False,
                                    input_shape=input_shape)

    # TÜM BASE MODEL DONDUR
    base_model.trainable = False

    # Giriş + preprocessing model içinde
    giris = keras.Input(shape=input_shape, name='goruntu_girisi')
    x = res_prep(giris)                          # Model-spesifik normalizasyon
    x = base_model(x, training=False)            # training=False: BN inference mod
    x = layers.GlobalAveragePooling2D()(x)       # Flatten yerine GAP
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu',
                     kernel_regularizer=keras.regularizers.l2(1e-4))(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    cikis = layers.Dense(n_sinif, activation='softmax')(x)

    model = keras.Model(giris, cikis, name='FeatureExtraction_ResNet50V2')

    frozen  = sum(1 for l in base_model.layers if not l.trainable)
    toplam  = base_model.count_params()
    egitim  = model.count_params() - toplam
    print(f'Donuk parametre : {toplam:>12,}  ({frozen} katman)')
    print(f'Eğitilen param. : {egitim:>12,}  ({100*egitim/(toplam+egitim):.1f}% toplam)')
    return model

# ============================================================
# 2. AŞAMALI İNCE AYARLAMA — EfficientNetB4
# ============================================================
def asamali_fine_tuning(n_sinif, img_size=224):
    """
    Üç aşamalı progressive fine-tuning:
    Aşama 1: Yalnızca baş (head) eğitimi — 10 epoch
    Aşama 2: Son 30 katman açıldı — 10 epoch (LR 10x küçültüldü)
    Aşama 3: Son 60 katman açıldı — 20 epoch (LR 100x küçültüldü)
    """
    input_shape = (img_size, img_size, 3)
    base = EfficientNetB4(weights='imagenet', include_top=False,
                          input_shape=input_shape)
    base.trainable = False

    giris = keras.Input(shape=input_shape)
    x = eff_prep(giris)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation='relu',
                     kernel_regularizer=keras.regularizers.l2(1e-4))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    cikis = layers.Dense(n_sinif, activation='softmax')(x)
    model = keras.Model(giris, cikis, name='ProgressiveFineTune_EfficientNetB4')

    callbacks_genel = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.3, patience=3, min_lr=1e-7),
    ]

    # --- AŞAMA 1: Sadece baş eğitimi ---
    print('\n=== AŞAMA 1: Baş katman eğitimi (LR=1e-3) ===')
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    # history1 = model.fit(X_train, y_train, epochs=10, callbacks=callbacks_genel, ...)

    # --- AŞAMA 2: Son 30 katman açıldı ---
    print('\n=== AŞAMA 2: Son 30 katman fine-tuning (LR=1e-4) ===')
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False
    # BatchNorm katmanlarını daima inference modunda tut
    for layer in base.layers:
        if isinstance(layer, layers.BatchNormalization):
            layer.trainable = False

    donuk_2 = sum(1 for l in base.layers if not l.trainable)
    print(f'  Dondurulmuş: {donuk_2} / {len(base.layers)} katman')

    model.compile(optimizer=keras.optimizers.Adam(1e-4),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    # history2 = model.fit(X_train, y_train, epochs=10, callbacks=callbacks_genel, ...)

    # --- AŞAMA 3: Son 60 katman açıldı ---
    print('\n=== AŞAMA 3: Son 60 katman fine-tuning (LR=5e-6) ===')
    for layer in base.layers[-60:]:
        if not isinstance(layer, layers.BatchNormalization):
            layer.trainable = True

    donuk_3 = sum(1 for l in base.layers if not l.trainable)
    print(f'  Dondurulmuş: {donuk_3} / {len(base.layers)} katman')

    model.compile(optimizer=keras.optimizers.Adam(5e-6),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    # history3 = model.fit(X_train, y_train, epochs=20, callbacks=callbacks_genel, ...)

    model.summary()
    return model

print('=== Transfer Öğrenimi Model Kurulumu ===')
print('\n--- Özellik Çıkarımı Modeli (ResNet50V2) ---')
fe_model = ozellik_cikarici_model(n_sinif=5)
print('\n--- Aşamalı Fine-Tuning Modeli (EfficientNetB4) ---')
ft_model = asamali_fine_tuning(n_sinif=5)
