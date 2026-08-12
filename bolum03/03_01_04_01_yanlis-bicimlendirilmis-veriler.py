# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.4. Bozuk Veri: Tanım, Sınıflandırma ve Teorik Çerçeve › 3.1.4.1. Yanlış Biçimlendirilmiş Veriler
# Kitap  : Kod 3.5 (Çok biçimli tarih verilerinin normalleştiril)
# Dosya : bolum03/03_01_04_01_yanlis-bicimlendirilmis-veriler.py
# Gerekli: pip install numpy pandas
# ==========================================================================
# ─── Cok bicimli tarih verilerini normalize etme ─────────────────
import pandas as pd
import numpy as np

tarih_verileri = pd.Series([
    "2023-05-14",    # ISO 8601 - dogru
    "14/05/2023",    # Gun/Ay/Yil
    "May 14, 2023",  # Uzun bicim
    "14-05-23",      # Kisa yil
    "2023.05.14",    # Nokta ayracli
    "33/13/2023",    # Gecersiz gun/ay
    None,            # Bos deger
])

def tarihi_normalize_et(tarih_str):
    if pd.isnull(tarih_str):
        return pd.NaT
    bicimleri = ["%Y-%m-%d", "%d/%m/%Y", "%B %d, %Y",
                 "%d-%m-%y", "%Y.%m.%d", "%m/%d/%Y"]
    for bicim in bicimleri:
        try:
            return pd.to_datetime(tarih_str, format=bicim)
        except ValueError:
            continue
    return pd.NaT

normalize_tarihler = tarih_verileri.apply(tarihi_normalize_et)
sonuc = pd.DataFrame({
    "Ham Deger":      tarih_verileri,
    "Normalize":      normalize_tarihler,
    "Gecerli mi?":    normalize_tarihler.notna()
})
print(sonuc.to_string(index=False))
