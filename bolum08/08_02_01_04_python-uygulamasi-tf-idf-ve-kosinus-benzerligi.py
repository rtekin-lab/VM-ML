# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 8
# Konum : BÖLÜM 8: BİRLİKTELİK KURALLARI VE TAVSİYE SİSTEMLERİ › 8.2. Tavsiye Sistemleri (Recommender Systems) › 8.2.1. İçerik Tabanlı (Content-Based) Filtreleme › 8.2.1.4. Python Uygulaması: TF-IDF ve Kosinüs Benzerliği
# Dosya : bolum08/08_02_01_04_python-uygulamasi-tf-idf-ve-kosinus-benzerligi.py
# Gerekli: pip install pandas scikit-learn
# ==========================================================================
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Örnek Film Veri Seti
movies = pd.DataFrame({
    'film_adi': ['Matrix', 'Yıldızlararası', 'Inception', 'Titanik',
                  'Şaşkın Aşıklar', 'Dövüş Kulübü', 'Marslı', 'Forrest Gump'],
    'aciklama': [
        'yapay zeka simülasyon felsefe aksiyon bilim kurgu hacker',
        'uzay kara delik boyutlar aşk bilim kurgu zaman yolculuğu astronot',
        'rüya bilinçaltı psikoloji aksiyon bilim kurgu hırsız fikir',
        'aşk gemi trajedi tarih romantizm felaket okyanus',
        'romantik komedi aşk Türkiye İstanbul ilişki güldürü',
        'kimlik psikoloji şiddet toplum erkeklik çatışma gerilim',
        'uzay Mars astronot hayatta kalma bilim akılcı problem çözme',
        'saf aşk arkadaşlık tarih ABD Vietnam engel aşma drama',
    ],
    'tur': ['Bilim Kurgu/Aksiyon', 'Bilim Kurgu/Drama', 'Bilim Kurgu/Aksiyon',
             'Romantik/Drama', 'Romantik Komedi', 'Gerilim/Dram',
             'Bilim Kurgu/Drama', 'Drama']
})

# 2. TF-IDF Vektörizasyonu
tfidf = TfidfVectorizer(min_df=1, stop_words=None)
tfidf_matrix = tfidf.fit_transform(movies['aciklama'])
print(f'TF-IDF Matris boyutu: {tfidf_matrix.shape}')
# (8 film, X kelime) şeklinde bir matris oluşur

# 3. Kosinüs Benzerlik Matrisini hesapla
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print('Kosinüs Benzerlik Matrisi:')
sim_df = pd.DataFrame(cosine_sim, index=movies['film_adi'],
                       columns=movies['film_adi'])
print(sim_df.round(3))

# 4. Bir filme göre benzer filmleri tavsiye eden fonksiyon
def get_content_recommendations(film_adi, cosine_sim=cosine_sim,
                                  df=movies, n=3):
    """Verilen film adına göre en benzer N filmi döndürür."""
    idx = df[df['film_adi'] == film_adi].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]  # Kendisi hariç ilk n film
    film_indices = [i[0] for i in sim_scores]
    return df[['film_adi', 'tur']].iloc[film_indices].assign(
        benzerlik_skoru=[round(s[1], 4) for s in sim_scores])

# 5. Test: 'Matrix' filmine benzer filmler
print('\n=== Matrix izlediyseniz önerilir ===')
print(get_content_recommendations('Matrix', n=3))

print('\n=== Yıldızlararası izlediyseniz önerilir ===')
print(get_content_recommendations('Yıldızlararası', n=3))
