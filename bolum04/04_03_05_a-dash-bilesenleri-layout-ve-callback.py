# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.5. Dash ile Web Uygulamaları: Reaktif Dashboard Mimarisi › A. Dash Bileşenleri: Layout ve Callback
# Dosya : bolum04/04_03_05_a-dash-bilesenleri-layout-ve-callback.py
# Gerekli: pip install dash numpy pandas plotly
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
import random
# ─── Kurulum ─────────────────────────────────────────────────────────────────
# pip install dash pandas

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─── Veri Seti Hazırlama ─────────────────────────────────────────────────────
np.random.seed(42)
tarihler = pd.date_range('2020-01-01', periods=365*2, freq='D')
hisse_a = 100 * np.exp(np.cumsum(np.random.randn(len(tarihler)) * 0.015))
hisse_b = 100 * np.exp(np.cumsum(np.random.randn(len(tarihler)) * 0.020))
hisse_c = 100 * np.exp(np.cumsum(np.random.randn(len(tarihler)) * 0.012))

df = pd.DataFrame({
    'Tarih': tarihler,
    'Hisse A': hisse_a,
    'Hisse B': hisse_b,
    'Hisse C': hisse_c,
})

# ════════════════════════════════════════════════════════════════════════════
# DASH UYGULAMASI
# ════════════════════════════════════════════════════════════════════════════

app = dash.Dash(__name__)

# ─── Layout: HTML/React Bileşen Ağacı ────────────────────────────────────────
app.layout = html.Div([
    html.H1("📈 Hisse Senedi Analiz Dashboard",
            style={'textAlign': 'center', 'color': '#1E3A5F', 'marginBottom': 30}),

    html.Div([
        html.Div([
            html.Label("Hisse Seçimi:", style={'fontWeight': 'bold', 'fontSize': 14}),
            dcc.Dropdown(
                id='hisse-dropdown',
                options=[
                    {'label': 'Hisse A', 'value': 'Hisse A'},
                    {'label': 'Hisse B', 'value': 'Hisse B'},
                    {'label': 'Hisse C', 'value': 'Hisse C'},
                ],
                value='Hisse A',
                clearable=False,
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),

        html.Div([
            html.Label("Tarih Aralığı:", style={'fontWeight': 'bold', 'fontSize': 14}),
            dcc.DatePickerRange(
                id='tarih-range',
                start_date=tarihler[0],
                end_date=tarihler[-1],
                display_format='YYYY-MM-DD',
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),

        html.Div([
            html.Label("Hareketli Ortalama Penceresi:", style={'fontWeight': 'bold', 'fontSize': 14}),
            dcc.Slider(
                id='ma-slider',
                min=5, max=90, step=5, value=30,
                marks={i: str(i) for i in range(5, 91, 15)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'width': '30%', 'display': 'inline-block'}),
    ], style={'marginBottom': 40}),

    # ─── Grafik Çıktıları ─────────────────────────────────────────────────────
    dcc.Graph(id='fiyat-grafik'),

    html.Div([
        html.Div([
            dcc.Graph(id='histogram-grafik')
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='box-grafik')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ]),

    # ─── İstatistikler Kartı ─────────────────────────────────────────────────
    html.Div(id='istatistik-kart',
             style={'marginTop': 30, 'padding': 20, 'backgroundColor': '#F8F9FA',
                    'borderRadius': 10, 'textAlign': 'center'})
], style={'padding': 40, 'fontFamily': 'Arial, sans-serif'})

# ════════════════════════════════════════════════════════════════════════════
# CALLBACK FONKSİYONLARI — Reaktif Güncelleme
# ════════════════════════════════════════════════════════════════════════════

# ─── Callback 1: Fiyat Grafiği + Hareketli Ortalama ──────────────────────────
@app.callback(
    Output('fiyat-grafik', 'figure'),
    [Input('hisse-dropdown', 'value'),
     Input('tarih-range', 'start_date'),
     Input('tarih-range', 'end_date'),
     Input('ma-slider', 'value')]
)
def update_fiyat_grafik(hisse, start, end, ma_pencere):
    # Tarih filtresi
    mask = (df['Tarih'] >= start) & (df['Tarih'] <= end)
    df_filtered = df[mask].copy()

    # Hareketli ortalama
    df_filtered['MA'] = df_filtered[hisse].rolling(window=ma_pencere).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['Tarih'], y=df_filtered[hisse],
        mode='lines', name='Fiyat',
        line=dict(color='#1E3A5F', width=1.5),
        fill='tozeroy', fillcolor='rgba(30,58,95,0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=df_filtered['Tarih'], y=df_filtered['MA'],
        mode='lines', name=f'{ma_pencere}-Gün MA',
        line=dict(color='#C44D34', width=2.5, dash='dash')
    ))

    fig.update_layout(
        title=f"{hisse} Fiyat Grafiği",
        xaxis=dict(title='Tarih'),
        yaxis=dict(title='Fiyat ($)'),
        hovermode='x unified',
        height=400
    )
    return fig

# ─── Callback 2: Günlük Getiri Histogramı ────────────────────────────────────
@app.callback(
    Output('histogram-grafik', 'figure'),
    [Input('hisse-dropdown', 'value'),
     Input('tarih-range', 'start_date'),
     Input('tarih-range', 'end_date')]
)
def update_histogram(hisse, start, end):
    mask = (df['Tarih'] >= start) & (df['Tarih'] <= end)
    df_filtered = df[mask].copy()

    # Günlük getiri: r_t = (P_t - P_{t-1}) / P_{t-1}
    df_filtered['Getiri'] = df_filtered[hisse].pct_change() * 100

    fig = go.Figure(data=[go.Histogram(
        x=df_filtered['Getiri'].dropna(),
        nbinsx=50,
        marker=dict(color='#2E5F8A', line=dict(color='white', width=1))
    )])

    fig.update_layout(
        title=f"{hisse} Günlük Getiri Dağılımı",
        xaxis=dict(title='Getiri (%)'),
        yaxis=dict(title='Frekans'),
        height=350
    )
    return fig

# ─── Callback 3: Kutu Grafiği (Aylık Getiri) ─────────────────────────────────
@app.callback(
    Output('box-grafik', 'figure'),
    [Input('hisse-dropdown', 'value'),
     Input('tarih-range', 'start_date'),
     Input('tarih-range', 'end_date')]
)
def update_box(hisse, start, end):
    mask = (df['Tarih'] >= start) & (df['Tarih'] <= end)
    df_filtered = df[mask].copy()
    df_filtered['Ay'] = df_filtered['Tarih'].dt.to_period('M').astype(str)
    df_filtered['Getiri'] = df_filtered[hisse].pct_change() * 100

    fig = px.box(df_filtered, x='Ay', y='Getiri',
                 title=f"{hisse} Aylık Getiri Dağılımı")
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=350)
    return fig

# ─── Callback 4: İstatistik Kartı ────────────────────────────────────────────
@app.callback(
    Output('istatistik-kart', 'children'),
    [Input('hisse-dropdown', 'value'),
     Input('tarih-range', 'start_date'),
     Input('tarih-range', 'end_date')]
)
def update_istatistik(hisse, start, end):
    mask = (df['Tarih'] >= start) & (df['Tarih'] <= end)
    df_f = df[mask].copy()

    ortalama = df_f[hisse].mean()
    std      = df_f[hisse].std()
    minimum  = df_f[hisse].min()
    maksimum = df_f[hisse].max()
    toplam_getiri = ((df_f[hisse].iloc[-1] - df_f[hisse].iloc[0]) / df_f[hisse].iloc[0]) * 100

    # İstatistik kartı oluştur (HTML.Div yapısı)
    stats_text = f"Ortalama: {ortalama:.2f}, Min: {minimum:.2f}, Maks: {maksimum:.2f}"
    return html.Div([html.H3(f"{hisse} İstatistikleri"), html.P(stats_text)])

# ─── Uygulamayı Başlat ───────────────────────────────────────────────────────
if __name__ == '__main__':
    # Not: Jupyter'da çalıştırmak için app.run_server(mode='inline')
    # Script modunda: app.run_server(debug=True)
    print("\n" + "="*70)
    print("Dash uygulaması hazır!")
    print("Çalıştırmak için:")
    print("  python dash_hisse_app.py")
    print("Ardından tarayıcıda: http://127.0.0.1:8050")
    print("="*70)
    # app.run_server(debug=True)  # Bu satırı aktifleştirin
