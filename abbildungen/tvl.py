"""Abbildung: Total Value Locked (TVL) im DeFi-Sektor, Gesamtverlauf.

Ersetzt Abb. 4.1 des Originals (dort: Screenshot von DeFiLlama).
Datenquelle: DeFiLlama-API (https://api.llama.fi/v2/historicalChainTvl),
eingecheckter Snapshot unter daten/defillama_tvl_gesamt.json.

Aufruf:  python abbildungen/tvl.py [--refresh]
Ausgabe: abbildungen/out/tvl.pdf und .svg
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
DATEN = HIER / "daten" / "defillama_tvl_gesamt.json"
API = "https://api.llama.fi/v2/historicalChainTvl"


def lade_daten(refresh: bool = False):
    if refresh or not DATEN.exists():
        print(f"Lade {API} …")
        with urllib.request.urlopen(API, timeout=60) as r:
            DATEN.write_bytes(r.read())
    punkte = json.loads(DATEN.read_text())
    tage = [datetime.fromtimestamp(p["date"]).date() for p in punkte]
    mrd = [p["tvl"] / 1e9 for p in punkte]
    # Reihe beginnt am 27.09.2017 bei ~0 TVL; die drei Rumpfmonate 2017 tragen
    # keine Information, lassen aber Achsenstart (erste Jahresmarke 2018) und
    # Bildunterschrift auseinanderfallen. Daher: volle Jahre ab 01.01.2018.
    ab = next(i for i, t in enumerate(tage) if t.year >= 2018)
    return tage[ab:], mrd[ab:]


def zeichne(tage, mrd) -> None:
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 3.4))

    ax.plot(tage, mrd, color=stil.BLAU, linewidth=1.4)
    ax.set_ylabel("TVL in Mrd. US-Dollar")
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: stil.deutsches_zahlenformat(v))
    )
    stil.achsen_aufraeumen(ax)

    # Höchststand direkt beschriften. Bewusst nur Monat/Jahr: Das Maximum vom
    # 09.11.2021 liegt nur 0,005 % über dem lokalen Hoch vom 02.12.2021 —
    # ein exakter Tagesstempel wäre datenrevisionsanfällig.
    MONATE = ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni",
              "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]
    i_max = max(range(len(mrd)), key=mrd.__getitem__)
    ax.scatter([tage[i_max]], [mrd[i_max]], s=14, color=stil.BLAU, zorder=3)
    ax.annotate(
        f"Höchststand {MONATE[tage[i_max].month - 1]} {tage[i_max].year}:\n"
        f"{stil.deutsches_zahlenformat(mrd[i_max], 1)} Mrd. USD",
        xy=(tage[i_max], mrd[i_max]),
        xytext=(-12, 4), textcoords="offset points",
        fontsize=8, color=stil.TINTE_SEKUNDAER, ha="right",
    )

    # Ereignismarker, die im Text der Arbeit diskutiert werden;
    # Terra links, FTX rechts der jeweiligen Linie beschriftet (kollisionsfrei)
    for tag in (date(2022, 5, 9), date(2022, 11, 11)):
        ax.axvline(tag, color=stil.EREIGNIS, linewidth=0.7, linestyle=(0, (2, 3)))
    ax.annotate(
        "Terra/UST-Kollaps", xy=(date(2022, 5, 9), 0.98), xycoords=("data", "axes fraction"),
        xytext=(4, 0), textcoords="offset points",
        fontsize=7.5, color=stil.GEDECKT, ha="left", va="top",
    )
    ax.annotate(
        "FTX-Insolvenz", xy=(date(2022, 11, 11), 0.89), xycoords=("data", "axes fraction"),
        xytext=(4, 0), textcoords="offset points",
        fontsize=7.5, color=stil.GEDECKT, ha="left", va="top",
    )

    letzter = tage[-1]
    stil.quellenzeile(
        fig,
        "Daten: DeFiLlama (api.llama.fi/v2/historicalChainTvl), "
        f"Stand: {stil.stichtag_text(letzter)} · Eigene Darstellung",
    )

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"tvl.{endung}")
    print(f"Geschrieben: {out}/tvl.pdf|svg — letzter Datenpunkt {letzter}, "
          f"{stil.deutsches_zahlenformat(mrd[-1], 1)} Mrd. USD")


if __name__ == "__main__":
    zeichne(*lade_daten(refresh="--refresh" in sys.argv))
