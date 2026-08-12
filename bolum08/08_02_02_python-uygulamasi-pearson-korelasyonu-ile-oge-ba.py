# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 8
# Konum : BÖLÜM 8: BİRLİKTELİK KURALLARI VE TAVSİYE SİSTEMLERİ › 8.2. Tavsiye Sistemleri (Recommender Systems) › 8.2.2. İşbirlikçi (Collaborative) Filtreleme › 8.2.2.B. Öğe Bazlı (Item-Based) İşbirlikçi Filtreleme (Amazon Modeli) › Python Uygulaması: Pearson Korelasyonu ile Öğe Bazlı Filtreleme
# Dosya : bolum08/08_02_02_python-uygulamasi-pearson-korelasyonu-ile-oge-ba.py
# Gerekli: pip install numpy pandas
# ==========================================================================
import pandas as pd
import numpy as np

# 1. Kullanıcı-Film Puan Veri Seti
ratings_data = {
    'kullanici': ['Ali','Ali','Ali','Ali','Ali',
                  'Ayşe','Ayşe','Ayşe','Ayşe',
                  'Mehmet','Mehmet','Mehmet','Mehmet',
                  'Zeynep','Zeynep','Zeynep','Zeynep','Zeynep'],
    'film': ['Matrix','Yıldızlararası','Inception','Dövüş Kulübü','Marslı',
              'Matrix','Yıldızlararası','Inception','Marslı',
              'Matrix','Inception','Dövüş Kulübü','Titanik',
              'Matrix','Yıldızlararası','Inception','Marslı','Titanik'],
    'puan': [5, 4, 5, 4, 3,
             4, 5, 4, 4,
             5, 5, 3, 2,
             4, 4, 5, 3, 5]
}

df = pd.DataFrame(ratings_data)

# 2. Fayda Matrisi: Satırlar=Kullanıcılar, Sütunlar=Filmler
movie_matrix = df.pivot_table(index='kullanici',
                               columns='film', values='puan')
print('=== Fayda Matrisi ===')
print(movie_matrix)

# 3. Öğe Bazlı Benzerlik: 'corrwith' ile Pearson Korelasyonu
def get_item_based_recommendations(film_adi, movie_matrix, n=3):
    """
    Belirtilen film ile tüm diğer filmler arasındaki
    Pearson Korelasyonunu hesaplar ve en benzer n filmi döndürür.
    """
    film_ratings = movie_matrix[film_adi]
    # corrwith: film_ratings vektörü ile diğer tüm sütunlar arasındaki korelasyon
    similar = movie_matrix.corrwith(film_ratings)
    corr_df = pd.DataFrame(similar, columns=['Korelasyon'])
    corr_df = corr_df.dropna()
    corr_df = corr_df[corr_df.index != film_adi]  # Kendisi hariç
    return corr_df.sort_values(by='Korelasyon', ascending=False).head(n)

# 4. Test
print('\n=== Matrix izleyenler ne izler? ===')
print(get_item_based_recommendations('Matrix', movie_matrix))

print('\n=== Titanik izleyenler ne izler? ===')
print(get_item_based_recommendations('Titanik', movie_matrix))

# 5. Belirli bir kullanıcı için kişiselleştirilmiş öneri
def recommend_for_user(kullanici_adi, movie_matrix, n_sim=2, top_n=3):
    """
    Kullanıcının izlediği filmlere benzer,
    henüz izlemediği filmleri önerir.
    """
    user_ratings = movie_matrix.loc[kullanici_adi].dropna()
    watched = set(user_ratings.index)
    all_films = set(movie_matrix.columns)
    unwatched = all_films - watched

    scores = {}
    for film in watched:
        similar_films = movie_matrix.corrwith(movie_matrix[film])
        similar_films = similar_films.dropna()
        for sim_film, sim_score in similar_films.items():
            if sim_film in unwatched:
                if sim_film not in scores:
                    scores[sim_film] = 0
                scores[sim_film] += sim_score * user_ratings[film]

    return pd.Series(scores).sort_values(ascending=False).head(top_n)

print(f'\n=== Ayşe için Kişiselleştirilmiş Öneriler ===')
print(recommend_for_user('Ayşe', movie_matrix))
