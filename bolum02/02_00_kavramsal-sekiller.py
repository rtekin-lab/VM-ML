# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: Veri Madenciliğine Giriş ve Matematiksel Temeller › Kavramsal şekiller
# Dosya : bolum02/02_00_kavramsal-sekiller.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================
"""Bölümün kavramsal şekillerini üretir: KDD süreci, kapsam ilişkisi, veri kaynakları."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

LACI, MAVI, ACIK, GRI = '#1F3864', '#2E5A8A', '#DCE6F1', '#7A7A7A'
plt.rcParams['font.size'] = 9


# --- Şekil 1: KDD süreç modeli -------------------------------------------
def kdd_sureci():
    adimlar = [
        ('Veri Seçimi', 'Hedef veri kümesinin\nbelirlenmesi'),
        ('Ön İşleme', 'Temizleme, eksik ve\naykırı değerler'),
        ('Dönüştürme', 'Ölçekleme, öznitelik\nüretimi, indirgeme'),
        ('Veri Madenciliği', 'Örüntü çıkarımı:\nmodel ve algoritma'),
        ('Yorumlama', 'Değerlendirme ve\nbilgiye dönüştürme'),
    ]
    fig, ax = plt.subplots(figsize=(11, 3.4))
    x, w, h = 0.3, 1.9, 1.5
    for i, (bas, alt) in enumerate(adimlar):
        kx = x + i * (w + 0.45)
        ax.add_patch(FancyBboxPatch((kx, 0.9), w, h, boxstyle='round,pad=0.06',
                                    facecolor=ACIK, edgecolor=LACI, linewidth=1.4))
        ax.text(kx + w / 2, 1.95, bas, ha='center', va='center',
                fontsize=10, fontweight='bold', color=LACI)
        ax.text(kx + w / 2, 1.35, alt, ha='center', va='center',
                fontsize=8, color='#333333')
        if i < len(adimlar) - 1:
            ax.add_patch(FancyArrowPatch((kx + w + 0.05, 1.65), (kx + w + 0.40, 1.65),
                                         arrowstyle='-|>', mutation_scale=14,
                                         color=MAVI, linewidth=1.6))
    ax.annotate('', xy=(x, 0.55), xytext=(x + 4 * (w + 0.45) + w, 0.55),
                arrowprops=dict(arrowstyle='<|-', color=GRI, linestyle='--', linewidth=1.2))
    ax.text(x + (4 * (w + 0.45) + w) / 2, 0.32, 'geri besleme: adımlar yinelemeli olarak tekrarlanır',
            ha='center', fontsize=8, color=GRI, style='italic')
    ax.text(x, 2.75, 'Ham veri', fontsize=9, color=GRI)
    ax.text(x + 4 * (w + 0.45) + w, 2.75, 'Eyleme dönüştürülebilir bilgi',
            fontsize=9, color=GRI, ha='right')
    ax.set_xlim(0, x + 5 * (w + 0.45)); ax.set_ylim(0, 3.1); ax.axis('off')
    plt.tight_layout()
    plt.show()


# --- Şekil 2: Kapsam ilişkisi --------------------------------------------
def kapsam_iliskisi():
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    katmanlar = [
        (2.6, 'Veri Bilimi', '#E8EEF7', 'İstatistik + bilgisayar bilimi +\nalan bilgisi + iletişim'),
        (1.9, 'Veri Madenciliği', '#C9DAEE', 'Büyük veri kümelerinden\nörüntü çıkarımı'),
        (1.15, 'Makine Öğrenmesi', '#9FC0E0', 'Veriden öğrenen\nalgoritmalar'),
        (0.55, 'Derin\nÖğrenme', '#6D9BD1', ''),
    ]
    for r, ad, renk, alt in katmanlar:
        ax.add_patch(Circle((0, 0), r, facecolor=renk, edgecolor=LACI, linewidth=1.2))
    ax.text(0, 2.25, 'Veri Bilimi', ha='center', fontsize=11, fontweight='bold', color=LACI)
    ax.text(0, 1.62, 'Veri Madenciliği', ha='center', fontsize=10, fontweight='bold', color=LACI)
    ax.text(0, 0.92, 'Makine Öğrenmesi', ha='center', fontsize=9.5, fontweight='bold', color=LACI)
    ax.text(0, 0.05, 'Derin\nÖğrenme', ha='center', va='center', fontsize=8.5,
            fontweight='bold', color='white')
    ax.text(2.85, 2.35, 'İstatistik, bilgisayar bilimi,\nalan bilgisi ve iletişimin kesişimi',
            fontsize=8, color='#333333', va='center')
    ax.text(2.85, 1.55, 'Büyük veri kümelerinden\nörüntü çıkarımı', fontsize=8,
            color='#333333', va='center')
    ax.text(2.85, 0.85, 'Veriden öğrenen algoritmalar', fontsize=8, color='#333333', va='center')
    for y, r in ((2.35, 2.6), (1.55, 1.9), (0.85, 1.15)):
        ax.plot([np.sqrt(max(r**2 - y**2, 0.01)), 2.75], [y, y], color=GRI, linewidth=0.8)
    ax.set_xlim(-3, 6.6); ax.set_ylim(-3, 3.1); ax.set_aspect('equal'); ax.axis('off')
    plt.tight_layout()
    plt.show()


# --- Şekil 3: Veri kaynakları taksonomisi --------------------------------
def veri_kaynaklari():
    gruplar = {
        'Yapılandırılmış': ['İlişkisel veritabanı', 'Veri ambarı / OLAP', 'İşlemsel kayıtlar'],
        'Yarı Yapılandırılmış': ['JSON / XML', 'REST API yanıtları', 'Günlük (log) dosyaları'],
        'Yapılandırılmamış': ['Metin ve belgeler', 'Görüntü ve video', 'Sosyal medya akışı'],
        'Akan / Zaman Serisi': ['IoT sensörleri', 'Finansal tik verisi', 'Tıklama akışı'],
    }
    fig, ax = plt.subplots(figsize=(11, 4.4))
    gw = 2.5
    for i, (ust, altlar) in enumerate(gruplar.items()):
        gx = 0.25 + i * (gw + 0.3)
        ax.add_patch(FancyBboxPatch((gx, 3.15), gw, 0.75, boxstyle='round,pad=0.05',
                                    facecolor=LACI, edgecolor=LACI))
        ax.text(gx + gw / 2, 3.52, ust, ha='center', va='center', fontsize=9.5,
                fontweight='bold', color='white')
        for j, alt in enumerate(altlar):
            ay = 2.35 - j * 0.72
            ax.add_patch(FancyBboxPatch((gx + 0.12, ay), gw - 0.24, 0.56,
                                        boxstyle='round,pad=0.04',
                                        facecolor=ACIK, edgecolor=MAVI, linewidth=0.9))
            ax.text(gx + gw / 2, ay + 0.28, alt, ha='center', va='center', fontsize=8.2)
            ax.plot([gx + gw / 2, gx + gw / 2], [ay + 0.56, ay + 0.72 if j else 3.15],
                    color=MAVI, linewidth=0.8)
    ax.set_xlim(0, 0.25 + 4 * (gw + 0.3)); ax.set_ylim(0, 4.05); ax.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    kdd_sureci()
    kapsam_iliskisi()
    veri_kaynaklari()
