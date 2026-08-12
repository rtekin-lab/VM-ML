# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.3. Veri Toplama ve API Entegrasyonları › 2.3.3. Veri Toplama Araçları ve Teknolojileri › Veritabanı Bağlantıları ve SQLAlchemy
# Dosya : bolum02/02_03_03_veritabani-baglantilari-ve-sqlalchemy.py
# Gerekli: pip install numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import sqlite3
import pandas as pd
import numpy as np

# 1. Veritabanı Bağlantı Konfigürasyonu
# Gerçek projelerde SQLAlchemy kullanımı:
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://user:password@host:5432/db')

# Eğitim amaçlı bellek içi (in-memory) SQLite bağlantısı:
conn = sqlite3.connect(':memory:')

# 2. Sentetik Veri Seti Yapılandırması ve Veritabanına Aktarım
np.random.seed(42)
n = 1000
sehirler = ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya']
kategoriler = ['Elektronik', 'Giyim', 'Gida', 'Mobilya', 'Kitap']

df_satis = pd.DataFrame({
    'satis_id'   : range(1, n+1),
    'tarih'      : pd.date_range('2023-01-01', periods=n, freq='8h'),
    'sehir'      : np.random.choice(sehirler, n),
    'kategori'   : np.random.choice(kategoriler, n),
    'tutar'      : np.abs(np.random.normal(500, 250, n)).round(2),
    'adet'       : np.random.randint(1, 10, n),
    'musteri_id' : np.random.randint(1, 200, n),
})

# to_sql: DataFrame nesnesini veritabanı tablosuna dönüştürür
df_satis.to_sql('satislar', conn, if_exists='replace', index=False)
print(f"[İşlem] {len(df_satis)} kayıt veritabanına aktarıldı.")

# 3. SQL Sorguları ile Analitik Veri Çekme
# Şehir bazlı aylık performans özeti
sorgu_performans = """
SELECT
    sehir,
    strftime('%Y-%m', tarih) AS ay,
    COUNT(*) AS islem_sayisi,
    ROUND(SUM(tutar), 2) AS toplam_tutar
FROM satislar
GROUP BY sehir, ay
ORDER BY ay DESC, toplam_tutar DESC
LIMIT 5
"""
df_ozet = pd.read_sql_query(sorgu_performans, conn)
print("\n--- Şehir Bazlı Aylik Özet ---")
print(df_ozet.to_string(index=False))

# 4. Kategori Bazlı ABC Analizi (Envanter Yönetimi)
# ABC analizi, ürünlerin toplam cirodaki payına göre sınıflandırılmasını sağlar.
sorgu_abc = """
SELECT
    kategori,
    ROUND(SUM(tutar), 2) AS toplam,
    ROUND(SUM(tutar) * 100.0 / (SELECT SUM(tutar) FROM satislar), 2) AS yuzde
FROM satislar
GROUP BY kategori
ORDER BY toplam DESC
"""
df_abc = pd.read_sql_query(sorgu_abc, conn)
df_abc['kumulatif'] = df_abc['yuzde'].cumsum()
df_abc['sinif'] = df_abc['kumulatif'].apply(lambda x: 'A' if x <= 70 else ('B' if x <= 90 else 'C'))

print("\n--- Kategori ABC Analizi ---")
print(df_abc.to_string(index=False))

conn.close()
