# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 6
# Konum : BÖLÜM 6: Sınıflandırma: Karar Ağaçlarından Topluluk Öğrenmesine › 6.2. Karar Ağaçları ve Topluluk (Ensemble) Devrimi › 6.2.1. Karar Ağaçları (Decision Trees) › Python Uygulaması — Karar Ağacı
# Kitap  : Kod 6.5 (Karar ağacı: eğitim, budama ve kural çıkarım)
# Dosya : bolum06/06_02_01_python-uygulamasi-karar-agaci.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================
# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import classification_report, accuracy_score

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
# ─── 1. Veri Hazırlama ────────────────────────────────────────────
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
# ─── 2. Temel Model (Budanmamış) ─────────────────────────────────
dt_full = DecisionTreeClassifier(criterion="entropy", random_state=42)
dt_full.fit(X_train, y_train)
print(f"Tam ağaç - Eğitim: {dt_full.score(X_train, y_train):.4f}, Test: {dt_full.score(X_test, y_test):.4f}")

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
# ─── 3. Ön-Budama (max_depth) ────────────────────────────────────
dt_pruned = DecisionTreeClassifier(
    criterion="entropy", max_depth=4,
    min_samples_split=10, min_samples_leaf=5,
    random_state=42)
dt_pruned.fit(X_train, y_train)
print(f"Budanmış ağaç - Test: {dt_pruned.score(X_test, y_test):.4f}")

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
# ─── 4. Sonradan-Budama: Cost Complexity Pruning ─────────────────
path = dt_full.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas[:-1]   # Son değer (tam budama) hariç

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
cv_scores = []
for alpha in ccp_alphas:
    dt = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42)
    scores = cross_val_score(dt, X_train, y_train, cv=5)
    cv_scores.append(scores.mean())

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
best_alpha = ccp_alphas[np.argmax(cv_scores)]
print(f"En iyi ccp_alpha: {best_alpha:.6f}")

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
dt_ccp = DecisionTreeClassifier(ccp_alpha=best_alpha, random_state=42)
dt_ccp.fit(X_train, y_train)
print(f"CCP Budanmış - Test: {dt_ccp.score(X_test, y_test):.4f}")

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
# ─── 5. Özellik Önemi Analizi ────────────────────────────────────
feat_imp = pd.Series(dt_ccp.feature_importances_,
                     index=data.feature_names).sort_values(ascending=False)
print("\nEn önemli 5 özellik:")
print(feat_imp.head())

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
# ─── 6. Karar Kurallarını Metin Olarak Görüntüleme ───────────────
print("\nKarar Ağacı Kuralları (ilk 3 seviye):")
print(export_text(dt_ccp, feature_names=list(data.feature_names),
                  max_depth=3))

# --- Python: Kapsamlı Karar Ağacı Uygulaması ---
# ─── 7. Sınıflandırma Raporu ─────────────────────────────────────
y_pred = dt_ccp.predict(X_test)
print(classification_report(y_test, y_pred,
      target_names=["Benign", "Malignant"]))
