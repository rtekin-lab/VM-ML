# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.2. NumPy — Sayısal Hesaplama Kütüphanesi › C. NumPy Temel İşlemler — Veri Bilimi Perspektifi
# Kitap  : Kod 1.14 (Bellek hesabı: 2×3×8 = 48 byte (denklem 1.4)) · Kod 1.15 (Z-skoru vektörleştirme (denklem 1.6)) · Kod 1.16 (Lineer Cebir) · Kod 1.17 (Özdeğer ayrışımı (PCA'nın matematiksel temel) · Kod 1.18 (Vektörleştirme vs. Döngü Hız karşılaştırması) · Kod 1.19 (Python döngüsü) · Kod 1.20 (NumPy vektörleştirilmiş) · Kod 1.21 (NumPy Temel İşlemler — Veri Bilimi Perspekti) · Kod 1.22 (NumPy Temel İşlemler — Veri Bilimi Perspekti)
# Dosya : bolum01/01_02_02_c-numpy-temel-islemler-veri-bilimi-perspektifi.py
# Gerekli: pip install numpy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np

# ─── 1. ndarray Oluşturma ─────────────────────────────────────────────────────
a = np.array([1.5, 2.3, 3.7, 4.1, 5.9])          # 1B vektör (float64)
M = np.array([[1, 2, 3], [4, 5, 6]], dtype=float) # 2B matris
T = np.zeros((3, 4, 5))                           # Sıfır tensör (3×4×5)
R = np.random.randn(100, 10)                      # Normal dağılım örnekleri

print(f"a.shape={a.shape}, M.shape={M.shape}, T.shape={T.shape}")
print(f"a.dtype={a.dtype}, M.nbytes={M.nbytes} byte")
# Bellek hesabı: 2×3×8 = 48 byte (denklem 1.4)

# ─── 2. İstatistiksel İşlemler (veri ön işleme için kritik) ──────────────────
veri = np.random.normal(loc=50, scale=10, size=1000)   # N(50,10²) örneklem
print(f"Ortalama  : {veri.mean():.4f}")
print(f"Std sapma : {veri.std():.4f}")
print(f"Medyan    : {np.median(veri):.4f}")
print(f"Q1, Q3    : {np.percentile(veri, 25):.2f}, {np.percentile(veri, 75):.2f}")

# Z-skoru vektörleştirme (denklem 1.6)
# z_i = (x_i - μ) / σ  — tam N eleman için Python döngüsü yok
z = (veri - veri.mean()) / veri.std()
print(f"Z-skor aralığı: [{z.min():.2f}, {z.max():.2f}]")

# ─── 3. Lineer Cebir ──────────────────────────────────────────────────────────
A = np.array([[3, 1], [1, 2]], dtype=float)
b = np.array([9, 8], dtype=float)
x = np.linalg.solve(A, b)     # Ax = b çözümü
print(f"Ax=b çözümü: x = {x}")       # [2. 3.]

# Özdeğer ayrışımı (PCA'nın matematiksel temeli)
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"Özdeğerler: {eigenvalues}")

# Matris çarpımı — broadcasting ile verimli
W = np.random.randn(10, 5)   # 10×5 ağırlık matrisi
X = np.random.randn(100, 10) # 100×10 veri matrisi
Y = X @ W                    # 100×5 sonuç (numpy BLAS kullanır)
print(f"Y.shape = {Y.shape}")

# ─── 4. Vektörleştirme vs. Döngü Hız Karşılaştırması ─────────────────────────
import time
n = 1_000_000
x = np.random.rand(n)

# Python döngüsü
t0 = time.perf_counter()
toplam = sum(xi ** 2 for xi in x)   # ~250ms
t_dongu = time.perf_counter() - t0

# NumPy vektörleştirilmiş
t0 = time.perf_counter()
toplam_np = np.sum(x ** 2)           # ~2ms
t_numpy = time.perf_counter() - t0

hiz_orani = t_dongu / t_numpy
print(f"Döngü    : {t_dongu*1000:.1f} ms")
print(f"NumPy    : {t_numpy*1000:.1f} ms")
print(f"Hız oranı: ~{hiz_orani:.0f}× daha hızlı")
