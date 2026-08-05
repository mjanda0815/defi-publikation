"""Titelgrafik des Whitepapers: TVL-Verlauf 2017–2026 als ruhiges Flächenband.

Bewusst reduziert (Titelseite, kein Analyse-Chart): eine Serie, eine Farbe,
keine Gridlines, keine y-Achse — nur Jahresmarken und eine Quellenzeile mit
Stichtag (harte Regel 1: jede Zahl braucht Quelle + Stichtag; die Grafik
behauptet ohne y-Skala keine Einzelwerte, benennt aber Kennzahl und Quelle).
Datenbasis ist derselbe eingecheckte DeFiLlama-Snapshot wie in Abbildung 4.1
(daten/defillama_tvl_gesamt.json) — reproduzierbar, keine Fremdgrafik.

Aufruf:  python abbildungen/titelgrafik.py
Ausgabe: abbildungen/out/titelgrafik.pdf|svg
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
DATEN = HIER / "daten" / "defillama_tvl_gesamt.json"


def lade_daten():
    punkte = json.loads(DATEN.read_text())
    tage = [datetime.fromtimestamp(p["date"]).date() for p in punkte]
    mrd = [p["tvl"] / 1e9 for p in punkte]
    # Reihe beginnt am 27.09.2017 bei ~0 TVL; die drei Rumpfmonate 2017 tragen
    # keine Information, verschieben aber Achsenstart (erste Jahresmarke 2018)
    # gegen die Bildunterschrift. Daher: volle Jahre ab 01.01.2018.
    ab = next(i for i, t in enumerate(tage) if t.year >= 2018)
    return tage[ab:], mrd[ab:]


def zeichne(tage, mrd) -> None:
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 1.7))

    ax.fill_between(tage, mrd, color=stil.BLAU, alpha=0.13, linewidth=0)
    ax.plot(tage, mrd, color=stil.BLAU, linewidth=1.5)

    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", labelsize=8)

    # Titelseiten-Reduktion: keine y-Achse, kein Raster — nur die Grundlinie.
    ax.grid(visible=False)
    ax.set_yticks([])
    for seite in ("top", "right", "left"):
        ax.spines[seite].set_visible(False)
    ax.spines["bottom"].set_color(stil.GRUNDLINIE)
    ax.tick_params(length=0)
    ax.margins(x=0.01)

    # zentrierte Quellenzeile (Titelseite) statt stil.quellenzeile (linksbündig);
    # Zeitraum wird aus den Daten abgeleitet — Achse und Unterschrift immer konsistent
    fig.text(
        0.5, -0.02,
        f"Total Value Locked in DeFi-Protokollen, {tage[0].year}–{tage[-1].year} · "
        f"Daten: DeFiLlama, Stand: {stil.stichtag_text(tage[-1])}",
        fontsize=7.5, color=stil.GEDECKT, ha="center", va="top",
    )

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"titelgrafik.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/titelgrafik.pdf|svg — letzter Datenpunkt {tage[-1]}")


if __name__ == "__main__":
    zeichne(*lade_daten())
