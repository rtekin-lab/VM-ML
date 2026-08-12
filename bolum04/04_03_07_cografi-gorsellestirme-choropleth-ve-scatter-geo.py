# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.7. Coğrafi Görselleştirme: Choropleth ve Scatter Geo
# Kitap  : Kod 4.22 (Coğrafi görselleştirme: choropleth ve scatte)
# Dosya : bolum04/04_03_07_cografi-gorsellestirme-choropleth-ve-scatter-geo.py
# Gerekli: pip install numpy pandas plotly
# ==========================================================================
# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
# ════════════════════════════════════════════════════════════════════════════
# A. CHOROPLETH — Ülke Bazlı Renklendirme
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
# Ülke verileri (ISO alpha-3 kodları)
ulke_verisi = pd.DataFrame({
    'iso_code': ['USA', 'CHN', 'JPN', 'DEU', 'IND', 'GBR', 'FRA', 'BRA',
                 'ITA', 'CAN', 'KOR', 'RUS', 'AUS', 'ESP', 'MEX', 'IDN'],
    'ulke': ['ABD', 'Çin', 'Japonya', 'Almanya', 'Hindistan', 'İngiltere',
             'Fransa', 'Brezilya', 'İtalya', 'Kanada', 'Güney Kore',
             'Rusya', 'Avustralya', 'İspanya', 'Meksika', 'Endonezya'],
    'gsyih': [21.4, 14.7, 5.1, 4.0, 2.9, 2.8, 2.8, 1.6, 2.0, 1.7,
              1.6, 1.5, 1.3, 1.4, 1.1, 1.0],  # Trilyon $
    'nufus': [331, 1411, 126, 83, 1380, 67, 65, 212, 60, 38,
              51, 146, 25, 47, 128, 273]  # Milyon
})

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
fig1 = px.choropleth(ulke_verisi,
                     locations='iso_code',
                     color='gsyih',
                     hover_name='ulke',
                     hover_data={'gsyih': ':.2f', 'nufus': ':,'},
                     color_continuous_scale='Viridis',
                     labels={'gsyih': 'GSYİH (Trilyon $)'},
                     title='Dünya GSYİH Haritası (Choropleth)')

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
fig1.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    ),
    height=500
)
fig1.write_html(os.path.join(tempfile.gettempdir(), "choropleth_world.html"))
print("Choropleth (dünya): /tmp/choropleth_world.html")

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
# ════════════════════════════════════════════════════════════════════════════
# B. SCATTER GEO — Şehir Koordinatları ve Nüfus
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
sehirler = pd.DataFrame({
    'Şehir': ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya',
              'Adana', 'Gaziantep', 'Konya', 'Mersin', 'Kayseri'],
    'Enlem': [41.0082, 39.9334, 38.4237, 40.1826, 36.8969,
              37.0000, 37.0662, 37.8746, 36.8121, 38.7312],
    'Boylam': [28.9784, 32.8597, 27.1428, 29.0665, 30.7133,
               35.3213, 37.3833, 32.4932, 34.6415, 35.4787],
    'Nüfus': [15.5, 5.7, 4.4, 3.1, 2.5, 2.2, 2.1, 2.2, 1.9, 1.4],  # Milyon
    'Bölge': ['Marmara', 'İç Anadolu', 'Ege', 'Marmara', 'Akdeniz',
              'Akdeniz', 'Güneydoğu', 'İç Anadolu', 'Akdeniz', 'İç Anadolu']
})

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
fig2 = px.scatter_geo(sehirler,
                      lat='Enlem', lon='Boylam',
                      size='Nüfus', color='Bölge',
                      hover_name='Şehir',
                      hover_data={'Nüfus': ':.1f', 'Enlem': ':.4f', 'Boylam': ':.4f'},
                      size_max=40,
                      title='Türkiye Büyük Şehirler (Scatter Geo)')

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
fig2.update_geos(
    projection_type="mercator",
    lataxis_range=[35, 43],
    lonaxis_range=[25, 45],
    showcountries=True, countrycolor="lightgray",
    showland=True, landcolor="#F0F0F0",
    showocean=True, oceancolor="#E0F2F7",
    showlakes=True, lakecolor="#E0F2F7"
)

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
fig2.update_layout(height=600)
fig2.write_html(os.path.join(tempfile.gettempdir(), "scatter_geo_turkey.html"))
print("Scatter Geo (Türkiye): /tmp/scatter_geo_turkey.html")

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
# ════════════════════════════════════════════════════════════════════════════
# C. SCATTER MAPBOX — OpenStreetMap Temel Harita
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
# Not: Mapbox token gerektirir (ücretsiz hesap: mapbox.com)
# Bu örnek token olmadan çalışır (open-street-map stili ile)

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
fig3 = go.Figure(go.Scattermapbox(
    lat=sehirler['Enlem'],
    lon=sehirler['Boylam'],
    mode='markers+text',
    marker=dict(size=sehirler['Nüfus']*3, color='red', opacity=0.7),
    text=sehirler['Şehir'],
    textposition="top center",
    hovertemplate='<b>%{text}</b><br>Nüfus: %{marker.size:.1f}M<extra></extra>'
))

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
fig3.update_layout(
    mapbox=dict(
        style="open-street-map",  # Mapbox token gerektirmeyen stil
        center=dict(lat=39, lon=35),
        zoom=5
    ),
    title='Türkiye Şehirleri (Mapbox)',
    height=600
)
fig3.write_html(os.path.join(tempfile.gettempdir(), "mapbox_turkey.html"))
print("Mapbox (Türkiye): /tmp/mapbox_turkey.html")

# --- ▌ Kod Örneği 4.3.7 — Choropleth Harita ve Scatter Geo ---
print("\nTüm coğrafi görselleştirmeler oluşturuldu.")
