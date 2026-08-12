# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 8
# Konum : BÖLÜM 8: BİRLİKTELİK KURALLARI VE TAVSİYE SİSTEMLERİ › 8.2. Tavsiye Sistemleri (Recommender Systems) › 8.2.3. Matris Faktörizasyonu (SVD): Seyrek Matrislerde Gizli Özellikleri Keşfetmek › 8.2.3.4. Bias (Sapmalar) ve Düzeltme › Python Uygulaması: Scipy ile SVD Tabanlı Tavsiye Sistemi
# Kitap  : Kod 8.3 (Kullanıcı ve öğe sapmalarının modele eklenme)
# Dosya : bolum08/08_02_03_04_python-uygulamasi-scipy-ile-svd-tabanli-tavsiye.py
# Gerekli: pip install numpy pandas scikit-learn scipy
# ==========================================================================
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error
from math import sqrt

# 1. Kullanıcı-Film Seyrek Puan Matrisi (0 = izlenmemiş)
# Gerçek sistemlerde bu matris milyonlarca satırdan oluşur
ratings_matrix = np.array([
    # Matrix  Yıldızl Inception Dövüş  Titanik  Marslı  Forrest
    [   5,      4,       5,        4,       0,       3,       0   ],  # Ali
    [   4,      5,       4,        0,       0,       4,       0   ],  # Ayşe
    [   5,      0,       5,        3,       2,       0,       0   ],  # Mehmet
    [   4,      4,       5,        0,       5,       3,       4   ],  # Zeynep
    [   0,      2,       0,        0,       5,       0,       5   ],  # Selin
    [   3,      0,       4,        5,       0,       4,       0   ],  # Hasan
], dtype=float)

film_names = ['Matrix','Yıldızlararası','Inception','Dövüş Kulübü',
              'Titanik','Marslı','Forrest Gump']
user_names = ['Ali','Ayşe','Mehmet','Zeynep','Selin','Hasan']

print('=== Orijinal Seyrek Matris (0 = izlenmemiş) ===')
print(pd.DataFrame(ratings_matrix, index=user_names, columns=film_names))

# 2. Normalizasyon: Her kullanıcının ortalama puanını çıkar (bias correction)
# Yalnızca izlenmiş filmler üzerinden ortalama hesapla
ratings_masked = np.where(ratings_matrix == 0, np.nan, ratings_matrix)
user_means = np.nanmean(ratings_masked, axis=1)

# Ortalama farkını sadece izlenen filmlere uygula
R_demeaned = ratings_matrix.copy()
for i in range(len(user_means)):
    R_demeaned[i, ratings_matrix[i] != 0] -= user_means[i]

# 3. SVD Uygulaması - k=3 gizli faktör
k = 3  # Gizli faktör sayısı (hiperparametre)
U, sigma, Vt = svds(R_demeaned, k=k)
sigma_diag = np.diag(sigma)

print(f'\n=== SVD Sonuçları (k={k}) ===')
print(f'U (Kullanıcı-Faktör): {U.shape}')
print(f'Sigma: {sigma}')
print(f'Vt (Faktör-Film): {Vt.shape}')

# 4. Tahmin Matrisi oluştur (bias'ı geri ekle)
all_predicted = np.dot(np.dot(U, sigma_diag), Vt) + user_means.reshape(-1, 1)

pred_df = pd.DataFrame(
    np.round(all_predicted, 2),
    index=user_names,
    columns=film_names
)
print('\n=== SVD Tahmin Matrisi (Tüm boşluklar dolduruldu) ===')
print(pred_df)

# 5. Kişiselleştirilmiş Öneri Fonksiyonu
def recommend_svd(kullanici_adi, pred_df, original_matrix, top_n=3):
    """
    SVD tahmin matrisine göre, kullanıcının daha önce izlemediği
    en yüksek tahmini puana sahip filmleri önerir.
    """
    user_idx = user_names.index(kullanici_adi)
    user_preds = pred_df.loc[kullanici_adi].copy()
    # Orijinal matriste 0 olan (izlenmemiş) filmleri filtrele
    unwatched_mask = original_matrix[user_idx] == 0
    recommendations = user_preds[unwatched_mask].sort_values(ascending=False)
    return recommendations.head(top_n)

print('\n=== Selin için Kişiselleştirilmiş SVD Önerileri ===')
print(recommend_svd('Selin', pred_df, ratings_matrix))

print('\n=== Mehmet için Kişiselleştirilmiş SVD Önerileri ===')
print(recommend_svd('Mehmet', pred_df, ratings_matrix))

# 6. Model Değerlendirmesi: RMSE hesapla
# Sadece orijinal matriste dolu olan değerleri karşılaştır
actual = ratings_masked.flatten()
predicted = all_predicted.flatten()
mask = ~np.isnan(actual)  # izlenmiş filmler
rmse = sqrt(mean_squared_error(actual[mask], predicted[mask]))
print(f'\n=== Model Değerlendirmesi ===')
print(f'Eğitim Seti RMSE: {rmse:.4f}')
print('(0 = mükemmel tahmin; gerçek sistemlerde 0.85-1.10 aralığı hedeflenir)')
