# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.7. statsmodels — İstatistiksel Modelleme Kütüphanesi
# Kitap  : Kod 1.48 (Statsmodels — İstatistiksel Modelleme Kütüph) · Kod 1.49 (Formül tabanlı OLS — R benzeri sözdizimi (Pa) · Kod 1.50 (Temel çıktılar) · Kod 1.51 (Artık analizi (istatistiksel varsayım sınama) · Kod 1.52 (Artık analizi (istatistiksel varsayım sınama)
# Dosya : bolum01/01_02_07_statsmodels-istatistiksel-modelleme-kutuphanesi-2.py
# Gerekli: pip install numpy pandas statsmodels
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
from scipy import stats
import random
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np

np.random.seed(42)

# ─── Çoklu Doğrusal Regresyon ─────────────────────────────────────────────────
n = 300
df = pd.DataFrame({
    'gelir'   : np.random.normal(55000, 20000, n),
    'egitim'  : np.random.randint(8, 22, n),
    'deneyim' : np.random.randint(0, 35, n),
    'sehir'   : np.random.choice(['Istanbul','Ankara','Izmir'], n),
})
# Gerçek ilişki: maaş = 20000 + 1500*egitim + 800*deneyim + gürültü
df['maas'] = (20000 + 1500*df['egitim'] + 800*df['deneyim']
              + 5000*(df['sehir']=='Istanbul')
              + np.random.normal(0, 5000, n))

# Formül tabanlı OLS — R benzeri sözdizimi (Patsy aracılığıyla)
model = smf.ols('maas ~ egitim + deneyim + C(sehir)', data=df)
sonuc = model.fit()
print(sonuc.summary())

# Temel çıktılar
print(f"R² = {sonuc.rsquared:.4f}")
print(f"Düzeltilmiş R² = {sonuc.rsquared_adj:.4f}")
print(f"F-istatistiği: {sonuc.fvalue:.2f}, p = {sonuc.f_pvalue:.4e}")
print("\nKatsayılar ve %95 GA:")
print(sonuc.conf_int())

# Artık analizi (istatistiksel varsayım sınaması)
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(sonuc.resid, sonuc.model.exog)
print(f"\nBreusch-Pagan (eş varyanslılık): LM={bp_test[0]:.4f}, p={bp_test[1]:.4f}")
