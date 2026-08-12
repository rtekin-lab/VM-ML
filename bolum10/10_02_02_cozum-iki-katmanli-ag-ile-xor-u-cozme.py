# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 10
# Konum : BÖLÜM 10: YAPAY SİNİR AĞLARINA GİRİŞ (ARTIFICIAL NEURAL NETWORKS) › 10.2. Perceptron (Yapay Nöron) ve Doğrusal Sınıflandırma › 10.2.2. Doğrusal Ayrılabilirlik Sorunu: XOR Problemi ve Minsky-Papert Eleştirisi › Çözüm: İki Katmanlı Ağ ile XOR'u Çözme
# Dosya : bolum10/10_02_02_cozum-iki-katmanli-ag-ile-xor-u-cozme.py
# Gerekli: pip install numpy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np

# ============================================================
# XOR PROBLEMI: PERCEPTRON'UN BAŞARISIZLIĞI ve ÇÖZÜM
# ============================================================

# 1. Tek katmanlı Perceptron ile XOR denemesi (başarısızlık)
print('=== XOR Problemi: Perceptron Başarısızlığı ===\n')

X_xor = np.array([[0,0],[0,1],[1,0],[1,1]])
y_xor = np.array([0, 1, 1, 0])

class SimplePerceptron:
    def __init__(self, lr=0.1, epochs=1000):
        self.lr = lr
        self.epochs = epochs

    def fit(self, X, y):
        np.random.seed(0)
        self.w = np.random.randn(X.shape[1]) * 0.01
        self.b = 0.0
        for _ in range(self.epochs):
            for xi, yi in zip(X, y):
                y_hat = 1 if np.dot(self.w, xi) + self.b >= 0 else 0
                delta = yi - y_hat
                self.w += self.lr * delta * xi
                self.b += self.lr * delta
        return self

    def predict(self, X):
        return np.array([1 if np.dot(self.w, xi) + self.b >= 0 else 0 for xi in X])

p_xor = SimplePerceptron(lr=0.1, epochs=500).fit(X_xor, y_xor)
pred = p_xor.predict(X_xor)
print('XOR girdileri       Beklenen  Tahmin  Doğru mu?')
for xi, yi, yp in zip(X_xor, y_xor, pred):
    correct = '✓' if yi == yp else '✗ YANLIŞ'
    print(f'  {xi}  →  {yi}         {yp}      {correct}')

accuracy = np.mean(pred == y_xor)
print(f'\nDoğruluk: {accuracy:.2%}  (Mükemmel doğruluk imkânsız!)')

# ============================================================
# 2. İki katmanlı ağ ile XOR çözümü (Manuel ağırlıklar)
# ============================================================
print('\n=== Çözüm: 2 Katmanlı Ağ ile XOR ===\n')

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def heaviside(z):
    return (z >= 0).astype(int)

# Gizli katman ağırlıkları (2 gizli nöron)
# h1 = OR benzeri (eşik 0.5), h2 = AND benzeri (eşik 1.5)
W1 = np.array([[1, 1],   # h1: x1 + x2 - 0.5
               [1, 1]])  # h2: x1 + x2 - 1.5
b1 = np.array([-0.5, -1.5])  # h1 bias, h2 bias

# Çıkış katmanı: y = h1 - h2 - 0.5
W2 = np.array([1, -1])
b2 = np.array([-0.5])

print('İşlem adımları:')
for xi in X_xor:
    # Gizli katman (Heaviside aktivasyon)
    h = heaviside(W1 @ xi + b1)
    # Çıkış katmanı (Heaviside aktivasyon)
    y = heaviside(W2 @ h + b2)
    expected = int(xi[0] != xi[1])  # XOR gerçek değeri
    print(f'  x={xi} → h={h} → y={y[0]}  [beklenen: {expected}]')

# ============================================================
# 3. NumPy ile mini 2-katman ağ - forward pass
# ============================================================
print('\n=== Forward Pass Matris Hesabı ===\n')

def forward_2layer(X, W1, b1, W2, b2):
    """İki katmanlı ağda ileri yayılım (tüm veriler birden)"""
    # Gizli katman
    Z1 = X @ W1.T + b1              # [4×2] @ [2×2].T + [2] = [4×2]
    H1 = heaviside(Z1)              # [4×2] — ikili aktivasyon
    # Çıkış katmanı
    Z2 = H1 @ W2 + b2               # [4×2] @ [2] + [1] = [4×1]
    Y  = heaviside(Z2)              # [4×1]
    return H1, Y

H1, Y_pred = forward_2layer(X_xor, W1, b1, W2, b2)

print('Gizli katman aktivasyonları (H1):')
print(H1)
print('\nFinal tahminler vs gerçek değerler:')
for xi, h, yp, ye in zip(X_xor, H1, Y_pred, y_xor):
    status = '✓' if yp == ye else '✗'
    print(f'  x={xi}, h={h}, ŷ={yp}, y={ye} {status}')
print(f'\n2-katmanlı ağ XOR doğruluğu: {np.mean(Y_pred == y_xor):.2%}')
