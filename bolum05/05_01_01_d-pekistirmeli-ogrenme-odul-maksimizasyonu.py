# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 5
# Konum : BÖLÜM 5: MAKİNE ÖĞRENMESİNE GİRİŞ VE REGRESYON ANALİZİ › 5.1. Makine Öğrenmesi Paradigması › 5.1.1. Öğrenme Türleri: Formal Tanımlar ve Matematiksel Çerçeve › D. Pekiştirmeli Öğrenme (Reinforcement Learning): Ödül Maksimizasyonu
# Kitap  : Kod 5.1 (Pekiştirmeli öğrenmede ödül maksimizasyonunu)
# Dosya : bolum05/05_01_01_d-pekistirmeli-ogrenme-odul-maksimizasyonu.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, silhouette_score

np.random.seed(42)

# ════════════════════════════════════════════════════════════════════════════
# A. GÖZETİMLİ ÖĞRENME — Binary Sınıflandırma
# ════════════════════════════════════════════════════════════════════════════

# Sentetik veri: 2 sınıf, 2 öznitelik
X_sup, y_sup = make_classification(n_samples=300, n_features=2, n_redundant=0,
                                    n_informative=2, n_clusters_per_class=1,
                                    class_sep=1.5, random_state=42)

# Train/Test split (70/30)
X_train, X_test, y_train, y_test = train_test_split(
    X_sup, y_sup, test_size=0.3, random_state=42)

# Model: Lojistik Regresyon
# Amaç: f: ℝ² → {0,1} fonksiyonunu öğren
model_sup = LogisticRegression()
model_sup.fit(X_train, y_train)

# Tahmin
y_pred = model_sup.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("═══ GÖZETİMLİ ÖĞRENME ═══")
print(f"Eğitim seti boyutu: {len(X_train)}")
print(f"Test seti boyutu  : {len(X_test)}")
print(f"Model Accuracy    : {accuracy:.3f}")
print(f"Öğrenilen ağırlıklar: {model_sup.coef_[0]}")
print(f"Kesişim (intercept) : {model_sup.intercept_[0]:.3f}")

# Görselleştirme
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Sol: Eğitim verisi + karar sınırı
ax1.scatter(X_train[y_train==0, 0], X_train[y_train==0, 1],
            c='blue', label='Sınıf 0 (Eğitim)', alpha=0.6, s=40)
ax1.scatter(X_train[y_train==1, 0], X_train[y_train==1, 1],
            c='red', label='Sınıf 1 (Eğitim)', alpha=0.6, s=40)

# Karar sınırı: w₁x₁ + w₂x₂ + b = 0  →  x₂ = -(w₁x₁ + b)/w₂
w1, w2 = model_sup.coef_[0]
b = model_sup.intercept_[0]
x1_line = np.linspace(X_train[:, 0].min(), X_train[:, 0].max(), 100)
x2_line = -(w1*x1_line + b) / w2
ax1.plot(x1_line, x2_line, 'k--', lw=2, label='Karar Sınırı')
ax1.set_title('Gözetimli: Eğitim + Karar Sınırı', fontweight='bold')
ax1.set_xlabel('Öznitelik 1'); ax1.set_ylabel('Öznitelik 2')
ax1.legend(); ax1.grid(alpha=0.3)

# Sağ: Test tahminleri
correct = (y_pred == y_test)
ax2.scatter(X_test[correct, 0], X_test[correct, 1],
            c='green', marker='o', label='Doğru Tahmin', alpha=0.7, s=60)
ax2.scatter(X_test[~correct, 0], X_test[~correct, 1],
            c='orange', marker='X', label='Yanlış Tahmin', s=100)
ax2.plot(x1_line, x2_line, 'k--', lw=2, label='Karar Sınırı')
ax2.set_title(f'Test Performansı (Acc: {accuracy:.2%})', fontweight='bold')
ax2.set_xlabel('Öznitelik 1'); ax2.legend(); ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "supervised_demo.png"), dpi=120, bbox_inches='tight')
plt.close()

# ════════════════════════════════════════════════════════════════════════════
# B. GÖZETİMSİZ ÖĞRENME — Kümeleme (K-Means)
# ════════════════════════════════════════════════════════════════════════════

# Sentetik veri: 4 doğal küme, ETİKETSİZ
X_unsup, y_true = make_blobs(n_samples=400, centers=4, n_features=2,
                              cluster_std=1.2, random_state=42)

# Gözetimsiz model: K-Means
# Amaç: X verilerini K kümeye böl, öyle ki küme içi varyans minimal olsun
k = 4
model_unsup = KMeans(n_clusters=k, random_state=42, n_init=10)
y_pred_unsup = model_unsup.fit_predict(X_unsup)

# Silhouette Score: Kümeleme kalitesi (-1 kötü, +1 mükemmel)
silhouette = silhouette_score(X_unsup, y_pred_unsup)

print("\n═══ GÖZETİMSİZ ÖĞRENME ═══")
print(f"Veri boyutu       : {len(X_unsup)}")
print(f"Küme sayısı (K)   : {k}")
print(f"Silhouette Score  : {silhouette:.3f}")
print(f"Küme merkezleri:\n{model_unsup.cluster_centers_}")

# Görselleştirme
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Sol: Gerçek (gizli) yapı
for i in range(4):
    ax1.scatter(X_unsup[y_true==i, 0], X_unsup[y_true==i, 1],
                label=f'Gerçek Küme {i}', alpha=0.6, s=40)
ax1.set_title('Gerçek (Gizli) Küme Yapısı', fontweight='bold')
ax1.set_xlabel('Öznitelik 1'); ax1.set_ylabel('Öznitelik 2')
ax1.legend(); ax1.grid(alpha=0.3)

# Sağ: K-Means tarafından bulunan kümeler
colors = ['red', 'blue', 'green', 'purple']
for i in range(k):
    ax2.scatter(X_unsup[y_pred_unsup==i, 0], X_unsup[y_pred_unsup==i, 1],
                c=colors[i], label=f'Bulunan Küme {i}', alpha=0.6, s=40)
# Küme merkezlerini işaretle
ax2.scatter(model_unsup.cluster_centers_[:, 0],
            model_unsup.cluster_centers_[:, 1],
            c='black', marker='X', s=200, label='Merkezler',
            edgecolors='yellow', linewidths=2)
ax2.set_title(f'K-Means Kümeleme (Silhouette: {silhouette:.3f})', fontweight='bold')
ax2.set_xlabel('Öznitelik 1'); ax2.legend(); ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "unsupervised_demo.png"), dpi=120, bbox_inches='tight')
plt.close()

print("\nGrafikler kaydedildi: /tmp/supervised_demo.png, /tmp/unsupervised_demo.png")
