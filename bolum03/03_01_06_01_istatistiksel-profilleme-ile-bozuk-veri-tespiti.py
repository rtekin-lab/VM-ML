# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.6. Bozuk Veri Tespit Yöntemleri › 3.1.6.1. İstatistiksel Profilleme ile Bozuk Veri Tespiti
# Kitap  : Kod 3.10 (pandas ile temel eksik veri analizi)
# Dosya : bolum03/03_01_06_01_istatistiksel-profilleme-ile-bozuk-veri-tespiti.py
# Gerekli: pip install numpy pandas scipy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Kapsamli istatistiksel profil fonksiyonu ────────────────────
import pandas as pd
import numpy as np
from scipy import stats

def kapsamli_profil(df):
    profil_list = []
    for col in df.select_dtypes(include="number").columns:
        seri = df[col].dropna()
        if len(seri) == 0:
            continue
        Q1, Q3 = seri.quantile([0.25, 0.75])
        IQR = Q3 - Q1
        n_aykiri = ((seri < Q1-1.5*IQR) | (seri > Q3+1.5*IQR)).sum()
        _, p_norm = stats.shapiro(seri[:50]) if len(seri)>=3 else (None,None)
        profil_list.append({
            "Sutun":       col,
            "n":           int(len(seri)),
            "Eksik (%)":   round(df[col].isnull().mean()*100, 2),
            "Ort":         round(seri.mean(), 2),
            "Medyan":      round(seri.median(), 2),
            "Std":         round(seri.std(), 2),
            "Min":         round(seri.min(), 2),
            "Max":         round(seri.max(), 2),
            "Carpiklik":   round(seri.skew(), 3),
            "n_Aykiri":    int(n_aykiri),
            "Shapiro-p":   round(p_norm, 4) if p_norm else None,
        })
    return pd.DataFrame(profil_list)

# Ornek uygulama
np.random.seed(42)
df_test = pd.DataFrame({
    "gelir":  np.concatenate([np.random.normal(5000,1000,195),[50000,-100,np.nan,np.nan,np.nan]]),
    "yas":    np.concatenate([np.random.randint(18,65,198).astype(float),[999,-5]]),
    "puan":   np.random.randint(0,101,200).astype(float)
})

profil = kapsamli_profil(df_test)
print(profil.to_string(index=False))

print("\nOlasi sorunlu sutunlar:")
for _, r in profil.iterrows():
    sorunlar = []
    if r["Eksik (%)"] > 5:      sorunlar.append(f"Yuksek eksik (%{r['Eksik (%)']:.1f})")
    if abs(r["Carpiklik"]) > 1: sorunlar.append(f"Carpik ({r['Carpiklik']:.2f})")
    if r["n_Aykiri"] > 0:       sorunlar.append(f"{r['n_Aykiri']} aykiri")
    if sorunlar:
        print(f"  {r['Sutun']:12s}: {', '.join(sorunlar)}")
