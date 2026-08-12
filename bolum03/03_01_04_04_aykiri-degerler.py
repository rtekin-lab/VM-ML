# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.4. Bozuk Veri: Tanım, Sınıflandırma ve Teorik Çerçeve › 3.1.4.4. Aykırı Değerler (Outliers)
# Kitap  : Kod 3.8 (IQR yöntemi ile aykırı değer tespiti)
# Dosya : bolum03/03_01_04_04_aykiri-degerler.py
# Gerekli: pip install matplotlib numpy pandas seaborn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── IQR yontemi ile aykiri deger tespiti ───────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(0)
degerler = np.concatenate([np.random.normal(50, 10, 200), [120, 130, -20, 160, 5]])
df_ay = pd.DataFrame({"deger": degerler})

Q1  = df_ay["deger"].quantile(0.25)
Q3  = df_ay["deger"].quantile(0.75)
IQR = Q3 - Q1
alt = Q1 - 1.5 * IQR
ust = Q3 + 1.5 * IQR

maske = (df_ay["deger"] < alt) | (df_ay["deger"] > ust)
print(f"Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
print(f"Alt sinir: {alt:.2f}  |  Ust sinir: {ust:.2f}")
print(f"Aykiri deger sayisi: {maske.sum()}")
print(f"Aykiri degerler: {sorted(df_ay[maske]['deger'].values)}")

# Gorsellestirme
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(y=df_ay["deger"], ax=ax1, color="#4C9BE8")
ax1.axhline(alt, color="red", linestyle="--", label=f"Alt ({alt:.1f})")
ax1.axhline(ust, color="red", linestyle="--", label=f"Ust ({ust:.1f})")
ax1.set_title("Kutu Grafigi (IQR)", fontweight="bold")
ax1.legend()
sns.histplot(df_ay["deger"], bins=30, kde=True, ax=ax2, color="#4C9BE8")
ax2.axvline(alt, color="red", linestyle="--")
ax2.axvline(ust, color="red", linestyle="--")
ax2.set_title("Histogram + KDE", fontweight="bold")
plt.tight_layout()
plt.show()
