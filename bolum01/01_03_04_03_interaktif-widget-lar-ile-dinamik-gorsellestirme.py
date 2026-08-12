# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 1
# Konum : BÖLÜM 1: Python Ortamının Hazırlanması ve Temel Python Konuları › 1.3. Alternatif Geliştirme Ortamları › 1.3.4. JupyterLab ve Jupyter Notebook › 1.3.4.3. Interaktif Widget'lar ile Dinamik Görselleştirme
# Kitap  : Kod 1.76 (Ipywidgets ile interaktif parametre keslifi )
# Dosya : bolum01/01_03_04_03_interaktif-widget-lar-ile-dinamik-gorsellestirme.py
# Gerekli: pip install ipywidgets matplotlib numpy scikit-learn
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, interactive
from IPython.display import display

# ─── Ornek 1: Basit @interact dekoratoru ─────────────────────────
@interact(
    frekans=widgets.FloatSlider(min=0.1, max=5.0, step=0.1, value=1.0),
    genlik  =widgets.FloatSlider(min=0.1, max=3.0, step=0.1, value=1.0),
    faz     =widgets.FloatSlider(min=0.0, max=6.28, step=0.1, value=0.0),
)
def sinüs_grafigi(frekans, genlik, faz):
    t = np.linspace(0, 4*np.pi, 1000)
    y = genlik * np.sin(frekans * t + faz)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, y, color="#2E75B6", linewidth=2)
    ax.set_xlabel("t"); ax.set_ylabel("y")
    ax.set_title(f"y = {genlik:.1f} sin({frekans:.1f}t + {faz:.1f})")
    ax.grid(True, alpha=0.3)
    plt.show()

# ─── Ornek 2: Polinom Derecesi Secimine Gore Karsılaştirma ───────
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

np.random.seed(42)
X = np.linspace(-3, 3, 100)
y = 0.5*X**3 - X**2 + 2*X + np.random.normal(0, 1.5, 100)

@interact(derece=widgets.IntSlider(min=1, max=10, step=1, value=3))
def polinom_uyum(derece):
    pipe = Pipeline([
        ("poly", PolynomialFeatures(degree=derece)),
        ("lr",   LinearRegression())
    ])
    pipe.fit(X.reshape(-1,1), y)
    y_pred = pipe.predict(X.reshape(-1,1))
    r2 = r2_score(y, y_pred)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(X, y, alpha=0.5, s=20, color="#e74c3c", label="Gercek")
    ax.plot(X, y_pred, color="#2E75B6", lw=2, label=f"Derece={derece} (R²={r2:.3f})")
    ax.legend(); ax.set_title(f"Polinom Regresyon (Derece={derece})")
    ax.grid(True, alpha=0.3); plt.show()
