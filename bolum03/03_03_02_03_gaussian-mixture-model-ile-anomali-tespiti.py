# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.2. Istatistiksel Anomali Tespit Yontemleri › 3.3.2.3. Gaussian Mixture Model (GMM) ile Anomali Tespiti
# Kitap  : Kod 3.30 (Gaussian karışım modeli ile anomali tespiti)
# Dosya : bolum03/03_03_02_03_gaussian-mixture-model-ile-anomali-tespiti.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# GMM ile Anomali Tespiti
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

np.random.seed(42)
X_k1 = np.random.multivariate_normal([2, 2],  [[1,0],[0,1]],   150)
X_k2 = np.random.multivariate_normal([8, 8],  [[1.5,0],[0,1.5]],100)
X_ay = np.random.uniform(-5, 13, (15, 2))
X = np.vstack([X_k1, X_k2, X_ay])

gmm = GaussianMixture(n_components=2, covariance_type="full", random_state=42)
gmm.fit(X)
log_prob = gmm.score_samples(X)
esik = np.percentile(log_prob, 5)
anomali_maske = log_prob < esik

print("GMM esik (5. yuzdelik): {:.4f}".format(esik))
print("Anomali sayisi: {}".format(anomali_maske.sum()))

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(X[~anomali_maske,0], X[~anomali_maske,1], c="#3498db", s=20, alpha=0.6, label="Normal")
ax.scatter(X[anomali_maske,0],  X[anomali_maske,1],  c="#e74c3c", s=80, marker="X", label="Anomali")
ax.set_title("GMM Anomali Tespiti", fontweight="bold"); ax.legend(); plt.show()
