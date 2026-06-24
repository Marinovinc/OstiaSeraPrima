# -*- coding: utf-8 -*-
"""Schemi tecnici (NON foto di prodotto) delle esche dell'assetto multi-specie.
Disegna silhouette riconoscibili: minnow, octopus/kona, piumetta, teaser."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Ellipse, Polygon, FancyArrow, Circle
import numpy as np
import os

OUT = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/esche_proposte.png"
FOTO = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/esche_foto/minnow_2.jpg"  # CC0
KONA_FOTO = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/esche_foto/piumetta_ov_0.jpg"  # CC BY-NC 2.0, Lonnie's Life (Flickr)

fig, axs = plt.subplots(2, 2, figsize=(11, 7.2))
fig.suptitle("Esche dell'assetto  -  2 foto reali (minnow, kona) + 2 schemi (piumetta, teaser)",
             fontsize=12.5, fontweight="bold")

def hook(ax, x, y, s=0.06, c="#444"):
    # amo semplice (gambo + curva)
    ax.plot([x, x], [y, y-s*2.2], color=c, lw=1.6)
    th = np.linspace(0.2, 3.4, 30)
    ax.plot(x - s + s*np.cos(th), (y-s*2.2) + s*np.sin(th), color=c, lw=1.6)

# --- 1) MINNOW ~13 cm  [FOTO REALE CC0] ---
ax = axs[0, 0]; ax.set_title("MINNOW ~13 cm (labbro tuffatore)  [FOTO REALE]", fontsize=11, fontweight="bold")
if os.path.exists(FOTO):
    img = mpimg.imread(FOTO)
    ax.imshow(img, extent=[0.05, 0.95, 0.30, 0.80], aspect="auto", zorder=1)
    ax.text(0.5, 0.13, "alalunga - aguglia imperiale - tunnidi\nflat lines (12-18 m). Colore naturale/silver.",
            ha="center", fontsize=9)
else:
    ax.text(0.5, 0.5, "(foto non trovata)", ha="center")

# --- 2) OCTOPUS / KONA  [FOTO REALE] ---
ax = axs[0, 1]; ax.set_title("OCTOPUS / KONA (skirt)  [FOTO REALE]", fontsize=11, fontweight="bold")
if os.path.exists(KONA_FOTO):
    ax.imshow(mpimg.imread(KONA_FOTO), extent=[0.05, 0.95, 0.30, 0.80], aspect="auto", zorder=1)
else:
    ax.text(0.5, 0.5, "(foto non trovata)", ha="center")
ax.text(0.5, 0.13, "aguglia imp. - tonno striato - lampuga - alalunga\nrigger (18-25 m). Jupe ~15-20 cm. Blu/verde in profondo.",
        ha="center", fontsize=9)

# --- 3) PIUMETTA / FEATHER ---
ax = axs[1, 0]; ax.set_title("PIUMETTA / feather (anche piombata)", fontsize=11, fontweight="bold")
ax.add_patch(Ellipse((0.34, 0.58), 0.16, 0.14, facecolor="#b9c2cc", edgecolor="#33414d", lw=1.3))  # testa/piombo
for i, yy in enumerate(np.linspace(0.50, 0.66, 9)):
    ax.plot([0.40, 0.84], [yy, 0.42 + 0.05*np.sin(i*0.8)], color="#c44", lw=1.4)  # piume
    ax.plot([0.40, 0.84], [yy, 0.74 - 0.05*np.sin(i*0.8)], color="#fff", lw=1.0)
hook(ax, 0.72, 0.50)
ax.text(0.5, 0.13, "tonno striato - alalunga - alletterato\nshotgun (30-40 m) e profondo (piombata).",
        ha="center", fontsize=9)

# --- 4) TEASER daisy-chain ---
ax = axs[1, 1]; ax.set_title("TEASER daisy-chain  (SENZA amo - ammesso)", fontsize=11, fontweight="bold")
ax.plot([0.12, 0.92], [0.58, 0.58], color="#555", lw=1.2)  # trave/lenza
for k, xx in enumerate([0.30, 0.46, 0.62, 0.78]):
    col = ["#2f5d8a", "#1f7a4d", "#c43", "#7a4fa0"][k]
    ax.add_patch(Polygon([[xx-0.05, 0.62], [xx+0.05, 0.62], [xx+0.05, 0.50], [xx-0.05, 0.50]],
                 closed=True, facecolor=col, edgecolor="#222"))
    for yy in np.linspace(0.50, 0.62, 4):
        ax.plot([xx-0.04, xx+0.04][0:1]+[xx], [yy, 0.44], color=col, lw=1.0)
ax.text(0.5, 0.13, "NON pesca: attira i branchi (striato/alalunga)\ndietro al teaser metti la canna che lavora.",
        ha="center", fontsize=9)

for ax in axs.flat:
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

fig.text(0.5, 0.005,
         "Foto reali: minnow (Wikimedia Commons, CC0) - kona/octopus (foto Lonnie's Life, Flickr, CC BY-NC 2.0). "
         "Piumetta e teaser = schemi (nessuna foto libera pulita). Verificate: minnow ~13 cm + piumette piombate [R7]; "
         "colori profondi blu/verde/glow [R4]. Solo artificiali singolo amo non-inox (regolamento).",
         ha="center", fontsize=7.3, style="italic", color="#444")
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig(OUT, dpi=130, facecolor="white")
print("OK", OUT)
