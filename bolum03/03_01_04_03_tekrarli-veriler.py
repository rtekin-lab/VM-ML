# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.4. Bozuk Veri: Tanım, Sınıflandırma ve Teorik Çerçeve › 3.1.4.3. Tekrarlı Veriler (Duplicate Records)
# Kitap  : Kod 3.7 (Tam tekrar ve fuzzy matching ile tekrarlı ka)
# Dosya : bolum03/03_01_04_03_tekrarli-veriler.py
# Gerekli: pip install pandas
# ==========================================================================
# ─── Tam ve fuzzy matching ile tekrarli kayit tespiti ────────────
import pandas as pd
from difflib import SequenceMatcher

musteri_df = pd.DataFrame({
    "ad_soyad": ["Ahmet Yilmaz","Ahmet Yilmaz","Mehmet Kaya","mehmet kaya","Zeynep Sen"],
    "telefon":  ["5321112233","5321112233","5553334455","5553334455","5447778899"],
    "email":    ["a.y@m.com","a.y@m.com","m.k@m.com","mk@m.com","z.s@m.com"],
})

# 1) Tam tekrar
print(f"Tam tekrar satir sayisi: {musteri_df.duplicated(keep=False).sum()}")

# 2) Telefon numarasina gore grupla
print("\nAyni telefona sahip kayitlar:")
for tel, grp in musteri_df.groupby("telefon"):
    if len(grp) > 1:
        print(f"  Tel: {tel}")
        print(grp[["ad_soyad","email"]].to_string())

# 3) Fuzzy ad/soyad eslesme
adlar = musteri_df["ad_soyad"].tolist()
print("\nFuzzy eslesmeler (benzerlik >= 0.80):")
for i in range(len(adlar)):
    for j in range(i+1, len(adlar)):
        skor = SequenceMatcher(None,adlar[i].lower(),adlar[j].lower()).ratio()
        if skor >= 0.80:
            print(f"  [{i}]{adlar[i]} <-> [{j}]{adlar[j]} | Skor: {skor:.3f}")
