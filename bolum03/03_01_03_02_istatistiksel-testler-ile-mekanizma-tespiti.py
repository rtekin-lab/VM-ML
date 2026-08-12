# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.3. Eksik Veri Tespit Yöntemleri › 3.1.3.2. İstatistiksel Testler ile Mekanizma Tespiti
# Kitap  : Kod 3.2 (L1 ve L2 normalizasyonu)
# Dosya : bolum03/03_01_03_02_istatistiksel-testler-ile-mekanizma-tespiti.py
# Gerekli: pip install scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum03/03_01_03_01_programatik-denetim-ile-eksik-veri-analizi.py
import numpy as np, pandas as pd
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
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

import pandas as pd
# ─── MAR/MCAR hizli kontrolu: t-testi ile gruplar arasi fark ──────
from scipy import stats

# Gelir eksik olan ve olmayan gruplarda "yas" ortalamasini karsilastir
gelir_eksik  = df[df["gelir"].isnull()]["yas"].dropna()
gelir_mevcut = df[df["gelir"].notna()]["yas"].dropna()

t_stat, p_val = stats.ttest_ind(gelir_eksik, gelir_mevcut)

print(f"Gelir eksik grubu   - Yas ort.: {gelir_eksik.mean():.2f} (n={len(gelir_eksik)})")
print(f"Gelir mevcut grubu  - Yas ort.: {gelir_mevcut.mean():.2f} (n={len(gelir_mevcut)})")
print(f"t-istatistigi: {t_stat:.4f},  p-degeri: {p_val:.4f}")

if p_val < 0.05:
    print("=> Anlamli fark var  -> MAR veya MNAR olabilir")
else:
    print("=> Anlamli fark yok  -> MCAR varsayimina yaklasilir")

# Eksiklik gostergesi korelasyon matrisi
gosterge = df.isnull().astype(int)
gosterge.columns = [f"{c}_eksik" for c in gosterge.columns]
corr = pd.concat([df.select_dtypes("number"), gosterge], axis=1).corr()
print("\nEksiklik gosterge korelasyonlari:")
print(corr.loc[df.select_dtypes("number").columns, gosterge.columns].round(3))
