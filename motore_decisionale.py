# -*- coding: utf-8 -*-
"""
MOTORE DECISIONALE - Ostia 2026 (ASD IschiaFishing)
Deriva la strategia del giorno (DOVE / QUOTA / COLORE / QUANDO / SPECIE) dalle
CONDIZIONI di quel giorno, applicando relazioni FONDATE su letteratura e su piu'
punti di calibrazione. NON copia il 21/6: quel giorno e' una sola realizzazione.

Punti di appoggio (onesti su cosa sono):
  - 21/6/2026  : [CALIBRAZIONE CONDIZIONI] uscita di Silvio, scarpata >700 m, blu limpido,
                 alba calma -> minnow a 5 cm sub-superficie, bianco/viola.
  - Forio 21/6 : [CALIBRAZIONE, corrobora] vittoria su strutture nelle finestre solunari.
  - Ostia 2025 : [EVIDENZA SPECIE, NON condizioni] Campionato SOCIETA', LUGLIO 2025 (mese diverso!),
                 vinto con 6 catture e specie diverse (tonno rosso, striato, aguglia imp., lampuga, spada)
                 -> dice COSA si cattura a Ostia, non con quali condizioni del 26-27/6.

Basi (referenze verificate, vedi RIFERIMENTI):
  [R1 Weber 2025]    strutture/secche concentrano i predatori per AGGREGAZIONE (oasi/hub), NON per produttivita' locale.
  [R2 Goetsch 2023]  features di superficie E subsuperficie (strato misto/termoclino) guidano le aggregazioni di foraggio.
  [R3 Zainuddin 2017] SST + anomalia + CHL = INDICATORI di hotspot (dove l'indice e' alto, sale la CPUE) - non meccanismo.
  [R4 fishingword]   colore esca: rosso svanisce ~5 m, blu/verde penetrano; acqua torbida -> contrasto.
Quindi: anomalia fredda/fronte = INDICATORE di dove cercare (non prova di upwelling); la struttura AGGREGA;
la quota dipende da termoclino/luce. La regola 'limpida=naturali' resta prassi, non da referenza.
"""

# RIFERIMENTI VERIFICATI (aperto il link, letto il contenuto, autore/anno confermati dalla pagina).
RIFERIMENTI = [
 # [R1] Strutture/secche concentrano i predatori per AGGREGAZIONE (oasi/hub) - NON per produttivita' locale.
 ("Weber et al., 2025, PLOS Biology - 'Shallow seamounts are oases and activity hubs for pelagic predators' "
  "(biomassa-preda +entro 2,5 km; ma 'no evidence of enhanced primary productivity')",
  "https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003016"),
 # [R2] Caratteristiche oceanografiche (superficie+SUBSUPERFICIE/strato misto) guidano le aggregazioni di foraggio.
 ("Goetsch, Gulka, Friedland et al., 2023, Ecology and Evolution 13(7):e10226 - features di superficie e "
  "subsuperficie (mixed layer depth) guidano abbondanza/diversita' del pesce foraggio",
  "https://pmc.ncbi.nlm.nih.gov/articles/PMC10334121/"),
 # [R3] Indice hotspot (SST + anomalia livello mare + CHL) -> CPUE tonno: i fronti/anomalie sono INDICATORI di hotspot.
 ("Zainuddin et al., 2017, PLoS One - Pelagic Hotspot Index (SST+SSH+CHL): 'Skipjack CPUEs increased "
  "significantly in the areas of highest pelagic hotspot index'",
  "https://pmc.ncbi.nlm.nih.gov/articles/PMC5624707/"),
 # [R4] Colore esca vs profondita'/luce: rosso svanisce ~5 m, blu/verde 25-35 m; torbida -> contrasto/scuri.
 ("fishingword.com (divulgativo) - colore esca: lunghezze d'onda lunghe (rosso) assorbite ~5 m, "
  "corte (blu/verde) penetrano 25-35 m; in acqua torbida conta il contrasto",
  "https://fishingword.com/newbie-guide/lure-color-science-underwater-visibility/"),
 # [R5] Evento 2026: specie target a Ostia (aguglia imperiale, lampuga), C&R.
 ("fishingboatmagazine.it - 'Il Big Game sbarca a Roma' (2026, 25-28/6, Ostia): specie target evidenziate "
  "aguglie imperiali e lampughe; Catch & Release",
  "https://www.fishingboatmagazine.it/il-big-game-sbarca-a-roma/"),
 # [NON verificata direttamente: 403] specie Ostia 2025 (tonno rosso/striato/aguglia/lampuga/spada, 6 catture):
 #   proveniente da snippet di ricerca di alassionews.it, NON letto direttamente -> trattare come indicativo.
]

def deriva_strategia(chl_med, sst_min, sst_max, cool_anom_C, cur_kn, cloud_pct, ora_finestra="mattino"):
    """Ritorna la strategia DERIVATA dalle condizioni. Tutti gli input dal dato fresco del giorno.
       chl_med mg/m3 (limpidezza); sst_min/max gradiente; cool_anom_C anomalia banda fredda;
       cur_kn corrente; cloud_pct nuvolosita'; ora_finestra mattino/mezzogiorno."""
    S = {}

    # --- DOVE: forza dei driver del giorno (non assume la scarpata del 21/6) ---
    # ATTENZIONE: le soglie qui sotto (gradiente SST 0.3/0.6 C; anomalia -0.10/-0.20 C) sono
    # valori INIZIALI ARBITRARI, NON validati su dati. Vanno ritarati. Non sono "verita'".
    grad = (sst_max - sst_min) if (sst_min is not None and sst_max is not None) else 0.0
    driver = []
    if cool_anom_C is not None and cool_anom_C <= -0.20: driver.append(("indicatore hotspot: banda fredda", "forte"))
    elif cool_anom_C is not None and cool_anom_C <= -0.10: driver.append(("indicatore hotspot: banda fredda", "debole"))
    if grad >= 0.6: driver.append(("fronte termico", "forte"))
    elif grad >= 0.3: driver.append(("fronte termico", "debole"))
    if not driver:
        S["dove"] = ("Nessun fronte/upwelling marcato: il driver dominante resta la STRUTTURA "
                     "(scarpata 700-900 m + banco/dorsali). Lavora le rotte sulla struttura.")
        S["dove_tag"] = "struttura"
    else:
        d = ", ".join(f"{n} ({f})" for n,f in driver)
        S["dove"] = (f"Driver attivi: {d}. L'area MIGLIORE e' dove questi coincidono con la struttura "
                     f"(scarpata/secche), NON necessariamente il punto del 21/6: segui la macchia fredda / il bordo del fronte.")
        S["dove_tag"] = "fronte+struttura"

    # --- QUOTA: da luce/ora/temperatura (Ref: penetrazione luce, comportamento foraggio) ---
    if ora_finestra == "mattino" and cur_kn is not None:
        S["quota"] = ("Finestre mattutine (luce media, mare in genere calmo): la presentazione di "
                      "SUPERFICIE/SUB-SUPERFICIE e' efficace (e' il caso del 21/6). "
                      "Tieni comunque 1-2 canne PROFONDE (divergenti) per BFT/spada.")
    else:
        S["quota"] = ("Sole alto / acqua calda: foraggio e predatori scendono -> privilegia le "
                      "canne PROFONDE (divergenti, 20-60 m) oltre allo spread di superficie.")
    if (sst_max or 0) >= 26:
        S["quota"] += " SST elevata (>=26 C): probabile termoclino marcato, i grossi stanno sotto."

    # --- COLORE: da limpidezza (CHL) + luce (Ref: lure color vs clarity/light) ---
    # COLORE: SOLO guida VERIFICATA (R4). Nessuna prescrizione di colore non verificata; niente esche anedottiche.
    chiaro = "<0.10 (blu limpido)" if (chl_med is not None and chl_med < 0.10) else \
             "0.10-0.30 (verdino)" if (chl_med is not None and chl_med < 0.30) else ">=0.30 (torbido)"
    col = "PROFONDITA': sulle canne profonde preferisci BLU/VERDE/glow (rosso/arancio svaniscono ~5 m) [R4 verificato]."
    if chl_med is not None and chl_med >= 0.30:
        col += " ACQUA TORBIDA: conta il CONTRASTO (silhouette scura o chartreuse) [R4 verificato]."
    else:
        col += " ACQUA LIMPIDA: non esiste una regola di colore verificata -> scelta per esperienza/test in mare."
    S["colore"] = (f"Acqua {chiaro}. {col} "
                   "NB: 'minnow 5 cm + bianco/viola' del 21/6 e' un ANEDDOTO non verificato (riferito da terzi): "
                   "spunto, NON regola da assumere.")

    # --- SPECIE / SPREAD: dalla colonna (calibrato anche su Ostia 2025) ---
    S["specie"] = ("Copri la COLONNA. Specie target VERIFICATE per l'evento Ostia (fonte 2026): "
                   "aguglia imperiale e lampuga [R5]. Indicative (Ostia 2025, da snippet NON letto direttamente): "
                   "anche tonno rosso, striato, spada. Spread di superficie (aguglia/lampuga/tunnidi/alalunga, 600) "
                   "+ 1-2 canne profonde (tonno rosso 1200, spada 600). Oggetti galleggianti/linee di alga -> LAMPUGA.")

    S["riferimenti"] = RIFERIMENTI
    return S

if __name__ == "__main__":
    # esempio: condizioni del 21/6 -> deve riprodurre 'superficie + bianco/viola'
    s = deriva_strategia(chl_med=0.05, sst_min=25.7, sst_max=26.0, cool_anom_C=-0.15, cur_kn=0.24, cloud_pct=0, ora_finestra="mattino")
    for k in ("dove","quota","colore","specie"): print(k.upper()+":", s[k], "\n")
