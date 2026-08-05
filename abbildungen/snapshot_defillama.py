"""Snapshot-Skript für die DeFiLlama-Referenzdaten (Kap. 4.6/4.7, 5.1).

Erzeugt reproduzierbar die eingecheckten Snapshots (Gütekriterium
„Datengrundlage und Reproduzierbarkeit", Kap. 1.3):
- daten/defillama_protokolle.json — Top-30 Protokolle nach TVL PLUS die sechs
  Fallstudien-Protokolle (dokumentierter Filter; Endpunkt /protocols)
- daten/defillama_chains.json — TVL je Blockchain (Endpunkt /v2/chains)

Aufruf:  python abbildungen/snapshot_defillama.py [--refresh]
Ohne --refresh werden nur die vorhandenen Snapshots zusammengefasst.
"""

import json
import sys
import urllib.request
from pathlib import Path

HIER = Path(__file__).parent
DATEN = HIER / "daten"

FALLSTUDIEN = {"aave", "compound", "compound-v2", "compound-v3", "uniswap",
               "pancakeswap", "curve-dex", "nexus-mutual", "opyn", "morpho",
               "lido", "sky", "makerdao", "eigenlayer", "yearn-finance",
               "dydx", "synthetix"}


def hole(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())


def refresh() -> None:
    prot = hole("https://api.llama.fi/protocols")
    def relevant(p):
        eltern = (p.get("parentProtocol") or "").replace("parent#", "")
        return p.get("slug") in FALLSTUDIEN or eltern in FALLSTUDIEN
    nach_tvl = sorted(prot, key=lambda p: -(p.get("tvl") or 0))
    auswahl = {p["slug"] for p in nach_tvl[:30]} | {p["slug"] for p in prot if relevant(p)}
    aus = [{k: p.get(k) for k in ("name", "slug", "category", "tvl", "chains", "parentProtocol")}
           for p in nach_tvl if p["slug"] in auswahl]
    (DATEN / "defillama_protokolle.json").write_text(json.dumps(aus, indent=1))

    chains = hole("https://api.llama.fi/v2/chains")
    (DATEN / "defillama_chains.json").write_text(json.dumps(chains, indent=1))


def bericht() -> None:
    prot = json.loads((DATEN / "defillama_protokolle.json").read_text())
    print("Top 10 Protokolle nach TVL (Mrd. USD):")
    for p in prot[:10]:
        print(f"  {p['name']:<28}{p['category']:<20}{(p['tvl'] or 0)/1e9:8.2f}")
    chains = json.loads((DATEN / "defillama_chains.json").read_text())
    tot = sum(c["tvl"] for c in chains)
    top = sorted(chains, key=lambda c: -c["tvl"])[:5]
    print("\nTop 5 Chains (Anteil am Gesamt-TVL):")
    for c in top:
        print(f"  {c['name']:<12}{c['tvl']/1e9:8.2f} Mrd  {100*c['tvl']/tot:5.1f} %")


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        refresh()
    bericht()
