# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.2. Modern NLP: Anlamsal Analiz › 9.2.2. Duygu Analizi (Sentiment Analysis): Sosyal Medya Verilerinde Kutuplaşma Analizi › 9.2.2.5. Python Uygulaması II: Makine Öğrenmesi ile Duygu Sınıflandırma
# Kitap  : Kod 9.9 (TF-IDF ve lojistik regresyonla duygu sınıfla)
# Dosya : bolum09/09_02_02_05_python-uygulamasi-ii-makine-ogrenmesi-ile-duygu.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. ETİKETLENMİŞ VERİ SETİ
# ============================================================
belgeler = [
    # OLUMLU
    'This product is absolutely amazing quality is superb',
    'Excellent service fast delivery highly recommend',
    'Best purchase I have made great value for money',
    'Outstanding performance exceeded my expectations',
    'Fantastic product works perfectly love it',
    'Very happy with this purchase great quality',
    'Wonderful experience customer service is brilliant',
    'Perfect exactly what I needed works great',
    # OLUMSUZ
    'Terrible quality broke after two days waste of money',
    'Absolutely horrible product do not buy this',
    'Worst purchase ever completely useless',
    'Very disappointed quality is poor not worth the price',
    'Awful experience product stopped working immediately',
    'Completely broken arrived damaged not recommended',
    'Poor quality fails to deliver on promises',
    'Dreadful product returned it immediately',
    # NÖTR
    'The product works as described nothing special',
    'Average quality for the price acceptable',
    'Decent product does what it says on the box',
    'Okay product nothing extraordinary',
    'It works fine not great but not bad either',
    'Standard quality meets basic requirements',
]
etiketler = (['olumlu']*8 + ['olumsuz']*8 + ['nötr']*6)

X_train, X_test, y_train, y_test = train_test_split(
    belgeler, etiketler,
    test_size=0.25,
    random_state=42,
    stratify=etiketler
)

# ============================================================
# 2. ÇOKLU MODEL KARŞILAŞTIRMASI
# ============================================================
modeller = {
    'Multinomial Naive Bayes': Pipeline([
        ('tfidf', TfidfVectorizer(min_df=1, sublinear_tf=True,
                                   ngram_range=(1,2))),
        ('clf', MultinomialNB(alpha=0.5))
    ]),
    'Complement Naive Bayes': Pipeline([
        ('tfidf', TfidfVectorizer(min_df=1, sublinear_tf=True,
                                   ngram_range=(1,2))),
        ('clf', ComplementNB(alpha=0.5))
    ]),
    'Logistik Regresyon': Pipeline([
        ('tfidf', TfidfVectorizer(min_df=1, sublinear_tf=True,
                                   ngram_range=(1,2))),
        ('clf', LogisticRegression(max_iter=1000, C=1.0))
    ]),
    'LinearSVC': Pipeline([
        ('tfidf', TfidfVectorizer(min_df=1, sublinear_tf=True,
                                   ngram_range=(1,2))),
        ('clf', LinearSVC(C=1.0, max_iter=2000))
    ]),
}

print('=== Model Karşılaştırması (5 Katlı Çapraz Doğrulama) ===')
print(f'{"Model":<25} {"CV F1 Ort.":>12} {"±Std":>8}')
print('-' * 48)

en_iyi_model = None
en_iyi_f1 = 0

for model_adi, pipeline in modeller.items():
    cv_scores = cross_val_score(
        pipeline, belgeler, etiketler,
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        scoring='f1_weighted'
    )
    print(f'{model_adi:<25} {cv_scores.mean():>12.4f} {cv_scores.std():>8.4f}')
    if cv_scores.mean() > en_iyi_f1:
        en_iyi_f1 = cv_scores.mean()
        en_iyi_model = (model_adi, pipeline)

# ============================================================
# 3. EN İYİ MODEL — DETAYLI DEĞERLENDİRME
# ============================================================
print(f'\n=== En İyi Model: {en_iyi_model[0]} ===')
en_iyi_model[1].fit(X_train, y_train)
y_pred = en_iyi_model[1].predict(X_test)

print(classification_report(y_test, y_pred, zero_division=0))

# ============================================================
# 4. YENI METİNLER İÇİN TAHMİN
# ============================================================
yeni_metinler = [
    'Absolutely love this! Best product I have ever used!',
    'Complete garbage, broke on day one, do not buy',
    'It does the job, nothing to write home about',
    'NOT happy with this at all, very disappointed!',
]

print('\n=== Yeni Metin Tahminleri ===')
tahminler = en_iyi_model[1].predict(yeni_metinler)
for m, t in zip(yeni_metinler, tahminler):
    print(f'  [{t.upper():>8}] {m[:55]}')

# ============================================================
# 5. EN AYIRT EDİCİ KELİMELER
# ============================================================
# Pipeline içinden TF-IDF'e eriş
pipeline = en_iyi_model[1]
if hasattr(pipeline['clf'], 'coef_'):
    feature_names = pipeline['tfidf'].get_feature_names_out()
    siniflar = pipeline['clf'].classes_
    print('\n=== Sınıfa Göre En Ayırt Edici Kelimeler (Top 5) ===')
    for i, sinif in enumerate(siniflar):
        if hasattr(pipeline['clf'], 'coef_'):
            top_idx = np.argsort(pipeline['clf'].coef_[i])[-5:][::-1]
            top_kelimeler = [(feature_names[j], round(pipeline['clf'].coef_[i][j], 3))
                             for j in top_idx]
            print(f'{sinif.upper():>10}: {top_kelimeler}')
