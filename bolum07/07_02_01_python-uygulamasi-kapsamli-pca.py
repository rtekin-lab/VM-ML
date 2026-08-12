# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 7
# Konum : BÖLÜM 7: GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME › 7.2. Boyut İndirgeme (Dimensionality Reduction) › 7.2.1. Temel Bileşenler Analizi (PCA): Özvektör ve Özdeğer Matematiği › Python Uygulaması — Kapsamlı PCA
# Kitap  : Kod 7.4 (PCA: scree plot, yükleme haritası ve Kernel )
# Dosya : bolum07/07_02_01_python-uygulamasi-kapsamli-pca.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================
# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, KernelPCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer, load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
# ─── 1. Veri Hazırlama ────────────────────────────────────────────
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = data.feature_names

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
scaler = StandardScaler()
X_sc = scaler.fit_transform(X)         # Standardizasyon zorunlu!

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
# ─── 2. Scree Plot — Bileşen Sayısı Seçimi ──────────────────────
pca_full = PCA(n_components=None)       # Tüm bileşenler
pca_full.fit(X_sc)

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
evr = pca_full.explained_variance_ratio_
cum_evr = np.cumsum(evr)

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
# Scree Plot (özdeğer grafiği)
axes[0].bar(range(1, len(evr)+1), evr, alpha=0.7, color="steelblue")
axes[0].step(range(1, len(evr)+1), cum_evr, color="crimson", linewidth=2)
axes[0].axhline(y=0.95, color="green", linestyle="--", label="%95 Varyans")
axes[0].set_title("Scree Plot — Açıklanan Varyans")
axes[0].set_xlabel("Bileşen Sayısı")
axes[0].set_ylabel("Varyans Oranı")
axes[0].legend()

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
# Kümülatif varyans
k_95 = np.argmax(cum_evr >= 0.95) + 1
k_80 = np.argmax(cum_evr >= 0.80) + 1
print(f"%80 varyans için gereken bileşen: {k_80} / {X.shape[1]}")
print(f"%95 varyans için gereken bileşen: {k_95} / {X.shape[1]}")

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
# Yükleme haritası — PC1 ve PC2 hangi özellikleri taşıyor?
pca_k = PCA(n_components=k_80)
X_pca = pca_k.fit_transform(X_sc)

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
loadings_df = pd.DataFrame(
    pca_k.components_[:2].T,
    index=feature_names,
    columns=["PC1", "PC2"]
)
axes[1].imshow(loadings_df.values, cmap="RdBu_r", aspect="auto")
axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(["PC1", "PC2"])
axes[1].set_yticks(range(len(feature_names)))
axes[1].set_yticklabels(feature_names, fontsize=7)
axes[1].set_title("PCA Yükleme Haritası (PC1–PC2)")

# --- Python: PCA — Scree Plot, Bileşen Seçimi ve Yorumlama ---
plt.tight_layout(); plt.show()

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# ─── 3. PCA + Sınıflandırıcı Pipeline ───────────────────────────
# PCA'nın model performansına katkısını ölç
from sklearn.model_selection import cross_val_score

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
results = {}
for n_comp in [2, 5, 10, k_80, X.shape[1]]:
    if n_comp == X.shape[1]:
        pipe = Pipeline([("scaler", StandardScaler()),
                          ("clf",    LogisticRegression(max_iter=1000))])
        label = f"Tüm boyutlar ({n_comp})"
    else:
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("pca",    PCA(n_components=n_comp)),
            ("clf",    LogisticRegression(max_iter=1000))
        ])
        label = f"PCA({n_comp})"
    score = cross_val_score(pipe, X, y, cv=5, scoring="roc_auc").mean()
    results[label] = score
    print(f"{label:25s}: ROC-AUC = {score:.4f}")

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# ─── 4. Kernel PCA — Doğrusal Olmayan Projeksiyon ────────────────
from sklearn.decomposition import KernelPCA

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# RBF kernel ile doğrusal olmayan projeksiyon
kpca = KernelPCA(
    n_components=2,
    kernel="rbf",
    gamma=0.05,
    fit_inverse_transform=True)   # Yeniden yapılandırma için

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
X_kpca = kpca.fit_transform(X_sc)

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# Orijinal (ilk 2 özellik)
axes[0].scatter(X_sc[:, 0], X_sc[:, 1], c=y, cmap="Set1", alpha=0.6, s=20)
axes[0].set_title("Orijinal (ilk 2 özellik)")

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# Standart PCA
X_std_pca = PCA(n_components=2).fit_transform(X_sc)
axes[1].scatter(X_std_pca[:, 0], X_std_pca[:, 1], c=y, cmap="Set1", alpha=0.6, s=20)
axes[1].set_title("Standart PCA (2 bileşen)")

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# Kernel PCA
axes[2].scatter(X_kpca[:, 0], X_kpca[:, 1], c=y, cmap="Set1", alpha=0.6, s=20)
axes[2].set_title("Kernel PCA (RBF kernel)")

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
for ax in axes:
    ax.set_xlabel("Boyut 1")
    ax.set_ylabel("Boyut 2")
plt.tight_layout(); plt.show()

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# ─── 5. PCA ile Gürültü Azaltma ──────────────────────────────────
digits = load_digits()
X_dig = StandardScaler().fit_transform(digits.data)

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
# %95 varyansı koruyarak boyut indir ve geri yansıt
pca_dn = PCA(n_components=0.95, svd_solver="full")
X_dn = pca_dn.fit_transform(X_dig)
X_reconstructed = pca_dn.inverse_transform(X_dn)

# --- Python: PCA ile Lojistik Regresyon Pipeline ve Kernel PCA ---
print(f"Orijinal boyut: {X_dig.shape[1]}")
print(f"Sıkıştırılmış boyut: {X_dn.shape[1]} (%95 varyans korunuyor)")
print(f"Sıkıştırma oranı: {X_dn.shape[1]/X_dig.shape[1]:.2%}")
