---
description: Zoek een juridische term in de kernwetten (IW 1990, Leidraad Invordering, UB IW 1990, AWR, Awb) en genereer een gestructureerd wetsanalyse-rapport als MD-bestand.
---

# /wetzoek — Juridische Termanalyse

**Zoekterm:** `$ARGUMENTS`

Voer onderstaande stappen strikt in volgorde uit. Wijk niet af van de voorgeschreven formats — consistentie tussen runs is een harde eis.

---

## Stap 1 — Morfologische variantenlijst (deterministisch)

Pas de volgende vaste regels toe op `$ARGUMENTS` om de zoekvariantenlijst samen te stellen. De lijst is altijd volledig bepaald door de regels — geen eigen aanvullingen.

**Regel 1 — Enkelvoud/meervoud:**

| Situatie | Actie |
|----------|-------|
| Term eindigt op `-en` en is een zelfstandig naamwoord | Voeg de stam toe (strip `-en`, pas eventuele klinkerverdubbeling of `-s`-omzetting terug) |
| Term eindigt niet op `-en` | Voeg de `-en`-vorm toe; voeg ook de `-s`-vorm toe als gangbaar |
| Term is al een stam | Voeg zowel `-en` als `-s`-meervoud toe indien beide bestaan |

**Regel 2 — Samenstellingen:** voeg uitsluitend toe als de samenstelling een zelfstandige juridische term is die als zodanig in wetgeving voorkomt. Gebruik de tabel:

| Stam | Vaste toevoeging |
|------|-----------------|
| termijn | termijnen, betalingstermijn, betalingstermijnen |
| beslag | beslagen, beslaglegging |
| uitstel | uitstel van betaling |
| aansprakelijk | aansprakelijkheid, aansprakelijkheden |
| dwangbevel | dwangbevelen |
| kwijtscheld | kwijtschelding, kwijtschelding van belasting |
| verjaring | verjaringstermijn, verjaringstermijnen |
| verrekening | verrekenen |

**Regel 3 — Maximaal:** de variantenlijst bevat maximaal 4 termen. Kies de meest voorkomende als er meer dan 4 zouden ontstaan.

Noteer de definitieve variantenlijst als: `[v1, v2, v3, ...]` en gebruik deze exact in alle volgende stappen.

---

## Stap 2 — Parallelle zoekoproepen via MCP

Roep **gelijktijdig** `wettenbank_ophalen` aan voor alle vijf bronnen met de primaire zoekterm `$ARGUMENTS`. Herhaal direct daarna voor elke variant die de primaire zoekterm niet al dekt. Combineer alle unieke artikelen per bron.

| Bron | BWB-id |
|------|--------|
| Invorderingswet 1990 | `BWBR0004770` |
| Leidraad Invordering 2008 | `BWBR0024096` |
| Uitvoeringsbesluit Invorderingswet 1990 | `BWBR0004772` |
| AWR | `BWBR0002320` |
| Awb | `BWBR0005537` |

Noteer per bron:
- Geldigheidsdatum van de geraadpleegde versie (uit het MCP-resultaat — gebruik exact deze datum)
- Alle gevonden artikelnummers (nog niet sorteren)
- Volledige letterlijke tekst van elk gevonden artikel, inclusief alle leden en onderdelen

Bij 0 resultaten op alle varianten: noteer "geen treffer" voor die bron en ga door.

---

## Stap 3 — Awb-toepasselijkheidscheck

Stel vast welke Awb-titels zijn uitgesloten via art. 1 lid 2 IW 1990. Citeer art. 1 lid 2 letterlijk. Vermeld per gevonden Awb-artikel of de betreffende titel van toepassing is of uitgesloten.

---

## Stap 4 — Kruisreferentie-inventarisatie

Scan de in Stap 2 verkregen artikelteksten op expliciete verwijzingen. Neem uitsluitend verwijzingen op die **letterlijk in de tekst staan** als "artikel X" of "artikel X, lid Y" of "artikel X, onderdeel Y". Voeg geen verwijzingen toe op basis van eigen kennis.

Categoriseer elke gevonden verwijzing:
- **Intern**: verwijzing naar een artikel binnen dezelfde bron — tekst al beschikbaar uit Stap 2
- **Extern**: verwijzing naar een andere bron — haal de betreffende artikeltekst op via `wettenbank_ophalen`

---

## Stap 5 — Statistieken berekenen

Tel per bron:
- **Aantal artikelen met treffer**: het aantal unieke artikelnummers uit Stap 2
- **Aantal vermeldingen**: tel hoe vaak de zoekterm of een variant letterlijk voorkomt in alle gevonden artikelteksten samen per bron (exact tellen, geen schatting)
- **Artikelnummers**: sorteer oplopend, numeriek (1, 2, 3…; bij letters na het nummer: 1, 2, 2a, 2b, 3…)

---

## Stap 6 — Rapport genereren en opslaan

Sla het rapport op als:
```
analyses/$ARGUMENTS-[TIMESTAMP].md
```
Haal de timestamp op via `date +%Y-%m-%d_%H-%M-%S`.

Genereer het rapport strikt conform het format hieronder. Elk veld is verplicht. Gebruik exact de voorgeschreven koppen en tabelstructuren.

---

## Rapportformat (elk veld verplicht, volgorde onwijzigbaar)

```markdown
---
zoekterm: "$ARGUMENTS"
varianten: [[v1], [v2], [v3], …]
datum: [YYYY-MM-DD]
timestamp: [YYYY-MM-DD_HH-MM-SS]
wetten:
  - IW 1990 (BWBR0004770)
  - Leidraad Invordering 2008 (BWBR0024096)
  - UB IW 1990 (BWBR0004772)
  - AWR (BWBR0002320)
  - Awb (BWBR0005537)
---

# Wetsanalyse: "$ARGUMENTS"

**Datum:** [DATUM]
**Doorzochte bronnen:** Invorderingswet 1990 · Leidraad Invordering 2008 · Uitvoeringsbesluit IW 1990 · AWR · Awb
**Peildatum wetgeving:** IW 1990: [datum] | Leidraad: [datum] | UB IW 1990: [datum] | AWR: [datum] | Awb: [datum]
**Gezochte varianten:** [v1], [v2], [v3], …

---

## 1. Statistieken

| Bron | Artikelen met treffer | Aantal vermeldingen | Artikelnummers (oplopend) |
|------|-----------------------|---------------------|---------------------------|
| IW 1990 | [n] | [n] | art. X, Y, Z |
| Leidraad Invordering | [n] | [n] | art. X, Y, Z |
| UB IW 1990 | [n] | [n] | art. X, Y, Z |
| AWR | [n] | [n] | art. X, Y, Z |
| Awb | [n] | [n] | art. X, Y, Z |
| **Totaal** | **[n]** | **[n]** | |

---

## 2. Vindplaatsen per bron

[Volgorde van secties altijd: 2.1 IW 1990 → 2.2 Leidraad → 2.3 UB IW 1990 → 2.4 AWR → 2.5 Awb]
[Artikelen binnen elke sectie altijd oplopend gesorteerd op artikelnummer]

### 2.1 Invorderingswet 1990 (BWBR0004770)

> *[Naam van het hoofdstuk en de afdeling, letterlijk uit de wetstekst]*

#### Artikel [X] (IW 1990)

> [Volledige letterlijke wetstekst, inclusief alle leden en onderdelen]

**Vindplaats zoekterm:** De term "[zoekterm of variant]" komt voor in [lid X / onderdeel Y].
**Rechtsgevolg:** [Één zin: wat is het directe rechtsgevolg van dit artikel voor de betalingsplicht of invorderingsbevoegdheid.]

---

### 2.2 Leidraad Invordering 2008 (BWBR0024096)

[Zelfde structuur. Bij geen treffer: schrijf exact: "Geen treffer voor varianten [v1, v2, …]. De Leidraad gebruikt voor dit begrip mogelijk een andere term."]

### 2.3 Uitvoeringsbesluit IW 1990 (BWBR0004772)

[Zelfde structuur. Bij geen treffer: zelfde standaardmelding.]

### 2.4 Algemene wet inzake rijksbelastingen (BWBR0002320)

[Zelfde structuur.]

### 2.5 Algemene wet bestuursrecht (BWBR0005537)

[Zelfde structuur, plus:]

**Awb-toepasselijkheid (art. 1 lid 2 IW 1990):**

> [Letterlijk citaat van art. 1 lid 2 IW 1990]

| Awb-titel / afdeling | Gevonden artikel | Van toepassing? |
|----------------------|------------------|-----------------|
| [Titel X.Y] | Art. [X:Y] | Ja / Nee — [reden] |

---

## 3. Kruisreferenties

[Alleen expliciete verwijzingen die letterlijk in de artikeltekst staan. Geen aanvullingen op basis van eigen kennis.]

### 3.1 Interne verwijzingen

| Artikel (bron) | Verwijst naar | Letterlijke verwijzingstekst |
|----------------|---------------|------------------------------|
| Art. X lid Y [wet] | Art. Z [wet] | "[exacte formulering uit de tekst]" |

[Bij geen interne verwijzingen: "Geen interne verwijzingen gevonden in de artikelteksten."]

### 3.2 Externe verwijzingen

| Artikel (bron) | Verwijst naar | Wet | Letterlijke verwijzingstekst | Geciteerde doeltekst |
|----------------|---------------|-----|------------------------------|----------------------|
| Art. X [wet] | Art. Y [wet] | [wet] | "[exacte formulering]" | "[letterlijke tekst van het gerefereerde lid]" |

[Bij geen externe verwijzingen: "Geen externe verwijzingen gevonden in de artikelteksten."]

---

## 4. Juridische samenvatting

### 4.1 Betekenis en gebruik van de term

Beantwoord de volgende drie vragen in deze volgorde, elk als afzonderlijke alinea:

1. **Primaire betekenis in de IW 1990:** Wat regelt de IW 1990 specifiek met betrekking tot "[zoekterm]"? Baseer dit uitsluitend op de in §2 geciteerde wetstekst.
2. **Meerdere betekenissen:** Wordt de term in de gevonden artikelen in meer dan één juridische betekenis gebruikt? Zo ja: benoem elke betekenis en de vindplaats. Zo nee: schrijf "De term wordt in de gevonden artikelen in één betekenis gebruikt."
3. **Verhouding IW 1990 – AWR – Awb:** Hoe verhoudt het gebruik in de IW 1990 zich tot het gebruik in de AWR en de Awb op basis van de gevonden artikelen?

### 4.2 Samenhang tussen de bronnen

Beantwoord de volgende drie vragen in deze volgorde, elk als afzonderlijke alinea:

1. **Lex specialis:** Welke bron bevat de primaire normstelling voor "[zoekterm]" en waarom is die lex specialis ten opzichte van de andere bronnen?
2. **Leidraad als beleidskader:** Hoe vult de Leidraad Invordering de wettelijke bepalingen aan? Verwijs naar het specifieke Leidraad-artikel uit §2. Bij geen treffer: "De Leidraad bevat geen bepalingen met de zoekterm; raadpleeg de Leidraad op aanverwante termen."
3. **Awb-toepasselijkheid:** Welke Awb-titels zijn op grond van art. 1 lid 2 IW 1990 van toepassing en welke zijn uitgesloten? Verwijs naar de tabel in §2.5.

### 4.3 Spanningsvelden

Gebruik uitsluitend de in §2 gevonden wetstekst als grondslag. Vul de tabel in voor elk geconstateerd spanningsveld. Bij geen spanningsvelden: schrijf de standaardzin exact als: "Op basis van de gevonden artikelen zijn geen spanningsvelden geconstateerd."

| Nr | Spanning | Betrokken artikelen | Type |
|----|---------|---------------------|------|
| 1 | [omschrijving] | Art. X [wet] – Art. Y [wet] | Onduidelijk / Meerduidig / Conflicterend |

### 4.4 Aandachtspunten voor de praktijk

Geef **precies 3** genummerde aandachtspunten. Elk aandachtspunt heeft exact de volgende structuur:

**[Nr]. [Titel van het aandachtspunt]**
*Vindplaats:* Art. X, lid Y [wet]
*Gevolg voor de praktijk:* [Één zin over wat de ontvanger of belastingschuldige moet doen of nalaten.]

### 4.5 Relevante jurisprudentie en beleid

Neem uitsluitend op:
- Verwijzingen naar Leidraad-artikelen die in §2 zijn gevonden
- Arresten die algemeen bekend zijn in het invorderingsrecht en direct betrekking hebben op de gevonden artikelen

Gebruik voor elk item exact dit format:

**[Naam / omschrijving]**
*Vindplaats:* [Leidraad art. X / HR [datum] / anders]
*Relevantie:* [Één zin.]
*Status:* Geverifieerd / **Verificatie vereist**

Sluit altijd af met deze vaste zin:
"Voor actuele jurisprudentie wordt raadpleging van rechtspraak.nl en de Leidraad Invordering (actuele versie) aanbevolen."

---

## 5. Bronnen

| Bron | BWB-id | Geraadpleegde versie | Vindplaats |
|------|--------|----------------------|------------|
| Invorderingswet 1990 | BWBR0004770 | [peildatum uit MCP] | wetten.overheid.nl |
| Leidraad Invordering 2008 | BWBR0024096 | [peildatum uit MCP] | wetten.overheid.nl |
| UB IW 1990 | BWBR0004772 | [peildatum uit MCP] | wetten.overheid.nl |
| AWR | BWBR0002320 | [peildatum uit MCP] | wetten.overheid.nl |
| Awb | BWBR0005537 | [peildatum uit MCP] | wetten.overheid.nl |
```

---

## Kwaliteitseisen (niet-onderhandelbaar)

- **Nooit parafraseren.** Wetstekst altijd letterlijk en volledig citeren.
- **Vijf bronnen altijd doorzoeken.** Ook als de verwachting is dat een bron niets oplevert.
- **Artikelvolgorde altijd oplopend.** Binnen elke bron: numeriek oplopend op artikelnummer.
- **Vermeldingen exact tellen.** Geen schattingen; tel het werkelijke aantal keren dat de zoekterm of variant voorkomt in de opgehaalde tekst.
- **Kruisreferenties alleen uit de tekst.** Geen verwijzingen toevoegen op basis van eigen kennis.
- **Samenvatting via vaste vragen.** Beantwoord de vragen in §4.1 t/m §4.4 in de voorgeschreven volgorde en structuur.
- **Precies 3 aandachtspunten.** Niet meer, niet minder; elk met vindplaats en praktijkgevolg.
- **Jurisprudentie altijd met status.** Elk item heeft "Geverifieerd" of "Verificatie vereist"; nooit ECLI-nummers fabriceren.
- **Standaardzin jurisprudentie altijd sluiten.** De vaste slotalinea is verplicht.
- **Nulresultaten standaardmelding.** Gebruik exact de voorgeschreven tekst bij geen treffer.
- **Peildatum uit MCP.** Gebruik de datum die het MCP-resultaat teruggeeft, niet de datum van vandaag.
- **Altijd opslaan.** Rapport als MD-bestand in `analyses/`.
