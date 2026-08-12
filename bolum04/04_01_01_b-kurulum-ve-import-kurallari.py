# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.1. Matplotlib'e Giriş: Tarihsel Arka Plan ve Mimari › B. Kurulum ve Import Kuralları
# Dosya : bolum04/04_01_01_b-kurulum-ve-import-kurallari.py
# Gerekli: pip install matplotlib numpy pandas
# ==========================================================================
# --- ▌ Kod Örneği 4.1.1 — Kurulum, Import ve Temel Yapılandırma ---
# Kurulum
# pip install matplotlib
# conda install -c conda-forge matplotlib  (McKinney önerisi)

# --- ▌ Kod Örneği 4.1.1 — Kurulum, Import ve Temel Yapılandırma ---
import matplotlib
import matplotlib.pyplot as plt   # pyplot: MATLAB benzeri state-machine API
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

# --- ▌ Kod Örneği 4.1.1 — Kurulum, Import ve Temel Yapılandırma ---
print(f"matplotlib sürümü: {matplotlib.__version__}")

# --- ▌ Kod Örneği 4.1.1 — Kurulum, Import ve Temel Yapılandırma ---
# Backend yapılandırması (script modunda)
matplotlib.use('Agg')    # GUI penceresi açmadan PNG/SVG üret

# --- ▌ Kod Örneği 4.1.1 — Kurulum, Import ve Temel Yapılandırma ---
# Kullanılabilir stiller
print("Kullanılabilir stiller (ilk 5):")
for stil in sorted(plt.style.available)[:5]:
    print(f"  {stil}")

# --- ▌ Kod Örneği 4.1.1 — Kurulum, Import ve Temel Yapılandırma ---
plt.style.use('seaborn-v0_8-whitegrid')

# --- ▌ Kod Örneği 4.1.1 — Kurulum, Import ve Temel Yapılandırma ---
# rcParams ile global yapılandırma
plt.rcParams.update({
    'font.family'     : 'DejaVu Sans',
    'font.size'       : 12,
    'axes.titlesize'  : 14,
    'axes.labelsize'  : 12,
    'figure.dpi'      : 100,
    'savefig.dpi'     : 150,
    'figure.figsize'  : (10, 6),
    'lines.linewidth' : 1.8,
    'axes.grid'       : True,
    'grid.alpha'      : 0.4,
})
