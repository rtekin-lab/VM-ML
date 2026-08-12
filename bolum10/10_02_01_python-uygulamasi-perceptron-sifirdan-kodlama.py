# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.2. Perceptron (Yapay Nöron) ve Doğrusal Sınıflandırma › 10.2.1. Perceptron Mimarisi: Girdiler, Ağırlıklar, Bias ve Net Girdi › Python Uygulaması: Perceptron Sıfırdan Kodlama
# Kitap  : Kod 10.1 (Perceptron öğrenme kuralının sıfırdan kodlan)
# Dosya : bolum10/10_02_01_python-uygulamasi-perceptron-sifirdan-kodlama.py
# Gerekli: pip install matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class Perceptron:
    """
    Frank Rosenblatt'ın 1957 Perceptron modelinin NumPy ile sıfırdan implementasyonu.
    Sadece doğrusal ayrılabilir problemleri çözebilir.
    """
    def __init__(self, learning_rate=0.01, max_epochs=1000, random_state=42, sabir=5):
        self.lr = learning_rate
        self.max_epochs = max_epochs
        self.sabir = sabir   # yakınsama sonrası kaç epoch daha çizilsin
        self.random_state = random_state
        self.weights = None
        self.bias = None
        self.errors_per_epoch = []

    def _heaviside(self, z):
        """Heaviside basamak fonksiyonu: z >= 0 → 1, z < 0 → 0"""
        return np.where(z >= 0, 1, 0)

    def fit(self, X, y):
        """
        Perceptron'u veriden eğit.
        X: (n_samples, n_features) — özellik matrisi
        y: (n_samples,) — ikili etiketler (0 veya 1)
        """
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape

        # Ağırlıkları küçük rastgele değerlerle başlat
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = 0.0

        sifir_seri = 0
        for epoch in range(self.max_epochs):
            epoch_errors = 0
            # Her eğitim örneği için güncelleme (online learning)
            for xi, yi in zip(X, y):
                # İleri hesaplama
                z = np.dot(self.weights, xi) + self.bias
                y_hat = self._heaviside(z)

                # Hata hesabı ve güncelleme
                delta = yi - y_hat
                if delta != 0:  # Yanlış tahmin
                    self.weights += self.lr * delta * xi
                    self.bias   += self.lr * delta
                    epoch_errors += 1

            self.errors_per_epoch.append(epoch_errors)

            # Yakınsama kontrolü: arka arkaya 'sabir' epoch sıfır hata → dur.
            # (Tek epoch'ta durmak öğrenme eğrisini 2 noktaya indirger; eğrinin
            #  yakınsama sonrası düzleştiği de görülmelidir.)
            if epoch_errors == 0:
                sifir_seri += 1
                if sifir_seri >= self.sabir:
                    print(f'Yakınsadı! Epoch: {epoch+1-self.sabir}/{self.max_epochs}')
                    break
            else:
                sifir_seri = 0
        else:
            print(f'Uyarı: {self.max_epochs} epoch sonunda tam yakınsama yok.')

        return self

    def predict(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self._heaviside(z)

    def net_input(self, X):
        """Ham net girdi değerlerini döndürür (karar sınırı için kullanışlı)"""
        return np.dot(X, self.weights) + self.bias

# ============================================================
# 1. MANTIK KAPILARI TESTİ
# ============================================================
print('=== Mantık Kapısı Öğrenme Testi ===\n')

# AND kapısı
X_and = np.array([[0,0],[0,1],[1,0],[1,1]])
y_and = np.array([0, 0, 0, 1])

p_and = Perceptron(learning_rate=0.1, max_epochs=100)
p_and.fit(X_and, y_and)
y_pred_and = p_and.predict(X_and)
print(f'AND Kapısı → Tahminler: {y_pred_and}, Beklenen: {y_and}')
print(f'AND Ağırlıklar: {p_and.weights}, Bias: {p_and.bias:.3f}')

# OR kapısı
y_or = np.array([0, 1, 1, 1])
p_or = Perceptron(learning_rate=0.1, max_epochs=100)
p_or.fit(X_and, y_or)
print(f'\nOR Kapısı → Tahminler: {p_or.predict(X_and)}, Beklenen: {y_or}')

# ============================================================
# 2. GERÇEK VERİ SETİ: İRİS (2 SINIF)
# ============================================================
print('\n=== Iris Veri Seti (2 Sınıf) ===\n')

iris = load_iris()
# Yalnızca Setosa ve Versicolor (doğrusal ayrılabilir 2 özellik)
X_iris = iris.data[:100, :2]  # 2 özellik: sepal length, sepal width
y_iris = iris.target[:100]    # 0=Setosa, 1=Versicolor

# Ölçekleme (Perceptron için önemli: büyük özellikler küçük ağırlıklara yol açar)
scaler = StandardScaler()
X_iris_scaled = scaler.fit_transform(X_iris)

X_train, X_test, y_train, y_test = train_test_split(
    X_iris_scaled, y_iris, test_size=0.2, random_state=42)

p_iris = Perceptron(learning_rate=0.01, max_epochs=200)   # küçük lr → okunabilir eğri
p_iris.fit(X_train, y_train)

y_pred = p_iris.predict(X_test)
print(f'Test Doğruluğu: {accuracy_score(y_test, y_pred):.4f}')
print(classification_report(y_test, y_pred,
      target_names=['Setosa', 'Versicolor']))

# ============================================================
# 3. ÖĞRENME EĞRİSİ GÖRSELLEŞTİRME
# ============================================================
plt.figure(figsize=(12, 5))

# Hata eğrisi
plt.subplot(1, 2, 1)
# Ikinci ornek: Versicolor vs Virginica — DOGRUSAL AYRILAMAZ.
# Perceptron yakinsama teoremi yalnizca ayrilabilir veri icin gecerlidir;
# ayrilamayan veride hata sifira inmez, salinim yapar. Ogrenme egrisinin
# ogretici olmasi icin iki durum yan yana gosterilir.
X_zor = StandardScaler().fit_transform(iris.data[50:150, :2])
y_zor = (iris.target[50:150] == 2).astype(int)
p_zor = Perceptron(learning_rate=0.01, max_epochs=30, sabir=30)
p_zor.fit(X_zor, y_zor)

epochs = range(1, len(p_iris.errors_per_epoch) + 1)
plt.plot(epochs, p_iris.errors_per_epoch, 'o-', color='steelblue', linewidth=2,
         markersize=5, label='Setosa vs Versicolor (ayrilabilir)')
ep_zor = range(1, len(p_zor.errors_per_epoch) + 1)
plt.plot(ep_zor, p_zor.errors_per_epoch, 's--', color='#e74c3c', linewidth=1.6,
         markersize=4, alpha=0.85, label='Versicolor vs Virginica (ayrilamaz)')
plt.legend(fontsize=9)
plt.ylim(bottom=-0.5)
plt.xlabel('Epoch')
plt.ylabel('Hata Sayısı')
plt.title('Perceptron Öğrenme Eğrisi\n(ayrılabilir vs ayrılamaz veri)')
plt.grid(True, alpha=0.3)

# Karar sınırı
plt.subplot(1, 2, 2)
x_min, x_max = X_iris_scaled[:, 0].min() - 0.5, X_iris_scaled[:, 0].max() + 0.5
y_min, y_max = X_iris_scaled[:, 1].min() - 0.5, X_iris_scaled[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                      np.linspace(y_min, y_max, 200))
Z = p_iris.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdBu)
scatter = plt.scatter(X_iris_scaled[:, 0], X_iris_scaled[:, 1],
                       c=y_iris, cmap=plt.cm.RdBu, edgecolors='k', s=50)
plt.xlabel('Sepal Length (ölçeklenmiş)')
plt.ylabel('Sepal Width (ölçeklenmiş)')
plt.title('Perceptron Karar Sınırı\n(Iris: 2 Özellik)')
plt.colorbar(scatter)
plt.tight_layout()
plt.savefig('perceptron_karar.png', dpi=150)
plt.show()
print('\nGörsel kaydedildi: perceptron_karar.png')
