# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.3. Eksik Veri Tespit Yöntemleri › 3.1.3.4. Eksik Veri Örüntüsü Analizi
# Kitap  : Kod 3.4 (Eksik veri örüntü analizi)
# Dosya : bolum03/03_01_03_04_eksik-veri-oruntusu-analizi.py
# ==========================================================================
# ─── Eksik veri oruntu analizi ──────────────────────────────────
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

pattern_df = df.isnull().astype(int)
pattern_df["oruntu"] = pattern_df.apply(lambda r: "".join(r.astype(str)), axis=1)

pattern_count = pattern_df["oruntu"].value_counts().reset_index()
pattern_count.columns = ["Oruntu", "Satir Sayisi"]

cols = df.columns.tolist()
pattern_count["Eksik Sutunlar"] = pattern_count["Oruntu"].apply(
    lambda p: [c for c,b in zip(cols,p) if b=="1"] or ["Yok"]
)

print("Eksik veri oruntuleri (0=Mevcut, 1=Eksik):")
for _, row in pattern_count.head(10).iterrows():
    print(f"  {row['Oruntu']}  -> {row['Satir Sayisi']:3d} satir",
          f"| Eksik: {row['Eksik Sutunlar']}")

print(f"\nBenzersiz oruntu sayisi: {len(pattern_count)}")
print(f"Tam eksiksiz satir: %{df.dropna().shape[0]/len(df)*100:.1f}")
