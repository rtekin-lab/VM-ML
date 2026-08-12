# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 6
# Konum : BÖLÜM 6: Sınıflandırma: Karar Ağaçlarından Topluluk Öğrenmesine › 6.1. Temel Sınıflandırıcılar › 6.1.3. Naive Bayes Sınıflandırıcılar › Python Uygulaması — Naive Bayes
# Kitap  : Kod 6.3 (Naive Bayes ile metin sınıflandırma: spam fi)
# Dosya : bolum06/06_01_03_python-uygulamasi-naive-bayes.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================
# ─── BÖLÜM A: Metin Sınıflandırma — Spam Filtresi ──────────────────
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score)

# Örnek e-posta veri seti
emails = [
    'Bedava kredi kartı teklifi hemen tıkla kazanma fırsatı',
    'Toplantı yarın saat 10da konferans odasında',
    'Büyük indirim sadece bugün yüzde yetmiş ucuz fiyat',
    'Proje raporu ekte gönderiyorum değerlendirmeni bekliyorum',
    'Ücretsiz üyelik hemen kayıt ol ödül kazan',
    'Müşteri şikayetleri için raporun hazır lütfen incele',
    'Para ödülü hemen al kredi başvurusu yap',
    'Akşam yemeği için rezervasyon yaptım saat sekizde',
    'Fatura vadesi geçti gecikme faizi işleniyor hemen öde',
    'Haftalık ekip toplantısı gündemine bakıldı',
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1: Spam, 0: Ham

# Pipeline: TF-IDF + MultinomialNB
# TF-IDF: Kelime önemini frekansa ve belge sayısına göre ağırlıklandırır
spam_pipeline = Pipeline([
    ('tfidf',       TfidfVectorizer(ngram_range=(1,2),  # Unigram+Bigram
                                   min_df=1,
                                   sublinear_tf=True)),
    ('classifier',  MultinomialNB(alpha=1.0))  # Laplace düzeltmesi
])

# Çapraz doğrulama (küçük veri seti için tüm veri kullanılıyor)
cv_scores = cross_val_score(spam_pipeline, emails, labels,
                             cv=3, scoring='accuracy')
print(f'Çapraz Doğrulama Doğruluk: {cv_scores.mean():.3f}')

spam_pipeline.fit(emails, labels)

# Yeni e-posta tahminleri
yeni_emailler = [
    'Bedava hediye çekilişi kazandınız hemen alın',
    'Yarınki sunum için slaytları paylaşıyorum',
]
tahminler = spam_pipeline.predict(yeni_emailler)
for email, tahmin in zip(yeni_emailler, tahminler):
    etiket = '🚫 SPAM' if tahmin == 1 else '✅ NORMAL'
    print(f'{etiket}: {email[:50]}')

# ─── BÖLÜM B: Sayısal Veri — Gaussian Naive Bayes ────────────────
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

wine = load_wine()
X_w, y_w = wine.data, wine.target

X_tr, X_te, y_tr, y_te = train_test_split(
    X_w, y_w, test_size=0.2, random_state=42, stratify=y_w
)

# GaussianNB için ölçeklendirme genellikle çok etkili değildir
# (normal dağılım varsayımı mevcutsa), ama yapılması zararlı değildir
gnb = GaussianNB(var_smoothing=1e-9)  # Sayısal kararlılık
gnb.fit(X_tr, y_tr)
y_pred_gnb = gnb.predict(X_te)

print('\n=== Gaussian Naive Bayes — Wine Veri Seti ===')
print(f'Test Doğruluğu: {accuracy_score(y_te, y_pred_gnb):.4f}')
print(classification_report(y_te, y_pred_gnb,
                             target_names=wine.target_names))

# Prior Olasılıklar (modelden okunabilir)
print('Sınıf Prior Olasılıkları:')
for cls, prior in enumerate(gnb.class_prior_):
    print(f'  Sınıf {cls}: {prior:.3f}')
