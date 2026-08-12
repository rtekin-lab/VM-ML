# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.1. Veri Normalizasyonu › 3.2.1.1. Min-Max Normalizasyonu (Lineer Ölçekleme) › Aykırı Değer Sorunu ve RobustScaler
# Kitap  : Kod 3.18 (MinMaxScaler ile RobustScaler karşılaştırmas)
# Dosya : bolum03/03_02_01_01_aykiri-deger-sorunu-ve-robustscaler.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── MinMaxScaler vs RobustScaler Karşılaştırması ────────────────
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, RobustScaler

np.random.seed(7)
normal = np.random.normal(50, 10, 95)
aykiri = np.array([300, 350, 400, 450, 500])  # 5 aykırı değer
x = np.concatenate([normal, aykiri]).reshape(-1, 1)

mm  = MinMaxScaler().fit_transform(x)
rob = RobustScaler().fit_transform(x)

print("Karşılaştırma (aykırı değer: n=5, %5):")
print(f"  MinMax  — normal örnekler aralığı: [{mm[:95].min():.4f}, {mm[:95].max():.4f}]")
print(f"  Robust  — normal örnekler aralığı: [{rob[:95].min():.4f}, {rob[:95].max():.4f}]")
print(f"  MinMax  — aykırılar aralığı: [{mm[95:].min():.4f}, {mm[95:].max():.4f}]")
print(f"  Robust  — aykırılar aralığı: [{rob[95:].min():.4f}, {rob[95:].max():.4f}]")

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, veri, baslik, renk in [
    (axes[0], x,   "Orijinal",  "#3498db"),
    (axes[1], mm,  "MinMaxScaler", "#e74c3c"),
    (axes[2], rob, "RobustScaler", "#2ecc71"),
]:
    ax.hist(veri, bins=30, color=renk, alpha=0.7)
    ax.set_title(baslik, fontweight="bold")
plt.suptitle("MinMax vs Robust: Aykırı Değer Etkisi", fontsize=12)
plt.tight_layout(); plt.show()
