# Ostia 2026 — Traina d'Altura · Guida del progetto

Sistema data-driven per il **62° Campionato Italiano Assoluto di Traina d'Altura** — Ostia/Torvaianica, **26-27 giugno 2026** (recupero 28/6), 08:00-15:00, Catch & Release. ASD IschiaFishing.

> Aggiornamento cache: GitHub Pages tiene 10 minuti. Se non vedi l'ultima versione, aggiungi `?v=N` all'URL o fai pull-to-refresh.

---

## Pagine live (apri dal telefono / iPad)

- **Dossier tattico** — rotte A/B/C con orari, campo, specie, assetto, esche:
  `https://marinovinc.github.io/OstiaSeraPrima/dossier.html`
- **Report sera-prima** (auto-aggiornato dai dati reali):
  `https://marinovinc.github.io/OstiaSeraPrima/index.html`
- **Mappa Fronte/Campo — versione telefono:**
  `https://marinovinc.github.io/OstiaSeraPrima/Fronte_Tevere_MOBILE.html`
- **Mappa Fronte/Campo — versione iPad:**
  `https://marinovinc.github.io/OstiaSeraPrima/Fronte_Tevere_IPAD.html`

---

## Documentazione (link)

- **Handover sessione (onesto, errori inclusi):** [`HANDOVER_SESSIONE_ostia2026_20260624.md`](HANDOVER_SESSIONE_ostia2026_20260624.md)
- **Documentazione tecnica (metodi, fonti, architettura, test):** [`DOCUMENTAZIONE_TECNICA_ostia2026_20260624.md`](DOCUMENTAZIONE_TECNICA_ostia2026_20260624.md)
- Operativo gara: `BRIEFING_ROTTE_OSTIA_2026.md` · `ROTTE_OSTIA_2026.gpx` (carica sul plotter)
- Modello foraggio: `PROGETTO_MODELLO_FORAGGIO_OSTIA_2026.md` · `SCHEDA_RIFERIMENTO_21-06-2026_GIORNO_VERITA.md`
- Fonti/riferimenti riusabili: `FONTI_RIFERIMENTI_PESCA.md`
- Ufficiali: Regolamento FIPSAS `55626_RG_REG_CI_ALTURA_ASSOLUTO_2026.pdf` · Ordinanza Capitaneria `ORD.67.26....pdf`

*(I .md operativi e i PDF stanno nella cartella di lavoro `D:\claude_handoff\outbox\Roma_pesca_campionato_2026\`.)*

---

## Generatori (come rigenerare)

- `python sera_prima_auto.py` — **lancialo la sera del 25/6 e del 26/6**: ricampiona CHL/SST/corrente reali, rigenera e pubblica `index.html`.
- `python build_dossier.py` — rigenera e pubblica `dossier.html`.
- `python build_fronte_mobile.py` — rigenera le versioni mobile/iPad dalla base `Fronte_Tevere_SQUADRA.html`.
- `python disegna_esche.py` — rigenera l'immagine esche (foto reali + schemi).
- Motore: `motore_decisionale.py` (`deriva_strategia(...)`). Dettagli: vedi documentazione tecnica.

---

## Campo di gara (ufficiale — Ord. Capitaneria Roma 67/2026)

| Punto | Lat | Lon | Pos |
|---|---|---|---|
| A | 41°42,222'N | 012°00,163'E | Nord |
| B | 41°32,224'N | 012°05,885'E | Est |
| C | 41°28,657'N | 011°53,087'E | Sud |
| D | 41°37,827'N | 011°46,426'E | Ovest |

---

## Stato e limiti onesti

- 4 pagine live, testate sul motore **WebKit (Safari)**. Conferma finale = aprirle su iPhone/iPad reali.
- Soglie "forti" del motore **non validate** (calibrazione su 1 sola giornata, il 21/6).
- Esche: 2 foto reali (minnow, kona) + 2 schemi (piumetta, teaser); taglie/montaggi kona/teaser = **prassi da confermare**.

---

## Sviluppi e miglioramenti futuri

**Dati/modello**
- Log esiti uscite (data + coordinate cattura + specie + condizioni) per **validare** le soglie "forti".
- Integrare subsuperficie/termoclino; trend multi-giorno della sera-prima.

**Esche/tecnica**
- Foto reali di **piumetta** e **teaser** (foto dell'equipaggio) al posto degli schemi.
- Scheda montaggi illustrata con foto reali.

**Mappe/UX**
- Pagina-hub pubblicata che linka tutto (accesso rapido dal telefono).
- Legenda colori CHL mostrata solo quando si carica il satellite.
- Verifica su dispositivi fisici (iOS/Android).

**Robustezza**
- Parametri esterni (velocità, finestre) non hard-coded.
- Smoke-test Playwright post-pubblicazione su tutti gli URL.
