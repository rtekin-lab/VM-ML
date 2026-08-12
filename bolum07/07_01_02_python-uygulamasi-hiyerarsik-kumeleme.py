# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 7
# Konum : BÖLÜM 7: GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME › 7.1. Kümeleme Analizi (Cluster Analysis) › 7.1.2. Hiyerarşik Kümeleme: Dendrogramlar ve Bağlantı Türleri › Python Uygulaması — Hiyerarşik Kümeleme
# Kitap  : Kod 7.2 (Hiyerarşik kümeleme: dendrogram ve bağlantı )
# Dosya : bolum07/07_01_02_python-uygulamasi-hiyerarsik-kumeleme.py
# Gerekli: pip install matplotlib numpy scikit-learn scipy
# ==========================================================================
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np

# ─── 1. Veri ──────────────────────────────────────────────────────
X, _ = make_blobs(n_samples=200, centers=4,
                   cluster_std=0.6, random_state=42)
X_sc = StandardScaler().fit_transform(X)

# ─── 2. Dendrogram Çizimi (Ward bağlantısı) ──────────────────────
linkage_matrix = sch.linkage(X_sc, method="ward")

plt.figure(figsize=(14, 6))
sch.dendrogram(
    linkage_matrix,
    truncate_mode="lastp",   # Yalnızca son p birleşimi göster
    p=30,
    leaf_rotation=90,
    leaf_font_size=10,
    show_contracted=True
)
plt.title("Agglomerative Kümeleme Dendrogramı (Ward Bağlantısı)")
plt.xlabel("Veri Noktaları (veya Alt Küme Boyutu)")
plt.ylabel("Birleşme Mesafesi (Ward)")
# Kesim seviyesini dendrogram üzerine işaretle
plt.axhline(y=6.5, color="red", linestyle="--", linewidth=2, label="K=4 kesim")
plt.legend(); plt.tight_layout(); plt.show()

# ─── 3. Dört Bağlantı Türünü Karşılaştır ─────────────────────────
linkages = ["ward", "complete", "average", "single"]

# Bagalanti olcutlerinin FARKINI gorebilmek icin anizotropik ve degisken
# yogunluklu veri gerekir. Kusursal, esit yayilimli kumelerde dort olcut de
# ayni sonucu verir ve karsilastirma ogretici olmaz.
X_anz, _ = make_blobs(n_samples=200, centers=4,
                       cluster_std=[1.0, 2.5, 0.5, 1.5], random_state=42)
X_anz = X_anz @ np.array([[0.6, -0.6], [-0.4, 0.85]])   # egme donusumu
X_anz_sc = StandardScaler().fit_transform(X_anz)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, linkage_type in zip(axes, linkages):
    agg = AgglomerativeClustering(
        n_clusters=4, metric="euclidean", linkage=linkage_type)
    labels = agg.fit_predict(X_anz_sc)
    sil = silhouette_score(X_anz_sc, labels)
    ax.scatter(X_anz_sc[:, 0], X_anz_sc[:, 1], c=labels, cmap="tab10", s=30)
    ax.set_title(f"{linkage_type.capitalize()} Linkage\nSil={sil:.3f}")
    ax.set_xticks([]); ax.set_yticks([])

plt.tight_layout(); plt.show()

# ─── 4. Farklı K Değerleri için Silhouette Karşılaştırması ───────
K_vals = range(2, 10)
sil_ward = []

for k in K_vals:
    agg = AgglomerativeClustering(n_clusters=k, linkage="ward")
    lbl = agg.fit_predict(X_sc)
    sil_ward.append(silhouette_score(X_sc, lbl))

best_k = K_vals[np.argmax(sil_ward)]
print(f"Ward + Silhouette ile optimal K: {best_k}")

# ─── 5. Mesafe Matrisine Dayalı Kümeleme (cosine metriği) ─────────
# Ward yalnızca Euclidean destekler; farklı metrik için average/complete kullan
agg_cos = AgglomerativeClustering(
    n_clusters=4, metric="cosine", linkage="average")
labels_cos = agg_cos.fit_predict(X_sc)
print(f"Cosine metric Silhouette: {silhouette_score(X_sc, labels_cos):.4f}")
