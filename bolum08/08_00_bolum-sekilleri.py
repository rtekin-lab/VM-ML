# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 8
# Konum : BÖLÜM 8: Birliktelik Kuralları ve Tavsiye Sistemleri › Bölüm şekilleri
# Dosya : bolum08/08_00_bolum-sekilleri.py
# Gerekli: pip install numpy matplotlib scikit-learn
# ==========================================================================
"""Bölüm 8'in kavramsal ve uygulamalı şekillerini üretir."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

LACI, MAVI, ACIK, GRI = '#1F3864', '#2E5A8A', '#DCE6F1', '#7A7A7A'
KIRMIZI = '#C0392B'
plt.rcParams['font.size'] = 9


# --- Şekil 1: Apriori arama uzayı ve budama ------------------------------
def apriori_kafes():
    """Dört öğeli evrende öğe kümesi kafesi ve anti-monoton budama."""
    ogeler = ['A', 'B', 'C', 'D']
    katmanlar = [[''], ['A', 'B', 'C', 'D'],
                 ['AB', 'AC', 'AD', 'BC', 'BD', 'CD'],
                 ['ABC', 'ABD', 'ACD', 'BCD'], ['ABCD']]
    budanan = {'D', 'AD', 'BD', 'CD', 'ABD', 'ACD', 'BCD', 'ABCD'}
    fig, ax = plt.subplots(figsize=(10, 5.4))
    konum = {}
    for k, katman in enumerate(katmanlar):
        y = len(katmanlar) - 1 - k
        genislik = len(katman)
        for i, ad in enumerate(katman):
            x = (i - (genislik - 1) / 2) * 1.5
            konum[ad] = (x, y)
            seyrek = ad in budanan
            ax.add_patch(Circle((x, y), 0.30,
                                facecolor='#F2D7D5' if seyrek else ACIK,
                                edgecolor=KIRMIZI if seyrek else LACI,
                                linewidth=1.3, linestyle='--' if seyrek else '-'))
            ax.text(x, y, ad if ad else '∅', ha='center', va='center',
                    fontsize=8.5, fontweight='bold',
                    color=KIRMIZI if seyrek else LACI)
    for k in range(len(katmanlar) - 1):
        for alt in katmanlar[k]:
            for ust in katmanlar[k + 1]:
                if all(c in ust for c in alt):
                    x1, y1 = konum[alt]; x2, y2 = konum[ust]
                    seyrek = alt in budanan or ust in budanan
                    ax.plot([x1, x2], [y1 - 0.30, y2 + 0.30],
                            color='#E8B4B0' if seyrek else '#B8C8DC',
                            linewidth=0.8, zorder=0)
    ax.text(-5.6, 3.0, 'Apriori özelliği:\nbir küme seyrekse\ntüm üst kümeleri de\nseyrektir',
            fontsize=8.5, color=KIRMIZI, va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FDF2F1', edgecolor=KIRMIZI))
    ax.text(-5.6, 1.0, 'D seyrek çıktığı için\nD içeren 7 aday\nhiç sayılmaz',
            fontsize=8.5, color=GRI, va='center')
    ax.set_xlim(-6.6, 5.2); ax.set_ylim(-0.7, 4.5); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 2: FP-Tree yapısı --------------------------------------------
def fp_tree():
    """Sıkıştırılmış FP-Tree ve başlık tablosu."""
    fig, ax = plt.subplots(figsize=(10, 5))
    dugumler = {'null': (0, 4, 'null', ''),
                'A': (-1.6, 3, 'A', '4'), 'B2': (1.6, 3, 'B', '2'),
                'B': (-2.6, 2, 'B', '3'), 'C2': (-0.4, 2, 'C', '1'),
                'C3': (1.6, 2, 'C', '2'),
                'C': (-3.4, 1, 'C', '2'), 'D2': (-1.8, 1, 'D', '1')}
    for ad, (x, y, etiket, sayi) in dugumler.items():
        ax.add_patch(FancyBboxPatch((x - 0.42, y - 0.24), 0.84, 0.48,
                                    boxstyle='round,pad=0.04',
                                    facecolor=ACIK if etiket != 'null' else '#EFEFEF',
                                    edgecolor=LACI, linewidth=1.2))
        yazi = f'{etiket}:{sayi}' if sayi else etiket
        ax.text(x, y, yazi, ha='center', va='center', fontsize=9, fontweight='bold', color=LACI)
    kenar = [('null', 'A'), ('null', 'B2'), ('A', 'B'), ('A', 'C2'),
             ('B2', 'C3'), ('B', 'C'), ('B', 'D2')]
    for a, b in kenar:
        x1, y1, *_ = dugumler[a]; x2, y2, *_ = dugumler[b]
        ax.annotate('', xy=(x2, y2 + 0.26), xytext=(x1, y1 - 0.26),
                    arrowprops=dict(arrowstyle='-', color=MAVI, linewidth=1.2))
    # başlık tablosu
    ax.add_patch(Rectangle((2.9, 0.6), 2.1, 2.9, facecolor='white', edgecolor=LACI, linewidth=1.2))
    ax.text(3.95, 3.25, 'Başlık Tablosu', ha='center', fontsize=9,
            fontweight='bold', color=LACI)
    for i, (oge, sayi) in enumerate([('A', 4), ('B', 5), ('C', 5), ('D', 1)]):
        y = 2.8 - i * 0.55
        ax.text(3.25, y, oge, fontsize=9, fontweight='bold')
        ax.text(3.85, y, str(sayi), fontsize=9)
        ax.annotate('', xy=(2.05, y), xytext=(4.4, y),
                    arrowprops=dict(arrowstyle='->', color=GRI,
                                    linestyle=':', linewidth=0.9))
    ax.text(-4.6, 4.1, 'Veritabanı yalnızca iki kez taranır:\n'
                       '1) öğe frekansları  2) ağacın kurulması\n'
                       'Aday küme üretilmez.',
            fontsize=8.5, color=GRI, va='top')
    ax.set_xlim(-5.2, 5.4); ax.set_ylim(0.2, 4.8); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 3: Destek, güven, kaldıraç ------------------------------------
def metrikler():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.4))
    # sol: küme diyagramı
    a1.add_patch(Rectangle((0, 0), 10, 6, facecolor='#F7F7F7', edgecolor=GRI))
    a1.add_patch(Circle((3.8, 3), 2.3, facecolor='#D6E4F5', edgecolor=MAVI, alpha=0.85))
    a1.add_patch(Circle((6.2, 3), 2.3, facecolor='#F5DDD6', edgecolor=KIRMIZI, alpha=0.7))
    a1.text(2.4, 3, 'X\n(ekmek)', ha='center', va='center', fontsize=9, fontweight='bold')
    a1.text(7.6, 3, 'Y\n(süt)', ha='center', va='center', fontsize=9, fontweight='bold')
    a1.text(5.0, 3, 'X ∪ Y', ha='center', va='center', fontsize=9, fontweight='bold')
    a1.text(0.4, 5.4, 'T: tüm işlemler', fontsize=8.5, color=GRI)
    a1.text(5, -0.9, 'destek(X→Y) = |X ∪ Y| / |T|      güven(X→Y) = |X ∪ Y| / |X|',
            ha='center', fontsize=8.5)
    a1.set_xlim(-0.5, 10.5); a1.set_ylim(-1.5, 6.5); a1.axis('off')
    a1.set_title('Destek ve güven')

    # sağ: örnek kuralların destek-güven düzleminde konumu, kaldıraça göre renklendirilmiş
    kurallar = [('ekmek → süt', 0.32, 0.72, 1.44), ('bebek bezi → bira', 0.06, 0.68, 3.10),
                ('çay → şeker', 0.21, 0.65, 1.85), ('makarna → salça', 0.14, 0.59, 2.05),
                ('süt → ekmek', 0.32, 0.55, 1.44), ('yoğurt → su', 0.11, 0.31, 0.62),
                ('deterjan → çikolata', 0.04, 0.19, 0.48), ('peynir → zeytin', 0.09, 0.44, 1.60)]
    d_ = np.array([k[1] for k in kurallar]); g_ = np.array([k[2] for k in kurallar])
    l_ = np.array([k[3] for k in kurallar])
    sc = a2.scatter(d_, g_, c=l_, s=140, cmap='RdYlBu', vmin=0.4, vmax=3.2,
                    edgecolor=LACI, linewidth=0.8, zorder=3)
    for ad, dd, gg, ll in kurallar:
        a2.annotate(f'{ad}\n(kaldıraç {ll:.2f})', (dd, gg), textcoords='offset points',
                    xytext=(7, 6), fontsize=7, color='#333333')
    a2.axhline(0.5, color=GRI, linestyle=':', linewidth=1)
    a2.axvline(0.10, color=GRI, linestyle=':', linewidth=1)
    a2.text(0.105, 0.86, 'minimum destek eşiği', fontsize=7.5, color=GRI, rotation=90, va='top')
    a2.text(0.345, 0.515, 'minimum güven eşiği', fontsize=7.5, color=GRI)
    plt.colorbar(sc, ax=a2, label='kaldıraç')
    a2.set_xlabel('destek'); a2.set_ylabel('güven')
    a2.set_xlim(0, 0.40); a2.set_ylim(0.1, 0.95)
    a2.set_title('Kuralların destek-güven düzleminde konumu'); a2.grid(alpha=0.25)
    plt.tight_layout(); plt.show()


# --- Şekil 4: Tavsiye yaklaşımlarının şeması -----------------------------
def tavsiye_semasi():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.6))
    for ax, baslik in [(a1, 'İçerik tabanlı filtreleme'),
                       (a2, 'İşbirlikçi filtreleme')]:
        ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off'); ax.set_title(baslik)
    # içerik tabanlı
    a1.add_patch(FancyBboxPatch((0.5, 4.6), 2.4, 1.5, boxstyle='round,pad=0.08',
                                facecolor=ACIK, edgecolor=LACI))
    a1.text(1.7, 5.35, 'Kullanıcının\nbeğendiği öğeler', ha='center', va='center', fontsize=8.5)
    a1.add_patch(FancyBboxPatch((3.9, 4.6), 2.4, 1.5, boxstyle='round,pad=0.08',
                                facecolor='#EAF3E9', edgecolor='#27AE60'))
    a1.text(5.1, 5.35, 'Öğe öznitelikleri\n(tür, yazar, metin)', ha='center', va='center', fontsize=8.5)
    a1.add_patch(FancyBboxPatch((7.1, 4.6), 2.4, 1.5, boxstyle='round,pad=0.08',
                                facecolor='#FDEEEA', edgecolor=KIRMIZI))
    a1.text(8.3, 5.35, 'Kullanıcı profili\n(TF-IDF vektörü)', ha='center', va='center', fontsize=8.5)
    a1.add_patch(FancyBboxPatch((3.9, 1.6), 2.4, 1.4, boxstyle='round,pad=0.08',
                                facecolor=ACIK, edgecolor=LACI))
    a1.text(5.1, 2.3, 'Kosinüs benzerliği\nile öneri', ha='center', va='center', fontsize=8.5)
    for x1, x2 in [(2.95, 3.85), (6.35, 7.05)]:
        a1.annotate('', xy=(x2, 5.35), xytext=(x1, 5.35),
                    arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    a1.annotate('', xy=(5.1, 3.1), xytext=(8.3, 4.55),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    a1.text(0.5, 0.5, 'Soğuk başlangıç yalnızca yeni kullanıcıda sorun olur;\n'
                      'yeni öğe hemen önerilebilir.', fontsize=8, color=GRI)

    # işbirlikçi
    a2.add_patch(FancyBboxPatch((0.5, 4.6), 3.0, 1.5, boxstyle='round,pad=0.08',
                                facecolor=ACIK, edgecolor=LACI))
    a2.text(2.0, 5.35, 'Kullanıcı-öğe\netkileşim matrisi', ha='center', va='center', fontsize=8.5)
    a2.add_patch(FancyBboxPatch((4.4, 5.4), 2.6, 1.2, boxstyle='round,pad=0.08',
                                facecolor='#EAF3E9', edgecolor='#27AE60'))
    a2.text(5.7, 6.0, 'Benzer kullanıcılar', ha='center', va='center', fontsize=8.5)
    a2.add_patch(FancyBboxPatch((4.4, 3.6), 2.6, 1.2, boxstyle='round,pad=0.08',
                                facecolor='#FDEEEA', edgecolor=KIRMIZI))
    a2.text(5.7, 4.2, 'Benzer öğeler', ha='center', va='center', fontsize=8.5)
    a2.add_patch(FancyBboxPatch((7.6, 4.6), 2.0, 1.4, boxstyle='round,pad=0.08',
                                facecolor=ACIK, edgecolor=LACI))
    a2.text(8.6, 5.3, 'Öneri', ha='center', va='center', fontsize=8.5)
    a2.annotate('', xy=(4.35, 6.0), xytext=(3.55, 5.6),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    a2.annotate('', xy=(4.35, 4.2), xytext=(3.55, 5.1),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    a2.annotate('', xy=(7.55, 5.5), xytext=(7.05, 6.0),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    a2.annotate('', xy=(7.55, 5.1), xytext=(7.05, 4.2),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    a2.text(0.5, 2.4, 'Öğe içeriği hiç kullanılmaz; yalnızca davranış verisi yeterlidir.\n'
                      'Yeni kullanıcı ve yeni öğe için soğuk başlangıç sorunu vardır.',
            fontsize=8, color=GRI)
    plt.tight_layout(); plt.show()


# --- Şekil 5: Matris faktörizasyonu ve seyreklik ------------------------
def matris_faktorizasyon():
    rng = np.random.default_rng(7)
    n_k, n_o, k = 40, 60, 3
    P = rng.normal(0, 1, (n_k, k))
    Q = rng.normal(0, 1, (n_o, k))
    R_tam = P @ Q.T
    maske = rng.random((n_k, n_o)) < 0.40          # %40 doluluk
    R = np.where(maske, R_tam, np.nan)

    fig = plt.figure(figsize=(13, 4.2))
    a1 = fig.add_subplot(1, 4, 1)
    a1.imshow(np.where(maske, 1.0, 0.0), cmap='Blues', aspect='auto', vmin=0, vmax=1.4)
    a1.set_title(f'R: kullanıcı × öğe\nseyreklik %{100 * (1 - maske.mean()):.0f}')
    a1.set_xlabel('öğe'); a1.set_ylabel('kullanıcı')

    a2 = fig.add_subplot(1, 4, 2)
    a2.text(0.5, 0.5, '≈', ha='center', va='center', fontsize=40, color=LACI)
    a2.axis('off')

    a3 = fig.add_subplot(1, 4, 3)
    a3.imshow(P, cmap='RdBu_r', aspect='auto')
    a3.set_title(f'P: kullanıcı × {k}\ngizli faktör'); a3.set_xticks(range(k))

    a4 = fig.add_subplot(1, 4, 4)
    a4.imshow(Q.T, cmap='RdBu_r', aspect='auto')
    a4.set_title(f'Qᵀ: {k} × öğe'); a4.set_yticks(range(k))
    plt.tight_layout(); plt.show()

    # gizli faktör sayısı - hata eğrisi
    # Gercek puanlar gurultu icerir; model gurultuyu degil yapiyi ogrenmelidir.
    R_gozlenen = R_tam + rng.normal(0, 0.8, R_tam.shape)
    gozlem = rng.permutation(np.argwhere(maske))
    kesim = int(0.8 * len(gozlem))
    egt, tst = gozlem[:kesim], gozlem[kesim:]
    egt_maske = np.zeros_like(maske)
    for i, j in egt:
        egt_maske[i, j] = True
    ort = R_gozlenen[egt_maske].mean()
    ranklar = range(1, 13)
    egt_h, tst_h = [], []
    for r in ranklar:
        # Yinelemeli SVD atamasi: eksik hucreler her turda modelin tahminiyle guncellenir
        M = np.where(egt_maske, R_gozlenen, ort)
        for _ in range(25):
            U, sv, Vt = np.linalg.svd(M, full_matrices=False)
            Rr = (U[:, :r] * sv[:r]) @ Vt[:r]
            M = np.where(egt_maske, R_gozlenen, Rr)
        egt_h.append(np.sqrt(np.mean([(Rr[i, j] - R_gozlenen[i, j]) ** 2 for i, j in egt])))
        tst_h.append(np.sqrt(np.mean([(Rr[i, j] - R_gozlenen[i, j]) ** 2 for i, j in tst])))
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(list(ranklar), egt_h, 'o-', label='Eğitim', color=LACI)
    ax.plot(list(ranklar), tst_h, 's--', label='Test', color=KIRMIZI)
    _en_iyi = int(np.argmin(tst_h)) + 1
    ax.axvline(_en_iyi, color=GRI, linestyle=':', linewidth=1)
    ax.text(_en_iyi + 0.15, max(tst_h) * 0.95,
            f'en düşük test hatası\nrank = {_en_iyi}', fontsize=8, color=GRI)
    ax.set_xlabel('Gizli faktör sayısı (rank)'); ax.set_ylabel('RMSE')
    ax.set_title('Gizli faktör sayısının hataya etkisi')
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.show()


if __name__ == '__main__':
    apriori_kafes()
    fp_tree()
    metrikler()
    tavsiye_semasi()
    matris_faktorizasyon()
