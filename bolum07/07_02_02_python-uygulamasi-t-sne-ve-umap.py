# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 7
# Konum : BÖLÜM 7: GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME › 7.2. Boyut İndirgeme (Dimensionality Reduction) › 7.2.2. t-SNE ve UMAP: Modern Doğrusal Olmayan Görselleştirme Yöntemleri › Python Uygulaması — t-SNE ve UMAP
# Kitap  : Kod 7.5 (t-SNE ve UMAP ile doğrusal olmayan gömme) · Kod 7.6 (umap-learn kurulumu)
# Dosya : bolum07/07_02_02_python-uygulamasi-t-sne-ve-umap.py
# Gerekli: pip install matplotlib numpy scikit-learn umap-learn
# ==========================================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits, load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ─── 1. Veri: Digits (8x8 piksel el yazısı rakamları) ─────────────
digits = load_digits()
X_dig = digits.data        # 1797 örnek, 64 özellik (piksel)
y_dig = digits.target      # 0–9 etiketleri

# Standartlaştır
X_dig_sc = StandardScaler().fit_transform(X_dig)

# ─── 2. t-SNE öncesinde PCA ile ön boyut indirgeme (hız için) ─────
# t-SNE için önerilen: önce PCA ile 50 bileşene indir, sonra t-SNE uygula
pca_pre = PCA(n_components=30, random_state=42)
X_pca_pre = pca_pre.fit_transform(X_dig_sc)
print(f"PCA ön işleme: 64 → 30 boyut, {pca_pre.explained_variance_ratio_.sum():.1%} varyans korundu")

# ─── 3. Farklı Perplexity Değerlerini Karşılaştır ─────────────────
perplexities = [5, 15, 30, 50]
fig, axes = plt.subplots(1, 4, figsize=(20, 4))

for ax, perp in zip(axes, perplexities):
    tsne = TSNE(
        n_components=2,
        perplexity=perp,
        learning_rate="auto",
        init="pca",            # PCA başlatma daha kararlı
        max_iter=1000,
        random_state=42)
    X_tsne = tsne.fit_transform(X_pca_pre)

    sc = ax.scatter(X_tsne[:, 0], X_tsne[:, 1],
                    c=y_dig, cmap="tab10", s=8, alpha=0.7)
    ax.set_title(f"t-SNE perplexity={perp}")
    ax.axis("off")

plt.colorbar(sc, ax=axes[-1], label="Rakam")
plt.suptitle("Digits Veri Seti: t-SNE Perplexity Karşılaştırması", y=1.02)
plt.tight_layout(); plt.show()

# ─── 4. PCA vs t-SNE Karşılaştırması ─────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# PCA
X_pca2 = PCA(n_components=2, random_state=42).fit_transform(X_dig_sc)
ax1.scatter(X_pca2[:, 0], X_pca2[:, 1], c=y_dig, cmap="tab10", s=10, alpha=0.7)
ax1.set_title("PCA (2 bileşen)")
ax1.axis("off")

# t-SNE (optimal ayarlar)
tsne_best = TSNE(n_components=2, perplexity=30, init="pca",
                  learning_rate="auto", max_iter=1500, random_state=42)
X_tsne_best = tsne_best.fit_transform(X_pca_pre)
ax2.scatter(X_tsne_best[:, 0], X_tsne_best[:, 1],
            c=y_dig, cmap="tab10", s=10, alpha=0.7)
ax2.set_title("t-SNE (perplexity=30, max_iter=1500)")
ax2.axis("off")

plt.suptitle("PCA vs t-SNE: Digits Görselleştirme")
plt.tight_layout(); plt.show()

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
# pip install umap-learn
import umap
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_digits

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
# ─── 1. Temel UMAP Uygulaması ─────────────────────────────────────
digits = load_digits()
X_dig_sc = StandardScaler().fit_transform(digits.data)

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
umap_viz = umap.UMAP(
    n_components=2,
    n_neighbors=15,        # Lokal komşuluk boyutu
    min_dist=0.1,          # Minimum küme sıkışıklığı
    metric="euclidean",
    random_state=42)

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
X_umap = umap_viz.fit_transform(X_dig_sc)

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
plt.figure(figsize=(8, 6))
sc = plt.scatter(X_umap[:, 0], X_umap[:, 1],
                 c=digits.target, cmap="tab10", s=10, alpha=0.8)
plt.colorbar(sc, label="Rakam")
plt.title("UMAP: Digits Veri Seti (n_neighbors=15, min_dist=0.1)")
plt.axis("off"); plt.tight_layout(); plt.show()

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
# ─── 2. n_neighbors ve min_dist Etkisi ───────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
params = [(5, 0.0), (15, 0.1), (50, 0.5),
           (15, 0.0), (15, 0.5), (15, 0.99)]

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
for ax, (nn, md) in zip(axes.ravel(), params):
    um = umap.UMAP(n_neighbors=nn, min_dist=md,
                    n_components=2, random_state=42)
    X_um = um.fit_transform(X_dig_sc)
    ax.scatter(X_um[:,0], X_um[:,1], c=digits.target,
               cmap="tab10", s=5, alpha=0.7)
    ax.set_title(f"n_neighbors={nn}, min_dist={md}")
    ax.axis("off")

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
plt.suptitle("UMAP Hiperparametre Etkisi")
plt.tight_layout(); plt.show()

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
# ─── 3. UMAP Projeksiyon — Yeni Veri Noktası Dönüştürme ──────────
# UMAP'ın t-SNE'ye büyük üstünlüğü: transform() methodu
from sklearn.model_selection import train_test_split

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
X_tr, X_te, y_tr, y_te = train_test_split(
    X_dig_sc, digits.target, test_size=0.2, random_state=42)

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
umap_pipe = umap.UMAP(n_components=10, n_neighbors=15,
                       random_state=42)
X_tr_umap = umap_pipe.fit_transform(X_tr)   # Sadece train üzerinde fit!
X_te_umap = umap_pipe.transform(X_te)        # Test verisini dönüştür

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
print(f"UMAP projeksiyon: {X_tr.shape[1]} → {X_tr_umap.shape[1]} boyut")

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
# ─── 4. UMAP + Sınıflandırıcı Pipeline ──────────────────────────
# UMAP sklearn API uyumlu — Pipeline içinde kullanılabilir
pipe_umap = Pipeline([
    ("scaler", StandardScaler()),
    ("umap",   umap.UMAP(n_components=10, n_neighbors=15, random_state=42)),
    ("clf",    RandomForestClassifier(n_estimators=100, random_state=42))
])

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
pipe_baseline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf",    RandomForestClassifier(n_estimators=100, random_state=42))
])

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
score_umap     = cross_val_score(pipe_umap,     digits.data, digits.target,
                                  cv=5, scoring="accuracy").mean()
score_baseline = cross_val_score(pipe_baseline, digits.data, digits.target,
                                  cv=5, scoring="accuracy").mean()

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
print(f"Tüm boyutlarla RF:         {score_baseline:.4f}")
print(f"UMAP(10D) + RF:            {score_umap:.4f}")

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
# ─── 5. PCA + t-SNE + UMAP Kapsamlı Karşılaştırma ───────────────
from sklearn.manifold import TSNE

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
cancer = load_breast_cancer()
X_c = StandardScaler().fit_transform(cancer.data)

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
methods = {
    "PCA (2D)"  : PCA(n_components=2, random_state=42),
    "t-SNE (2D)": TSNE(n_components=2, perplexity=30,
                        init="pca", random_state=42),
    "UMAP (2D)" : umap.UMAP(n_components=2, n_neighbors=15,
                             min_dist=0.1, random_state=42),
}

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, (name, model) in zip(axes, methods.items()):
    X_2d = model.fit_transform(X_c)
    ax.scatter(X_2d[:,0], X_2d[:,1],
               c=cancer.target, cmap="Set1", s=15, alpha=0.8)
    ax.set_title(f"{name}")
    ax.axis("off")

# --- Python: UMAP — Uygulama ve Pipeline Entegrasyonu ---
plt.suptitle("PCA vs t-SNE vs UMAP: Breast Cancer Görselleştirme")
plt.tight_layout(); plt.show()
