# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.8. Zaman Serisi Anomali Tespiti
# Kitap  : Kod 3.38 (Zaman serisinde hareketli Z-skoru ile anomal)
# Dosya : bolum03/03_03_08_zaman-serisi-anomali-tespiti.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# Zaman Serisi Anomali Tespiti: Hareketli Z-Skoru
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

np.random.seed(42)
T = 730
tarihler = pd.date_range("2022-01-01", periods=T, freq="D")
trend   = np.linspace(100, 150, T)
mevsim  = 20 * np.sin(2*np.pi*np.arange(T)/365)
haftalik= 10 * np.sin(2*np.pi*np.arange(T)/7)
ts = trend + mevsim + haftalik + np.random.normal(0,5,T)
anom_idx = [50,100,200,350,500,600,680]
for idx in anom_idx: ts[idx:idx+3] += np.random.choice([-1,1])*np.random.uniform(30,60)

df_ts = pd.DataFrame({"deger":ts}, index=tarihler)
pencere = 30
df_ts["ort"] = df_ts["deger"].rolling(pencere,center=True).mean()
df_ts["std"] = df_ts["deger"].rolling(pencere,center=True).std()
df_ts["z_t"] = (df_ts["deger"]-df_ts["ort"])/(df_ts["std"]+1e-9)
df_ts["anom_z"] = df_ts["z_t"].abs()>3.0
print("Hareketli Z-Skoru anomali sayisi: {}".format(df_ts["anom_z"].sum()))

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(16,8),sharex=True)
ax1.plot(df_ts.index, df_ts["deger"], color="#3498db", linewidth=0.8, alpha=0.8)
ax1.scatter(df_ts.index[df_ts["anom_z"]], df_ts["deger"][df_ts["anom_z"]],
            c="#e74c3c", s=60, zorder=5, label="Anomali")
ax1.set_title("Hareketli Z-Skoru Anomali Tespiti (pencere=30)"); ax1.legend()
ax2.plot(df_ts.index, df_ts["z_t"], color="#2ecc71", linewidth=0.8)
ax2.axhline(3.0, color="red", linestyle="--"); ax2.axhline(-3.0, color="red", linestyle="--")
ax2.set_title("Hareketli Z-Skoru (|z|>3 = anomali)")
plt.tight_layout(); plt.show()
