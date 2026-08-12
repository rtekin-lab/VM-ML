# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 6
# Konum : BÖLÜM 6: Sınıflandırma: Karar Ağaçlarından Topluluk Öğrenmesine › 6.1. Temel Sınıflandırıcılar › 6.1.2. K-En Yakın Komşu (K-Nearest Neighbors — KNN) › Python Uygulaması — KNN
# Kitap  : Kod 6.2 (KNN: k seçimi, uzaklık metrikleri ve ölçekle)
# Dosya : bolum06/06_01_02_python-uygulamasi-knn.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================
# ─── KNN: Kapsamlı Uygulama Örneği ─────────────────────────────────
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import (train_test_split,
                                      cross_val_score, GridSearchCV)
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ─── 1. Veri ──────────────────────────────────────────────────────
iris = load_iris()
X = iris.data      # 4 özellik: sepal/petal uzunluk-genişlik
y = iris.target    # 3 sınıf: 0,1,2

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ─── 2. Ölçeklendirme (ZORUNLU!) ─────────────────────────────────
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ─── 3. K Değeri Seçimi (Çapraz Doğrulama ile) ───────────────────
k_values = range(1, 31)
cv_scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k, weights='distance')
    scores = cross_val_score(knn, X_train_s, y_train,
                             cv=5, scoring='accuracy')
    cv_scores.append(scores.mean())

best_k = k_values[np.argmax(cv_scores)]
print(f'En iyi K = {best_k}, CV Doğruluk = {max(cv_scores):.4f}')

# ─── 4. Farklı Uzaklık Metriklerini Karşılaştırma ────────────────
metrics = {'euclidean': 2, 'manhattan': 1, 'chebyshev': None}
results = {}

for name, p_val in metrics.items():
    if p_val is not None:
        knn = KNeighborsClassifier(n_neighbors=best_k,
                                   metric='minkowski', p=p_val)
    else:
        knn = KNeighborsClassifier(n_neighbors=best_k,
                                   metric='chebyshev')
    knn.fit(X_train_s, y_train)
    results[name] = knn.score(X_test_s, y_test)

for metric, acc in results.items():
    print(f'{metric:15s}: {acc:.4f}')

# ─── 5. En iyi model ile değerlendirme ───────────────────────────
best_knn = KNeighborsClassifier(n_neighbors=best_k, weights='distance')
best_knn.fit(X_train_s, y_train)
y_pred = best_knn.predict(X_test_s)

print('\n=== Sınıflandırma Raporu ===')
print(classification_report(y_test, y_pred,
                             target_names=iris.target_names))
