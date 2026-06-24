# -*- coding: utf-8 -*-
"""Corregge il campo gara nel Briefing storico: pentagono -> quadrilatero ufficiale
(Ord. Capitaneria 67/2026), sostituisce l'immagine-mappa cotta del pentagono con la
mappa corretta del quadrilatero, e mette un banner di superamento. Verifica i conteggi."""
import base64, os

SRC = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/"
F   = SRC + "Briefing_tattico_Roma_2026.html"
MAP = SRC + "ROTTE_OSTIA_2026_mappa.png"   # mappa corretta (quadrilatero + rotte)

h = open(F, encoding="utf-8").read()
orig = h

# --- 1) sostituzioni di testo (ordine importante) ---
REPL = [
 ("pentagono A–E", "quadrilatero A–D"),
 ("Vertici del pentagono (da plotter)", "Vertici del campo (quadrilatero ufficiale, Ord. Capitaneria 67/2026)"),
 ("A 41°44.2′N 12°06.0′E · B 41°38.1′N 11°43.0′E · C 41°21.5′N 11°55.0′E · D 41°33.0′N 12°20.0′E · E 41°41.5′N 12°13.0′E.",
  "A 41°42.222′N 012°00.163′E · B 41°32.224′N 012°05.885′E · C 41°28.657′N 011°53.087′E · D 41°37.827′N 011°46.426′E."),
 ("<strong>pentagono</strong>", "<strong>quadrilatero</strong>"),
 ("pentagono", "quadrilatero"),                       # eventuali residui
 ("fuori dal vertice E", "fuori dal lato NE del campo"),
 ("vicino al vertice D", "vicino al bordo del campo"),
 ("(vertice C)", "(bordo SW del campo)"),
]
counts = {}
for old, new in REPL:
    c = h.count(old); counts[old[:32]] = c
    if c: h = h.replace(old, new)

# --- 2) sostituzione immagine-mappa cotta (quella del campo gara) ---
img_done = False
idx = h.find("Mappa di riferimento: il campo gara")
if idx > 0 and os.path.exists(MAP):
    ist = h.rfind("<img", 0, idx)
    ss  = h.find('src="', ist)
    if 0 < ist < idx and ss > 0:
        ve = h.find('"', ss + 5)
        b64 = base64.b64encode(open(MAP, "rb").read()).decode()
        h = h[:ss + 5] + "data:image/png;base64," + b64 + h[ve:]
        img_done = True

# --- 3) banner di superamento dopo <body> ---
banner = ('<div style="background:#7a1020;color:#fff;padding:10px 16px;'
          'font-family:sans-serif;font-size:13px;border-bottom:3px solid #e94560">'
          '<b>NOTA 2026-06-24:</b> strategia storica (superata dal dossier nuovo). '
          '<b>Campo gara corretto al quadrilatero ufficiale A/B/C/D</b> '
          '(Ord. Capitaneria di Porto Roma 67/2026). Riferimento operativo: '
          'dossier nuovo + ROTTE_OSTIA_2026.gpx.</div>')
banner_done = False
bi = h.find("<body")
if bi > 0:
    be = h.find(">", bi) + 1
    if "NOTA 2026-06-24" not in h:
        h = h[:be] + banner + h[be:]; banner_done = True

open(F, "w", encoding="utf-8").write(h)
print("CONTEGGI sostituzioni testo:")
for k, v in counts.items(): print(f"  {v:2d}x  {k}")
print("immagine campo sostituita:", img_done)
print("banner inserito:", banner_done)
print("delta bytes:", len(h) - len(orig))
print("residui 'pentagono':", h.count("pentagono"), "| 'vertice E':", h.count("vertice E"),
      "| coord vecchie 44.2:", h.count("44.2′N"))
