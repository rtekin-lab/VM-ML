# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.2. Gerekli Python Kütüphanelerinin Kurulumu › 1.2.9. IPython ve Jupyter — Etkileşimli Geliştirme Ortamı
# Kitap  : Kod 1.59 (IPython sihirli komutları (Magic Commands))
# Dosya : bolum01/01_02_09_ipython-ve-jupyter-etkilesimli-gelistirme-ortami-2.py
# ==========================================================================
# Yararlı Jupyter Magic komutları
# %timeit  — tek satır için çalışma süresi ölçümü
# %%timeit — hücre için çalışma süresi
# %matplotlib inline  — grafikleri notebook'a göm
# %autoreload 2       — modülleri otomatik yeniden yükle
# !pip install paket  — terminal komutu
# %run script.py      — script çalıştır
# %debug              — hata ayıklama

# IPython sihirli komutları (Magic Commands)
import IPython
print(IPython.__version__)

# Örnek profilleme
# %timeit [x**2 for x in range(1000)]
# Örnek: 36.4 µs ± 0.8 µs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
