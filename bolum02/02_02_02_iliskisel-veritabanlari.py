# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.2. Farklı Veri Kaynakları ve Özellikleri › İlişkisel Veritabanları (Relational Databases)
# Kitap  : Kod 2.12 (SQLAlchemy ile ilişkisel veritabanından veri)
# Dosya : bolum02/02_02_02_iliskisel-veritabanlari.py
# Gerekli: pip install numpy pandas
# ==========================================================================
import sqlite3
import pandas as pd
import numpy as np

# 1. Bellek İçi (In-Memory) SQLite Veritabanı Konfigürasyonu
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Veri Şemalarının Oluşturulması (Schema Definition)
cursor.execute("""
CREATE TABLE musteriler (
    id INTEGER PRIMARY KEY,
    ad TEXT,
    yas INTEGER,
    gelir REAL,
    sehir TEXT
)
""")

cursor.execute("""
CREATE TABLE islemler (
    id INTEGER PRIMARY KEY,
    musteri_id INTEGER,
    tarih TEXT,
    tutar REAL,
    urun_kategori TEXT,
    FOREIGN KEY (musteri_id) REFERENCES musteriler(id)
)
""")

# Örnek Veri Setinin Enjeksiyonu
musteriler_data = [
    (1, 'Ahmet', 34, 75000, 'İstanbul'), (2, 'Ayşe', 28, 55000, 'Ankara'),
    (3, 'Mehmet', 45, 90000, 'İzmir'),    (4, 'Fatma', 38, 65000, 'İstanbul'),
    (5, 'Ali', 52, 110000, 'Bursa'),     (6, 'Zeynep', 31, 60000, 'Ankara')
]
cursor.executemany("INSERT INTO musteriler VALUES (?,?,?,?,?)", musteriler_data)

islemler_data = [
    (1, 1, '2024-01-15', 1200, 'Elektronik'), (2, 1, '2024-02-03', 450, 'Giyim'),
    (3, 2, '2024-01-20', 800, 'Elektronik'),  (4, 3, '2024-02-10', 2500, 'Mobilya'),
    (5, 4, '2024-01-25', 350, 'Giyim'),       (6, 5, '2024-02-15', 3200, 'Elektronik'),
    (7, 6, '2024-01-18', 600, 'Gıda')
]
cursor.executemany("INSERT INTO islemler VALUES (?,?,?,?,?)", islemler_data)
conn.commit()

# 2. Analitik Sorgulama: İlişkisel Birleştirme ve Agregasyon
sorgu = """
SELECT
    m.ad, m.yas, m.gelir, m.sehir,
    SUM(i.tutar) AS toplam_harcama,
    COUNT(i.id)  AS islem_sayisi,
    AVG(i.tutar) AS ort_tutar
FROM musteriler m
LEFT JOIN islemler i ON m.id = i.musteri_id
GROUP BY m.id
ORDER BY toplam_harcama DESC
"""

# Verinin Pandas DataFrame Yapısına Aktarılması
df = pd.read_sql_query(sorgu, conn)
print("--- Müşteri Harcama Profili Analizi ---")
print(df.to_string(index=False))

# 3. İstatistiksel Analiz: Değişkenler Arası Korelasyon
korelasyon = df['gelir'].corr(df['toplam_harcama'])
print(f"\nGelir - Toplam Harcama Korelasyonu: {korelasyon:.4f}")
