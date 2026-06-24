# DOCUMENTAZIONE TECNICA — Ostia 2026

**Data:** 2026-06-24 · **Progetto:** Campionato Italiano Traina d'Altura, Ostia 26-27/6/2026 · **Squadra:** ASD IschiaFishing.
**Scopo:** riferimento tecnico riproducibile per continuare il lavoro (file, metodi, fonti dati, pubblicazione, test).

> Onestà: questo progetto **NON usa un database**. È **file-based**: generatori Python → HTML statici pubblicati su GitHub Pages; i dati ambientali si campionano **live da API** (Copernicus/EMODnet/Open-Meteo); la batimetria di bordo è un'immagine base64 incorporata; le rotte stanno in un GPX. Le **soglie** del motore sono ancorate a una sola giornata (21/6) e il lato "forte" **non è validato**.

---

## 1. INFRASTRUTTURA E PUBBLICAZIONE

- **Repo:** `github.com/Marinovinc/OstiaSeraPrima` — branch **`main`**.
- **GitHub Pages:** `https://marinovinc.github.io/OstiaSeraPrima/` (serve la root del branch main). Cache-Control `max-age=600` (10 min): per vedere subito un aggiornamento usare un **cache-buster** `?v=N` o hard-refresh.
- **Cartella generatori:** `D:\Dev\OstiaSeraPrima\` (= repo).
- **Cartella lavoro doc/immagini:** `D:\claude_handoff\outbox\Roma_pesca_campionato_2026\` (NON pubblicata; `SRC` nei generatori).
- **Flusso di pubblicazione:** il generatore scrive l'HTML nel repo e fa `git add` + `commit` + `push origin HEAD/main` (es. `build_dossier.py` ~riga 285; `sera_prima_auto.py` usa `git add -A`). Pages si aggiorna in ~20-60 s.
- **Python:** `C:\Python313\python.exe`. Dipendenze: `matplotlib`, `numpy`, `Pillow (PIL)`, `playwright` (+ browser `webkit`/`chromium`), `tifffile` (per batimetria, se serve).

**URL live correnti (tutti 200):**
```
https://marinovinc.github.io/OstiaSeraPrima/dossier.html
https://marinovinc.github.io/OstiaSeraPrima/index.html              (sera-prima)
https://marinovinc.github.io/OstiaSeraPrima/Fronte_Tevere_MOBILE.html
https://marinovinc.github.io/OstiaSeraPrima/Fronte_Tevere_IPAD.html
```

---

## 2. GENERATORI (file → metodo → output)

### `motore_decisionale.py` (133 righe)
- **`deriva_strategia(chl_med, front_grad_km, cool_anom_C, cur_kn, cloud_pct, ora_finestra="mattino", sst_med=None)`** → dict con chiavi `dove_tag, dove, quota, colore, specie, assetto, segni, riferimenti`.
- Soglie DOVE (ancorate al 21/6): `forte = (anom<=-0.25) or (grad>=0.30)` **[STIMA non validata]**; `debole = (anom<=-0.12) or (grad>=0.14)` [ancorato al 21/6].
- `RIFERIMENTI` = lista (titolo, URL) R1-R7 (vedi §6).
- `SPECIE`: ripartizione per quota (superficie vs profondo). `ASSETTO`: 7 canne multi-specie.

### `sera_prima_auto.py` (257 righe)
- Campiona **CHL L4 gapfree** e **SST (L3 con fallback L4)** su una griglia del campo via **GetFeatureInfo** Copernicus; calcola il **gradiente LOCALE di SST** (°C/km tra punti adiacenti entro ~3,5 km = metrica fronte corretta) e l'anomalia della banda fredda; legge la **corrente**.
- Chiama `deriva_strategia(...)`; rende l'HTML nello standard `template_briefing` (loop su DOVE/QUOTA/COLORE/SPECIE/ASSETTO/SEGNI + Riferimenti).
- Scrive `index.html` + `report_<data>.html` nel repo e una **copia autonoma** (font Google rimossi via regex → offline) in `REPORT_sera_prima_autonomo.html`; poi `git add -A` + commit + push.
- **NB f-string:** il template è una f-string → eventuale JS/CSS con `{}` va con **graffe raddoppiate** `{{ }}`.

### `build_dossier.py` (297 righe)
- `img64(name)` inietta le PNG come **base64** (autoportante/offline). Costanti `IM_ROTTE/HEAT/PROF/RA/RB/RC/ESCHE`.
- Assembla `dossier.html` (sezioni + tabelle + callout + figure), lo scrive nel repo + **copia autonoma** `DOSSIER_OSTIA_2026_autonomo.html`, poi commit+push.
- Sezioni chiave: rotte A/B/C (sub-sezioni dedicate + mini-mappa + **tabella waypoint** + **callout Tempi** orari/percorrenza), campo, specie per quota, **assetto 7 canne**, **schede esca**, figura esche.

### `build_fronte_mobile.py` (77 righe)
- Legge il **base** `Fronte_Tevere_SQUADRA.html`, inietta CSS responsivo (`@media 640/1024`) + JS toggle (pulsanti Guida/Scala) e produce `Fronte_Tevere_MOBILE.html` e `_IPAD.html`. Flag per file: `window.__INFO_OPEN__`, `window.__SCALE_OPEN__` (entrambi `false` = pannelli chiusi di default).

### `disegna_esche.py` (77 righe)
- Pannello matplotlib `esche_proposte.png`: **minnow** (foto reale `esche_foto/minnow_2.jpg`, CC0) + **kona/octopus** (foto reale `esche_foto/piumetta_ov_0.jpg`, CC BY-NC 2.0) + **piumetta** e **teaser** (schemi). Costanti `FOTO`, `KONA_FOTO`.

### `scarica_esche_foto.py` / `scarica_esche_openverse.py`
- Scaricano foto a licenza libera: **Wikimedia Commons** API (`commons.wikimedia.org/w/api.php`, ricerca/categorie File namespace) e **Openverse** API (`api.openverse.org/v1/images/?q=...&license_type=all-cc`). Salvano `manifest*.json` con autore/licenza/fonte.

### Script di correzione one-off (documentati per riproducibilità)
- `fix_briefing_campo.py` (pentagono→quadrilatero nel Briefing + sostituzione immagine cotta), `fix_pentagono_residui.py` (termine "pentagono" residuo), `rimuovi_hotspot_invalidi.py` (rimozione α/β/γ + D1-D5 da Fronte_Tevere con test punto-nel-poligono).

---

## 3. FONTI DATI / ENDPOINT (no DB — API live)

- **Copernicus Marine (CMEMS)** — WMTS `https://wmts.marine.copernicus.eu/teroWmts` (lettura puntuale via `request=GetFeatureInfo`, regex `uom="..">valore<`).
  - CHL L4 gapfree: `OCEANCOLOUR_MED_BGC_L4_NRT_009_142`. SST L4: `SST_MED_PHY_SUBSKIN_L4_NRT_010_036`. SST L3 ~1 km: `SST_MED_SST_L3S_NRT_OBSERVATIONS_010_012_a/_b`. Correnti: `MEDSEA_ANALYSISFORECAST_PHY_006_013`. NB: prodotti **NRT = non futuri** (si campiona "la sera prima").
- **EMODnet Bathymetry** — WCS `https://ows.emodnet-bathymetry.eu/wcs` (GeoTIFF, `coverageId=emodnet__mean`), DTM ~115 m/cella. Usato per profili/georeferenziazione per profondità.
- **Open-Meteo** — `api.open-meteo.com/v1/forecast` (vento/pressione/nuvole/alba-tramonto) + `marine-api.open-meteo.com/v1/marine` (onde + SST). Senza chiave.
- **tides4fishing** (marea Fiumicino) · **PyEphem** (solunare).
- **Immagini esche:** Wikimedia Commons API · Openverse API (vedi §2).

> Dettaglio completo e affidabilità delle fonti: `FONTI_RIFERIMENTI_PESCA.md`.

---

## 4. ARCHITETTURA MAPPA LEAFLET (Fronte_Tevere) — z-index dei pane

Ordine di sovrapposizione corretto (fix di sessione):

| Pane | z-index | Contenuto |
|---|---|---|
| `tilePane` | 200 | tile scure CartoDB (contesto coste/etichette) |
| `offlineBase` | **250** | **immagine batimetrica** (fondali) — base64 incorporata, sempre visibile |
| `chlPane` | **300** | layer satellitare **CHL/SST** (on-demand) — sopra la batimetria |
| `overlayPane` | 400 | campo (quadrilatero), rotte, marker, isobate |

- Bug risolto: la batimetria era a **150** (sotto le tile) → online i fondali sparivano. Alzata a 250; il CHL spostato su `chlPane` 300 (creato con `map.createPane('chlPane')`; nel DOM la classe diventa `leaflet-chl-pane` perché Leaflet rimuove "Pane", ma `pane:'chlPane'` funziona).
- I layer CHL/SST (`currentLayer`, `sstLiveOverlay`) ricevono `pane: 'chlPane'`.

**Callout a scomparsa (dossier/sera-prima):** JS che avvolge il corpo di ogni `.call` in `.call-body` e aggiunge classe `collapsed`; CSS `.call.collapsed .call-body{display:none}` + marker **triangolo CSS** (`border-left-color`, NON glifo unicode → niente "tofu" su Safari).

---

## 5. CAMPO DI GARA (ufficiale, Ord. Capitaneria Roma 67/2026)

| Punto | Lat (DDM) | Lon (DDM) | Decimali | Pos |
|---|---|---|---|---|
| A | 41°42,222'N | 012°00,163'E | 41.7037 / 12.0027 | Nord |
| B | 41°32,224'N | 012°05,885'E | 41.5371 / 12.0981 | Est |
| C | 41°28,657'N | 011°53,087'E | 41.4776 / 11.8848 | Sud |
| D | 41°37,827'N | 011°46,426'E | 41.6305 / 11.7738 | Ovest |

Quadrilatero "a rombo". Punteggio FIPSAS: tonno rosso ×2 = 1.200; aguglia imp./spada/marlin bianco/alalunga/striato/alletterato/lampuga = 600; altri sportivi = 300. C&R, video, ispettore fotografa GPS a ogni ferrata, ferrata fuori campo = nulla, lenza max 15 kg, 7 canne, solo artificiali, 370 m tra barche.

---

## 6. RIFERIMENTI SCIENTIFICI/TECNICI (R1-R7, verificati)

- **R1** Weber et al. 2025, PLOS Biology — strutture = oasi/hub di aggregazione (no produttività locale).
- **R2** Goetsch/Gulka/Friedland et al. 2023, Ecology and Evolution 13(7):e10226 — superficie + **subsuperficie/termoclino** guidano il foraggio.
- **R3** Zainuddin et al. 2017, PLoS One — Pelagic Hotspot Index (SST+SSH+CHL).
- **R4** fishingword.com — colore esca: rosso svanisce ~5 m, blu/verde penetrano 25-35 m; torbida → contrasto/scuri.
- **R5** fishingboatmagazine — aguglia imperiale + lampuga target Ostia 2026.
- **R6** obiettivopesca.org — alalunga Tirreno: fondali 500-2000 m, traina 6-9 kn.
- **R7** BigGame.it — minnow Rapala ~13 cm + piumette piombate; uccelli ai bordi delle mangianze = branchi in caccia.

**Licenze immagini esche:** minnow `CC0` (Wikimedia Commons); kona/octopus `CC BY-NC 2.0` — foto di *Lonnie's Life*, Flickr `flickr.com/photos/9047144@N06/2953846893` (uso non-commerciale, attribuzione, non modificata).

---

## 7. METODO DI TEST (Playwright WebKit = motore di Safari)

- Browser: `p.webkit.launch()` (installare con `python -m playwright install webkit`). **WebKit = stesso motore di Safari** → proxy fedele di iOS (non identico a un iPhone fisico: niente barra Safari/safe-area reali).
- Profili dispositivo: `p.devices["iPhone 13"]`, `p.devices["iPad (gen 7)"]`.
- **Simulazione "in barca senza segnale":** intercettare e abortire le richieste alle tile (`pg.route` su `cartocdn/openstreetmap/arcgisonline/marine.copernicus/earthdata`) → resta solo la batimetria base64 + vettori.
- Controlli utili: `pg.on("pageerror", ...)` (zero ReferenceError attesi), misura `#map` bounding box, stato `.collapsed`, verifica HTTP status sull'URL **live**.

---

## 8. RIFERIMENTI INCROCIATI

- Handover sessione: `HANDOVER_SESSIONE_ostia2026_20260624.md`.
- Operativo gara: `BRIEFING_ROTTE_OSTIA_2026.md`, `ROTTE_OSTIA_2026.gpx`.
- Modello: `PROGETTO_MODELLO_FORAGGIO_OSTIA_2026.md`, `SCHEDA_RIFERIMENTO_21-06-2026_GIORNO_VERITA.md`.
- Fonti: `FONTI_RIFERIMENTI_PESCA.md`.
- Documenti ufficiali: `55626_RG_REG_CI_ALTURA_ASSOLUTO_2026.pdf` (Regolamento FIPSAS), `ORD.67.26...pdf` (Ordinanza Capitaneria).
- Storico (superato, con banner): `DOCUMENTAZIONE_TECNICA_roma2026_20260602.md`, `INDICE.md`, `README_SQUADRA.md`.
