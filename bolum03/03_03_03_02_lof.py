# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.3. Yogunluk Tabanlı Anomali Tespit Yontemleri › 3.3.3.2. LOF (Local Outlier Factor)
# Kitap  : Kod 3.32 (LOF ile yerel aykırılık tespiti)
# Dosya : bolum03/03_03_03_02_lof.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# LOF (Local Outlier Factor) ile Anomali Tespiti
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor

np.random.seed(42)
kume1 = np.random.multivariate_normal([0,0],[[0.3,0],[0,0.3]],100)
kume2 = np.random.multivariate_normal([6,0],[[1.5,0],[0,1.5]], 50)
kume3 = np.random.multivariate_normal([3,5],[[0.5,0],[0,0.5]], 60)
anomali = np.array([[10,8],[-4,5],[3,-4],[8,-3],[-3,-5],[12,2]])
X = np.vstack([kume1, kume2, kume3, anomali])

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
tahmin = lof.fit_predict(X)
lof_skor = -lof.negative_outlier_factor_

print("Anomali sayisi: {}".format((tahmin==-1).sum()))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
normal_pts = X[tahmin==1]; anomali_pts = X[tahmin==-1]
axes[0].scatter(normal_pts[:,0], normal_pts[:,1], c="#3498db", s=20, alpha=0.7, label="Normal")
axes[0].scatter(anomali_pts[:,0],anomali_pts[:,1],c="#e74c3c", s=120, marker="X", label="Anomali")
axes[0].set_title("LOF Anomali Tespiti (k=20)"); axes[0].legend()
sc = axes[1].scatter(X[:,0], X[:,1], c=lof_skor, cmap="RdYlBu_r", s=lof_skor*5, alpha=0.7, vmin=1, vmax=5)
plt.colorbar(sc, ax=axes[1], label="LOF Skoru")
axes[1].set_title("LOF Skor Yogunlugu")
plt.tight_layout(); plt.show()
