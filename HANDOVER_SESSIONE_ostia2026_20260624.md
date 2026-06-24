# HANDOVER SESSIONE — Ostia 2026 (consolidamento: campo, mobile, esche)

**Data:** 2026-06-24
**Progetto:** 62° Campionato Italiano Assoluto di Traina d'Altura — Ostia/Torvaianica, **26-27 giugno 2026** (recupero 28/6), 08:00-15:00, Catch & Release.
**Squadra:** ASD IschiaFishing.
**Repo pubblicato:** `github.com/Marinovinc/OstiaSeraPrima` → GitHub Pages `https://marinovinc.github.io/OstiaSeraPrima/`
**Cartella di lavoro doc/immagini:** `D:\claude_handoff\outbox\Roma_pesca_campionato_2026\`
**Generatori:** `D:\Dev\OstiaSeraPrima\` (repo).

> Documento gemello: `DOCUMENTAZIONE_TECNICA_ostia2026_20260624.md` (metodi, endpoint, architettura). Guida/indice: `README.md`.

---

## 1. SINTESI DELLA SESSIONE

Sessione di **consolidamento** su un progetto già avviato (modello foraggio + motore decisionale + dossier + sera-prima). Macro-attività:

1. Chiarito e corretto il gergo "**prime tonni**" (vecchio `gara_plan.js`).
2. Collocate **aguglia imperiale** e **tonno striato** nella strategia (specie di **superficie** sullo stesso blu profondo).
3. Definito un **assetto 7 canne multi-specie** + identificate le **esche multi-specie** (kona/octopus, piumetta, minnow).
4. **Campo di gara ufficiale**: letta l'Ordinanza Capitaneria **n. 67/2026** → il campo è un **QUADRILATERO A/B/C/D**, non il pentagono delle bozze vecchie. Corretto ovunque.
5. **Rimossi** gli hotspot α/β/γ e i canyon D1-D5 dalle mappe vecchie (5 su 8 cadevano **fuori** dal campo ufficiale → ferrate nulle). Non riposizionati (= sarebbe inventare).
6. **Versioni mobile e iPad** di `Fronte_Tevere` + **pubblicazione** (erano irraggiungibili dal telefono) + fix **fondali/batimetria** non visibili + pannelli **a scomparsa**.
7. **Callout a scomparsa** anche in dossier e sera-prima.
8. **Esche con foto reali** (minnow CC0 + kona/octopus CC BY-NC) + schede **colore/taglia/montaggio**.

**Stato finale:** 4 pagine live e testate sul motore **WebKit (Safari)**: `dossier.html`, `index.html` (sera-prima), `Fronte_Tevere_MOBILE.html`, `Fronte_Tevere_IPAD.html` — tutte HTTP 200.

---

## 2. CRONOLOGIA ATTIVITÀ (per blocco)

### 2.1 "prime tonni" + specie di periodo
- "prime tonni" era inglese maccheronico (*prime = prima scelta/momento migliore*) nel **vecchio** `D:\Dev\IschiaFishing\gara_plan.js` (piano "angolo NE", superato). Riscritto in italiano chiaro; backup creato e rimosso.
- **Aguglia imperiale** e **tonno striato**: non hanno uno spot diverso, sono **questione di quota** sullo stesso blu profondo. Resi espliciti nel motore (`SPECIE`) e nel dossier (callout "Specie per quota"): SUPERFICIE = aguglia imp./striato/alletterato/lampuga/alalunga (600); PROFONDO = tonno rosso (1200) + spada (600).

### 2.2 Assetto canne + esche multi-specie
- Aggiunto `S["assetto"]` al motore e una **tabella assetto 7 canne** al dossier (2 flat minnow, 2 rigger kona, 1 shotgun piumetta, 2 profonde piombate, + teaser senza amo).
- Esche **multi-specie** privilegiate: octopus/kona piccolo-medio, piumetta, minnow.

### 2.3 Campo di gara — la correzione più importante
- Letta direttamente l'**Ordinanza Capitaneria di Porto di Roma n. 67/2026** (firmata 15/06/2026). Campo = **quadrilatero**:
  - A 41°42,222'N 012°00,163'E → 41.7037 / 12.0027 (Nord)
  - B 41°32,224'N 012°05,885'E → 41.5371 / 12.0981 (Est)
  - C 41°28,657'N 011°53,087'E → 41.4776 / 11.8848 (Sud)
  - D 41°37,827'N 011°46,426'E → 41.6305 / 11.7738 (Ovest)
- Il **pentagono a 5 vertici** dei doc del 02/06 era una **stima sbagliata**. Corretto in: `DOCUMENTAZIONE_TECNICA_roma2026_20260602.md` (§5 banner + tabella), `INDICE.md`, `README_SQUADRA.md`, `Fronte_Tevere_SQUADRA.html` (poligono vettoriale), `Briefing_tattico_Roma_2026.html` (testo + **immagine-mappa cotta sostituita** con la mappa corretta), e ripulito il termine "pentagono" in 5 doc storici.
- I due 3D (`CAMPO_GARA_3D.html`, `_TATTICO.html`) erano **già** corretti (traccia "campo gara" a 4 vertici chiusi); il flag iniziale era un **falso positivo** (la stringa "1108"/"vertice" stava nel codice minificato di plotly/mapbox, non nei dati).

### 2.4 Rimozione hotspot/canyon non validi
- Test **punto-nel-poligono** sul quadrilatero ufficiale: **5 su 8** (β, γ, D1, D2, D3) cadono **a sud del vertice C → fuori campo** (ferrata nulla). I 3 interni (α, D4, D5) erano comunque della tesi superata e ridondanti con le rotte A/B/C.
- Decisione: **rimuovere, non riposizionare** (riposizionare = inventare coordinate). Tolti marker + toggle + legenda + handler da `Fronte_Tevere_SQUADRA.html`; aggiunto banner storico. Zero riferimenti JS pendenti.

### 2.5 Mobile/iPad + pubblicazione + fondali + a scomparsa
- Create `Fronte_Tevere_MOBILE.html` e `_IPAD.html` (pannelli Guida/Scala **collassabili**, CSS responsive).
- **Causa reale del "non funziona sul telefono": consegna.** I file stavano solo in `claude_handoff` (fuori dal repo) → **HTTP 404** sulla GitHub Pages che il telefono apre. Risolto pubblicandoli nel repo.
- **Fondali/batimetria invisibili online**: l'imageOverlay batimetrico era a **z-index 150** (sotto le tile scure CartoDB a 200). Alzato a **250**; il layer satellitare CHL/SST spostato su pane dedicato **`chlPane` z-index 300** (sopra la batimetria, sotto i vettori) per non romperlo.
- Test fatto col motore **WebKit (Safari)** a profilo iPhone 13 / iPad, anche sugli URL live.

### 2.6 Callout a scomparsa (dossier + sera-prima)
- Piccolo JS che avvolge il corpo di ogni `.call` in `.call-body` e lo collassa (robusto sui nodi di testo); marker **triangolo CSS** (border, niente glifo unicode). Chiusi di default.

### 2.7 Esche con foto reali + schede
- `Attrezzatura_pesca_*.jpeg` (Downloads): **render generici/AI**, senza kona/piumette/teaser → scartate onestamente.
- Foto reali a licenza libera: **minnow** (Wikimedia Commons, **CC0**) + **kona/octopus** (foto di *Lonnie's Life*, Flickr, **CC BY-NC 2.0**, non modificata, uso non-commerciale). Per **piumetta (feather)** e **teaser** non esistono foto libere pulite → restano **schemi** etichettati.
- Aggiunta tabella **"Schede esca" (colore · taglia · montaggio)** con marcatura verificato [R4/R7] vs prassi.

---

## 3. ERRORI CONFESSATI (onestà brutale)

1. **Test non rappresentativo spacciato per prova.** Ho dichiarato che le versioni mobile/iPad "funzionano sul dispositivo" basandomi su **screenshot di Chromium headless**, che NON è Safari/iOS. Solo dopo ho installato e usato **WebKit** (motore di Safari). Confidenza dichiarata (9/10) inizialmente non provata.
2. **Consegna non verificata (errore grave).** Ho creato i file mobile/iPad in `claude_handoff` (fuori dal repo pubblicato) **assumendo** fossero raggiungibili dal telefono. Erano **404**. Causa reale del "non hai fatto niente".
3. **Riferimenti scientifici inventati** (in fase iniziale: autori Morato/Suca/Mukti) → corretti citando solo titolo+URL e poi verificando i veri autori (Weber 2025, Goetsch 2023, Zainuddin 2017).
4. **Esca non verificata come raccomandazione** ("minnow 5 cm bianco/viola" del 21/6) → declassata ad **aneddoto** in tutti i file.
5. **Metrica fronte degenere**: usavo il range max-min di SST di campo (sempre ≥ soglia → "fronte sempre attivo"). Corretto al **gradiente LOCALE °C/km**.
6. **Marker "tofu".** Ho **assunto** che il carattere freccia unicode rendesse su Safari: rendeva come riquadro vuoto □. Corretto con triangolo disegnato in CSS.
7. **Bug f-string.** Inserito JS con graffe `{}` in una f-string Python (`sera_prima_auto.py`) → SyntaxError. Corretto raddoppiando `{{ }}`.
8. **Assunzione sulle foto attrezzatura.** Ho supposto che le `Attrezzatura_pesca` contenessero kona/teaser: erano render AI senza quelle esche.
9. **"Non aggiornato" = cache.** Avevo dichiarato successo senza segnalare la cache del browser (GitHub Pages `max-age=600`): il live era già corretto, ma l'utente vedeva la copia in cache.
10. **Over-fit iniziale** della strategia su un solo giorno (21/6) e, in un passaggio, dichiarato che una coordinata "serviva all'utente" quando avevo i riferimenti per georeferenziarla.

Pattern: ho lavorato bene quando ho **riprodotto e verificato** prima di concludere; ho sbagliato quando ho **assunto** (consegna, motore di rendering, contenuto delle foto).

---

## 4. STATO ATTUALE — dove siamo arrivati

**Live e verificato (WebKit/Safari, HTTP 200):**
- `dossier.html` — dossier tattico completo (rotte A/B/C con tempi, campo quadrilatero, specie per quota, assetto, schede esca, foto esche reali, callout a scomparsa).
- `index.html` — report **sera-prima** auto-generato (callout a scomparsa).
- `Fronte_Tevere_MOBILE.html` / `_IPAD.html` — mappa con **fondali visibili**, campo quadrilatero, Guida/Scala a scomparsa.

**Coerenza dati:**
- Campo = **quadrilatero ufficiale A/B/C/D** ovunque (allineato a `ROTTE_OSTIA_2026.gpx`).
- Motore decisionale: deriva DOVE/QUOTA/COLORE/SPECIE/ASSETTO/SEGNI dalle condizioni; **soglie ancorate al 21/6**, lato "forte" **NON validato** (gap dichiarato).
- Esche: 2 foto reali + 2 schemi; taglie/montaggi kona/teaser = **prassi da confermare**.

---

## 5. COME CONTINUARE (da dove e come)

1. **Foto reali mancanti:** chiedere all'utente **una foto delle proprie piumette e del teaser** (e kona se vuole le sue) → sostituire gli schemi in `disegna_esche.py` (variabili `KONA_FOTO`-style), rigenerare con `build_dossier.py`.
2. **Confermare le schede esca:** l'utente (esperto) deve validare taglie/colori/montaggi marcati "prassi" nella tabella "Schede esca".
3. **Validare le soglie "forti"** del motore: serve un **log esiti uscite** (data + coordinate cattura + specie + condizioni) per ritarare il lato non validato. Vedi §6.
4. **Conferma su dispositivo fisico:** WebKit è il motore di Safari ma su PC — far aprire i 4 link su iPhone/iPad reali per chiudere l'ultimo decimo.
5. **Sera-prima del 25/6 e 26/6:** lanciare `python sera_prima_auto.py` la sera prima di ogni manche (ricampiona dati reali e pubblica).

---

## 6. SVILUPPI E MIGLIORAMENTI FUTURI

**Dati / modello**
- **Log esiti uscite** (CSV/DB locale) per accumulare giornate etichettate e **validare statisticamente** le soglie "forti" del motore (oggi 1 sola giornata = 21/6).
- Integrare **subsuperficie/termoclino** [R2] quando disponibile (proxy migliore del solo SST di superficie).
- Auto-confronto **più giorni** di sera-prima (trend CHL/SST) invece del singolo campione.

**Esche / tecnica**
- Completare le **foto reali** di piumetta e teaser (foto dell'utente).
- Scheda **montaggi** illustrata (weak-link, divergenti, daisy-chain) con foto reali.

**Mappe / UX**
- **Pagina-hub** pubblicata (index che linka dossier, sera-prima, mappe mobile/iPad) per accesso rapido dal telefono.
- Auto-mostra della legenda colori CHL solo **quando** si carica il layer satellitare.
- Pubblicare anche `Fronte_Tevere_SQUADRA.html` (desktop) se serve da PC.
- Verifica su **dispositivi fisici** reali (iOS Safari, Android Chrome).

**Robustezza**
- `config`/parametri esterni (velocità traina, finestre) invece che hard-coded.
- Test automatico (Playwright) come **smoke-test** post-pubblicazione su tutti gli URL.

---

## 7. FILE TOCCATI (mappa)

**Repo (pubblicati):** `motore_decisionale.py`, `sera_prima_auto.py`, `build_dossier.py`, `build_fronte_mobile.py`, `disegna_esche.py`, `scarica_esche_foto.py`, `scarica_esche_openverse.py`, `fix_briefing_campo.py`, `fix_pentagono_residui.py`, `rimuovi_hotspot_invalidi.py`; `dossier.html`, `index.html`, `Fronte_Tevere_MOBILE.html`, `Fronte_Tevere_IPAD.html`; `README.md`.

**Cartella Roma_pesca (lavoro):** `Fronte_Tevere_SQUADRA.html` (base, corretto), `Briefing_tattico_Roma_2026.html` (campo + immagine), `DOCUMENTAZIONE_TECNICA_roma2026_20260602.md`, `INDICE.md`, `README_SQUADRA.md`, `MANUALE_*`, `esche_proposte.png`, `esche_foto/` (foto reali + manifest), `DOSSIER_OSTIA_2026_autonomo.html`, `REPORT_sera_prima_autonomo.html`.

**Altro:** `D:\Dev\IschiaFishing\gara_plan.js` ("prime tonni" corretto).

---

## 8. AGGIORNAMENTO SESSIONE 2026-06-24 (pomeriggio) — piumetta foto reale, .nojekyll, assetto canne

Tre interventi su due repo, tutti pubblicati e verificati nel live.

### 8.1 Piumetta come FOTO REALE nel dossier (repo OstiaSeraPrima)
- Sostituito lo **schema** piumetta (quadrante 3 di `esche_proposte.png`) con una **foto-prodotto reale**: **Williamson Flash Feather** blu/bianco (scaricata da nootica.com). Teaser **resta schema** daisy-chain (scelta utente: l'Exciter Bird trovato e' un "bird teaser", non una daisy-chain).
- File: `disegna_esche.py` (costante `PIUMETTA_FOTO`, quadrante 3 da schema a `imshow`, titolo "3 foto reali + 1 schema", crediti); `build_dossier.py` (caption figura esche). Foto in `esche_foto/piumetta_prod.jpg`; provenienza/licenza in `esche_foto/manifest_prodotto.json` (incl. `teaser_prod.jpg` scaricato ma NON usato).
- **Copyright:** foto-prodotto (c) Williamson/Rapala su repo PUBBLICO, uso non commerciale squadra, con credito. **Da sostituire con foto reale dell'utente** quando disponibile (piano "1": lasciare il file, rigenerare con `build_dossier.py`).
- Commit `647e9d5` (dossier) + `869fcd1` (disegna_esche). Live verificato con screenshot WebKit (`dossier_live_webkit_esche.png`).

### 8.2 Fix build GitHub Pages: aggiunto `.nojekyll` (repo OstiaSeraPrima)
- **Problema scoperto:** dal commit `647e9d5` il **build Pages falliva** ("Page build failed") → il deploy del dossier aggiornato era bloccato (live fermo all'ultimo build OK). Causa: GitHub Pages processava con **Jekyll** un sito di HTML statici autoportanti.
- **Fix:** aggiunto file vuoto **`.nojekyll`** in root (commit `805f468`) → Pages serve i file as-is, build tornato `built`. Protegge anche index/mobile/ipad/report futuri.
- **Lezione:** per i repo di HTML statici pubblicati su Pages, mettere SEMPRE `.nojekyll`. NB: il repo **GaraOstia2026 NON ha .nojekyll** ma i suoi build passano lo stesso (contenuto non problematico per Jekyll) — valutare di aggiungerlo per prevenzione.

### 8.3 Diagramma "Assetto 7 canne a ventaglio" nella guida di bordo (repo GaraOstia2026)
- Aggiunto alla sezione **"VI · Tecnica di traina"** di `GUIDA_RAPIDA_BARCA.html` un **diagramma SVG a ventaglio** (vista dall'alto: prua/poppa/T-TOP, divergenti dx/sx, canne C1->C7 con distanze + legenda), nello stile dei briefing tattici Forio (`Briefing_tattico_Forio_2026_*.html`, sez. "Assetto: le 7 canne"). Inserito sopra la tabella "Assetto multi-specie" gia' presente.
- **Distanze/esche dalla tabella Ostia esistente** (non inventate): C1/C7 flat 15-25 m, C2/C6 outrigger corto ~40 m, C3/C5 outrigger lungo ~60 m, C4 shotgun ~90 m. Geometria del ventaglio ripresa da Forio.
- **Errore corretto in corsa:** la prima versione copiava i colori Forio (C2/C3/C5/C6 = "skirted"), incoerente con la tabella Ostia che li' mette **minnow a paletta Halco**. Allineato: verde = minnow paletta Halco (C2/C3/C5/C6), ocra = flat piombate cedar/polpetto (C1/C7), rosso = kona/skirted shotgun (C4).
- Commit `d10ad21`. Build `built`, live verificato.

### 8.4 Errori confessati di questa sessione
1. **Assunzione sul file foto:** il file `Briefing_Forio_2026_20.html` indicato dall'utente NON conteneva foto sue, ma foto-prodotto da URL esterni (Halco/Rapala/Nootica/Williamson) + 3 mappe base64. Chiarito prima di procedere.
2. **Incoerenza colori diagramma** (vedi 8.3): schema-colori Forio applicato senza adattarlo alla logica esche di Ostia. Trovato allo screenshot di verifica e corretto.
3. **`rm -rf __pycache__`** ha cancellato 2 `.pyc` tracciati nel repo OstiaSeraPrima → ripristinati con `git checkout` (nessuna modifica indesiderata persistita).

### 8.5 File live aggiornati (oltre ai 4 gia' noti)
- `https://marinovinc.github.io/GaraOstia2026/GUIDA_RAPIDA_BARCA.html` (guida di bordo con diagramma assetto).
