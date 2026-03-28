"""
Figure 6 — BGP attraction basins in anycast DNS routing.
Illustrates how BGP path-length routing creates counter-intuitive attraction
basins that do not follow geographic proximity.
Based on Bortzmeyer (2013) data for d.nic.fr: Paris 36%, Frankfurt 36%,
with North America → Paris at 55% due to BGP peering.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))
fig.patch.set_facecolor('white')

GREY_DARK  = '#2c2c2c'
GREY_MED   = '#555555'
GREY_LIGHT = '#aaaaaa'
GREY_BG    = '#f0f0f0'

# ══════════════════════════════════════════════════════════════════════════════
# Panel (a) — Intuitive expectation (geographic proximity routing)
# ══════════════════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.set_title('(a) Expected routing (geographic proximity)',
             fontsize=10, fontweight='bold', color=GREY_DARK, pad=8)

def box(ax, x, y, w, h, label, sublabel=None, fc='white',
        ec='#2c2c2c', lw=1.4, fontsize=8.5, bold=False):
    rect = FancyBboxPatch((x-w/2, y-h/2), w, h,
                          boxstyle='round,pad=0.02,rounding_size=0.04',
                          facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    dy = 0.025 if sublabel else 0
    ax.text(x, y+dy, label, ha='center', va='center',
            fontsize=fontsize, color=GREY_DARK, fontweight=weight, zorder=4)
    if sublabel:
        ax.text(x, y-dy*2, sublabel, ha='center', va='center',
                fontsize=6.5, color=GREY_MED, zorder=4)

def arr(ax, x0, y0, x1, y1, color=GREY_DARK, lw=1.5, ls='-', style='->'):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, shrinkA=6, shrinkB=6))

# PoPs
box(ax, 0.28, 0.80, 0.30, 0.12, 'PoP Paris [CDG]', '36% global traffic',
    fc='#e0e0e0', bold=True, fontsize=8)
box(ax, 0.72, 0.80, 0.30, 0.12, 'PoP Frankfurt [FRA]', '36% global traffic',
    fc='#e0e0e0', bold=True, fontsize=8)

# Clients — expected geographic routing
clients_a = [
    (0.15, 0.55, 'Brussels\n(EU West)', True,  True),    # → Paris ✓
    (0.30, 0.40, 'London\n(EU NW)',     True,  True),
    (0.50, 0.55, 'Warsaw\n(EU East)',   False, True),    # → Frankfurt ✓
    (0.70, 0.40, 'Moscow\n(EU East)',   False, True),
    (0.20, 0.18, 'New York\n(NA)',      False, False),   # expected → Frankfurt (transatlantic)
    (0.80, 0.18, 'Tokyo\n(APAC)',       False, False),
]

for x, y, label, to_paris, show in clients_a:
    box(ax, x, y, 0.21, 0.11, label, fontsize=7.5)
    target_x = 0.28 if to_paris else 0.72
    target_y = 0.74
    color = GREY_DARK
    arr(ax, x, y+0.055, target_x + (x-target_x)*0.05, target_y, color=color)

# Basin boundaries (dashed vertical)
ax.axvline(0.50, ymin=0.28, ymax=0.90, color=GREY_LIGHT,
           linestyle='--', linewidth=1.2, zorder=1)
ax.text(0.50, 0.92, 'geographic\nboundary', ha='center', va='bottom',
        fontsize=7, color=GREY_LIGHT, fontstyle='italic')

# Labels
ax.text(0.25, 0.02, '← Paris basin\n(EU West + NA expected)',
        ha='center', fontsize=7.5, color=GREY_MED, va='bottom')
ax.text(0.75, 0.02, 'Frankfurt basin →\n(EU East + APAC)',
        ha='center', fontsize=7.5, color=GREY_MED, va='bottom')


# ══════════════════════════════════════════════════════════════════════════════
# Panel (b) — Actual BGP routing (Bortzmeyer 2013, d.nic.fr)
# ══════════════════════════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
ax.set_title('(b) Actual BGP routing  —  d.nic.fr (Bortzmeyer, 2013)',
             fontsize=10, fontweight='bold', color=GREY_DARK, pad=8)

# PoPs
box(ax, 0.28, 0.80, 0.30, 0.12, 'PoP Paris [CDG]', '36% global — 55% NA',
    fc='#e0e0e0', bold=True, fontsize=8)
box(ax, 0.72, 0.80, 0.30, 0.12, 'PoP Frankfurt [FRA]', '36% global',
    fc='#e0e0e0', bold=True, fontsize=8)

# BGP basins (shaded backgrounds — asymmetric!)
import matplotlib.patches as mpatch
# Paris basin: EU West + counterintuitively NA
basin_paris = mpatch.FancyBboxPatch((0.02, 0.08), 0.60, 0.60,
                                     boxstyle='round,pad=0.02',
                                     fc='#ebebeb', ec=GREY_LIGHT,
                                     lw=1, ls='--', zorder=0)
ax.add_patch(basin_paris)
ax.text(0.04, 0.66, 'BGP basin → Paris\n(EU West + North America!)',
        fontsize=7, color='#555555', fontstyle='italic', va='top')

# Frankfurt basin: EU East + APAC
basin_fra = mpatch.FancyBboxPatch((0.38, 0.08), 0.60, 0.60,
                                   boxstyle='round,pad=0.02',
                                   fc='#f5f5f5', ec=GREY_LIGHT,
                                   lw=1, ls='--', zorder=0)
ax.add_patch(basin_fra)
ax.text(0.96, 0.66, 'BGP basin → Frankfurt\n(EU East + APAC)',
        fontsize=7, color='#555555', fontstyle='italic',
        va='top', ha='right')

# Clients — actual routing
clients_b = [
    (0.15, 0.52, 'Brussels (EU W)', True),
    (0.28, 0.35, 'London (EU NW)',  True),
    (0.62, 0.52, 'Warsaw (EU E)',   False),
    (0.75, 0.35, 'Moscow (EU E)',   False),
    (0.20, 0.16, 'New York (NA)',   True,   True),   # counter-intuitive → Paris
    (0.80, 0.16, 'Tokyo (APAC)',    False),
]

for item in clients_b:
    x, y, label = item[0], item[1], item[2]
    to_paris     = item[3]
    counter      = item[4] if len(item) > 4 else False

    color = GREY_DARK
    fc_c  = '#ffffff'
    lw    = 1.4
    if counter:
        fc_c  = '#d0d0d0'
        lw    = 2.0
    box(ax, x, y, 0.23, 0.11, label, fc=fc_c, lw=lw, fontsize=7.5)
    target_x = 0.28 if to_paris else 0.72
    arr(ax, x, y + 0.055, target_x + (x-target_x)*0.04, 0.74,
        color=GREY_DARK, lw=lw)
    if counter:
        ax.text(x, y - 0.075,
                '⚠ counter-intuitive\n(BGP peering via Paris)',
                ha='center', fontsize=6.5, color='#555555',
                fontstyle='italic', va='top')

# Basin boundary
ax.axvline(0.50, ymin=0.08, ymax=0.88, color='#888888',
           linestyle=':', linewidth=1, zorder=1)
ax.text(0.50, 0.90, 'expected\nboundary', ha='center', va='bottom',
        fontsize=6.5, color='#888888', fontstyle='italic')

# Annotation about BGP
ax.annotate(
    'BGP path-length minimisation routes\n'
    'New York (NA) → Paris via transatlantic\n'
    'peering agreements (55% of NA probes)',
    xy=(0.20, 0.10), xytext=(0.03, 0.02),
    fontsize=7, color=GREY_DARK,
    bbox=dict(boxstyle='round,pad=0.3', fc='white',
              ec='#aaaaaa', lw=0.8),
    arrowprops=dict(arrowstyle='->', color='#888888', lw=1),
    zorder=5)

plt.tight_layout(pad=2.0)
out = '/workspace/latex/figures/fig6_bgp_attraction_basins.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
