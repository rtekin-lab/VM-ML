# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.7. Eksik ve Bozuk Veriyle Başa Çıkma Stratejileri › 3.1.7.4. MICE (Multiple Imputation by Chained Equations)
# Kitap  : Kod 3.15 (MICE algoritması ile çoklu atama (IterativeI)
# Dosya : bolum03/03_01_07_04_mice.py
# Gerekli: pip install pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── MICE: sklearn IterativeImputer ─────────────────────────────
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
import pandas as pd, numpy as np

np.random.seed(42)
df_m = pd.DataFrame({
    "gelir":      np.where(np.random.rand(200)<0.15,np.nan,np.random.normal(5000,1200,200)),
    "yas":        np.where(np.random.rand(200)<0.10,np.nan,np.random.randint(18,65,200).astype(float)),
    "egitim_yil": np.where(np.random.rand(200)<0.08,np.nan,np.random.randint(8,20,200).astype(float)),
})

mice = IterativeImputer(
    estimator=BayesianRidge(),
    max_iter=10,
    random_state=42,
    imputation_order="ascending"
)
df_m_dolu = pd.DataFrame(mice.fit_transform(df_m), columns=df_m.columns)

print("Gelir - MICE sonrasi istatistikler:")
print(pd.DataFrame({"Orijinal": df_m["gelir"].describe(),
                    "MICE":     df_m_dolu["gelir"].describe()}).round(2))
print(f"\nMICE sonrasi kalan eksik deger: {df_m_dolu.isnull().sum().sum()}")
