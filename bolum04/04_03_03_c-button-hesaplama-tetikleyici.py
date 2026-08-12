# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.3. İnteraktif Kontroller: Slider, Dropdown, Button › C. Button (Düğme): Hesaplama Tetikleyici
# Dosya : bolum04/04_03_03_c-button-hesaplama-tetikleyici.py
# Gerekli: pip install numpy plotly
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import pandas as pd
import random
import plotly.graph_objects as go
import numpy as np

# ════════════════════════════════════════════════════════════════════════════
# A. SLIDER — Sinyal Frekans Kontrolü
# ════════════════════════════════════════════════════════════════════════════

t = np.linspace(0, 2*np.pi, 500)

# Her frekans için bir trace oluştur (başlangıçta sadece biri görünür)
traces = []
for f in range(1, 11):  # 1 Hz'den 10 Hz'e
    traces.append(go.Scatter(
        x=t, y=np.sin(f * t),
        mode='lines', name=f'{f} Hz',
        visible=(f == 1),  # Sadece ilk trace başlangıçta görünür
        line=dict(color='#1E3A5F', width=2.5)
    ))

fig1 = go.Figure(data=traces)

# Slider adımları oluştur
steps = []
for i, f in enumerate(range(1, 11)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(traces)},  # Tüm trace'leri gizle
              {"title": f"Sinyal Frekansı: {f} Hz"}],
        label=f"{f} Hz"
    )
    step["args"][0]["visible"][i] = True  # Sadece i. trace'i göster
    steps.append(step)

sliders = [dict(
    active=0,
    yanchor="top", y=0.99,
    xanchor="left", x=0.01,
    currentvalue=dict(prefix="Frekans: ", font=dict(size=14)),
    pad=dict(b=10, t=50),
    len=0.9,
    steps=steps
)]

fig1.update_layout(
    sliders=sliders,
    title="Sinyal Frekans Kontrolü (Slider) — y = sin(f·t)",
    xaxis=dict(title='t (radyan)', range=[0, 2*np.pi]),
    yaxis=dict(title='Genlik', range=[-1.1, 1.1]),
    height=500
)
fig1.write_html(os.path.join(tempfile.gettempdir(), "slider_freq.html"))
print("Slider grafiği: /tmp/slider_freq.html")

# ════════════════════════════════════════════════════════════════════════════
# B. DROPDOWN — Fonksiyon Seçici
# ════════════════════════════════════════════════════════════════════════════

x = np.linspace(-5, 5, 300)
fonksiyonlar = {
    'sin(x)':     np.sin(x),
    'cos(x)':     np.cos(x),
    'exp(-x²/2)': np.exp(-x**2/2),
    'tanh(x)':    np.tanh(x),
    'x²':         x**2,
}

fig2 = go.Figure()

# Tüm fonksiyonları ekle (başlangıçta sadece biri görünür)
for i, (isim, y) in enumerate(fonksiyonlar.items()):
    fig2.add_trace(go.Scatter(
        x=x, y=y, mode='lines', name=isim,
        visible=(i == 0),
        line=dict(width=2.5)
    ))

# Dropdown menü düğmeleri
buttons = []
for i, isim in enumerate(fonksiyonlar.keys()):
    button = dict(
        label=isim,
        method="update",
        args=[{"visible": [j == i for j in range(len(fonksiyonlar))]},
              {"title": f"Fonksiyon: {isim}"}]
    )
    buttons.append(button)

fig2.update_layout(
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        pad=dict(r=10, t=10),
        showactive=True,
        x=0.01, xanchor="left",
        y=1.15, yanchor="top"
    )],
    title="Matematiksel Fonksiyon Seçici (Dropdown)",
    xaxis=dict(title='x', zeroline=True),
    yaxis=dict(title='f(x)', zeroline=True),
    height=500
)
fig2.write_html(os.path.join(tempfile.gettempdir(), "dropdown_func.html"))
print("Dropdown grafiği: /tmp/dropdown_func.html")

# ════════════════════════════════════════════════════════════════════════════
# C. BUTTON — Ölçek Değiştirici (Log/Linear)
# ════════════════════════════════════════════════════════════════════════════

x_exp = np.linspace(0.1, 5, 100)
y_exp = np.exp(x_exp)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=x_exp, y=y_exp, mode='lines+markers',
                          line=dict(color='#2E5F8A', width=2.5),
                          marker=dict(size=4)))

# Butonlar: Linear vs Log ölçeği
fig3.update_layout(
    updatemenus=[dict(
        type="buttons",
        direction="left",
        buttons=[
            dict(label="Linear Y", method="relayout",
                 args=[{"yaxis.type": "linear"}]),
            dict(label="Log Y", method="relayout",
                 args=[{"yaxis.type": "log"}])
        ],
        pad=dict(r=10, t=10),
        showactive=True,
        x=0.01, xanchor="left",
        y=1.15, yanchor="top"
    )],
    title="Üstel Büyüme: y = e^x (Button ile Ölçek Değiştirme)",
    xaxis=dict(title='x'),
    yaxis=dict(title='y = e^x'),
    height=500
)
fig3.write_html(os.path.join(tempfile.gettempdir(), "button_scale.html"))
print("Button grafiği: /tmp/button_scale.html")

# ════════════════════════════════════════════════════════════════════════════
# D. RANGESLIDER — Zaman Serisi Zoom ve Pan
# ════════════════════════════════════════════════════════════════════════════

tarihler = pd.date_range('2020-01-01', periods=365*2, freq='D')
np.random.seed(42)
hisse = 100 * np.exp(np.cumsum(np.random.randn(len(tarihler)) * 0.02))

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=tarihler, y=hisse, mode='lines',
                          line=dict(color='#1E3A5F', width=1.5),
                          fill='tozeroy', fillcolor='rgba(30,58,95,0.1)'))

fig4.update_xaxes(
    rangeslider=dict(visible=True, thickness=0.05),  # Alt kısımda range slider
    rangeselector=dict(
        buttons=[
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all", label="Tümü")
        ],
        x=0.01, y=1.05, xanchor="left", yanchor="top"
    )
)

fig4.update_layout(
    title="Hisse Senedi Fiyatı (RangeSlider + RangeSelector)",
    xaxis=dict(title='Tarih'),
    yaxis=dict(title='Fiyat ($)'),
    hovermode='x unified',
    height=600
)
fig4.write_html(os.path.join(tempfile.gettempdir(), "rangeslider_timeseries.html"))
print("RangeSlider grafiği: /tmp/rangeslider_timeseries.html")

print("\nTüm interaktif kontroller oluşturuldu.")
