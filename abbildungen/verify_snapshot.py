"""Verifikation der im Artikel „DeFi mit Bitcoin" (v1.1) genannten Zahlen
gegen die eingecheckten Snapshots und die Rechenbeispiele.

Prüft (PASS/FAIL je Zeile, Exit-Code 1 bei mindestens einem FAIL):
- Tabelle 1: USD-Umrechnungen (L-BTC, sBTC, Lightning) mit dem Snapshot-Kurs
- Abschnitt 4.3: Rootstock-Anteil am Sektor (Promille), BTC-Marktwert,
  Kursanstieg ggü. Erstfassung (64.430,87 USD), Chain-Summen-Anstieg
- Abschnitt 4.2: native Vier, Protokollsumme vs. Chain-TVL, Einträge
- Abschnitt 4.1: Transfergebühr aus Gaspreis-Snapshot
- Abschnitt 6: MARA-Arithmetik (450+300=750, 600+150=750, LTV),
  LTV-Rechenbeispiel (10 BTC, 100.000 USD, 500.000 USD, 80 %)

Aufruf:  python3 abbildungen/verify_snapshot.py   (bzw. make verify-data)
Die Sollwerte sind die im Artikeltext genannten, gerundeten Zahlen.
"""

import json
import sys
from pathlib import Path

DATEN = Path(__file__).parent / "daten"
PREIS_V10 = 64430.87276167584   # Snapshot-Kurs der Erstfassung (05.08.2026)
SUMME_V10 = 74767034641.60213   # Chain-Summe der Erstfassung (05.08.2026)

ergebnisse = []


def pruefe(name, ist, soll, toleranz=0.0):
    ok = abs(ist - soll) <= toleranz
    ergebnisse.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}: ist {ist:,.4f}, soll {soll:,.4f} (±{toleranz})")


b = json.loads((DATEN / "bitcoin_bruecken.json").read_text())
tvl = json.loads((DATEN / "rootstock_tvl.json").read_text())
prot = json.loads((DATEN / "rootstock_protokolle.json").read_text())
p = b["btc_preis_usd"]

print(f"Snapshot-Stichtag {b['stichtag']}, BTC-Kurs {p:,.2f} USD\n")

# --- Tabelle 1 (Mio. USD, gerundet wie im Text) ---
pruefe("Tab. 1 wBTC (Mrd. USD)", b["wbtc_usd"] / 1e9, 9.63, 0.005)
pruefe("Tab. 1 Babylon (Mrd. USD)", b["babylon_usd"] / 1e9, 3.34, 0.005)
pruefe("Tab. 1 tBTC (Mio. USD)", b["tbtc_usd"] / 1e6, 351, 0.5)
pruefe("Tab. 1 L-BTC (BTC)", b["lbtc_btc"], 4235, 0.5)
pruefe("Tab. 1 L-BTC × Kurs (Mio. USD)", b["lbtc_btc"] * p / 1e6, 346, 0.5)
pruefe("Tab. 1 Lightning (BTC)", b["lightning_btc"], 3795, 0.5)
pruefe("Tab. 1 Lightning × Kurs (Mio. USD)", b["lightning_btc"] * p / 1e6, 310, 0.5)
pruefe("Tab. 1 sBTC (BTC)", b["sbtc_btc"], 2488, 0.5)
pruefe("Tab. 1 sBTC × Kurs (Mio. USD)", b["sbtc_btc"] * p / 1e6, 203, 0.5)
pruefe("Tab. 1 Rootstock Chain-TVL (Mio. USD)", b["chain_tvl_usd"]["Rootstock"] / 1e6, 82, 0.5)
pruefe("Tab. 1 Citrea Chain-TVL (Mio. USD)", b["chain_tvl_usd"]["Citrea"] / 1e6, 9, 0.5)

# --- Abschnitt 4.3 ---
pruefe("4.3 Rootstock-TVL letzter Punkt (Mio. USD)", tvl[-1]["tvl"] / 1e6, 82, 0.5)
ath = max(tvl, key=lambda x: x["tvl"])
pruefe("4.3 Rootstock-ATH (Mio. USD)", ath["tvl"] / 1e6, 283, 0.5)
pruefe("4.3 Ethereum Chain-TVL (Mrd. USD)", b["chain_tvl_usd"]["Ethereum"] / 1e9, 51.5, 0.05)
pruefe("4.3 Chain-Summe (Mrd. USD)", b["chain_tvl_summe_usd"] / 1e9, 92.1, 0.05)
pruefe("4.3 Rootstock-Anteil (Promille)", b["chain_tvl_usd"]["Rootstock"] / b["chain_tvl_summe_usd"] * 1000, 0.89, 0.005)
pruefe("4.3 Chain-Summe Anstieg ggü. 05.08. (%)", (b["chain_tvl_summe_usd"] / SUMME_V10 - 1) * 100, 23, 0.5)
pruefe("4.3 BTC-Kursanstieg ggü. 05.08. (%)", (p / PREIS_V10 - 1) * 100, 27, 0.5)
pruefe("4.3 BTC-Umlauf (Mio. BTC)", b["btc_umlauf"] / 1e6, 20.1, 0.05)
pruefe("4.3 BTC-Marktwert (Bio. USD)", b["btc_umlauf"] * p / 1e12, 1.64, 0.005)
pruefe("3 Babylon-Anteil an Chain „Bitcoin\" (Mrd. USD)", b["chain_tvl_usd"]["Bitcoin"] / 1e9, 4.4, 0.05)

# --- Abschnitt 4.2 ---
native = {"RIF ON CHAIN", "MoneyOnChain", "Sovryn Zero", "Sovryn Dex"}
pruefe("4.2 Protokolleinträge (Anzahl)", len(prot), 36)
pruefe("4.2 native Vier (Mio. USD)", sum(x["tvl_rsk"] for x in prot if x["name"] in native) / 1e6, 77, 0.6)
pruefe("4.2 Protokollsumme (Mio. USD)", sum(x["tvl_rsk"] for x in prot) / 1e6, 85.6, 0.05)
pruefe("4.2 Sovryn Zero (Mio. USD)", next(x["tvl_rsk"] for x in prot if x["name"] == "Sovryn Zero") / 1e6, 20.5, 0.05)
pruefe("4.2 Sovryn Lend (USD)", next(x["tvl_rsk"] for x in prot if x["name"] == "Sovryn Lend"), 0)
pruefe("4.2 Uniswap V3 (Mio. USD)", next(x["tvl_rsk"] for x in prot if x["name"] == "Uniswap V3") / 1e6, 2.2, 0.05)
pruefe("4.2 Mellow Core (Mio. USD)", next(x["tvl_rsk"] for x in prot if x["name"] == "Mellow Core") / 1e6, 1.2, 0.05)

# --- Abschnitt 4.1: Gebühr ---
gas_wei = b["rsk_min_gaspreis_wei"]
pruefe("4.1 Mindest-Gaspreis (Gwei)", gas_wei / 1e9, 0.026, 0.0005)
pruefe("4.1 Transfer 21.000 Gas (US-Cent)", 21000 * gas_wei / 1e18 * p * 100, 4.5, 0.05)

# --- Abschnitt 6: MARA + LTV-Beispiel ---
pruefe("6.2 MARA 450 + 300 (Mio. USD)", 450 + 300, 750)
pruefe("6.2 MARA 600 + 150 (Mio. USD)", 600 + 150, 750)
pruefe("6.2 MARA Fazilitätsnominal/Sicherheit 750/1.200 (%)", 750 / 1200 * 100, 62, 0.6)
pruefe("6.3 Sicherheit 10 BTC × 100.000 (USD)", 10 * 100_000, 1_000_000)
pruefe("6.3 LTV Start (%)", 500_000 / 1_000_000 * 100, 50)
pruefe("6.3 Liquidationskurs (USD)", 100_000 * 0.50 / 0.80, 62_500)
pruefe("6.3 LTV bei 62.500 (%)", 500_000 / (10 * 62_500) * 100, 80)
pruefe("6.3 Kursrückgang (%)", (1 - 62_500 / 100_000) * 100, 37.5)
pruefe("6.4 Fazilitäten / Rootstock-TVL (Faktor)", 750e6 / b["chain_tvl_usd"]["Rootstock"], 9, 0.5)

n_fail = ergebnisse.count(False)
print(f"\n{len(ergebnisse)} Prüfungen, {n_fail} FAIL")
sys.exit(1 if n_fail else 0)
