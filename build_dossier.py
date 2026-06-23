# -*- coding: utf-8 -*-
"""Costruisce il DOSSIER TATTICO completo (tutti i contenuti) in HTML nello
standard template_briefing.html, autoportante (immagini base64), e lo pubblica.
Output: dossier.html nel repo OstiaSeraPrima."""
import os, base64, subprocess, re
REPO = os.path.dirname(os.path.abspath(__file__))
SRC  = "D:/claude_handoff/outbox/Roma_pesca_campionato_2026/"

def img64(name):
    p = os.path.join(SRC, name)
    if not os.path.exists(p): return ""
    return "data:image/png;base64," + base64.b64encode(open(p,"rb").read()).decode()

IM_ROTTE  = img64("ROTTE_OSTIA_2026_mappa.png")
IM_HEAT   = img64("TATTICA_26-27_2D.png")
IM_PROF   = img64("PROFILO_3D_zona_21-06.png")
IM_RA     = img64("ROTTA_A_mappa.png")
IM_RB     = img64("ROTTA_B_mappa.png")
IM_RC     = img64("ROTTA_C_mappa.png")

CSS = """<style>
:root{--paper:#F1ECDE;--paper-2:#FAF6E8;--paper-3:#ECE5D2;--ink:#181715;--ink-2:#4A4842;--ink-3:#7F7C73;--rule:#C9BFA8;--navy:#0E2A40;--navy-2:#1F4660;--sea:#2D6E5F;--brass:#9C6D14;--rust:#9A3A1C;--bg-warn:#FBF3E0;--bg-info:#E8F0EE;--bg-danger:#F7E9E2;}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--paper);color:var(--ink);font-family:"Public Sans",sans-serif;font-size:15px;line-height:1.6}
body{background-image:radial-gradient(rgba(120,100,70,.04) 1px,transparent 1px),radial-gradient(rgba(120,100,70,.03) 1px,transparent 1px);background-size:24px 24px,13px 13px;background-position:0 0,7px 7px}
.wrap{max-width:920px;margin:0 auto;padding:26px 22px 60px}
h1,h2,h3,h4{font-family:"Fraunces",serif;font-weight:500;color:var(--ink);letter-spacing:-.01em;margin:0}
.num{font-family:"IBM Plex Mono",monospace}
a{color:var(--navy-2)}
.masthead{border-top:5px double var(--ink);border-bottom:1px solid var(--ink);padding:14px 0 16px;margin-bottom:8px}
.mh-kicker{text-align:center;letter-spacing:.32em;font-size:.68rem;text-transform:uppercase;color:var(--brass);font-weight:700;margin-bottom:10px}
.mh-title{text-align:center;font-size:3.2rem;line-height:1.02;color:var(--navy)}
.mh-sub{text-align:center;color:var(--ink-2);font-size:1rem;margin-top:8px;font-style:italic;font-family:"Fraunces",serif}
.dateline{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:7px 2px;margin:14px 0 0;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.toc-h{text-align:center;font-family:"Fraunces",serif;font-style:italic;font-size:1.6rem;color:var(--navy);margin:28px 0 16px}
.toc-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.toc-card{display:flex;gap:13px;align-items:flex-start;padding:13px 15px;background:var(--paper-2);border:1px solid var(--rule);border-left:4px solid var(--brass);border-radius:3px;text-decoration:none;color:inherit}
.toc-n{font-family:"Fraunces",serif;font-style:italic;font-weight:600;font-size:1.5rem;color:var(--brass);width:30px;flex-shrink:0}
.toc-t{font-size:.92rem;font-weight:700;color:var(--navy)} .toc-d{font-size:.76rem;color:var(--ink-3);line-height:1.3}
section{margin:38px 0}
.sec-head{display:flex;align-items:baseline;gap:14px;border-bottom:2px solid var(--ink);padding-bottom:8px;margin-bottom:18px}
.sec-num{font-family:"Fraunces",serif;font-style:italic;font-weight:600;font-size:1.5rem;color:var(--brass)}
.sec-head h2{font-size:1.5rem}
.lead{font-size:1.05rem;color:var(--ink-2);margin:0 0 16px}
.lead .drop{float:left;font-family:"Fraunces",serif;font-size:3.1rem;line-height:.8;padding:6px 10px 0 0;color:var(--rust)}
figure{margin:20px 0;background:var(--paper-2);border:1px solid var(--rule);border-radius:4px;padding:10px}
figure img{display:block;width:100%;height:auto;border-radius:2px}
figcaption{font-size:.8rem;color:var(--ink-3);margin-top:8px;font-style:italic;font-family:"Fraunces",serif}
.call{border-left:4px solid var(--brass);background:var(--bg-warn);padding:13px 16px;margin:16px 0;border-radius:0 3px 3px 0;font-size:.92rem}
.call.info{border-color:var(--sea);background:var(--bg-info)} .call.danger{border-color:var(--rust);background:var(--bg-danger)}
.call .lab{font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:.68rem;display:block;margin-bottom:4px;color:var(--ink-2)}
table{width:100%;border-collapse:collapse;font-size:.84rem;margin:16px 0}
th,td{border:1px solid var(--rule);padding:6px 9px;text-align:left;vertical-align:top}
th{background:var(--navy);color:var(--paper-2);font-weight:600;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase}
tr:nth-child(even) td{background:var(--paper-2)}
td.num,th.num{font-family:"IBM Plex Mono",monospace}
.hot{color:var(--rust);font-weight:700}
.tag{display:inline-block;font-size:.64rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:2px 7px;border-radius:10px;background:var(--navy);color:var(--paper-2)}
ul{margin:10px 0;padding-left:22px} li{margin:5px 0}
.colophon{border-top:5px double var(--ink);margin-top:50px;padding-top:16px;font-size:.78rem;color:var(--ink-3);text-align:center}
@media(max-width:760px){.toc-grid{grid-template-columns:1fr}.mh-title{font-size:2.3rem}}
</style>"""

HEAD = ('<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>Dossier tattico - Ostia 2026</title>'
 '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,600&family=Public+Sans:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')

BODY = """</head><body><div class="wrap">

<div class="masthead">
 <div class="mh-kicker">ASD IschiaFishing &middot; Dossier tattico</div>
 <h1 class="mh-title">Ostia 2026</h1>
 <div class="mh-sub">62&deg; Campionato Italiano Assoluto di Traina d'Altura &middot; tutti i contenuti</div>
 <div class="dateline"><span>Manche &middot; Ven 26 + Sab 27/6</span><span>Fonti &middot; FIPSAS, Capitaneria, Copernicus, EMODnet</span><span>Autore &middot; ASD IschiaFishing</span></div>
</div>

<div class="toc-h">Sommario</div>
<div class="toc-grid">
 <a class="toc-card" href="#s1"><span class="toc-n">I</span><span><span class="toc-t">Gara, campo e punteggio</span><br><span class="toc-d">regolamento, coordinate ufficiali, coefficienti</span></span></a>
 <a class="toc-card" href="#s2"><span class="toc-n">II</span><span><span class="toc-t">Il giorno-verita' (21/6)</span><br><span class="toc-d">tutti i parametri ambientali misurati</span></span></a>
 <a class="toc-card" href="#s3"><span class="toc-n">III</span><span><span class="toc-t">Struttura & linea rossa</span><br><span class="toc-d">zona georeferenziata e validata</span></span></a>
 <a class="toc-card" href="#s4"><span class="toc-n">IV</span><span><span class="toc-t">Modello & proiezione</span><br><span class="toc-d">finestre d'oro 26-27</span></span></a>
 <a class="toc-card" href="#s5"><span class="toc-n">V</span><span><span class="toc-t">Le rotte (A/B/C)</span><br><span class="toc-d">waypoint, GPX, mappa</span></span></a>
 <a class="toc-card" href="#s6"><span class="toc-n">VI</span><span><span class="toc-t">Come: spread & tecnica</span><br><span class="toc-d">esca, assetto, punteggio</span></span></a>
 <a class="toc-card" href="#s7"><span class="toc-n">VII</span><span><span class="toc-t">Sera-prima (auto)</span><br><span class="toc-d">report fresco che si aggiorna da solo</span></span></a>
</div>

<section id="s1"><div class="sec-head"><span class="sec-num">I</span><h2>Gara, campo e punteggio</h2></div>
 <p class="lead"><span class="drop">D</span>ue manche, <b>Ven 26 + Sab 27 giugno</b>, ore <b>08:00&ndash;15:00</b>. Solo <b>Catch &amp; Release</b>, video obbligatorio. Campo ufficiale (Ordinanza Capitaneria di Roma):</p>
 <table><tr><th>Vertice</th><th>Latitudine</th><th>Longitudine</th></tr>
  <tr><td>A (NE)</td><td class="num">41&deg; 42,222' N</td><td class="num">012&deg; 00,163' E</td></tr>
  <tr><td>B (SE)</td><td class="num">41&deg; 32,224' N</td><td class="num">012&deg; 05,885' E</td></tr>
  <tr><td>C (S)</td><td class="num">41&deg; 28,657' N</td><td class="num">011&deg; 53,087' E</td></tr>
  <tr><td>D (W)</td><td class="num">41&deg; 37,827' N</td><td class="num">011&deg; 46,426' E</td></tr></table>
 <p>Punteggio = bonus pesce (g)/10 &times; coefficiente. <b>Conta la specie e il numero di ferrate</b>, non il peso.</p>
 <table><tr><th>Specie</th><th>Mis. min</th><th class="num">Punti</th></tr>
  <tr><td><b>Tonno rosso</b></td><td>80 cm</td><td class="num hot">1.200</td></tr>
  <tr><td>Aguglia imp. / spada / marlin bianco</td><td>130 cm</td><td class="num">600</td></tr>
  <tr><td>Alalunga / tonno striato / alletterato / lampuga</td><td>60 cm</td><td class="num">600</td></tr>
  <tr><td>Altri pesci sportivi</td><td>60 cm</td><td class="num">300</td></tr>
  <tr><td>Sottomisura (specie elencate)</td><td>&mdash;</td><td class="num">1</td></tr></table>
 <div class="call info"><span class="lab">In sintesi</span>Vince il <b>numero di ferrate valide</b> + il <b>tonno rosso (&times;2)</b> come turbo e re dello spareggio. <b>Cala presto:</b> a parita', vince chi ferra per primo.</div>
 <div class="call"><span class="lab">Regole chiave</span>Max <b>7 canne</b>, lenza unica <b>15 kg</b>, solo <b>artificiali</b> (no vivo), divergenti di superficie e profondita' ammessi. <b>370 m</b> minimo tra barche; <b>ferrata fuori campo = nulla</b>.</div>
</section>

<section id="s2"><div class="sec-head"><span class="sec-num">II</span><h2>Il giorno-verita': Domenica 21/6</h2></div>
 <p class="lead"><span class="drop">L</span>a calibrazione del modello: un giorno con catture note (zona di Silvio Riccardi), di cui abbiamo ricostruito <b>tutti i parametri reali</b>. Si e' pescato nel <b>blu profondo (&gt;700 m)</b>, sulla scarpata.</p>
 <table><tr><th>Parametro</th><th>Valore 21/6</th><th>Fonte</th></tr>
  <tr><td>Sole</td><td class="num">alba 05:37 &middot; tram. 20:50</td><td>effemeridi</td></tr>
  <tr><td>Luna</td><td class="num">45% crescente</td><td>effemeridi</td></tr>
  <tr><td>Solunare maggiore</td><td class="num hot">05:40&ndash;07:40 (alba)</td><td>antitransito 06:39</td></tr>
  <tr><td>Vento</td><td>mattino calmo (NE 1&ndash;4 kn) &rarr; brezza O pom. ~8 kn</td><td>Open-Meteo</td></tr>
  <tr><td>Pressione</td><td class="num">1021&ndash;1023 hPa (alta, stabile)</td><td>Open-Meteo</td></tr>
  <tr><td>Mare</td><td class="num">piatto (&lt;0,10 m)</td><td>Open-Meteo Marine</td></tr>
  <tr><td>SST</td><td class="num">25,85 &deg;C &middot; banda fredda &minus;0,15 &deg;C</td><td>Copernicus L4/L3</td></tr>
  <tr><td>Clorofilla</td><td class="num">0,05 mg/m&sup3; (blu)</td><td>Copernicus MED L4</td></tr>
  <tr><td>Corrente</td><td class="num">0,24 kn verso S</td><td>Copernicus phy</td></tr>
  <tr><td>Marea</td><td class="num">bassa 09:09 &rarr; alta 15:26 (escurs. 0,2 m)</td><td>tides4fishing</td></tr></table>
 <div class="call info"><span class="lab">Lettura</span>Giornata a <b>segnali deboli</b>: blu profondo, CHL piatta, banda fredda di pochi decimi. Le catture si spiegano come <b>tempistica (alba/solunare) + scarpata + mare calmo</b>, non un fronte forte.</div>
 <div class="call"><span class="lab">Secondo punto di calibrazione</span>La <b>vittoria a Forio</b> (stesso 21/6, regolamento identico) e' arrivata su <b>strutture</b> nelle <b>finestre solunari</b> &rarr; corrobora lo schema <b>struttura + finestra</b>.</div>
</section>

<section id="s3"><div class="sec-head"><span class="sec-num">III</span><h2>Struttura del fondo & linea rossa</h2></div>
 <p class="lead"><span class="drop">L</span>a zona di pesca (linea rossa del plotter) e' stata <b>georeferenziata e validata per profondita'</b>: tracciando la scarpata dal check-point sul DTM EMODnet, i fondali calcolati combaciano con quelli del plotter.</p>
 <table><tr><th>Plotter</th><th class="num">EMODnet</th><th>Posizione</th></tr>
  <tr><td>789 m</td><td class="num">&minus;788 m</td><td class="num">41.6433 / 11.9501</td></tr>
  <tr><td>827 m</td><td class="num">&minus;829 m</td><td class="num">41.6350 / 11.9418</td></tr>
  <tr><td>901 m</td><td class="num">&minus;904 m</td><td class="num">41.6121 / 11.9188</td></tr></table>
 <p><b>Zona di pesca (&gt;700 m):</b> dal punto <span class="num">41.6559 / 11.9627</span> al punto <span class="num">41.6121 / 11.9188</span>, ~6 km a SW del check-point.</p>
 __FIG_PROF__
 <div class="call danger"><span class="lab">Caveat anchor</span>Al check-point: plotter 466 m vs EMODnet 393 m (su pendio ripido). La posizione assoluta ha ~poche centinaia di m d'incertezza; la zona profonda resta fissata dai fondali (validati).</div>
</section>

<section id="s4"><div class="sec-head"><span class="sec-num">IV</span><h2>Modello & proiezione 26&ndash;27</h2></div>
 <p class="lead"><span class="drop">L</span>e finestre d'oro cadono <b>dentro l'orario di gara</b>: solunare maggiore + marea in riflusso + mare ancora calmo.</p>
 <table><tr><th>Manche</th><th>Finestra d'oro</th><th>Luna</th><th>Marea</th></tr>
  <tr><td>Ven 26</td><td class="num hot">09:15&ndash;11:15</td><td>89% gibbosa</td><td>alta 07:53 &rarr; riflusso</td></tr>
  <tr><td>Sab 27</td><td class="num hot">10:00&ndash;12:00</td><td>94% gibbosa</td><td>alta 08:41 &rarr; riflusso</td></tr></table>
 __FIG_HEAT__
 <div class="call info"><span class="lab">Area</span>Primaria: la <b>scarpata profonda</b> (zona 21/6) + le secche W (banco &minus;687 m). Da <b>ritarare la sera prima</b> col dato fresco (sez. VII).</div>
</section>

<section id="s5"><div class="sec-head"><span class="sec-num">V</span><h2>Le rotte</h2></div>
 <p class="lead"><span class="drop">T</span>re rotte, tutti i waypoint <b>verificati dentro il campo</b>. Assegnabili alle <b>3 barche del club</b> (A/B/C), con ferrate condivise via radio. GPX da caricare sul plotter: <span class="num">ROTTE_OSTIA_2026.gpx</span>.</p>
 __FIG_ROTTE__

 <div class="sec-head" style="margin-top:26px;border-bottom-width:1px"><span class="sec-num" style="font-size:1.15rem">A</span><h2 style="font-size:1.2rem">Scarpata 21/6 <span class="tag b">primaria</span></h2></div>
 <p>Transetto sulla <b>linea rossa georeferenziata e validata</b>: scende la scarpata dove si &egrave; pescato il 21/6, tagliando le quote da ~590 a ~900 m, l&rsquo;orlo dove i pelagici seguono il foraggio sul break.</p>
 <ul>
  <li><b>Quando:</b> prima scelta; soprattutto a <b>segnale debole</b> (struttura dominante) o per restare sull&rsquo;acqua provata.</li>
  <li><b>Target:</b> alalunga / tunnidi (600) sul tratto <b>A2&ndash;A4 (700&ndash;830 m)</b>; tonno rosso (1200) sulla canna profonda; spada nel profondo. A1 = approccio/cala spread, A5 = orlo profondo.</li>
  <li><b>Tecnica:</b> stop-and-go sull&rsquo;orlo, zigzag sui due lati della scarpata.</li>
 </ul>
 <table><tr><th>WP</th><th>Lat</th><th>Lon</th><th>Fondale</th></tr>
  <tr><td>A1</td><td class="num">N 41 40.200'</td><td class="num">E 011 58.560'</td><td>593 m (approccio)</td></tr>
  <tr><td>A2</td><td class="num">N 41 39.354'</td><td class="num">E 011 57.762'</td><td>696 m (zona 21/6)</td></tr>
  <tr><td>A3</td><td class="num">N 41 38.598'</td><td class="num">E 011 57.006'</td><td>788 m</td></tr>
  <tr><td>A4</td><td class="num">N 41 38.100'</td><td class="num">E 011 56.508'</td><td>829 m</td></tr>
  <tr><td>A5</td><td class="num">N 41 36.726'</td><td class="num">E 011 55.128'</td><td>904 m</td></tr></table>
 __FIG_RA__

 <div class="sec-head" style="margin-top:26px;border-bottom-width:1px"><span class="sec-num" style="font-size:1.15rem">B</span><h2 style="font-size:1.2rem">Banco &minus;687 m + dorsali W</h2></div>
 <p>Le <b>vere strutture</b> del settore W del campo (banco e dorsali a ~700 m): per <b>aggregazione</b> [R1, Weber 2025] concentrano i predatori. Si lavorano gli <b>orli</b> di banco e dorsali.</p>
 <ul>
  <li><b>Quando:</b> quando banco/dorsali sono pi&ugrave; vicini alla <b>macchia fredda/fronte del giorno</b>, o per cercare il pezzo grosso sulla struttura netta.</li>
  <li><b>Target:</b> tonno rosso (1200) e alalunga sugli orli; spada nel profondo adiacente (B1 &minus;935 m).</li>
  <li><b>Tecnica:</b> passate ravvicinate sugli orli del banco, stop-and-go.</li>
 </ul>
 <table><tr><th>WP</th><th>Lat</th><th>Lon</th><th>Fondale</th></tr>
  <tr><td>B1</td><td class="num">N 41 35.100'</td><td class="num">E 011 51.720'</td><td>935 m (approccio)</td></tr>
  <tr><td>B2</td><td class="num">N 41 33.852'</td><td class="num">E 011 51.240'</td><td>687 m (banco)</td></tr>
  <tr><td>B3</td><td class="num">N 41 35.520'</td><td class="num">E 011 50.160'</td><td>705 m</td></tr>
  <tr><td>B4</td><td class="num">N 41 37.020'</td><td class="num">E 011 50.280'</td><td>700 m</td></tr>
  <tr><td>B5</td><td class="num">N 41 38.220'</td><td class="num">E 011 49.800'</td><td>700 m</td></tr></table>
 __FIG_RB__

 <div class="sec-head" style="margin-top:26px;border-bottom-width:1px"><span class="sec-num" style="font-size:1.15rem">C</span><h2 style="font-size:1.2rem">Transetto ampio</h2></div>
 <p>Copre <b>scarpata (NE) e banco (SW)</b> in un transetto diagonale: per la barca che vuole <b>leggere tutto il campo</b> in una passata.</p>
 <ul>
  <li><b>Quando:</b> giornata di <b>ricerca</b>, quando non sai dove sia il pesce, o come manche d&rsquo;esplorazione.</li>
  <li><b>Target:</b> spread completo, copri tutta la colonna.</li>
  <li><b>Nota:</b> <b>C4 (&minus;1063 m) &egrave; solo transito</b> (fondo piatto, non in pesca): attraversi la fossa per passare da scarpata a banco.</li>
 </ul>
 <table><tr><th>WP</th><th>Lat</th><th>Lon</th><th>Fondale</th></tr>
  <tr><td>C1</td><td class="num">N 41 40.200'</td><td class="num">E 011 58.560'</td><td>593 m</td></tr>
  <tr><td>C2</td><td class="num">N 41 38.598'</td><td class="num">E 011 57.006'</td><td>788 m (zona 21/6)</td></tr>
  <tr><td>C3</td><td class="num">N 41 37.200'</td><td class="num">E 011 54.300'</td><td>931 m</td></tr>
  <tr><td>C4</td><td class="num">N 41 35.400'</td><td class="num">E 011 52.320'</td><td>1063 m (transito)</td></tr>
  <tr><td>C5</td><td class="num">N 41 33.852'</td><td class="num">E 011 51.240'</td><td>687 m (banco)</td></tr></table>
 __FIG_RC__
</section>

<section id="s6"><div class="sec-head"><span class="sec-num">VI</span><h2>Come: spread & tecnica</h2></div>
 <p class="lead"><span class="drop">C</span>opri la colonna d'acqua; le scelte di esca/colore qui sotto sono solo quelle <b>verificate</b>.</p>
 <ul>
  <li><b>Colore esca [VERIFICATO, R4]:</b> sulle canne profonde preferisci <b>blu/verde/glow</b> (il rosso/arancio svanisce ~5 m); in acqua torbida conta il <b>contrasto</b>. In acqua limpida non esiste una regola di colore verificata.</li>
  <li><b>Spread 7 canne:</b> flat / rigger / shotgun + <b>1&ndash;2 canne profonde</b> (divergenti di profondita') per battere la colonna nel blu.</li>
  <li><b>Tecnica:</b> <b>stop-and-go sulla scarpata</b>, velocita' 6,2&ndash;7,2 kn, zigzag sui due lati dell'orlo.</li>
  <li><b>Piano orario:</b> cala spread ~08:30 &rarr; massima concentrazione nella <b>finestra</b> &rarr; segui le ferrate radio &rarr; ultima passata ~14:30.</li>
 </ul>
 <div class="call danger"><span class="lab">Esca non verificata</span>Il "minnow ~5 cm sotto la superficie + bianco/viola" del 21/6 e' un <b>ANEDDOTO riferito da terzi</b> (Aldo/Silvio), <b>non verificato</b>: spunto, NON una regola da assumere.</div>
 <div class="call"><span class="lab">Punteggio operativo</span>Tonno rosso 1200 (&times;2), il resto 600. <b>Cala presto</b> (spareggio). Aggancia <b>taglia valida</b> (tonno &ge;80, aguglia &ge;130).</div>
</section>

<section id="s7"><div class="sec-head"><span class="sec-num">VII</span><h2>Sera-prima (si aggiorna da solo)</h2></div>
 <p class="lead"><span class="drop">I</span>l report fresco si ricampiona da solo e si pubblica: lo apri dal telefono, anche a Ostia senza PC.</p>
 <p><b>Link:</b> <a href="https://marinovinc.github.io/OstiaSeraPrima/">marinovinc.github.io/OstiaSeraPrima</a></p>
 <ul>
  <li>Ricampiona <b>CHL / SST (1 km) / corrente</b> reali e ritara l'area verso l'eventuale banda fredda.</li>
  <li>Si aggiorna le <b>sere del 25 e 26 (20:00)</b> e le <b>mattine di gara 26 e 27 (06:30)</b>.</li>
 </ul>
 <div class="call danger"><span class="lab">Onesta'</span>Modello calibrato su un giorno a segnali deboli &rarr; priorita' a <b>struttura + timing</b>. La macchia fredda va <b>confermata col sensore di bordo</b>. Nessun piano di pesca garantisce le catture.</div>
</section>

<div class="colophon">
 Dossier tattico Ostia 2026 &middot; ASD IschiaFishing<br>
 Fonti: Regolamento FIPSAS, Ordinanza Capitaneria di Roma, Copernicus CMEMS, EMODnet DTM 2024, Open-Meteo, tides4fishing &middot; tutti i dati verificati o dichiarati
</div>
</div></body></html>"""

def fig(b64, cap):
    return (f'<figure><img src="{b64}" alt="{cap}"><figcaption>{cap}</figcaption></figure>') if b64 else f'<p><i>({cap} &mdash; immagine non disponibile)</i></p>'

body = (BODY
  .replace("__FIG_PROF__",  fig(IM_PROF,  "Profilo 2D+3D della scarpata del 21/6 (EMODnet DTM): si pesca sul pendio, non su una secca."))
  .replace("__FIG_HEAT__",  fig(IM_HEAT,  "Heatmap di probabilita' (rosso = scarpata 700-900 m) con marker zona 21/6 e secche W."))
  .replace("__FIG_ROTTE__", fig(IM_ROTTE, "Le 3 rotte sulla batimetria del campo: A (scarpata, rosso), B (banco/dorsali, magenta), C (transetto, verde)."))
  .replace("__FIG_RA__", fig(IM_RA, "Rotta A in dettaglio: la scarpata, dai 593 m (A1) ai 904 m (A5)."))
  .replace("__FIG_RB__", fig(IM_RB, "Rotta B in dettaglio: banco -687 m e dorsali W (~700 m)."))
  .replace("__FIG_RC__", fig(IM_RC, "Rotta C in dettaglio: transetto scarpata->banco (C4 = transito sulla fossa).")))

html = HEAD + CSS + body
open(os.path.join(REPO,"dossier.html"),"w",encoding="utf-8").write(html)
print("dossier.html scritto (%d KB)" % (len(html)//1024))
# copia AUTONOMA (offline, no font CDN) fuori dal repo -> NON pubblicata su GitHub
try:
    auton = re.sub(r'<link[^>]*fonts\.g[^>]*>','',html)
    if os.path.isdir(SRC):
        open(os.path.join(SRC,"DOSSIER_OSTIA_2026_autonomo.html"),"w",encoding="utf-8").write(auton)
        print("DOSSIER autonomo salvato (locale):", os.path.join(SRC,"DOSSIER_OSTIA_2026_autonomo.html"))
except Exception as e:
    print("autonomo:", e)
try:
    subprocess.run(["git","-C",REPO,"add","dossier.html","build_dossier.py"],check=True,timeout=60)
    subprocess.run(["git","-C",REPO,"commit","-q","-m","dossier completo (template)"],check=True,timeout=60)
    subprocess.run(["git","-C",REPO,"push","-q","origin","HEAD"],check=True,timeout=120)
    print("PUBLISHED: dossier.html")
except Exception as e:
    print("PUSH:", e)
