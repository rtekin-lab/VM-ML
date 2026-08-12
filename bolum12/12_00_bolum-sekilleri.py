# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: Büyük Veri Analitiği ve Dağıtık Makine Öğrenmesi › Bölüm şekilleri
# Dosya : bolum12/12_00_bolum-sekilleri.py
# Gerekli: pip install numpy matplotlib
# ==========================================================================
"""Bölüm 12'nin kavramsal şekillerini üretir."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

LACI, MAVI, ACIK, GRI = '#1F3864', '#2E5A8A', '#DCE6F1', '#7A7A7A'
YESIL, KIRMIZI, TURUNCU = '#27AE60', '#C0392B', '#E67E22'
plt.rcParams['font.size'] = 9


def kutu(ax, x, y, w, h, metin, renk=ACIK, kenar=LACI, fs=8.5, kalin=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05',
                                facecolor=renk, edgecolor=kenar, linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, metin, ha='center', va='center',
            fontsize=fs, fontweight='bold' if kalin else 'normal')


# --- Şekil 1: Dikey ve yatay ölçekleme ----------------------------------
def olcekleme():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.2))
    # dikey
    for i, (h, ad) in enumerate([(0.9, '4 çekirdek\n16 GB'), (1.5, '16 çekirdek\n128 GB'),
                                 (2.4, '64 çekirdek\n1 TB')]):
        kutu(a1, 0.6 + i * 2.6, 0.6, 2.0, h, ad, ACIK if i < 2 else '#C9DAEE')
        a1.text(1.6 + i * 2.6, 0.35, f'{(i+1)*8}× maliyet', ha='center',
                fontsize=7.5, color=GRI)
    a1.annotate('', xy=(7.6, 3.3), xytext=(0.7, 3.3),
                arrowprops=dict(arrowstyle='-|>', color=KIRMIZI, linewidth=1.6))
    a1.text(4.1, 3.5, 'donanım sınırına kadar', ha='center', fontsize=8, color=KIRMIZI)
    a1.set_title('Dikey ölçekleme: tek makineyi güçlendir')
    a1.text(0.6, 0.02, 'Tek hata noktası. Maliyet doğrusaldan hızlı artar.',
            fontsize=7.5, color=GRI)
    a1.set_xlim(0, 9); a1.set_ylim(-0.2, 4); a1.axis('off')

    # yatay
    for i in range(8):
        x, y = 0.6 + (i % 4) * 2.0, 2.1 - (i // 4) * 1.15
        kutu(a2, x, y, 1.7, 0.85, '4 çekirdek\n16 GB', ACIK, LACI, fs=7)
    a2.annotate('', xy=(8.4, 3.4), xytext=(0.7, 3.4),
                arrowprops=dict(arrowstyle='-|>', color=YESIL, linewidth=1.6))
    a2.text(4.5, 3.6, 'düğüm ekleyerek sınırsız', ha='center', fontsize=8, color=YESIL)
    a2.set_title('Yatay ölçekleme: sıradan makineleri çoğalt')
    a2.text(0.6, 0.3, 'Bir düğüm düşerse iş sürer. Yazılım karmaşıklığı artar.',
            fontsize=7.5, color=GRI)
    a2.set_xlim(0, 9); a2.set_ylim(0, 4); a2.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 2: HDFS blok yerleşimi ---------------------------------------
def hdfs():
    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    kutu(ax, 0.3, 3.5, 2.6, 0.9, 'NameNode\n(üstveri: blok → düğüm)', '#EFEFEF', LACI, kalin=True)
    ax.text(0.3, 3.2, '512 MB dosya → 128 MB\'lık 4 blok', fontsize=8, color=GRI)
    renkler = ['#D6E4F5', '#F5DDD6', '#DFF0D8', '#F9E7C4']
    yerlesim = [[0, 1, 2], [1, 2, 3], [0, 2, 3], [0, 1, 3]]   # her blok 3 düğümde
    for dn in range(4):
        dx = 0.3 + dn * 2.9
        ax.add_patch(Rectangle((dx, 0.35), 2.5, 2.3, facecolor='#FAFAFA',
                               edgecolor=GRI, linewidth=1.1))
        ax.text(dx + 1.25, 2.42, f'DataNode {dn + 1}', ha='center',
                fontsize=8.5, fontweight='bold', color=LACI)
        sira = 0
        for blok, dugumler in enumerate(yerlesim):
            if dn in dugumler:
                kutu(ax, dx + 0.25, 1.75 - sira * 0.55, 2.0, 0.42,
                     f'Blok {blok + 1}', renkler[blok], GRI, fs=7.5)
                sira += 1
        ax.annotate('', xy=(dx + 1.25, 2.72), xytext=(1.6, 3.45),
                    arrowprops=dict(arrowstyle='->', color=GRI, linestyle=':', linewidth=0.8))
    ax.text(0.3, 0.05, 'Her blok üç ayrı düğümde tutulur: bir düğüm düşse de veri erişilebilir kalır.',
            fontsize=8, color=GRI)
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.6); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 3: MapReduce akışı -------------------------------------------
def mapreduce():
    fig, ax = plt.subplots(figsize=(13, 4.6))
    asama = [('Girdi\nbölünmesi', 0.3, ['satır 1-100', 'satır 101-200', 'satır 201-300']),
             ('Map', 3.3, ['(kedi,1)\n(köpek,1)', '(kedi,1)\n(kuş,1)', '(köpek,1)\n(kedi,1)']),
             ('Shuffle\n& Sort', 6.3, ['kedi:[1,1,1]', 'köpek:[1,1]', 'kuş:[1]']),
             ('Reduce', 9.3, ['kedi: 3', 'köpek: 2', 'kuş: 1'])]
    for ad, x, kutular in asama:
        ax.text(x + 1.1, 3.75, ad, ha='center', fontsize=9.5,
                fontweight='bold', color=LACI)
        for i, m in enumerate(kutular):
            kutu(ax, x, 2.6 - i * 1.0, 2.2, 0.8, m,
                 ACIK if ad != 'Reduce' else '#DFF0D8', LACI, fs=7.5)
    for x in (2.6, 5.6, 8.6):
        for i in range(3):
            ax.annotate('', xy=(x + 0.65, 3.0 - i * 1.0), xytext=(x, 3.0 - i * 1.0),
                        arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.2))
    ax.text(6.3, 0.15, 'Shuffle aşaması ağ üzerinden veri taşır; MapReduce\'un en pahalı adımıdır.',
            ha='center', fontsize=8, color=KIRMIZI)
    ax.set_xlim(0, 11.8); ax.set_ylim(0, 4.2); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 4: Spark mimarisi ve DAG -------------------------------------
def spark_mimari():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.4),
                                 gridspec_kw={'width_ratios': [1, 1.15]})
    kutu(a1, 2.2, 3.3, 3.2, 1.0, 'Driver Program\n(SparkContext)', '#EFEFEF', LACI, kalin=True)
    kutu(a1, 2.2, 1.9, 3.2, 0.85, 'Cluster Manager\n(YARN / Mesos / K8s)', ACIK, LACI)
    for i in range(3):
        kutu(a1, 0.4 + i * 2.5, 0.4, 2.1, 0.9, f'Executor {i+1}\nRAM + görevler',
             '#DFF0D8', YESIL, fs=7.5)
        a1.annotate('', xy=(1.45 + i * 2.5, 1.35), xytext=(3.8, 1.85),
                    arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.1))
    a1.annotate('', xy=(3.8, 2.8), xytext=(3.8, 3.25),
                arrowprops=dict(arrowstyle='<|-|>', color=MAVI, linewidth=1.3))
    a1.set_title('Spark mimarisinin üç katmanı')
    a1.set_xlim(0, 7.6); a1.set_ylim(0, 4.6); a1.axis('off')

    dugum = {'metin': (0.6, 3.4, 'textFile'), 'filtre': (2.9, 3.4, 'filter'),
             'esle': (5.2, 3.4, 'map'), 'grup': (3.9, 1.9, 'reduceByKey'),
             'topla': (3.9, 0.5, 'collect')}
    for ad, (x, y, etiket) in dugum.items():
        renk = '#F5DDD6' if ad in ('grup',) else ACIK
        kutu(a2, x, y, 1.9, 0.7, etiket, renk, LACI, fs=8)
    for a, b in [('metin', 'filtre'), ('filtre', 'esle')]:
        x1 = dugum[a][0] + 1.9; x2 = dugum[b][0]
        a2.annotate('', xy=(x2, 3.75), xytext=(x1, 3.75),
                    arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.2))
    a2.annotate('', xy=(4.85, 2.6), xytext=(6.15, 3.35),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.2))
    a2.annotate('', xy=(4.85, 1.2), xytext=(4.85, 1.85),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.2))
    a2.text(0.6, 2.5, 'Dar bağımlılık\n(shuffle yok)', fontsize=8, color=YESIL)
    a2.text(6.4, 2.0, 'Geniş bağımlılık\n→ Stage sınırı', fontsize=8, color=KIRMIZI)
    a2.text(0.6, 0.1, 'Dönüşümler tembeldir; DAG ancak bir eylem çağrıldığında çalıştırılır.',
            fontsize=8, color=GRI)
    a2.set_title('DAG: dönüşüm grafiği ve stage sınırı')
    a2.set_xlim(0, 8.4); a2.set_ylim(0, 4.6); a2.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 5: Veri ve model paralelizmi ---------------------------------
def paralelizm():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.2))
    # veri paralelizmi
    for i in range(3):
        kutu(a1, 0.4 + i * 2.6, 2.5, 2.2, 1.2, f'GPU {i+1}\nMODELİN TAM KOPYASI',
             ACIK, LACI, fs=7.5)
        kutu(a1, 0.4 + i * 2.6, 1.0, 2.2, 0.8, f'Veri parçası {i+1}', '#DFF0D8', YESIL, fs=7.5)
        a1.annotate('', xy=(1.5 + i * 2.6, 2.45), xytext=(1.5 + i * 2.6, 1.85),
                    arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.2))
    a1.text(4.2, 4.0, 'Gradyanlar all-reduce ile birleştirilir', ha='center',
            fontsize=8, color=KIRMIZI)
    a1.set_title('Veri paralelizmi: model küçük, veri büyük')
    a1.set_xlim(0, 8.4); a1.set_ylim(0.5, 4.4); a1.axis('off')

    # model paralelizmi
    parcalar = ['Katman 1-10', 'Katman 11-20', 'Katman 21-30']
    for i, ad in enumerate(parcalar):
        kutu(a2, 0.4 + i * 2.6, 2.5, 2.2, 1.2, f'GPU {i+1}\n{ad}', '#F5DDD6', KIRMIZI, fs=7.5)
        if i < 2:
            a2.annotate('', xy=(3.0 + i * 2.6, 3.1), xytext=(2.6 + i * 2.6, 3.1),
                        arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    kutu(a2, 3.0, 1.0, 2.2, 0.8, 'Tüm veri', '#DFF0D8', YESIL, fs=7.5)
    a2.text(4.2, 4.0, 'Model tek GPU belleğine sığmıyorsa', ha='center',
            fontsize=8, color=KIRMIZI)
    a2.set_title('Model paralelizmi: model büyük')
    a2.set_xlim(0, 8.4); a2.set_ylim(0.5, 4.4); a2.axis('off')
    plt.tight_layout(); plt.show()


if __name__ == '__main__':
    olcekleme()
    hdfs()
    mapreduce()
    spark_mimari()
    paralelizm()
