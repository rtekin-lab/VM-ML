# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 5
# Konum : BÖLÜM 5: MAKİNE ÖĞRENMESİNE GİRİŞ VE REGRESYON ANALİZİ › 5.2. Regresyon Analizi: Klasikten Moderne › 5.2.2. Modern Optimizasyon: Gradyan İnişi › A. Gradyan İnişi Matematiği
# Dosya : bolum05/05_02_02_a-gradyan-inisi-matematigi.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
X = np.random.randn(200, 1)
y = 2*X.ravel() + 3 + np.random.randn(200)*0.5

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_b = np.c_[np.ones((len(X_scaled), 1)), X_scaled]

def batch_gd(X, y, lr=0.01, n_iter=1000):
    m, n = X.shape
    theta = np.random.randn(n)
    history = []
    for _ in range(n_iter):
        gradients = (1/m) * X.T.dot(X.dot(theta) - y)
        theta -= lr * gradients
        cost = (1/(2*m)) * np.sum((X.dot(theta) - y)**2)
        history.append(cost)
    return theta, history

def sgd(X, y, lr=0.01, n_epochs=50):
    m, n = X.shape
    theta = np.random.randn(n)
    history = []
    for _ in range(n_epochs):
        for i in range(m):
            gradients = X[i:i+1].T.dot(X[i:i+1].dot(theta) - y[i:i+1])
            theta -= lr * gradients
        cost = (1/(2*m)) * np.sum((X.dot(theta) - y)**2)
        history.append(cost)
    return theta, history

theta_b, hist_b = batch_gd(X_b, y, lr=0.1, n_iter=500)
theta_s, hist_s = sgd(X_b, y, lr=0.01, n_epochs=50)

print(f"Batch GD final θ: {theta_b}")
print(f"SGD final θ: {theta_s}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(hist_b, 'b-', lw=2, label='Batch GD', alpha=0.8)
ax.plot(hist_s, 'r-', lw=2, label='SGD', alpha=0.7)
ax.set_xlabel('Iteration/Epoch')
ax.set_ylabel('Cost (MSE)')
ax.set_title('Gradient Descent Convergence')
ax.legend()
ax.grid(alpha=0.3)
ax.set_yscale('log')
plt.savefig(os.path.join(tempfile.gettempdir(), "gd_convergence.png"), dpi=120)
print("Saved: /tmp/gd_convergence.png")
