# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.8. Performans Optimizasyonu ve Production Tips
# Dosya : bolum04/04_03_08_performans-optimizasyonu-ve-production-tips.py
# Gerekli: pip install numpy plotly
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import tempfile

import random
# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
import plotly.graph_objects as go
import numpy as np

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# ════════════════════════════════════════════════════════════════════════════
# A. WebGL MOD — Yüksek Nokta Sayılı Scatter
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
np.random.seed(42)
n = 500_000  # 500K nokta

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
x = np.random.randn(n)
y = np.random.randn(n)
colors = np.random.rand(n)

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# YAVAŞ: go.Scatter (SVG render)
# fig_slow = go.Figure(data=[go.Scatter(x=x, y=y, mode='markers', ...)])

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# HIZLI: go.Scattergl (WebGL render)
fig_fast = go.Figure(data=[go.Scattergl(
    x=x, y=y, mode='markers',
    marker=dict(
        size=2,
        color=colors,
        colorscale='Viridis',
        showscale=True
    )
)])

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
fig_fast.update_layout(
    title=f'WebGL Scatter: {n:,} Nokta (GPU Render)',
    xaxis=dict(title='x'),
    yaxis=dict(title='y'),
    height=600
)
# fig_fast.write_html(os.path.join(tempfile.gettempdir(), "scattergl_500k.html"))  # ~5MB
print(f"WebGL scatter oluşturuldu: {n:,} nokta")

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# ════════════════════════════════════════════════════════════════════════════
# B. DATA DECIMATION — Ramer-Douglas-Peucker Algoritması
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
def rdp_simplify(points, epsilon):
    """
    Ramer-Douglas-Peucker line simplification.
    points: [(x1,y1), (x2,y2), ...]
    epsilon: Tolerans (daha büyük = daha fazla decimation)
    """
    if len(points) < 3:
        return points

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
    # En uzak nokta bul
    dmax, index = 0, 0
    end = len(points) - 1
    for i in range(1, end):
        d = perpendicular_distance(points[i], points[0], points[end])
        if d > dmax:
            dmax, index = d, i

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
    # Recursive simplify
    if dmax > epsilon:
        left = rdp_simplify(points[:index+1], epsilon)
        right = rdp_simplify(points[index:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
def perpendicular_distance(point, line_start, line_end):
    if line_start == line_end:
        return np.linalg.norm(np.array(point) - np.array(line_start))
    n = np.abs((line_end[1]-line_start[1])*point[0] -
               (line_end[0]-line_start[0])*point[1] +
               line_end[0]*line_start[1] -
               line_end[1]*line_start[0])
    d = np.linalg.norm(np.array(line_end) - np.array(line_start))
    return n / d

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# Örnek zaman serisi
t = np.linspace(0, 10, 10000)
signal = np.sin(t) + 0.1*np.random.randn(len(t))
points_original = list(zip(t, signal))

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# Decimation uygula
points_simplified = rdp_simplify(points_original, epsilon=0.05)
t_simp, signal_simp = zip(*points_simplified)

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
print(f"Decimation: {len(points_original):,} → {len(points_simplified):,} nokta "
      f"(%{100*(1-len(points_simplified)/len(points_original)):.1f} azalma)")

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
fig_dec = go.Figure()
fig_dec.add_trace(go.Scatter(
    x=t, y=signal, mode='lines', name='Orijinal (10K)',
    line=dict(color='lightblue', width=1), opacity=0.5
))
fig_dec.add_trace(go.Scatter(
    x=t_simp, y=signal_simp, mode='lines+markers', name=f'Decimated ({len(points_simplified)})',
    line=dict(color='#1E3A5F', width=2),
    marker=dict(size=3, color='red')
))
fig_dec.update_layout(
    title='Data Decimation: Ramer-Douglas-Peucker',
    xaxis=dict(title='Zaman'),
    yaxis=dict(title='Sinyal'),
    height=500
)
fig_dec.write_html(os.path.join(tempfile.gettempdir(), "decimation_demo.html"))
print("Decimation demo: /tmp/decimation_demo.html")

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# ════════════════════════════════════════════════════════════════════════════
# C. PRODUCTION EXPORT — Optimize Edilmiş HTML
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
fig_prod = go.Figure(data=[go.Scatter(
    x=[1,2,3,4,5], y=[1,4,2,3,5],
    mode='lines+markers',
    line=dict(color='#1E3A5F', width=2.5),
    marker=dict(size=8)
)])

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
fig_prod.update_layout(
    title='Production Export Demo',
    template='plotly_white',
    height=400
)

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
# Optimize export ayarları
config_prod = {
    'displayModeBar': True,           # Toolbar göster
    'displaylogo': False,              # Plotly logosu kaldır
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],  # Gereksiz düğmeleri kaldır
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'grafik',
        'height': 800,
        'width': 1200,
        'scale': 2                     # 2× resolution for export
    }
}

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
fig_prod.write_html(
    os.path.join(tempfile.gettempdir(), "production_export.html"),
    include_plotlyjs='cdn',            # Plotly.js CDN'den yükle (-3MB)
    config=config_prod,
    auto_open=False
)

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
import os
boyut_kb = os.path.getsize(os.path.join(tempfile.gettempdir(), "production_export.html")) / 1024
print(f"\nProduction export: {boyut_kb:.1f} KB (plotly.js CDN'de)")

# --- ▌ Kod Örneği 4.3.8 — WebGL, Decimation ve Production Export ---
print("\n─── Production Tips ───────────────────────────────────────────")
print("1. Büyük veri (>10K nokta): go.Scattergl kullanın")
print("2. Zaman serisi: RDP decimation uygulayın (epsilon tuning)")
print("3. HTML export: include_plotlyjs='cdn' (~3MB tasarruf)")
print("4. Dash: dcc.Store ile veri client-side cache'leyin")
print("5. Billion-scale: Datashader + Plotly heatmap pipeline")
