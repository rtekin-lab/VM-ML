# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.3. PyCharm › 1.3.3.3. PyCharm Bilimsel Mod (Scientific Mode)
# Kitap  : Kod 1.73 (PyCharm Bilimsel Mod — hücre tabanlı interak)
# Dosya : bolum01/01_03_03_03_pycharm-bilimsel-mod.py
# Gerekli: pip install numpy pandas scikit-learn
# ==========================================================================
# PyCharm Bilimsel Mod — # %% hucreleri
# View > Scientific Mode secenegiyle etkinlestirilir
# Her # %% blogu ayri hucre olarak calistirilabilir

# %%
import pandas as pd
import numpy as np

# PyCharm'in DataFrame viewer'i otomatik acilir
df = pd.read_csv("veriler.csv")
print(f"Boyut: {df.shape}")

# %%
# Degisken inspector'da df, X, y degerleri gosterilir
X = df.drop("hedef", axis=1).values
y = df["hedef"].values
print(f"X: {X.shape}, y: {y.shape}")

# %%
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
sc = StandardScaler()
X_tr_s = sc.fit_transform(X_tr)
X_te_s = sc.transform(X_te)

model = LogisticRegression(max_iter=1000)
model.fit(X_tr_s, y_tr)
print(classification_report(y_te, model.predict(X_te_s)))
