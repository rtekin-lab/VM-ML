# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.1. Metin Ön İşleme ve Temel Temsil › 9.1.1. Temizlik: Tokenization, Stop-words Temizliği, Stemming ve Lemmatization › 9.1.1.1. Ham Metin Temizleme
# Dosya : bolum09/09_01_01_01_ham-metin-temizleme.py
# Gerekli: pip install beautifulsoup4
# ==========================================================================
import re
from bs4 import BeautifulSoup

def ham_metin_temizle(metin):
    """
    Ham metin gürültüsünü kademeli olarak temizleyen fonksiyon.
    """
    # 1. HTML etiketlerini kaldır
    metin = BeautifulSoup(metin, 'html.parser').get_text()
    # 2. URL'leri kaldır (http, https, www ile başlayanlar)
    metin = re.sub(r'http\S+|www\.\S+', '', metin)
    # 3. Sosyal medya etiketleri: @mention ve #hashtag
    metin = re.sub(r'@\w+|#\w+', '', metin)
    # 4. Özel karakterleri ve noktalama işaretlerini kaldır
    metin = re.sub(r'[^a-zA-ZğüşöçıİĞÜŞÖÇ\s]', ' ', metin)
    # 5. Küçük harfe çevir
    metin = metin.lower()
    # 6. Fazla boşlukları tek boşluğa indir
    metin = re.sub(r'\s+', ' ', metin).strip()
    return metin

# Test
ornek = '<p>Bu ürün MÜKEMMEL! https://shop.com/urun @kullanici #indirim fiyat: 299₺</p>'
print('Orijinal :', ornek)
print('Temizlenmiş:', ham_metin_temizle(ornek))
# Çıktı: 'bu ürün mükemmel fiyat'
