# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 8
# Konum : BÖLÜM 8: BİRLİKTELİK KURALLARI VE TAVSİYE SİSTEMLERİ › 8.2. Tavsiye Sistemleri (Recommender Systems) › 8.2.3. Matris Faktörizasyonu (SVD): Seyrek Matrislerde Gizli Özellikleri Keşfetmek › 8.2.3.5. surprise Kütüphanesi ile Gelişmiş SVD
# Kitap  : Kod 8.4 (scikit-surprise kurulumu)
# Dosya : bolum08/08_02_03_05_surprise-kutuphanesi-ile-gelismis-svd.py
# Gerekli: pip install pandas scikit-surprise
# ==========================================================================
# pip install scikit-surprise
from surprise import SVD, SVDpp, Dataset, Reader, accuracy
from surprise.model_selection import cross_validate, train_test_split, GridSearchCV
import pandas as pd

# 1. Veri Hazırlama
ratings_dict = {
    'itemID': ['Matrix','Matrix','Matrix','Inception','Inception',
               'Yıldızlararası','Yıldızlararası','Titanik','Titanik','Marslı'],
    'userID': ['Ali','Ayşe','Mehmet','Ali','Zeynep',
               'Ayşe','Zeynep','Selin','Zeynep','Ali'],
    'rating': [5, 4, 5, 5, 5, 5, 4, 5, 5, 3]
}
df = pd.DataFrame(ratings_dict)

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

# 2. SVD Modeli - 5 katlı çapraz doğrulama
svd_model = SVD(n_factors=50, n_epochs=20, lr_all=0.005, reg_all=0.02)
results = cross_validate(svd_model, data, measures=['RMSE', 'MAE'],
                          cv=5, verbose=True)

print(f'Ortalama RMSE: {results["test_rmse"].mean():.4f}')
print(f'Ortalama MAE : {results["test_mae"].mean():.4f}')

# 3. SVD++ (daha gelişmiş: örtük geri bildirimi de kullanır)
svdpp_model = SVDpp(n_factors=20, n_epochs=20)
results_pp = cross_validate(svdpp_model, data, measures=['RMSE'], cv=3)
print(f'\nSVD++ Ortalama RMSE: {results_pp["test_rmse"].mean():.4f}')

# 4. Hiperparametre Optimizasyonu
param_grid = {
    'n_factors': [20, 50, 100],
    'n_epochs': [10, 20],
    'lr_all': [0.002, 0.005],
    'reg_all': [0.02, 0.1]
}
gs = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3)
gs.fit(data)
print(f'\nEn iyi RMSE: {gs.best_score["rmse"]:.4f}')
print(f'En iyi parametreler: {gs.best_params["rmse"]}')

# 5. Eğitilmiş modelle tahmin üretme
trainset = data.build_full_trainset()
svd_model.fit(trainset)

# Zeynep'in Marslı'ya vereceği tahmini puanı hesapla
pred = svd_model.predict(uid='Zeynep', iid='Marslı', verbose=True)
print(f'\nZeynep - Marslı tahmini puan: {pred.est:.2f}')
