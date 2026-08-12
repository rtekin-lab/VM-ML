# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.7. Kapsamlı Ornek: Uctan Uca Anomali Tespit Pipeline'ı
# Kitap  : Kod 3.37 (Uçtan uca banka işlemi anomali tespiti: topl)
# Dosya : bolum03/03_03_07_kapsamli-ornek-uctan-uca-anomali-tespit-pipeline.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# Uctan Uca Anomali Tespit Pipeline'ı — Banka Islemi Senaryosu
import numpy as np, pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, classification_report
import matplotlib.pyplot as plt
import warnings; warnings.filterwarnings("ignore")

np.random.seed(42)
n = 2000
df = pd.DataFrame({
    "tutar":  np.concatenate([np.random.lognormal(5,1,int(n*0.97)),np.random.uniform(5000,20000,int(n*0.03))]),
    "saat":   np.concatenate([np.random.randint(8,22,int(n*0.97)),np.random.randint(0,6,int(n*0.03))]).astype(float),
    "gun_is": np.concatenate([np.random.poisson(3,int(n*0.97)),np.random.poisson(25,int(n*0.03))]).astype(float),
    "yabanci":np.concatenate([np.zeros(int(n*0.97)),np.ones(int(n*0.03))]),
    "etiket": np.concatenate([np.zeros(int(n*0.97)),np.ones(int(n*0.03))]),
})
df["log_tutar"] = np.log1p(df["tutar"])
df["gece"]      = ((df["saat"]<6)|(df["saat"]>23)).astype(int)

ozl = ["log_tutar","saat","gun_is","yabanci","gece"]
X = StandardScaler().fit_transform(df[ozl].values)
y = df["etiket"].values

# Ensemble skor
skor_if  = -IsolationForest(contamination=0.03,random_state=42).fit(X).decision_function(X)
skor_lof = -LocalOutlierFactor(n_neighbors=20).fit(X).negative_outlier_factor_
skor_if_n  = (skor_if -skor_if.min())/(skor_if.max()-skor_if.min())
skor_lof_n = (skor_lof-skor_lof.min())/(skor_lof.max()-skor_lof.min())
skor_ens   = (skor_if_n + skor_lof_n) / 2

# Esik optimizasyonu
esikler = np.linspace(0.3, 0.9, 100)
en_iyi_f1, en_iyi_esik = 0, 0.5
for e in esikler:
    pred = (skor_ens > e).astype(int)
    f1 = f1_score(y.astype(int), pred, zero_division=0)
    if f1 > en_iyi_f1: en_iyi_f1, en_iyi_esik = f1, e

tahmin = (skor_ens > en_iyi_esik).astype(int)
print("Optimal esik: {:.3f} | F1: {:.4f}".format(en_iyi_esik, en_iyi_f1))
print(classification_report(y.astype(int), tahmin, target_names=["Normal","Anomali"]))
