# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.3. Örnek Proje: MNIST ile Uçtan Uca Görüntü Sınıflandırma › Bonus: Iris Veri Seti ile MLP Regresyon ve Sınıflandırma Karşılaştırması
# Kitap  : Kod 10.15 (Iris veri setinde MLP ile çok sınıflı sınıfl)
# Dosya : bolum10/10_06_03_bonus-iris-veri-seti-ile-mlp-regresyon-ve-sinifl.py
# Gerekli: pip install numpy scikit-learn tensorflow
# ==========================================================================
# ─────────────────────────────────────────────────────────────────────
# Iris Veri Seti: MLP ile Çoklu Sınıflandırma
# ─────────────────────────────────────────────────────────────────────

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
import numpy as np

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Normalizasyon: Önemli! Iris özellikleri farklı ölçeklerde
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Model
iris_model = keras.Sequential([
    keras.layers.Dense(64, activation="relu", input_shape=(4,),
                       kernel_initializer="he_normal"),
    keras.layers.Dense(32, activation="relu",
                       kernel_initializer="he_normal"),
    keras.layers.Dense(3, activation="softmax")   # 3 sınıf: setosa, versicolor, virginica
])

iris_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history = iris_model.fit(
    X_train_scaled, y_train,
    epochs=100,
    batch_size=16,
    validation_split=0.2,
    verbose=0,
    callbacks=[keras.callbacks.EarlyStopping(patience=15, restore_best_weights=True)]
)

_, test_acc = iris_model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Iris Test Doğruluğu: {test_acc:.4f}  ({test_acc*100:.1f}%)")

# Tahmin olasılıkları
probs = iris_model.predict(X_test_scaled[:3])
for i, (prob, true) in enumerate(zip(probs, y_test[:3])):
    print(f"Örnek {i}: Gerçek={iris.target_names[true]:12s} | ",
          f"{dict(zip(iris.target_names, np.round(prob,3)))}")
