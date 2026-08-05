"""Abbildung: Der DeFi-Stack (mehrschichtige Architektur), Kapitel 3.4.

Eigenanfertigung in Anlehnung an Schär (2021), ersetzt die Fremdgrafik
Abb. 3.1 des Originals (Bildrechte). Fünf Schichten mit Beispielen;
die Sicherheitsabhängigkeit (jede Schicht nur so sicher wie die darunter)
wird durch den seitlichen Pfeil visualisiert.

Aufruf:  python abbildungen/defi_stack.py
Ausgabe: abbildungen/out/defi_stack.pdf und .svg
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent

SCHICHTEN = [
    ("5 — Aggregationsschicht", "Plattformen über mehreren Anwendungen (z. B. DEX-Aggregatoren, Dashboards)"),
    ("4 — Anwendungsschicht", "Nutzeroberflächen der Protokolle (Web-Frontends, Wallet-Integrationen)"),
    ("3 — Protokollschicht", "Smart-Contract-Standards je Anwendungsfall (Handel, Kredit, Derivate, Verwaltung)"),
    ("2 — Vermögensschicht", "Native Token und Token-Standards (z. B. ETH, ERC-20, ERC-721)"),
    ("1 — Abwicklungsschicht", "Blockchain und Protokoll-Asset (z. B. Ethereum): Konsens, Eigentum, Endgültigkeit"),
]


def zeichne() -> None:
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.25, 5.35)
    ax.axis("off")

    hoehe, luecke = 0.88, 0.14
    # Abwicklungsschicht unten kräftig (tragende Schicht), nach oben heller
    fuellungen = ["#ffffff", "#f2f7fd", "#e2edfa", "#c7ddf6", stil.BLAU_HELL]
    for i, (titel, beispiele) in enumerate(SCHICHTEN):
        y = (len(SCHICHTEN) - 1 - i) * (hoehe + luecke)
        box = FancyBboxPatch(
            (0.55, y), 8.0, hoehe,
            boxstyle="round,pad=0.03,rounding_size=0.05",
            facecolor=fuellungen[i], edgecolor=stil.GRUNDLINIE, linewidth=0.9,
        )
        ax.add_patch(box)
        ax.text(0.85, y + hoehe / 2 + 0.17, titel, fontsize=9.5,
                color=stil.TINTE, va="center", fontweight="bold")
        ax.text(0.85, y + hoehe / 2 - 0.2, beispiele, fontsize=7.5,
                color=stil.TINTE_SEKUNDAER, va="center")

    # Sicherheitsabhängigkeit: Pfeil von unten nach oben
    pfeil = FancyArrowPatch(
        (9.0, 0.30), (9.0, 4.55),
        arrowstyle="-|>", mutation_scale=12,
        color=stil.GEDECKT, linewidth=1.1,
    )
    ax.add_patch(pfeil)
    ax.text(9.25, 2.45,
            "Sicherheit hängt von den\ndarunterliegenden Schichten ab",
            fontsize=7.5, color=stil.GEDECKT, va="center", rotation=90)


    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"defi_stack.{endung}")
    print(f"Geschrieben: {out}/defi_stack.pdf|svg")


if __name__ == "__main__":
    zeichne()
