# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.7. 3D Grafikler: Yüzey, Kontur ve Scatter
# Dosya : bolum04/04_01_07_d-grafikler-yuzey-kontur-ve-scatter.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# ─── A. 3D Yüzey: sinc(r) = sin(πr)/(πr) ────────────────────────────────────
fig = plt.figure(figsize=(16, 5))

x = np.linspace(-6, 6, 120); y = np.linspace(-6, 6, 120)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2); Z = np.sinc(R)

ax1 = fig.add_subplot(1, 3, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.9, rstride=2, cstride=2)
fig.colorbar(surf, ax=ax1, shrink=0.5)
ax1.set_title('3D Yüzey: sinc(r)', fontweight='bold')
ax1.view_init(elev=30, azim=-60)

ax2 = fig.add_subplot(1, 3, 2)
cf = ax2.contourf(X, Y, Z, levels=20, cmap='coolwarm')
ct = ax2.contour(X, Y, Z, levels=10, colors='white', linewidths=0.5, alpha=0.6)
ax2.clabel(ct, fmt='%.1f', fontsize=7)
fig.colorbar(cf, ax=ax2, shrink=0.9)
ax2.set_title('Kontur + Renk Dolgusu', fontweight='bold')
ax2.set_aspect('equal')

ax3 = fig.add_subplot(1, 3, 3, projection='3d')
np.random.seed(42); n = 300
xs = np.random.randn(n); ys = np.random.randn(n)
zs = xs*ys + np.random.randn(n)*0.5
sc = ax3.scatter(xs, ys, zs, c=np.sqrt(xs**2+ys**2+zs**2), cmap='viridis', alpha=0.6, s=15)
ax3.scatter(xs, ys, zs.min()-0.5, c='lightgray', alpha=0.2, s=5)
fig.colorbar(sc, ax=ax3, shrink=0.6)
ax3.set_title('3D Scatter + Yansıma', fontweight='bold')
ax3.view_init(elev=25, azim=45)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "3d.png"), dpi=120, bbox_inches='tight'); plt.close()

# ─── B. Rosenbrock: Makine Öğrenmesinde Kayıp Yüzeyi ────────────────────────
# f(x,y) = (1-x)² + 100(y-x²)²  — global min: (1,1), değer=0
fig = plt.figure(figsize=(12, 5))
xr = np.linspace(-2, 2, 150); yr = np.linspace(-1, 3, 150)
Xr, Yr = np.meshgrid(xr, yr)
Zr = (1-Xr)**2 + 100*(Yr-Xr**2)**2
Zl = np.log1p(Zr)

ax3d = fig.add_subplot(1, 2, 1, projection='3d')
ax3d.plot_surface(Xr, Yr, Zl, cmap='hot', alpha=0.8, rstride=3, cstride=3)
ax3d.scatter([1],[1],[0], color='lime', s=100, zorder=5, label='Min (1,1)')
ax3d.set_title('Rosenbrock: log(1+f(x,y))\nKayıp Fonksiyonu', fontweight='bold', fontsize=10)
ax3d.view_init(elev=40, azim=-50)

ax2d = fig.add_subplot(1, 2, 2)
cnt = ax2d.contourf(Xr, Yr, Zl, levels=30, cmap='hot')
ax2d.scatter([1],[1], color='lime', s=150, zorder=5, marker='*', label='Min: (1,1)')
ax2d.set_title('Kontur Görünümü', fontweight='bold')
ax2d.legend()
fig.colorbar(cnt, ax=ax2d)

plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "kayip_fct.png"), dpi=120, bbox_inches='tight'); plt.close()
print("3D grafikler tamamlandı.")
