"""Snapshot-Skript für den Artikel „DeFi mit Bitcoin" (artikel/bitcoin-defi/).

Erzeugt reproduzierbar die eingecheckten Snapshots (Gütekriterium
„Datengrundlage und Reproduzierbarkeit" des Whitepapers, Kap. 1.3):
- daten/rootstock_tvl.json        — TVL-Historie der Rootstock-Chain (DeFiLlama)
- daten/rootstock_protokolle.json — Protokolle auf Rootstock (Chain-Key „RSK")
- daten/bitcoin_bruecken.json     — Volumina der Bitcoin-Brücken/Wege je Quelle:
    wBTC, tBTC, Lightning, Babylon (DeFiLlama-Protokoll-Endpunkte),
    Chain-TVL Rootstock/Stacks/Citrea/BOB/Bitcoin/Ethereum (DeFiLlama /v2/chains),
    L-BTC-Umlauf (Blockstream-Esplora), sBTC-Umlauf (Hiro-API),
    Lightning-Kapazität in BTC (mempool.space), BTC-Referenzpreis (DeFiLlama coins).

Aufruf:  python abbildungen/snapshot_bitcoin.py [--refresh]
Ohne --refresh werden nur die vorhandenen Snapshots zusammengefasst.
"""

import json
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path

HIER = Path(__file__).parent
DATEN = HIER / "daten"

LBTC_ASSET = "6f0279e9ed041c3d710a9f57d0c02928416460c4b722ae3457a11eec381c526d"
SBTC_TOKEN = "SM3VDXK3WZZSA84XXFKAFAF15NNZX32CTSG82JFQ4.sbtc-token"


def hole(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())


def hole_zahl(url: str) -> float:
    """Endpunkte, die eine nackte Zahl liefern (z. B. blockchain.info/q/*)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return float(r.read())


def protokoll_tvl(slug: str) -> float:
    """Aktueller Gesamt-TVL eines DeFiLlama-Protokolls in USD."""
    d = hole(f"https://api.llama.fi/protocol/{slug}")
    reihe = d.get("tvl") or []
    return reihe[-1]["totalLiquidityUSD"] if reihe else 0.0


def refresh() -> None:
    # Rootstock: TVL-Historie und Protokoll-Liste
    (DATEN / "rootstock_tvl.json").write_text(json.dumps(
        hole("https://api.llama.fi/v2/historicalChainTvl/Rootstock"), indent=1))
    prot = hole("https://api.llama.fi/protocols")
    rsk = [{k: p.get(k) for k in ("name", "slug", "category")} |
           {"tvl_rsk": (p.get("chainTvls") or {}).get("RSK", 0)}
           for p in prot if "RSK" in (p.get("chains") or [])]
    rsk.sort(key=lambda p: -p["tvl_rsk"])
    (DATEN / "rootstock_protokolle.json").write_text(json.dumps(rsk, indent=1))

    # Brücken-/Wege-Volumina (je Eintrag: Wert + Quelle, Stichtag = heute)
    chains = {c["name"]: c["tvl"] for c in hole("https://api.llama.fi/v2/chains")}
    btc_preis = hole("https://coins.llama.fi/prices/current/coingecko:bitcoin"
                     )["coins"]["coingecko:bitcoin"]["price"]
    lbtc = hole(f"https://blockstream.info/liquid/api/asset/{LBTC_ASSET}")["chain_stats"]
    lbtc_btc = (lbtc["peg_in_amount"] - lbtc["peg_out_amount"] - lbtc["burned_amount"]) / 1e8
    sbtc_btc = int(hole(f"https://api.hiro.so/metadata/v1/ft/{SBTC_TOKEN}"
                        )["total_supply"]) / 1e8
    ln = hole("https://mempool.space/api/v1/lightning/statistics/latest")["latest"]

    bruecken = {
        "stichtag": date.today().isoformat(),
        "btc_preis_usd": btc_preis,
        "btc_umlauf": hole_zahl("https://blockchain.info/q/totalbc") / 1e8,
        "wbtc_usd": protokoll_tvl("wbtc"),
        "tbtc_usd": protokoll_tvl("tbtc"),
        "lightning_usd": protokoll_tvl("lightning-network"),
        "babylon_usd": protokoll_tvl("babylon-protocol"),
        "lbtc_btc": lbtc_btc,
        "sbtc_btc": sbtc_btc,
        "lightning_btc": ln["total_capacity"] / 1e8,
        "lightning_kanaele": ln["channel_count"],
        "chain_tvl_usd": {name: chains.get(name) for name in
                          ("Rootstock", "Stacks", "Citrea", "BOB",
                           "Bitcoin", "Ethereum")},
        "quellen": {
            "wbtc/tbtc/lightning/babylon": "api.llama.fi/protocol/<slug>",
            "chains": "api.llama.fi/v2/chains",
            "lbtc": f"blockstream.info/liquid/api/asset/{LBTC_ASSET}",
            "sbtc": f"api.hiro.so/metadata/v1/ft/{SBTC_TOKEN}",
            "lightning_btc": "mempool.space/api/v1/lightning/statistics/latest",
            "btc_preis": "coins.llama.fi/prices/current/coingecko:bitcoin",
        },
    }
    (DATEN / "bitcoin_bruecken.json").write_text(json.dumps(bruecken, indent=1))


def bericht() -> None:
    tvl = json.loads((DATEN / "rootstock_tvl.json").read_text())
    ath = max(tvl, key=lambda p: p["tvl"])
    print(f"Rootstock-TVL: {tvl[-1]['tvl']/1e6:.1f} Mio USD "
          f"({datetime.fromtimestamp(tvl[-1]['date']).date()}); "
          f"ATH {ath['tvl']/1e6:.1f} Mio ({datetime.fromtimestamp(ath['date']).date()})")
    b = json.loads((DATEN / "bitcoin_bruecken.json").read_text())
    print(f"Stichtag {b['stichtag']}, BTC {b['btc_preis_usd']:,.0f} USD")
    for k in ("wbtc_usd", "babylon_usd", "tbtc_usd", "lightning_usd"):
        print(f"  {k:<14}{b[k]/1e6:10.1f} Mio USD")
    print(f"  L-BTC {b['lbtc_btc']:,.0f} BTC · sBTC {b['sbtc_btc']:,.0f} BTC · "
          f"Lightning {b['lightning_btc']:,.1f} BTC")
    for name, v in b["chain_tvl_usd"].items():
        print(f"  Chain {name:<10}{(v or 0)/1e6:10.1f} Mio USD")


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        refresh()
    bericht()
