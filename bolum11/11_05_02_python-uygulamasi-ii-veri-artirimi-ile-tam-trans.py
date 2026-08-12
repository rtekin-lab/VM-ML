# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.5. Transfer Öğrenimi (Transfer Learning) › 11.5.2. Özellik Çıkarımı ve İnce Ayarlama › Python Uygulaması II: Veri Artırımı ile Tam Transfer Öğrenim Pipeline'ı
# Kitap  : Kod 11.9 (Uçtan uca transfer öğrenimi boru hattı)
# Dosya : bolum11/11_05_02_python-uygulamasi-ii-veri-artirimi-ile-tam-trans.py
# Gerekli: pip install tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import numpy as np
# ============================================================
# TAM TRANSFER ÖĞRENİMİ PIPELINE'I
# Gerçek dünya projesinde tüm adımlar birlikte
# ============================================================
from tensorflow.keras.applications import MobileNetV3Large

def transfer_pipeline(veri_dizini, n_sinif, img_size=224, batch_size=32):
    """
    Gerçek bir transfer öğrenimi pipeline'ı:
    1. Veri yükleme + augmentation
    2. Özellik çıkarımı ile ısınma
    3. Aşamalı fine-tuning
    """

    # ---- VERİ ARTIRIMI (Keras Preprocessing Layers — model içinde) ----
    veri_artirimi = keras.Sequential([
        layers.RandomFlip('horizontal'),
        layers.RandomRotation(0.10),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10),
        layers.RandomBrightness(factor=0.10),
        layers.RandomTranslation(0.05, 0.05),
    ], name='veri_artirimi')

    # ---- MODEL KURULUMU ----
    giris = keras.Input(shape=(img_size, img_size, 3))
    x = veri_artirimi(giris)          # Sadece training=True'da aktif

    base = MobileNetV3Large(weights='imagenet', include_top=False,
                             input_tensor=x)
    base.trainable = False            # Başlangıçta dondur

    x = layers.GlobalAveragePooling2D()(base.output)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.4)(x)
    cikis = layers.Dense(n_sinif, activation='softmax')(x)
    model = keras.Model(giris, cikis, name='MobileNetV3_Pipeline')

    # ---- AŞAMA 1: ISıNMA (Warm-up) ----
    model.compile(
        optimizer=keras.optimizers.AdamW(learning_rate=1e-3, weight_decay=1e-4),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    print(f'Aşama 1 — Eğitilen param: {sum(np.prod(w.shape) for w in model.trainable_weights):,}')

    # Gerçek veriyle eğitim:
    # train_ds = tf.keras.utils.image_dataset_from_directory(
    #     veri_dizini, validation_split=0.2, subset='training',
    #     seed=42, image_size=(img_size,img_size), batch_size=batch_size)
    # val_ds = tf.keras.utils.image_dataset_from_directory(
    #     veri_dizini, validation_split=0.2, subset='validation',
    #     seed=42, image_size=(img_size,img_size), batch_size=batch_size)
    # Performans için: train_ds = train_ds.cache().prefetch(tf.data.AUTOTUNE)

    # ---- AŞAMA 2: FİNE-TUNİNG ----
    base.trainable = True
    # BatchNorm frozen
    for layer in base.layers:
        if isinstance(layer, layers.BatchNormalization):
            layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.AdamW(learning_rate=1e-5, weight_decay=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    print(f'Aşama 2 — Eğitilen param: {sum(np.prod(w.shape) for w in model.trainable_weights):,}')
    return model

model_full = transfer_pipeline('/data/siniflar', n_sinif=10)
print('\nTransfer pipeline hazır!')
