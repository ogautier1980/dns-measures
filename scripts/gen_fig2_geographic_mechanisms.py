"""
Figure 2 — Three geographic variation mechanisms in DNS.
Three side-by-side panels: CDN routing, IP anycast BGP basins, ECS.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(14, 6.5))
fig.patch.set_facecolor('white')

GREY_DARK  = '#2c2c2c'
GREY_MED   = '#555555'
GREY_LIGHT = '#aaaaaa'
GREY_BG    = '#f0f0f0'
WHITE      = '#ffffff'
BLACK      = '#000000'

# ── shared helpers ────────────────────────────────────────────────────────────

def box(ax, x, y, w, h, label, sublabel=None, radius=0.06,
        fc=WHITE, ec=GREY_DARK, lw=1.2, fontsize=8.5, bold=False):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle=f"round,pad=0.01,rounding_size={radius}",
                          facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y + (0.02 if sublabel else 0), label,
            ha='center', va='center', fontsize=fontsize, color=GREY_DARK,
            fontweight=weight, zorder=4)
    if sublabel:
        ax.text(x, y - 0.13, sublabel, ha='center', va='center',
                fontsize=7, color=GREY_MED, zorder=4)

def arrow(ax, x0, y0, x1, y1, label=None, color=GREY_DARK, lw=1.2,
          style='->', fontsize=7):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, shrinkA=4, shrinkB=4))
    if label:
        mx, my = (x0+x1)/2, (y0+y1)/2
        ax.text(mx + 0.04, my, label, fontsize=fontsize, color=color,
                ha='left', va='center', zorder=5)

def region_circle(ax, x, y, r, label, fc=GREY_BG, ec=GREY_LIGHT):
    circ = plt.Circle((x, y), r, facecolor=fc, edgecolor=ec,
                      linewidth=1, zorder=1)
    ax.add_patch(circ)
    ax.text(x, y - r - 0.08, label, ha='center', va='top',
            fontsize=7.5, color=GREY_MED)


# ══════════════════════════════════════════════════════════════════════════════
# Panel 1 — CDN-based geographic routing
# ══════════════════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.set_title('(a) CDN geographic routing', fontsize=10, fontweight='bold',
             color=GREY_DARK, pad=8)

# CDN authoritative server (top centre)
box(ax, 0.50, 0.85, 0.46, 0.13,
    'CDN authoritative server', 'cdn.example.com',
    fc='#e8e8e8', ec=GREY_DARK, bold=True)

# EU client (left)
region_circle(ax, 0.18, 0.50, 0.13, 'Europe', fc='#f5f5f5')
box(ax, 0.18, 0.50, 0.22, 0.11, 'Client EU', '192.0.2.1')

# US client (right)
region_circle(ax, 0.82, 0.50, 0.13, 'North America', fc='#f5f5f5')
box(ax, 0.82, 0.50, 0.22, 0.11, 'Client US', '198.51.100.1')

# EU PoP (left-bottom)
box(ax, 0.18, 0.15, 0.26, 0.11, 'EU edge server', '104.20.1.1  [AMS]',
    fc='#e8e8e8')
# US PoP (right-bottom)
box(ax, 0.82, 0.15, 0.26, 0.11, 'US edge server', '104.17.200.1  [IAD]',
    fc='#e8e8e8')

# Arrows: clients → CDN auth
arrow(ax, 0.18, 0.56, 0.38, 0.80, 'A cdn.example.com?', fontsize=6.5)
arrow(ax, 0.82, 0.56, 0.62, 0.80, 'A cdn.example.com?', fontsize=6.5)

# Arrows: CDN auth → clients (responses differ)
arrow(ax, 0.38, 0.79, 0.18, 0.56, '104.20.1.1', color='#333333',
      style='<-', fontsize=6.5)
arrow(ax, 0.62, 0.79, 0.82, 0.56, '104.17.200.1', color='#333333',
      style='<-', fontsize=6.5)

# Arrows: clients → PoPs
arrow(ax, 0.18, 0.44, 0.18, 0.21)
arrow(ax, 0.82, 0.44, 0.82, 0.21)

# Annotation
ax.text(0.50, 0.04, 'Same domain → different IPs\nby client location',
        ha='center', va='bottom', fontsize=7.5, color=GREY_MED,
        fontstyle='italic')


# ══════════════════════════════════════════════════════════════════════════════
# Panel 2 — IP anycast BGP attraction basins
# ══════════════════════════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.set_title('(b) IP anycast BGP attraction basins', fontsize=10,
             fontweight='bold', color=GREY_DARK, pad=8)

# Single anycast IP label
ax.text(0.50, 0.95, 'Anycast IP: 192.0.0.1',
        ha='center', va='top', fontsize=8.5, color=GREY_DARK,
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', fc='#e8e8e8', ec=GREY_DARK, lw=1))

# PoPs
box(ax, 0.25, 0.68, 0.28, 0.11, 'PoP Paris [CDG]', '192.0.0.1',
    fc='#e8e8e8')
box(ax, 0.75, 0.68, 0.28, 0.11, 'PoP New York [JFK]', '192.0.0.1',
    fc='#e8e8e8')

# BGP basins (dashed regions)
import matplotlib.patches as mpatch
# Basin 1 — Europe + North America → Paris (counter-intuitive)
basin1 = mpatch.FancyBboxPatch((0.02, 0.05), 0.55, 0.48,
                                boxstyle="round,pad=0.02",
                                facecolor='#f0f0f0', edgecolor=GREY_LIGHT,
                                linewidth=1, linestyle='--', zorder=1)
ax.add_patch(basin1)
ax.text(0.04, 0.50, 'BGP basin → Paris', fontsize=7, color=GREY_MED,
        fontstyle='italic')

# Basin 2 — Asia + rest → New York
basin2 = mpatch.FancyBboxPatch((0.43, 0.05), 0.55, 0.48,
                                boxstyle="round,pad=0.02",
                                facecolor='#e8e8e8', edgecolor=GREY_LIGHT,
                                linewidth=1, linestyle='--', zorder=1)
ax.add_patch(basin2)
ax.text(0.96, 0.50, 'BGP basin → New York', fontsize=7, color=GREY_MED,
        fontstyle='italic', ha='right')

# Clients
box(ax, 0.20, 0.30, 0.24, 0.10, 'Client EU', 'Brussels')
box(ax, 0.35, 0.14, 0.24, 0.10, 'Client NA', 'Toronto')  # counter-intuitive
box(ax, 0.75, 0.30, 0.24, 0.10, 'Client APAC', 'Tokyo')
box(ax, 0.65, 0.14, 0.24, 0.10, 'Client SA', 'São Paulo')

# Arrows to PoPs
arrow(ax, 0.20, 0.35, 0.25, 0.63)
arrow(ax, 0.35, 0.19, 0.27, 0.63)  # counter-intuitive: Toronto → Paris
arrow(ax, 0.75, 0.35, 0.75, 0.63)
arrow(ax, 0.65, 0.19, 0.73, 0.63)

# Annotation counter-intuitive
ax.annotate('counter-intuitive\n(BGP path length)',
            xy=(0.27, 0.63), xytext=(0.04, 0.70),
            fontsize=6.5, color='#666666', fontstyle='italic',
            arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8))

ax.text(0.50, 0.02, 'Same anycast IP → different physical instances\nby BGP routing, not geography',
        ha='center', va='bottom', fontsize=7.5, color=GREY_MED,
        fontstyle='italic')


# ══════════════════════════════════════════════════════════════════════════════
# Panel 3 — EDNS Client Subnet (ECS)
# ══════════════════════════════════════════════════════════════════════════════
ax = axes[2]
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.set_title('(c) EDNS Client Subnet (ECS)', fontsize=10, fontweight='bold',
             color=GREY_DARK, pad=8)

# Actors
box(ax, 0.15, 0.82, 0.24, 0.11, 'Client', '192.51.100.42\n[Brussels]',
    fontsize=8)
box(ax, 0.15, 0.52, 0.24, 0.13, 'Recursive\nresolver', 'Google 8.8.8.8\n[US]',
    fontsize=8)
box(ax, 0.82, 0.52, 0.28, 0.13, 'CDN auth.\nserver', 'cdn.example.com',
    fontsize=8, fc='#e8e8e8')
box(ax, 0.40, 0.17, 0.30, 0.11, 'EU edge server',
    '198.41.128.1  [AMS]', fc='#e8e8e8', fontsize=8)
box(ax, 0.82, 0.17, 0.28, 0.11, 'US edge server',
    '104.17.200.1  [IAD]', fc='#e8e8e8', fontsize=8)

# client → resolver
arrow(ax, 0.15, 0.76, 0.15, 0.59, 'A cdn.example.com?', fontsize=6.5)

# resolver → CDN auth WITHOUT ECS
ax.annotate('', xy=(0.68, 0.57), xytext=(0.27, 0.57),
            arrowprops=dict(arrowstyle='->', color=GREY_LIGHT, lw=1.2,
                            linestyle='dashed', shrinkA=4, shrinkB=4))
ax.text(0.475, 0.61, 'without ECS:\nsource = 8.8.8.8 (US)',
        ha='center', fontsize=6.2, color=GREY_LIGHT, fontstyle='italic')
# CDN → US server (dashed)
ax.annotate('', xy=(0.82, 0.23), xytext=(0.82, 0.46),
            arrowprops=dict(arrowstyle='->', color=GREY_LIGHT, lw=1.2,
                            linestyle='dashed', shrinkA=4, shrinkB=4))

# resolver → CDN auth WITH ECS
ax.annotate('', xy=(0.68, 0.48), xytext=(0.27, 0.48),
            arrowprops=dict(arrowstyle='->', color=GREY_DARK, lw=1.5,
                            shrinkA=4, shrinkB=4))
ax.text(0.475, 0.42, 'with ECS:\nclient prefix 192.51.100.0/24',
        ha='center', fontsize=6.5, color=GREY_DARK, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#aaaaaa', lw=0.8))
# CDN → EU server (solid)
ax.annotate('', xy=(0.40, 0.23), xytext=(0.68, 0.46),
            arrowprops=dict(arrowstyle='->', color=GREY_DARK, lw=1.5,
                            shrinkA=4, shrinkB=4))

# EU server → client
arrow(ax, 0.29, 0.17, 0.15, 0.46, '198.41.128.1', color=GREY_DARK,
      style='<-', fontsize=6.5)

# Legend
ax.plot([0.03, 0.10], [0.07, 0.07], color=GREY_DARK, lw=1.5)
ax.text(0.11, 0.07, 'with ECS (EU PoP assigned)',
        fontsize=6.5, color=GREY_DARK, va='center')
ax.plot([0.03, 0.10], [0.035, 0.035], color=GREY_LIGHT, lw=1.2,
        linestyle='--')
ax.text(0.11, 0.035, 'without ECS (US PoP assigned)',
        fontsize=6.5, color=GREY_LIGHT, va='center')


plt.tight_layout(pad=1.5)
out = '/workspace/latex/figures/fig2_geographic_mechanisms.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
