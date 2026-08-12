# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.2. Veri Standartlaştırma › 3.2.2.3. MaxAbsScaler ve Seyrek Veri Ölçeklendirme
# Kitap  : Kod 3.23 (MaxAbsScaler ile seyrek matris ölçeklendirme)
# Dosya : bolum03/03_02_02_03_maxabsscaler-ve-seyrek-veri-olceklendirme.py
# Gerekli: pip install numpy scikit-learn scipy
# ==========================================================================
# ─── MaxAbsScaler ile Seyrek Veri Ölçeklendirme ─────────────────
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.preprocessing import MaxAbsScaler

# TF-IDF benzeri seyrek matris
X = np.array([[0,3,0,0,5],[2,0,0,4,0],[0,0,7,0,0],[1,2,0,0,3]], dtype=float)
X_sparse = csr_matrix(X)

scaler = MaxAbsScaler()
X_scaled = scaler.fit_transform(X_sparse)

print("MaxAbsScaler sonucu:")
print(X_scaled.toarray().round(4))
print(f"Korunan sıfır sayısı: {(X_scaled.toarray()==0).sum()} / {X.size}")
print("Ölçekleme faktörleri (her sütun için):", scaler.scale_)
