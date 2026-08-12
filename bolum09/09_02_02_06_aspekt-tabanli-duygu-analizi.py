# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.2. Modern NLP: Anlamsal Analiz › 9.2.2. Duygu Analizi (Sentiment Analysis): Sosyal Medya Verilerinde Kutuplaşma Analizi › 9.2.2.6. Aspekt Tabanlı Duygu Analizi (ABSA)
# Kitap  : Kod 9.10 (Aspekt tabanlı duygu analizi (ABSA))
# Dosya : bolum09/09_02_02_06_aspekt-tabanli-duygu-analizi.py
# Gerekli: pip install nltk
# ==========================================================================
import re
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
analyzer = SentimentIntensityAnalyzer()

# Basit kural tabanlı ABSA demo
# Gerçek ABSA için fine-tuned BERT modelleri kullanılır

ASPEKT_SOZLUGU = {
    'kamera': ['kamera', 'fotoğraf', 'çekim', 'lens', 'zoom', 'görüntü'],
    'pil': ['pil', 'batarya', 'şarj', 'enerji', 'dayanma'],
    'fiyat': ['fiyat', 'para', 'ücret', 'maliyet', 'değer', 'ucuz', 'pahalı'],
    'tasarim': ['tasarım', 'görünüm', 'hafif', 'ağır', 'güzel', 'estetik'],
    'performans': ['hız', 'işlemci', 'yavaş', 'hızlı', 'kasma', 'performans'],
}

def aspekt_duygu_analiz(yorum):
    """
    Verilen yorumdan aspektleri tespit eder ve
    her aspekt için duygu skoru hesaplar.
    """
    yorum_lower = yorum.lower()
    cumleler = yorum.split(',')  # Basit cümle bölme
    sonuclar = {}

    for aspekt, kelimeler in ASPEKT_SOZLUGU.items():
        ilgili_cumleler = []
        for cumle in cumleler:
            cumle_lower = cumle.lower()
            if any(k in cumle_lower for k in kelimeler):
                ilgili_cumleler.append(cumle.strip())

        if ilgili_cumleler:
            # Aspektle ilgili cümlelerin VADER skorunu hesapla
            skorlar = [analyzer.polarity_scores(c)['compound']
                       for c in ilgili_cumleler]
            ortalama_skor = sum(skorlar) / len(skorlar)
            karar = ('Pozitif' if ortalama_skor >= 0.05 else
                     'Negatif' if ortalama_skor <= -0.05 else 'Nötr')
            sonuclar[aspekt] = {
                'skor': round(ortalama_skor, 3),
                'karar': karar,
                'ilgili_cumle': ' | '.join(ilgili_cumleler)
            }

    return sonuclar

# Test
yorumlar = [
    'Kamera kalitesi mükemmel, fotoğraflar çok net. Fakat pil ömrü berbat, yarım günde bitiyor.',
    'Fiyatı biraz pahalı ama performansı gerçekten iyi. Tasarım da şık görünüyor.',
    'Hız açısından harika, kasma yok. Şarj çok uzun sürüyor ve pil zayıf.',
]

for yorum in yorumlar:
    print(f'\nYorum: {yorum[:60]}...')
    print('Aspekt Analizi:')
    sonuclar = aspekt_duygu_analiz(yorum)
    for aspekt, bilgi in sonuclar.items():
        print(f"  {aspekt:>12}: {bilgi['karar']:>8} (skor: {bilgi['skor']:>6}) — {bilgi['ilgili_cumle'][:40]}")
