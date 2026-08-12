# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.7. Eksik ve Bozuk Veriyle Başa Çıkma Stratejileri › 3.1.7.2. Tek Değişkenli İmputation
# Kitap  : Kod 3.13 (SimpleImputer ile ortalama, medyan ve mod ta)
# Dosya : bolum03/03_01_07_02_tek-degiskenli-imputation.py
# Gerekli: pip install pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── SimpleImputer ile tek degiskenli doldurma ───────────────────
from sklearn.impute import SimpleImputer
import pandas as pd, numpy as np

np.random.seed(42)
df_imp = pd.DataFrame({
    "gelir": np.where(np.random.rand(100)<0.15, np.nan,
                      np.random.normal(5000,1000,100)),
    "yas":   np.where(np.random.rand(100)<0.10, np.nan,
                      np.random.randint(18,65,100).astype(float)),
    "sehir": np.where(np.random.rand(100)<0.08, np.nan,
                      np.random.choice(["Ankara","Istanbul","Izmir"],100)),
})

imp_ort = SimpleImputer(strategy="mean")
imp_med = SimpleImputer(strategy="median")

gelir_ort = pd.Series(imp_ort.fit_transform(df_imp[["gelir"]]).ravel())
gelir_med = pd.Series(imp_med.fit_transform(df_imp[["gelir"]]).ravel())

print("Gelir Std Sapma Karsilastirmasi:")
print(f"  Orijinal        : {df_imp['gelir'].std():.4f}")
print(f"  Ortalama ile    : {gelir_ort.std():.4f}")
print(f"  Medyan ile      : {gelir_med.std():.4f}")

# Kategorik: mod
imp_mod = SimpleImputer(strategy="most_frequent")
sehir_d = pd.Series(imp_mod.fit_transform(df_imp[["sehir"]]).ravel())
print("\nSehir - Mod ile Doldurma:")
print(sehir_d.value_counts())
