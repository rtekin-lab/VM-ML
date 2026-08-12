# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 11
# Konum : BÖLÜM 11: DERİN ÖĞRENME (DEEP LEARNING) MİMARİLERİ VE OPTİMİZASYON › 11.4. Tekrarlayan Sinir Ağları (Recurrent Neural Networks — RNN) ve Sıralı Veriler › 11.4.3. LSTM ve GRU: Uzun Vadeli Bellek Mimarileri › Python Uygulaması: LSTM ile Zaman Serisi Tahmini
# Kitap  : Kod 11.7 (LSTM ile zaman serisi tahmini)
# Dosya : bolum11/11_04_03_python-uygulamasi-lstm-ile-zaman-serisi-tahmini.py
# Gerekli: pip install matplotlib numpy scikit-learn tensorflow
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# ============================================================
# 1. SİNÜS DALGA TAHMINI (TEMEL ZAMAN SERİSİ)
# ============================================================
np.random.seed(42)
t = np.linspace(0, 100, 1000)
# Gürültülü sinüs sinyali — gerçekçi zaman serisi simülasyonu
zaman_serisi = np.sin(0.1 * t) + 0.5 * np.sin(0.5 * t) + 0.1 * np.random.randn(1000)

def dizi_olustur(veri, n_adim):
    """Kayan pencere ile giriş-çıktı çiftleri oluşturur"""
    X, y = [], []
    for i in range(len(veri) - n_adim):
        X.append(veri[i:i + n_adim])
        y.append(veri[i + n_adim])
    return np.array(X), np.array(y)

n_adim = 30  # Son 30 adımı kullanarak bir sonraki değeri tahmin et
X, y = dizi_olustur(zaman_serisi, n_adim)

# Normalizasyon
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y.reshape(-1,1)).ravel()

# Train/test split
split = int(0.8 * len(X_scaled))
X_train = X_scaled[:split].reshape(-1, n_adim, 1)
X_test  = X_scaled[split:].reshape(-1, n_adim, 1)
y_train = y_scaled[:split]
y_test  = y_scaled[split:]

print(f'Eğitim: {X_train.shape}, Test: {X_test.shape}')

# ============================================================
# 2. LSTM MODELİ
# ============================================================
lstm_model = keras.Sequential([
    layers.LSTM(64, return_sequences=True, input_shape=(n_adim, 1)),
    layers.Dropout(0.2),
    layers.LSTM(32, return_sequences=False),
    layers.Dropout(0.2),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='linear')  # Regresyon çıktısı
], name='LSTM_ZamanSerisi')

lstm_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='mse',
    metrics=['mae']
)
lstm_model.summary()

history = lstm_model.fit(
    X_train, y_train,
    epochs=50, batch_size=32,
    validation_split=0.2,
    callbacks=[keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)],
    verbose=0
)

test_loss, test_mae = lstm_model.evaluate(X_test, y_test, verbose=0)
print(f'Test MSE: {test_loss:.6f}, Test MAE: {test_mae:.6f}')

# ============================================================
# 3. GRU vs LSTM KARŞILAŞTIRMASI
# ============================================================
def model_olustur(tur, n_adim):
    model = keras.Sequential(name=tur)
    if tur == 'SimpleRNN':
        model.add(layers.SimpleRNN(64, return_sequences=True, input_shape=(n_adim,1)))
        model.add(layers.SimpleRNN(32))
    elif tur == 'LSTM':
        model.add(layers.LSTM(64, return_sequences=True, input_shape=(n_adim,1)))
        model.add(layers.LSTM(32))
    elif tur == 'GRU':
        model.add(layers.GRU(64, return_sequences=True, input_shape=(n_adim,1)))
        model.add(layers.GRU(32))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

print('\n=== RNN / LSTM / GRU Karşılaştırması ===')
print(f'{"Model":<12} {"Parametre":>12} {"Test MAE":>10}')
print('-' * 37)

for tur in ['SimpleRNN', 'GRU', 'LSTM']:
    m = model_olustur(tur, n_adim)
    m.fit(X_train, y_train, epochs=30, batch_size=32,
          validation_split=0.1, verbose=0)
    _, mae = m.evaluate(X_test, y_test, verbose=0)
    params = m.count_params()
    print(f'{tur:<12} {params:>12,} {mae:>10.6f}')

# ============================================================
# 4. DUYGU ANALİZİ: Many-to-One LSTM
# ============================================================
print('\n=== Duygu Analizi: LSTM Many-to-One ===\n')

max_kelime = 10000
max_uzunluk = 200
embedding_dim = 64

# IMDB veri seti
(X_imdb_train, y_imdb_train), (X_imdb_test, y_imdb_test) = \
    keras.datasets.imdb.load_data(num_words=max_kelime)

X_imdb_train = keras.preprocessing.sequence.pad_sequences(
    X_imdb_train, maxlen=max_uzunluk, padding='post')
X_imdb_test = keras.preprocessing.sequence.pad_sequences(
    X_imdb_test, maxlen=max_uzunluk, padding='post')

duygu_model = keras.Sequential([
    # Embedding: Kelime indekslerini yoğun vektörlere dönüştürür
    layers.Embedding(max_kelime, embedding_dim, input_length=max_uzunluk),
    layers.Dropout(0.2),
    # İki katmanlı Bidirectional LSTM
    layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
    layers.Dropout(0.3),
    layers.Bidirectional(layers.LSTM(32)),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')  # İkili sınıflandırma
], name='Bidirectional_LSTM_Duygu')

duygu_model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss='binary_crossentropy',
    metrics=['accuracy']
)
duygu_model.summary()

# (Eğitim satırı — gerçekte çalıştırılabilir)
# history = duygu_model.fit(X_imdb_train, y_imdb_train,
#     epochs=5, batch_size=128, validation_split=0.2)
# Beklenen Test Doğruluğu: ~%87-89
