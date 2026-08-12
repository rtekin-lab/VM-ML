# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.1. Python Ortamının Kurulumu › 1.1.6. Kurulum Doğrulama ve Çevreyi Test Etme
# Kitap  : Kod 1.9 (Kapsamlı kurulum doğrulama betiği — tüm kütü)
# Dosya : bolum01/01_01_06_kurulum-dogrulama-ve-cevreyi-test-etme.py
# Gerekli: pip install matplotlib numpy pandas torch
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
# ─── kurulum_test.py ────────────────────────────────────────────
"""
Python veri bilimi ortami kurulum dogrulama betigi.
Tüm testler gecmeli; baskı ciktisi sorunu teşhis etmeye yarar.
"""
import sys
import subprocess

def test_python():
    sürüm = sys.version_info
    assert sürüm >= (3, 9), f"Python >= 3.9 gerekli, mevcut: {sys.version}"
    print(f"[OK] Python {sürüm.major}.{sürüm.minor}.{sürüm.micro}")

def test_kutuphaneler():
    kutuphaneler = {
        "numpy":      "1.23.0",
        "pandas":     "1.5.0",
        "matplotlib": "3.5.0",
        "seaborn":    "0.12.0",
        "sklearn":    "1.1.0",
        "scipy":      "1.9.0",
        "jupyter":    "1.0.0",
    }
    for pkg, min_sürüm in kutuphaneler.items():
        try:
            modül = __import__(pkg if pkg != "sklearn" else "sklearn")
            sürüm = getattr(modül, "__version__", "?")
            print(f"  [OK] {pkg:<12} v{sürüm}")
        except ImportError:
            print(f"  [HATA] {pkg} YUKLU DEGIL — pip install {pkg}")

def test_numpy_islemi():
    import numpy as np
    A = np.random.randn(1000, 1000)
    deger, vektör = np.linalg.eig(A)
    assert len(deger) == 1000
    print(f"  [OK] NumPy lineer cebir (1000x1000 matris ozdegerleri)")

def test_pandas_islemi():
    import pandas as pd
    df = pd.DataFrame({"x": range(10_000), "y": range(10_000)})
    assert df.shape == (10_000, 2)
    print(f"  [OK] pandas DataFrame (10.000 satır)")

def test_matplotlib():
    import matplotlib
    matplotlib.use("Agg")   # baslıksız test
    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots()
    ax.plot(np.sin(np.linspace(0, 2*3.14159, 100)))
    plt.savefig(os.path.join(tempfile.gettempdir(), "test_plot.png"), dpi=72)
    plt.close()
    print("  [OK] matplotlib görsel olusturma")

def test_gpu():
    try:
        import torch
        cuda = torch.cuda.is_available()
        gpu  = torch.cuda.get_device_name(0) if cuda else "Mevcut degil"
        print(f"  [OK] PyTorch {torch.__version__} | CUDA: {cuda} | GPU: {gpu}")
    except ImportError:
        print("  [BILGI] PyTorch yuklu degil (ihtiyari)")

if __name__ == "__main__":
    print("="*55)
    print("  Python Veri Bilimi Ortami — Kurulum Dogrulama")
    print("="*55)
    test_python()
    print("\nKütüphaneler:")
    test_kutuphaneler()
    print("\nIslemsel Testler:")
    test_numpy_islemi()
    test_pandas_islemi()
    test_matplotlib()
    test_gpu()
    print("\nTum testler tamamlandi!")
