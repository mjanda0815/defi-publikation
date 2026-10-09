"""Abbildungen des Artikels „DeFi mit Bitcoin", Abschnitt 6 (Version 1.1):

1. miner_finanzierung — zwei Besicherungsarchitekturen eines
   BTC-besicherten Betriebsmittelkredits als getrennte Panels
   (A: On-chain-Variante auf Rootstock, B: institutionelle verwahrte
   Variante); Flüsse Sicherheit → Liquidität → Betriebskosten →
   Tilgung → Freigabe mit gerichteten Pfeilen, Risikohinweis je Panel.
   Schematisch — keine konkrete Produktarchitektur (etwa Rootstock Vaults).
2. ltv_szenario — Loan-to-Value in Abhängigkeit vom BTC-Preis für das
   hypothetische Rechenbeispiel des Artikels (10 BTC Sicherheit,
   500.000 USD Kreditschuld, Liquidationsgrenze 80 % LTV).

Beides Eigenanfertigungen ohne externe Daten (harte Regel 3); das
LTV-Beispiel ist bewusst parametrisch, keine Produktkondition.
Gestaltung (Publication Gate 10/2026): Beschriftungen >= 8 pt.

Aufruf:  python3 abbildungen/miner_finanzierung.py [--en]
Ausgabe: abbildungen/out/miner_finanzierung[_en].pdf|svg
         abbildungen/out/ltv_szenario[_en].pdf|svg
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))
import stil

HIER = Path(__file__).parent

# Rechenbeispiel (Abschnitt 6.3): konstante Schuld, konstante BTC-Menge
BTC_MENGE = 10.0
KREDIT_USD = 500_000.0
P_START = 100_000.0
LTV_GRENZE = 0.80

TEXTE = {
    "de": {
        "panel_a": "A — On-chain-Variante (DeFi auf Rootstock)",
        "panel_b": "B — Institutionelle Variante (verwahrt)",
        "miner": "Mining-Firma:\nBTC-Reserve;\nEinnahmen BTC,\nKosten USD/EUR",
        "a": ["Peg-in:\nBTC → RBTC\n(PowPeg,\n5-von-9-\nFöderation)",
              "RBTC als\nSicherheit im\nLending-Contract\n(überbesichert,\nautomatische\nLiquidation)",
              "Stablecoin-\nKredit →\nBetriebskosten\n(Strom, Hosting,\nHardware,\nPersonal)"],
        "b": ["BTC an\nVerwahrer oder\nCollateral-\nKonto\n(vertraglich\ngebunden)",
              "bilateraler\nKreditvertrag\n(Prime Broker;\nMargin Calls)",
              "US-Dollar-\nKredit →\nBetriebskosten\n(Strom, Hosting,\nHardware,\nPersonal)"],
        "ende": "Tilgung +\nZinsen →\nFreigabe der\nSicherheit",
        "risiko_a": "Risiken: erbt Brücken-, Smart-Contract- und Orakelrisiko sowie das Peg-Risiko des Stablecoins\n"
                    "(Abschnitt 8); Liquidation automatisch, ohne Ermessen.",
        "risiko_b": "Risiken: Verwahrer-, Gegenpartei- und Rehypothezierungsrisiko; Nachschuss und Verwertung\n"
                    "nach Vertrag und Ermessen des Kreditgebers.",
        "quelle_flow": "Zwei Besicherungsarchitekturen für denselben Finanzierungsfall — schematisch, keine konkrete\n"
                       "Produktarchitektur (auch nicht die von Rootstock Vaults). Eigene Darstellung.",
        "y_label": "Loan-to-Value (%)",
        "x_label": "BTC-Preis (Tsd. US-Dollar)",
        "kurve": "LTV bei konstanter Schuld\n(10 BTC, 500.000 USD Kredit)",
        "grenze": "angenommene Liquidationsgrenze: 80 %",
        "start_pkt": "Start: LTV 50 %\nbei 100.000 USD",
        "liq_pkt": "Grenze erreicht bei\n62.500 USD (−37,5 %)",
        "zone": "Nachschuss- bzw.\nLiquidationszone",
        "quelle_ltv": "Hypothetisches Rechenbeispiel, keine Produktkondition; konstante BTC-Menge und Kreditschuld,\n"
                      "ohne aufgelaufene Zinsen und Gebühren. Es gilt $P_{Liq} = P_0 \\cdot LTV_0\\,/\\,LTV_{Grenze}$.\n"
                      "Eigene Darstellung.",
        "suffix": "",
    },
    "en": {
        "panel_a": "A — On-chain variant (DeFi on Rootstock)",
        "panel_b": "B — Institutional variant (custodial)",
        "miner": "Mining company:\nBTC reserve;\nrevenue BTC,\ncosts USD/EUR",
        "a": ["Peg-in:\nBTC → RBTC\n(PowPeg,\n5-of-9\nfederation)",
              "RBTC as\ncollateral in\nlending contract\n(over-\ncollateralised,\nautomatic\nliquidation)",
              "Stablecoin\ncredit →\noperating costs\n(power, hosting,\nhardware,\npayroll)"],
        "b": ["BTC to\ncustodian or\ncollateral\naccount\n(contractually\nbound)",
              "bilateral credit\nagreement\n(prime broker;\nmargin calls)",
              "US-dollar\ncredit →\noperating costs\n(power, hosting,\nhardware,\npayroll)"],
        "ende": "Repayment +\ninterest →\ncollateral\nrelease",
        "risiko_a": "Risks: inherits bridge, smart-contract and oracle risk plus the stablecoin's peg risk (Section 8);\n"
                    "liquidation is automatic, without discretion.",
        "risiko_b": "Risks: custodian, counterparty and rehypothecation risk; margin calls and enforcement\n"
                    "per contract and at the lender's discretion.",
        "quelle_flow": "Two collateral architectures for the same financing case — schematic, not a specific\n"
                       "product architecture (nor that of Rootstock Vaults). Own illustration.",
        "y_label": "Loan-to-value (%)",
        "x_label": "BTC price (thousand US dollars)",
        "kurve": "LTV at constant debt\n(10 BTC, 500,000 USD loan)",
        "grenze": "assumed liquidation threshold: 80 %",
        "start_pkt": "Start: LTV 50 %\nat 100,000 USD",
        "liq_pkt": "Threshold reached at\n62,500 USD (−37.5 %)",
        "zone": "Margin-call /\nliquidation zone",
        "quelle_ltv": "Hypothetical worked example, not a product term; constant BTC amount and debt,\n"
                      "excluding accrued interest and fees. $P_{liq} = P_0 \\cdot LTV_0\\,/\\,LTV_{max}$.\n"
                      "Own illustration.",
        "suffix": "_en",
    },
}


def box(ax, x, y, w, h, text, fuellung="#f2f7fd", fontsize=8.8):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.05",
        facecolor=fuellung, edgecolor=stil.GRUNDLINIE, linewidth=0.9))
    ax.text(x + w / 2, y + h / 2, text, fontsize=fontsize,
            color=stil.TINTE_SEKUNDAER, ha="center", va="center",
            linespacing=1.25)


def pfeil(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=11,
        color=stil.TINTE_SEKUNDAER, linewidth=1.1, shrinkA=2, shrinkB=2))


def panel(ax, y, titel, schritte, miner, ende, risiko):
    """Eine Zeile aus fünf Boxen: Miner → drei Schritte → Tilgung/Freigabe."""
    w, h, luecke = 1.74, 2.55, 0.43
    ax.text(0.05, y + h + 0.45, titel, fontsize=11, color=stil.TINTE,
            fontweight="bold", va="center")
    texte = [miner] + list(schritte) + [ende]
    fuellungen = [stil.BLAU_HELL, "#f2f7fd", "#f2f7fd", "#f2f7fd", "#e2edfa"]
    x = 0.05
    for i, (text, f) in enumerate(zip(texte, fuellungen)):
        box(ax, x, y, w, h, text, fuellung=f)
        if i < len(texte) - 1:
            pfeil(ax, x + w + 0.02, y + h / 2, x + w + luecke - 0.02, y + h / 2)
        x += w + luecke
    ax.text(0.05, y - 0.22, risiko, fontsize=8.8, color=stil.TINTE_SEKUNDAER,
            va="top", style="italic", linespacing=1.25)


def zeichne_fluss(t) -> None:
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 5.4))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.15, 8.9)
    ax.axis("off")

    panel(ax, 5.55, t["panel_a"], t["a"], t["miner"], t["ende"], t["risiko_a"])
    panel(ax, 1.0, t["panel_b"], t["b"], t["miner"], t["ende"], t["risiko_b"])

    stil.quellenzeile(fig, t["quelle_flow"])

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"miner_finanzierung{t['suffix']}.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/miner_finanzierung{t['suffix']}.pdf|svg")


def zeichne_ltv(t) -> None:
    stil.aktiviere_stil()
    fig, ax = plt.subplots(figsize=(stil.BREITE_TEXT, 2.9))

    p_liq = P_START * (KREDIT_USD / (BTC_MENGE * P_START)) / LTV_GRENZE
    preise = [40_000 + i * 500 for i in range(0, 141)]
    ltv = [KREDIT_USD / (BTC_MENGE * p) * 100 for p in preise]

    ax.axvspan(40, p_liq / 1000, color=stil.RASTER, alpha=0.55, linewidth=0)
    ax.plot([p / 1000 for p in preise], ltv, color=stil.BLAU, linewidth=1.4)
    ax.axhline(LTV_GRENZE * 100, color=stil.GEDECKT, linewidth=1.0,
               linestyle=(0, (4, 3)))

    ax.plot([P_START / 1000], [50], "o", color=stil.BLAU, markersize=4.5)
    ax.plot([p_liq / 1000], [LTV_GRENZE * 100], "o", color=stil.TINTE,
            markersize=4.5)

    ax.annotate(t["start_pkt"], xy=(P_START / 1000, 50), xytext=(6, 10),
                textcoords="offset points", fontsize=8.3,
                color=stil.TINTE_SEKUNDAER)
    ax.annotate(t["liq_pkt"], xy=(p_liq / 1000, LTV_GRENZE * 100),
                xytext=(8, 6), textcoords="offset points", fontsize=8.3,
                color=stil.TINTE_SEKUNDAER)
    ax.text(41.5, 48, t["zone"], fontsize=8.3, color=stil.TINTE_SEKUNDAER,
            va="bottom")
    ax.text(108.5, LTV_GRENZE * 100 + 3, t["grenze"], fontsize=8.3,
            color=stil.TINTE_SEKUNDAER, ha="right")
    ax.text(108.5, 36, t["kurve"], fontsize=8.3, color=stil.BLAU, ha="right")

    ax.set_xlim(40, 110)
    ax.set_ylim(30, 130)
    ax.set_xlabel(t["x_label"])
    ax.set_ylabel(t["y_label"])
    stil.achsen_aufraeumen(ax)
    ax.margins(x=0)
    stil.quellenzeile(fig, t["quelle_ltv"])

    out = HIER / "out"
    out.mkdir(exist_ok=True)
    for endung in ("pdf", "svg"):
        fig.savefig(out / f"ltv_szenario{t['suffix']}.{endung}")
    plt.close(fig)
    print(f"Geschrieben: {out}/ltv_szenario{t['suffix']}.pdf|svg")


if __name__ == "__main__":
    t = TEXTE["en" if "--en" in sys.argv else "de"]
    zeichne_fluss(t)
    zeichne_ltv(t)
