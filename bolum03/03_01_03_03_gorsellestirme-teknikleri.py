# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.1. Eksik ve Bozuk Verilerin Tespiti › 3.1.3. Eksik Veri Tespit Yöntemleri › 3.1.3.3. Görselleştirme Teknikleri
# Kitap  : Kod 3.3 (Gaussian karışım modeli ile anomali tespiti)
# Dosya : bolum03/03_01_03_03_gorsellestirme-teknikleri.py
# Gerekli: pip install matplotlib missingno
# ==========================================================================
# ─── missingno ile kapsamli gorsellestirme ───────────────────────
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

import missingno as msno
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

msno.matrix(df, ax=axes[0,0], sparkline=False, color=(0.18,0.46,0.71))
axes[0,0].set_title("Eksik Veri Matrisi", fontsize=12, fontweight="bold")

msno.bar(df, ax=axes[0,1], color=(0.18,0.46,0.71))
axes[0,1].set_title("Sutun Bazinda Doluluk Orani", fontsize=12, fontweight="bold")

msno.heatmap(df, ax=axes[1,0])
axes[1,0].set_title("Eksiklik Korelasyon Isi Haritasi", fontsize=12, fontweight="bold")

msno.dendrogram(df, ax=axes[1,1])
axes[1,1].set_title("Eksiklik Dendrogrami", fontsize=12, fontweight="bold")

plt.tight_layout()
plt.savefig("eksik_veri_gorsellestirme.png", dpi=150, bbox_inches="tight")
plt.show()
