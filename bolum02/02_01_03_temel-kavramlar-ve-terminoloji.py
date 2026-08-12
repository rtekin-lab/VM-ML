# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.1. Veri Bilimi Nedir? Veri Madenciliği ile İlişkisi › 2.1.3. Temel Kavramlar ve Terminoloji
# Kitap  : Kod 2.10 (Öznitelik, örneklem ve etiket kavramlarının )
# Dosya : bolum02/02_01_03_temel-kavramlar-ve-terminoloji.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# 1. Karma Veri Setinin Yapılandırılması
data = {
    'Müşteri_ID': range(1, 11),
    'Yaş': [25, 30, 35, 28, 45, 32, 29, 38, 42, 27],                 # Sayısal - Sürekli
    'Gelir': [45000, 52000, 61000, 48000, 75000,
              55000, 49000, 68000, 72000, 47000],                   # Sayısal - Sürekli
    'Çocuk_Sayısı': [0, 1, 2, 0, 3, 1, 0, 2, 2, 1],                # Sayısal - Ayrık
    'Şehir': ['İstanbul', 'Ankara', 'İzmir', 'İstanbul', 'Ankara',
              'İzmir', 'İstanbul', 'Ankara', 'İzmir', 'İstanbul'],   # Kategorik - Nominal
    'Eğitim': ['Lise', 'Üniversite', 'Yüksek Lisans', 'Lise', 'Doktora',
               'Üniversite', 'Lise', 'Yüksek Lisans', 'Doktora', 'Üniversite'], # Kategorik - Ordinal
    'Kredi_Kartı': [True, True, False, True, True,
                    False, True, True, False, True]                # Kategorik - Binary
}

df = pd.DataFrame(data)

# 2. Veri Yapısının İncelenmesi
print("Tablo: Değişkenlerin Veri Tipleri")
print(df.dtypes)
print("-" * 60)

# 3. Kategorik Veri Kodlama (Encoding) Teknikleri

# A. Ordinal Encoding (Sıralı Kategoriler İçin)
# Eğitim seviyeleri arasındaki hiyerarşik yapı manuel olarak haritalanır.
education_order = ['Lise', 'Üniversite', 'Yüksek Lisans', 'Doktora']
df['Eğitim_Kodlu'] = df['Eğitim'].map({edu: i for i, edu in enumerate(education_order)})

print("\nOrdinal Veri Dönüşümü (Eğitim Seviyesi):")
print(df[['Eğitim', 'Eğitim_Kodlu']].head())

# B. One-Hot Encoding (Sıralı Olmayan Nominal Kategoriler İçin)
# Şehirler arası sıralama olmadığından her şehir için ayrı bir sütun oluşturulur.
city_dummies = pd.get_dummies(df['Şehir'], prefix='Şehir')
df_encoded = pd.concat([df, city_dummies], axis=1)

print("\nNominal Veri Dönüşümü (Şehir - One-Hot):")
print(df_encoded.filter(like='Şehir').head())

# 4. Betimsel İstatistiksel Özet
print("-" * 60)
print("Sayısal Değişkenlerin Merkezi Eğilim ve Dağılım İstatistikleri:")
print(df[['Yaş', 'Gelir', 'Çocuk_Sayısı']].describe().T)
