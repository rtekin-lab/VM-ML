# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.2. Farklı Veri Kaynakları ve Özellikleri › Zaman Serisi ve Akış Verileri (Time-Series & Streaming Data)
# Kitap  : Kod 2.13 (Zaman serisi verisinin pandas ile yeniden ör)
# Dosya : bolum02/02_02_02_zaman-serisi-ve-akis-verileri.py
# Gerekli: pip install matplotlib numpy pandas statsmodels
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

# 1. Sentetik Zaman Serisi Oluşturma (Trend, Mevsimsellik ve Gürültü)
np.random.seed(42)
n = 200
t = np.arange(n)
trend_comp    = 0.3 * t                          # Doğrusal trend
seasonal_comp = 15 * np.sin(2 * np.pi * t/52)    # 52 haftalık periyodik döngü
noise_comp    = np.random.normal(0, 5, n)
ts_data       = trend_comp + seasonal_comp + noise_comp

df = pd.DataFrame({'deger': ts_data},
                  index=pd.date_range('2020-01-01', periods=n, freq='W'))

# 2. Durağanlık Analizi: Augmented Dickey-Fuller (ADF) Testi
adf_res = adfuller(df['deger'].dropna())
print("--- ADF Testi Sonuçları ---")
print(f"p-değeri: {adf_res[1]:.4f}")
print(f"Durum: {'Durağan' if adf_res[1] < 0.05 else 'Durağan Değil'}")

# 3. Bileşen Ayrıştırma (STL Decomposition)
# Seriyi Trend, Mevsimsellik ve Artık (Resid) bileşenlerine ayırır
decomposition = seasonal_decompose(df['deger'], model='additive', period=52)
print("\n--- Bileşen İstatistikleri ---")
print(f"Trend Ortalaması: {decomposition.trend.mean():.2f}")
print(f"Mevsimsel Etki Standart Sapması: {decomposition.seasonal.std():.2f}")

# 4. Tahminleme Süreci: ARIMA(2,1,2)
# p=2 (AR), d=1 (Fark alma), q=2 (MA) parametreleri ile model eğitimi
model = ARIMA(df['deger'], order=(2,1,2))
results = model.fit()
forecast = results.forecast(steps=12)

print("\n--- 12 Haftalık Tahmin Kestirimi ---")
print(forecast.round(2).to_string())
