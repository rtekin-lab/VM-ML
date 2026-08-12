# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 7
# Konum : BÖLÜM 7: GÖZETİMSİZ ÖĞRENME: KÜMELEME VE BOYUT İNDİRGEME › 7.1. Kümeleme Analizi (Cluster Analysis) › 7.1.3. Yoğunluk Tabanlı Yöntemler (DBSCAN) › ε ve MinPts Parametrelerinin Seçimi › ε Seçimi: k-NN Mesafe Grafiği
# Dosya : bolum07/07_01_03_secimi-k-nn-mesafe-grafigi.py
# Gerekli: pip install scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# ─── Ön hazırlık ─────────────────────────────────────────────────────
# Bu kesim, kitapta bir önceki kesimde kurulan veriyi/modeli kullanır.
# Dosyanın tek başına çalışabilmesi için o hazırlık burada yinelenmiştir.
# Kaynak: bolum07/07_01_03_python-uygulamasi-dbscan-ve-hdbscan.py
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
X_ham, _ = make_moons(n_samples=300, noise=0.05, random_state=42)
X_sc = StandardScaler().fit_transform(X_ham)
# ─── Ön hazırlık sonu ────────────────────────────────────────────────

import numpy as np
import matplotlib.pyplot as plt
# --- Python: k-NN Mesafe Grafiği ile ε Seçimi ---
from sklearn.neighbors import NearestNeighbors

# --- Python: k-NN Mesafe Grafiği ile ε Seçimi ---
MinPts = 5
k = MinPts - 1   # k. en yakın komşu mesafesi

# --- Python: k-NN Mesafe Grafiği ile ε Seçimi ---
nn = NearestNeighbors(n_neighbors=k)
nn.fit(X_sc)
distances, _ = nn.kneighbors(X_sc)

# --- Python: k-NN Mesafe Grafiği ile ε Seçimi ---
# k. komşu mesafeleri büyükten küçüğe sırala
k_distances = np.sort(distances[:, -1])[::-1]

# --- Python: k-NN Mesafe Grafiği ile ε Seçimi ---
plt.figure(figsize=(8, 4))
plt.plot(k_distances, linewidth=2)
plt.xlabel("Noktalar (büyükten küçüğe sıralı)")
plt.ylabel(f"{k}. En Yakın Komşu Mesafesi")
plt.title(f"k-NN Mesafe Grafiği (k={k}) — Dirsek Noktası = optimal ε")
# Dirsek noktasini elle secmek yerine egrinin en buyuk egrilik noktasindan turet.
# (Sabit 0.5 degeri egrinin cok uzerinde kaliyor ve grafigi yaniltici hale getiriyordu.)
# Dirsek: egrinin ilk ve son noktasini birlestiren kirise en uzak nokta
_x = np.arange(len(k_distances), dtype=float)
_y = k_distances.astype(float)
_xn = (_x - _x.min()) / (_x.max() - _x.min())
_yn = (_y - _y.min()) / (_y.max() - _y.min())
_p1 = np.array([_xn[0], _yn[0]])
_p2 = np.array([_xn[-1], _yn[-1]])
_vek = _p2 - _p1
_vek = _vek / np.linalg.norm(_vek)
_noktalar = np.column_stack([_xn, _yn]) - _p1
_izdusum = np.outer(_noktalar @ _vek, _vek)
_uzaklik = np.linalg.norm(_noktalar - _izdusum, axis=1)
_dirsek = int(np.argmax(_uzaklik))
eps_tahmin = float(_y[_dirsek])
plt.axhline(y=eps_tahmin, color="red", linestyle="--",
            label=f"ε ≈ {eps_tahmin:.3f} (dirsek noktası)")
plt.axvline(x=_dirsek, color="gray", linestyle=":", linewidth=1)
plt.legend(); plt.tight_layout(); plt.show()
