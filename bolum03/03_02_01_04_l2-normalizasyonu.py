# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 3
# Konum : BÖLÜM 3: Veri Ön İşleme ve Temizleme Teknikleri › 3.2. Veri Normalizasyonu ve Standartlaştırma › 3.2.1. Veri Normalizasyonu › 3.2.1.4. L2 Normalizasyonu (Öklid Normu Tabanlı)
# Kitap  : Kod 3.20 (L1 ve L2 normalizasyonu)
# Dosya : bolum03/03_02_01_04_l2-normalizasyonu.py
# Gerekli: pip install matplotlib numpy pandas scikit-learn
# ==========================================================================
# ─── L1 ve L2 Normalizasyonu ─────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

# Kelime frekans matrisi (belge × kelime)
belgeler = np.array([
    [3, 0, 1, 0, 5, 2],   # Belge 1
    [0, 1, 0, 4, 0, 1],   # Belge 2
    [2, 2, 3, 0, 1, 0],   # Belge 3 (daha uzun)
    [0, 0, 0, 1, 2, 8],   # Belge 4 (kısa, bir kelime baskın)
], dtype=float)

# L1 normalizasyonu
b_l1 = normalize(belgeler, norm="l1")
print("L1 Normalize (her satır toplamı 1):")
print(np.round(b_l1, 4))
print("Satır L1 normları:", np.abs(b_l1).sum(axis=1))

# L2 normalizasyonu
b_l2 = normalize(belgeler, norm="l2")
print("\nL2 Normalize (her satır L2=1):")
print(np.round(b_l2, 4))
print("Satır L2 normları:", np.round(np.sqrt((b_l2**2).sum(axis=1)), 6))

# L2 normalize vektörler: nokta çarpımı = kosinus benzerliği
kosinus_sim = b_l2 @ b_l2.T
print("\nBelge Kosinus Benzerlik Matrisi:")
print(np.round(kosinus_sim, 3))

# Geometrik görselleştirme: 2B birim çember
v = np.array([[3,4],[1,7],[6,2],[5,5]], dtype=float)
v_l2 = normalize(v, norm="l2")
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,5))
renkler = ["#e74c3c","#3498db","#2ecc71","#f39c12"]
for i,(vor,vn) in enumerate(zip(v,v_l2)):
    ax1.quiver(0,0,vor[0],vor[1],angles="xy",scale_units="xy",scale=1,color=renkler[i],label=f"v{i+1}")
    ax2.quiver(0,0,vn[0],vn[1],angles="xy",scale_units="xy",scale=1,color=renkler[i])
theta=np.linspace(0,2*np.pi,100)
ax2.plot(np.cos(theta),np.sin(theta),"k--",alpha=0.3)
ax1.set_xlim(-0.5, v[:,0].max()*1.15); ax1.set_ylim(-0.5, v[:,1].max()*1.15)
ax1.set_aspect("equal"); ax1.grid(alpha=0.3)
ax2.set_xlim(-1.2, 1.2); ax2.set_ylim(-1.2, 1.2); ax2.grid(alpha=0.3)
ax1.set_title("Orijinal Vektörler"); ax1.legend(fontsize=8)
ax2.set_title("L2 Normalize (Birim Çember)"); ax2.set_aspect("equal")
plt.tight_layout(); plt.show()
