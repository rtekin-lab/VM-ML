# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.4. Agac Tabanlı Anomali Tespit Yontemleri › 3.3.4.2. One-Class SVM (OC-SVM)
# Kitap  : Kod 3.34 (One-Class SVM ile anomali tespiti)
# Dosya : bolum03/03_03_04_02_one-class-svm.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# One-Class SVM ile Anomali Tespiti
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

np.random.seed(42)
X_eg = np.random.multivariate_normal([3,3],[[1.5,0.5],[0.5,1.5]],200)
X_te_n = np.random.multivariate_normal([3,3],[[1.5,0.5],[0.5,1.5]],100)
X_te_a = np.random.uniform(-3, 9, (20, 2))
X_te = np.vstack([X_te_n, X_te_a])
y_te = np.array([1]*100+[-1]*20)

sc = StandardScaler().fit(X_eg)
X_eg_s = sc.transform(X_eg)
X_te_s = sc.transform(X_te)

ocsvm = OneClassSVM(kernel="rbf", nu=0.1, gamma="scale")
ocsvm.fit(X_eg_s)
tahmin = ocsvm.predict(X_te_s)
print(classification_report(y_te, tahmin, target_names=["Anomali","Normal"]))

# Izgara sinirlarini veriden turet (sabit -4..7 araligi uc noktalari disarida birakiyordu)
_tum = np.vstack([X_eg_s, X_te_s])
_pad = 0.8
xx, yy = np.meshgrid(
    np.linspace(_tum[:,0].min()-_pad, _tum[:,0].max()+_pad, 200),
    np.linspace(_tum[:,1].min()-_pad, _tum[:,1].max()+_pad, 200))
Z = ocsvm.decision_function(np.c_[xx.ravel(),yy.ravel()]).reshape(xx.shape)
fig, ax = plt.subplots(figsize=(8,6))
ax.contourf(xx, yy, Z, levels=15, cmap="RdBu_r", alpha=0.5)
ax.contour(xx, yy, Z, levels=[0], colors="black", linewidths=2)
ax.scatter(X_eg_s[:,0], X_eg_s[:,1], c="#95a5a6", s=15, alpha=0.4, label="Egitim")
ax.scatter(X_te_s[tahmin==1,0], X_te_s[tahmin==1,1], c="#3498db", s=40, label="Normal(test)")
ax.scatter(X_te_s[tahmin==-1,0],X_te_s[tahmin==-1,1],c="#e74c3c",s=80,marker="X",label="Anomali")
ax.set_title("One-Class SVM: Karar Siniri (RBF)"); ax.legend(); plt.show()
