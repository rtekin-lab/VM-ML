# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 6
# Konum : BÖLÜM 6: Sınıflandırma: Karar Ağaçlarından Topluluk Öğrenmesine › 6.2. Karar Ağaçları ve Topluluk (Ensemble) Devrimi › 6.2.2. Bagging ve Random Forests › Python Uygulaması — Random Forest ve OOB
# Kitap  : Kod 6.6 (Random Forest: OOB hatası ve öznitelik öneml)
# Dosya : bolum06/06_02_02_python-uygulamasi-random-forest-ve-oob.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================
# --- Python: Random Forest — Kapsamlı Uygulama ---
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.inspection import permutation_importance

# --- Python: Random Forest — Kapsamlı Uygulama ---
# ─── 1. Veri ──────────────────────────────────────────────────────
data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# --- Python: Random Forest — Kapsamlı Uygulama ---
# ─── 2. Temel Random Forest + OOB Skoru ──────────────────────────
rf = RandomForestClassifier(
    n_estimators=200,
    max_features="sqrt",
    oob_score=True,          # OOB genelleme tahmini
    n_jobs=-1,               # Tüm CPU çekirdeklerini kullan
    random_state=42)
rf.fit(X_train, y_train)

# --- Python: Random Forest — Kapsamlı Uygulama ---
print(f"OOB Skoru:  {rf.oob_score_:.4f}")
print(f"Test Skoru: {rf.score(X_test, y_test):.4f}")

# --- Python: Random Forest — Kapsamlı Uygulama ---
# ─── 3. n_estimators Artışının Etkisi (Hata Analizi) ─────────────
oob_errors = []
for n in range(10, 301, 10):
    rf_n = RandomForestClassifier(n_estimators=n, oob_score=True,
                                   n_jobs=-1, random_state=42)
    rf_n.fit(X_train, y_train)
    oob_errors.append(1 - rf_n.oob_score_)
# n artıkça OOB hatası düşer, yaklaşık n=100-150 civarında plato oluşur

# --- Python: Random Forest — Kapsamlı Uygulama ---
# ─── 4. RandomizedSearchCV ile Hiperparametre Optimizasyonu ───────
param_dist = {
    "n_estimators"    : [100, 200, 300],
    "max_features"    : ["sqrt", "log2", 0.3, 0.5],
    "max_depth"       : [None, 10, 20, 30],
    "min_samples_leaf": [1, 2, 5, 10],
    "class_weight"    : [None, "balanced"]
}
rscv = RandomizedSearchCV(
    RandomForestClassifier(oob_score=True, n_jobs=-1, random_state=42),
    param_distributions=param_dist,
    n_iter=30, cv=5, scoring="roc_auc",
    n_jobs=-1, random_state=42)
rscv.fit(X_train, y_train)
print(f"En iyi parametreler: {rscv.best_params_}")
print(f"En iyi CV ROC-AUC:  {rscv.best_score_:.4f}")

# --- Python: Random Forest — Kapsamlı Uygulama ---
# ─── 5. Özellik Önemi (Gini + Permütasyon) ───────────────────────
best_rf = rscv.best_estimator_

# --- Python: Random Forest — Kapsamlı Uygulama ---
# Gini tabanlı özellik önemi
gini_imp = pd.Series(best_rf.feature_importances_,
                     index=data.feature_names).sort_values(ascending=False)
print("\nGini Tabanlı En Önemli 5 Özellik:")
print(gini_imp.head())

# --- Python: Random Forest — Kapsamlı Uygulama ---
# Permütasyon tabanlı özellik önemi (daha güvenilir)
perm_imp = permutation_importance(
    best_rf, X_test, y_test, n_repeats=15,
    random_state=42, scoring="roc_auc")
perm_df = pd.DataFrame({
    "importance_mean": perm_imp.importances_mean,
    "importance_std" : perm_imp.importances_std
}, index=data.feature_names).sort_values("importance_mean", ascending=False)
print("\nPermütasyon Tabanlı En Önemli 5 Özellik:")
print(perm_df.head())

# --- Python: Random Forest — Kapsamlı Uygulama ---
# ─── 6. Nihai Değerlendirme ───────────────────────────────────────
y_pred = best_rf.predict(X_test)
y_prob = best_rf.predict_proba(X_test)[:,1]
print(f"\nTest Doğruluğu: {roc_auc_score(y_test, y_prob):.4f} (ROC-AUC)")
print(classification_report(y_test, y_pred,
      target_names=["Benign","Malignant"]))
