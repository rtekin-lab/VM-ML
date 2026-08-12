# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.6. scikit-learn — Makine Öğrenmesi Kütüphanesi › C. scikit-learn Pipeline ile Tam ML İş Akışı
# Kitap  : Kod 1.41 (Scikit-learn Pipeline ile Tam ML İş Akışı) · Kod 1.42 (Scikit-learn Pipeline ile Tam ML İş Akışı) · Kod 1.43 (Model karşılaştırması (Estimator API'nın güc) · Kod 1.44 (Scikit-learn Pipeline ile Tam ML İş Akışı) · Kod 1.45 (En İyi Model: GridSearchCV ile Hiperparametr) · Kod 1.46 (Scikit-learn Pipeline ile Tam ML İş Akışı) · Kod 1.47 (Scikit-learn Pipeline ile Tam ML İş Akışı)
# Dosya : bolum01/01_02_06_c-scikit-learn-pipeline-ile-tam-ml-is-akisi.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, roc_curve)
from sklearn.impute import SimpleImputer

np.random.seed(42)

# ─── 1. Veri Seti ─────────────────────────────────────────────────────────────
X, y = make_classification(n_samples=2000, n_features=15, n_informative=10,
                            n_redundant=3, n_classes=2, random_state=42)
# %10 eksik değer ekle
mask = np.random.rand(*X.shape) < 0.10
X[mask] = np.nan

X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# ─── 2. Ön İşleme Pipeline ────────────────────────────────────────────────────
on_isleme = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler())
])

# ─── 3. Model Karşılaştırması (Estimator API'nin gücü) ────────────────────────
modeller = {
    'Lojistik Regresyon': LogisticRegression(max_iter=500, random_state=42),
    'Random Forest'     : RandomForestClassifier(n_estimators=200, random_state=42),
    'Gradient Boosting' : GradientBoostingClassifier(n_estimators=200, random_state=42),
}

print("=== MODEL KARŞILAŞTIRMASI (5-Katlı Çapraz Doğrulama) ===")
sonuclar = {}
for isim, model in modeller.items():
    boru = Pipeline([('on_isleme', on_isleme), ('model', model)])
    cv_skorlari = cross_val_score(boru, X_egitim, y_egitim, cv=5, scoring='roc_auc', n_jobs=-1)
    sonuclar[isim] = cv_skorlari
    print(f"  {isim:<25}: AUC = {cv_skorlari.mean():.4f} ± {cv_skorlari.std():.4f}")

# ─── 4. En İyi Model: GridSearchCV ile Hiperparametre Ayarı ──────────────────
print("\n=== BEST MODEL: GridSearchCV ===")
param_grid = {
    'model__n_estimators': [100, 200, 300],
    'model__max_depth'   : [3, 5, None],
}
boru_rf = Pipeline([('on_isleme', on_isleme),
                    ('model', RandomForestClassifier(random_state=42))])
grid_search = GridSearchCV(boru_rf, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
grid_search.fit(X_egitim, y_egitim)

print(f"En iyi parametreler: {grid_search.best_params_}")
print(f"CV AUC            : {grid_search.best_score_:.4f}")

# ─── 5. Test Seti Değerlendirmesi ─────────────────────────────────────────────
y_tahmin  = grid_search.predict(X_test)
y_olasilik= grid_search.predict_proba(X_test)[:, 1]
test_auc  = roc_auc_score(y_test, y_olasilik)

print(f"\n=== TEST SETİ SONUÇLARI ===")
print(f"Test AUC           : {test_auc:.4f}")
print(classification_report(y_test, y_tahmin, target_names=['Sınıf 0', 'Sınıf 1']))
