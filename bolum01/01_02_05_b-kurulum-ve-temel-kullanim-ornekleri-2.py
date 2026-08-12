# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.5. SciPy — Bilimsel Hesaplama Kütüphanesi › B. Kurulum ve Temel Kullanım Örnekleri
# Kitap  : Kod 1.37 (Kurulum ve Temel Kullanım örnekleri) · Kod 1.38 (Shapiro-Wilk normallik testi) · Kod 1.39 (SciPy.optimize: Eğri Uydurma) · Kod 1.40 (Kurulum ve Temel Kullanım örnekleri)
# Dosya : bolum01/01_02_05_b-kurulum-ve-temel-kullanim-ornekleri-2.py
# Gerekli: pip install numpy scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
from scipy import stats, optimize, linalg

# ─── 1. scipy.stats: İstatistiksel Testler ────────────────────────────────────
np.random.seed(42)
# Bağımsız iki örneklem t-testi
grup_a = np.random.normal(75, 10, 50)   # Kontrol grubu
grup_b = np.random.normal(80, 12, 50)   # Deney grubu

t_ist, p_deg = stats.ttest_ind(grup_a, grup_b)
print(f"t-testi: t={t_ist:.4f}, p={p_deg:.4f}")
print(f"H0 {'reddedildi' if p_deg < 0.05 else 'reddedilemedi'} (α=0.05)")

# Cohen's d etki büyüklüğü
# d = (μ₁ - μ₂) / σ_ortak
sigma_ort = np.sqrt(((len(grup_a)-1)*grup_a.std()**2 +
                     (len(grup_b)-1)*grup_b.std()**2) /
                    (len(grup_a)+len(grup_b)-2))
cohens_d = (grup_b.mean() - grup_a.mean()) / sigma_ort
print(f"Cohen's d = {cohens_d:.3f}  ({'büyük' if abs(cohens_d)>0.8 else 'orta' if abs(cohens_d)>0.5 else 'küçük'} etki)")

# Shapiro-Wilk normallik testi
w_ist, p_normallik = stats.shapiro(grup_a)
print(f"Normallik testi (Shapiro-Wilk): W={w_ist:.4f}, p={p_normallik:.4f}")

# ─── 2. scipy.linalg: Tekil Değer Ayrışımı (SVD) ─────────────────────────────
# SVD: PCA ve öneri sistemlerinin matematiği
A = np.random.randn(10, 6)           # 10×6 veri matrisi
U, s, Vt = linalg.svd(A, full_matrices=False)
# A ≈ U @ diag(s) @ Vt
print(f"\nSVD: U{U.shape}, s{s.shape}, Vt{Vt.shape}")
print(f"Tekil değerler: {s.round(2)}")
aciklanan_var = s**2 / np.sum(s**2)
print(f"Açıklanan varyans (ilk 3 bileşen): {aciklanan_var[:3].sum()*100:.1f}%")

# ─── 3. scipy.optimize: Eğri Uydurma ─────────────────────────────────────────
# Lojistik büyüme modeli uydurma
def lojistik(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

x_veri = np.linspace(0, 10, 50)
y_gercek = lojistik(x_veri, L=100, k=1.5, x0=5)
y_gurultulu = y_gercek + np.random.normal(0, 3, 50)

params, cov = optimize.curve_fit(lojistik, x_veri, y_gurultulu, p0=[90, 1, 5])
L_est, k_est, x0_est = params
print(f"\nLojistik parametreler: L={L_est:.2f}, k={k_est:.2f}, x0={x0_est:.2f}")
