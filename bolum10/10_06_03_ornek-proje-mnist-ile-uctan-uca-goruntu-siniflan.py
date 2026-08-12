# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.6. Keras ve TensorFlow ile İlk Sinir Ağı Uygulaması › 10.6.3. Örnek Proje: MNIST ile Uçtan Uca Görüntü Sınıflandırma
# Kitap  : Kod 10.13 (MNIST ile uçtan uca görüntü sınıflandırma)
# Dosya : bolum10/10_06_03_ornek-proje-mnist-ile-uctan-uca-goruntu-siniflan.py
# Gerekli: pip install matplotlib numpy scikit-learn seaborn tensorflow
# ==========================================================================
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# ─────────────────────────────────────────────────────────────────────
# ADIM 1: VERİ YÜKLEME VE KEŞİFSEL ANALİZ
# ─────────────────────────────────────────────────────────────────────

(X_train_raw, y_train), (X_test_raw, y_test) = keras.datasets.mnist.load_data()

print(f"Eğitim seti boyutu  : {X_train_raw.shape}")   # (60000, 28, 28)
print(f"Test seti boyutu    : {X_test_raw.shape}")    # (10000, 28, 28)
print(f"Piksel değer aralığı: [{X_train_raw.min()}, {X_train_raw.max()}]")
print(f"Sınıf dağılımı      : {np.bincount(y_train)}")

# Örnek görüntülerin görselleştirilmesi
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(X_train_raw[i], cmap="gray")
    ax.set_title(f"Sınıf: {y_train[i]}", fontsize=10)
    ax.axis("off")
plt.suptitle("MNIST Örnek Görüntüler", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.show()

# ─────────────────────────────────────────────────────────────────────
# ADIM 2: ÖN İŞLEME (PREPROCESSING)
# ─────────────────────────────────────────────────────────────────────

# 2a. Normalizasyon: 0-255 → 0.0-1.0
X_train = X_train_raw.astype("float32") / 255.0
X_test  = X_test_raw.astype("float32")  / 255.0

# 2b. Düzleştirme: 28×28 → 784 (MLP için)
X_train_flat = X_train.reshape(-1, 784)
X_test_flat  = X_test.reshape(-1, 784)

# 2c. Doğrulama setini ayır
from sklearn.model_selection import train_test_split
X_tr, X_val, y_tr, y_val = train_test_split(
    X_train_flat, y_train, test_size=0.15, random_state=42, stratify=y_train
)
print(f"Eğitim  : {X_tr.shape[0]} örnek")
print(f"Doğrulama: {X_val.shape[0]} örnek")
print(f"Test    : {X_test_flat.shape[0]} örnek")

# ─────────────────────────────────────────────────────────────────────
# ADIM 3: MODEL MİMARİSİ KURMA
# ─────────────────────────────────────────────────────────────────────

def build_mnist_model(hidden_units=[256, 128, 64],
                      dropout_rate=0.3,
                      use_batchnorm=True):
    """
    Parametrik MLP model oluşturucu.

    Args:
        hidden_units  : Her gizli katmandaki nöron sayıları listesi
        dropout_rate  : Dropout oranı (0: yok, 1: tümünü sıfırla)
        use_batchnorm : Batch Normalization eklensin mi?
    """
    model = keras.Sequential(name="MNIST_MLP")
    model.add(layers.Input(shape=(784,)))

    for i, units in enumerate(hidden_units):
        model.add(layers.Dense(
            units,
            activation="relu",
            kernel_initializer="he_normal",
            name=f"dense_{i+1}"
        ))
        if use_batchnorm:
            model.add(layers.BatchNormalization(name=f"bn_{i+1}"))
        if dropout_rate > 0:
            model.add(layers.Dropout(dropout_rate, name=f"dropout_{i+1}"))

    model.add(layers.Dense(10, activation="softmax", name="cikis"))
    return model

model = build_mnist_model(hidden_units=[256, 128, 64], dropout_rate=0.3)
model.summary()

# ─────────────────────────────────────────────────────────────────────
# ADIM 4: DERLEME VE EĞİTİM
# ─────────────────────────────────────────────────────────────────────

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Callback'ler
callbacks = [
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=8,
                                  restore_best_weights=True, verbose=1),
    keras.callbacks.ModelCheckpoint("best_mnist.keras",
                                    monitor="val_accuracy",
                                    save_best_only=True, verbose=0),
    keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5,
                                      patience=4, min_lr=1e-6, verbose=1),
    keras.callbacks.TensorBoard(log_dir="./logs/mnist", histogram_freq=1),
]

history = model.fit(
    X_tr, y_tr,
    epochs=50,
    batch_size=64,
    validation_data=(X_val, y_val),
    callbacks=callbacks,
    verbose=1
)

# ─────────────────────────────────────────────────────────────────────
# ADIM 5: EĞİTİM SONUÇLARININ GÖRSELLEŞTİRİLMESİ
# ─────────────────────────────────────────────────────────────────────

def plot_training_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Kayıp grafiği
    ax1.plot(history.history["loss"],     "b-",  lw=2, label="Eğitim Kaybı")
    ax1.plot(history.history["val_loss"], "r--", lw=2, label="Doğrulama Kaybı")
    ax1.set_xlabel("Epoch"); ax1.set_ylabel("Kayıp (Loss)")
    ax1.set_title("Kayıp Fonksiyonunun Gelişimi", fontweight="bold")
    ax1.legend(); ax1.grid(True, alpha=0.3)

    # Doğruluk grafiği
    ax2.plot(history.history["accuracy"],     "b-",  lw=2, label="Eğitim Doğruluğu")
    ax2.plot(history.history["val_accuracy"], "r--", lw=2, label="Doğrulama Doğruluğu")
    ax2.set_xlabel("Epoch"); ax2.set_ylabel("Doğruluk (Accuracy)")
    ax2.set_title("Doğruluğun Gelişimi", fontweight="bold")
    ax2.legend(); ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("mnist_training_history.png", dpi=150)
    plt.show()

plot_training_history(history)

# ─────────────────────────────────────────────────────────────────────
# ADIM 6: MODEL DEĞERLENDİRME
# ─────────────────────────────────────────────────────────────────────

test_loss, test_acc = model.evaluate(X_test_flat, y_test, verbose=0)
print(f"\nTest Kaybı (Loss)    : {test_loss:.4f}")
print(f"Test Doğruluğu (Acc) : {test_acc:.4f}  ({test_acc*100:.2f}%)")

# Sınıflandırma raporu
y_pred = np.argmax(model.predict(X_test_flat, verbose=0), axis=1)
print("\nSınıflandırma Raporu:")
print(classification_report(y_test, y_pred,
      target_names=[str(i) for i in range(10)]))

# Karışıklık matrisi (Confusion Matrix)
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=range(10), yticklabels=range(10))
plt.xlabel("Tahmin Edilen Sınıf"); plt.ylabel("Gerçek Sınıf")
plt.title("Karışıklık Matrisi (Confusion Matrix)", fontweight="bold")
plt.tight_layout(); plt.savefig("mnist_confusion_matrix.png", dpi=150)
plt.show()

# ─────────────────────────────────────────────────────────────────────
# ADIM 7: TAHMİN VE MODEL KAYDETME / YÜKLEME
# ─────────────────────────────────────────────────────────────────────

# Bireysel tahmin örneği
test_img = X_test_flat[0:1]   # (1, 784)
probabilities = model.predict(test_img, verbose=0)[0]
predicted_class = np.argmax(probabilities)
print(f"\nGerçek sınıf    : {y_test[0]}")
print(f"Tahmin edilen   : {predicted_class}")
print(f"Güven (confidence): {probabilities[predicted_class]*100:.2f}%")

# Model kaydetme (SavedModel formatı – önerilen)
model.save("mnist_model_saved")

# Model yükleme
loaded_model = keras.models.load_model("mnist_model_saved")
_, loaded_acc = loaded_model.evaluate(X_test_flat, y_test, verbose=0)
print(f"\nYüklenen model doğruluğu: {loaded_acc:.4f}")

# Legacy HDF5 formatı (eski projelerde kullanılabilir)
model.save("mnist_model.h5")
model_h5 = keras.models.load_model("mnist_model.h5")
