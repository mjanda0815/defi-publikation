"""Referenzwerte: Stablecoin-Umlauf aus dem eingecheckten DeFiLlama-Snapshot.

Kein Diagramm — das Skript macht die im Text (Kap. 3.5.1) genannten Aggregate
reproduzierbar (Gütekriterium „Datengrundlage und Reproduzierbarkeit", Kap. 1.3).

Aufruf:  python abbildungen/stablecoins.py [--refresh]
Ausgabe: Top-Assets und Gesamtsumme der USD-gebundenen Stablecoins (Konsole)
"""

import json
import sys
import urllib.request
from pathlib import Path

HIER = Path(__file__).parent
DATEN = HIER / "daten" / "defillama_stablecoins.json"
API = "https://stablecoins.llama.fi/stablecoins?includePrices=false"


def lade(refresh: bool = False):
    if refresh or not DATEN.exists():
        print(f"Lade {API} …")
        with urllib.request.urlopen(API, timeout=60) as r:
            DATEN.write_bytes(r.read())
    return json.loads(DATEN.read_text())["peggedAssets"]


def main() -> None:
    assets = lade(refresh="--refresh" in sys.argv)
    usd = [a for a in assets if a.get("pegType") == "peggedUSD"]
    gesamt = sum(a["circulating"]["peggedUSD"] for a in usd)
    top = sorted(usd, key=lambda a: -a["circulating"]["peggedUSD"])[:6]
    print("USD-gebundene Stablecoins (Umlauf, Mrd. USD):")
    for a in top:
        print(f"  {a['name']:<28} {a['symbol']:<6} {a['circulating']['peggedUSD'] / 1e9:8.1f}")
    print(f"  {'GESAMT':<35} {gesamt / 1e9:8.1f}")


if __name__ == "__main__":
    main()
