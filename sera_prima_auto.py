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
        dyn+=(f"<div class='hot'><b>AREA RITARATA:</b> lavora la scarpata (Rotta A) verso la banda fredda "
              f"@ ~{coolest[1][0]:.3f}/{coolest[1][1]:.3f} nelle finestre. Conferma la macchia fredda col sensore di bordo.</div>")
    if err: dyn+=f"<p style='color:#e88'>Nota: alcuni dati non recuperati ({err}).</p>"
    rows="".join(f"<tr><td>{n}</td><td>{la}</td><td>{lo}</td><td>{d}</td></tr>" for n,la,lo,d in ROUTE_A)
    img=f"<img src='data:image/png;base64,{png_b64}'>" if png_b64 else "<p>(mappa non disponibile)</p>"

    html=f"""<!doctype html><html lang=it><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Ostia 2026 — Sera prima</title><style>
body{{margin:0;background:#0b1626;color:#e3ecf7;font-family:system-ui,Arial;line-height:1.45}}
.wrap{{max-width:760px;margin:0 auto;padding:14px}}
h1{{font-size:20px;margin:6px 0}} h2{{font-size:16px;color:#7fd1ff;border-bottom:1px solid #24405e;padding-bottom:4px;margin-top:22px}}
.win{{background:#13314a;border-radius:10px;padding:10px 12px;margin:8px 0;font-size:18px;font-weight:700}}
.hot{{background:#5a1d1d;border-radius:8px;padding:8px 10px;margin:8px 0}}
table{{width:100%;border-collapse:collapse;font-size:13px}} td,th{{border:1px solid #24405e;padding:4px 6px;text-align:left}}
img{{max-width:100%;height:auto;border-radius:8px;background:#fff;margin-top:8px}}
small{{color:#9fb3cc}}</style></head><body><div class=wrap>
<h1>🎣 Ostia 2026 — Report sera-prima</h1>
<small>Aggiornato: {stamp} · dato Copernicus del <b>{date}</b> · auto-pubblicato</small>

<h2>Finestre d'oro (essere sullo spot)</h2>
<div class=win>Ven 26: <b>09:15–11:15</b></div>
<div class=win>Sab 27: <b>10:00–12:00</b></div>

<h2>Dato fresco del {date}</h2>
{dyn}
{img}

<h2>Rotta A — scarpata (linea rossa, 700–900 m)</h2>
<table><tr><th>WP</th><th>Lat</th><th>Lon</th><th>Fondale</th></tr>{rows}</table>
<small>Tratto migliore A2–A4. WP verificati dentro il campo, validati per profondità.</small>

<h2>Come</h2>
<p><b>Esca:</b> minnow shallow-runner tarato per lavorare a <b>~5 cm sotto la superficie</b> + octopus/kona <b>bianco e viola</b> + 1–2 canne profonde (divergenti di profondità).</p>
<p><b>Tecnica:</b> stop-and-go sulla scarpata, 6,2–7,2 kn. <b>Punteggio:</b> tonno rosso 1200 (×2), il resto 600; <b>cala presto</b> (lo spareggio premia chi ferra per primo). C&R, video, ferrata fuori campo = nulla, 370 m tra barche.</p>
<small>SST L3 ~1 km (fallback L4). Macchia fredda da confermare col sensore di bordo. ASD IschiaFishing.</small>
</div></body></html>"""
    open(os.path.join(REPO,"index.html"),"w",encoding="utf-8").write(html)
    open(os.path.join(REPO,f"report_{date}.html"),"w",encoding="utf-8").write(html)

    # PUBLISH
    try:
        subprocess.run(["git","-C",REPO,"add","-A"],check=True,timeout=60)
        subprocess.run(["git","-C",REPO,"commit","-q","-m",f"sera-prima {date} ({stamp})"],check=True,timeout=60)
        subprocess.run(["git","-C",REPO,"push","-q","origin","HEAD"],check=True,timeout=120)
        print("PUBLISHED:", date)
    except Exception as e:
        print("PUSH FALLITO:", e)

if __name__=="__main__": run()
