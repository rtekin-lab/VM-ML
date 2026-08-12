# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.2. Istatistiksel Anomali Tespit Yontemleri › 3.3.2.2. Z-Skoru ve Modified Z-Skoru
# Kitap  : Kod 3.29 (Z-skoru ile düzeltilmiş Z-skorunun maskeleme)
# Dosya : bolum03/03_03_02_02_z-skoru-ve-modified-z-skoru.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# Z-Skoru ve Modified Z-Skoru Karsilastirmasi
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 500
normal = np.random.normal(50, 8, int(n*0.95))
aykiri = np.array([110.0, 115.0, 120.0, -15.0, -20.0, -25.0,
                    110.0, 115.0, 120.0, -15.0, -20.0, -25.0,
                    110.0, 115.0, 120.0, -15.0, -20.0, -25.0,
                    110.0, 115.0, 120.0, -15.0, -20.0, -25.0,
                    110.0, 115.0])
x = np.concatenate([normal, aykiri])

# Standart Z-Skoru
mu, sigma = x.mean(), x.std()
z = (x - mu) / sigma
maske_z = np.abs(z) > 3.0

# Modified Z-Skoru
medyan = np.median(x)
mad = np.median(np.abs(x - medyan))
M = 0.6745 * (x - medyan) / mad
maske_mz = np.abs(M) > 3.5

print("Z-Skoru (|z|>3.0)    : {} anomali".format(maske_z.sum()))
print("Mod Z-Skoru (|M|>3.5): {} anomali".format(maske_mz.sum()))

# Maskeleme etkisi
x2 = np.concatenate([normal, np.array([200.0]*15)])
z2 = (x2 - x2.mean()) / x2.std()
M2 = 0.6745*(x2 - np.median(x2)) / np.median(np.abs(x2 - np.median(x2)))
print("Maskeleme (15 buyuk aykiri):")
print("  Z-Skoru anomali: {} (maskeleme riski!)".format((np.abs(z2)>3).sum()))
print("  Mod Z-Skoru    : {} (maskelemeye dayanikli)".format((np.abs(M2)>3.5).sum()))
