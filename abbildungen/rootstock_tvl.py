"""Abbildung A2 des Artikels „DeFi mit Bitcoin": Rootstock-TVL-Verlauf.

Datenbasis: eingecheckter DeFiLlama-Snapshot daten/rootstock_tvl.json
(erzeugt von snapshot_bitcoin.py — reproduzierbar, harte Regel 3).
Gestaltung wie tvl.py/titelgrafik.py (stil.py); ATH als Ereignismarke.

Aufruf:  python abbildungen/rootstock_tvl.py
Ausgabe: abbildungen/out/rootstock_tvl.pdf|svg
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


def lade_daten():
    punkte = json.loads(DATEN.read_text())
    tage = [datetime.fromtimestamp(p["date"]).date() for p in punkte]
    mio = [p["tvl"] / 1e6 for p in punkte]
    return tage, mio


def zeichne(tage, mio) -> None:
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 2.6))

    ax.fill_between(tage, mio, color=stil.BLAU, alpha=0.13, linewidth=0)
    ax.plot(tage, mio, color=stil.BLAU, linewidth=1.4)

    # ATH als Ereignismarke (fällt auf den zweiten Gipfel des Gesamtsektors);
    # Kopffreiheit über dem Maximum, damit die Beschriftung die Kurve nicht schneidet
    i_ath = max(range(len(mio)), key=lambda i: mio[i])
    ax.annotate(
        f"Hoch: {stil.deutsches_zahlenformat(mio[i_ath])} Mio. USD "
        f"({tage[i_ath].strftime('%d.%m.%Y')})",
        xy=(tage[i_ath], mio[i_ath]), xytext=(-8, 8),
        textcoords="offset points", ha="right", va="bottom",
        fontsize=8, color=stil.TINTE_SEKUNDAER,
    )

    ax.set_ylim(0, max(mio) * 1.16)
    ax.set_ylabel("TVL (Mio. US-Dollar)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    stil.achsen_aufraeumen(ax)
    stil.quellenzeile(
        fig, f"Total Value Locked der Rootstock-Chain · Daten: DeFiLlama, "
             f"Stand: {stil.stichtag_text(tage[-1])}")

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"rootstock_tvl.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/rootstock_tvl.pdf|svg — letzter Punkt {tage[-1]}")


if __name__ == "__main__":
    zeichne(*lade_daten())
