# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.1. Metin Ön İşleme ve Temel Temsil › 9.1.1. Temizlik: Tokenization, Stop-words Temizliği, Stemming ve Lemmatization › 9.1.1.3. Durdurma Kelimeleri (Stop-words) Temizliği
# Kitap  : Kod 9.2 (Durdurma kelimelerinin kaldırılması ve etkis)
# Dosya : bolum09/09_01_01_03_durdurma-kelimeleri-temizligi.py
# Gerekli: pip install nltk
# ==========================================================================
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# 1. Mevcut stop-words listeleri
ingilizce_sw = set(stopwords.words('english'))
print(f'İngilizce stop-words sayısı: {len(ingilizce_sw)}')
print(f'Örnek: {list(ingilizce_sw)[:10]}')

# Türkçe için manual liste veya özel kütüphane gerekebilir
turkce_stop_words = {
    'bir', 've', 'bu', 'da', 'de', 'ile', 'için', 'ama', 'veya',
    'ki', 'gibi', 'mi', 'mu', 'mü', 'mı', 'ne', 'ya', 'çok',
    'daha', 'en', 'bunu', 'buna', 'bunun', 'olan', 'olarak', 'olan'
}

# 2. Örnek metin
metin = """
Veri madenciliği ve makine öğrenmesi ile büyük veri setlerinden
anlamlı örüntüler çıkarmak için bu teknikleri kullanıyoruz.
Bu yöntemler çok güçlü ve etkili araçlardır.
"""

# 3. Tokenize et ve stop-words temizle
tokenlar = word_tokenize(metin.lower())
temiz_tokenlar = [t for t in tokenlar
                  if t.isalpha() and t not in turkce_stop_words]

print(f'\nOrijinal token sayısı: {len(tokenlar)}')
print(f'Temizlenmiş token sayısı: {len(temiz_tokenlar)}')
print(f'Temiz tokenlar: {temiz_tokenlar}')

# 4. En sık kelimeler karşılaştırması
print('\n=== Stop-words Öncesi En Sık 5 Kelime ===')
print(Counter([t for t in tokenlar if t.isalpha()]).most_common(5))

print('\n=== Stop-words Sonrası En Sık 5 Kelime ===')
print(Counter(temiz_tokenlar).most_common(5))

# 5. Alan özgü (domain-specific) stop-words ekleme
domain_stop_words = turkce_stop_words | {'yöntemler', 'araçlardır', 'kullanıyoruz'}
ultra_temiz = [t for t in tokenlar if t.isalpha() and t not in domain_stop_words]
print(f'\nAlan özgü temizlik sonrası: {ultra_temiz}')
