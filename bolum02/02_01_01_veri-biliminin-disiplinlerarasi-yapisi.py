# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.1. Veri Bilimi Nedir? Veri Madenciliği ile İlişkisi › 2.1.1. Veri Biliminin Tanımı ve Kapsamı › Veri Biliminin Disiplinlerarası Yapısı
# Kitap  : Kod 2.1 (NumPy ile veri matrisi ve öznitelik vektörle) · Kod 2.2 (Python listesi ile NumPy dizisinin başarım k) · Kod 2.3 (Matris işlemleri: çarpım, transpoz ve tersin)
# Dosya : bolum02/02_01_01_veri-biliminin-disiplinlerarasi-yapisi.py
# Gerekli: pip install numpy scipy
# ==========================================================================
# --- Uygulama Örneği 2.1.1: Temel İstatistiksel Hesaplamalar ---
import numpy as np
from scipy import stats

# 1. Veri Setinin Tanımlanması
# Bir grup öğrencinin sınav notlarını temsil eden örnek veri seti
data = np.array([23, 45, 56, 78, 90, 34, 67, 89, 12, 54])

# 2. Merkezi Eğilim Ölçüleri
# Verinin merkezini belirlemek için kullanılan hesaplamalar
mean_val   = np.mean(data)
median_val = np.median(data)
mode_res   = stats.mode(data, keepdims=True)
mode_val   = mode_res.mode[0]

# 3. Yayılım (Dağılım) Ölçüleri
# Verinin ne kadar geniş bir alana yayıldığını ölçen değerler
variance   = np.var(data)        # Varyans
std_dev    = np.std(data)        # Standart Sapma
data_range = np.ptp(data)        # Açıklık (Peak-to-Peak: Max - Min)

# 4. Çeyrekler ve IQR (Çeyrekler Açıklığı)
# Veriyi dört parçaya bölerek aykırı değer analizi için temel sağlar
q1  = np.percentile(data, 25)    # Birinci Çeyrek (%25)
q3  = np.percentile(data, 75)    # Üçüncü Çeyrek (%75)
iqr = q3 - q1                    # Çeyrekler Arası Fark

# 5. Sonuçların Raporlanması
print("--- Temel İstatistiksel Özet ---")
print(f"Aritmetik Ortalama : {mean_val:.2f}")
print(f"Medyan (Ortanca)   : {median_val:.2f}")
print(f"Mod (En Çok Tekrar): {mode_val}")
print(f"Varyans            : {variance:.2f}")
print(f"Standart Sapma     : {std_dev:.2f}")
print(f"Açıklık (Range)    : {data_range}")
print(f"IQR (Interquartile): {iqr:.2f}")

# --- Uygulama Örneği 2.1.2: Veri Yapıları ve Performans ---
import time
import numpy as np

# --- 1. Liste ve NumPy Array Performans Karşılaştırması ---
n = 1_000_000  # İşlem yapılacak eleman sayısı

# A. Standart Python Listesi ile İşlem
start = time.time()
python_list = list(range(n))
result_list = [x**2 for x in python_list]
list_time = time.time() - start

# B. NumPy Array ile Vektörel İşlem
start = time.time()
numpy_array = np.arange(n)
result_array = numpy_array**2
numpy_time = time.time() - start

# Performans Sonuçlarının Raporlanması
print(f"Liste süresi  : {list_time:.4f} saniye")
print(f"NumPy süresi  : {numpy_time:.4f} saniye")
print(f"Hız artışı    : {list_time/numpy_time:.2f}x")

print("-" * 35)

# --- 2. Karma Tablo (Hash Table) Kullanımı ---
# Sözlük yapıları O(1) zaman karmaşıklığı ile veri erişimi sağlar.
user_data = {
    'user_001': {'name': 'Ali', 'age': 25, 'city': 'İstanbul'},
    'user_002': {'name': 'Ayşe', 'age': 30, 'city': 'Ankara'},
    'user_003': {'name': 'Mehmet', 'age': 35, 'city': 'İzmir'}
}

# Sabit Zamanlı (Constant Time) Veri Erişimi
user = user_data.get('user_002')
print(f"Kullanıcı bilgisi (user_002): {user}")

# --- Uygulama Örneği 2.1.3: Doğrusal Cebir İşlemleri ---
import numpy as np
from numpy.linalg import eig, inv, norm

# --- 1. Matris Tanımlama ---
A = np.array([[4, 2],
              [1, 3]])

B = np.array([[1, 0],
              [0, 2]])

# --- 2. Temel Matris İşlemleri ---
C = np.dot(A, B)      # Matris çarpımı (A × B)
A_inv = inv(A)        # Ters matris (Inverse)
A_T = A.T             # Transpoz (Devrik)

print("Matris A:")
print(A)
print("\nMatris Çarpımı (A × B):")
print(C)

# --- 3. Özdeğer ve Özvektör Analizi ---
eigenvalues, eigenvectors = eig(A)
print(f"\nÖzdeğerler: {eigenvalues}")
print(f"Özvektörler:\n{eigenvectors}")

# --- 4. Vektör İşlemleri ---
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

dot_product = np.dot(v1, v2)      # Nokta Çarpım (Skaler)
cross_product = np.cross(v1, v2)  # Çapraz Çarpım (Vektörel)
v1_norm = norm(v1)                # Vektör Uzunluğu (Öklid Normu)

print(f"\nNokta Çarpımı: {dot_product}")
print(f"Çapraz Çarpım: {cross_product}")
print(f"v1'in Normu: {v1_norm:.2f}")
