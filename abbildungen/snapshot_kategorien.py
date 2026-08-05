"""Kategorien-Aggregation aus dem freien DeFiLlama-/protocols-Endpoint.

Hintergrund: Der dedizierte /categories-Endpoint ist inzwischen kostenpflichtig
(HTTP 402, Stand 03.08.2026). Die Kategorien-Summen lassen sich aber
reproduzierbar aus der freien Protokoll-Liste aggregieren (Summe der TVL je
category-Feld). Ergebnis wird als kompakter Snapshot eingecheckt und belegt
die Kategorien-Aussagen in Abschnitt 3.5.6, 4.6 und 6.2.

Hinweis zur Interpretation: CEX-, Bridge- und Canonical-Bridge-Einträge sind
Verwahr-/Brückenbestände, keine DeFi-Kategorien im Sinne dieser Arbeit
(gleiche Abgrenzung wie in Abschnitt 4.2.1/4.6).

Aufruf:  python abbildungen/snapshot_kategorien.py --refresh  (zieht neu)
         python abbildungen/snapshot_kategorien.py            (liest Snapshot)
"""

import json
import sys
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

HIER = Path(__file__).parent
DATEN = HIER / "daten" / "defillama_kategorien.json"
API = "https://api.llama.fi/protocols"


def erzeuge_snapshot() -> dict:
    req = urllib.request.Request(API, headers={"User-Agent": "Mozilla/5.0"})
    protokolle = json.loads(urllib.request.urlopen(req, timeout=120).read())
    agg = defaultdict(float)
    for p in protokolle:
        agg[p.get("category") or "unbekannt"] += p.get("tvl") or 0
    kategorien = [
        {"kategorie": k, "tvl_usd": round(v)}
        for k, v in sorted(agg.items(), key=lambda kv: -kv[1])
        if v >= 1e8  # Rauschgrenze 0,1 Mrd — Kleinstkategorien entfallen
    ]
    return {
        "quelle": API,
        "stand": date.today().isoformat(),
        "hinweis": "TVL-Summe je category-Feld über alle Protokolle; "
                   "CEX/Bridge/Canonical Bridge sind keine DeFi-Kategorien "
                   "im Sinne der Arbeit.",
        "kategorien": kategorien,
    }


def main() -> None:
    if "--refresh" in sys.argv or not DATEN.exists():
        snap = erzeuge_snapshot()
        DATEN.write_text(json.dumps(snap, ensure_ascii=False, indent=1))
        print(f"Geschrieben: {DATEN} (Stand {snap['stand']})")
    else:
        snap = json.loads(DATEN.read_text())
        print(f"Snapshot vom {snap['stand']}:")
    for k in snap["kategorien"][:12]:
        print(f"  {k['kategorie']:24s} {k['tvl_usd']/1e9:7.1f} Mrd USD")


if __name__ == "__main__":
    main()
