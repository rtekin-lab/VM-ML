# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 13
# Konum : BÖLÜM 13: VERİ AKIŞI İŞLEME VE GERÇEK ZAMANLI ANALİTİK › 13.3. Apache Flink ile Gerçek Zamanlı Veri İşleme Motoru › 13.3.3. Veri Akışı Operatörleri: Matematiksel Temelleri ve Python Uygulamaları
# Dosya : bolum13/13_03_03_veri-akisi-operatorleri-matematiksel-temelleri-v.py
# Gerekli: pip install apache-flink
# ==========================================================================
# ================================================================
# PyFlink Gerçek Zamanlı Analitik Pipeline
# pip install apache-flink
# ================================================================
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import (
    MapFunction, FilterFunction, FlatMapFunction,
    ReduceFunction, ProcessWindowFunction, KeyedProcessFunction
)
from pyflink.datastream.window import TumblingEventTimeWindows, SlidingEventTimeWindows
from pyflink.common.time import Time
from pyflink.datastream.state import ValueStateDescriptor
import json
import logging

logging.basicConfig(level=logging.INFO)

# ---- 1. MAP: JSON dönüşümü + özellik çıkarımı ----
class EventParserMap(MapFunction):
    """Kafka'dan gelen ham JSON string'i Python dict'ine çevirir."""
    def map(self, value):
        try:
            event = json.loads(value)
            # Türetilmiş özellik: toplam değer
            event['total_value'] = event.get('price', 0) * event.get('quantity', 1)
            return json.dumps(event)
        except json.JSONDecodeError:
            return None  # Bozuk veri filtre edilecek

# ---- 2. FILTER: Bozuk ve gereksiz olayları elee ----
class ValidEventFilter(FilterFunction):
    """Yalnızca geçerli ve anlamlı olayları akışta bırakır."""
    VALID_ACTIONS = {'purchase', 'add_to_cart', 'checkout', 'view_product'}

    def filter(self, value):
        if value is None:
            return False
        try:
            event = json.loads(value)
            return (
                event.get('action') in self.VALID_ACTIONS and
                event.get('price', 0) > 0 and
                event.get('user_id') is not None
            )
        except Exception:
            return False

# ---- 3. FLATMAP: Satın alma olayından birden fazla analiz üret ----
class PurchaseEventExpander(FlatMapFunction):
    """
    Her 'purchase' olayı için hem global hem de kullanıcı bazlı
    analiz mesajları üretir (bire-çok dönüşüm).
    """
    def flat_map(self, value):
        event = json.loads(value)
        if event.get('action') != 'purchase':
            yield value  # Diğer olaylar değişmeden geçsin
            return
        # Orijinal olay
        yield value
        # Kullanıcı segmentasyon mesajı
        segment_msg = {
            'type': 'user_segment_update',
            'user_id': event['user_id'],
            'segment': 'high_value' if event['total_value'] > 1000 else 'standard',
            'timestamp': event['timestamp']
        }
        yield json.dumps(segment_msg)

# ---- 4. REDUCE: Pencere içinde toplam harcama birikim ----
class RevenueReducer(ReduceFunction):
    """
    İki olay arasında toplam geliri biriktirir.
    S_t = f_reduce(S_{t-1}, x_t) kalıbını uygular.
    """
    def reduce(self, value1, value2):
        ev1 = json.loads(value1)
        ev2 = json.loads(value2)
        ev1['total_value'] = ev1.get('total_value', 0) + ev2.get('total_value', 0)
        ev1['event_count']  = ev1.get('event_count', 1) + 1
        return json.dumps(ev1)

# ---- 5. KEYED PROCESS FUNCTION: Fraud tespiti için stateful işlem ----
class FraudDetector(KeyedProcessFunction):
    """
    Kullanıcı başına son N işlemin toplamını takip eder.
    Belirli eşiği geçen kullanıcılar için fraud uyarısı üretir.
    """
    FRAUD_THRESHOLD = 5000.0  # 5000 birim üstü şüpheli
    WINDOW_SECONDS  = 300     # 5 dakikalık pencere

    def open(self, runtime_context):
        # Kullanıcı bazında birikimli harcama state'i
        self.total_spend = runtime_context.get_state(
            ValueStateDescriptor('user_spend', Types.DOUBLE())
        )
        # Son olay zamanı (pencere sıfırlama için)
        self.last_event_time = runtime_context.get_state(
            ValueStateDescriptor('last_event_time', Types.LONG())
        )

    def process_element(self, value, ctx):
        event = json.loads(value)
        current_time = ctx.timestamp() or int(event.get('timestamp', 0) * 1000)

        # Eski state'i al
        current_spend = self.total_spend.value() or 0.0
        last_time = self.last_event_time.value() or current_time

        # Pencere süresi dolduysa state'i sıfırla
        if (current_time - last_time) > self.WINDOW_SECONDS * 1000:
            current_spend = 0.0

        # State güncelle
        new_spend = current_spend + event.get('total_value', 0)
        self.total_spend.update(new_spend)
        self.last_event_time.update(current_time)

        # Fraud kontrol
        if new_spend > self.FRAUD_THRESHOLD:
            alert = {
                'alert_type':   'POTENTIAL_FRAUD',
                'user_id':      event['user_id'],
                'window_spend': new_spend,
                'threshold':    self.FRAUD_THRESHOLD,
                'timestamp':    event['timestamp']
            }
            yield json.dumps(alert)
        else:
            yield value

# ---- MAIN: Pipeline Tanımı ----
def build_pipeline():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    env.set_parallelism(4)  # 4 paralel görev

    # Checkpoint: exactly-once garantisi için
    env.enable_checkpointing(30000)  # Her 30sn checkpoint

    # Kafka Source
    kafka_props = {'bootstrap.servers': 'localhost:9092', 'group.id': 'flink_pipeline'}
    kafka_source = FlinkKafkaConsumer(
        topics='user_clickstream',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )
    kafka_source.set_start_from_latest()

    # Pipeline Zinciri
    stream = env.add_source(kafka_source)              \
        .map(EventParserMap(), output_type=Types.STRING())    \
        .filter(ValidEventFilter())                    \
        .flat_map(PurchaseEventExpander(), output_type=Types.STRING())

    # Key bazlı fraud tespiti (stateful)
    fraud_stream = stream \
        .key_by(lambda x: json.loads(x).get('user_id', 'unknown')) \
        .process(FraudDetector(), output_type=Types.STRING())

    # Tumbling Window ile 5 dakikalık gelir toplamı
    revenue_stream = stream \
        .filter(lambda x: json.loads(x).get('action') == 'purchase') \
        .key_by(lambda x: json.loads(x).get('category', 'unknown')) \
        .window(TumblingEventTimeWindows.of(Time.minutes(5))) \
        .reduce(RevenueReducer())

    # Sonuçları yazdır (gerçekte başka bir Kafka topic'e veya DB'e yazılır)
    fraud_stream.print()
    revenue_stream.print()

    env.execute('Ecommerce_Realtime_Analytics_Job')

if __name__ == '__main__':
    build_pipeline()

# ================================================================
# Kayan Pencere (Sliding Window) ile Fiyat Anomali Tespiti
# ================================================================
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import SlidingEventTimeWindows
from pyflink.datastream.functions import AggregateFunction, ProcessWindowFunction
from pyflink.common.time import Time
from pyflink.common.typeinfo import Types
import json, math

class PriceStatsAggregator(AggregateFunction):
    """
    Kayan penceredeki fiyat istatistiklerini online olarak toplar.
    Welford'un online varyans algoritmasını kullanır:
    M_k = M_{k-1} + (x_k - M_{k-1}) / k
    S_k = S_{k-1} + (x_k - M_{k-1}) * (x_k - M_k)
    Varyans = S_k / (k - 1)  [örneklem varyansı]
    """
    def create_accumulator(self):
        # (count, mean, M2, min, max)
        return (0, 0.0, 0.0, float('inf'), float('-inf'))

    def add(self, value, accumulator):
        event = json.loads(value)
        price = event.get('price', 0)
        count, mean, M2, mn, mx = accumulator
        count += 1
        delta  = price - mean
        mean  += delta / count
        delta2 = price - mean
        M2    += delta * delta2
        return (count, mean, M2, min(mn, price), max(mx, price))

    def get_result(self, accumulator):
        count, mean, M2, mn, mx = accumulator
        variance = M2 / (count - 1) if count > 1 else 0.0
        std_dev  = math.sqrt(variance)
        return json.dumps({
            'count':    count,
            'mean':     round(mean, 2),
            'std_dev':  round(std_dev, 2),
            'min':      mn,
            'max':      mx
        })

    def merge(self, acc1, acc2):
        # Welford'un paralel merge formülü
        c1, m1, M2_1, mn1, mx1 = acc1
        c2, m2, M2_2, mn2, mx2 = acc2
        count = c1 + c2
        if count == 0:
            return (0, 0.0, 0.0, float('inf'), float('-inf'))
        delta = m2 - m1
        mean  = (m1 * c1 + m2 * c2) / count
        M2    = M2_1 + M2_2 + delta**2 * c1 * c2 / count
        return (count, mean, M2, min(mn1, mn2), max(mx1, mx2))

class AnomalyWindowProcessor(ProcessWindowFunction):
    """
    Pencere istatistiklerine göre z-score tabanlı anomali tespiti.
    z = (x - μ) / σ ; |z| > 3 ise anomali (3-sigma kuralı)
    """
    ZSCORE_THRESHOLD = 3.0

    def process(self, key, context, elements, out):
        for stats_json in elements:
            stats = json.loads(stats_json)
            mean    = stats['mean']
            std_dev = stats['std_dev']
            if std_dev < 0.001:  # Tüm fiyatlar eşit, anomali yok
                continue
            # z-score ile eşik kontrolü
            upper_bound = mean + self.ZSCORE_THRESHOLD * std_dev
            lower_bound = mean - self.ZSCORE_THRESHOLD * std_dev
            result = {
                'category':     key,
                'window_start': context.window().start,
                'window_end':   context.window().end,
                'mean':         mean,
                'std_dev':      std_dev,
                'upper_3sigma': round(upper_bound, 2),
                'lower_3sigma': round(lower_bound, 2),
                **stats
            }
            out.collect(json.dumps(result))

def anomaly_pipeline():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    env.enable_checkpointing(15000)

    # 10 dakika uzunlukta, 2 dakikada bir kayan pencere
    stream = env.from_collection([], type_info=Types.STRING())

    result = stream \
        .key_by(lambda x: json.loads(x).get('category', 'unknown')) \
        .window(SlidingEventTimeWindows.of(
            Time.minutes(10),  # Pencere uzunluğu: L=10dk
            Time.minutes(2)    # Adım boyutu:     S=2dk
        )) \
        .aggregate(
            PriceStatsAggregator(),
            window_function=AnomalyWindowProcessor(),
            accumulator_type=Types.STRING(),
            output_type=Types.STRING()
        )

    result.print()
    env.execute('Price_Anomaly_Detection_Job')
