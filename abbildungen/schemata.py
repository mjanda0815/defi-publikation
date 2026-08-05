"""Konzeptionelle Schaubilder (Eigenanfertigungen) für die Kapitel 1, 2, 3 und 5.

Ersetzt die verbliebenen Fremdgrafiken des Originals durch eigene Darstellungen
(harte Regel 3, CLAUDE.md). Erzeugt acht Schaubilder:
  cefi_defi            (Kap. 1)   — CeFi vs. DeFi
  byzantiner           (Kap. 2.3) — byzantinisches Generalsproblem
  pow_schema           (Kap. 2.4) — Proof-of-Work-Schleife
  blockchain_kette     (Kap. 2.5) — Verkettung der Blöcke
  kreditkarte          (Kap. 2.6) — Kreditkartenzahlung (in Anlehnung an ibi research)
  smart_contract       (Kap. 2.7) — Smart-Contract-Ablauf E-Commerce
  dex_akteure          (Kap. 3.5) — Akteure einer DEX (in Anlehnung an Auer et al.)
  ntt_framework        (Kap. 5.2) — Integrator-Framework Bank/Krypto (n. NTT DATA)

Aufruf:  python abbildungen/schemata.py
Ausgabe: abbildungen/out/<name>.pdf|svg
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent
ROT = "#e34948"


def kasten(ax, x, y, b, h, text, fuellung="white", rand=None, fs=8.5, fett=False):
    ax.add_patch(FancyBboxPatch((x - b / 2, y - h / 2), b, h,
                 boxstyle="round,pad=0.04,rounding_size=0.06",
                 facecolor=fuellung, edgecolor=rand or stil.GRUNDLINIE, linewidth=1.0))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=stil.TINTE, fontweight="bold" if fett else "normal")


def pfeil(ax, von, nach, farbe=None, stilart="-|>", krumm=0.0, lw=1.1, ls="-"):
    ax.add_patch(FancyArrowPatch(von, nach, arrowstyle=stilart, mutation_scale=11,
                 color=farbe or stil.GEDECKT, linewidth=lw, linestyle=ls,
                 connectionstyle=f"arc3,rad={krumm}", shrinkA=2, shrinkB=2))


def beschriftung(ax, x, y, text, fs=7.5, farbe=None, ha="center"):
    ax.text(x, y, text, fontsize=fs, color=farbe or stil.TINTE_SEKUNDAER,
            ha=ha, va="center")


def neu(hoehe=3.0, xlim=10, ylim=5):
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, hoehe))
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    ax.axis("off")
    return fig, ax


def speichere(fig, name, quelle=None):
    # quelle wird bewusst nicht mehr ins Bild gesetzt: Der Herkunfts-/
    # Anlehnungsvermerk steht vollständig in der Bildunterschrift (LaTeX);
    # die Doppelung „Eigene Darstellung" im Bild UND in der Caption entfiel
    # im Abschluss-Review (02.08.2026).
    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"{name}.{endung}")
    plt.close(fig)
    print(f"Geschrieben: out/{name}.pdf|svg")


def cefi_defi():
    fig, ax = neu(3.0)
    ax.text(2.5, 4.7, "Traditionell (CeFi)", ha="center", fontsize=10,
            fontweight="bold", color=stil.TINTE)
    ax.text(7.5, 4.7, "DeFi", ha="center", fontsize=10,
            fontweight="bold", color=stil.TINTE)
    ax.plot([5, 5], [0.4, 4.9], color=stil.RASTER, linewidth=0.8)
    # links: Intermediär
    kasten(ax, 0.85, 2.4, 1.15, 0.75, "Kunde A", fs=8)
    kasten(ax, 2.5, 2.4, 1.55, 1.0, "Bank /\nIntermediär", fuellung=stil.BLAU_HELL, fett=True, fs=8)
    kasten(ax, 4.15, 2.4, 1.15, 0.75, "Kunde B", fs=8)
    pfeil(ax, (1.45, 2.4), (1.7, 2.4), stilart="<|-|>")
    pfeil(ax, (3.3, 2.4), (3.55, 2.4), stilart="<|-|>")
    beschriftung(ax, 2.5, 1.35, "Vertrauen, Prüfung und Abwicklung\nliegen beim Intermediär\n(Konto, Identität, Gebühren)")
    # rechts: Smart Contract
    kasten(ax, 5.85, 2.4, 1.15, 0.75, "Kunde A", fs=8)
    kasten(ax, 7.5, 2.4, 1.55, 1.0, "Smart\nContract", fuellung=stil.BLAU_HELL, fett=True, fs=8)
    kasten(ax, 9.15, 2.4, 1.15, 0.75, "Kunde B", fs=8)
    pfeil(ax, (6.45, 2.4), (6.7, 2.4), stilart="<|-|>")
    pfeil(ax, (8.3, 2.4), (8.55, 2.4), stilart="<|-|>")
    beschriftung(ax, 7.5, 1.35, "Regeln sind im Code festgelegt,\nAusführung automatisch auf der\nBlockchain (Wallet statt Konto)")
    speichere(fig, "cefi_defi")


def byzantiner():
    fig, ax = neu(3.0)
    kasten(ax, 5.0, 2.5, 1.9, 0.9, "gemeinsames\nAngriffsziel", fuellung="#f2f7fd", fett=True)
    # General 5 bei y=4.5 statt 4.6: mit Kastenhöhe 0.75 + Rundungs-Padding lag
    # die Oberkante sonst knapp über ylim=5 und wurde abgeschnitten.
    pos = [(1.2, 4.2), (1.2, 0.8), (8.8, 4.2), (8.8, 0.8), (5.0, 4.5)]
    for i, (x, y) in enumerate(pos, 1):
        abtruennig = (i == 3)
        kasten(ax, x, y, 1.7, 0.75, f"General {i}",
               rand=ROT if abtruennig else None)
        if abtruennig:
            pfeil(ax, (x - 0.4, y - 0.4), (6.6, 0.6), farbe=ROT, lw=1.4)
            beschriftung(ax, 9.15, 3.3, "abtrünnig:\nzieht nicht mit", farbe=ROT)
        else:
            zielx = 5.0 + (0.55 if x > 5 else -0.55 if x < 5 else 0)
            ziely = 2.95 if y > 2.5 else 2.05
            pfeil(ax, (x + (0.5 if x < 5 else -0.5 if x > 5 else 0), y - (0.38 if y > 2.5 else -0.38)),
                  (zielx, ziely))
    beschriftung(ax, 2.6, 2.5, "Abstimmung nur über\nunsichere Kanäle", ha="center")
    speichere(fig, "byzantiner")


def pow_schema():
    fig, ax = neu(2.9)
    kasten(ax, 1.5, 3.4, 2.4, 1.1, "Blockheader\n+ Nonce")
    kasten(ax, 5.0, 3.4, 1.9, 0.9, "SHA-256", fuellung=stil.BLAU_HELL, fett=True)
    kasten(ax, 8.4, 3.4, 2.5, 1.1, "Hash <\nZielschwelle?")
    kasten(ax, 8.4, 1.2, 2.7, 1.0, "Block gültig →\nan Netzwerk senden", fuellung="#e2edfa")
    kasten(ax, 3.2, 1.2, 2.6, 0.9, "Nonce ändern")
    pfeil(ax, (2.7, 3.4), (4.05, 3.4))
    pfeil(ax, (5.95, 3.4), (7.15, 3.4))
    pfeil(ax, (8.4, 2.85), (8.4, 1.7)); beschriftung(ax, 8.75, 2.3, "ja")
    pfeil(ax, (7.15, 3.1), (4.5, 1.5), krumm=0.25); beschriftung(ax, 5.7, 1.9, "nein")
    pfeil(ax, (1.95, 1.2), (1.5, 2.85), krumm=0.3)
    beschriftung(ax, 5.0, 4.5, "Jeder Versuch erfordert eine Hash-Berechnung — Sicherheit durch nachweisbaren Rechenaufwand", fs=8)
    speichere(fig, "pow_schema")


def blockchain_kette():
    fig, ax = neu(3.0)
    for i, x in enumerate([1.8, 5.0, 8.2]):
        kasten(ax, x, 2.6, 2.7, 3.3, "", fuellung="#fbfcfe")
        ax.text(x, 4.0, f"Block {i+1}", ha="center", fontsize=9,
                fontweight="bold", color=stil.TINTE)
        kasten(ax, x, 3.35, 2.3, 0.6, "Hash des\nVorgängerblocks", fs=7.2,
               fuellung=stil.BLAU_HELL if i > 0 else "white")
        kasten(ax, x, 2.6, 2.3, 0.55, "Nonce, Zeitstempel", fs=7.2)
        kasten(ax, x, 1.95, 2.3, 0.55, "Merkle-Root", fs=7.2)
        kasten(ax, x, 1.25, 2.3, 0.6, "Transaktionen", fs=7.2)
    pfeil(ax, (3.85, 3.35), (3.15, 3.35), lw=1.4, farbe=stil.BLAU)
    pfeil(ax, (7.05, 3.35), (6.35, 3.35), lw=1.4, farbe=stil.BLAU)
    beschriftung(ax, 5.0, 4.75, "Jeder Block verweist auf den Hash seines Vorgängers — nachträgliche Änderungen machen alle Folgeblöcke ungültig", fs=8)
    speichere(fig, "blockchain_kette")


def kreditkarte():
    fig, ax = neu(3.0)
    kasten(ax, 1.3, 3.6, 1.9, 0.85, "Kunde\n(Karte)")
    kasten(ax, 5.0, 3.6, 1.9, 0.85, "Händler")
    kasten(ax, 8.7, 3.6, 1.9, 0.85, "Acquirer", fuellung=stil.BLAU_HELL, fett=True)
    kasten(ax, 8.7, 1.3, 2.4, 0.85, "Kreditkartenkonto\ndes Kunden")
    pfeil(ax, (2.25, 3.6), (4.05, 3.6)); beschriftung(ax, 3.15, 3.95, "1. Kartendaten")
    pfeil(ax, (5.95, 3.6), (7.75, 3.6)); beschriftung(ax, 6.85, 3.95, "2. Autorisierung")
    pfeil(ax, (8.7, 3.17), (8.7, 1.75)); beschriftung(ax, 9.6, 2.5, "3. Belastung", ha="center")
    pfeil(ax, (7.75, 3.35), (5.95, 3.35), krumm=0.0, ls=(0, (3, 2)))
    beschriftung(ax, 6.85, 2.95, "4. Gutschrift abzüglich Disagio")
    beschriftung(ax, 3.4, 1.7, "Vertrauen und Abwicklung laufen über Intermediäre;\ndas Entgelt (Disagio) trägt der Händler", ha="center")
    speichere(fig, "kreditkarte",
              "Eigene Darstellung in Anlehnung an ibi research (2009), stark vereinfacht")


def smart_contract():
    fig, ax = neu(3.1)
    kasten(ax, 1.4, 3.9, 1.9, 0.85, "Käufer")
    kasten(ax, 5.0, 3.9, 2.5, 1.0, "Smart Contract\n(Treuhand)", fuellung=stil.BLAU_HELL, fett=True)
    kasten(ax, 8.6, 3.9, 1.9, 0.85, "Verkäufer")
    kasten(ax, 5.0, 1.3, 2.5, 0.85, "Logistik-\ndienstleister")
    pfeil(ax, (2.35, 3.9), (3.75, 3.9)); beschriftung(ax, 3.05, 4.25, "1. Kaufpreis\nhinterlegen")
    pfeil(ax, (7.65, 4.1), (6.25, 4.1)); beschriftung(ax, 6.95, 4.45, "2. Ware\nversenden")
    pfeil(ax, (5.0, 1.73), (5.0, 3.4)); beschriftung(ax, 6.35, 2.6, "3. Lieferbestätigung\n(Auslöser)", ha="center")
    pfeil(ax, (6.25, 3.7), (7.65, 3.7), ls=(0, (3, 2)))
    beschriftung(ax, 6.7, 3.2, "4. automatische\nZahlung")
    beschriftung(ax, 1.9, 2.2, "Kein Vorleistungsrisiko,\nkein zusätzlicher\nZahlungsdienstleister", ha="center")
    speichere(fig, "smart_contract")


def dex_akteure():
    fig, ax = neu(3.3)
    kasten(ax, 5.0, 2.6, 3.0, 1.2, "Liquiditätspool\n$x \\cdot y = k$", fuellung=stil.BLAU_HELL, fett=True, fs=9.5)
    kasten(ax, 1.4, 4.3, 2.2, 0.8, "Trader")
    kasten(ax, 8.6, 4.3, 2.4, 0.8, "Liquiditäts-\nanbieter", fs=8)
    kasten(ax, 1.4, 0.9, 2.2, 0.8, "Arbitrageure")
    kasten(ax, 8.6, 0.9, 2.4, 0.8, "Governance-\nNutzer", fs=8)
    pfeil(ax, (2.5, 4.0), (3.7, 3.2)); beschriftung(ax, 2.1, 3.55, "Token tauschen\n(Swap)", ha="center")
    pfeil(ax, (7.5, 4.0), (6.3, 3.2)); pfeil(ax, (6.3, 3.35), (7.5, 4.15), krumm=0.25)
    beschriftung(ax, 8.35, 3.55, "Liquidität einzahlen /\nentnehmen; Gebührenanteil", ha="center")
    pfeil(ax, (2.5, 1.2), (3.7, 2.0)); beschriftung(ax, 2.15, 1.75, "Preisabweichungen\nausgleichen", ha="center")
    pfeil(ax, (7.5, 1.2), (6.3, 2.0)); beschriftung(ax, 8.2, 1.6, "Parameter/Gebühren\nfestlegen (Token-Stimmen)", ha="center")
    speichere(fig, "dex_akteure",
              "Eigene Darstellung in Anlehnung an Auer/Choi/Kundu (2022), BIS Working Paper 1066")


def ntt_framework():
    fig, ax = neu(3.0, xlim=10.3)
    kasten(ax, 1.3, 2.5, 1.9, 0.85, "Kunde")
    kasten(ax, 4.0, 2.5, 2.3, 1.05, "Bank\n(Depotverwaltung)")
    kasten(ax, 6.9, 2.5, 2.3, 1.05, "Integrator-\nFramework", fuellung=stil.BLAU_HELL, fett=True)
    kasten(ax, 9.3, 4.1, 1.6, 0.75, "Krypto-\nbörsen", fs=7.5)
    kasten(ax, 9.3, 2.5, 1.6, 0.75, "Verwahrung", fs=7.5)
    kasten(ax, 9.3, 0.9, 1.6, 0.75, "DeFi-\nAnbieter", fs=7.5)
    pfeil(ax, (2.25, 2.5), (2.85, 2.5))
    pfeil(ax, (5.15, 2.5), (5.75, 2.5))
    pfeil(ax, (8.05, 2.85), (8.5, 3.9))
    pfeil(ax, (8.05, 2.5), (8.5, 2.5))
    pfeil(ax, (8.05, 2.15), (8.5, 1.1))
    beschriftung(ax, 4.0, 1.35, "gewohnte Bankschnittstelle,\nkeine technischen Details", ha="center")
    beschriftung(ax, 6.9, 1.35, "White-Label:\nAnbindung als Dienstleistung", ha="center")
    speichere(fig, "ntt_framework",
              "Eigene Darstellung in Anlehnung an NTT DATA (2021), stark vereinfacht")


if __name__ == "__main__":
    cefi_defi()
    byzantiner()
    pow_schema()
    blockchain_kette()
    kreditkarte()
    smart_contract()
    dex_akteure()
    ntt_framework()
