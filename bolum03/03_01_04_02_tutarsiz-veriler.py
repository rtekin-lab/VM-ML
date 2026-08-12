# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.4. Bozuk Veri: Tanım, Sınıflandırma ve Teorik Çerçeve › 3.1.4.2. Tutarsız Veriler
# Kitap  : Kod 3.6 (Kronolojik tutarsızlık tespiti örneği)
# Dosya : bolum03/03_01_04_02_tutarsiz-veriler.py
# Gerekli: pip install pandas
# ==========================================================================
# ─── Kronolojik tutarsizlik tespiti ─────────────────────────────
import pandas as pd
from datetime import date

musteri_df = pd.DataFrame({
    "musteri_id":   [1,    2,          3,          4,          5],
    "dogum_tarihi": pd.to_datetime(["1990-03-15","2005-08-22",
                                    "1985-11-01","1978-06-30","2000-01-10"]),
    "beyan_yas":    [34,   18,         38,         72,         35],
})

bugun = pd.Timestamp(date.today())
musteri_df["hesap_yas"] = ((bugun - musteri_df["dogum_tarihi"]).dt.days / 365.25).astype(int)
musteri_df["yas_farki"]  = abs(musteri_df["beyan_yas"] - musteri_df["hesap_yas"])
musteri_df["tutarsiz"]   = musteri_df["yas_farki"] > 2

print("Yas tutarsizligi tespit edilen kayitlar:")
print(musteri_df[musteri_df["tutarsiz"]]
      [["musteri_id","dogum_tarihi","beyan_yas","hesap_yas","yas_farki"]]
      .to_string(index=False))
