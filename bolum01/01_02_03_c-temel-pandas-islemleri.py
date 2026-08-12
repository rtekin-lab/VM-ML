# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.3. pandas — Yapısal Veri Analizi Kütüphanesi › C. Temel pandas İşlemleri
# Kitap  : Kod 1.23 (Temel inceleme) · Kod 1.24 (Seçim ve Filtreleme) · Kod 1.25 (Temel pandas İşlemleri) · Kod 1.26 (Pivot table — çift boyutlu özet) · Kod 1.27 (Eksik Veri yönetimi) · Kod 1.28 (Temel pandas İşlemleri) · Kod 1.29 (Zaman Serisi)
# Dosya : bolum01/01_02_03_c-temel-pandas-islemleri.py
# Gerekli: pip install numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import pandas as pd
import numpy as np

# ─── 1. Veri Yükleme ve İnceleme ─────────────────────────────────────────────
# CSV'den DataFrame oluşturma (McKinney 2022 Ch.5)
np.random.seed(42)
n = 500
df = pd.DataFrame({
    'ad'       : [f'Musteri_{i}' for i in range(n)],
    'yas'      : np.random.randint(18, 75, n),
    'gelir'    : np.abs(np.random.normal(55000, 20000, n)).round(2),
    'sehir'    : np.random.choice(['Istanbul','Ankara','Izmir','Bursa'], n),
    'kayit_tar': pd.date_range('2020-01-01', periods=n, freq='D'),
    'urun_kat' : np.random.choice(['Elektronik','Giyim','Gida','Ev'], n),
    'satin_alim': np.random.poisson(3, n),
})

# Temel inceleme
print(df.shape)         # (500, 7)
print(df.dtypes)        # sütun tipleri
print(df.describe())    # sayısal özet istatistikler
print(df.info())        # bellek kullanımı dahil özet

# ─── 2. Seçim ve Filtreleme ────────────────────────────────────────────────────
# loc: etiket bazlı; iloc: konuma dayalı (McKinney Ch.5)
ilk_5     = df.iloc[:5]                              # ilk 5 satır
genc_ist  = df.loc[(df['yas'] < 30) & (df['sehir'] == 'Istanbul')]
yuksek_gel= df[df['gelir'] > df['gelir'].quantile(0.90)]

print(f"İstanbul'daki genç müşteri: {len(genc_ist)}")
print(f"En yüksek %10 gelir: {len(yuksek_gel)} kişi, ortalama: {yuksek_gel['gelir'].mean():,.0f} TL")

# ─── 3. Gruplama ve Agregasyon ─────────────────────────────────────────────────
# GroupBy (McKinney Ch.10)
sehir_ozet = df.groupby('sehir').agg(
    musteri_say = ('ad', 'count'),
    ort_yas     = ('yas', 'mean'),
    ort_gelir   = ('gelir', 'mean'),
    toplam_alim = ('satin_alim', 'sum')
).round(2)
print(sehir_ozet)

# Pivot table — çift boyutlu özet
pivot = df.pivot_table(
    values='gelir',
    index='sehir',
    columns='urun_kat',
    aggfunc='mean'
).round(0)
print(pivot)

# ─── 4. Eksik Veri Yönetimi ────────────────────────────────────────────────────
# Eksiklik enjekte et
df.loc[np.random.choice(n, 50), 'gelir'] = np.nan
df.loc[np.random.choice(n, 30), 'yas']   = np.nan

print(f"Eksik değerler:\n{df.isnull().sum()}")

df['gelir_dolu'] = df['gelir'].fillna(df['gelir'].median())
df = df.dropna(subset=['yas'])   # yas eksik satırları sil
print(f"Temizleme sonrası: {df.shape}")

# ─── 5. Zaman Serisi ──────────────────────────────────────────────────────────
# (McKinney 2022 Ch.11)
df_ts = df.set_index('kayit_tar')
aylik = df_ts['gelir_dolu'].resample('ME').mean()   # pandas >= 2.2: 'M' yerine 'ME'
print(f"Aylık ortalama gelir (ilk 3 ay):\n{aylik.head(3)}")
print(f"\n=== pandas {pd.__version__} temel işlemleri tamamlandı ===")
