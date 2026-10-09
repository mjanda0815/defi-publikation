"""Abbildung des Artikels „DeFi mit Bitcoin": Architekturübersicht des
Bitcoin-DeFi-Stacks am Beispiel Rootstock (Version 1.1, Abschnitt 4.1).

Schichtenmodell analog zu defi_stack.py (Whitepaper, nach Schär 2021),
erweitert um die je Schicht hinzukommende Vertrauensannahme — die zentrale
Analysefigur des Artikels: Jede Schicht erbt die Annahmen aller darunter.
Die oberste Schicht ist eine illustrative On-chain-Umsetzung des
Mining-Kreditfalls, ausdrücklich nicht die verwahrten MARA-Fazilitäten.

Gestaltung (Publication Gate 10/2026): Beschriftungen >= 8,5 pt bei
Einbindung auf Satzspiegelbreite, keine grau-auf-grau-Außenkommentare.

Aufruf:  python3 abbildungen/bitcoin_defi_stack.py [--en]
Ausgabe: abbildungen/out/bitcoin_defi_stack[_en].pdf|svg
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent

TEXTE = {
    "de": {
        "schichten": [
            ("5 — Anwendungsfall",
             "Illustrative On-chain-Umsetzung eines Mining-Kreditfalls\n"
             "(nicht die verwahrten MARA-Fazilitäten, Abschnitt 6)",
             "+ Markt-, Liquidations- und\nGegenparteirisiko"),
            ("4 — Protokollschicht",
             "Money on Chain, Sovryn, RIF on Chain, Uniswap v3 …\n"
             "(CDP, AMM, Kreditmärkte)",
             "+ Smart-Contract- und\nOrakel-Risiko"),
            ("3 — Ausführungsschicht",
             "Rootstock-Sidechain: EVM-kompatibel, 30-s-Blöcke,\n"
             "Gas ausschließlich in RBTC",
             "+ Merge-Mining-Anteil an der\nBitcoin-Hashrate (84 %, Q2 2026;\nRootstockLabs-Bericht)"),
            ("2 — Brückenschicht",
             "PowPeg: Peg-in 100 BTC-Bestätigungen,\n"
             "Peg-out 4.000 RSK-Blöcke (ca. 33 h)",
             "+ 5-von-9-Föderation + PowHSM\n(nicht vom Bitcoin-Protokoll\nerzwungen)"),
            ("1 — Basisschicht",
             "Bitcoin: PoW-Konsens, UTXO-Modell,\n"
             "zustandsloses Script — kein gemeinsamer Zustand",
             "+ ehrliche Hashrate-Mehrheit"),
        ],
        "pfeil": "Jede Schicht erbt die Vertrauensannahmen\naller darunterliegenden Schichten",
        "spalte": "hinzukommende Vertrauensannahme",
        "quelle": "Architektur des Bitcoin-DeFi-Stacks am Beispiel Rootstock. Eigene Darstellung\n"
                  "(Schichtenmodell in Anlehnung an Schär 2021); Merge-Mining-Quote: RootstockLabs, Q2 2026.",
        "suffix": "",
    },
    "en": {
        "schichten": [
            ("5 — Use case",
             "Illustrative on-chain implementation of a mining-credit case\n"
             "(not the custodial MARA facilities, Section 6)",
             "+ market, liquidation and\ncounterparty risk"),
            ("4 — Protocol layer",
             "Money on Chain, Sovryn, RIF on Chain, Uniswap v3 …\n"
             "(CDPs, AMMs, credit markets)",
             "+ smart-contract and\noracle risk"),
            ("3 — Execution layer",
             "Rootstock sidechain: EVM-compatible, 30-second blocks,\n"
             "gas paid exclusively in RBTC",
             "+ merged-mining share of Bitcoin\nhashrate (84 %, Q2 2026;\nRootstockLabs report)"),
            ("2 — Bridge layer",
             "PowPeg: peg-in 100 BTC confirmations,\n"
             "peg-out 4,000 RSK blocks (approx. 33 h)",
             "+ 5-of-9 federation + PowHSM\n(not enforced by the\nBitcoin protocol)"),
            ("1 — Base layer",
             "Bitcoin: PoW consensus, UTXO model,\n"
             "stateless Script — no shared state",
             "+ honest majority of hashrate"),
        ],
        "pfeil": "Each layer inherits the trust assumptions\nof all layers below it",
        "spalte": "additional trust assumption",
        "quelle": "Architecture of the Bitcoin DeFi stack, using Rootstock as the example. Own illustration\n"
                  "(layer model following Schär 2021); merged-mining share: RootstockLabs, Q2 2026.",
        "suffix": "_en",
    },
}


def zeichne(sprache: str) -> None:
    t = TEXTE[sprache]
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 4.3))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, 10.9)
    ax.set_ylim(-0.2, 6.35)
    ax.axis("off")

    hoehe, luecke = 1.04, 0.14
    x0, breite = 0.7, 6.15
    # Basisschicht unten kräftig (tragende Schicht), nach oben heller
    fuellungen = ["#ffffff", "#f2f7fd", "#e2edfa", "#c7ddf6", stil.BLAU_HELL]
    for i, (titel, beispiele, annahme) in enumerate(t["schichten"]):
        y = (len(t["schichten"]) - 1 - i) * (hoehe + luecke)
        ax.add_patch(FancyBboxPatch(
            (x0, y), breite, hoehe,
            boxstyle="round,pad=0.03,rounding_size=0.05",
            facecolor=fuellungen[i], edgecolor=stil.GRUNDLINIE, linewidth=0.9))
        ax.text(x0 + 0.25, y + hoehe - 0.22, titel, fontsize=10,
                color=stil.TINTE, va="center", fontweight="bold")
        ax.text(x0 + 0.25, y + 0.36, beispiele, fontsize=8.5,
                color=stil.TINTE_SEKUNDAER, va="center", linespacing=1.25)
        ax.text(x0 + breite + 0.2, y + hoehe / 2, annahme, fontsize=8.5,
                color=stil.TINTE_SEKUNDAER, va="center", style="italic",
                linespacing=1.2)

    ax.text(x0 + breite + 0.2, 6.1, t["spalte"], fontsize=8.5,
            color=stil.TINTE, va="center", fontweight="bold")

    ax.add_patch(FancyArrowPatch(
        (0.33, 0.35), (0.33, 5.5), arrowstyle="-|>", mutation_scale=13,
        color=stil.TINTE_SEKUNDAER, linewidth=1.2))
    ax.text(0.1, 2.95, t["pfeil"], fontsize=8, color=stil.TINTE_SEKUNDAER,
            va="center", ha="center", rotation=90, linespacing=1.2)

    stil.quellenzeile(fig, t["quelle"])

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"bitcoin_defi_stack{t['suffix']}.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/bitcoin_defi_stack{t['suffix']}.pdf|svg")


if __name__ == "__main__":
    zeichne("en" if "--en" in sys.argv else "de")
