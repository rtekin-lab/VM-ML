# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 5
# Konum : BÖLÜM 5: MAKİNE ÖĞRENMESİNE GİRİŞ VE REGRESYON ANALİZİ › 5.1. Makine Öğrenmesi Paradigması › 5.1.2. Model Değerlendirme Çerçevesi: Genelleme Yeteneğini Ölçmek › C. Performans Metrikleri: Problem Tipine Göre Seçim
# Kitap  : Kod 5.2 (Problem tipine göre başarım metriklerinin he)
# Dosya : bolum05/05_01_02_c-performans-metrikleri-problem-tipine-gore-seci.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression, load_iris
from sklearn.model_selection import (KFold, cross_val_score, cross_validate,
                                     learning_curve, validation_curve)
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, f1_score
import pandas as pd

np.random.seed(42)

# ════════════════════════════════════════════════════════════════════════════
# A. REGRESYON: K-FOLD CV İLE MODEL DEĞERLENDİRME
# ════════════════════════════════════════════════════════════════════════════

# Sentetik regresyon verisi
X_reg, y_reg = make_regression(n_samples=200, n_features=5, noise=10, random_state=42)

# Model: Ridge Regresyon (alpha=1.0)
model_ridge = Ridge(alpha=1.0)

# K-Fold tanımı (K=5, karıştırmalı)
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

# Çapraz doğrulama skorları (negatif MSE)
cv_scores = cross_val_score(model_ridge, X_reg, y_reg, cv=kfold,
                             scoring='neg_mean_squared_error')

# Mutlak değere çevir (MSE pozitif olmalı)
mse_scores = -cv_scores
rmse_scores = np.sqrt(mse_scores)

print("═══ REGRESYON: 5-FOLD CROSS-VALIDATION ═══")
print(f"Fold MSE Skorları : {mse_scores}")
print(f"Ortalama MSE      : {mse_scores.mean():.2f} ± {mse_scores.std():.2f}")
print(f"Ortalama RMSE     : {rmse_scores.mean():.2f} ± {rmse_scores.std():.2f}")

# R² skorları da hesaplayalım
cv_r2 = cross_val_score(model_ridge, X_reg, y_reg, cv=kfold, scoring='r2')
print(f"\nFold R² Skorları  : {cv_r2}")
print(f"Ortalama R²       : {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")

# Görselleştirme: Fold skorları
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

folds = np.arange(1, 6)
ax1.plot(folds, mse_scores, 'o-', color='#1E3A5F', markersize=10, lw=2, label='MSE')
ax1.axhline(mse_scores.mean(), color='red', ls='--', lw=2, label=f'Ortalama: {mse_scores.mean():.2f}')
ax1.fill_between(folds, mse_scores.mean()-mse_scores.std(),
                  mse_scores.mean()+mse_scores.std(),
                  alpha=0.2, color='red', label='±1 std')
ax1.set_xlabel('Fold #', fontsize=12); ax1.set_ylabel('MSE', fontsize=12)
ax1.set_title('K-Fold CV: MSE Skorları', fontweight='bold')
ax1.set_xticks(folds); ax1.legend(); ax1.grid(alpha=0.3)

ax2.plot(folds, cv_r2, 's-', color='#2E8B57', markersize=10, lw=2, label='R²')
ax2.axhline(cv_r2.mean(), color='red', ls='--', lw=2, label=f'Ortalama: {cv_r2.mean():.3f}')
ax2.set_xlabel('Fold #', fontsize=12); ax2.set_ylabel('R²', fontsize=12)
ax2.set_title('K-Fold CV: R² Skorları', fontweight='bold')
ax2.set_xticks(folds); ax2.legend(); ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "kfold_regression.png"), dpi=120, bbox_inches='tight')
plt.close()

# ════════════════════════════════════════════════════════════════════════════
# B. SINIFLANDIRMA: DETAYLI CV SONUÇLARI (cross_validate)
# ════════════════════════════════════════════════════════════════════════════

# Iris veri seti (çok sınıflı)
iris = load_iris()
X_clf, y_clf = iris.data, iris.target

# Model: Random Forest
model_rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Çoklu metrik ile CV
scoring_metrics = {
    'accuracy': 'accuracy',
    'precision_macro': 'precision_macro',
    'recall_macro': 'recall_macro',
    'f1_macro': 'f1_macro'
}

cv_results = cross_validate(model_rf, X_clf, y_clf, cv=5,
                             scoring=scoring_metrics, return_train_score=True)

print("\n═══ SINIFLANDIRMA: 5-FOLD CV (ÇOKLU METRİK) ═══")
results_df = pd.DataFrame({
    'Fold': range(1, 6),
    'Train Acc': cv_results['train_accuracy'],
    'Test Acc': cv_results['test_accuracy'],
    'Test F1': cv_results['test_f1_macro'],
    'Test Precision': cv_results['test_precision_macro'],
    'Test Recall': cv_results['test_recall_macro']
})
print(results_df.to_string(index=False))
print(f"\nOrtalama Test Accuracy: {cv_results['test_accuracy'].mean():.3f}")
print(f"Ortalama Test F1-Score: {cv_results['test_f1_macro'].mean():.3f}")

# Train vs Test performans karşılaştırması (overfitting kontrolü)
fig, ax = plt.subplots(figsize=(10, 6))
folds = np.arange(1, 6)
width = 0.35
ax.bar(folds - width/2, cv_results['train_accuracy'], width,
       label='Train Accuracy', color='#1E3A5F', alpha=0.8)
ax.bar(folds + width/2, cv_results['test_accuracy'], width,
       label='Test Accuracy', color='#C44D34', alpha=0.8)
ax.axhline(cv_results['train_accuracy'].mean(), color='blue', ls='--', lw=1.5, alpha=0.7)
ax.axhline(cv_results['test_accuracy'].mean(), color='red', ls='--', lw=1.5, alpha=0.7)
ax.set_xlabel('Fold #', fontsize=12); ax.set_ylabel('Accuracy', fontsize=12)
ax.set_title('Train vs Test Accuracy (Overfitting Check)', fontweight='bold')
ax.set_xticks(folds); ax.legend(); ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0.8, 1.05)
plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "kfold_classification.png"), dpi=120, bbox_inches='tight')
plt.close()

# ════════════════════════════════════════════════════════════════════════════
# C. LEARNING CURVE: Eğitim Seti Boyutu vs Performans
# ════════════════════════════════════════════════════════════════════════════

# Learning curve: Farklı eğitim boyutlarında model performansı
train_sizes, train_scores, test_scores = learning_curve(
    model_rf, X_clf, y_clf, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy', n_jobs=-1, random_state=42
)

# Ortalama ve std hesapla
train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
test_mean = test_scores.mean(axis=1)
test_std = test_scores.std(axis=1)

print("\n═══ LEARNING CURVE ANALİZİ ═══")
print(f"Min eğitim boyutu: {train_sizes.min():.0f} örnek")
print(f"Max eğitim boyutu: {train_sizes.max():.0f} örnek")
print(f"Final test acc   : {test_mean[-1]:.3f} ± {test_std[-1]:.3f}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(train_sizes, train_mean, 'o-', color='blue', lw=2, label='Train Score')
ax.fill_between(train_sizes, train_mean-train_std, train_mean+train_std,
                 alpha=0.2, color='blue')
ax.plot(train_sizes, test_mean, 's-', color='red', lw=2, label='CV Score (Test)')
ax.fill_between(train_sizes, test_mean-test_std, test_mean+test_std,
                 alpha=0.2, color='red')
ax.set_xlabel('Eğitim Seti Boyutu', fontsize=12)
ax.set_ylabel('Accuracy', fontsize=12)
ax.set_title('Learning Curve: Random Forest (Iris)', fontweight='bold')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "learning_curve.png"), dpi=120, bbox_inches='tight')
plt.close()

print("\nTüm grafikler kaydedildi: /tmp/kfold_*.png, /tmp/learning_curve.png")
