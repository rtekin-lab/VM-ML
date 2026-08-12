# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.3. Örnek Proje: MNIST ile Uçtan Uca Görüntü Sınıflandırma › Model Performans Analizi: Hatalı Tahminlerin İncelenmesi
# Kitap  : Kod 10.14 (Hatalı tahminlerin incelenmesi ve hata matri)
# Dosya : bolum10/10_06_03_model-performans-analizi-hatali-tahminlerin-ince.py
# Gerekli: pip install pandas
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum10/10_06_02_adim-3-*
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import confusion_matrix
(X_train, y_train), (X_test_raw, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 784).astype("float32") / 255.0
X_test  = X_test_raw.reshape(-1, 784).astype("float32") / 255.0
model = keras.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(X_train, y_train, epochs=5, batch_size=128, verbose=0)
y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
cm = confusion_matrix(y_test, y_pred)
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

import numpy as np
import matplotlib.pyplot as plt
# Hatalı tahminleri bul
wrong_idx = np.where(y_pred != y_test)[0]
print(f"Hatalı tahmin sayısı: {len(wrong_idx)} / {len(y_test)}")
print(f"Hata oranı          : {len(wrong_idx)/len(y_test)*100:.2f}%")

# En çok karıştırılan çiftler
import pandas as pd
cm_df = pd.DataFrame(cm, index=range(10), columns=range(10))
np.fill_diagonal(cm, 0)  # Doğru tahminleri sıfırla
most_confused = np.unravel_index(cm.argmax(), cm.shape)
print(f"\nEn çok karıştırılan çift: {most_confused[0]} ↔ {most_confused[1]}")

# Hatalı örnekleri görselleştir
fig, axes = plt.subplots(3, 6, figsize=(15, 8))
for i, ax in enumerate(axes.flat):
    if i < len(wrong_idx):
        idx = wrong_idx[i]
        ax.imshow(X_test_raw[idx], cmap="gray")
        ax.set_title(f"G:{y_test[idx]} T:{y_pred[idx]}",
                     color="red", fontsize=9)
        ax.axis("off")
plt.suptitle("Hatalı Sınıflandırılan Örnekler (G=Gerçek, T=Tahmin)",
             fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("wrong_predictions.png", dpi=150)
plt.show()
