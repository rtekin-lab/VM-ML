# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.2. Temel İnteraktif Grafikler: Express vs Graph Objects › B. Graph Objects: İmperatif Kontrol
# Kitap  : Kod 4.20 (Graph Objects ile imperatif grafik kurulumu)
# Dosya : bolum04/04_03_02_b-graph-objects-imperatif-kontrol.py
# Gerekli: pip install numpy pandas plotly
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

np.random.seed(42)

# ════════════════════════════════════════════════════════════════════════════
# A. PLOTLY EXPRESS — Yüksek Seviye API
# ════════════════════════════════════════════════════════════════════════════

# ─── Veri Seti: Gapminder Tarzı ──────────────────────────────────────────────
ulkeler  = ['ABD', 'Çin', 'Japonya', 'Almanya', 'Hindistan', 'İngiltere', 'Fransa']
yillar   = list(range(2000, 2021))
veri_list = []

for ulke in ulkeler:
    for yil in yillar:
        veri_list.append({
            'Ülke': ulke,
            'Yıl': yil,
            'GSYİH (T$)': np.random.uniform(1, 20) * (1 + (yil-2000)*0.03),
            'Nüfus (M)': np.random.uniform(50, 1400),
            'Ömür (yıl)': np.random.uniform(70, 85),
            'Kıta': 'Asya' if ulke in ['Çin','Japonya','Hindistan'] else
                    'Avrupa' if ulke in ['Almanya','İngiltere','Fransa'] else 'Amerika'
        })

df = pd.DataFrame(veri_list)

# ─── Express: Çizgi Grafiği (Otomatik Renklendirme) ──────────────────────────
fig1 = px.line(df, x='Yıl', y='GSYİH (T$)', color='Ülke',
               title='GSYİH Trendleri (2000-2020) — Plotly Express',
               labels={'GSYİH (T$)': 'GSYİH (Trilyon $)'},
               hover_data=['Nüfus (M)', 'Ömür (yıl)'])
fig1.update_layout(hovermode='x unified')  # Tüm seriler tek hover'da
fig1.write_html(os.path.join(tempfile.gettempdir(), "px_line.html"))
print("Express çizgi grafiği: /tmp/px_line.html")

# ─── Express: Scatter (Animasyon Kareleri) ───────────────────────────────────
fig2 = px.scatter(df, x='GSYİH (T$)', y='Ömür (yıl)', size='Nüfus (M)',
                  color='Kıta', hover_name='Ülke', animation_frame='Yıl',
                  size_max=60, range_x=[0, 22], range_y=[68, 88],
                  title='GSYİH vs Ömür (Animasyonlu Bubble Chart)')
fig2.update_layout(transition={'duration': 500})
fig2.write_html(os.path.join(tempfile.gettempdir(), "px_bubble_anim.html"))
print("Express animasyonlu scatter: /tmp/px_bubble_anim.html")

# ─── Express: Histogram + Box (Facet Grid) ───────────────────────────────────
fig3 = px.histogram(df[df['Yıl'] == 2020], x='Ömür (yıl)', color='Kıta',
                    marginal='box',  # Kenar kutu grafiği
                    nbins=15, title='Ömür Dağılımı (2020) — Kıtalara Göre')
fig3.write_html(os.path.join(tempfile.gettempdir(), "px_histogram.html"))

# ════════════════════════════════════════════════════════════════════════════
# B. GRAPH OBJECTS — Düşük Seviye API (Tam Kontrol)
# ════════════════════════════════════════════════════════════════════════════

# ─── Graph Objects: Çoklu Trace ve Özel Stil ─────────────────────────────────
fig4 = go.Figure()

for ulke in ['ABD', 'Çin', 'Almanya']:
    df_ulke = df[df['Ülke'] == ulke]
    fig4.add_trace(go.Scatter(
        x=df_ulke['Yıl'], y=df_ulke['GSYİH (T$)'],
        mode='lines+markers',
        name=ulke,
        line=dict(width=2.5),
        marker=dict(size=6, line=dict(width=1, color='white')),
        hovertemplate='<b>%{fullData.name}</b><br>Yıl: %{x}<br>GSYİH: $%{y:.2f}T<extra></extra>'
    ))

# Anotasyon ekle (ok + metin)
fig4.add_annotation(
    x=2008, y=df[(df['Ülke']=='ABD')&(df['Yıl']==2008)]['GSYİH (T$)'].values[0],
    text="2008 Mali Krizi", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
    arrowcolor='red', ax=-60, ay=-40,
    font=dict(size=11, color='red'), bgcolor='rgba(255,255,255,0.8)'
)

fig4.update_layout(
    title='GSYİH Karşılaştırması (Graph Objects) — Özel Annotasyon',
    xaxis=dict(title='Yıl', showgrid=True, gridcolor='#E0E0E0'),
    yaxis=dict(title='GSYİH (Trilyon $)', showgrid=True, gridcolor='#E0E0E0'),
    hovermode='x unified',
    plot_bgcolor='#F8F9FA', paper_bgcolor='white',
    font=dict(family='Arial', size=12)
)
fig4.write_html(os.path.join(tempfile.gettempdir(), "go_custom.html"))
print("Graph Objects özel grafik: /tmp/go_custom.html")

# ─── Graph Objects: Çift Y Ekseni ────────────────────────────────────────────
fig5 = go.Figure()

df_abd = df[df['Ülke'] == 'ABD']
fig5.add_trace(go.Scatter(
    x=df_abd['Yıl'], y=df_abd['GSYİH (T$)'],
    name='GSYİH', yaxis='y1',
    line=dict(color='#1E3A5F', width=2.5)
))
fig5.add_trace(go.Scatter(
    x=df_abd['Yıl'], y=df_abd['Ömür (yıl)'],
    name='Ömür Beklentisi', yaxis='y2',
    line=dict(color='#C44D34', width=2.5, dash='dash')
))

fig5.update_layout(
    title='ABD: GSYİH ve Ömür Beklentisi (Çift Eksen)',
    xaxis=dict(title='Yıl'),
    yaxis=dict(title='GSYİH (Trilyon $)', side='left', titlefont=dict(color='#1E3A5F')),
    yaxis2=dict(title='Ömür (yıl)', side='right', overlaying='y', titlefont=dict(color='#C44D34')),
    hovermode='x unified'
)
fig5.write_html(os.path.join(tempfile.gettempdir(), "go_dual_axis.html"))
print("Çift eksen grafiği: /tmp/go_dual_axis.html")

print("\nTüm Plotly grafikleri oluşturuldu.")
