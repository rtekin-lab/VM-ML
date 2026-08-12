# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.1. Metin Ön İşleme ve Temel Temsil › 9.1.1. Temizlik: Tokenization, Stop-words Temizliği, Stemming ve Lemmatization › 9.1.1.4. Kök Bulma (Stemming) ve Gövdeleme (Lemmatization) › Lemmatization (Gövdeleme)
# Kitap  : Kod 9.3 (Kök bulma (stemming) ve gövdeleme (lemmatiza)
# Dosya : bolum09/09_01_01_04_lemmatization.py
# Gerekli: pip install nltk spacy
# ==========================================================================
import re
import nltk
import spacy
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# Gerekli NLTK verileri
for resource in ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger',
                  'punkt_tab', 'averaged_perceptron_tagger_eng']:
    nltk.download(resource, quiet=True)

# Örnek Metin
metin = "The quick brown foxes are jumping over the lazy dogs. Studies show they are better runners."

# 1. Ön Temizlik ve Tokenization
temiz = re.sub(r'[^a-zA-Z\s]', '', metin).lower()
tokenlar = word_tokenize(temiz)
stop_words = set(stopwords.words('english'))
temiz_tokenlar = [t for t in tokenlar if t not in stop_words]

print('Temizlenmiş Tokenlar:', temiz_tokenlar)

# 2. Stemming - Porter
porter = PorterStemmer()
porter_result = [porter.stem(t) for t in temiz_tokenlar]
print('\nPorter Stemming :', porter_result)

# 3. Stemming - Snowball (İngilizce)
snowball = SnowballStemmer('english')
snowball_result = [snowball.stem(t) for t in temiz_tokenlar]
print('Snowball Stemming:', snowball_result)

# 4. Lemmatization - NLTK WordNet (POS etiketiyle daha doğru)
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(nltk_tag):
    """NLTK POS etiketini WordNet formatına çevirir."""
    if nltk_tag.startswith('J'): return wordnet.ADJ
    elif nltk_tag.startswith('V'): return wordnet.VERB
    elif nltk_tag.startswith('N'): return wordnet.NOUN
    elif nltk_tag.startswith('R'): return wordnet.ADV
    else: return wordnet.NOUN

pos_tagged = pos_tag(temiz_tokenlar)
lemma_result = [lemmatizer.lemmatize(w, get_wordnet_pos(pos))
                for w, pos in pos_tagged]
print('NLTK Lemmatization (POS ile):', lemma_result)

# 5. Karşılaştırma tablosu
print('\n{:<15} {:<15} {:<15} {:<15}'.format(
    'Orijinal', 'Porter', 'Snowball', 'Lemma(POS)'))
print('-' * 65)
for orig, port, snow, lemma in zip(temiz_tokenlar, porter_result,
                                    snowball_result, lemma_result):
    print(f'{orig:<15} {port:<15} {snow:<15} {lemma:<15}')

# 6. spaCy ile Lemmatization (Endüstri standardı)
try:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(metin)
    print('\n=== spaCy Lemmatization ===')
    print([(t.text, t.lemma_, t.pos_) for t in doc if not t.is_stop and t.is_alpha])
except:
    print('spaCy: python -m spacy download en_core_web_sm')
