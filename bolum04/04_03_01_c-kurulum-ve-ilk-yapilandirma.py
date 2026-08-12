# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.1. Plotly'e Giriş: Mimari ve Ekosistem › C. Kurulum ve İlk Yapılandırma
# Dosya : bolum04/04_03_01_c-kurulum-ve-ilk-yapilandirma.py
# Gerekli: pip install numpy pandas plotly
# ==========================================================================
# ─── Kurulum ─────────────────────────────────────────────────────────────────
# pip install plotly kaleido   # kaleido: statik görüntü export için
# pip install plotly-express    # yüksek seviye API (Plotly 4.0+ ile birleştirildi)

# ─── Import Kuralları ─────────────────────────────────────────────────────────
import plotly.graph_objects as go          # Düşük seviye API (tam kontrol)
import plotly.express as px                # Yüksek seviye API (hızlı prototip)
import plotly.io as pio                    # I/O, renderer, tema yönetimi
from plotly.subplots import make_subplots  # Alt grafik düzeni
import pandas as pd
import numpy as np

print(f"plotly sürümü: {go.__version__ if hasattr(go, '__version__') else 'N/A'}")

# ─── Renderer Yapılandırması ──────────────────────────────────────────────────
# Jupyter: 'notebook', 'jupyterlab', 'colab'
# IDE:     'browser' (varsayılan tarayıcı), 'firefox', 'chrome'
# Statik:  'png', 'svg', 'pdf' (kaleido gerekir)

# Varsayılan renderer ayarla (Jupyter notebook için)
# pio.renderers.default = 'notebook'

# Tüm renderer'ları listele\nprint("\nKullanılabilir renderer'lar:")
for r in pio.renderers:
    print(f"  {r}")

# ─── Tema (Template) Sistemi ──────────────────────────────────────────────────
# Plotly 10+ yerleşik tema sunar: plotly, plotly_white, plotly_dark, ggplot2, seaborn, ...
print("\nKullanılabilir temalar:")
for t in pio.templates:
    print(f"  {t}")

# Varsayılan tema ayarla
pio.templates.default = "plotly_white"

# Özel tema oluşturma
custom_theme = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Arial, sans-serif", size=12, color="#333"),
        plot_bgcolor="#F8F9FA",
        paper_bgcolor="white",
        title=dict(font=dict(size=16, color="#1E3A5F")),
        xaxis=dict(gridcolor="#E0E0E0", showline=True, linecolor="#CCC"),
        yaxis=dict(gridcolor="#E0E0E0", showline=True, linecolor="#CCC"),
    )
)
pio.templates["custom"] = custom_theme
# pio.templates.default = "custom"

print("\nPlotly yapılandırması tamamlandı.")
