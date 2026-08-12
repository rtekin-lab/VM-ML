# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.6. İleri Düzey Özellikler: Subplots, Facets, Animations
# Kitap  : Kod 4.21 (Alt grafik, panel ve animasyon özellikleri)
# Dosya : bolum04/04_03_06_ileri-duzey-ozellikler-subplots-facets-animation.py
# Gerekli: pip install numpy pandas plotly
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

np.random.seed(42)

# ════════════════════════════════════════════════════════════════════════════
# A. MAKE_SUBPLOTS — Heterojen Alt Grafik Düzeni
# ════════════════════════════════════════════════════════════════════════════

fig1 = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Zaman Serisi', 'Scatter', 'Histogram', 'Box'),
    specs=[
        [{"type": "scatter"}, {"type": "scatter"}],
        [{"type": "histogram"}, {"type": "box"}]
    ]
)

# [1,1] Zaman serisi
t = np.linspace(0, 4*np.pi, 300)
fig1.add_trace(go.Scatter(x=t, y=np.sin(t), name='sin(t)', line=dict(color='#1E3A5F')),
               row=1, col=1)

# [1,2] Scatter
x_s = np.random.randn(200)
y_s = 0.5*x_s + np.random.randn(200)*0.3
fig1.add_trace(go.Scatter(x=x_s, y=y_s, mode='markers', name='Scatter',
                          marker=dict(color='#2E5F8A', size=5)),
               row=1, col=2)

# [2,1] Histogram
data_h = np.concatenate([np.random.normal(-1, 0.5, 150),
                         np.random.normal(2, 0.8, 150)])
fig1.add_trace(go.Histogram(x=data_h, name='Histogram',
                            marker=dict(color='#5B8DB8')),
               row=2, col=1)

# [2,2] Box
kategoriler = ['A', 'B', 'C', 'D']
veri_box = [np.random.normal(i*2, 1, 100) for i in range(4)]
for i, kat in enumerate(kategoriler):
    fig1.add_trace(go.Box(y=veri_box[i], name=kat, marker=dict(color='#A8C6E8')),
                   row=2, col=2)

fig1.update_layout(title_text="make_subplots: Heterojen Düzen", height=700, showlegend=False)
fig1.write_html(os.path.join(tempfile.gettempdir(), "subplots_heterojen.html"))
print("Subplots (heterojen): /tmp/subplots_heterojen.html")

# ════════════════════════════════════════════════════════════════════════════
# B. FACET — Kıtalara Göre Ayrılmış Scatter Matrix
# ════════════════════════════════════════════════════════════════════════════

# Veri seti
ulkeler = ['ABD', 'Çin', 'Japonya', 'Almanya', 'Hindistan', 'İngiltere',
           'Fransa', 'Brezilya', 'İtalya', 'Kanada']
kitalar = ['Amerika', 'Asya', 'Asya', 'Avrupa', 'Asya', 'Avrupa',
           'Avrupa', 'Amerika', 'Avrupa', 'Amerika']
gsyih   = np.random.uniform(1, 20, 10)
nufus   = np.random.uniform(50, 1400, 10)
omur    = np.random.uniform(70, 85, 10)

df_facet = pd.DataFrame({
    'Ülke': ulkeler, 'Kıta': kitalar,
    'GSYİH': gsyih, 'Nüfus': nufus, 'Ömür': omur
})

fig2 = px.scatter(df_facet, x='GSYİH', y='Ömür', size='Nüfus',
                  color='Kıta', hover_name='Ülke',
                  facet_col='Kıta',  # Kıtalara göre paneller
                  title='GSYİH vs Ömür (Facet: Kıtalara Göre Paneller)')

fig2.update_layout(height=400)
fig2.write_html(os.path.join(tempfile.gettempdir(), "facet_kita.html"))
print("Facet (kıta): /tmp/facet_kita.html")

# ════════════════════════════════════════════════════════════════════════════
# C. ANIMATION — Gapminder Tarzı Animasyonlu Bubble Chart
# ════════════════════════════════════════════════════════════════════════════

# Çok yıllı veri
yillar = list(range(2000, 2021))
df_anim_list = []
for yil in yillar:
    for ulke, kita in zip(ulkeler, kitalar):
        df_anim_list.append({
            'Yıl': yil,
            'Ülke': ulke,
            'Kıta': kita,
            'GSYİH': np.random.uniform(1, 20) * (1 + (yil-2000)*0.03),
            'Nüfus': np.random.uniform(50, 1400),
            'Ömür': np.random.uniform(72, 85)
        })

df_anim = pd.DataFrame(df_anim_list)

fig3 = px.scatter(df_anim, x='GSYİH', y='Ömür', size='Nüfus',
                  color='Kıta', hover_name='Ülke',
                  animation_frame='Yıl',  # Animasyon kareleri
                  size_max=60, range_x=[0, 25], range_y=[70, 88],
                  title='Animasyonlu Bubble Chart: GSYİH vs Ömür (2000-2020)')

fig3.update_layout(
    transition={'duration': 800},
    height=600
)
fig3.write_html(os.path.join(tempfile.gettempdir(), "animation_bubble.html"))
print("Animation (bubble): /tmp/animation_bubble.html")

# ════════════════════════════════════════════════════════════════════════════
# D. SUNBURST — Hiyerarşik Veri Görselleştirme
# ════════════════════════════════════════════════════════════════════════════

# Şirket organizasyon hiyerarşisi
df_sunburst = pd.DataFrame({
    'Etiket': ['Şirket',
               'Mühendislik', 'Pazarlama', 'Satış',
               'Backend', 'Frontend', 'DevOps',
               'Dijital', 'Marka',
               'B2B', 'B2C'],
    'Üst': ['',
            'Şirket', 'Şirket', 'Şirket',
            'Mühendislik', 'Mühendislik', 'Mühendislik',
            'Pazarlama', 'Pazarlama',
            'Satış', 'Satış'],
    'Değer': [0,
              0, 0, 0,
              50, 40, 30,
              35, 25,
              60, 45]
})

fig4 = px.sunburst(df_sunburst, names='Etiket', parents='Üst', values='Değer',
                   title='Sunburst: Şirket Organizasyon Hiyerarşisi',
                   color='Değer', color_continuous_scale='RdBu')

fig4.update_layout(height=600)
fig4.write_html(os.path.join(tempfile.gettempdir(), "sunburst_org.html"))
print("Sunburst (hiyerarşi): /tmp/sunburst_org.html")

print("\nTüm ileri düzey özellikler oluşturuldu.")
