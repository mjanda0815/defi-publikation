"""Abbildung: Preisbildung eines Constant Function Market Makers (Kapitel 3.5.3).

Eigenanfertigung in Anlehnung an Schär (2021), ersetzt Abb. 3.2 des Originals.
Durchgezogene Kurve: x*y = k. Ein Tausch bewegt die Reserven entlang der Kurve
(Pfeil von A nach B). Gestrichelte Kurve: Handelsgebühren vergrößern k mit der
Zeit und verschieben die Kurve nach außen.

Aufruf:  python abbildungen/cfmm.py
Ausgabe: abbildungen/out/cfmm.pdf und .svg
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent


def zeichne() -> None:
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 3.2))

    k1, k2 = 100.0, 140.0
    xs = [x / 10 for x in range(28, 320)]
    ax.plot(xs, [k1 / x for x in xs], color=stil.BLAU, linewidth=1.6,
            label="$x \\cdot y = k$")
    ax.plot(xs, [k2 / x for x in xs], color=stil.BLAU, linewidth=1.3,
            linestyle=(0, (4, 3)),
            label="$x \\cdot y = k' > k$ (nach Gebühren)")

    # Beispiel-Tausch: A -> B entlang der Kurve k1
    ax_a, ax_b = 5.0, 12.5
    a = (ax_a, k1 / ax_a)
    b = (ax_b, k1 / ax_b)
    ax.annotate(
        "", xy=b, xytext=a,
        arrowprops=dict(arrowstyle="-|>", color=stil.TINTE_SEKUNDAER,
                        linewidth=1.1, shrinkA=4, shrinkB=4,
                        connectionstyle="arc3,rad=-0.25"),
    )
    for punkt, name, dx, dy in [(a, "A", -0.4, 0.8), (b, "B", 0.5, 0.6)]:
        ax.scatter([punkt[0]], [punkt[1]], s=16, color=stil.BLAU, zorder=3)
        ax.annotate(name, xy=punkt, xytext=(punkt[0] + dx, punkt[1] + dy),
                    fontsize=9, color=stil.TINTE)
    ax.annotate(
        "Tausch: Pool erhält $\\Delta x$,\ngibt $\\Delta y$ ab",
        xy=(13.2, 15.6), fontsize=8, color=stil.TINTE_SEKUNDAER,
    )

    ax.set_xlim(0, 32)
    ax.set_ylim(0, 26)
    ax.set_xlabel("Bestand Token $x$ im Pool")
    ax.set_ylabel("Bestand Token $y$ im Pool")
    stil.achsen_aufraeumen(ax)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")


    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"cfmm.{endung}")
    print(f"Geschrieben: {out}/cfmm.pdf|svg")


if __name__ == "__main__":
    zeichne()
