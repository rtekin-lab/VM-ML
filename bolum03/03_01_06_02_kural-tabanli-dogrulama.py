# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.6. Bozuk Veri Tespit Yöntemleri › 3.1.6.2. Kural Tabanlı Doğrulama
# Kitap  : Kod 3.11 (Kural tabanlı veri doğrulama sistemi)
# Dosya : bolum03/03_01_06_02_kural-tabanli-dogrulama.py
# Gerekli: pip install pandas
# ==========================================================================
# ─── Kural tabanlı veri dogrulama sistemi ────────────────────────
import pandas as pd
import re

df_val = pd.DataFrame({
    "tckn":      ["12345678901","99999999999","123456789","12345678901","abc"],
    "email":     ["u@mail.com","eksik-at","u@d.org","","v@t.net"],
    "yas":       [25, -3, 200, 42, 18],
    "puan":      [85, 105, 90, -10, 77],
    "giris_yil": [2010, 2015, 2020, 2018, 2022],
    "cikis_yil": [2015, 2013, 2022, 2020, 2025],
})

hatalar = []

for idx, row in df_val.iterrows():
    if not str(row["tckn"]).isdigit() or len(str(row["tckn"])) != 11:
        hatalar.append((idx,"tckn","11 haneli sayisal olmali",row["tckn"]))

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(row["email"])):
        hatalar.append((idx,"email","Gecersiz e-posta bicimi",row["email"]))

    if not (0 <= row["yas"] <= 120):
        hatalar.append((idx,"yas","0-120 arasinda olmali",row["yas"]))

    if not (0 <= row["puan"] <= 100):
        hatalar.append((idx,"puan","0-100 arasinda olmali",row["puan"]))

    if row["cikis_yil"] < row["giris_yil"]:
        hatalar.append((idx,"cikis_yil","Giris yilindan once olamaz",row["cikis_yil"]))

hata_df = pd.DataFrame(hatalar, columns=["Satir","Sutun","Kural Ihlali","Deger"])
print(f"Toplam ihlal sayisi: {len(hata_df)}")
print(hata_df.to_string(index=False))
