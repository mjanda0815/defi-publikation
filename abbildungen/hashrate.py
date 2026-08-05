"""Abbildung: Bitcoin-Hashrate, Verlauf ab 2016.

Ersetzt Abb. 2.2 des Originals (dort: Screenshot von BitInfoCharts).
Datenquelle: blockchain.com-API (https://api.blockchain.info/charts/hash-rate),
eingecheckter Snapshot unter daten/blockchain_info_hashrate.json (Einheit TH/s).

Aufruf:  python abbildungen/hashrate.py [--refresh]
Ausgabe: abbildungen/out/hashrate.pdf und .svg
"""

import json
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent
DATEN = HIER / "daten" / "blockchain_info_hashrate.json"
API = "https://api.blockchain.info/charts/hash-rate?timespan=all&format=json&sampled=false"

AB_JAHR = 2016  # linear ab 2016; davor liegt die Hashrate um Größenordnungen niedriger

# Halvings im dargestellten Zeitraum (Blockbelohnung halbiert sich)
HALVINGS = [
    (date(2016, 7, 9), "3. Halving\n(12,5 BTC)"),
    (date(2020, 5, 11), "4. Halving\n(6,25 BTC)"),
    (date(2024, 4, 20), "5. Halving\n(3,125 BTC)"),
]


def gleitender_mittelwert(werte, fenster: int):
    erg, summe = [], 0.0
    for i, w in enumerate(werte):
        summe += w
        if i >= fenster:
            summe -= werte[i - fenster]
        erg.append(summe / min(i + 1, fenster))
    return erg


def lade_daten(refresh: bool = False):
    if refresh or not DATEN.exists():
        print(f"Lade {API} …")
        with urllib.request.urlopen(API, timeout=90) as r:
            DATEN.write_bytes(r.read())
    rohdaten = json.loads(DATEN.read_text())
    assert rohdaten["unit"] == "Hash Rate TH/s", rohdaten["unit"]
    punkte = [
        (datetime.fromtimestamp(p["x"]).date(), p["y"] / 1e6)  # TH/s -> EH/s
        for p in rohdaten["values"]
    ]
    return [(t, w) for t, w in punkte if t.year >= AB_JAHR]


def zeichne(punkte) -> None:
    stil.aktiviere_stil()
    tage = [t for t, _ in punkte]
    ehs = [w for _, w in punkte]
    mittel = gleitender_mittelwert(ehs, 30)

    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 3.4))
    ax.plot(tage, ehs, color=stil.BLAU_HELL, linewidth=0.6)
    ax.plot(tage, mittel, color=stil.BLAU, linewidth=1.6)
    ax.set_ylabel("Hashrate in EH/s")
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: stil.deutsches_zahlenformat(v))
    )
    stil.achsen_aufraeumen(ax)

    for tag, beschriftung in HALVINGS:
        ax.axvline(tag, color=stil.EREIGNIS, linewidth=0.7, linestyle=(0, (2, 3)))
        ax.annotate(
            beschriftung, xy=(tag, ax.get_ylim()[1]),
            xytext=(3, -4), textcoords="offset points",
            fontsize=7.5, color=stil.GEDECKT, va="top",
        )

    # Legende als direkte Beschriftung: Tageswerte vs. 30-Tage-Mittel
    # (unterhalb der Halving-Label platziert, links ist die Kurve nahe null)
    ax.annotate(
        "Tageswerte (hell),\n30-Tage-Mittel (kräftig)",
        xy=(0.015, 0.87), xycoords="axes fraction",
        fontsize=8, color=stil.TINTE_SEKUNDAER, va="top",
    )

    letzter = tage[-1]
    stil.quellenzeile(
        fig,
        "Daten: blockchain.com (api.blockchain.info/charts/hash-rate), "
        f"Stand: {stil.stichtag_text(letzter)} · Eigene Darstellung",
    )

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"hashrate.{endung}")
    print(f"Geschrieben: {out}/hashrate.pdf|svg — letzter Datenpunkt {letzter}, "
          f"30-Tage-Mittel {stil.deutsches_zahlenformat(mittel[-1])} EH/s")


if __name__ == "__main__":
    zeichne(lade_daten(refresh="--refresh" in sys.argv))
