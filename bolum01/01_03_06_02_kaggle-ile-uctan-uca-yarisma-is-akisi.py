# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.6. Kaggle Notebooks (Kernels) › 1.3.6.2. Kaggle ile Uctan Uca Yarısma Is Akisi
# Kitap  : Kod 1.82 (Kaggle ev fiyat yarışması — uçtan uca ML pip)
# Dosya : bolum01/01_03_06_02_kaggle-ile-uctan-uca-yarisma-is-akisi.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================
# Kaggle Notebook — Ev Fiyat Tahmini Ornegi
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

# Veri yukle
train = pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/train.csv")
test  = pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/test.csv")

# Hedef degisken
y = np.log1p(train["SalePrice"])

# Sayisal ve kategorik sutunlar
num_cols = train.select_dtypes(include=np.number).columns.drop(["SalePrice","Id"]).tolist()
cat_cols = train.select_dtypes(include="object").columns.tolist()

# Pipeline
num_transformer = Pipeline([("imputer", SimpleImputer(strategy="median")),
                             ("scaler", StandardScaler())])
cat_transformer = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                             ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value",
                                                        unknown_value=-1))])

preprocessor = ColumnTransformer([
    ("num", num_transformer, num_cols),
    ("cat", cat_transformer, cat_cols),
])

model = Pipeline([
    ("prep",  preprocessor),
    ("model", GradientBoostingRegressor(n_estimators=300, max_depth=4,
                                         learning_rate=0.05, random_state=42))
])

# Capraz dogrulama
X = train[num_cols + cat_cols]
cv = cross_val_score(model, X, y, cv=5, scoring="neg_root_mean_squared_error")
print(f"RMSE (5-fold CV): {-cv.mean():.4f} +/- {cv.std():.4f}")

# Model egit ve tahmin
model.fit(X, y)
tahmin = np.expm1(model.predict(test[num_cols + cat_cols]))

# Kaggle gonderi dosyasi
gonteri = pd.DataFrame({"Id": test["Id"], "SalePrice": tahmin})
gonteri.to_csv("submission.csv", index=False)
print(gonteri.head())
