# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK › 13.4. Akan Veri Üzerinde Makine Öğrenmesi Uygulamaları (Stream ML) › 13.4.1. Akan Veride Sınıflandırma ve Kümeleme: Teorik Temeller ve Algoritmalar
# Kitap  : Kod 13.5 (CluStream mikro-küme yapısının uygulanması) · Kod 13.6 (River ile çevrim içi öğrenme: test-sonra-eği)
# Dosya : bolum13/13_04_01_akan-veride-siniflandirma-ve-kumeleme-teorik-tem.py
# Gerekli: pip install apache-flink
# ==========================================================================
# ================================================================
# CluStream Mikro-Küme Güncelleyici — Flink KeyedProcessFunction
# River kütüphanesi (pip install river) ile Online ML
# ================================================================
import json, math
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.common.typeinfo import Types

class MicroClusterCF:
    """
    CluStream CF Vektörü: (N, LS, SS, LT, ST)
    Bellek: O(1) — nokta sayısından bağımsız.
    """
    __slots__ = ['n', 'ls', 'ss', 'lt', 'st', 'dim']

    def __init__(self, dim: int):
        self.n   = 0
        self.ls  = [0.0] * dim   # Doğrusal toplam (her boyut)
        self.ss  = [0.0] * dim   # Kareli toplam (her boyut)
        self.lt  = 0.0           # Zaman doğrusal toplamı
        self.st  = 0.0           # Zaman kareli toplamı
        self.dim = dim

    def add_point(self, x: list, t: float):
        """O(d) karmaşıklığıyla yeni nokta ekle."""
        self.n  += 1
        self.lt += t
        self.st += t * t
        for i, xi in enumerate(x):
            self.ls[i] += xi
            self.ss[i] += xi * xi

    @property
    def centroid(self) -> list:
        """Centroid = LS / N"""
        if self.n == 0:
            return [0.0] * self.dim
        return [ls_i / self.n for ls_i in self.ls]

    @property
    def radius(self) -> float:
        """
        Radius = sqrt(SS/N - (LS/N)^2)
        Öklid uzayında mikro-kümenin ortalama yarıçapı.
        """
        if self.n < 2:
            return 0.0
        centroid = self.centroid
        r_sq = sum(
            (self.ss[i] / self.n) - (centroid[i] ** 2)
            for i in range(self.dim)
        )
        return math.sqrt(max(r_sq, 0.0))

    def distance_to(self, x: list) -> float:
        """Noktanın centroid'e Öklid uzaklığı."""
        c = self.centroid
        return math.sqrt(sum((xi - ci)**2 for xi, ci in zip(x, c)))

    def to_dict(self) -> dict:
        return {
            'n':        self.n,
            'centroid': self.centroid,
            'radius':   round(self.radius, 4),
            'mean_time': self.lt / self.n if self.n > 0 else 0
        }

    @staticmethod
    def merge(cf1: 'MicroClusterCF', cf2: 'MicroClusterCF') -> 'MicroClusterCF':
        """İki CF vektörünü birleştir: Additive property."""
        merged = MicroClusterCF(cf1.dim)
        merged.n  = cf1.n  + cf2.n
        merged.lt = cf1.lt + cf2.lt
        merged.st = cf1.st + cf2.st
        merged.ls = [a + b for a, b in zip(cf1.ls, cf2.ls)]
        merged.ss = [a + b for a, b in zip(cf1.ss, cf2.ss)]
        return merged

class OnlineClusteringProcessor(KeyedProcessFunction):
    """
    Flink KeyedProcessFunction olarak CluStream Faz-1 (Online).
    Her anahtar (ör. ürün kategorisi) için bağımsız mikro-kümeler tutar.
    """
    MAX_MICRO_CLUSTERS = 10
    RADIUS_FACTOR      = 1.5  # Mevcut en yakın küme yarıçapının kaç katı

    def open(self, runtime_context):
        # Mikro-küme listesi state olarak saklanır
        desc = ValueStateDescriptor('micro_clusters', Types.STRING())
        self.cluster_state = runtime_context.get_state(desc)

    def process_element(self, value, ctx):
        event = json.loads(value)

        # Özellik vektörü çıkar
        features = [
            event.get('price', 0),
            event.get('quantity', 0),
            event.get('total_value', 0)
        ]
        t = event.get('timestamp', 0)

        # Mevcut mikro-kümeleri yükle
        raw = self.cluster_state.value()
        clusters_data = json.loads(raw) if raw else []
        clusters = []
        for cd in clusters_data:
            mc = MicroClusterCF(dim=3)
            mc.n, mc.ls, mc.ss, mc.lt, mc.st = (
                cd['n'], cd['ls'], cd['ss'], cd['lt'], cd['st']
            )
            clusters.append(mc)

        # En yakın mikro-kümeyi bul
        best_mc   = None
        best_dist = float('inf')
        for mc in clusters:
            d = mc.distance_to(features)
            if d < best_dist:
                best_dist = d
                best_mc   = mc

        # Atama kararı
        max_radius = (best_mc.radius * self.RADIUS_FACTOR
                      if best_mc and best_mc.radius > 0 else 1.0)
        if best_mc and best_dist <= max_radius:
            best_mc.add_point(features, t)  # Mevcut kümeye ekle
        elif len(clusters) < self.MAX_MICRO_CLUSTERS:
            new_mc = MicroClusterCF(dim=3)  # Yeni mikro-küme oluştur
            new_mc.add_point(features, t)
            clusters.append(new_mc)
        else:
            # En küçük kümeyi en yakın komşusuyla birleştir, yer aç
            smallest = min(clusters, key=lambda c: c.n)
            clusters.remove(smallest)
            if best_mc:
                merged = MicroClusterCF.merge(smallest, best_mc)
                clusters.remove(best_mc)
                clusters.append(merged)
            new_mc = MicroClusterCF(dim=3)
            new_mc.add_point(features, t)
            clusters.append(new_mc)

        # State'i güncelle
        clusters_data = [{'n': c.n, 'ls': c.ls, 'ss': c.ss, 'lt': c.lt, 'st': c.st}
                         for c in clusters]
        self.cluster_state.update(json.dumps(clusters_data))

        # Sonuç çıktısı
        result = {
            'category':      ctx.get_current_key(),
            'micro_clusters': [c.to_dict() for c in clusters],
            'timestamp':     t
        }
        yield json.dumps(result)
