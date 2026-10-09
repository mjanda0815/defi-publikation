"""Abbildung A1 des Artikels „DeFi mit Bitcoin": Brücken-Spektrum, zwei Panels.

Zwei getrennte Darstellungen statt einer gemischten (Lesedurchgang Martin,
05.08.2026): Oben die gepeggten bzw. gesperrten Bestände je Weg (heterogene
Verwendungszwecke und Messgrößen, Berichtswährung USD; Log-Skala, Spanne 45:1),
unten das in DeFi-Protokollen gebundene Kapital der programmierbaren
Bitcoin-Umgebungen (Chain-TVL, lineare Skala). So stehen nicht länger
Verwahrbestände und Chain-TVL im selben Balkendiagramm.
Datenbasis: eingecheckter Snapshot daten/bitcoin_bruecken.json.

Aufruf:  python abbildungen/bitcoin_bruecken.py [--en]
Ausgabe: abbildungen/out/bitcoin_bruecken[_en].pdf|svg
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

TEXTE = {
    "de": {
        "verwahrer": "Verwahrer",
        "covenant": "Covenant-Komitee",
        "tbtc": "51 von 100, rotierend",
        "foederation": "Föderation (2/3)",
        "lightning": "nativ, je Kanal",
        "sbtc": "15 Signer, 70 %",
        "bz_wbtc": "Verwahrbestand",
        "bz_babylon": "gesperrte BTC",
        "bz_umlauf": "Token-Umlauf",
        "bz_peg": "Buchbestand",
        "bz_kanaele": "öffentl. Kanäle",
        "c_stacks": "sBTC: 15 Signer, 70 %",
        "c_rootstock": "PowPeg: Föderation (5 von 9)",
        "c_bob": "Rollup; BitVM-Brücke im Test",
        "c_citrea": "BitVM-Brücke, 1 von n",
        "mrd": "Mrd.",
        "mio": "Mio.",
        "xlabel_oben": "gepeggter bzw. gesperrter Bestand (USD, logarithmische Skala)",
        "xlabel_unten": "in DeFi-Protokollen gebundenes Kapital (Chain-TVL, Mio. USD, linear)",
        "fuss": "Oben: Bestände je Weg (heterogene Zwecke und Messgrößen, Berichtswährung USD) · "
                "Unten: DeFi-Nutzung programmierbarer Bitcoin-Umgebungen\n"
                "Umrechnung: {preis} USD/BTC · Daten: DeFiLlama, "
                "Blockstream, Hiro, mempool.space, Stand: {stichtag}",
        "suffix": "",
    },
    "en": {
        "verwahrer": "custodian",
        "covenant": "covenant committee",
        "tbtc": "51 of 100, rotating",
        "foederation": "federation (2/3)",
        "lightning": "native, per channel",
        "sbtc": "15 signers, 70 %",
        "bz_wbtc": "custodied balance",
        "bz_babylon": "locked BTC",
        "bz_umlauf": "token supply",
        "bz_peg": "book balance",
        "bz_kanaele": "public channels",
        "c_stacks": "sBTC: 15 signers, 70 %",
        "c_rootstock": "PowPeg: federation (5 of 9)",
        "c_bob": "rollup; BitVM bridge in testing",
        "c_citrea": "BitVM bridge, 1 of n",
        "mrd": "bn",
        "mio": "m",
        "xlabel_oben": "pegged or locked balance (USD, logarithmic scale)",
        "xlabel_unten": "capital committed in DeFi protocols (chain TVL, million USD, linear)",
        "fuss": "Top: balances per route (heterogeneous purposes and measures, reported in USD) · "
                "Bottom: DeFi usage of programmable Bitcoin environments\n"
                "Conversion: {preis} USD/BTC · Data: DeFiLlama, "
                "Blockstream, Hiro, mempool.space, as of {stichtag}",
        "suffix": "_en",
    },
}


def zahl(wert: float, nachkomma: int, en: bool) -> str:
    if en:
        return f"{wert:,.{nachkomma}f}"
    return stil.deutsches_zahlenformat(wert, nachkomma)


def lade_daten(t=TEXTE["de"]):
    b = json.loads(DATEN.read_text())
    p = b["btc_preis_usd"]
    # Panel 1: gepeggte/gesperrte Bestände (Name, Vertrauensannahme, USD, Bezugsgröße)
    bestaende = [
        ("wBTC (Ethereum)", t["verwahrer"], b["wbtc_usd"], t["bz_wbtc"]),
        ("Babylon (Staking)", t["covenant"], b["babylon_usd"], t["bz_babylon"]),
        ("tBTC", t["tbtc"], b["tbtc_usd"], t["bz_umlauf"]),
        ("Liquid", t["foederation"], b["lbtc_btc"] * p, t["bz_peg"]),
        # Kanalkapazität (mempool.space) zum Snapshot-Kurs — konsistent zur
        # Tabelle 1 des Artikels (eine Preisquelle für alle BTC-Bestände)
        ("Lightning", t["lightning"], b["lightning_btc"] * p, t["bz_kanaele"]),
        ("sBTC (Stacks)", t["sbtc"], b["sbtc_btc"] * p, t["bz_umlauf"]),
    ]
    # Panel 2: Chain-TVL programmierbarer Bitcoin-Umgebungen
    ct = b["chain_tvl_usd"]
    chains = [
        ("Stacks", t["c_stacks"], ct["Stacks"]),
        ("Rootstock", t["c_rootstock"], ct["Rootstock"]),
        ("BOB", t["c_bob"], ct["BOB"]),
        ("Citrea", t["c_citrea"], ct["Citrea"]),
    ]
    bestaende.sort(key=lambda w: w[2])
    chains.sort(key=lambda w: w[2])
    return bestaende, chains, date.fromisoformat(b["stichtag"]), p


def wert_text(usd: float, t=TEXTE["de"], en: bool = False) -> str:
    if usd >= 1e9:
        return f"{zahl(usd / 1e9, 1, en)} {t['mrd']}"
    return f"{zahl(usd / 1e6, 0, en)} {t['mio']}"


def zeichne(bestaende, chains, stichtag, btc_preis, sprache="de") -> None:
    t = TEXTE[sprache]
    en = sprache == "en"
    stil.aktiviere_stil()
    fig, (oben, unten) = plt.subplots(
        2, 1, figsize=(stil.BREITE_TEXT, 5.6),
        height_ratios=[len(bestaende), len(chains) + 0.6])

    # Panel 1: Bestände, logarithmisch (Spanne 45:1)
    oben.barh([w[0] for w in bestaende], [w[2] for w in bestaende],
              color=stil.BLAU, height=0.6)
    oben.set_xscale("log")
    for i, (_, vertrauen, usd, bezug) in enumerate(bestaende):
        oben.text(usd * 1.15, i, f"{wert_text(usd, t, en)} ({bezug})  ·  {vertrauen}",
                  va="center", ha="left", fontsize=LABELGROESSE,
                  color=TEXTFARBE)
    oben.set_xlim(right=max(w[2] for w in bestaende) * 40)
    oben.set_xlabel(t["xlabel_oben"])

    # Panel 2: Chain-TVL, linear
    unten.barh([w[0] for w in chains], [w[2] for w in chains],
               color=stil.BLAU, height=0.6)
    for i, (_, vertrauen, usd) in enumerate(chains):
        unten.text(usd + max(w[2] for w in chains) * 0.02, i,
                   f"{wert_text(usd, t, en)}  ·  {vertrauen}",
                   va="center", ha="left", fontsize=LABELGROESSE,
                   color=TEXTFARBE)
    unten.set_xlim(right=max(w[2] for w in chains) * 2.4)
    unten.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: zahl(x / 1e6, 0, en)))
    unten.set_xlabel(t["xlabel_unten"])

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
             t["fuss"].format(
                 preis=zahl(btc_preis, 0, en),
                 stichtag=stichtag.strftime("%-d %b %Y") if en
                 else stil.stichtag_text(stichtag)),
             fontsize=8.5, color=QUELLENFARBE, ha="left", va="top")

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"bitcoin_bruecken{t['suffix']}.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/bitcoin_bruecken{t['suffix']}.pdf|svg")


if __name__ == "__main__":
    sprache = "en" if "--en" in sys.argv else "de"
    zeichne(*lade_daten(TEXTE[sprache]), sprache)
