# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.1. Metin Ön İşleme ve Temel Temsil › 9.1.1. Temizlik: Tokenization, Stop-words Temizliği, Stemming ve Lemmatization › 9.1.1.5. Tam Metin Normalizasyon Pipeline'ı
# Kitap  : Kod 9.4 (Uçtan uca metin normalizasyon boru hattı)
# Dosya : bolum09/09_01_01_05_tam-metin-normalizasyon-pipeline-i.py
# Gerekli: pip install nltk spacy
# ==========================================================================
import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

class MetinNormalizasyonPipeline:
    """
    Tam metin ön işleme pipeline'ı.
    Zincir: Temizlik → Tokenization → Stop-words → Stemming/Lemmatization
    """
    def __init__(self, dil='english', yontem='stemming', min_uzunluk=2):
        self.dil = dil
        self.yontem = yontem  # 'stemming' veya 'lemmatization'
        self.min_uzunluk = min_uzunluk
        self.stop_words = set(stopwords.words(dil))
        if yontem == 'stemming':
            from nltk.stem import SnowballStemmer
            self.normalizer = SnowballStemmer(dil)
        else:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except:
                print('spaCy modeli yok, stemming kullanılıyor.')
                from nltk.stem import SnowballStemmer
                self.normalizer = SnowballStemmer(dil)
                self.yontem = 'stemming'

    def on_temizlik(self, metin):
        metin = re.sub(r'http\S+|www.\S+', '', metin)  # URL
        metin = re.sub(r'@\w+|#\w+', '', metin)         # @mention, #hashtag
        metin = re.sub(r'[^a-zA-Z\s]', ' ', metin)      # Özel karakter
        return metin.lower().strip()

    def isle(self, metin):
        # Adım 1: Temizlik
        temiz = self.on_temizlik(metin)
        # Adım 2: Tokenization
        tokenlar = word_tokenize(temiz)
        # Adım 3: Stop-words filtresi + minimum uzunluk
        tokenlar = [t for t in tokenlar
                    if t not in self.stop_words and len(t) >= self.min_uzunluk]
        # Adım 4: Stemming veya Lemmatization
        if self.yontem == 'stemming':
            tokenlar = [self.normalizer.stem(t) for t in tokenlar]
        else:
            doc = self.nlp(' '.join(tokenlar))
            tokenlar = [t.lemma_ for t in doc]
        return tokenlar

    def isle_toplu(self, metinler):
        """Birden fazla metni toplu işler."""
        return [' '.join(self.isle(m)) for m in metinler]

# Kullanım
pipeline = MetinNormalizasyonPipeline(dil='english', yontem='stemming')

ornekler = [
    "The researchers are studying deep learning algorithms!",
    "NLP models have been improving rapidly since 2017. @user #AI",
    "She was running faster than the other players in the team."
]

print('=== Pipeline Çıktıları ===')
for ornek in ornekler:
    print(f'\nGiriş: {ornek}')
    print(f'Çıkış: {pipeline.isle(ornek)}')

# Toplu işleme (corpus için)
islenmiş_corpus = pipeline.isle_toplu(ornekler)
print('\n=== İşlenmiş Corpus (Modele Hazır) ===')
for m in islenmiş_corpus:
    print(m)
