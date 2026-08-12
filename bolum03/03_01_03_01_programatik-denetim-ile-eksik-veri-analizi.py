# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.3. Eksik Veri Tespit Yöntemleri › 3.1.3.1. Programatik Denetim ile Eksik Veri Analizi
# Kitap  : Kod 3.1 (pandas ile temel eksik veri analizi)
# Dosya : bolum03/03_01_03_01_programatik-denetim-ile-eksik-veri-analizi.py
# Gerekli: pip install numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Eksik veri analizi: temel pandas araçları ───────────────────
import pandas as pd
import numpy as np

np.random.seed(42)
n = 200
df = pd.DataFrame({
    "yas":         np.where(np.random.rand(n) < 0.05, np.nan,
                            np.random.randint(18, 65, n).astype(float)),
    "gelir":       np.where(np.random.rand(n) < 0.12, np.nan,
                            np.random.normal(5000, 1500, n)),
    "egitim_yil":  np.where(np.random.rand(n) < 0.08, np.nan,
                            np.random.randint(8, 22, n).astype(float)),
    "kredi_skoru": np.where(np.random.rand(n) < 0.20, np.nan,
                            np.random.randint(300, 850, n).astype(float)),
    "sehir":       np.random.choice(["Ankara","Istanbul","Izmir",None],
                                     n, p=[0.35,0.35,0.20,0.10]),
})

# Sutun bazında eksiklik ozeti
eksik_df = pd.DataFrame({
    "Eksik Sayisi":   df.isnull().sum(),
    "Eksik Oran (%)": df.isnull().mean().mul(100).round(2),
    "Veri Tipi":      df.dtypes
}).sort_values("Eksik Oran (%)", ascending=False)

print("=== Sutun Bazli Eksiklik Ozeti ===")
print(eksik_df)

# Satir bazinda kac sutunda eksiklik var?
satirbazli = df.isnull().sum(axis=1)
print("\n=== Satir Bazli Eksik Sutun Sayisi Dagilimi ===")
print(satirbazli.value_counts().sort_index())

# Tam eksiksiz satir orani
tam = df.dropna().shape[0]
print(f"\nTam eksiksiz satir: {tam} ({tam/n*100:.1f}%)")
