# -*- coding: utf-8 -*-
"""Corregge i residui 'pentagono' che descrivono la FORMA del campo (-> quadrilatero/campo).
NON tocca: le note di correzione in INDICE/README ('vecchio pentagono') ne' lo strikethrough
storico voluto in DOCUMENTAZIONE_TECNICA §5 ('Campo a pentagono (SUPERATO...)')."""
SRC = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/"

FIXES = {
 "Briefing_tattico_Roma_2026.html":            [("Pentagono", "Quadrilatero")],
 "Fronte_Tevere_SQUADRA.html":                 [("campo gara (pentagono)", "campo gara (quadrilatero)")],
 "MANUALE_ZIGZAG_AP44_TrojanF32.html":         [("nel pentagono)", "nel campo)")],
 "HANDOVER_SESSIONE_roma2026_strategia_zigzag_20260602.md": [("celle nel pentagono,", "celle nel campo,")],
 "MANUALE_AP44_ZIGZAG_TRAINA.md":              [("dentro il pentagono", "dentro il campo")],
 "DOCUMENTAZIONE_TECNICA_roma2026_20260602.md":[("nel pentagono del campo", "nel campo")],
}

for fn, reps in FIXES.items():
    p = SRC + fn
    h = open(p, encoding="utf-8").read()
    tot = 0
    for old, new in reps:
        c = h.count(old); tot += c
        if c: h = h.replace(old, new)
        print(f"  {fn[:40]:40s} {c}x  {old[:30]}")
    if tot:
        open(p, "w", encoding="utf-8").write(h)

# verifica finale: residui 'pentagon' che NON siano le note volute
import re, glob
print("\n=== residui 'pentagon' rimasti (attesi solo: note correzione + strikethrough §5) ===")
for p in glob.glob(SRC + "*.html") + glob.glob(SRC + "*.md"):
    if ".BAK" in p: continue
    h = open(p, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r"[Pp]entagon[a-z]*", h):
        ctx = h[max(0,m.start()-35):m.start()+25].replace("\n"," ")
        print(f"  {p.split('/')[-1][:34]:34s} ...{ctx}...")
