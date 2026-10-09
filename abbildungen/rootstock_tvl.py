"""Abbildung A2 des Artikels „DeFi mit Bitcoin": Rootstock-TVL-Verlauf.

Datenbasis: eingecheckter DeFiLlama-Snapshot daten/rootstock_tvl.json
(erzeugt von snapshot_bitcoin.py — reproduzierbar, harte Regel 3).
Gestaltung wie tvl.py/titelgrafik.py (stil.py); ATH als Ereignismarke.

Aufruf:  python abbildungen/rootstock_tvl.py [--en]
Ausgabe: abbildungen/out/rootstock_tvl[_en].pdf|svg
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent
DATEN = HIER / "daten" / "rootstock_tvl.json"

TEXTE = {
    "de": {
        "peak": "Hoch: {wert} Mio. USD ({datum})",
        "y_label": "TVL (Mio. US-Dollar)",
        "quelle": "Total Value Locked der Rootstock-Chain · Daten: DeFiLlama, "
                  "Stand: {stichtag}",
        "suffix": "",
    },
    "en": {
        "peak": "Peak: {wert} million USD ({datum})",
        "y_label": "TVL (million US dollars)",
        "quelle": "Total value locked of the Rootstock chain · Data: DeFiLlama, "
                  "as of {stichtag}",
        "suffix": "_en",
    },
}


def lade_daten():
    punkte = json.loads(DATEN.read_text())
    tage = [datetime.fromtimestamp(p["date"]).date() for p in punkte]
    mio = [p["tvl"] / 1e6 for p in punkte]
    return tage, mio


def zeichne(tage, mio, sprache="de") -> None:
    t = TEXTE[sprache]
    en = sprache == "en"
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 2.6))

    ax.fill_between(tage, mio, color=stil.BLAU, alpha=0.13, linewidth=0)
    ax.plot(tage, mio, color=stil.BLAU, linewidth=1.4)

    # ATH als Ereignismarke (fällt auf den zweiten Gipfel des Gesamtsektors);
    # Kopffreiheit über dem Maximum, damit die Beschriftung die Kurve nicht schneidet
    i_ath = max(range(len(mio)), key=lambda i: mio[i])
    ax.annotate(
        t["peak"].format(
            wert=f"{mio[i_ath]:,.1f}" if en else stil.deutsches_zahlenformat(mio[i_ath]),
            datum=tage[i_ath].strftime("%d %b %Y" if en else "%d.%m.%Y")),
        xy=(tage[i_ath], mio[i_ath]), xytext=(-8, 8),
        textcoords="offset points", ha="right", va="bottom",
        fontsize=8, color=stil.TINTE_SEKUNDAER,
    )

    ax.set_ylim(0, max(mio) * 1.16)
    ax.set_ylabel(t["y_label"])
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    stil.achsen_aufraeumen(ax)
    stil.quellenzeile(
        fig, t["quelle"].format(
            stichtag=tage[-1].strftime("%-d %b %Y") if en
            else stil.stichtag_text(tage[-1])))

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"rootstock_tvl{t['suffix']}.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/rootstock_tvl{t['suffix']}.pdf|svg — letzter Punkt {tage[-1]}")


if __name__ == "__main__":
    zeichne(*lade_daten(), "en" if "--en" in sys.argv else "de")
