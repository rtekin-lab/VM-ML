# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.3. Veri Toplama ve API Entegrasyonları › 2.3.3. Veri Toplama Araçları ve Teknolojileri › Finansal Veri Toplama (yfinance Entegrasyonu)
# Dosya : bolum02/02_03_03_finansal-veri-toplama.py
# Gerekli: pip install numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import pandas as pd
import numpy as np

# 1. Veri Simülasyonu: Geometrik Brownian Motion Modeli
np.random.seed(42)
n_gun = 252  # Yıllık iş günü sayısı
mu, sigma, S0 = 0.0003, 0.015, 180.0

# Günlük getirilerin ve kümülatif fiyat serisinin oluşturulması
getiriler = np.random.normal(mu, sigma, n_gun)
fiyatlar  = S0 * np.exp(np.cumsum(getiriler))
tarihler  = pd.bdate_range('2026-01-02', periods=n_gun)

df_hisse = pd.DataFrame({
    'Open'  : fiyatlar * np.random.uniform(0.99, 1.00, n_gun),
    'High'  : fiyatlar * np.random.uniform(1.00, 1.02, n_gun),
    'Low'   : fiyatlar * np.random.uniform(0.98, 1.00, n_gun),
    'Close' : fiyatlar,
    'Volume': np.random.randint(20e6, 80e6, n_gun),
}, index=tarihler)

# 2. Teknik İndikatörlerin Hesaplanması
# Hareketli Ortalamalar (Moving Averages)
df_hisse['MA20'] = df_hisse['Close'].rolling(window=20).mean()

# Bollinger Bantları (Volatilite Kanalları)
df_hisse['BB_Orta'] = df_hisse['Close'].rolling(20).mean()
df_hisse['BB_Std']  = df_hisse['Close'].rolling(20).std()
df_hisse['BB_Ust']   = df_hisse['BB_Orta'] + (2 * df_hisse['BB_Std'])
df_hisse['BB_Alt']   = df_hisse['BB_Orta'] - (2 * df_hisse['BB_Std'])

# 3. Risk ve Performans Metrikleri
df_hisse['Log_Getiri'] = np.log(df_hisse['Close'] / df_hisse['Close'].shift(1))
yillik_vol = df_hisse['Log_Getiri'].std() * np.sqrt(252)
sharpe_orani = (df_hisse['Log_Getiri'].mean() * 252) / yillik_vol

# Maksimum Düşüş (Maximum Drawdown)
zirve = df_hisse['Close'].cummax()
dusus = (df_hisse['Close'] - zirve) / zirve
max_dusus = dusus.min()

print(f"Yıllık Volatilite: %{yillik_vol*100:.2f}")
print(f"Sharpe Oranı: {sharpe_orani:.3f}")
print(f"Maksimum Düşüş: %{max_dusus*100:.2f}")
