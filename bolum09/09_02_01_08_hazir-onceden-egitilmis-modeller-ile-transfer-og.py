# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 9
# Konum : BÖLÜM 9: Metin Madenciliği ve Doğal Dil İşleme (NLP) › 9.2. Modern NLP: Anlamsal Analiz › 9.2.1. Kelime Gömüleri (Word Embeddings): Kelimeleri Vektör Uzayında Temsil Etmek › 9.2.1.8. Hazır Önceden Eğitilmiş Modeller ile Transfer Öğrenmesi
# Kitap  : Kod 9.7 (BERT ile [CLS] token gömüsünden metin düzeyi)
# Dosya : bolum09/09_02_01_08_hazir-onceden-egitilmis-modeller-ile-transfer-og.py
# Gerekli: pip install gensim numpy torch transformers
# ==========================================================================
import gensim.downloader as api
from gensim.models import KeyedVectors
import numpy as np

# ============================================================
# 1. GENSIM'DEN HAZIR MODEL (İNDİRİLMESİ GEREKİR)
# ============================================================
# Mevcut modelleri listele
print('Kullanılabilir hazır modeller:')
for model_name in list(api.info()['models'].keys())[:10]:
    print(f'  - {model_name}')

# Google News Word2Vec (3 milyar kelime, 300 boyut) — 1.6 GB
# wv = api.load('word2vec-google-news-300')

# GloVe Wikipedia + Gigaword (6B kelime, 100 boyut) — 128 MB
# wv = api.load('glove-wiki-gigaword-100')

# Küçük test modeli (hızlı indirme)
print('\nKüçük model yükleniyor...')
wv = api.load('glove-wiki-gigaword-50')
print(f'Model yüklendi: {len(wv)} kelime, {wv.vector_size} boyut')

# ============================================================
# 2. HAZIR MODEL ANALİZLERİ
# ============================================================
print('\n=== king - man + woman analojisi ===')
result = wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=3)
for word, score in result:
    print(f'  {word}: {score:.4f}')
# Beklenen çıktı: queen ≈ 0.85

print('\n=== Ülke - Başkent analojisi (Paris - France + Germany) ===')
result = wv.most_similar(positive=['paris', 'germany'], negative=['france'], topn=3)
for word, score in result:
    print(f'  {word}: {score:.4f}')
# Beklenen: berlin

# ============================================================
# 3. EMBEDDING'İ ÖZELLİK OLARAK KULLANMA (Metin Sınıflandırma)
# ============================================================
def metin_vektoru(metin, wv, boyut=50):
    """
    Bir metindeki tüm kelimelerin embedding'lerinin ortalamasını
    alarak metin düzeyinde vektör üretir.
    """
    kelimeler = metin.lower().split()
    vektorler = [wv[k] for k in kelimeler if k in wv]
    if not vektorler:
        return np.zeros(boyut)
    return np.mean(vektorler, axis=0)

# Test
metinler = [
    'the movie was absolutely fantastic and entertaining',
    'terrible film complete waste of time',
    'neural networks learn from large datasets',
]
for m in metinler:
    vec = metin_vektoru(m, wv)
    print(f'\nMetin: {m[:40]}...')
    print(f'Vektör şekli: {vec.shape}, İlk 5 değer: {np.round(vec[:5], 4)}')

# ============================================================
# 4. HUGGINGFACE İLE BERT EMBEDDING'İ
# ============================================================
try:
    from transformers import AutoTokenizer, AutoModel
    import torch

    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    bert_model = AutoModel.from_pretrained('bert-base-uncased')

    metin = 'The bank is on the river bank near the financial bank'
    inputs = tokenizer(metin, return_tensors='pt', padding=True)

    # [CLS] token embedding — metin düzeyi temsil
    with torch.no_grad():
        outputs = bert_model(**inputs)

    cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
    print(f'\nBERT [CLS] embedding boyutu: {cls_embedding.shape}')
    # Her 'bank' kelimesi için farklı bağlamsal vektör üretildi!
except ImportError:
    print('Kurulum: pip install transformers torch')
