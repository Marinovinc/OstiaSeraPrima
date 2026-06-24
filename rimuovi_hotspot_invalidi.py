# -*- coding: utf-8 -*-
"""Rimuove da Fronte_Tevere i marker hotspot a/b/g + canyon D1-D5: 5/8 sono FUORI
dal campo ufficiale (ferrate nulle), gli altri non validati e ridondanti con le rotte
A/B/C. Non li riposiziona (sarebbe inventare). Toglie marker, toggle, legenda, handler;
aggiunge banner storico. Verifica nessun riferimento pendente."""
F = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/Fronte_Tevere_SQUADRA.html"
h = open(F, encoding="utf-8").read(); orig = h
rep = {}

def cut(old, new=""):
    c = h.count(old); rep[old[:38]] = c
    return h.replace(old, new) if c else h

# R1 toggle canyon
h = cut('    <label>\n        <input type="checkbox" id="toggleCanyon" checked> Canyon SW (D1-D5)\n    </label>\n')
# R2 legenda hotspot
h = cut('    <div class="legend-item"><div class="legend-color" style="background:#ffd700;"></div> Hotspot (alpha, beta, gamma)</div>\n')
# R4 handler toggleCanyon
h = cut("document.getElementById('toggleCanyon').addEventListener('change', function() {\n    this.checked ? canyonGroup.addTo(map) : map.removeLayer(canyonGroup);\n});\n")
# R5 popup rotta B
h = cut("Start -> Fronte NE -> alpha (solunare) -> beta (alalunghe)",
        "Start -> Fronte NE -> scarpata profonda (solunare)")
# R6 narrativa pannello
h = cut("il sistema di canyon SW (beta/gamma/C + D1-D5, pareti 58-98%) dove l'upwelling da vento attiva la pesca",
        "le strutture profonde dentro il campo (rotte A/B/C nel dossier nuovo)")

# R3 blocco const/group (slice tra ancore)
s = h.find("const alpha = [41.60, 12.00];")
a = h.find("canyonPoints.map(p => canyonMarker")
e = h.find(").addTo(map);", a)
blk_ok = (0 < s < a < e)
if blk_ok:
    e += len(").addTo(map);")
    h = h[:s] + ("// hotspot alpha/beta/gamma + canyon D1-D5 RIMOSSI 2026-06-24:\n"
                 "// 5/8 erano FUORI dal campo ufficiale (ferrata nulla), gli altri non validati\n"
                 "// e ridondanti con le rotte A/B/C. NON riposizionati (= inventare). Vedi dossier nuovo.\n") + h[e:]

# R7 banner storico dopo <body>
banner = ('<div style="background:#7a1020;color:#fff;padding:9px 15px;font-family:sans-serif;'
          'font-size:13px;border-bottom:3px solid #e94560"><b>NOTA 2026-06-24:</b> tool storico '
          '(strategia fronte-Tevere superata). Campo gara = <b>quadrilatero ufficiale A/B/C/D</b>. '
          'I vecchi hotspot a/b/g e canyon D1-D5 sono stati <b>rimossi</b> (5 cadevano fuori dal campo, '
          'gli altri non validati). Riferimento operativo: dossier nuovo + ROTTE_OSTIA_2026.gpx.</div>')
bi = h.find("<body"); ban_ok = False
if bi >= 0 and "NOTA 2026-06-24" not in h:
    be = h.find(">", bi) + 1; h = h[:be] + banner + h[be:]; ban_ok = True

open(F, "w", encoding="utf-8").write(h)
print("Sostituzioni:")
for k, v in rep.items(): print(f"  {v}x  {k}")
print("blocco const/group rimosso:", blk_ok, "| banner:", ban_ok, "| delta bytes:", len(h)-len(orig))
print("\nRiferimenti pendenti residui (devono essere ~0):")
for kw in ("hotspotGroup","canyonGroup","hotspotMarker","canyonMarker","toggleCanyon","const alpha","canyonPoints"):
    print(f"  {kw:15s}: {h.count(kw)}")
