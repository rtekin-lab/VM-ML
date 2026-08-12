# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.3. Veri Kaynaklarının Değerlendirilmesi ve Seçimi › Veri Erişimi, Maliyeti, Gizliliği ve Yasal Çerçeve
# Dosya : bolum02/02_02_03_veri-erisimi-maliyeti-gizliligi-ve-yasal-cerceve.py
# Gerekli: pip install numpy pandas
# ==========================================================================
import pandas as pd
import numpy as np

# 1. Veri Kaynağı Değerlendirme Matrisinin Oluşturulması
# Kriterler: Kalite, Erişim, Güncellik, Ters Maliyet (Yüksek Skor = Düşük Maliyet), GDPR/KVKK Uyum
kaynaklar_data = {
    'Kaynak'       : ['İlişkisel DB (Kurumsal)', 'Açık Devlet Verisi',
                      'Sosyal Medya API', 'Ticari Veri Sağlayıcı', 'IoT Sensörleri'],
    'Kalite'       : [9, 7, 5, 9, 8],
    'Erişim'       : [9, 9, 7, 5, 7],
    'Güncellik'    : [8, 4, 10, 9, 10],
    'Maliyet_Ters' : [7, 10, 8, 3, 6],
    'Hukuki_Uyum'  : [9, 10, 4, 8, 7]
}
df = pd.DataFrame(kaynaklar_data)

# 2. Ağırlıklandırılmış Toplam Puan Hesaplama
# Proje gereksinimlerine göre kriterlerin önem katsayıları (Ağırlıklar toplamı = 1.0)
agirliklar = {
    'Kalite': 0.30,
    'Erişim': 0.20,
    'Güncellik': 0.20,
    'Maliyet_Ters': 0.15,
    'Hukuki_Uyum': 0.15
}

df['Toplam_Skor'] = sum(df[kriter] * agirlik for kriter, agirlik in agirliklar.items())

# 3. Skor Normalizasyonu (0 - 100 Aralığına Ölçekleme)
df['Norm_Skor'] = (df['Toplam_Skor'] / df['Toplam_Skor'].max() * 100).round(1)

# Sonuçların Azalan Sırada Sıralanması
df_analiz = df[['Kaynak', 'Toplam_Skor', 'Norm_Skor']].sort_values('Norm_Skor', ascending=False)

print("--- VERİ KAYNAĞI SEÇİM SKORLARI ---")
print(df_analiz.to_string(index=False))

# Kriter Bazlı Detaylı Karşılaştırma
print("\n--- Kriter Bazlı Ağırlıklı Analiz ---")
print(df.set_index('Kaynak').round(2))
