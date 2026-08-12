# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 7
# Konum : BÖLÜM 7: GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME › 7.1. Kümeleme Analizi (Cluster Analysis) › 7.1.3. Yoğunluk Tabanlı Yöntemler (DBSCAN) › Python Uygulaması — DBSCAN ve HDBSCAN
# Kitap  : Kod 7.3 (DBSCAN ve HDBSCAN uygulaması)
# Dosya : bolum07/07_01_03_python-uygulamasi-dbscan-ve-hdbscan.py
# Gerekli: pip install hdbscan matplotlib numpy pandas scikit-learn
# ==========================================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons, make_circles, make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

# ─── 1. Şekil Bağımsız Kümeleme Testi ────────────────────────────
datasets = {
    "Hilal (Moons)"  : make_moons(n_samples=300, noise=0.05, random_state=42),
    "Halkalar (Circles)": make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42),
    "Kümeler"        : make_blobs(n_samples=300, centers=4, cluster_std=0.5, random_state=42),
}

params = {
    "Hilal (Moons)"     : {"eps": 0.3,  "min_samples": 5},
    "Halkalar (Circles)": {"eps": 0.35, "min_samples": 5},   # 0.2 cok kucuktu: 18 parca
    "Kümeler"           : {"eps": 0.5,  "min_samples": 5},
}

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

for col, (name, (X_d, _)) in enumerate(datasets.items()):
    X_sc_d = StandardScaler().fit_transform(X_d)

    # K-Means
    from sklearn.cluster import KMeans
    km_lbl = KMeans(n_clusters=2, random_state=42).fit_predict(X_sc_d)
    axes[0, col].scatter(X_sc_d[:,0], X_sc_d[:,1], c=km_lbl, cmap="tab10", s=20)
    axes[0, col].set_title(f"K-Means: {name}")

    # DBSCAN
    p = params[name]
    db_lbl = DBSCAN(**p).fit_predict(X_sc_d)
    n_clusters = len(set(db_lbl)) - (1 if -1 in db_lbl else 0)
    n_noise = (db_lbl == -1).sum()
    axes[1, col].scatter(X_sc_d[:,0], X_sc_d[:,1], c=db_lbl, cmap="tab10", s=20)
    axes[1, col].set_title(f"DBSCAN: {name}\n(K={n_clusters}, Gürültü={n_noise})")

plt.tight_layout(); plt.show()

# ─── 2. Parametre Izgarası ile DBSCAN Optimizasyonu ───────────────
X_bl, _ = make_blobs(n_samples=400, centers=4, cluster_std=0.7, random_state=42)
X_bl_sc = StandardScaler().fit_transform(X_bl)

results = []
for eps in [0.2, 0.3, 0.4, 0.5, 0.6, 0.8]:
    for min_pts in [3, 5, 7, 10]:
        lbl = DBSCAN(eps=eps, min_samples=min_pts).fit_predict(X_bl_sc)
        n_c = len(set(lbl)) - (1 if -1 in lbl else 0)
        n_n = (lbl == -1).sum()
        if n_c > 1:   # Silhouette gürültüsüz noktalarda hesaplanır
            mask = lbl != -1
            sil = silhouette_score(X_bl_sc[mask], lbl[mask]) if mask.sum() > 10 else 0
        else:
            sil = -1
        results.append({"eps": eps, "min_pts": min_pts,
                         "n_clusters": n_c, "n_noise": n_n, "sil": sil})

import pandas as pd
df_res = pd.DataFrame(results)
best = df_res.loc[df_res.sil.idxmax()]
print(f"En iyi params → eps={best.eps}, min_pts={best.min_pts:.0f}")
print(f"Kümeler: {best.n_clusters:.0f}, Gürültü: {best.n_noise:.0f}, Sil: {best.sil:.4f}")

# --- Python: HDBSCAN Uygulaması ---
# pip install hdbscan
import hdbscan

# --- Python: HDBSCAN Uygulaması ---
X_m, _ = make_moons(n_samples=400, noise=0.08, random_state=42)
X_m_sc = StandardScaler().fit_transform(X_m)

# --- Python: HDBSCAN Uygulaması ---
# HDBSCAN — ε yoktur; min_cluster_size yeterli
hdb = hdbscan.HDBSCAN(
    min_cluster_size=15,   # Minimum küme boyutu
    min_samples=5,         # Çekirdek nokta için min komşu
    cluster_selection_epsilon=0.0,  # 0 = tam hiyerarşik seçim
    prediction_data=True)

# --- Python: HDBSCAN Uygulaması ---
hdb_labels = hdb.fit_predict(X_m_sc)

# --- Python: HDBSCAN Uygulaması ---
n_clusters = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
n_noise = (hdb_labels == -1).sum()
print(f"HDBSCAN Kümeler: {n_clusters}, Gürültü Noktaları: {n_noise}")

# --- Python: HDBSCAN Uygulaması ---
# Yumuşak kümeleme — olasılık skoru
soft_clusters = hdbscan.all_points_membership_vectors(hdb)
print(f"İlk 5 noktanın küme üyelik olasılıkları:\n{soft_clusters[:5].round(3)}")

# --- Python: HDBSCAN Uygulaması ---
# Küme kararlılık skoru
print(f"Küme Kararlılıkları: {hdb.cluster_persistence_}")

# --- Python: HDBSCAN Uygulaması ---
# Görselleştirme
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# --- Python: HDBSCAN Uygulaması ---
sc1 = axes[0].scatter(X_m_sc[:,0], X_m_sc[:,1],
                      c=hdb_labels, cmap="tab10", s=30)
axes[0].set_title(f"HDBSCAN Etiketleri (K={n_clusters})")

# --- Python: HDBSCAN Uygulaması ---
# Renk = üyelik olasılığı
axes[1].scatter(X_m_sc[:,0], X_m_sc[:,1],
               c=hdb.probabilities_, cmap="viridis", s=30)
plt.colorbar(axes[1].scatter(X_m_sc[:,0], X_m_sc[:,1],
             c=hdb.probabilities_, cmap="viridis", s=30),
             ax=axes[1], label="Küme Olasılığı")
axes[1].set_title("HDBSCAN Yumuşak Kümeleme Olasılıkları")

# --- Python: HDBSCAN Uygulaması ---
plt.tight_layout(); plt.show()
