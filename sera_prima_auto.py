# -*- coding: utf-8 -*-
"""
SERA-PRIMA AUTO - Ostia 2026. Campiona CHL/SST/corrente reali, ritara l'area,
genera una dashboard HTML per telefono e la PUBBLICA su GitHub Pages.
Pensato per girare da solo le sere del 25 e 26/6 (Task Scheduler).
URL fisso: https://marinovinc.github.io/OstiaSeraPrima/
"""
import sys, os, datetime, urllib.request, io, math, re, time, base64, subprocess
import numpy as np, tifffile
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from motore_decisionale import deriva_strategia, RIFERIMENTI  # motore: deriva la strategia dal dato, non copia il 21/6

REPO = os.path.dirname(os.path.abspath(__file__))
WMTS = "https://wmts.marine.copernicus.eu/teroWmts"
CHL = "OCEANCOLOUR_MED_BGC_L4_NRT_009_142/cmems_obs-oc_med_bgc-plankton_nrt_l4-gapfree-multi-1km_P1D_202207/CHL"
SST_L4  = "SST_MED_PHY_SUBSKIN_L4_NRT_010_036/cmems_obs-sst_med_phy-sst_nrt_diurnal-oi-0.0625deg_PT1H-m_202105/analysed_sst"
SST_L3A = "SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012/SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012_a_202311/sea_surface_temperature"
SST_L3B = "SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012/SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012_b_202311/sea_surface_temperature"
UO = "MEDSEA_ANALYSISFORECAST_PHY_006_013/cmems_mod_med_phy-cur_anfc_4.2km_P1D-m_202511/uo"
VO = "MEDSEA_ANALYSISFORECAST_PHY_006_013/cmems_mod_med_phy-cur_anfc_4.2km_P1D-m_202511/vo"
CORN = [(41.7037,12.0027),(41.5371,12.0981),(41.4776,11.8848),(41.6305,11.7738)]
W,Eb,S,N = 11.74,12.12,41.45,41.72
ROUTE_A = [("A1","N 41 40.200'","E 011 58.560'","593 m (approccio)"),
           ("A2","N 41 39.354'","E 011 57.762'","696 m (zona 21/6)"),
           ("A3","N 41 38.598'","E 011 57.006'","788 m"),
           ("A4","N 41 38.100'","E 011 56.508'","829 m"),
           ("A5","N 41 36.726'","E 011 55.128'","904 m")]

def tij(la,lo,z):
    n=2**z; x=(lo+180)/360*n; y=(1-math.asinh(math.tan(math.radians(la)))/math.pi)/2*n
    return z,int(y*256//256),int(x*256//256),int((x*256)%256),int((y*256)%256)
def samp(layer,la,lo,date,z=10):
    zz,row,col,i,j=tij(la,lo,z)
    url=(f"{WMTS}?service=WMTS&version=1.0.0&request=GetFeatureInfo&layer={layer}&style="
         f"&TileMatrixSet=EPSG:3857&TileMatrix={zz}&TileRow={row}&TileCol={col}&I={i}&J={j}&infoformat=text/xml&TIME={date}")
    try:
        t=urllib.request.urlopen(url,timeout=30).read().decode('utf-8','ignore')
        m=re.search(r'>([\-0-9.][0-9.eE\-]*)</',t); return float(m.group(1)) if m else None
    except Exception: return None
def samp_sst(la,lo,date):
    for lay,zz in ((SST_L3A,11),(SST_L3B,11),(SST_L4,10)):
        v=samp(lay,la,lo,date,zz)
        if v is not None: return v
    return None
def inpoly(la,lo,p=CORN):
    c=False;n=len(p);j=n-1
    for i in range(n):
        yi,xi=p[i];yj,xj=p[j]
        if((xi>lo)!=(xj>lo)) and (la<(yj-yi)*(lo-xi)/(xj-xi)+yi): c=not c
        j=i
    return c
def freshest():
    base=datetime.date.today()
    for k in range(1,9):
        d=(base-datetime.timedelta(days=k)).isoformat()
        if samp(CHL,41.66,11.95,d) is not None: return d
    return None

def run():
    date = sys.argv[1] if len(sys.argv)>1 else freshest()
    stamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    chl={}; sst={}; coolest=(None,None); chl_med=sst_med=None; cur=None; err=""
    try:
        glat=np.linspace(41.50,41.70,8); glon=np.linspace(11.80,12.05,8)
        for la in glat:
            for lo in glon:
                if not inpoly(la,lo): continue
                chl[(la,lo)]=samp(CHL,la,lo,date); time.sleep(0.1)
                sst[(la,lo)]=samp_sst(la,lo,date); time.sleep(0.1)
        cv=[v for v in chl.values() if v]; sv=[v-273.15 for v in sst.values() if v]
        chl_med=float(np.median(cv)) if cv else None
        sst_med=float(np.median(sv)) if sv else None
        coolest=min(((s-273.15,p) for p,s in sst.items() if s), default=(None,None))
        u=samp(UO,41.66,11.95,date); v=samp(VO,41.66,11.95,date)
        if u is not None and v is not None:
            cur=((u*u+v*v)**.5*1.94, math.degrees(math.atan2(u,v))%360)
    except Exception as e:
        err=str(e)[:120]

    # mappa
    png_b64=""
    try:
        em=("https://ows.emodnet-bathymetry.eu/wcs?service=WCS&version=2.0.1&request=GetCoverage"
            "&coverageId=emodnet__mean&format=image/tiff"f"&subset=Lat({S},{N})&subset=Long({W},{Eb})")
        A=tifffile.imread(io.BytesIO(urllib.request.urlopen(em,timeout=120).read())).astype(float)
        if A.ndim==3: A=A[...,0]
        A=np.where((A<0)&(A>-12000),A,np.nan); gh,gw=A.shape
        bl=N-(np.arange(gh)+0.5)/gh*(N-S); bo=W+(np.arange(gw)+0.5)/gw*(Eb-W)
        bm=np.array([[inpoly(bl[i],bo[j]) for j in range(gw)] for i in range(gh)])
        fig,ax=plt.subplots(figsize=(8,8))
        ax.imshow(np.where(bm,A,np.nan),extent=[W,Eb,S,N],origin='upper',cmap='Greys_r',alpha=.7,aspect='auto')
        if sst:
            la_=[p[0] for p,s in sst.items() if s]; lo_=[p[1] for p,s in sst.items() if s]; c_=[s-273.15 for s in sst.values() if s]
            if c_:
                sc=ax.scatter(lo_,la_,c=c_,cmap='coolwarm_r',s=120,edgecolor='k'); plt.colorbar(sc,ax=ax,shrink=.6,label='SST C (blu=freddo)')
        if coolest[1]: ax.plot(coolest[1][1],coolest[1][0],'*',color='cyan',mec='k',ms=22)
        poly=CORN+[CORN[0]]; ax.plot([c[1] for c in poly],[c[0] for c in poly],'b-',lw=2)
        ax.plot([11.9760,11.9627,11.9501,11.9418,11.9188],[41.6700,41.6559,41.6433,41.6350,41.6121],'r-o',ms=4,label='Rotta A')
        ax.legend(loc='lower left',fontsize=8); ax.set_title(f"SST {date} + Rotta A")
        b=io.BytesIO(); plt.savefig(b,format='png',dpi=110,bbox_inches='tight'); png_b64=base64.b64encode(b.getvalue()).decode()
    except Exception as e:
        err=(err+" | mappa: "+str(e)[:80]).strip(" |")

    # blocchi dinamici
    dyn=f"<p><b>CHL campo:</b> mediana {chl_med:.3f} mg/m³</p>" if chl_med else "<p>CHL: n/d</p>"
    if sst_med: dyn+=f"<p><b>SST campo:</b> mediana {sst_med:.2f} °C</p>"
    if coolest[0] is not None:
        an=coolest[0]-(sst_med or coolest[0])
        dyn+=f"<p><b>Banda fredda (upwelling):</b> {coolest[0]:.2f} °C @ {coolest[1][0]:.3f}/{coolest[1][1]:.3f} (anomalia {an:+.2f} °C)</p>"
    if cur: dyn+=f"<p><b>Corrente zona:</b> {cur[0]:.2f} kn → {cur[1]:.0f}°</p>"
    if coolest[1]:
        dyn+=(f'<div class="call info"><span class="lab">Area ritarata</span>Lavora la scarpata (Rotta A) verso la banda fredda '
              f'@ ~{coolest[1][0]:.3f}/{coolest[1][1]:.3f} nelle finestre. <b>Conferma la macchia fredda col sensore di bordo.</b></div>')
    if err: dyn+=f'<div class="call danger"><span class="lab">Nota</span>Alcuni dati non recuperati ({err}).</div>'
    rows="".join(f"<tr><td>{n}</td><td>{la}</td><td>{lo}</td><td>{d}</td></tr>" for n,la,lo,d in ROUTE_A)
    img=f"<img src='data:image/png;base64,{png_b64}'>" if png_b64 else "<p>(mappa non disponibile)</p>"

    # --- MOTORE: strategia DERIVATA dal dato di oggi (non copia il 21/6) ---
    strat_html=""
    try:
        # gradiente LOCALE di SST (C/km) tra punti adiacenti (~3 km): fronte vero, non range di campo
        pts=[(p[0],p[1],v-273.15) for p,v in sst.items() if v]; _grad=0.0
        for _i in range(len(pts)):
            for _j in range(_i+1,len(pts)):
                la1,lo1,t1=pts[_i]; la2,lo2,t2=pts[_j]
                _d=(((la2-la1)*111.32)**2+((lo2-lo1)*111.32*math.cos(math.radians((la1+la2)/2)))**2)**0.5
                if 0<_d<=3.5:
                    _g=abs(t1-t2)/_d
                    if _g>_grad: _grad=_g
        _anom=(coolest[0]-sst_med) if (coolest[0] is not None and sst_med is not None) else None
        strat=deriva_strategia(chl_med, _grad, _anom, (cur[0] if cur else None), None, "mattino", sst_med)
        strat_html=("".join(f'<p><b>{k}:</b> {strat[k.lower()]}</p>' for k in ("DOVE","QUOTA","COLORE","SPECIE","ASSETTO","SEGNI")))
        refs="".join(f'<li><a href="{u}">{t}</a></li>' for t,u in RIFERIMENTI)
        strat_html+=f'<div class="call"><span class="lab">Riferimenti verificati</span><ul>{refs}</ul></div>'
    except Exception as e:
        strat_html=f'<div class="call danger"><span class="lab">Motore</span>Strategia non derivata ({str(e)[:80]}).</div>'

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
.toc-n{font-family:"Fraunces",serif;font-style:italic;font-weight:600;font-size:1.5rem;color:var(--brass);width:26px;flex-shrink:0}
.toc-t{font-size:.92rem;font-weight:700;color:var(--navy)} .toc-d{font-size:.76rem;color:var(--ink-3);line-height:1.3}
section{margin:38px 0}
.sec-head{display:flex;align-items:baseline;gap:14px;border-bottom:2px solid var(--ink);padding-bottom:8px;margin-bottom:18px}
.sec-num{font-family:"Fraunces",serif;font-style:italic;font-weight:600;font-size:1.5rem;color:var(--brass)}
.sec-head h2{font-size:1.5rem}
.lead{font-size:1.05rem;color:var(--ink-2);margin:0 0 16px}
figure{margin:20px 0;background:var(--paper-2);border:1px solid var(--rule);border-radius:4px;padding:10px}
figure img{display:block;width:100%;height:auto;border-radius:2px}
figcaption{font-size:.8rem;color:var(--ink-3);margin-top:8px;font-style:italic;font-family:"Fraunces",serif}
.call{border-left:4px solid var(--brass);background:var(--bg-warn);padding:13px 16px;margin:16px 0;border-radius:0 3px 3px 0;font-size:.92rem}
.call.info{border-color:var(--sea);background:var(--bg-info)} .call.danger{border-color:var(--rust);background:var(--bg-danger)}
.call .lab{font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:.68rem;display:block;margin-bottom:4px;color:var(--ink-2)}
/* callout a scomparsa (guide/legende collassabili) */
.call>.lab{cursor:pointer;position:relative;padding-left:15px;-webkit-user-select:none;user-select:none}
.call>.lab::before{content:"";position:absolute;left:2px;top:.32em;border:5px solid transparent;border-left-color:var(--brass);transition:transform .15s}
.call:not(.collapsed)>.lab::before{transform:rotate(90deg)}
.call.collapsed .call-body{display:none}
table{width:100%;border-collapse:collapse;font-size:.84rem;margin:16px 0}
th,td{border:1px solid var(--rule);padding:6px 9px;text-align:left;vertical-align:top}
th{background:var(--navy);color:var(--paper-2);font-weight:600;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase}
tr:nth-child(even) td{background:var(--paper-2)}
td.num,th.num{font-family:"IBM Plex Mono",monospace}
.hot{color:var(--rust);font-weight:700}
ul{margin:10px 0;padding-left:22px} li{margin:5px 0}
.colophon{border-top:5px double var(--ink);margin-top:50px;padding-top:16px;font-size:.78rem;color:var(--ink-3);text-align:center}
@media(max-width:760px){.toc-grid{grid-template-columns:1fr}.mh-title{font-size:2.3rem}}
</style>"""
    head=('<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">'
          '<meta name="viewport" content="width=device-width,initial-scale=1">'
          '<title>Ostia 2026 - Sera prima</title>'
          '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,600&family=Public+Sans:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')
    body=f"""</head><body><div class="wrap">
<div class="masthead">
 <div class="mh-kicker">ASD IschiaFishing &middot; Report sera-prima</div>
 <h1 class="mh-title">Ostia 2026</h1>
 <div class="mh-sub">Campionato Italiano Traina d'Altura &middot; area ritarata col dato satellitare fresco</div>
 <div class="dateline"><span>Aggiornato &middot; {stamp}</span><span>Dato &middot; Copernicus {date}</span><span>Auto &middot; pubblicato</span></div>
</div>
<div class="call"><span class="lab">Dossier completo</span><a href="dossier.html">&rarr; Apri il dossier tattico con tutti i contenuti</a> (regolamento, calibrazione 21/6, struttura, rotte, tecnica).</div>
<div class="toc-h">Sommario</div>
<div class="toc-grid">
 <a class="toc-card" href="#s1"><span class="toc-n">I</span><span><span class="toc-t">Finestre d'oro</span><br><span class="toc-d">quando essere sullo spot</span></span></a>
 <a class="toc-card" href="#s2"><span class="toc-n">II</span><span><span class="toc-t">Dato fresco</span><br><span class="toc-d">CHL/SST/corrente + area</span></span></a>
 <a class="toc-card" href="#s3"><span class="toc-n">III</span><span><span class="toc-t">Rotta A</span><br><span class="toc-d">waypoint 700-900 m</span></span></a>
 <a class="toc-card" href="#s4"><span class="toc-n">IV</span><span><span class="toc-t">Come</span><br><span class="toc-d">esca, tecnica, punteggio</span></span></a>
</div>
<section id="s1"><div class="sec-head"><span class="sec-num">I</span><h2>Finestre d'oro</h2></div>
 <p class="lead">Essere sul tratto migliore (Rotta A) in questa finestra: solunare + marea in riflusso + mare ancora calmo.</p>
 <table><tr><th>Manche</th><th>Finestra</th></tr><tr><td>Ven 26</td><td class="num hot">09:15-11:15</td></tr><tr><td>Sab 27</td><td class="num hot">10:00-12:00</td></tr></table>
</section>
<section id="s2"><div class="sec-head"><span class="sec-num">II</span><h2>Dato fresco del {date}</h2></div>
 {dyn}
 <figure>{img}<figcaption>SST del campo + banda fredda (stella ciano) + Rotta A (rosso).</figcaption></figure>
</section>
<section id="s3"><div class="sec-head"><span class="sec-num">III</span><h2>Rotta A - scarpata (700-900 m)</h2></div>
 <p class="lead">Linea rossa georeferenziata e validata per profondita'. Tratto migliore <b>A2-A4</b>.</p>
 <table><tr><th>WP</th><th>Lat</th><th>Lon</th><th>Fondale</th></tr>{rows}</table>
</section>
<section id="s4"><div class="sec-head"><span class="sec-num">IV</span><h2>Strategia derivata dal dato (non copia il 21/6)</h2></div>
 <p class="lead">Il motore deriva la strategia dalle condizioni di oggi, su basi <b>verificate</b>; le esche/colori NON verificati restano spunti, non regole.</p>
 {strat_html}
 <ul><li><b>Tecnica:</b> stop-and-go sulla scarpata, 6,2-7,2 kn.</li><li><b>Punteggio:</b> tonno rosso 1200 (x2), il resto 600; <b>cala presto</b> (lo spareggio premia chi ferra per primo).</li><li><b>Regole:</b> C&amp;R, video, ferrata fuori campo = nulla, 370 m tra barche.</li></ul>
 <div class="call danger"><span class="lab">Attenzione</span>SST L3 ~1 km (fallback L4): la macchia fredda va <b>confermata col sensore di bordo</b>. Le soglie del motore sono iniziali, non validate.</div>
</section>
<div class="colophon">Report sera-prima Ostia 2026 &middot; ASD IschiaFishing<br>Copernicus CMEMS &middot; EMODnet &middot; auto-aggiornato &middot; dato {date}</div>
</div>
<script>
document.querySelectorAll('.call').forEach(function(c){{
 var lab=c.querySelector('.lab'); if(!lab) return;
 var body=document.createElement('div'); body.className='call-body';
 while(lab.nextSibling){{ body.appendChild(lab.nextSibling); }}
 c.appendChild(body); c.classList.add('collapsed');
 lab.addEventListener('click',function(){{ c.classList.toggle('collapsed'); }});
}});
</script>
</body></html>"""
    html = head + CSS + body
    open(os.path.join(REPO,"index.html"),"w",encoding="utf-8").write(html)
    open(os.path.join(REPO,f"report_{date}.html"),"w",encoding="utf-8").write(html)

    # COPIA AUTONOMA (offline: rimuove i font CDN -> nessuna risorsa esterna). Salvata FUORI dal repo
    # cosi' NON viene pubblicata su GitHub: e' un file locale da portare in barca offline.
    try:
        auton = re.sub(r'<link[^>]*fonts\.g[^>]*>','',html)
        ext_dir = r"D:/claude_handoff/outbox/Roma_pesca_campionato_2026"
        if os.path.isdir(ext_dir):
            open(os.path.join(ext_dir,"REPORT_sera_prima_autonomo.html"),"w",encoding="utf-8").write(auton)
            print("AUTONOMO salvato (locale, non su GitHub):", os.path.join(ext_dir,"REPORT_sera_prima_autonomo.html"))
    except Exception as e:
        print("autonomo:", e)

    # PUBLISH
    try:
        subprocess.run(["git","-C",REPO,"add","-A"],check=True,timeout=60)
        subprocess.run(["git","-C",REPO,"commit","-q","-m",f"sera-prima {date} ({stamp})"],check=True,timeout=60)
        subprocess.run(["git","-C",REPO,"push","-q","origin","HEAD"],check=True,timeout=120)
        print("PUBLISHED:", date)
    except Exception as e:
        print("PUSH FALLITO:", e)

if __name__=="__main__": run()
