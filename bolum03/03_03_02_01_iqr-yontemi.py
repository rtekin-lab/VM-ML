# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.2. Istatistiksel Anomali Tespit Yontemleri › 3.3.2.1. IQR Yontemi (Ceyrekler Arası Aclık)
# Kitap  : Kod 3.28 (IQR yöntemi ile anomali tespiti)
# Dosya : bolum03/03_03_02_01_iqr-yontemi.py
# Gerekli: pip install matplotlib numpy pandas seaborn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# IQR Yontemi ile Anomali Tespiti
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
n = 300
normal = np.random.normal(50, 10, n)
aykirilar = np.array([130, 140, -15, -25, 155, -30, 145])
veri = np.concatenate([normal, aykirilar])
df = pd.DataFrame({"deger": veri})

def iqr_anomali_tespit(dizi, k=1.5):
    Q1, Q3 = np.percentile(dizi, [25, 75])
    IQR = Q3 - Q1
    alt = Q1 - k * IQR
    ust = Q3 + k * IQR
    maske = (dizi < alt) | (dizi > ust)
    return maske, Q1, Q3, IQR, alt, ust

maske, Q1, Q3, IQR, alt, ust = iqr_anomali_tespit(df["deger"].values)

print("=== IQR Anomali Tespit Raporu ===")
print(f"  Q1={Q1:.3f}, Q3={Q3:.3f}, IQR={IQR:.3f}")
print(f"  Alt sinir (k=1.5): {alt:.3f}")
print(f"  Ust sinir (k=1.5): {ust:.3f}")
print(f"  Tespit edilen anomali sayisi: {maske.sum()}")
print(f"  Anomali degerleri: {sorted(df['deger'][maske].values)}")

# k=3.0 (asiri aykiri)
maske3, _, _, _, alt3, ust3 = iqr_anomali_tespit(df["deger"].values, k=3.0)
print(f"  k=3.0 => Sinirlar: [{alt3:.3f}, {ust3:.3f}] | Anomali: {maske3.sum()}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].boxplot(df["deger"], patch_artist=True, boxprops=dict(facecolor="#AED6F1"),
                medianprops=dict(color="red", lw=2))
axes[0].set_title("Kutu Grafigi ile IQR", fontweight="bold")
normal_pts = df["deger"][~maske]
aykiri_pts = df["deger"][maske]
axes[1].scatter(range(len(normal_pts)), normal_pts.values, c="#3498db", alpha=0.5, s=20, label="Normal")
axes[1].scatter(range(len(aykiri_pts)), aykiri_pts.values, c="#e74c3c", s=80, marker="x", lw=2, label="Anomali")
axes[1].axhline(ust, color="orange", linestyle="--", label=f"Ust {ust:.1f}")
axes[1].axhline(alt, color="green", linestyle="--", label=f"Alt {alt:.1f}")
axes[1].legend(); axes[1].set_title("Anomali Noktalari", fontweight="bold")
plt.tight_layout(); plt.show()
