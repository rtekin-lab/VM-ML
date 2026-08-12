# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.10. Grafikleri Kaydetme ve Yayımlama Kalitesi
# Kitap  : Kod 4.2 (Şekilleri yayım kalitesinde kaydetme)
# Dosya : bolum04/04_01_10_grafikleri-kaydetme-ve-yayimlama-kalitesi.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import tempfile

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

def yayin_grafigi(kayit_yolu_temel):
    """Akademik yayın kalitesinde grafik üretir ve çoklu formatta kaydeder."""

    # Akademik stil
    plt.rcParams.update({
        'font.family'       : 'serif',
        'font.size'         : 11,
        'axes.titlesize'    : 12,
        'axes.labelsize'    : 11,
        'figure.figsize'    : (7, 5),      # 2 sütunlu dergi ~88mm
        'axes.spines.top'   : False,
        'axes.spines.right' : False,
        'lines.linewidth'   : 1.5,
        'axes.grid'         : True,
        'grid.alpha'        : 0.3,
        'grid.linestyle'    : ':',
    })

    fig, ax = plt.subplots()
    x = np.linspace(0, 2*np.pi, 200)
    ax.plot(x, np.sin(x),       label='sin(x)',     color='#1E3A5F', lw=1.8)
    ax.plot(x, np.cos(x),       label='cos(x)',     color='#C44D34', lw=1.8, ls='--')
    ax.plot(x, np.sin(2*x)*0.7, label='0.7sin(2x)', color='#2E8B57', lw=1.5, ls=':')

    ax.set_xlabel('x (radyan)', labelpad=8)
    ax.set_ylabel('f(x)', labelpad=8)
    ax.set_title('Trigonometrik Fonksiyonlar', pad=12)
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_xlim(0, 2*np.pi)

    # Birden fazla formatta kaydet
    for fmt, params in {
        'png': {'dpi':300, 'bbox_inches':'tight', 'facecolor':'white'},
        'svg': {'bbox_inches':'tight', 'facecolor':'white'},
        'pdf': {'bbox_inches':'tight', 'facecolor':'white'},
    }.items():
        yol = f"{kayit_yolu_temel}.{fmt}"
        fig.savefig(yol, format=fmt, **params)
        if os.path.exists(yol):
            print(f"  {fmt.upper():<5} → {yol} ({os.path.getsize(yol)/1024:.1f} KB)")

    plt.close(fig)
    matplotlib.rcdefaults()

print("Yayın kalitesinde grafik üretiliyor...")
yayin_grafigi(os.path.join(tempfile.gettempdir(), "yayin_grafigi"))

# Format özet tablosu
print("\n─── Format ve DPI Rehberi ─────────────────────────────────────")
rehber = [
    ('PNG 72 DPI',  'Hızlı taslak, ekran görüntüsü'),
    ('PNG 150 DPI', 'Web yayını, sunum'),
    ('PNG 300 DPI', 'Baskı kalitesi, dergi'),
    ('SVG',         'Vektör, web/interaktif uygulama'),
    ('PDF',         'LaTeX entegrasyonu, akademik yayın'),
    ('EPS',         'Eski journal/LaTeX sistemleri'),
    ('TIFF 600 DPI','Yüksek kaliteli ofset baskı'),
]
for fmt, kullanim in rehber:
    print(f"  {fmt:<15} : {kullanim}")
