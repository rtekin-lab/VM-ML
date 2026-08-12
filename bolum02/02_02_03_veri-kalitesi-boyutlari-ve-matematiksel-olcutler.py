# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.3. Veri Kaynaklarının Değerlendirilmesi ve Seçimi › Veri Kalitesi Boyutları ve Matematiksel Ölçütleri
# Dosya : bolum02/02_02_03_veri-kalitesi-boyutlari-ve-matematiksel-olcutler.py
# Gerekli: pip install numpy pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import pandas as pd
import numpy as np

# 1. Sentetik Veri Setinin Yapılandırılması
np.random.seed(42)
n = 500
data = {
    'musteri_id'    : range(1, n+1),
    'yas'           : np.random.choice(
       np.concatenate([np.random.randint(18, 80, 450), [-5, 200, np.nan, np.nan, np.nan]]),
       n, replace=True),
    'gelir'         : np.random.choice(
       np.concatenate([np.random.normal(55000, 20000, 470), [np.nan] * 30]),
       n, replace=False),
    'cinsiyet'      : np.random.choice(['Kadın', 'Erkek', 'K', 'E', None, 'erkek'], n),
    'harcama'       : np.random.exponential(500, n),
    'kayit_tarihi'  : pd.date_range('2020-01-01', periods=n, freq='D'),
}
df = pd.DataFrame(data)

# 2. Veri Kalitesi Denetim Raporu
print("=== VERİ KALİTESİ ANALİZ RAPORU ===")
print(f"Toplam Gözlem: {len(df)} | Toplam Öznitelik: {len(df.columns)}")

# Eksik Veri Analizi
eksiklik = pd.DataFrame({
    'Eksik_Sayı'  : df.isnull().sum(),
    'Eksik_Oran%' : (df.isnull().sum() / len(df) * 100).round(2)
})
print("\nEksiklik Analizi:")
print(eksiklik[eksiklik['Eksik_Sayı'] > 0])

# Aykırı Değer Tespiti (Interquartile Range - IQR Yöntemi)
print("\nAykırı Değer Analizi (IQR):")
sayisal_sutunlar = ['yas', 'gelir', 'harcama']
for sutun in sayisal_sutunlar:
    Q1, Q3 = df[sutun].quantile(0.25), df[sutun].quantile(0.75)
    IQR = Q3 - Q1
    alt_sinir, ust_sinir = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    aykiri_sayisi = ((df[sutun] < alt_sinir) | (df[sutun] > ust_sinir)).sum()
    print(f"{sutun:10s}: {aykiri_sayisi} aykırı değer tespit edildi.")

# 3. Veri Ön İşleme ve Temizleme Hattı (Cleaning Pipeline)
df_temiz = df.copy()

# Mantıksal Filtreleme: Yaş değerlerini makul aralığa çekme
df_temiz = df_temiz[(df_temiz['yas'] >= 18) & (df_temiz['yas'] <= 100) | df_temiz['yas'].isna()]

# Kategorik Normalizasyon
cinsiyet_map = {'K': 'Kadın', 'E': 'Erkek', 'kadın': 'Kadın', 'erkek': 'Erkek'}
df_temiz['cinsiyet'] = df_temiz['cinsiyet'].map(lambda x: cinsiyet_map.get(x, x) if pd.notna(x) else x)

# Eksik Değer Atama (Imputation)
df_temiz['gelir'] = df_temiz['gelir'].fillna(df_temiz['gelir'].median())

print("\nTemizleme Sonrası Özet:")
print(f"Kaldırılan Satır Sayısı: {len(df) - len(df_temiz)}")
