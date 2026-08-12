# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 4
# Konum : BÖLÜM 4: Veri Görselleştirme Araçları › 4.1. Matplotlib: Temel Görselleştirme Kütüphanesi › 4.1.8. Animasyonlar ve Dinamik Görselleştirme
# Dosya : bolum04/04_01_08_animasyonlar-ve-dinamik-gorsellestirme.py
# Gerekli: pip install matplotlib numpy
# ==========================================================================
# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
# Windows/macOS/Linux uyumu: sabit /tmp yerine sistemin gecici dizini
import os
import tempfile

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
# ─── FuncAnimation: Gerçek Zamanlı Sinyal Simülasyonu ────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Dinamik Veri Görselleştirme (FuncAnimation)', fontsize=13, fontweight='bold')

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
n_pnt  = 100
t_data = np.linspace(0, 4*np.pi, n_pnt)
y_hist = []

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
line1, = ax1.plot([], [], '#1E3A5F', lw=2)
ax1.set_xlim(0, 4*np.pi); ax1.set_ylim(-2, 2)
ax1.set_title('Anlık Sinyal'); ax1.set_xlabel('t')
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=10)

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
line2, = ax2.plot([], [], '#C44D34', lw=2)
ax2.set_xlim(0, n_pnt); ax2.set_ylim(-2, 2)
ax2.set_title('Orta Nokta İzleme')

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2, time_text

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
def animate(frame):
    faz  = frame * 0.1
    y    = np.sin(t_data + faz) * (1 + 0.3*np.sin(0.5*faz))
    line1.set_data(t_data, y)
    time_text.set_text(f't = {faz:.2f} rad')
    y_hist.append(y[n_pnt//2])
    if len(y_hist) > n_pnt: y_hist.pop(0)
    line2.set_data(range(len(y_hist)), y_hist)
    return line1, line2, time_text

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=80, interval=50, blit=True)
try:
    ani.save(os.path.join(tempfile.gettempdir(), "animasyon.gif"), writer='pillow', fps=20, dpi=80)
    print("GIF kaydedildi: /tmp/animasyon.gif")
except Exception as e:
    plt.savefig(os.path.join(tempfile.gettempdir(), "animasyon_kare.png"), dpi=100)
    print(f"Statik kare kaydedildi (pillow kurulmamış).")
finally:
    plt.close()

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
# ─── ArtistAnimation: Önceden Hesaplanmış Kareler ───────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 4*np.pi); ax.set_ylim(-1.5, 1.5)

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
kareler = []
for i in range(40):
    t = np.linspace(0, 4*np.pi, 300)
    faz = i * np.pi/20
    y   = np.sin(t + faz)
    l,  = ax.plot(t, y, '#2E5F8A', lw=2.5)
    txt = ax.text(0.5, 1.05, f'Faz: {np.degrees(faz):.1f}°',
                  transform=ax.transAxes, ha='center', fontsize=11)
    kareler.append([l, txt])

# --- ▌ Kod Örneği 4.1.8 — FuncAnimation ve ArtistAnimation ---
ani2 = animation.ArtistAnimation(fig, kareler, interval=80, blit=True)
ax.set_title('Faz Kayması Animasyonu')
plt.tight_layout()
plt.savefig(os.path.join(tempfile.gettempdir(), "artist_ani.png"), dpi=100); plt.close()
print("ArtistAnimation tamamlandı.")
