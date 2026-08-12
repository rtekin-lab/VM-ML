# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.2. Sıralı (Sequential) API ile Model İnşası, Derleme ve Eğitim › Adım 1: Katmanların İnşası (Model Architecture)
# Kitap  : Kod 10.9 (Keras Sequential API ile model kurulumu)
# Dosya : bolum10/10_06_02_adim-1-katmanlarin-insasi.py
# Gerekli: pip install tensorflow
# ==========================================================================
from tensorflow import keras
from tensorflow.keras import layers

# ─── Yöntem 1: Katmanları Constructor'da Listele ─────────────────────
model = keras.Sequential([
    layers.Input(shape=(784,)),          # Giriş şeklini açıkça belirt
    layers.Dense(256, activation="relu",
                 kernel_initializer="he_normal",
                 name="gizli_katman_1"),
    layers.Dropout(0.3, name="dropout_1"),   # %30 nöron rastgele sıfırla
    layers.Dense(128, activation="relu",
                 kernel_initializer="he_normal",
                 name="gizli_katman_2"),
    layers.BatchNormalization(name="bn_1"),  # Aktivasyon öncesi normalize
    layers.Dense(64, activation="relu",
                 kernel_initializer="he_normal",
                 name="gizli_katman_3"),
    layers.Dropout(0.2, name="dropout_2"),
    layers.Dense(10, activation="softmax", name="cikis_katmani")
], name="mnist_mlp")

# ─── Yöntem 2: .add() Metodu ile Katman Ekle ─────────────────────────
model2 = keras.Sequential(name="mnist_mlp_v2")
model2.add(layers.Flatten(input_shape=(28, 28)))  # 2D → 1D düzleştir
model2.add(layers.Dense(128, activation="relu"))
model2.add(layers.Dense(10,  activation="softmax"))

# Model mimarisini görüntüle
model.summary()
# Parametreler: 256*(784+1) + 128*(256+1) + 64*(128+1) + 10*(64+1) = ~249.738
