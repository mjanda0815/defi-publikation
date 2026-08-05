"""Abbildung: Merkle-Baum mit durchgerechnetem Beispiel (Kapitel 2).

Eigenanfertigung, ersetzt Abb. 2.8 des Originals (Analytics Vidhya).
Die Hashwerte sind echte (gekürzte) SHA-256-Werte der gezeigten Beispiel-
Transaktionen und damit reproduzierbar; zur Vereinfachung wird einfaches
SHA-256 statt Bitcoins doppeltem SHA-256 verwendet (im Text vermerkt).
Hervorgehoben ist der SPV-Nachweispfad für T3: Zum Existenznachweis genügen
H(T4) und H12 sowie die Merkle-Root.

Aufruf:  python abbildungen/merkle.py
Ausgabe: abbildungen/out/merkle.pdf und .svg
"""

import hashlib
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent

TRANSAKTIONEN = [
    "T1: Alice zahlt Bob 5 BTC",
    "T2: Bob zahlt Carol 2 BTC",
    "T3: Carol zahlt Dave 1 BTC",
    "T4: Dave zahlt Alice 3 BTC",
]


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def kasten(ax, x, y, breite, hoehe, titel, hashwert, hervorheben=False, rand=None):
    box = FancyBboxPatch(
        (x - breite / 2, y - hoehe / 2), breite, hoehe,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        facecolor=stil.BLAU_HELL if hervorheben else "white",
        edgecolor=rand or (stil.BLAU if hervorheben else stil.GRUNDLINIE),
        linewidth=1.6 if rand else (1.0 if hervorheben else 0.9),
    )
    ax.add_patch(box)
    ax.text(x, y + 0.16, titel, ha="center", va="center",
            fontsize=8.5, color=stil.TINTE)
    ax.text(x, y - 0.17, hashwert + "…", ha="center", va="center",
            fontsize=8, color=stil.TINTE_SEKUNDAER, family="monospace")


def zeichne() -> None:
    stil.aktiviere_stil()
    h = [sha(t) for t in TRANSAKTIONEN]
    h12 = sha(h[0] + h[1])
    h34 = sha(h[2] + h[3])
    root = sha(h12 + h34)

    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 3.6))
    ax.set_xlim(0, 8)
    ax.set_ylim(-1.15, 3.9)
    ax.axis("off")

    bx, bh = 1.85, 0.78
    xs = [1.1, 3.05, 5.0, 6.95]
    # Blätter: Transaktions-Hashes; T3 = nachzuweisende Transaktion (blauer Rand),
    # H(T4) gehört zum Nachweispfad (hervorgehoben)
    for i, x in enumerate(xs):
        kasten(ax, x, 0.55, bx, bh, f"H{i+1} = H(T{i+1})", h[i][:8],
               hervorheben=(i == 3), rand=stil.BLAU if i == 2 else None)
        ax.text(x, -0.35, TRANSAKTIONEN[i].split(": ")[1], ha="center",
                fontsize=7.5, color=stil.GEDECKT)
        ax.text(x, -0.72, f"(T{i+1})", ha="center",
                fontsize=7.5, color=stil.GEDECKT)

    kasten(ax, 2.075, 1.95, bx + 0.35, bh, "H12 = H(H1||H2)", h12[:8],
           hervorheben=True)
    kasten(ax, 5.975, 1.95, bx + 0.35, bh, "H34 = H(H3||H4)", h34[:8])
    kasten(ax, 4.025, 3.35, bx + 1.1, bh, "Merkle-Root = H(H12||H34)", root[:8])

    # Kanten Kind -> Eltern
    for (x0, y0), (x1, y1) in [
        ((1.1, 0.94), (1.9, 1.56)), ((3.05, 0.94), (2.25, 1.56)),
        ((5.0, 0.94), (5.8, 1.56)), ((6.95, 0.94), (6.15, 1.56)),
        ((2.075, 2.34), (3.7, 2.96)), ((5.975, 2.34), (4.35, 2.96)),
    ]:
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=stil.GEDECKT,
                                    linewidth=0.9, shrinkA=0, shrinkB=0))

    ax.text(0.08, 3.82,
            "Nachweis für T3 (SPV):\nes genügen H4 und H12\n(hervorgehoben) sowie\ndie Merkle-Root",
            fontsize=8, color=stil.TINTE_SEKUNDAER, va="top")


    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"merkle.{endung}")
    print(f"Geschrieben: {out}/merkle.pdf|svg — Root {root[:8]}…")


if __name__ == "__main__":
    zeichne()
