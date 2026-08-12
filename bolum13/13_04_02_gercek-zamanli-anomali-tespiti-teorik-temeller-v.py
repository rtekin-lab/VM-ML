# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK › 13.4. Akan Veri Üzerinde Makine Öğrenmesi Uygulamaları (Stream ML) › 13.4.2. Gerçek Zamanlı Anomali Tespiti: Teorik Temeller ve Uygulama Mimarileri
# Dosya : bolum13/13_04_02_gercek-zamanli-anomali-tespiti-teorik-temeller-v.py
# Gerekli: pip install apache-flink river
# ==========================================================================
# ================================================================
# Çok Katmanlı Fraud Tespiti — River (Online ML) + Flink
# pip install river apache-flink
# ================================================================
import json, math, time
from collections import deque, defaultdict
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.common.typeinfo import Types

# ---- Online Welford İstatistik Takipçisi ----
class WelfordOnlineStats:
    """
    Welford'un tek geçişli online ortalama ve varyans algoritması.
    Bellek: O(1) — tüm geçmiş veri noktaları depolanmaz.
    Güncelleme karmaşıklığı: O(1)
    """
    def __init__(self):
        self.n     = 0
        self.mean  = 0.0
        self.M2    = 0.0  # Varyansın birikimli karesi

    def update(self, x: float):
        self.n    += 1
        delta      = x - self.mean
        self.mean += delta / self.n
        delta2     = x - self.mean
        self.M2   += delta * delta2

    @property
    def variance(self) -> float:
        return self.M2 / (self.n - 1) if self.n > 1 else 0.0

    @property
    def std_dev(self) -> float:
        return math.sqrt(self.variance)

    def z_score(self, x: float) -> float:
        """z = (x - μ) / σ; |z| > 3 ise anomali."""
        if self.std_dev < 1e-9:
            return 0.0
        return (x - self.mean) / self.std_dev

# ---- CUSUM Değişim Noktası Dedektörü ----
class CUSUMDetector:
    """
    C_t = max(0, C_{t-1} + (x_t - mu0 - k))
    Alarm: C_t > H
    """
    def __init__(self, mu0: float = 0.0, k: float = 0.5, H: float = 5.0):
        self.mu0 = mu0   # Referans ortalama
        self.k   = k     # Slack (izin verilen sapma)
        self.H   = H     # Alarm eşiği
        self.C   = 0.0   # Kümülatif toplam

    def update(self, x: float) -> bool:
        self.C = max(0.0, self.C + (x - self.mu0 - self.k))
        return self.C > self.H  # True ise alarm

    def reset(self):
        self.C = 0.0

# ---- Kural Tabanlı Filtre ----
class RuleBasedFilter:
    """Hız, coğrafya ve tutar tabanlı deterministik kurallar."""

    def check(self, event: dict, history: deque) -> list:
        alerts = []
        price  = event.get('price', 0)

        # Kural 1: Aşırı yüksek tutar
        if price > 10000:
            alerts.append(('HIGH_AMOUNT', 0.8))

        # Kural 2: Hız kontrolü — 60sn içinde 5+ işlem
        now = event.get('timestamp', time.time())
        recent = [e for e in history if now - e.get('timestamp', 0) < 60]
        if len(recent) >= 5:
            alerts.append(('HIGH_VELOCITY', 0.9))

        # Kural 3: Daha önce hiç görmediğimiz yüksek riskli ülke
        HIGH_RISK = {'NG', 'RU', 'CN', 'PK'}
        if event.get('country', '') in HIGH_RISK and price > 500:
            alerts.append(('HIGH_RISK_COUNTRY', 0.7))

        return alerts

# ---- Ana Fraud Dedektörü (Flink KeyedProcessFunction) ----
class StreamingFraudDetector(KeyedProcessFunction):
    """
    Çok katmanlı fraud tespiti:
    1. Kural katmanı (deterministik)
    2. İstatistiksel katman (z-score, Welford)
    3. CUSUM değişim noktası tespiti
    Son karar: ağırlıklı ensemble skoru
    """
    FRAUD_SCORE_THRESHOLD = 0.6   # Bu değer üstü = fraud şüphesi
    HISTORY_SIZE          = 20    # Son 20 işlem hafızada

    def open(self, runtime_context):
        # Welford istatistik state'i (JSON serialized)
        self.stats_state = runtime_context.get_state(
            ValueStateDescriptor('welford_stats', Types.STRING())
        )
        # İşlem geçmişi (son N işlem)
        self.history_state = runtime_context.get_state(
            ValueStateDescriptor('tx_history', Types.STRING())
        )
        # CUSUM state
        self.cusum_state = runtime_context.get_state(
            ValueStateDescriptor('cusum_C', Types.DOUBLE())
        )
        # Kalıcı sınıf örnekleri (state değil, in-memory helper)
        self.rule_filter = RuleBasedFilter()

    def _load_stats(self) -> WelfordOnlineStats:
        raw = self.stats_state.value()
        ws  = WelfordOnlineStats()
        if raw:
            d = json.loads(raw)
            ws.n, ws.mean, ws.M2 = d['n'], d['mean'], d['M2']
        return ws

    def _save_stats(self, ws: WelfordOnlineStats):
        self.stats_state.update(json.dumps({'n': ws.n, 'mean': ws.mean, 'M2': ws.M2}))

    def process_element(self, value, ctx):
        event    = json.loads(value)
        price    = event.get('price', 0)
        user_id  = ctx.get_current_key()

        # ---- Geçmişi yükle ----
        raw_hist  = self.history_state.value()
        history   = deque(json.loads(raw_hist) if raw_hist else [], maxlen=self.HISTORY_SIZE)

        # ---- Katman 1: Kural bazlı ----
        rule_alerts = self.rule_filter.check(event, history)
        rule_score  = max((score for _, score in rule_alerts), default=0.0)

        # ---- Katman 2: İstatistiksel (Welford z-score) ----
        ws          = self._load_stats()
        z_score     = ws.z_score(price)
        stat_score  = min(abs(z_score) / 5.0, 1.0)  # Normalize [0,1]
        ws.update(price)  # Modeli güncelle
        self._save_stats(ws)

        # ---- Katman 3: CUSUM ----
        cusum_C      = self.cusum_state.value() or 0.0
        cusum        = CUSUMDetector(mu0=ws.mean, k=ws.std_dev * 0.5, H=5.0)
        cusum.C      = cusum_C
        cusum_alarm  = cusum.update(price)
        cusum_score  = 0.7 if cusum_alarm else 0.0
        self.cusum_state.update(cusum.C if not cusum_alarm else 0.0)

        # ---- Ensemble: Ağırlıklı Ortalama ----
        final_score = (0.4 * rule_score + 0.35 * stat_score + 0.25 * cusum_score)

        result = {
            **event,
            'fraud_score':    round(final_score, 4),
            'rule_score':     round(rule_score, 4),
            'stat_score':     round(stat_score, 4),
            'z_score':        round(z_score, 4),
            'cusum_score':    round(cusum_score, 4),
            'rule_alerts':    [name for name, _ in rule_alerts],
            'is_fraud_alert': final_score >= self.FRAUD_SCORE_THRESHOLD
        }

        # Geçmişi güncelle
        history.append(event)
        self.history_state.update(json.dumps(list(history)))

        yield json.dumps(result)

# ================================================================
# River — Python Online Machine Learning Kütüphanesi
# pip install river
# Referans: Online ML için scikit-multiflow'dan daha modern alternatif
# ================================================================
from river import (
    stream as rv_stream,
    tree,
    ensemble,
    anomaly,
    drift,
    metrics,
    preprocessing
)
import json

# ---- Online Hoeffding Tree Sınıflandırıcı ----
class OnlineStreamClassifier:
    """
    River'ın Hoeffding Tree sınıflandırıcısını kullanan online model.
    Her örnek görüldükten sonra model güncellenir (learn_one).
    ADWIN ile konsept kayması izlenir.
    """
    def __init__(self):
        # Hoeffding Adaptive Tree: konsept kaymasına yerleşik adaptasyon
        self.model = ensemble.AdaptiveRandomForestClassifier(
            n_models=10,
            seed=42
        )
        # Konsept Kayması Detektörü
        self.drift_detector = drift.ADWIN(delta=0.002)
        # Performans metrikleri
        self.accuracy  = metrics.Accuracy()
        self.kappa     = metrics.CohenKappa()
        self.n_samples = 0
        self.n_drifts  = 0

    def predict_and_update(self, x: dict, y: int) -> dict:
        """
        1. Tahmin yap (predict_one)
        2. Gerçek etiketi öğren (learn_one)
        3. ADWIN ile konsept kayması kontrol et
        """
        # Tahmin
        pred = self.model.predict_one(x)
        prob = self.model.predict_proba_one(x)

        # Öğren
        self.model.learn_one(x, y)
        self.n_samples += 1

        # Metrik güncelle
        if pred is not None:
            self.accuracy.update(y, pred)
            self.kappa.update(y, pred)

        # ADWIN: konsept kayması tespiti
        correct = int(pred == y) if pred is not None else 0
        self.drift_detector.update(correct)
        drift_detected = self.drift_detector.drift_detected
        if drift_detected:
            self.n_drifts += 1

        return {
            'prediction':    pred,
            'probability':   prob,
            'accuracy':      self.accuracy.get(),
            'kappa':         self.kappa.get(),
            'drift_detected': drift_detected,
            'n_drifts':      self.n_drifts,
            'n_samples':     self.n_samples
        }

# ---- Kullanım: Simüle Edilmiş Fraud Akışı ----
def simulate_streaming_fraud_detection():
    from river.datasets import CreditCard

    classifier = OnlineStreamClassifier()

    print(f"{'Örnek':>8} | {'Tahmin':>7} | {'Gerçek':>7} | {'Doğruluk':>9} | {'Kayma':>6}")
    print('-' * 55)

    # Streaming veri simülasyonu (her örnek tek seferde işlenir)
    for i, (x, y) in enumerate(CreditCard().take(10000)):

        # Özellik ön-işleme (online normalleştirme)
        result = classifier.predict_and_update(x, y)

        if i % 500 == 0:
            print(
                f"{i:>8} | {result['prediction']:>7} | {y:>7} | "
                f"{result['accuracy']:>9.4f} | {result['n_drifts']:>6}"
            )

    print(f"\nFinal Doğruluk: {classifier.accuracy.get():.4f}")
    print(f"Toplam Konsept Kayması Sayısı: {classifier.n_drifts}")
    print(f"Cohen Kappa: {classifier.kappa.get():.4f}")

if __name__ == '__main__':
    simulate_streaming_fraud_detection()
