# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: Veri Akışı İşleme ve Gerçek Zamanlı Analitik › Bölüm şekilleri
# Dosya : bolum13/13_00_bolum-sekilleri.py
# Gerekli: pip install numpy matplotlib
# ==========================================================================
"""Bölüm 13'ün kavramsal ve uygulamalı şekillerini üretir."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

LACI, MAVI, ACIK, GRI = '#1F3864', '#2E5A8A', '#DCE6F1', '#7A7A7A'
YESIL, KIRMIZI, TURUNCU = '#27AE60', '#C0392B', '#E67E22'
plt.rcParams['font.size'] = 9


def kutu(ax, x, y, w, h, metin, renk=ACIK, kenar=LACI, fs=8.5, kalin=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05',
                                facecolor=renk, edgecolor=kenar, linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, metin, ha='center', va='center',
            fontsize=fs, fontweight='bold' if kalin else 'normal')


# --- Şekil 1: Yığın ve akış işleme -------------------------------------
def yigin_akis():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 5.2))
    # yığın
    for i in range(4):
        a1.add_patch(Rectangle((0.5 + i * 3.0, 1.4), 2.4, 1.0,
                               facecolor=ACIK, edgecolor=LACI, linewidth=1.2))
        a1.text(1.7 + i * 3.0, 1.9, f'Gün {i+1} verisi\n(biriktirilir)',
                ha='center', va='center', fontsize=8)
        a1.annotate('', xy=(1.7 + i * 3.0, 0.9), xytext=(1.7 + i * 3.0, 1.35),
                    arrowprops=dict(arrowstyle='-|>', color=GRI, linewidth=1.1))
        a1.text(1.7 + i * 3.0, 0.55, 'gece 02:00 işlenir', ha='center',
                fontsize=7.5, color=GRI)
    a1.set_title('Yığın işleme: veri önce birikir, sonra toplu işlenir', fontsize=10)
    a1.text(0.5, 2.7, 'Gecikme: saatler. Veri sınırlı ve baştan bilinir.',
            fontsize=8, color=GRI)
    a1.set_xlim(0, 12.4); a1.set_ylim(0.2, 3.1); a1.axis('off')

    # akış
    t = np.linspace(0, 12, 400)
    a2.plot(t, 1.6 + 0.35 * np.sin(t * 2.2), color=MAVI, linewidth=1.6)
    rng = np.random.default_rng(2)
    olay_t = np.sort(rng.uniform(0.3, 11.7, 26))
    a2.scatter(olay_t, 1.6 + 0.35 * np.sin(olay_t * 2.2), s=22,
               color=LACI, zorder=3)
    for x in (3.0, 6.0, 9.0):
        a2.axvline(x, color=GRI, linestyle=':', linewidth=0.9)
        a2.text(x, 0.55, 'anlık sonuç', ha='center', fontsize=7.5, color=YESIL)
    a2.set_title('Akış işleme: her olay geldiği anda işlenir', fontsize=10)
    a2.text(0.2, 2.55, 'Gecikme: milisaniyeler. Veri sınırsız, sonu bilinmez.',
            fontsize=8, color=GRI)
    a2.set_xlim(0, 12.4); a2.set_ylim(0.3, 2.9); a2.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 2: Zaman pencereleri ----------------------------------------
def pencereler():
    fig, axes = plt.subplots(3, 1, figsize=(12, 6))
    rng = np.random.default_rng(5)
    olaylar = np.sort(rng.uniform(0.2, 11.8, 24))

    def olay_ciz(ax):
        ax.scatter(olaylar, np.full_like(olaylar, 0.35), s=26, color=LACI, zorder=4)
        ax.plot([0, 12], [0.35, 0.35], color=GRI, linewidth=0.8, zorder=1)

    # atlamalı
    ax = axes[0]
    for i, s in enumerate(range(0, 12, 3)):
        ax.add_patch(Rectangle((s, 0.6), 3, 0.75, facecolor=ACIK,
                               edgecolor=LACI, alpha=0.85))
        ax.text(s + 1.5, 0.98, f'P{i+1}', ha='center', va='center', fontsize=8.5)
    olay_ciz(ax)
    ax.set_title('Atlamalı (tumbling): pencereler bitişik, çakışma yok', fontsize=9.5)

    # kayan
    ax = axes[1]
    for i, s in enumerate(np.arange(0, 10.5, 1.5)):
        ax.add_patch(Rectangle((s, 0.6 + (i % 3) * 0.28), 3, 0.26,
                               facecolor=['#D6E4F5', '#C9DAEE', '#B8CDE8'][i % 3],
                               edgecolor=LACI, alpha=0.9))
    olay_ciz(ax)
    ax.set_title('Kayan (sliding): pencere boyu 3 br, kayma 1,5 br — olaylar birden çok pencerede',
                 fontsize=9.5)

    # oturum
    ax = axes[2]
    gruplar = [(0.2, 2.3), (3.9, 6.4), (8.1, 11.8)]
    for i, (a, b) in enumerate(gruplar):
        ax.add_patch(Rectangle((a - 0.15, 0.6), b - a + 0.3, 0.75,
                               facecolor='#DFF0D8', edgecolor=YESIL, alpha=0.85))
        ax.text((a + b) / 2, 0.98, f'Oturum {i+1}', ha='center', va='center', fontsize=8.5)
    for x in (3.1, 7.2):
        ax.annotate('boşluk > 1 br', xy=(x, 0.45), fontsize=7.5, color=KIRMIZI,
                    ha='center')
    olay_ciz(ax)
    ax.set_title('Oturum (session): etkinlik boşluğuna göre pencere kapanır', fontsize=9.5)

    for ax in axes:
        ax.set_xlim(-0.3, 12.3); ax.set_ylim(0.1, 1.55); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 3: Watermark ve geç gelen olaylar ---------------------------
def watermark():
    fig, ax = plt.subplots(figsize=(11.5, 4.4))
    rng = np.random.default_rng(11)
    olay_zamani = np.sort(rng.uniform(0, 10, 22))
    gecikme = rng.exponential(0.6, 22)
    islem_zamani = olay_zamani + gecikme
    ax.scatter(islem_zamani, olay_zamani, s=30, color=LACI, zorder=3, label='olay')
    ax.plot([0, 11], [0, 11], color=GRI, linestyle='--', linewidth=1,
            label='ideal (gecikmesiz)')
    ax.plot([0, 11], [-2, 9], color=KIRMIZI, linewidth=1.8,
            label='watermark (2 br tolerans)')
    gec = olay_zamani < islem_zamani - 2
    ax.scatter(islem_zamani[gec], olay_zamani[gec], s=90, facecolor='none',
               edgecolor=KIRMIZI, linewidth=1.6, zorder=4)
    for x, y in zip(islem_zamani[gec], olay_zamani[gec]):
        ax.annotate('geç kaldı', (x, y), textcoords='offset points',
                    xytext=(8, -4), fontsize=7.5, color=KIRMIZI)
    ax.set_xlabel('İşleme zamanı'); ax.set_ylabel('Olay zamanı')
    ax.set_title('Watermark: geç gelen olaylar için tolerans sınırı')
    ax.legend(fontsize=8, loc='upper left'); ax.grid(alpha=0.3)
    ax.set_xlim(0, 11); ax.set_ylim(-0.5, 11)
    plt.tight_layout(); plt.show()


# --- Şekil 4: Kafka mimarisi -------------------------------------------
def kafka():
    fig, ax = plt.subplots(figsize=(12.5, 5)) 
    for i in range(2):
        kutu(ax, 0.3, 3.3 - i * 1.2, 2.0, 0.85, f'Üretici {i+1}', ACIK, LACI)
    ax.add_patch(Rectangle((3.2, 0.5), 5.2, 4.2, facecolor='#FAFAFA',
                           edgecolor=GRI, linewidth=1.2))
    ax.text(5.8, 4.45, "Konu: 'tweets'", ha='center', fontsize=9.5,
            fontweight='bold', color=LACI)
    for b in range(3):
        y = 3.3 - b * 1.25
        ax.text(3.45, y + 0.42, f'Bölüm {b}', fontsize=8, color=LACI)
        for o in range(6):
            renk = '#D6E4F5' if o < 4 else '#FFFFFF'
            ax.add_patch(Rectangle((4.35 + o * 0.62, y), 0.58, 0.55,
                                   facecolor=renk, edgecolor=GRI, linewidth=0.9))
            if o < 4:
                ax.text(4.64 + o * 0.62, y + 0.27, str(o), ha='center',
                        va='center', fontsize=7)
        ax.annotate('', xy=(8.15, y + 0.27), xytext=(4.3, y + 0.27),
                    arrowprops=dict(arrowstyle='-|>', color=GRI, linewidth=0.8))
    ax.text(5.8, 0.15, 'Sıra garantisi bölüm içindedir, konu genelinde değil.',
            ha='center', fontsize=8, color=KIRMIZI)
    ax.add_patch(Rectangle((9.0, 0.9), 3.1, 3.4, facecolor='#F4FAF3',
                           edgecolor=YESIL, linewidth=1.2))
    ax.text(10.55, 4.0, 'Tüketici grubu', ha='center', fontsize=9, fontweight='bold',
            color=YESIL)
    for i in range(3):
        kutu(ax, 9.25, 2.9 - i * 0.9, 2.6, 0.7, f'Tüketici {i+1} → Bölüm {i}',
             '#DFF0D8', YESIL, fs=7.5)
    for i in range(2):
        ax.annotate('', xy=(3.15, 3.7 - i * 1.2), xytext=(2.35, 3.7 - i * 1.2),
                    arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.3))
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 4.9); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 5: Konsept kayması ve ADWIN ---------------------------------
def konsept_kaymasi():
    rng = np.random.default_rng(3)
    n = 600
    dogruluk = np.concatenate([
        rng.normal(0.92, 0.02, 200),                 # kararlı
        np.linspace(0.92, 0.62, 100) + rng.normal(0, 0.02, 100),   # kademeli kayma
        rng.normal(0.62, 0.02, 80),
        rng.normal(0.88, 0.02, 220),                 # uyarlanma sonrası
    ])
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.5, 5.4), sharex=True)
    a1.plot(dogruluk, color=MAVI, linewidth=1.1)
    a1.axvspan(200, 300, color='#FDEEEA', alpha=0.8)
    a1.axvline(305, color=KIRMIZI, linestyle='--', linewidth=1.4)
    a1.text(207, 0.965, 'konsept kayması', fontsize=8.5, color=KIRMIZI)
    a1.text(312, 0.70, 'ADWIN kaymayı bildirir\n→ model sıfırlanır',
            fontsize=8, color=KIRMIZI)
    a1.set_ylabel('Çevrim içi doğruluk'); a1.set_ylim(0.5, 1.0)
    a1.set_title('Konsept kayması: veri dağılımı değişince model başarımı düşer')
    a1.grid(alpha=0.3)

    pencere = np.array([min(i + 1, 120) if i < 305 else min(i - 305 + 1, 120)
                        for i in range(n)])
    a2.plot(pencere, color=TURUNCU, linewidth=1.4)
    a2.axvline(305, color=KIRMIZI, linestyle='--', linewidth=1.4)
    a2.set_xlabel('Örnek numarası'); a2.set_ylabel('ADWIN pencere boyu')
    a2.set_title('Uyarlanabilir pencere: kayma algılandığında eski veri atılır')
    a2.grid(alpha=0.3)
    plt.tight_layout(); plt.show()


# --- Şekil 6: Uçtan uca mimari -----------------------------------------
def uctan_uca():
    fig, ax = plt.subplots(figsize=(13, 3.8))
    asama = [('Kaynak', 'Twitter API /\nsimülatör', ACIK),
             ('Taşıma', "Kafka\nkonu: 'tweets'", '#DCE6F1'),
             ('İşleme', 'Flink\npencere + NLP', '#DFF0D8'),
             ('Model', 'VADER +\nDistilBERT', '#FDEEEA'),
             ('Depolama', 'Kafka çıktı /\nveritabanı', '#DCE6F1'),
             ('Sunum', 'Gerçek zamanlı\npano', '#F9E7C4')]
    w, bosluk = 1.85, 0.42
    for i, (ust, alt, renk) in enumerate(asama):
        x = 0.25 + i * (w + bosluk)
        ax.text(x + w / 2, 2.75, ust, ha='center', fontsize=9,
                fontweight='bold', color=LACI)
        kutu(ax, x, 1.2, w, 1.35, alt, renk, LACI, fs=8)
        if i < len(asama) - 1:
            ax.annotate('', xy=(x + w + bosluk - 0.04, 1.88), xytext=(x + w + 0.04, 1.88),
                        arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.5))
    ax.text(0.25, 0.75, 'Uçtan uca gecikme hedefi: 2 saniyenin altı. '
                        'Her aşama bağımsız ölçeklenebilir.',
            fontsize=8, color=GRI)
    ax.set_xlim(0, 0.25 + 6 * (w + bosluk)); ax.set_ylim(0.4, 3.1); ax.axis('off')
    plt.tight_layout(); plt.show()


if __name__ == '__main__':
    yigin_akis()
    pencereler()
    watermark()
    kafka()
    konsept_kaymasi()
    uctan_uca()
