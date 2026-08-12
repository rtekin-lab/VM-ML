# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.1. Veri Bilimi Nedir? Veri Madenciliği ile İlişkisi › 2.1.2. Veri Madenciliği ve Veri Bilimi İlişkisi › Veri Madenciliği ve Büyük Veri İlişkisi
# Kitap  : Kod 2.9 (Büyük veri ölçeğinde bellek kullanımının ölç)
# Dosya : bolum02/02_01_02_veri-madenciligi-ve-buyuk-veri-iliskisi.py
# Gerekli: pip install dask numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import dask.dataframe as dd
import pandas as pd
import numpy as np

# 1. Büyük Veri Setinin Okunması (Lazy Evaluation)
# Dask veriyi hemen belleğe yüklemez, sadece işlem planını (graph) oluşturur
# Örn: df_dask = dd.read_csv('büyük_veri_dosyaları_*.csv')

# 2. Sentetik Büyük Veri Yapılandırması
n_partitions = 4 # Verinin kaç parçaya bölüneceği
data = {
    'id': range(1000000),
    'value': np.random.randn(1000000),
    'category': np.random.choice(['A', 'B', 'C'], 1000000)
}
df_pandas = pd.DataFrame(data)

# Pandas DataFrame'ini Dask yapısına dönüştürme
df_dask = dd.from_pandas(df_pandas, npartitions=n_partitions)

# 3. Paralel Filtreleme ve Gruplandırma İşlemleri
# .compute() çağrılana kadar gerçek hesaplama başlamaz
filtered = df_dask[df_dask['value'] > 0]
grouped = filtered.groupby('category')['value'].mean()

# 4. Hesaplamanın Başlatılması ve Sonuçların Alınması
result = grouped.compute()

print("Kategori Bazında Paralel Hesaplanan Ortalamalar:")
print(result)
