# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.3. Anomali Tespiti › 3.3.4. Agac Tabanlı Anomali Tespit Yontemleri › 3.3.4.1. Isolation Forest
# Kitap  : Kod 3.33 (Isolation Forest, çok değişkenli anomali tes)
# Dosya : bolum03/03_03_04_01_isolation-forest.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# Isolation Forest ile Anomali Tespiti
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score

np.random.seed(42)
n_norm, n_anom = 1000, 50
X_norm = np.random.multivariate_normal([5,5,5,5], np.eye(4)*1.5, n_norm)
X_anom = np.random.uniform(low=-5, high=15, size=(n_anom, 4))
X = np.vstack([X_norm, X_anom])
y = np.array([1]*n_norm + [-1]*n_anom)
X_s = StandardScaler().fit_transform(X)

isof = IsolationForest(n_estimators=100, contamination=0.05, max_samples=256, random_state=42)
isof.fit(X_s)
tahmin = isof.predict(X_s)
skorlar = isof.decision_function(X_s)

y_bin = (y==-1).astype(int)
p_bin = (tahmin==-1).astype(int)
print(classification_report(y_bin, p_bin, target_names=["Normal","Anomali"]))
print("ROC-AUC: {:.4f}".format(roc_auc_score(y_bin, -skorlar)))

# contamination etkisi
for cont in [0.01, 0.03, 0.05, 0.08, 0.10]:
    prd = IsolationForest(contamination=cont, random_state=42).fit_predict(X_s)
    tp = ((prd==-1)&(y==-1)).sum()
    fp = ((prd==-1)&(y==1)).sum()
    fn = ((prd==1)&(y==-1)).sum()
    print("  cont={:.2f}: TP={}, FP={}, FN={}".format(cont,tp,fp,fn))
