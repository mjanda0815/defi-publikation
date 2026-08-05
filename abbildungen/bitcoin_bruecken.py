"""Abbildung A1 des Artikels „DeFi mit Bitcoin": Brücken-Spektrum, zwei Panels.

Zwei getrennte Darstellungen statt einer gemischten (Lesedurchgang Martin,
05.08.2026): Oben die gepeggten bzw. gesperrten Bestände je Weg (heterogene
Verwendungszwecke, aber einheitliche Messgröße; Log-Skala, Spanne 45:1),
unten das in DeFi-Protokollen gebundene Kapital der programmierbaren
Bitcoin-Umgebungen (Chain-TVL, lineare Skala). So stehen nicht länger
Verwahrbestände und Chain-TVL im selben Balkendiagramm.
Datenbasis: eingecheckter Snapshot daten/bitcoin_bruecken.json.

Aufruf:  python abbildungen/bitcoin_bruecken.py
Ausgabe: abbildungen/out/bitcoin_bruecken.pdf|svg
"""

import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent
DATEN = HIER / "daten" / "bitcoin_bruecken.json"

# Lesbarkeit (Feedback Martin, 05.08.2026): größere Schrift, dunklere Farben
# als der gemeinsame stil.py-Standard — lokale Overrides, stil.py bleibt
# unverändert (Whitepaper-Abbildungen sind veröffentlicht).
LABELGROESSE = 10
TEXTFARBE = stil.TINTE            # Balken-Labels: volle Tinte statt Sekundärgrau
ACHSENFARBE = "#3f3e3b"           # Achsen-/Tick-Beschriftung: deutlich dunkler als GEDECKT
QUELLENFARBE = "#52514E"          # Quellenzeile: TINTE_SEKUNDAER statt GEDECKT


def lade_daten():
    b = json.loads(DATEN.read_text())
    p = b["btc_preis_usd"]
    # Panel 1: gepeggte/gesperrte Bestände (Name, Vertrauensannahme, USD, Bezugsgröße)
    bestaende = [
        ("wBTC (Ethereum)", "Verwahrer", b["wbtc_usd"], "Verwahrbestand"),
        ("Babylon (Staking)", "Covenant-Komitee", b["babylon_usd"], "gesperrte BTC"),
        ("tBTC", "51 von 100, rotierend", b["tbtc_usd"], "Token-Umlauf"),
        ("Liquid", "Föderation (2/3)", b["lbtc_btc"] * p, "Peg-Bestand"),
        ("Lightning", "nativ, je Kanal", b["lightning_usd"], "öffentl. Kanäle"),
        ("sBTC (Stacks)", "15 Signer, 70 %", b["sbtc_btc"] * p, "Token-Umlauf"),
    ]
    # Panel 2: Chain-TVL programmierbarer Bitcoin-Umgebungen
    ct = b["chain_tvl_usd"]
    chains = [
        ("Stacks", "sBTC: 15 Signer, 70 %", ct["Stacks"]),
        ("Rootstock", "PowPeg: Föderation (5 von 9)", ct["Rootstock"]),
        ("BOB", "Rollup; BitVM-Brücke im Test", ct["BOB"]),
        ("Citrea", "BitVM-Brücke, 1 von n", ct["Citrea"]),
    ]
    bestaende.sort(key=lambda w: w[2])
    chains.sort(key=lambda w: w[2])
    return bestaende, chains, date.fromisoformat(b["stichtag"]), p


def wert_text(usd: float) -> str:
    if usd >= 1e9:
        return f"{stil.deutsches_zahlenformat(usd / 1e9, 1)} Mrd."
    return f"{stil.deutsches_zahlenformat(usd / 1e6)} Mio."


def zeichne(bestaende, chains, stichtag, btc_preis) -> None:
    stil.aktiviere_stil()
    fig, (oben, unten) = plt.subplots(
        2, 1, figsize=(stil.BREITE_TEXT, 5.6),
        height_ratios=[len(bestaende), len(chains) + 0.6])

    # Panel 1: Bestände, logarithmisch (Spanne 45:1)
    oben.barh([w[0] for w in bestaende], [w[2] for w in bestaende],
              color=stil.BLAU, height=0.6)
    oben.set_xscale("log")
    for i, (_, vertrauen, usd, bezug) in enumerate(bestaende):
        oben.text(usd * 1.15, i, f"{wert_text(usd)} ({bezug})  ·  {vertrauen}",
                  va="center", ha="left", fontsize=LABELGROESSE,
                  color=TEXTFARBE)
    oben.set_xlim(right=max(w[2] for w in bestaende) * 40)
    oben.set_xlabel("gepeggter bzw. gesperrter Bestand (USD, logarithmische Skala)")

    # Panel 2: Chain-TVL, linear
    unten.barh([w[0] for w in chains], [w[2] for w in chains],
               color=stil.BLAU, height=0.6)
    for i, (_, vertrauen, usd) in enumerate(chains):
        unten.text(usd + max(w[2] for w in chains) * 0.02, i,
                   f"{wert_text(usd)}  ·  {vertrauen}",
                   va="center", ha="left", fontsize=LABELGROESSE,
                   color=TEXTFARBE)
    unten.set_xlim(right=max(w[2] for w in chains) * 2.4)
    unten.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: stil.deutsches_zahlenformat(x / 1e6)))
    unten.set_xlabel("in DeFi-Protokollen gebundenes Kapital (Chain-TVL, Mio. USD, linear)")

    for ax in (oben, unten):
        ax.grid(axis="y", visible=False)
        stil.achsen_aufraeumen(ax)
        ax.grid(axis="x", color=stil.RASTER, linewidth=0.6)
        ax.tick_params(axis="y", labelsize=11, labelcolor=TEXTFARBE)
        ax.tick_params(axis="x", labelsize=9.5, labelcolor=ACHSENFARBE)
        ax.xaxis.label.set_color(TEXTFARBE)
        ax.xaxis.label.set_size(10.5)

    fig.tight_layout(h_pad=2.2)
    # Quellenzeile zweizeilig: eine einzeilige Fassung wäre breiter als die
    # Achsen und bläht die tight-Bounding-Box auf — die Abbildung würde beim
    # Einbinden (Artikel, Karussell) entsprechend verkleinert.
    fig.text(0.005, -0.02,
             "Oben: Bestände je Weg (heterogene Verwendungszwecke, einheitliche Messgröße) · "
             "Unten: DeFi-Nutzung programmierbarer Bitcoin-Umgebungen\n"
             f"Umrechnung: {stil.deutsches_zahlenformat(btc_preis)} USD/BTC · Daten: DeFiLlama, "
             f"Blockstream, Hiro, mempool.space, Stand: {stil.stichtag_text(stichtag)}",
             fontsize=8.5, color=QUELLENFARBE, ha="left", va="top")

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"bitcoin_bruecken.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/bitcoin_bruecken.pdf|svg")


if __name__ == "__main__":
    zeichne(*lade_daten())
