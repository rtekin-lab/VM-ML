# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.2. Farklı Veri Kaynakları ve Özellikleri › Nesnelerin İnterneti (IoT) ve Sensör Verileri
# Kitap  : Kod 2.16 (IoT sensör akışının benzetimle üretilmesi)
# Dosya : bolum02/02_02_02_nesnelerin-interneti-ve-sensor-verileri.py
# Gerekli: pip install numpy pandas
# ==========================================================================
import pandas as pd
import numpy as np

# 1. Simüle edilmiş IoT Sıcaklık Sensörü Verisi
data = {
    'timestamp': pd.date_range(start='2024-01-01', periods=10, freq='min'),
    'sicaklik': [22.1, 22.5, 22.3, 85.0, 22.2, 22.4, 22.6, -10.0, 22.1, 22.3] # 85.0 ve -10.0 gürültüdür
}
df_sensor = pd.DataFrame(data)

# 2. Z-Score Hesaplama
mu = df_sensor['sicaklik'].mean()
sigma = df_sensor['sicaklik'].std()
df_sensor['z_score'] = (df_sensor['sicaklik'] - mu) / sigma

# 3. Aykırı Değerlerin Filtrelenmesi
anomaliler = df_sensor[df_sensor['z_score'].abs() > 2] # Örnek amaçlı eşik 2 seçilmiştir
print("--- Tespit Edilen Anormal Sensör Ölçümleri ---")
print(anomaliler[['timestamp', 'sicaklik', 'z_score']])
