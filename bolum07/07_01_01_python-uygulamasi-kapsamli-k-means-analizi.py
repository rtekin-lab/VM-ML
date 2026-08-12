# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 7
# Konum : BÖLÜM 7: GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME › 7.1. Kümeleme Analizi (Cluster Analysis) › 7.1.1. Bölümlemeli Yöntemler: K-Means Algoritması › Python Uygulaması — Kapsamlı K-Means Analizi
# Kitap  : Kod 7.1 (K-Means: küme sayısı seçimi ve üç ölçütle de)
# Dosya : bolum07/07_01_01_python-uygulamasi-kapsamli-k-means-analizi.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================
# --- Python: Veri Hazırlama ve Temel K-Means ---
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.datasets import make_blobs, load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

# --- Python: Veri Hazırlama ve Temel K-Means ---
# ─── 1. Sentetik Veri Seti (4 doğal küme) ────────────────────────
X, y_true = make_blobs(
    n_samples=600, centers=4, cluster_std=0.85, random_state=42)

# --- Python: Veri Hazırlama ve Temel K-Means ---
# Kümeleme öncesi MUTLAKA standartlaştır
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Python: Veri Hazırlama ve Temel K-Means ---
# ─── 2. K Seçimi: Elbow + Silhouette + DBI ────────────────────────
wcss, sil_scores, dbi_scores = [], [], []
K_range = range(2, 12)

# --- Python: Veri Hazırlama ve Temel K-Means ---
for k in K_range:
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    wcss.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))
    dbi_scores.append(davies_bouldin_score(X_scaled, labels))

# --- Python: Veri Hazırlama ve Temel K-Means ---
print("K | WCSS      | Silhouette | DBI")
for i, k in enumerate(K_range):
    print(f"{k:2d}| {wcss[i]:9.2f}| {sil_scores[i]:10.4f}| {dbi_scores[i]:.4f}")

# --- Python: Veri Hazırlama ve Temel K-Means ---
# Grafik
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].plot(K_range, wcss, "o--", color="steelblue")
axes[0].set_title("Elbow Yöntemi (WCSS)")
axes[0].set_xlabel("K")
axes[0].set_ylabel("WCSS")

# --- Python: Veri Hazırlama ve Temel K-Means ---
axes[1].plot(K_range, sil_scores, "s--", color="forestgreen")
axes[1].set_title("Silhouette Skoru (↑ iyi)")
axes[1].set_xlabel("K")

# --- Python: Veri Hazırlama ve Temel K-Means ---
axes[2].plot(K_range, dbi_scores, "^--", color="crimson")
axes[2].set_title("Davies-Bouldin İndeksi (↓ iyi)")
axes[2].set_xlabel("K")

# --- Python: Veri Hazırlama ve Temel K-Means ---
plt.tight_layout()
plt.show()

import time
from sklearn.metrics import silhouette_samples

# ─── 3. En İyi K ile Nihai Model ─────────────────────────────────
best_k = 4   # Metriklerden belirlendi
final_km = KMeans(n_clusters=best_k, init="k-means++",
                  n_init=15, max_iter=300, random_state=42)
labels = final_km.fit_predict(X_scaled)

print(f"Nihai Model — K={best_k}")
print(f"  WCSS (Eylemsizlik): {final_km.inertia_:.2f}")
print(f"  Silhouette Skoru:   {silhouette_score(X_scaled, labels):.4f}")
print(f"  Davies-Bouldin:     {davies_bouldin_score(X_scaled, labels):.4f}")
print(f"  İterasyon Sayısı:   {final_km.n_iter_}")

# Küme boyutları
unique, counts = np.unique(labels, return_counts=True)
for c, n in zip(unique, counts):
    print(f"  Küme {c}: {n} örnek")

# ─── 4. Silhouette Görselleştirmesi ───────────────────────────────
sil_vals = silhouette_samples(X_scaled, labels)
avg_sil  = silhouette_score(X_scaled, labels)

fig, ax = plt.subplots(figsize=(8, 5))
y_lower = 10
cmap = plt.get_cmap("tab10")   # plt.cm.get_cmap matplotlib 3.11'de kaldirildi

for i in range(best_k):
    sil_i = np.sort(sil_vals[labels == i])
    size_i = sil_i.shape[0]
    y_upper = y_lower + size_i
    ax.fill_betweenx(np.arange(y_lower, y_upper), 0, sil_i,
                     facecolor=cmap(i), alpha=0.75)
    ax.text(-0.05, y_lower + 0.5 * size_i, f"Küme {i}")
    y_lower = y_upper + 10

ax.axvline(x=avg_sil, color="red", linestyle="--")
ax.set_title(f"Silhouette Grafiği (K={best_k}, Ort={avg_sil:.3f})")
ax.set_xlabel("Silhouette Katsayısı")
ax.set_ylabel("Küme Etiketi")
plt.tight_layout(); plt.show()

# ─── 5. Mini-Batch K-Means (Büyük Veri) ──────────────────────────
t0 = time.time()
km_full = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit(X_scaled)
print(f"KMeans süresi:       {time.time()-t0:.3f}s")

t0 = time.time()
mb_km = MiniBatchKMeans(n_clusters=best_k, batch_size=128,
                         n_init=10, random_state=42).fit(X_scaled)
print(f"MiniBatch KMeans:    {time.time()-t0:.3f}s")
print(f"MiniBatch Sil Skoru: {silhouette_score(X_scaled, mb_km.labels_):.4f}")
