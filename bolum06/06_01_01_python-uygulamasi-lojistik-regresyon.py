# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 6
# Konum : BÖLÜM 6: Sınıflandırma: Karar Ağaçlarından Topluluk Öğrenmesine › 6.1. Temel Sınıflandırıcılar › 6.1.1. Lojistik Regresyon (Logistic Regression) › Python Uygulaması — Lojistik Regresyon
# Kitap  : Kod 6.1 (Lojistik regresyon: model kurma, değerlendir)
# Dosya : bolum06/06_01_01_python-uygulamasi-lojistik-regresyon.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================
# ─── Kütüphaneler ───────────────────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score,
                             RocCurveDisplay)

# ─── 1. Veri Yükleme ──────────────────────────────────────────────
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name='target')  # 1: Malignant, 0: Benign

# ─── 2. Eğitim / Test Bölmesi ────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)  # stratify=y: sınıf dağılımını korur

# ─── 3. Özellik Ölçeklendirme (ZORUNLU) ──────────────────────────
# Gradyan tabanlı optimizasyon için tüm özellikler aynı ölçekte olmalı
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)  # fit + transform
X_test_s  = scaler.transform(X_test)        # sadece transform (veri sızıntısı önlenir)

# ─── 4. Model Eğitimi ─────────────────────────────────────────────
# penalty='l2' (Ridge): varsayılan; C=1.0
# solver='lbfgs': küçük-orta boyutlu veri için optimize edilmiş
# max_iter: konverjans için yeterli iterasyon
lr = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs',
                        max_iter=1000, random_state=42)
lr.fit(X_train_s, y_train)

# ─── 5. Tahmin ve Değerlendirme ───────────────────────────────────
y_pred      = lr.predict(X_test_s)
y_pred_prob = lr.predict_proba(X_test_s)[:, 1]  # P(y=1)

print(f'Doğruluk (Accuracy): {accuracy_score(y_test, y_pred):.4f}')
print(f'ROC-AUC:             {roc_auc_score(y_test, y_pred_prob):.4f}')
print()
print('=== Sınıflandırma Raporu ===')
print(classification_report(y_test, y_pred,
                             target_names=['Benign', 'Malignant']))

# ─── 6. Karışıklık Matrisi ────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
print('Karışıklık Matrisi:')
print(pd.DataFrame(cm, index=['Gerçek 0','Gerçek 1'],
                       columns=['Tahmin 0','Tahmin 1']))

# ─── 7. Katsayı Yorumlama ─────────────────────────────────────────
coef_df = pd.DataFrame({
    'Özellik'   : data.feature_names,
    'Katsayı'   : lr.coef_[0],
    'Odds Oranı': np.exp(lr.coef_[0])
}).sort_values('Katsayı', ascending=False)

print('\nEn etkili 5 pozitif özellik:')
print(coef_df.head())

# ─── 8. Hiperparametre Optimizasyonu: GridSearch ──────────────────
param_grid = {
    'C'      : [0.001, 0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2'],
    'solver' : ['liblinear']  # L1 desteği için liblinear kullanılır
}
gs = GridSearchCV(LogisticRegression(max_iter=1000, random_state=42),
                  param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
gs.fit(X_train_s, y_train)
print(f'\nEn iyi parametreler: {gs.best_params_}')
print(f'En iyi CV ROC-AUC: {gs.best_score_:.4f}')
