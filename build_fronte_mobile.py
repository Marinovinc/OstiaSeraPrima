# -*- coding: utf-8 -*-
"""Genera versioni MOBILE e IPAD di Fronte_Tevere_SQUADRA.html.
Problema risolto: i pannelli overlay 'Come leggere' e 'scala colori' coprivano la
mappa sul telefono. Resi COLLASSABILI con pulsanti nella barra controlli + tuning CSS
responsive. Default: mobile = guida chiusa; ipad = guida aperta. Nessuna modifica ai dati."""
import os
SRC = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/"
base = open(SRC + "Fronte_Tevere_SQUADRA.html", encoding="utf-8").read()

# 1) id al banner storico (per poterlo rimpicciolire su mobile)
base = base.replace(
    '<body><div style="background:#7a1020;',
    '<body><div id="histbanner" style="background:#7a1020;', 1)

# 2) CSS di tuning (iniettato prima di </head>)
TUNE = """
<style id="mobtune">
/* === TUNING MOBILE/IPAD (2026-06-24) === */
.info-box.collapsed, .color-scale.collapsed { display:none !important; }
.ctlbtn { background:#0f3460 !important; border:1px solid #e94560 !important; }
@media (max-width:1024px){
  #histbanner{ font-size:11px; padding:7px 11px; max-height:30vh; overflow:auto; }
  .info-box{ max-width:min(360px,84vw); max-height:70vh; overflow:auto; top:48px; }
  .color-scale{ bottom:14px; }
}
@media (max-width:640px){
  #histbanner{ font-size:10px; line-height:1.35; max-height:22vh; }
  .controls{ padding:6px 8px; gap:6px 8px; }
  .controls h1{ font-size:13px; width:100%; margin:0 0 2px; }
  .controls > label{ flex:1 1 46%; min-width:0; font-size:12px; }
  .controls > label[style*="margin-left:auto"]{ margin-left:0 !important; }
  /* select/data/opacita: a tutta riga SOTTO l'etichetta, senza sforare */
  .controls select, .controls input[type=date]{ display:block; width:100%; min-width:0; margin-top:2px; }
  .controls input[type=range]{ width:100%; }
  /* i checkbox restano in linea col testo (non vanno a blocco) */
  .controls button{ flex:1 1 46%; padding:9px 8px; }
  #map{ height:60vh; min-height:340px; flex:none; }
  /* guida come overlay scrollabile a tutta larghezza, in basso (quando aperta) */
  .info-box{ position:fixed; left:6vw; right:6vw; width:88vw; max-width:88vw;
             top:auto; bottom:10px; max-height:68vh; overflow:auto; }
  .color-scale{ transform:scale(.8); transform-origin:bottom left; bottom:8px; left:2px; }
  .color-bar, .color-labels{ height:120px; }
}
</style>
"""
base = base.replace("</head>", TUNE + "</head>", 1)

# 3) script: pulsanti Guida/Scala nella barra controlli + stato default
TOGGLE = """
<script>
(function(){
  var ib=document.querySelector('.info-box'),
      cs=document.querySelector('.color-scale'),
      ctl=document.querySelector('.controls');
  if(ctl){
    function mk(txt,fn){ var b=document.createElement('button'); b.type='button';
      b.className='ctlbtn'; b.textContent=txt; b.onclick=fn; return b; }
    ctl.appendChild(mk('❓ Guida', function(){ if(ib) ib.classList.toggle('collapsed'); }));
    ctl.appendChild(mk('🎨 Scala', function(){ if(cs) cs.classList.toggle('collapsed'); }));
  }
  if(ib && !window.__INFO_OPEN__) ib.classList.add('collapsed');
  if(cs && !window.__SCALE_OPEN__) cs.classList.add('collapsed');
})();
</script>
"""

variants = {
  # Default pulito su entrambi: guida e scala CHIUSE (mostra subito i fondali, niente
  # pannelli che interferiscono). Si aprono on-demand coi pulsanti Guida/Scala.
  "Fronte_Tevere_MOBILE.html": "<script>window.__INFO_OPEN__=false;window.__SCALE_OPEN__=false;</script>",
  "Fronte_Tevere_IPAD.html":   "<script>window.__INFO_OPEN__=false;window.__SCALE_OPEN__=false;</script>",
}
for fn, flag in variants.items():
    html = base.replace("</body>", flag + TOGGLE + "</body>", 1)
    open(SRC + fn, "w", encoding="utf-8").write(html)
    print("scritto", fn, len(html)//1024, "KB",
          "| tune:", "mobtune" in html, "| toggle:", "__INFO_OPEN__" in html)
