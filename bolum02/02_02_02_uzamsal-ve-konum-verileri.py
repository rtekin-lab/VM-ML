# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.2. Farklı Veri Kaynakları ve Özellikleri › Uzamsal ve Konum Verileri (Spatial Data)
# Kitap  : Kod 2.14 (Uzamsal veride koordinat tabanlı mesafe hesa)
# Dosya : bolum02/02_02_02_uzamsal-ve-konum-verileri.py
# Gerekli: pip install geopandas pandas
# ==========================================================================
import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd

# 1. Geometrik Nesnelerin Oluşturulması
# Bir şehri temsil eden örnek poligon (koordinat sınırları)
sehir_siniri = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])

# Analiz edilecek noktalar (Müşteri konumları veya sensör noktaları)
noktalar = {
    'lokasyon_ad': ['Nokta_A', 'Nokta_B', 'Nokta_C'],
    'geometry': [Point(5, 5), Point(12, 12), Point(2, 8)]
}

# 2. GeoDataFrame Yapılandırması
gdf = gpd.GeoDataFrame(noktalar, crs="EPSG:4326")

# 3. Mekânsal İlişki Analizi (Point-in-Polygon)
# Her bir noktanın şehir sınırları içinde olup olmadığının kontrolü
gdf['sehir_icinde_mi'] = gdf.geometry.within(sehir_siniri)

print("--- Uzamsal Analiz Sonuçları ---")
print(gdf[['lokasyon_ad', 'sehir_icinde_mi']])

# 4. İstatistiksel Özet
icerdeki_sayisi = gdf['sehir_icinde_mi'].sum()
print(f"\nSınırlar dahilindeki toplam nokta sayısı: {icerdeki_sayisi}")
