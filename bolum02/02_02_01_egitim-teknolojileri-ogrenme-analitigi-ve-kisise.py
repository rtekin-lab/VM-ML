# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 2
# Konum : BÖLÜM 2: VERİ MADENCİLİĞİNE GİRİŞ VE MATEMATİKSEL TEMELLER › 2.2. Gerçek Dünya Problemleri ve Veri Kaynakları › 2.2.1. Veri Bilimi ile Çözülebilecek Gerçek Dünya Problemleri › Eğitim Teknolojileri: Öğrenme Analitiği ve Kişiselleştirme
# Kitap  : Kod 2.11 (Öğrenme analitiği: öğrenci başarımının izlen)
# Dosya : bolum02/02_02_01_egitim-teknolojileri-ogrenme-analitigi-ve-kisise.py
# Gerekli: pip install pandas scikit-learn
# ==========================================================================
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Örnek öğrenci etkileşim verisi (Sentetik)
# Öznitelikler: Video izleme süresi, forum mesaj sayısı, ödev notu
data = {
    'video_izleme_saat': [12, 5, 18, 2, 25, 3, 15, 20, 1, 22],
    'forum_katilim': [5, 1, 10, 0, 15, 2, 8, 12, 0, 18],
    'odev_notu': [80, 40, 95, 20, 100, 30, 85, 90, 10, 98],
    'kurs_tamamlama': [1, 0, 1, 0, 1, 0, 1, 1, 0, 1]  # Hedef değişken
}

df = pd.DataFrame(data)

# Verinin bölümlenmesi
X = df.drop('kurs_tamamlama', axis=1)
y = df['kurs_tamamlama']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Modelinin Eğitilmesi
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Tahmin ve Performans Analizi
y_pred = model.predict(X_test)
print(f"Model Doğruluğu: {accuracy_score(y_test, y_pred):.2f}")
print("\nSınıflandırma Raporu:\n", classification_report(y_test, y_pred))
