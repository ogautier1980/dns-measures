"""
Figure 3 — Triangle of RIPE Atlas measurement constraints.
Three-axis trade-off: domain coverage / geographic coverage / temporal resolution,
bounded by the RIPE Atlas credit budget.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(7, 6.5))
fig.patch.set_facecolor('white')
ax.set_xlim(-0.15, 1.15)
ax.set_ylim(-0.22, 1.10)
ax.set_aspect('equal')
ax.axis('off')

GREY_DARK  = '#2c2c2c'
GREY_MED   = '#666666'
GREY_LIGHT = '#bbbbbb'

# ── Equilateral triangle vertices ─────────────────────────────────────────────
h = np.sqrt(3) / 2
V = np.array([[0.0, 0.0],   # bottom-left  → Domain coverage
              [1.0, 0.0],   # bottom-right → Geographic coverage
              [0.5, h  ]])  # top          → Temporal resolution
centroid = V.mean(axis=0)

# Draw triangle edges
triangle = plt.Polygon(V, closed=True, fill=False,
                        edgecolor=GREY_DARK, linewidth=2, zorder=2)
ax.add_patch(triangle)

# ── Shade the feasible region (slightly inset triangle) ───────────────────────
scale = 0.55
inner = centroid + scale * (V - centroid)
inner_patch = plt.Polygon(inner, closed=True,
                           facecolor='#d8d8d8', edgecolor='#999999',
                           linewidth=1, linestyle='--', zorder=1, alpha=0.7)
ax.add_patch(inner_patch)

# ── Operating point ───────────────────────────────────────────────────────────
# 10K domains × 100 probes × 1/day  →  moderate on all three axes
op = centroid + 0.10 * np.array([0.15, -0.20])   # slightly toward domains+geo
ax.plot(*op, 'o', color=GREY_DARK, markersize=9, zorder=5)
ax.annotate('Operating point\n10K domains × 100 probes × 1/day\n(~210M credits / 90 days)',
            xy=op, xytext=(op[0] + 0.22, op[1] - 0.09),
            fontsize=8, color=GREY_DARK,
            bbox=dict(boxstyle='round,pad=0.35', fc='white',
                      ec=GREY_DARK, lw=1),
            arrowprops=dict(arrowstyle='->', color=GREY_DARK, lw=1.2),
            zorder=6)

# ── Axis labels at vertices ────────────────────────────────────────────────────
label_offset = 0.10
# Bottom-left: Domain coverage
ax.text(V[0,0] - label_offset, V[0,1] - 0.07,
        'Domain coverage\n(# domains measured)',
        ha='center', va='top', fontsize=10, fontweight='bold', color=GREY_DARK)
ax.text(V[0,0] - label_offset, V[0,1] - 0.17,
        '↑ Top 100K   ↓ Top 1K',
        ha='center', va='top', fontsize=7.5, color=GREY_MED, fontstyle='italic')

# Bottom-right: Geographic coverage
ax.text(V[1,0] + label_offset, V[1,1] - 0.07,
        'Geographic coverage\n(# probes / regions)',
        ha='center', va='top', fontsize=10, fontweight='bold', color=GREY_DARK)
ax.text(V[1,0] + label_offset, V[1,1] - 0.17,
        '↑ 500 probes   ↓ 20 probes',
        ha='center', va='top', fontsize=7.5, color=GREY_MED, fontstyle='italic')

# Top: Temporal resolution
ax.text(V[2,0], V[2,1] + 0.07,
        'Temporal resolution\n(measurement frequency)',
        ha='center', va='bottom', fontsize=10, fontweight='bold', color=GREY_DARK)
ax.text(V[2,0], V[2,1] + 0.16,
        '↑ hourly   ↓ weekly',
        ha='center', va='bottom', fontsize=7.5, color=GREY_MED, fontstyle='italic')

# ── Trade-off arrows along edges ──────────────────────────────────────────────
def mid_edge(A, B, t=0.5):
    return A + t * (B - A)

# Edge: domains ↔ geographic (bottom edge)
m_dg = mid_edge(V[0], V[1])
ax.annotate('', xy=V[1]*0.85 + centroid*0.15,
            xytext=V[0]*0.85 + centroid*0.15,
            arrowprops=dict(arrowstyle='<->', color=GREY_LIGHT,
                            lw=1.2, shrinkA=0, shrinkB=0))
ax.text(m_dg[0], m_dg[1] - 0.06, 'trade-off',
        ha='center', fontsize=7, color=GREY_LIGHT, fontstyle='italic')

# Edge: domains ↔ temporal (left edge)
m_dt = mid_edge(V[0], V[2])
ax.annotate('', xy=V[2]*0.85 + centroid*0.15,
            xytext=V[0]*0.85 + centroid*0.15,
            arrowprops=dict(arrowstyle='<->', color=GREY_LIGHT,
                            lw=1.2, shrinkA=0, shrinkB=0))
ax.text(m_dt[0] - 0.10, m_dt[1], 'trade-off',
        ha='center', fontsize=7, color=GREY_LIGHT, fontstyle='italic',
        rotation=60)

# Edge: geographic ↔ temporal (right edge)
m_gt = mid_edge(V[1], V[2])
ax.annotate('', xy=V[2]*0.85 + centroid*0.15,
            xytext=V[1]*0.85 + centroid*0.15,
            arrowprops=dict(arrowstyle='<->', color=GREY_LIGHT,
                            lw=1.2, shrinkA=0, shrinkB=0))
ax.text(m_gt[0] + 0.10, m_gt[1], 'trade-off',
        ha='center', fontsize=7, color=GREY_LIGHT, fontstyle='italic',
        rotation=-60)

# ── Credit budget label ────────────────────────────────────────────────────────
ax.text(centroid[0], centroid[1] + 0.22,
        'Feasible region\n(RIPE Atlas credit budget)',
        ha='center', va='center', fontsize=8, color='#444444',
        fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.3', fc='white',
                  ec='#aaaaaa', lw=0.8, alpha=0.85))

# ── Corner examples ────────────────────────────────────────────────────────────
# Extreme corners annotations
ax.text(V[0,0] + 0.13, V[0,1] + 0.06,
        'e.g. OpenINTEL:\n123M domains,\n1 vantage point,\ndaily',
        fontsize=6.2, color='#888888', fontstyle='italic', va='bottom')
ax.text(V[1,0] - 0.13, V[1,1] + 0.06,
        'e.g. single-probe study:\n1 VP, many domains,\nhigh frequency',
        fontsize=6.2, color='#888888', fontstyle='italic',
        va='bottom', ha='right')

out = '/workspace/latex/figures/fig3_constraints_triangle.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
