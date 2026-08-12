# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.2. Hadoop Ekosistemi ve MapReduce Mantığı › 12.2.2. MapReduce Programlama Modeli › Python Uygulaması II: Saf Python'da MapReduce Simülasyonu
# Kitap  : Kod 12.5 (Paralel işlemeyle MapReduce benzetimi)
# Dosya : bolum12/12_02_02_python-uygulamasi-ii-saf-python-da-mapreduce-sim.py
# ==========================================================================
# ============================================================
# Saf Python'da MapReduce Mantığını Anlamak
# (Gerçek dağıtık framework kullanmadan kavramsal demo)
# ============================================================
from collections import defaultdict
from functools import reduce as py_reduce
from multiprocessing import Pool
import time

# ---- VERİ SİMÜLASYONU ----
def buyuk_metin_uret(satir_sayisi=100_000):
    import random
    kelimeler = ['python', 'büyük', 'veri', 'spark', 'hadoop', 'makine',
                 'öğrenme', 'dağıtık', 'sistem', 'analiz', 'model', 'küme']
    satirlar = []
    for _ in range(satir_sayisi):
        n = random.randint(5, 15)
        satirlar.append(' '.join(random.choices(kelimeler, k=n)))
    return satirlar

# ---- MAP FONKSİYONU ----
def map_fonksiyon(satir):
    """(satir) → list[(kelime, 1)]"""
    return [(kelime.lower(), 1) for kelime in satir.split()]

# ---- SHUFFLE & SORT ----
def shuffle_sort(anahtar_deger_listesi):
    """Tüm (kelime, 1) çiftlerini anahtara göre grupla"""
    gruplama = defaultdict(list)
    for kelime, sayi in anahtar_deger_listesi:
        gruplama[kelime].append(sayi)
    return dict(gruplama)

# ---- REDUCE FONKSİYONU ----
def reduce_fonksiyon(anahtar, degerler):
    """(kelime, [1, 1, 1, ...]) → (kelime, toplam)"""
    return (anahtar, sum(degerler))

# ---- SEKANSİYEL (TEK MAKİNE) ÇALIŞMA ----
def sekansiyel_word_count(satirlar):
    baslangic = time.time()
    # Map aşaması
    tum_cifter = []
    for satir in satirlar:
        tum_cifter.extend(map_fonksiyon(satir))
    # Shuffle & Sort
    gruplu = shuffle_sort(tum_cifter)
    # Reduce aşaması
    sonuclar = {k: reduce_fonksiyon(k, v) for k, v in gruplu.items()}
    with Pool(n_workers) as pool:
        reduce_sonuclar = pool.starmap(reduce_fonksiyon, gruplu.items())

    sure = time.time() - baslangic
    return sonuclar, sure

# ---- PARALELİZE EDİLMİŞ (ÇOK ÇEKIRDEK) ÇALIŞMA ----
def paralel_word_count(satirlar, n_workers=4):
    baslangic = time.time()
    # Veriyi n_workers parçaya böl
    parcalar = [satirlar[i::n_workers] for i in range(n_workers)]

    # Paralel Map (çok çekirdek)
    with Pool(n_workers) as pool:
        # Her chunk'a map_fonksiyon uygula
        sonuclar = pool.map(
            lambda parca: [p for satir in parca for p in map_fonksiyon(satir)],
            parcalar
        )

    # Shuffle & Sort (birleştir)
    tum_cifter = [c for sonuc in sonuclar for c in sonuc]
    gruplu = shuffle_sort(tum_cifter)

    sure = time.time() - baslangic
    return dict(reduce_sonuclar), sure

# ---- DEMO ----
satirlar = buyuk_metin_uret(100_000)
print(f'Toplam satır sayısı: {len(satirlar):,}')
print(f'Toplam kelime tahmini: {sum(len(s.split()) for s in satirlar[:1000]) * 100:,}')

# Sekansiyel çalıştırma
seq_sonuc, seq_sure = sekansiyel_word_count(satirlar)
en_siklar_seq = sorted(seq_sonuc.values(), key=lambda x: -x[1])[:5]
print(f'\nSekansiyel süre : {seq_sure:.3f} sn')
print(f'En sık 5 kelime : {en_siklar_seq}')

# Not: paralel_word_count lambda ile Pool.map uyumsuzluğu olabilir
# Gerçek Hadoop/Spark ortamında bu sorun yoktur
print('\nGerçek dağıtık işlemde Hadoop/Spark bu adımları otonom yönetir.')
