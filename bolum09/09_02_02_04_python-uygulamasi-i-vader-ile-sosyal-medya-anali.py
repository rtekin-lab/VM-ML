# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.2. Modern NLP: Anlamsal Analiz › 9.2.2. Duygu Analizi (Sentiment Analysis): Sosyal Medya Verilerinde Kutuplaşma Analizi › 9.2.2.4. Python Uygulaması I: VADER ile Sosyal Medya Analizi
# Kitap  : Kod 9.8 (VADER ile sosyal medya metinlerinde duygu an)
# Dosya : bolum09/09_02_02_04_python-uygulamasi-i-vader-ile-sosyal-medya-anali.py
# Gerekli: pip install nltk numpy pandas
# ==========================================================================
import nltk
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter

nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

# ============================================================
# 1. TEMEL VADER ANALİZİ
# ============================================================
ornekler = [
    # Normal pozitif/negatif
    'The new product is absolutely fantastic! Highly recommend.',
    'Terrible service, worst experience of my life.',
    'The movie was okay, nothing special.',
    # Büyük harf şiddetlendirme
    'This is AMAZING! Best thing ever!!!',
    'This is amazing. Best thing ever.',
    # Negasyon testi
    'The food is not good at all.',
    'The food is good.',
    # Sarkasm (VADER bu konuda sınırlı)
    'Oh great, another Monday morning...',
    # Emoji ve sosyal medya
    'Just got promoted! :D #blessed',
    'Stuck in traffic again... :(',
]

print('='*70)
print(f'{"Tweet":<45} {"Neg":>5} {"Pos":>5} {"Comp":>6} {"Karar"}')
print('='*70)

for tweet in ornekler:
    s = analyzer.polarity_scores(tweet)
    karar = 'OLUMLU' if s['compound'] >= 0.05 else (
             'OLUMSUZ' if s['compound'] <= -0.05 else 'NÖTR')
    print(f"{tweet[:44]:<45} {s['neg']:>5.2f} {s['pos']:>5.2f}"
          f" {s['compound']:>6.3f} {karar}")

# ============================================================
# 2. SOSYAL MEDYA CORPUS ANALİZİ
# ============================================================
sosyal_medya_df = pd.DataFrame({
    'id': range(1, 11),
    'platform': ['Twitter']*5 + ['Reddit']*5,
    'metin': [
        'Love the new update! Works perfectly now #tech',
        'App keeps crashing! Developers fix this ASAP',
        'Decent product for the price, nothing extraordinary',
        'WORST APP EVER!!! Delete immediately!!!',
        'Pretty good actually, surprised by the quality :)',
        'This is the best library I have used in years!',
        'Does not work as advertised, very disappointing',
        'Average at best, would not buy again',
        'Outstanding! Exceeded all my expectations',
        'Terrible quality, broke after one day',
    ]
})

# VADER analizi uygula
def vader_analiz(metin):
    s = analyzer.polarity_scores(metin)
    s['karar'] = ('OLUMLU' if s['compound'] >= 0.05 else
                  'OLUMSUZ' if s['compound'] <= -0.05 else 'NÖTR')
    return pd.Series(s)

sonuclar = sosyal_medya_df['metin'].apply(vader_analiz)
df_analiz = pd.concat([sosyal_medya_df, sonuclar], axis=1)

print('\n=== Sosyal Medya Duygu Analizi Sonuçları ===')
print(df_analiz[['platform', 'metin', 'compound', 'karar']].to_string())

# ============================================================
# 3. PLATFORM VE DUYGU DAĞILIMI
# ============================================================
print('\n=== Platform Bazlı Duygu Dağılımı ===')
print(df_analiz.groupby(['platform', 'karar']).size().unstack(fill_value=0))

print('\n=== Ortalama Compound Skorları ===')
print(df_analiz.groupby('platform')['compound'].agg(['mean', 'std', 'min', 'max']))

# ============================================================
# 4. ZAMAN SERİSİ TREND ANALİZİ
# ============================================================
import random
random.seed(42)

# Simüle edilmiş günlük tweet verisi
gunler = pd.date_range('2024-01-01', periods=30)
gunluk_duygu = []

for gun in gunler:
    gun_skorlari = [random.gauss(0.1, 0.5) for _ in range(50)]
    gun_skorlari = [max(-1, min(1, s)) for s in gun_skorlari]
    gunluk_duygu.append({
        'tarih': gun,
        'ortalama_compound': np.mean(gun_skorlari),
        'pozitif_oran': sum(1 for s in gun_skorlari if s >= 0.05) / 50,
        'negatif_oran': sum(1 for s in gun_skorlari if s <= -0.05) / 50,
    })

trend_df = pd.DataFrame(gunluk_duygu)
print('\n=== 30 Günlük Duygu Trend Özeti ===')
print(trend_df[['tarih','ortalama_compound','pozitif_oran','negatif_oran']].tail(5))
