# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.7. Eksik ve Bozuk Veriyle Başa Çıkma Stratejileri › 3.1.7.3. KNN Imputation
# Kitap  : Kod 3.14 (KNN Imputation ile çok değişkenli eksik veri)
# Dosya : bolum03/03_01_07_03_knn-imputation.py
# Gerekli: pip install pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── KNN Imputation ─────────────────────────────────────────────
from sklearn.impute import KNNImputer
import pandas as pd, numpy as np

np.random.seed(42)
df_knn = pd.DataFrame({
    "gelir":       np.where(np.random.rand(150)<0.15,np.nan,np.random.normal(5000,1000,150)),
    "yas":         np.where(np.random.rand(150)<0.10,np.nan,np.random.randint(18,65,150).astype(float)),
    "egitim_yil":  np.where(np.random.rand(150)<0.08,np.nan,np.random.randint(8,20,150).astype(float)),
    "kredi_skoru": np.where(np.random.rand(150)<0.12,np.nan,np.random.randint(300,850,150).astype(float)),
})

knn = KNNImputer(n_neighbors=5, weights="distance")
df_dolu = pd.DataFrame(knn.fit_transform(df_knn), columns=df_knn.columns)

print("Eksik deger - Once vs Sonra:")
print(pd.DataFrame({"Once": df_knn.isnull().sum(), "Sonra": df_dolu.isnull().sum()}))

print("\nGelir Istatistikleri:")
print(pd.DataFrame({"Orijinal": df_knn["gelir"].describe(),
                    "KNN":      df_dolu["gelir"].describe()}).round(2))
