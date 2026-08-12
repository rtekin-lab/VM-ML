# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.1. Veri Bilimi Nedir? Veri Madenciliği ile İlişkisi › 2.1.2. Veri Madenciliği ve Veri Bilimi İlişkisi › Veri Madenciliği Teknikleri ve Algoritmaları
# Kitap  : Kod 2.4 (Sınıflandırma: karar ağacı ile müşteri kaybı) · Kod 2.5 (Kümeleme: K-Means ile müşteri segmentasyonu) · Kod 2.6 (Birliktelik kuralları: pazar sepeti analizi) · Kod 2.7 (Regresyon: doğrusal modelle sürekli değer ta) · Kod 2.8 (Anomali tespiti: Isolation Forest ile aykırı)
# Dosya : bolum02/02_01_02_veri-madenciligi-teknikleri-ve-algoritmalari.py
# Gerekli: pip install matplotlib mlxtend numpy pandas scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Iris veri setinin yüklenmesi
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Verinin eğitim ve test alt kümelerine ayrılması (%70 Eğitim, %30 Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Model havuzunun tanımlanması
models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', random_state=42),
    'k-NN': KNeighborsClassifier(n_neighbors=5)
}

# Modellerin iteratif eğitimi ve performans değerlendirmesi
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel: {name}")
    print(f"Doğruluk Oranı: {accuracy:.4f}")
    print("Sınıflandırma Raporu:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

# 1. Sentetik Veri Kümesi Oluşturma
# 300 örnek, 4 merkezli ve 0.60 standart sapmalı veri üretimi
X, y_true = make_blobs(n_samples=300, centers=4,
                       cluster_std=0.60, random_state=42)

# 2. K-Means Modelinin Yapılandırılması ve Eğitimi
# n_clusters=4: Verinin 4 gruba ayrılacağı varsayılır
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
y_pred = kmeans.fit_predict(X)

# 3. Performans Değerlendirme Metrikleri
# Silhouette Skoru: Kümeleme kalitesini (-1 ile 1 arası) ölçer
# Inertia: Küme içi karesel uzaklıkların toplamıdır
silhouette = silhouette_score(X, y_pred)
inertia = kmeans.inertia_

print(f"Silhouette Skoru: {silhouette:.4f}")
print(f"Inertia (Toplam Karesel Mesafe): {inertia:.2f}")
print(f"\nKüme Merkezleri:\n{kmeans.cluster_centers_}")

# 4. İdeal Küme Sayısının Belirlenmesi: Dirsek Yöntemi (Elbow Method)
inertias = []
K_range = range(1, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)

# Sonuçların Raporlanması
print(f"\nFarklı k değerleri için Inertia sonuçları:")
for k, val in zip(K_range, inertias):
    print(f"k={k}: {val:.2f}")

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 1. Veri Hazırlama: İşlem (Transaction) Listesi
transactions = [
    ['Ekmek', 'Süt', 'Peynir'],
    ['Ekmek', 'Tereyağı'],
    ['Süt', 'Tereyağı', 'Yumurta'],
    ['Ekmek', 'Süt', 'Tereyağı', 'Peynir'],
    ['Ekmek', 'Süt', 'Tereyağı'],
    ['Süt', 'Peynir']
]

# 2. Veri Dönüştürme: One-Hot Encoding (Vektörizasyon)
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

# 3. Sık Öğe Kümelerinin Keşfi (Min Support = 0.3)
frequent_itemsets = apriori(df, min_support=0.3, use_colnames=True)

# 4. Birliktelik Kurallarının Türetilmesi (Min Confidence = 0.5)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

# 5. Analiz ve Raporlama
print("Keşfedilen Birliktelik Kuralları (Özet):")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())

# En yüksek kaldıraç (Lift) değerine sahip kuralların filtrelenmesi
top_rules = rules.nlargest(3, 'lift')
print("\n--- En Güçlü 3 İlişki Analizi ---")
for _, rule in top_rules.iterrows():
    print(f"Kural: {set(rule['antecedents'])} => {set(rule['consequents'])}")
    print(f"  Destek: {rule['support']:.2%}")
    print(f"  Güven:  {rule['confidence']:.2%}")
    print(f"  Kaldıraç (Lift): {rule['lift']:.2f}\n")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 1. Sentetik Veri Setinin Oluşturulması
np.random.seed(42)
n_samples = 200

# Bağımsız Değişkenler: Metrekare, Oda Sayısı, Yapı Yaşı
metrekare = np.random.uniform(50, 200, n_samples)
oda_sayisi = np.random.randint(1, 6, n_samples)
yas = np.random.uniform(0, 30, n_samples)

# Bağımlı Değişken: Fiyat (Sürekli Değer)
fiyat = (metrekare * 2000 +
         oda_sayisi * 50000 -
         yas * 1000 +
         np.random.normal(0, 20000, n_samples))

df = pd.DataFrame({
    'metrekare': metrekare,
    'oda_sayisi': oda_sayisi,
    'yas': yas,
    'fiyat': fiyat
})

# 2. Verinin Hazırlanması ve Bölünmesi
X = df[['metrekare', 'oda_sayisi', 'yas']]
y = df['fiyat']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Model Eğitimi
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Tahmin ve Performans Değerlendirme
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# 5. Sonuçların Raporlanması
print("Model Katsayıları (Betas):")
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature.capitalize()}: {coef:.2f}")

print(f"\nKesim Noktası (Intercept): {model.intercept_:.2f}")
print("-" * 30)
print(f"MSE  : {mse:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R² Skoru: {r2:.4f}")

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# 1. Veri Setinin Hazırlanması
# Normal dağılım sergileyen veriler ile yapay anomalilerin birleştirilmesi
np.random.seed(42)
normal_data = np.random.randn(200, 2)
anomalies = np.random.uniform(low=-6, high=6, size=(20, 2))
X = np.vstack([normal_data, anomalies])

# 2. Veri Standardizasyonu
# Özniteliklerin aynı ölçeğe getirilmesi algoritma performansını artırır
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Isolation Forest Modelinin Kurulması
# contamination: Veri setindeki beklenen anomali oranı
iso_forest = IsolationForest(contamination=0.1, random_state=42)
predictions = iso_forest.fit_predict(X_scaled)

# 4. Anomali Skorlarının Hesaplanması
# Skor ne kadar düşükse, gözlemin anomali olma ihtimali o kadar yüksektir
scores = iso_forest.score_samples(X_scaled)

# 5. Sonuçların Analizi
n_anomalies = np.sum(predictions == -1)
print(f"Tespit Edilen Toplam Anomali Sayısı: {n_anomalies}")

print("\nEn Yüksek Anomali Skoruna Sahip 5 Gözlem:")
anomaly_indices = np.argsort(scores)[:5]
for idx in anomaly_indices:
    print(f"  İndeks {idx:3d}: Anomali Skoru = {scores[idx]:.4f}")
