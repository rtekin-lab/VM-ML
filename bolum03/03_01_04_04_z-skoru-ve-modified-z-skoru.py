# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.4. Bozuk Veri: Tanım, Sınıflandırma ve Teorik Çerçeve › 3.1.4.4. Aykırı Değerler (Outliers) › Z-Skoru ve Modified Z-Skoru
# Kitap  : Kod 3.9 (Z-skoru ve düzeltilmiş Z-skoru ile aykırı de)
# Dosya : bolum03/03_01_04_04_z-skoru-ve-modified-z-skoru.py
# Gerekli: pip install numpy pandas scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Z-Skoru ve Modified Z-Skoru ile aykiri deger tespiti ───────
import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(42)
veri = np.concatenate([np.random.normal(50, 10, 300), [120, -30, 140, 200]])
df_z = pd.DataFrame({"deger": veri})

# Standart Z-Skoru
df_z["z_skoru"]  = stats.zscore(df_z["deger"])
df_z["z_aykiri"] = df_z["z_skoru"].abs() > 3

# Modified Z-Skoru
medyan = df_z["deger"].median()
mad    = np.median(np.abs(df_z["deger"] - medyan))
df_z["mz_skoru"]  = 0.6745 * (df_z["deger"] - medyan) / mad
df_z["mz_aykiri"] = df_z["mz_skoru"].abs() > 3.5

print(f"Z-Skoru    (|Z|>3.0)  aykiri sayisi: {df_z['z_aykiri'].sum()}")
print(f"Mod.Z-Sko. (|M|>3.5)  aykiri sayisi: {df_z['mz_aykiri'].sum()}")

print("\nZ-Skoru aykiri degerler:")
print(df_z[df_z["z_aykiri"]][["deger","z_skoru"]].sort_values("deger").to_string(index=False))
