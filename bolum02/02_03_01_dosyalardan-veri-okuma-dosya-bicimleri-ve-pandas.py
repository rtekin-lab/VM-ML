# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.3. Veri Toplama ve API Entegrasyonları › 2.3.1. Veri Toplama Yöntemleri › Dosyalardan Veri Okuma: Dosya Biçimleri ve pandas Entegrasyonu
# Dosya : bolum02/02_03_01_dosyalardan-veri-okuma-dosya-bicimleri-ve-pandas.py
# Gerekli: pip install pandas
# ==========================================================================
import pandas as pd
import json, io

# 1. CSV Formatından Veri Okuma ve Gelişmiş Parametre Yönetimi
# csv_icerik değişkeni ham bir CSV dosyasını simüle etmektedir.
csv_data = """ad,yas,sehir,maas
Ahmet,34,Istanbul,75000
Ayse,28,Ankara,62000
Mehmet,45,Izmir,88000
Fatma,31,Bursa,55000
Ali,52,Istanbul,110000"""

# dtype: Sütun tiplerini belirler, na_values: Eksik değerleri tanımlar
df_csv = pd.read_csv(
    io.StringIO(csv_data),
    dtype={'yas': 'int32', 'maas': 'float64'},
    na_values=['N/A', 'missing', '-']
)

print("=== CSV Veri Yapısı ve Tipleri ===")
print(df_csv.info())

# 2. JSON Veri İşleme ve Normalizasyon (Flattening)
# İç içe geçmiş (nested) sözlük yapıları düz tablo formatına dönüştürülür.
json_raw = [
    {"ad": "Ahmet", "yas": 34, "adres": {"sehir": "Istanbul", "ilce": "Kadikoy"}},
    {"ad": "Ayse",  "yas": 28, "adres": {"sehir": "Ankara",   "ilce": "Cankaya"}}
]

# json_normalize: Hiyerarşik yapıları sütunlara açar (sep parametresi ayırıcıyı belirler)
df_normalized = pd.json_normalize(json_raw, sep='_')
print("\n=== Normalize Edilmiş JSON Verisi ===")
print(df_normalized)

# 3. Veri Tipi Dönüşümü ve Bellek Optimizasyonu
# Kategorik verilerin 'category' tipine dönüştürülmesi ve sayısal downcasting işlemi
print("\n--- Bellek Kullanımı Analizi ---")
print(f"Başlangıç Bellek Tüketimi: {df_csv.memory_usage(deep=True).sum()} byte")

df_opt = df_csv.copy()
df_opt['sehir'] = df_opt['sehir'].astype('category')
df_opt['yas']   = pd.to_numeric(df_opt['yas'], downcast='integer')
df_opt['maas']  = pd.to_numeric(df_opt['maas'], downcast='float')

print(f"Optimizasyon Sonrası Bellek Tüketimi: {df_opt.memory_usage(deep=True).sum()} byte")
