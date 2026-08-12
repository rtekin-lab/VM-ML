# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.3. Plotly: Modern İnteraktif Veri Görselleştirme › 4.3.4. 3D Grafikler ve Yüzey Görselleştirme
# Dosya : bolum04/04_03_04_d-grafikler-ve-yuzey-gorsellestirme.py
# Gerekli: pip install numpy plotly
# ==========================================================================

# --- kitapta önceki blokta yer alan import'lar (dosya tek başına çalışsın diye eklendi)
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import random
# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
import plotly.graph_objects as go
import numpy as np

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
# ════════════════════════════════════════════════════════════════════════════
# A. 3D SCATTER — Küme Analizi Görselleştirme
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
np.random.seed(42)
n_cluster = 4
n_per_cluster = 100

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
X, Y, Z, labels = [], [], [], []
renk_map = {0: 'red', 1: 'blue', 2: 'green', 3: 'orange'}

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
for k in range(n_cluster):
    merkez = np.random.uniform(-5, 5, 3)
    for _ in range(n_per_cluster):
        nokta = merkez + np.random.randn(3) * 0.8
        X.append(nokta[0])
        Y.append(nokta[1])
        Z.append(nokta[2])
        labels.append(k)

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig1 = go.Figure(data=[go.Scatter3d(
    x=X, y=Y, z=Z,
    mode='markers',
    marker=dict(
        size=4,
        color=labels,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Küme ID"),
        line=dict(color='white', width=0.5)
    ),
    text=[f'Küme {l}' for l in labels],
    hovertemplate='<b>%{text}</b><br>x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>'
)])

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig1.update_layout(
    title="3D Scatter: Küme Analizi Görselleştirme",
    scene=dict(
        xaxis=dict(title='Özellik 1', backgroundcolor='#F0F0F0', gridcolor='white'),
        yaxis=dict(title='Özellik 2', backgroundcolor='#F0F0F0', gridcolor='white'),
        zaxis=dict(title='Özellik 3', backgroundcolor='#F0F0F0', gridcolor='white'),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
    ),
    height=700
)
fig1.write_html(os.path.join(tempfile.gettempdir(), "3d_scatter_clusters.html"))
print("3D scatter (kümeler): /tmp/3d_scatter_clusters.html")

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
# ════════════════════════════════════════════════════════════════════════════
# B. 3D SURFACE — Matematiksel Fonksiyon Yüzeyi
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
# Saddle (Eyer) fonksiyonu: z = x² - y²
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 - Y**2

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig2 = go.Figure(data=[go.Surface(
    x=X, y=Y, z=Z,
    colorscale='RdBu',
    contours=dict(
        z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project=dict(z=True))
    ),
    hovertemplate='x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>'
)])

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig2.update_layout(
    title="3D Surface: Saddle (Eyer) Fonksiyonu — z = x² - y²",
    scene=dict(
        xaxis=dict(title='x'),
        yaxis=dict(title='y'),
        zaxis=dict(title='z = x² - y²'),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
    ),
    height=700
)
fig2.write_html(os.path.join(tempfile.gettempdir(), "3d_surface_saddle.html"))
print("3D surface (eyer): /tmp/3d_surface_saddle.html")

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
# ════════════════════════════════════════════════════════════════════════════
# C. 3D CONTOUR — Seviye Eğrileri (Topoloji Haritası)
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
# Gaussian tepesi
x = np.linspace(-5, 5, 150)
y = np.linspace(-5, 5, 150)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2) / 4) * np.cos(X) * np.sin(Y)

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig3 = go.Figure(data=[go.Surface(
    x=X, y=Y, z=Z,
    colorscale='Viridis',
    contours=dict(
        x=dict(show=True, color="white", width=2),
        y=dict(show=True, color="white", width=2),
        z=dict(show=True, usecolormap=True, width=2, project=dict(z=True))
    )
)])

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig3.update_layout(
    title="3D Contour: Gaussian Tepesi — z = exp(-(x²+y²)/4)·cos(x)·sin(y)",
    scene=dict(
        xaxis=dict(title='x'),
        yaxis=dict(title='y'),
        zaxis=dict(title='z'),
        camera=dict(eye=dict(x=1.8, y=1.8, z=1.5))
    ),
    height=700
)
fig3.write_html(os.path.join(tempfile.gettempdir(), "3d_contour_gaussian.html"))
print("3D contour (gaussian): /tmp/3d_contour_gaussian.html")

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
# ════════════════════════════════════════════════════════════════════════════
# D. MESH3D — Torus (Simit) Geometrisi
# ════════════════════════════════════════════════════════════════════════════

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
# Parametrik Torus: x = (R+r·cos(v))·cos(u), y = (R+r·cos(v))·sin(u), z = r·sin(v)
R, r = 3, 1  # Büyük yarıçap, küçük yarıçap
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, 2*np.pi, 50)
U, V = np.meshgrid(u, v)

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
X_torus = (R + r*np.cos(V)) * np.cos(U)
Y_torus = (R + r*np.cos(V)) * np.sin(U)
Z_torus = r * np.sin(V)

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig4 = go.Figure(data=[go.Surface(
    x=X_torus, y=Y_torus, z=Z_torus,
    colorscale='Plasma',
    showscale=False
)])

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
fig4.update_layout(
    title="3D Mesh: Torus (Simit) Geometrisi — Parametrik Yüzey",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
        aspectmode='data'
    ),
    height=700
)
fig4.write_html(os.path.join(tempfile.gettempdir(), "3d_mesh_torus.html"))
print("3D mesh (torus): /tmp/3d_mesh_torus.html")

# --- ▌ Kod Örneği 4.3.4 — 3D Scatter, Surface, Contour ve Mesh3d ---
print("\nTüm 3D grafikler oluşturuldu.")
