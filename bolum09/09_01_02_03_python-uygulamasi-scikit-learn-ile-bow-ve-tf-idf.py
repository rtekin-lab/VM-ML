# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.1. Metin Ön İşleme ve Temel Temsil › 9.1.2. Sayısal Temsil: Bag-of-Words (BoW) ve TF-IDF Matrisleri › 9.1.2.3. Python Uygulaması: Scikit-learn ile BoW ve TF-IDF
# Kitap  : Kod 9.5 (scikit-learn ile Bag-of-Words ve TF-IDF matr)
# Dosya : bolum09/09_01_02_03_python-uygulamasi-scikit-learn-ile-bow-ve-tf-idf.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Örnek Belge Kümesi (Corpus)
corpus = [
    'veri madenciliği ile veri bilimi çok önemlidir',
    'makine öğrenmesi algoritmaları veri madenciliği temellidir',
    'derin öğrenme ve yapay zeka geleceği şekillendirir',
    'nlp metin madenciliği duygu analizi uygular',
    'metin sınıflandırma veri ön işleme gerektirir',
]

# ====================================================
# 1. BAG-OF-WORDS (Count Vectorizer)
# ====================================================
print('=' * 60)
print('BAG-OF-WORDS MATRİSİ')
print('=' * 60)

bow_vectorizer = CountVectorizer(
    min_df=1,          # En az 1 belgede geçmeli
    max_df=1.0,        # En fazla %100 belgede geçmeli (stop-word etkisi)
    ngram_range=(1, 2) # Unigram + Bigram
)
bow_matrix = bow_vectorizer.fit_transform(corpus)

print(f'Kelime Dağarcığı Boyutu (1-2 gram): {len(bow_vectorizer.vocabulary_)}')

# Sadece unigram için tekrar deneyelim
bow_uni = CountVectorizer(min_df=1)
bow_uni_matrix = bow_uni.fit_transform(corpus)

bow_df = pd.DataFrame(bow_uni_matrix.toarray(),
                       columns=bow_uni.get_feature_names_out(),
                       index=[f'Belge {i+1}' for i in range(len(corpus))])
print('\nBag-of-Words Matrisi (Unigram):')
print(bow_df)

# ====================================================
# 2. TF-IDF VEKTÖRİZASYONU
# ====================================================
print('\n' + '=' * 60)
print('TF-IDF MATRİSİ')
print('=' * 60)

tfidf_vectorizer = TfidfVectorizer(
    min_df=1,           # En az 1 belgede geçmeli
    max_df=0.95,        # Tüm belgelerde geçiyorsa kaldır (%95 üstü)
    sublinear_tf=True,  # TF için logaritmik ölçek: 1 + log(TF)
    norm='l2',          # L2 normalizasyon (kosinüs benzerliği için)
    ngram_range=(1, 1)  # Sadece unigram
)
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

tfidf_df = pd.DataFrame(tfidf_matrix.toarray(),
                         columns=tfidf_vectorizer.get_feature_names_out(),
                         index=[f'Belge {i+1}' for i in range(len(corpus))])
print('\nTF-IDF Matrisi:')
print(round(tfidf_df, 3))

# ====================================================
# 3. TF-IDF SKORLARI ANALİZİ
# ====================================================
print('\n=== Her Belge için En Ayırt Edici Kelimeler ===')
feature_names = tfidf_vectorizer.get_feature_names_out()
for i, belge in enumerate(corpus):
    tfidf_skorlar = tfidf_matrix[i].toarray()[0]
    top_idx = tfidf_skorlar.argsort()[-3:][::-1]  # En yüksek 3 skor
    top_kelimeler = [(feature_names[j], round(tfidf_skorlar[j], 4))
                     for j in top_idx if tfidf_skorlar[j] > 0]
    print(f'Belge {i+1}: {top_kelimeler}')

# ====================================================
# 4. KOSİNÜS BENZERLİĞİ ile Belge Benzerliği
# ====================================================
print('\n=== Belgeler Arası Kosinüs Benzerliği ===')
cos_sim = cosine_similarity(tfidf_matrix)
sim_df = pd.DataFrame(cos_sim,
                       index=[f'B{i+1}' for i in range(len(corpus))],
                       columns=[f'B{i+1}' for i in range(len(corpus))])
print(round(sim_df, 3))

# En benzer belge çifti
np.fill_diagonal(cos_sim, 0)  # Kendisiyle benzerliği sıfırla
max_idx = np.unravel_index(cos_sim.argmax(), cos_sim.shape)
print(f'\nEn benzer belge çifti: Belge {max_idx[0]+1} - Belge {max_idx[1]+1}')
print(f'Kosinüs Benzerliği: {cos_sim[max_idx]:.4f}')

# ====================================================
# 5. METIN SINIFLANDIRMA ile TF-IDF Entegrasyonu
# ====================================================
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Genişletilmiş etiketli corpus
belgeler = [
    'veri madenciliği veri analizi önemlidir',
    'makine öğrenmesi sınıflandırma algoritmaları',
    'derin öğrenme sinir ağları yapay zeka',
    'veri bilimi veri temizleme önişleme',
    'nlp metin işleme dil modeli',
    'kümeleme boyut indirgeme PCA algoritmaları',
    'regresyon sınıflandırma karar ağacı',
    'doğal dil işleme transformer BERT',
]
etiketler = [0, 0, 1, 0, 1, 0, 0, 1]  # 0: Veri Mad., 1: NLP/Derin Öğrenme

X_train, X_test, y_train, y_test = train_test_split(
    belgeler, etiketler, test_size=0.25, random_state=42
)

# TF-IDF + Naive Bayes Pipeline
clf_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(min_df=1, sublinear_tf=True)),
    ('clf', MultinomialNB(alpha=0.1))
])

clf_pipeline.fit(X_train, y_train)
y_pred = clf_pipeline.predict(X_test)

print('\n=== TF-IDF + Naive Bayes Sınıflandırma ===')
print(classification_report(y_test, y_pred,
      target_names=['Veri Mad.', 'NLP/DL'], zero_division=0))
