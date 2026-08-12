# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.2. Modern NLP: Anlamsal Analiz › 9.2.1. Kelime Gömüleri (Word Embeddings): Kelimeleri Vektör Uzayında Temsil Etmek › 9.2.1.7. Python Uygulaması: Gensim ile Word2Vec Eğitimi ve Analizi
# Kitap  : Kod 9.6 (Gensim ile Word2Vec eğitimi ve analoji sorgu)
# Dosya : bolum09/09_02_01_07_python-uygulamasi-gensim-ile-word2vec-egitimi-ve.py
# Gerekli: pip install gensim matplotlib nltk numpy scikit-learn
# ==========================================================================
import nltk
import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# ============================================================
# 1. CORPUS VE EĞİTİM
# ============================================================
cumleler = [
    'kral sarayda hüküm sürer ve ülkeyi yönetir',
    'kraliçe sarayda oturur ve ülkeyi yönetir',
    'erkek adam güçlü ve cesur olmalıdır',
    'kadın güçlü ve cesur olabilir kraliçe gibi',
    'kedi evcil hayvan olarak evde yaşar',
    'köpek evcil hayvan olarak evde yaşar',
    'kedi ve köpek çok iyi evcil hayvanlardır',
    'veri bilimi makine öğrenmesi algoritmaları ile çalışır',
    'yapay zeka derin öğrenme sinir ağları kullanır',
    'doğal dil işleme metin analizi için kullanılır',
    'python programlama dili veri analizi için idealdir',
    'java programlama dili nesne yönelimli bir dildir',
    'paris fransa başkentidir avrupa şehridir',
    'berlin almanya başkentidir avrupa şehridir',
    'roma italya başkentidir tarihi avrupa şehridir',
]

# Tokenize: Cümleleri kelime listelerine böl
token_cumleler = [nltk.word_tokenize(c.lower()) for c in cumleler]

# Word2Vec modeli eğitimi
model = Word2Vec(
    sentences=token_cumleler,
    vector_size=50,    # Embedding boyutu (üretimde 100-300)
    window=3,          # Bağlam penceresi yarıçapı
    min_count=1,       # Minimum kelime frekansı
    sg=1,              # 1=Skip-Gram, 0=CBOW
    negative=5,        # Negative sampling sayısı
    epochs=100,        # Eğitim döngüsü sayısı
    workers=4          # Paralel iş parçacığı
)

print(f'Kelime Dağarcığı: {len(model.wv)} kelime')
print(f'Vektör Boyutu: {model.vector_size}')

# ============================================================
# 2. KELİME VEKTÖRLERİ VE BENZERLİK
# ============================================================
print('\n=== Kelime Vektörü (kral) — İlk 10 boyut ===')
print(np.round(model.wv['kral'][:10], 4))

print('\n=== kedi kelimesine en benzer kelimeler ===')
for kelime, skor in model.wv.most_similar('kedi', topn=5):
    print(f'  {kelime:<15} benzerlik: {skor:.4f}')

print('\n=== kral-erkek+kadın analojisi ===')
try:
    sonuc = model.wv.most_similar(
        positive=['kral', 'kadın'],
        negative=['erkek'],
        topn=3
    )
    print('Beklenen: kraliçe')
    for k, s in sonuc:
        print(f'  {k}: {s:.4f}')
except Exception as e:
    print(f'Küçük corpus sınırlaması: {e}')

# Kosinüs benzerliği hesaplama
if 'kedi' in model.wv and 'köpek' in model.wv:
    sim_kedi_kopek = model.wv.similarity('kedi', 'köpek')
    sim_kedi_ucak = model.wv.similarity('kedi', 'veri')
    print(f'\nkedi — köpek benzerliği: {sim_kedi_kopek:.4f}')
    print(f'kedi — veri benzerliği:  {sim_kedi_ucak:.4f}')

# ============================================================
# 3. MODELİ KAYDETME VE YÜKLEME
# ============================================================
model.wv.save('kelime_vektorleri.kv')
# Yükleme:
# loaded_wv = KeyedVectors.load('kelime_vektorleri.kv')
print('\nModel kaydedildi: kelime_vektorleri.kv')

# ============================================================
# 4. PCA İLE 2 BOYUTLU GÖRSELLEŞTİRME
# ============================================================
kelimeler = ['kral', 'kraliçe', 'erkek', 'kadın', 'kedi', 'köpek',
             'paris', 'berlin', 'roma', 'python', 'java']
mevcut = [k for k in kelimeler if k in model.wv]

if mevcut:
    vektorler = np.array([model.wv[k] for k in mevcut])
    pca = PCA(n_components=2)
    koordinatlar = pca.fit_transform(vektorler)

    plt.figure(figsize=(10, 7))
    plt.scatter(koordinatlar[:, 0], koordinatlar[:, 1],
                c='steelblue', s=100, alpha=0.7)
    for i, kelime in enumerate(mevcut):
        plt.annotate(kelime, (koordinatlar[i, 0], koordinatlar[i, 1]),
                     fontsize=12, ha='right')
    plt.title('Word2Vec Vektörlerinin PCA ile 2D Projeksiyonu')
    plt.xlabel('1. Bileşen')
    plt.ylabel('2. Bileşen')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('w2v_pca.png', dpi=150)
    plt.show()
    print(f'\nPCA Açıklanan Varyans: {pca.explained_variance_ratio_.sum():.2%}')
