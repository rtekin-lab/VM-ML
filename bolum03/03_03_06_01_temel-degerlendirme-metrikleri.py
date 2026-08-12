# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.6. Anomali Tespit Modellerini Degerlendirme › 3.3.6.1. Temel Degerlendirme Metrikleri
# Kitap  : Kod 3.36 (Anomali tespit modellerinin kapsamlı değerle)
# Dosya : bolum03/03_03_06_01_temel-degerlendirme-metrikleri.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# Kapsamlı Model Degerlendirme
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score,
                             roc_curve, precision_recall_curve)
from sklearn.model_selection import train_test_split
import warnings; warnings.filterwarnings("ignore")

np.random.seed(42)
n_norm, n_anom = 950, 50
X_n = np.random.multivariate_normal([5,5],[[2,0.5],[0.5,2]],n_norm)
X_a = np.random.uniform(-3,13,(n_anom,2))
X = np.vstack([X_n, X_a])
y = np.array([0]*n_norm+[1]*n_anom)
X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.3,stratify=y,random_state=42)
sc = StandardScaler().fit(X_tr)
X_tr_s = sc.transform(X_tr); X_te_s = sc.transform(X_te)

modeller = {
    "Isolation Forest": IsolationForest(contamination=0.05, random_state=42),
    "LOF (k=20)": LocalOutlierFactor(n_neighbors=20, contamination=0.05, novelty=True),
    "One-Class SVM": OneClassSVM(nu=0.05, kernel="rbf", gamma="scale"),
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
renkler = {"Isolation Forest":"#e74c3c","LOF (k=20)":"#3498db","One-Class SVM":"#2ecc71"}

for isim, model in modeller.items():
    model.fit(X_tr_s)
    pred = (model.predict(X_te_s)==-1).astype(int)
    skor = -model.decision_function(X_te_s)
    pr = precision_score(y_te,pred,zero_division=0)
    rc = recall_score(y_te,pred,zero_division=0)
    f1 = f1_score(y_te,pred,zero_division=0)
    auc = roc_auc_score(y_te,skor)
    print("{}: P={:.3f} R={:.3f} F1={:.3f} AUC={:.3f}".format(isim,pr,rc,f1,auc))
    fpr,tpr,_ = roc_curve(y_te,skor)
    p,r,_ = precision_recall_curve(y_te,skor)
    ax1.plot(fpr,tpr,color=renkler[isim],lw=2,label="{} ({:.3f})".format(isim,auc))
    ax2.plot(r,p,color=renkler[isim],lw=2,label="{} ({:.3f})".format(isim,average_precision_score(y_te,skor)))

ax1.plot([0,1],[0,1],"k--"); ax1.set_title("ROC Egrisi"); ax1.legend(fontsize=8)
ax2.set_title("Precision-Recall Egrisi"); ax2.legend(fontsize=8)
plt.tight_layout(); plt.show()
