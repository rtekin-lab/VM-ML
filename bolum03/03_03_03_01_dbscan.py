# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.3. Yogunluk Tabanlı Anomali Tespit Yontemleri › 3.3.3.1. DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
# Kitap  : Kod 3.31 (DBSCAN ile anomali tespiti)
# Dosya : bolum03/03_03_03_01_dbscan.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# DBSCAN ile Anomali Tespiti
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

np.random.seed(42)
theta = np.linspace(0, 2*np.pi, 200)
r1 = 3 + np.random.normal(0, 0.3, 200)
ring1 = np.c_[r1*np.cos(theta), r1*np.sin(theta)]
blob1 = np.random.multivariate_normal([0,0],[[0.5,0],[0,0.5]],150)
blob2 = np.random.multivariate_normal([7,3],[[0.8,0],[0,0.8]],100)
anomali = np.array([[6,0],[8,-2],[-4,5],[-5,-4],[9,6],[-6,3]])
X = np.vstack([ring1, blob1, blob2, anomali])
X_s = StandardScaler().fit_transform(X)

# k-Mesafe grafigi ile epsilon secimi
knn = NearestNeighbors(n_neighbors=5).fit(X_s)
mesafeler, _ = knn.kneighbors(X_s)
kinci_dist = np.sort(mesafeler[:,4])[::-1]

dbscan = DBSCAN(eps=0.3, min_samples=5)
etiketler = dbscan.fit_predict(X_s)
n_kume = len(set(etiketler)) - (1 if -1 in etiketler else 0)
n_anom = (etiketler == -1).sum()
print("Kume sayisi : {}".format(n_kume))
print("Anomali     : {}".format(n_anom))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(kinci_dist, color="#3498db")
ax1.axhline(0.3, color="red", linestyle="--", label="eps=0.3")
ax1.set_title("k-Mesafe Grafigi (eps secimi)"); ax1.legend()
for lbl in set(etiketler):
    pts = X[etiketler==lbl]
    c = "#e74c3c" if lbl==-1 else plt.cm.tab10(lbl%10)
    ax2.scatter(pts[:,0],pts[:,1],c=[c],s=15 if lbl!=-1 else 80,
                marker="o" if lbl!=-1 else "X",
                label="Anomali" if lbl==-1 else "Kume {}".format(lbl))
ax2.set_title("DBSCAN (eps=0.3, MinPts=5)"); ax2.legend(fontsize=8)
plt.tight_layout(); plt.show()
