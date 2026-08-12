# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.1. Metin Ön İşleme ve Temel Temsil › 9.1.1. Temizlik: Tokenization, Stop-words Temizliği, Stemming ve Lemmatization › 9.1.1.2. Parçalama (Tokenization) › Tokenization Türleri
# Kitap  : Kod 9.1 (NLTK ve spaCy ile parçalama (tokenization))
# Dosya : bolum09/09_01_01_02_tokenization-turleri.py
# Gerekli: pip install nltk spacy
# ==========================================================================
import nltk
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize, TweetTokenizer
from nltk.util import ngrams

# Gerekli NLTK verileri (ilk kullanımda indirilmeli)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

metin = "Doğal dil işleme, yapay zekanın en heyecan verici dallarından biridir! "\
         "ChatGPT, BERT ve GPT-4 gibi modeller bu alanı kökten değiştirdi."

# 1. Kelime Tokenization (NLTK)
print('=== NLTK Kelime Tokenization ===')
nltk_tokens = word_tokenize(metin)
print(nltk_tokens)
# ['Doğal', 'dil', 'işleme', ',', 'yapay', 'zekanın', ...]

# 2. Cümle Tokenization (NLTK)
print('\n=== NLTK Cümle Tokenization ===')
cumleler = sent_tokenize(metin)
for i, c in enumerate(cumleler):
    print(f'Cümle {i+1}: {c}')

# 3. Tweet Tokenizer (Sosyal Medya için özelleştirilmiş)
tweet = "Harika ürün!! :) @marka #indirim fiyat 299 TL http://link.com"
tweet_tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
print('\n=== Tweet Tokenizer ===')
print(tweet_tokenizer.tokenize(tweet))
# ['Harika', 'ürün', '!', ':)', '#indirim', 'fiyat', '299', 'TL']

# 4. N-gram Tokenization
print('\n=== Bigram (2-gram) Tokenization ===')
bigrams = list(ngrams(word_tokenize('veri madenciliği çok önemli bir alandır'), 2))
print(bigrams[:5])

# 5. spaCy ile Gelişmiş Tokenization (POS ve bağımlılık bilgisiyle birlikte)
try:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp('Data mining and NLP are key topics in AI research.')
    print('\n=== spaCy Tokenization (POS etiketleriyle) ===')
    for token in doc:
        print(f'{token.text:<15} POS: {token.pos_:<8} DEP: {token.dep_}')
except OSError:
    print('spaCy modeli yüklenmedi. python -m spacy download en_core_web_sm')
