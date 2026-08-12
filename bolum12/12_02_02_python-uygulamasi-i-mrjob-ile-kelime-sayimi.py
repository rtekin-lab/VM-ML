# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.2. Hadoop Ekosistemi ve MapReduce Mantığı › 12.2.2. MapReduce Programlama Modeli › Python Uygulaması I: mrjob ile Kelime Sayımı
# Kitap  : Kod 12.3 (mrjob ile MapReduce: kelime sayımı)
# Dosya : bolum12/12_02_02_python-uygulamasi-i-mrjob-ile-kelime-sayimi.py
# ==========================================================================
# ============================================================
# mrjob ile MapReduce — Kelime Sayımı (Big Data 'Hello World')
# Gereksinim: pip install mrjob
# Çalıştırma: python kelime_sayim.py genis_metin.txt
# ============================================================
from mrjob.job import MRJob
from mrjob.step import MRStep
import re

KELIME_RE = re.compile(r"[\w']+")

class GelismisKelimeSayimi(MRJob):
    """
    Çok adımlı MapReduce:
    Adım 1: Kelime frekanslarını say
    Adım 2: En sık 10 kelimeyi bul (sıralama için ikinci M-R)
    """

    def steps(self):
        return [
            MRStep(mapper=self.mapper_kelime_say,
                   combiner=self.combiner_toplam,    # Yerel ön-toplama
                   reducer=self.reducer_toplam),
            MRStep(mapper=self.mapper_ters_cevir,
                   reducer=self.reducer_en_siklar),
        ]

    # ---- ADIM 1: Kelime → (kelime, 1) ----
    def mapper_kelime_say(self, _, satir):
        """Her satırı kelimelerine ayır, küçük harfe çevir"""
        for kelime in KELIME_RE.findall(satir.lower()):
            if len(kelime) > 2:  # Çok kısa kelimeleri filtrele
                yield kelime, 1

    # ---- COMBINER: Yerel pre-reduce (ağ trafiğini azaltır) ----
    def combiner_toplam(self, kelime, sayilar):
        yield kelime, sum(sayilar)

    # ---- REDUCER 1: Toplam frekans hesabı ----
    def reducer_toplam(self, kelime, sayilar):
        yield None, (sum(sayilar), kelime)  # None: tek reducer'a topla

    # ---- ADIM 2: (None, (sayi, kelime)) → (sayi, kelime) ----
    def mapper_ters_cevir(self, _, sayi_kelime):
        sayi, kelime = sayi_kelime
        yield -sayi, kelime   # Eksi: büyükten küçüğe sıralama için

    # ---- REDUCER 2: En sık N kelimeyi döndür ----
    def reducer_en_siklar(self, ters_sayi, kelimeler):
        for i, kelime in enumerate(kelimeler):
            if i >= 10:  # İlk 10'u al
                break
            yield kelime, -ters_sayi

if __name__ == '__main__':
    GelismisKelimeSayimi.run()

# ============================================================
# Basit tek adımlı MapReduce (referans amaçlı)
# ============================================================
class BasitKelimeSayimi(MRJob):
    def mapper(self, _, satir):
        for kelime in KELIME_RE.findall(satir):
            yield (kelime.lower(), 1)

    def combiner(self, kelime, sayilar):  # Yerel ön-reduce
        yield (kelime, sum(sayilar))

    def reducer(self, kelime, sayilar):
        yield (kelime, sum(sayilar))

# Hadoop kümesinde çalıştırma:
# python kelime_sayim.py -r hadoop hdfs:///input/buyuk_metin.txt --output-dir=hdfs:///output/

# Yerel modda test:
# python kelime_sayim.py test_metin.txt
