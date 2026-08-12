# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.8. Görselleştirme Kütüphaneleri: seaborn ve Plotly › A. seaborn — İstatistiksel Görselleştirme
# Kitap  : Kod 1.53 (Seaborn — İstatistiksel Görselleştirme) · Kod 1.54 (Seaborn — İstatistiksel Görselleştirme) · Kod 1.55 (Seaborn — İstatistiksel Görselleştirme) · Kod 1.56 (Seaborn — İstatistiksel Görselleştirme)
# Dosya : bolum01/01_02_08_a-seaborn-istatistiksel-gorsellestirme-2.py
# Gerekli: pip install pandas seaborn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import seaborn as sns
import pandas as pd, numpy as np, matplotlib.pyplot as plt

np.random.seed(42)
df = pd.DataFrame({
    'puan'  : np.concatenate([np.random.normal(70, 10, 200),
                               np.random.normal(85, 8, 200)]),
    'sinif' : ['A']*200 + ['B']*200,
    'cinsiyet': np.random.choice(['K','E'], 400),
})
# Puanla iliskili bagimsiz bir degisken uret (gurultulu dogrusal iliski)
df['calisma_saati'] = (df['puan'] - 40) / 6 + np.random.normal(0, 1.8, 400)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Violin plot — dağılım + medyan + IQR
sns.violinplot(data=df, x='sinif', y='puan', hue='cinsiyet',
               split=True, palette='Set2', ax=axes[0])
axes[0].set_title('Sınıf × Cinsiyet Puan Dağılımı')

# Regresyon scatter: puan ~ calisma_saati (x ile y ayni olursa dogru y=x cikar)
sns.regplot(data=df, x='calisma_saati', y='puan',
            scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=axes[1])
axes[1].set_title('Çalışma Saati ile Puan İlişkisi')
axes[1].set_xlabel('Haftalık Çalışma Saati'); axes[1].set_ylabel('Puan')

plt.tight_layout()
plt.savefig('/home/claude/seaborn_ornek.png', dpi=120)
plt.close()
print("seaborn örnek grafik oluşturuldu")
