# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.4. Normalizasyon mu, Standartlaştırma mı? Seçim Rehberi
# Kitap  : Kod 3.25 (Scikit-learn Pipeline ve ColumnTransformer i)
# Dosya : bolum03/03_02_04_normalizasyon-mu-standartlastirma-mi-secim-rehbe.py
# Gerekli: pip install numpy scikit-learn
# ==========================================================================
# ─── Pipeline ile Güvenli Ölçeklendirme ──────────────────────────
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# YANLIŞ: tüm veri üzerinde fit (data leakage!)
# scaler.fit_transform(X)  <- X test de içeriyor!

# DOĞRU: Pipeline kullanımı
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LogisticRegression(max_iter=1000, random_state=42)),
])
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="accuracy")
print(f"Pipeline CV: %{cv_scores.mean()*100:.2f} ± %{cv_scores.std()*100:.2f}")

# ColumnTransformer: farklı sütunlara farklı dönüşüm
preprocessor = ColumnTransformer(transformers=[
    ("zscore", StandardScaler(),          list(range(5))),
    ("yeo",    PowerTransformer("yeo-johnson"), list(range(5,10))),
])
full_pipe = Pipeline([("prep", preprocessor), ("model", LogisticRegression(max_iter=1000))])
full_pipe.fit(X_train, y_train)
print(f"ColumnTransformer Test Doğruluğu: %{full_pipe.score(X_test,y_test)*100:.2f}")
