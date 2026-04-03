#!/usr/bin/env python3
"""
wettenbank_xml.py — Haal de volledige XML van een wet op uit het Basiswettenbestand.
Omzeilt de 50KB-limiet van de MCP-server.

Gebruik:
    python3 wettenbank_xml.py BWBR0005537               # Awb, meest recente versie
    python3 wettenbank_xml.py BWBR0005537 2026-01-01    # Awb, specifieke peildatum
    python3 wettenbank_xml.py BWBR0005537 --artikel 3:40
    python3 wettenbank_xml.py BWBR0005537 --lijst       # alle artikelnummers tonen
    python3 wettenbank_xml.py BWBR0005537 --cache-pad   # pad naar lokale XML

Cache: ~/.cache/wettenbank/<BWB_ID>_<versie>.xml (wordt hergebruikt)
"""

import sys
import re
import argparse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date

# ── Configuratie ──────────────────────────────────────────────────────────────

CACHE_DIR    = Path.home() / ".cache" / "wettenbank"
BASE_URL     = "https://repository.officiele-overheidspublicaties.nl/bwb"
MANIFEST_URL = BASE_URL + "/{bwb_id}/manifest.xml"
XML_URL      = BASE_URL + "/{bwb_id}/{versie}/xml/{bwb_id}_{versie}.xml"

# ── Versie-ontdekking via manifest.xml ────────────────────────────────────────

def haal_versie_op(bwb_id: str, peildatum: str | None) -> str:
    """
    Ontdek de versie-string via manifest.xml.
    Retourneert bijv. '2026-01-01_0'.
    Zonder peildatum: gebruik _latestItem uit de manifest-root.
    Met peildatum: zoek de expressie waarvan datum_inwerkingtreding <= peildatum < einddatum.
    """
    url = MANIFEST_URL.format(bwb_id=bwb_id)
    print(f"Manifest ophalen: {url}", file=sys.stderr)

    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        print(f"HTTP-fout {e.code}: {e.reason}\nURL: {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Verbindingsfout: {e.reason}", file=sys.stderr)
        sys.exit(1)

    root = ET.fromstring(data)

    # Zonder peildatum: gebruik _latestItem
    if not peildatum:
        latest = root.get("_latestItem", "")
        if latest:
            # Formaat: "2026-01-01_0/xml/BWBR0005537_2026-01-01_0.xml"
            versie = latest.split("/")[0]
            print(f"Meest recente versie: {versie}", file=sys.stderr)
            return versie
        # Fallback: neem de laatste expression
        expressies = root.findall("expression")
        if expressies:
            versie = expressies[-1].get("label", "")
            print(f"Versie (laatste expressie): {versie}", file=sys.stderr)
            return versie
        print("Geen versie gevonden in manifest.", file=sys.stderr)
        sys.exit(1)

    # Met peildatum: zoek de juiste expressie
    zoek = peildatum
    kandidaten = []
    for expr in root.findall("expression"):
        meta = expr.find("metadata")
        if meta is None:
            continue
        inwt = (meta.findtext("datum_inwerkingtreding") or "").strip()
        eind = (meta.findtext("einddatum") or "9999-12-31").strip() or "9999-12-31"
        if inwt <= zoek <= eind:
            kandidaten.append((inwt, expr.get("label", "")))

    if not kandidaten:
        # Neem de meest recente versie vóór de peildatum
        eerdere = []
        for expr in root.findall("expression"):
            meta = expr.find("metadata")
            if meta is None:
                continue
            inwt = (meta.findtext("datum_inwerkingtreding") or "").strip()
            if inwt <= zoek:
                eerdere.append((inwt, expr.get("label", "")))
        if eerdere:
            kandidaten = [max(eerdere, key=lambda x: x[0])]

    if not kandidaten:
        print(f"Geen versie gevonden voor peildatum {zoek}.", file=sys.stderr)
        sys.exit(1)

    versie = kandidaten[-1][1]
    print(f"Versie voor {zoek}: {versie}", file=sys.stderr)
    return versie


# ── XML downloaden met cache ──────────────────────────────────────────────────

def haal_xml_op(bwb_id: str, versie: str) -> Path:
    """
    Download de volledige XML naar de cache. Hergebruik bij bestaand bestand.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_pad = CACHE_DIR / f"{bwb_id}_{versie}.xml"

    if cache_pad.exists():
        grootte_kb = cache_pad.stat().st_size / 1024
        print(f"Cache gevonden: {cache_pad} ({grootte_kb:.0f} KB)", file=sys.stderr)
        return cache_pad

    url = XML_URL.format(bwb_id=bwb_id, versie=versie)
    print(f"XML downloaden: {url}", file=sys.stderr)

    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        print(f"HTTP-fout {e.code}: {e.reason}\nURL: {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Verbindingsfout: {e.reason}", file=sys.stderr)
        sys.exit(1)

    cache_pad.write_bytes(data)
    grootte_kb = len(data) / 1024
    print(f"Opgeslagen: {cache_pad} ({grootte_kb:.0f} KB)", file=sys.stderr)
    return cache_pad


# ── Artikel-extractie uit BWB-XML ─────────────────────────────────────────────

def _tekst_van_node(node) -> str:
    """Extraheer platte tekst uit een XML-node, whitespace genormaliseerd.
    Strips ook de trailing metadata (publicatienummers/datums) die de BWB-XML toevoegt."""
    tekst = "".join(node.itertext())
    tekst = re.sub(r"\s+", " ", tekst).strip()
    # Strip trailing metadata: patroon zoals "201268227-12-201220-12-201232450..."
    # of "1994 1 06-01-1994 29-12-1993..."
    tekst = re.sub(r"\s*\d{4}\s*\d+\s*\d{2}-\d{2}-\d{4}.*$", "", tekst).strip()
    return tekst


def extraheer_artikel(xml_pad: Path, artikelnummer: str) -> str | None:
    """
    Zoek een artikel op nummer in de BWB-XML.
    Werkt namespace-agnostisch: strips namespace-prefix uit tagnamen.
    Retourneert de volledige genormaliseerde tekst, of None als niet gevonden.
    """
    tree = ET.parse(xml_pad)
    root = tree.getroot()

    def lokaal(tag: str) -> str:
        return tag.split("}")[-1] if "}" in tag else tag

    for node in root.iter():
        if lokaal(node.tag) != "artikel":
            continue
        # Zoek <kop><nr> binnen dit artikel
        for kop in node:
            if lokaal(kop.tag) != "kop":
                continue
            for nr_el in kop:
                if lokaal(nr_el.tag) == "nr" and nr_el.text:
                    if nr_el.text.strip() == str(artikelnummer):
                        return _tekst_van_node(node)

    return None


def lijst_artikelen(xml_pad: Path) -> list[str]:
    """Retourneer alle artikelnummers in volgorde van voorkomen."""
    tree = ET.parse(xml_pad)
    root = tree.getroot()

    def lokaal(tag: str) -> str:
        return tag.split("}")[-1] if "}" in tag else tag

    nummers = []
    for node in root.iter():
        if lokaal(node.tag) != "artikel":
            continue
        for kop in node:
            if lokaal(kop.tag) != "kop":
                continue
            for nr_el in kop:
                if lokaal(nr_el.tag) == "nr" and nr_el.text:
                    nummers.append(nr_el.text.strip())
    return nummers


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Haal de volledige wetstekst op uit het Basiswettenbestand (omzeilt MCP 50KB-limiet).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("bwb_id", help="BWB-id, bijv. BWBR0005537 (Awb)")
    parser.add_argument("peildatum", nargs="?", default=None,
                        help="Peildatum YYYY-MM-DD (standaard: meest recente versie)")
    parser.add_argument("--artikel", "-a", metavar="NR",
                        help="Extraheer één artikel, bijv. 3:40 of 25")
    parser.add_argument("--lijst", "-l", action="store_true",
                        help="Toon alle artikelnummers in de wet")
    parser.add_argument("--cache-pad", action="store_true",
                        help="Toon het pad naar het lokale XML-cachebestand en stop")

    args = parser.parse_args()

    versie  = haal_versie_op(args.bwb_id, args.peildatum)
    xml_pad = haal_xml_op(args.bwb_id, versie)

    if args.cache_pad:
        print(xml_pad)
        return

    if args.lijst:
        nummers = lijst_artikelen(xml_pad)
        print(f"Artikelen in {args.bwb_id} versie {versie} ({len(nummers)} totaal):")
        for nr in nummers:
            print(f"  Art. {nr}")
        return

    if args.artikel:
        tekst = extraheer_artikel(xml_pad, args.artikel)
        if tekst:
            print(tekst)
        else:
            print(f"Artikel {args.artikel} niet gevonden in {args.bwb_id}.", file=sys.stderr)
            sys.exit(1)
        return

    # Geen argument: toon artikellijst als samenvatting
    nummers = lijst_artikelen(xml_pad)
    print(f"{args.bwb_id} versie {versie} — {len(nummers)} artikelen beschikbaar.")
    print("Gebruik --lijst voor alle nummers of --artikel NR voor een specifiek artikel.")


if __name__ == "__main__":
    main()
