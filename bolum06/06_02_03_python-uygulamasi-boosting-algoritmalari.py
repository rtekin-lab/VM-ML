# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 6
# Konum : BÖLÜM 6: Sınıflandırma: Karar Ağaçlarından Topluluk Öğrenmesine › 6.2. Karar Ağaçları ve Topluluk (Ensemble) Devrimi › 6.2.3. Boosting Algoritmaları (Modern Standart) › Python Uygulaması — Boosting Algoritmaları
# Kitap  : Kod 6.7 (AdaBoost, Gradient Boosting ve XGBoost karşı)
# Dosya : bolum06/06_02_03_python-uygulamasi-boosting-algoritmalari.py
# Gerekli: pip install catboost lightgbm numpy pandas scikit-learn xgboost
# ==========================================================================
# --- Python: AdaBoost ve Gradient Boosting ---
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import (AdaBoostClassifier,
                               GradientBoostingClassifier)
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, classification_report

# --- Python: AdaBoost ve Gradient Boosting ---
# ─── Ortak Veri Hazırlama ─────────────────────────────────────────
data = load_breast_cancer()
X, y = pd.DataFrame(data.data, columns=data.feature_names), data.target
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# --- Python: AdaBoost ve Gradient Boosting ---
# ─── AdaBoost ─────────────────────────────────────────────────────
# base_estimator: max_depth=1 (stump) varsayılan zayıf öğrenici
ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=200,
    learning_rate=0.5,
    random_state=42)
ada.fit(X_tr, y_tr)
print(f"AdaBoost ROC-AUC: {roc_auc_score(y_te, ada.predict_proba(X_te)[:,1]):.4f}")

# --- Python: AdaBoost ve Gradient Boosting ---
# Staging: Her iterasyonda test hatasını takip et
staged_auc = [roc_auc_score(y_te, pred[:,1])
              for pred in ada.staged_predict_proba(X_te)]
best_n = np.argmax(staged_auc) + 1
print(f"En iyi n_estimators: {best_n}, AUC: {max(staged_auc):.4f}")

# --- Python: AdaBoost ve Gradient Boosting ---
# ─── Sklearn GradientBoosting ────────────────────────────────────
gbm = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    subsample=0.8,          # Stochastic GB: alt-örnekleme ile hız+çeşitlilik
    max_features="sqrt",    # Her bölünmede rastgele özellik alt kümesi
    random_state=42)
gbm.fit(X_tr, y_tr)
print(f"GBM  ROC-AUC: {roc_auc_score(y_te, gbm.predict_proba(X_te)[:,1]):.4f}")

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
import xgboost as xgb
# pip install xgboost

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
# ─── XGBoost ─────────────────────────────────────────────────────
xgb_clf = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.8,
    colsample_bytree=0.8,   # Her ağaçta kullanılacak özellik oranı
    reg_alpha=0.1,          # L1 düzenlileştirme
    reg_lambda=1.0,         # L2 düzenlileştirme
    use_label_encoder=False,
    eval_metric="auc",
    random_state=42)

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
# Erken Durdurma (Early Stopping): Doğrulama seti ile fazla ağacı engelle
xgb_clf.fit(X_tr, y_tr,
            eval_set=[(X_te, y_te)],
            early_stopping_rounds=20,   # 20 ardışık gerileme toleransı
            verbose=False)

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
print(f"XGBoost En iyi iterasyon: {xgb_clf.best_iteration}")
print(f"XGBoost ROC-AUC: {roc_auc_score(y_te, xgb_clf.predict_proba(X_te)[:,1]):.4f}")

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
# ─── SHAP Değerleri ile Yorumlanabilirlik ────────────────────────
# pip install shap
import shap

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
explainer = shap.TreeExplainer(xgb_clf)
shap_values = explainer.shap_values(X_te)

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
# Global özellik önemi (SHAP bazlı)
shap_imp = pd.Series(
    np.abs(shap_values).mean(axis=0),
    index=data.feature_names).sort_values(ascending=False)
print("\nSHAP Tabanlı En Önemli 5 Özellik:")
print(shap_imp.head())

# --- Python: XGBoost — Erken Durdurma ve SHAP ---
# Tek bir örnek için yerel yorum
print("\nÖrnek 0 için SHAP açıklaması (ilk 5 özellik):")
for feat, sv in zip(data.feature_names[:5], shap_values[0][:5]):
    print(f"  {feat:35s}: {sv:+.4f}")

# --- Python: LightGBM ve CatBoost ---
import lightgbm as lgb
# pip install lightgbm catboost
from catboost import CatBoostClassifier

# --- Python: LightGBM ve CatBoost ---
# ─── LightGBM ────────────────────────────────────────────────────
lgbm_clf = lgb.LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,          # Yaprak sayısı; max_depth yerine ana kontrol
    max_depth=-1,           # -1 = sınırsız (num_leaves ile kontrol)
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    verbose=-1)

# --- Python: LightGBM ve CatBoost ---
lgbm_clf.fit(X_tr, y_tr,
             eval_set=[(X_te, y_te)],
             callbacks=[lgb.early_stopping(20), lgb.log_evaluation(0)])

# --- Python: LightGBM ve CatBoost ---
print(f"LightGBM ROC-AUC: {roc_auc_score(y_te, lgbm_clf.predict_proba(X_te)[:,1]):.4f}")

# --- Python: LightGBM ve CatBoost ---
# ─── CatBoost ────────────────────────────────────────────────────
# Kategorik değişkenleri belirtmek yeterli; otomatik kodlar
cat_clf = CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    l2_leaf_reg=3.0,
    random_seed=42,
    verbose=0)

# --- Python: LightGBM ve CatBoost ---
cat_clf.fit(X_tr, y_tr,
            eval_set=(X_te, y_te),
            early_stopping_rounds=20)

# --- Python: LightGBM ve CatBoost ---
print(f"CatBoost  ROC-AUC: {roc_auc_score(y_te, cat_clf.predict_proba(X_te)[:,1]):.4f}")

# --- Python: LightGBM ve CatBoost ---
# ─── Tüm Modelleri Karşılaştır ───────────────────────────────────
models = {
    "AdaBoost"       : ada,
    "GBM"            : gbm,
    "XGBoost"        : xgb_clf,
    "LightGBM"       : lgbm_clf,
    "CatBoost"       : cat_clf,
}
print("\n=== Model Karşılaştırması ===")
print(f"{'Model':15s}  {'ROC-AUC':>8s}  {'Accuracy':>9s}")
print("-" * 38)
for name, model in models.items():
    proba = model.predict_proba(X_te)[:,1]
    pred  = model.predict(X_te)
    auc   = roc_auc_score(y_te, proba)
    acc   = (pred == y_te).mean()
    print(f"{name:15s}  {auc:>8.4f}  {acc:>9.4f}")
