# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.8. Kapsamlı Örnek: Uçtan Uca Veri Kalite Pipeline'ı
# Kitap  : Kod 3.16 (Uçtan uca veri kalite boru hattı: IQR temizl)
# Dosya : bolum03/03_01_08_kapsamli-ornek-uctan-uca-veri-kalite-pipeline-i.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Uctan Uca Veri Kalite Pipeline ─────────────────────────────
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings("ignore")

# 1) Kirli veri seti simulasyonu
np.random.seed(42)
n = 300
df_ham = pd.DataFrame({
    "musteri_id": range(1, n+1),
    "yas": np.concatenate([np.random.randint(18,65,n-10).astype(float),
                           [np.nan]*5, [-3,999,0,200,1500]]),
    "gelir": np.where(np.random.rand(n)<0.12, np.nan,
                      np.random.lognormal(8.5,0.6,n)),
    "harcama": np.where(np.random.rand(n)<0.08, np.nan,
                         np.random.normal(3000,800,n)),
    "sehir": np.where(np.random.rand(n)<0.07, np.nan,
                       np.random.choice(["Ankara","Istanbul","Izmir"],n)),
})

# 2) Kalite raporu fonksiyonu
def kalite_raporu(df, baslik):
    print(f"\n{'='*55}")
    print(f"  {baslik}  |  {len(df)} satir, {len(df.columns)} sutun")
    print(f"{'='*55}")
    eksik = df.isnull().sum()
    if eksik.any():
        for col, ne in eksik[eksik>0].items():
            print(f"  {col:15s}: {ne} eksik ({ne/len(df)*100:.1f}%)")
    else:
        print("  Tum degerler tam!")

kalite_raporu(df_ham, "HAM VERI")

# 3) IQR ile aykiri degerleri maskele
def iqr_maskele(df, col, k=1.5):
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    maske = (df[col] < Q1-k*IQR) | (df[col] > Q3+k*IQR)
    if maske.sum() > 0:
        print(f"  {col}: {maske.sum()} aykiri NaN yapildi")
    df.loc[maske, col] = np.nan
    return df

df_temiz = df_ham.copy()
print("\nAykiri Deger Temizleme:")
for col in ["yas","gelir","harcama"]:
    df_temiz = iqr_maskele(df_temiz, col)

# 4) Tekrarli kayitlari kaldir
n_once = len(df_temiz)
df_temiz = df_temiz.drop_duplicates(subset="musteri_id")
print(f"\nTekrarli kayit: {n_once-len(df_temiz)}")

# 5) Eksik degerleri doldur (KNN + mod)
sayisal = ["yas","gelir","harcama"]
kategorik = ["sehir"]

knn = KNNImputer(n_neighbors=5, weights="distance")
df_temiz[sayisal] = knn.fit_transform(df_temiz[sayisal])

for col in kategorik:
    mod = df_temiz[col].mode()[0]
    df_temiz[col] = df_temiz[col].fillna(mod)

# 6) Son kalite raporu
kalite_raporu(df_temiz, "TEMIZLENMIS VERI")

print(f"\nOzet:")
print(f"  Orijinal satir       : {len(df_ham)}")
print(f"  Temiz veri satir     : {len(df_temiz)}")
print(f"  Kalan eksik deger    : {df_temiz.isnull().sum().sum()}")
