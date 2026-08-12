# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › Bölüm şekilleri
# Dosya : bolum09/09_00_bolum-sekilleri.py
# Gerekli: pip install numpy matplotlib scikit-learn
# ==========================================================================
"""Bölüm 9'un kavramsal ve uygulamalı şekillerini üretir."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

LACI, MAVI, ACIK, GRI = '#1F3864', '#2E5A8A', '#DCE6F1', '#7A7A7A'
YESIL, KIRMIZI = '#27AE60', '#C0392B'
plt.rcParams['font.size'] = 9

BELGELER = [
    "kedi bahçede uyudu",
    "köpek bahçede koştu ve kedi kaçtı",
    "kedi kedi kedi mırıldandı",
    "veri madenciliği örüntü keşfeder",
    "makine öğrenmesi veri kullanır",
]


# --- Şekil 1: Metin normalizasyon boru hattı ----------------------------
def normalizasyon_hatti():
    adimlar = [
        ('Ham metin', '"Bu ÜRÜNÜ çok\nbeğendim!!! 5 yıldız."'),
        ('Temizleme', 'noktalama, sayı ve\nfazla boşluk atılır'),
        ('Küçük harf', '"bu ürünü çok\nbeğendim yıldız"'),
        ('Parçalama', '[bu, ürünü, çok,\nbeğendim, yıldız]'),
        ('Durdurma\nkelimeleri', '[ürünü, çok,\nbeğendim, yıldız]'),
        ('Kök / gövde', '[ürün, çok,\nbeğen, yıldız]'),
    ]
    fig, ax = plt.subplots(figsize=(13.5, 3.4))
    w, h, bosluk = 1.95, 1.6, 0.34
    for i, (bas, alt) in enumerate(adimlar):
        x = 0.2 + i * (w + bosluk)
        ax.add_patch(FancyBboxPatch((x, 0.9), w, h, boxstyle='round,pad=0.06',
                                    facecolor=ACIK, edgecolor=LACI, linewidth=1.3))
        ax.text(x + w / 2, 2.15, bas, ha='center', va='center',
                fontsize=9, fontweight='bold', color=LACI)
        ax.text(x + w / 2, 1.42, alt, ha='center', va='center', fontsize=7.5, color='#333333')
        if i < len(adimlar) - 1:
            ax.annotate('', xy=(x + w + bosluk - 0.05, 1.7), xytext=(x + w + 0.04, 1.7),
                        arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.5))
    ax.text(0.2, 0.45, 'Her adım sözcük dağarcığını küçültür; hangi adımın uygulanacağı göreve bağlıdır.',
            fontsize=8, color=GRI)
    ax.set_xlim(0, 0.2 + 6 * (w + bosluk)); ax.set_ylim(0.1, 2.8); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 2: BoW ve TF-IDF matrisleri ----------------------------------
def bow_tfidf():
    cv = CountVectorizer()
    X = cv.fit_transform(BELGELER).toarray()
    tf = TfidfVectorizer()
    T = tf.fit_transform(BELGELER).toarray()
    kelimeler = cv.get_feature_names_out()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13.5, 4.4))
    for ax, M, ad, cmap in [(a1, X, 'Bag-of-Words (ham sayım)', 'Blues'),
                            (a2, T, 'TF-IDF (ağırlıklandırılmış)', 'Oranges')]:
        im = ax.imshow(M, cmap=cmap, aspect='auto')
        ax.set_xticks(range(len(kelimeler)))
        ax.set_xticklabels(kelimeler, rotation=60, ha='right', fontsize=7.5)
        ax.set_yticks(range(len(BELGELER)))
        ax.set_yticklabels([f'B{i+1}' for i in range(len(BELGELER))], fontsize=8)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i, j] > 0:
                    ax.text(j, i, f'{M[i, j]:.2f}'.rstrip('0').rstrip('.') if ad.startswith('TF')
                            else f'{int(M[i, j])}', ha='center', va='center', fontsize=6.5,
                            color='white' if M[i, j] > M.max() * 0.6 else '#333333')
        ax.set_title(ad)
        plt.colorbar(im, ax=ax, shrink=0.8)
    a1.set_ylabel('belge')
    plt.tight_layout(); plt.show()

    # "kedi" sözcüğünün iki temsildeki ağırlığı
    idx = list(kelimeler).index('kedi')
    # Iki temsili kendi olcegiyle, cift eksende karsilastir (olcekleme yaniltici olurdu)
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    x = np.arange(len(BELGELER))
    ax.bar(x - 0.2, X[:, idx], 0.4, label='BoW sayımı', color=MAVI)
    ax.set_xticks(x); ax.set_xticklabels([f'B{i+1}' for i in x])
    ax.set_ylabel('BoW sayımı', color=MAVI); ax.tick_params(axis='y', labelcolor=MAVI)
    ax2 = ax.twinx()
    ax2.bar(x + 0.2, T[:, idx], 0.4, label='TF-IDF ağırlığı', color='#E67E22')
    ax2.set_ylabel('TF-IDF ağırlığı', color='#E67E22'); ax2.tick_params(axis='y', labelcolor='#E67E22')
    for i in x:
        if X[i, idx] > 0:
            ax.text(i - 0.2, X[i, idx] + 0.05, f'{int(X[i, idx])}', ha='center', fontsize=8)
        if T[i, idx] > 0:
            ax2.text(i + 0.2, T[i, idx] + 0.015, f'{T[i, idx]:.2f}', ha='center', fontsize=8)
    ax.set_title('"kedi" sözcüğünün belgelere göre ağırlığı')
    ax.grid(alpha=0.3, axis='y')
    ax.set_ylim(0, 3.9); ax2.set_ylim(0, 1.17)
    ax.text(0.5, -0.22, 'B3\'te "kedi" üç kez geçtiği için TF-IDF en yüksek değerini burada alır; '
                        'sözcük üç belgede birden\ngöründüğünden IDF terimi ağırlığın daha da '
                        'artmasını engeller. B4 ve B5\'te sözcük hiç geçmez.',
            transform=ax.transAxes, fontsize=7.5, va='top', ha='center', color=GRI)
    plt.tight_layout(rect=[0, 0.08, 1, 1]); plt.show()


# --- Şekil 3: Seyrek ve yoğun temsil ------------------------------------
def seyrek_yogun():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4),
                                 gridspec_kw={'width_ratios': [1.6, 1]})
    rng = np.random.default_rng(3)
    V = 60
    seyrek = np.zeros((5, V))
    for i in range(5):
        seyrek[i, rng.choice(V, 4, replace=False)] = rng.integers(1, 4, 4)
    a1.imshow(seyrek, cmap='Blues', aspect='auto')
    a1.set_title(f'TF-IDF / BoW: {V} boyut, %{100*(seyrek==0).mean():.0f} sıfır')
    a1.set_xlabel('sözcük dağarcığı boyutu'); a1.set_ylabel('belge')
    a1.set_yticks(range(5)); a1.set_yticklabels([f'B{i+1}' for i in range(5)])

    # Yogun temsilde benzer belgeler benzer vektorler alir (rastgele degil, yapili)
    temel = rng.normal(0, 1, (2, 8))
    yogun = np.vstack([temel[0] + rng.normal(0, 0.25, 8),
                       temel[0] + rng.normal(0, 0.25, 8),
                       temel[0] + rng.normal(0, 0.25, 8),
                       temel[1] + rng.normal(0, 0.25, 8),
                       temel[1] + rng.normal(0, 0.25, 8)])
    im = a2.imshow(yogun, cmap='RdBu_r', aspect='auto')
    a2.set_title('Kelime gömüsü: 8 boyut, sıfır yok\nB1–B3 ve B4–B5 benzer örüntü')
    a2.set_xlabel('gizli boyut'); a2.set_yticks(range(5))
    a2.set_yticklabels([f'B{i+1}' for i in range(5)])
    plt.colorbar(im, ax=a2, shrink=0.85)
    plt.tight_layout(); plt.show()


# --- Şekil 4: CBOW ve Skip-Gram mimarileri ------------------------------
def cbow_skipgram():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.4))
    baglam = ['kedi', 'bahçede', 'uyudu', 'sabaha']
    hedef = 'sessizce'

    def kutu(ax, x, y, w, h, metin, renk, kenar):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05',
                                    facecolor=renk, edgecolor=kenar, linewidth=1.2))
        ax.text(x + w / 2, y + h / 2, metin, ha='center', va='center', fontsize=8.5)

    # CBOW: bağlam -> hedef
    for i, b in enumerate(baglam):
        kutu(a1, 0.3, 4.4 - i * 1.05, 1.8, 0.7, b, ACIK, LACI)
        a1.annotate('', xy=(3.0, 2.9), xytext=(2.15, 4.75 - i * 1.05),
                    arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.1))
    kutu(a1, 3.0, 2.55, 1.7, 0.75, 'ortalama\n(gizli katman)', '#EFEFEF', GRI)
    kutu(a1, 5.6, 2.55, 1.8, 0.75, hedef, '#FDEEEA', KIRMIZI)
    a1.annotate('', xy=(5.55, 2.92), xytext=(4.75, 2.92),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    a1.set_title('CBOW: bağlamdan hedef kelimeyi kestir')
    a1.text(0.3, 0.7, 'Sık kelimelerde daha hızlı ve kararlı.', fontsize=8, color=GRI)

    # Skip-Gram: hedef -> bağlam
    kutu(a2, 0.4, 2.55, 1.8, 0.75, hedef, '#FDEEEA', KIRMIZI)
    kutu(a2, 3.0, 2.55, 1.7, 0.75, 'gizli katman', '#EFEFEF', GRI)
    a2.annotate('', xy=(2.95, 2.92), xytext=(2.25, 2.92),
                arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.4))
    for i, b in enumerate(baglam):
        kutu(a2, 5.6, 4.4 - i * 1.05, 1.8, 0.7, b, ACIK, LACI)
        a2.annotate('', xy=(5.55, 4.75 - i * 1.05), xytext=(4.75, 2.92),
                    arrowprops=dict(arrowstyle='-|>', color=MAVI, linewidth=1.1))
    a2.set_title('Skip-Gram: hedeften bağlamı kestir')
    a2.text(0.4, 0.7, 'Az veride ve seyrek kelimelerde daha başarılı.', fontsize=8, color=GRI)
    for ax in (a1, a2):
        ax.set_xlim(0, 7.8); ax.set_ylim(0.3, 5.6); ax.axis('off')
    plt.tight_layout(); plt.show()


# --- Şekil 5: Duygu analizi yaklaşımlarının karşılaştırması -------------
def duygu_yaklasimlari():
    yaklasimlar = ['Sözlük tabanlı\n(VADER)', 'Klasik ML\n(TF-IDF + LR)',
                   'Kelime gömüsü\n(Word2Vec + LR)', 'Bağlamsal\n(BERT ince ayar)']
    dogruluk = [0.68, 0.84, 0.86, 0.93]
    veri = ['etiketli veri\ngerekmez', '~1.000 örnek', '~5.000 örnek', '~10.000 örnek']
    maliyet = [1, 2, 3, 5]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.2))
    renkler = ['#95A5A6', MAVI, '#E67E22', LACI]
    b = a1.bar(range(4), dogruluk, color=renkler, edgecolor='white')
    for i, (d, v) in enumerate(zip(dogruluk, veri)):
        a1.text(i, d + 0.012, f'{d:.2f}', ha='center', fontsize=9, fontweight='bold')
        a1.text(i, 0.03, v, ha='center', fontsize=7.5, color='white')
    a1.set_xticks(range(4)); a1.set_xticklabels(yaklasimlar, fontsize=8)
    a1.set_ylim(0, 1.0); a1.set_ylabel('Doğruluk (temsilî)')
    a1.set_title('Yaklaşımların başarımı ve veri gereksinimi')
    a1.grid(alpha=0.3, axis='y')

    a2.scatter(maliyet, dogruluk, s=180, c=renkler, edgecolor=LACI, zorder=3)
    for i, ad in enumerate(['VADER', 'TF-IDF+LR', 'Word2Vec+LR', 'BERT']):
        a2.annotate(ad, (maliyet[i], dogruluk[i]), textcoords='offset points',
                    xytext=(8, -4), fontsize=8)
    a2.set_xlabel('Hesaplama ve kurulum maliyeti (göreli)')
    a2.set_ylabel('Doğruluk'); a2.set_xlim(0, 6); a2.set_ylim(0.6, 1.0)
    a2.set_title('Başarım ile maliyet arasındaki ödünleşim')
    a2.grid(alpha=0.3)
    plt.tight_layout(); plt.show()


if __name__ == '__main__':
    normalizasyon_hatti()
    bow_tfidf()
    seyrek_yogun()
    cbow_skipgram()
    duygu_yaklasimlari()
