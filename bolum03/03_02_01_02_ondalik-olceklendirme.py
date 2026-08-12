# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.1. Veri Normalizasyonu › 3.2.1.2. Ondalık Ölçeklendirme (Decimal Scaling)
# Kitap  : Kod 3.19 (Ondalık ölçeklendirme, manuel uygulama ve ço)
# Dosya : bolum03/03_02_01_02_ondalik-olceklendirme.py
# Gerekli: pip install numpy pandas
# ==========================================================================
# ─── Ondalık Ölçeklendirme ───────────────────────────────────────
import numpy as np
import pandas as pd
import math

def decimal_scaling(x):
    """x' = x / 10^d,  d = ceil(log10(max|x|))"""
    x = np.asarray(x, dtype=float)
    max_abs = np.max(np.abs(x))
    if max_abs == 0: return x.copy(), 0
    d = math.ceil(math.log10(max_abs))
    return x / (10 ** d), d

# Test 1: Genel örnekler
ornekler = [
    ("Küçük tamsayılar", [12, 34, -7, 98, -23]),
    ("Yüzlük", [120, 345, -78, 987, -23]),
    ("Binlik (gelir)", [15000, 45000, 120000, 980000]),
    ("Ondalık", [0.05, 0.12, 0.87, -0.33]),
]

print("Veri Seti              d  Orijinal -> Olceklendirilmis"),
print("-"*75)
for isim, degerler in ornekler:
    arr = np.array(degerler, dtype=float)
    scaled, d = decimal_scaling(arr)
    print(f"{isim:<22} {d:>4}  {arr}  → {np.round(scaled,4)}")

# Test 2: DataFrame üzerinde
df = pd.DataFrame({"A":[10,50,90,30], "B":[1000,5500,9000,3200], "C":[0.01,0.05,0.09,0.03]})
df_sc = df.copy()
for col in df.columns:
    df_sc[col], d = decimal_scaling(df[col].values)
    print(f"Sütun {col}: d={d}, aralık=[{df_sc[col].min():.4f}, {df_sc[col].max():.4f}]")
