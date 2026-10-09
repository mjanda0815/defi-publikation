# Eingecheckte Rohdaten für die Abbildungen

## Artikel „DeFi mit Bitcoin" (v1.1, Stichtag 08.10.2026)

Erzeugt mit `python3 abbildungen/snapshot_bitcoin.py --refresh`; geprüft mit
`make verify-data` (39 Werte, Stand 09.10.2026: alle PASS). Zeitzone der
Abrufe: MESZ; Abrufzeitpunkt = Commit-Datum der JSON-Dateien.

| Datei | Endpunkte | Felder (Schema) | Messgröße |
|---|---|---|---|
| `bitcoin_bruecken.json` | `api.llama.fi/protocol/{wbtc,tbtc,lightning-network,babylon-protocol}`, `api.llama.fi/v2/chains`, `coins.llama.fi/prices/current/coingecko:bitcoin`, `blockstream.info/liquid/api/asset/<L-BTC>`, `api.hiro.so/metadata/v1/ft/<sBTC>`, `mempool.space/api/v1/lightning/statistics/latest`, `blockchain.info/q/totalbc`, `public-node.rsk.co` (`eth_gasPrice`) | `stichtag`, `btc_preis_usd`, `rsk_min_gaspreis_wei`, `btc_umlauf`, `wbtc_usd`, `tbtc_usd`, `lightning_usd`, `babylon_usd`, `lbtc_btc`, `sbtc_btc`, `lightning_btc`, `lightning_kanaele`, `chain_tvl_usd{Rootstock,Stacks,Citrea,BOB,Bitcoin,Ethereum}`, `chain_tvl_summe_usd`, `quellen` | wBTC/tBTC/Babylon: DeFiLlama-Protokoll-TVL in USD (Verwahr-/Sperrbestand bzw. Token-Umlauf); `lbtc_btc` = Peg-ins − Peg-outs − Burns (Buchbestand); `sbtc_btc` = Total Supply; `lightning_btc` = öffentliche Kanalkapazität; Chain-TVL = DeFiLlama-Aggregat je Chain; Summe = Σ aller Chains |
| `rootstock_tvl.json` | `api.llama.fi/v2/historicalChainTvl/Rootstock` | Liste `{date (Unix), tvl (USD)}` | tägliche Chain-TVL-Historie (Abb. 3, ATH 07.10.2025) |
| `rootstock_protokolle.json` | `api.llama.fi/protocols` (gefiltert auf Chain-Key `RSK`) | Liste `{name, slug, category, tvl_rsk}` | Protokoll-TVL auf Rootstock (Abschnitt 4.2); Σ ≠ Chain-TVL (Aggregator-Abgrenzung) |

Berechnungsschritte im Artikel (alle in `verify_snapshot.py` nachgerechnet):
USD-Werte für L-BTC/sBTC/Lightning = BTC-Menge × `btc_preis_usd`; Rootstock-Anteil
= `chain_tvl_usd.Rootstock / chain_tvl_summe_usd`; BTC-Marktwert = `btc_umlauf ×
btc_preis_usd`; Transfergebühr = 21.000 × `rsk_min_gaspreis_wei` / 1e18 × Kurs.

## Whitepaper (Stichtage 01.–03.08.2026)

Alle Marktdaten stammen aus Primärquellen (harte Regel 2, CLAUDE.md) und liegen
hier als Snapshot im Repository, damit jede Abbildung reproduzierbar ist.
Aktualisieren mit `python abbildungen/<name>.py --refresh` (überschreibt den
Snapshot und setzt den Stichtag in der Grafik neu — vor Redaktionsschluss einmal
final ausführen).

| Datei | Quelle (API) | Inhalt | Stichtag Snapshot |
|---|---|---|---|
| `defillama_tvl_gesamt.json` | https://api.llama.fi/v2/historicalChainTvl | DeFi-TVL gesamt (alle Chains), täglich, USD | 02.08.2026 |
| `blockchain_info_hashrate.json` | https://api.blockchain.info/charts/hash-rate?timespan=all&format=json&sampled=false | Bitcoin-Hashrate, täglich, TH/s | 01.08.2026 |
| `defillama_protokolle.json` | https://api.llama.fi/protocols (Top-30 + Fallstudien, Skript `snapshot_defillama.py`) | TVL je Protokoll | 02.08.2026 |
| `defillama_chains.json` | https://api.llama.fi/v2/chains (Skript `snapshot_defillama.py`) | TVL je Blockchain | 02.08.2026 |
| `defillama_stablecoins.json` | https://stablecoins.llama.fi/stablecoins (Skript `stablecoins.py`) | Stablecoin-Umlauf je Asset | 02.08.2026 |
| `defillama_protokolle_2023.json` | https://api.llama.fi/protocol/\<slug\> (Feld `tvl`, Zeitreihe) | TVL je Protokoll zum Stichtag 09.03.2023 (Vergleichswerte für Kap. 4.7) | 02.08.2026 (Abfrage), Datenstichtag 09.03.2023 |

Referenzwerte aus dem TVL-Snapshot (für konsistente Zahlen im Text, alle Werte
gerundet, Quelle: DeFiLlama):

- Allzeithoch: **177,5 Mrd. USD am 09.11.2021**
- Anfang 2023: ~37,8 Mrd. USD (01.01.2023); ~44,2 Mrd. USD am 10.03.2023
  (Vergleichswert zur Abb. 4.1 des Originals, „März 2023"); beides widerlegt
  die „150 Mrd. im Januar 2023"-Angabe in Kap. 5.1.1
- Zweiter Gipfel nach der Erholung: **171,0 Mrd. USD am 07.10.2025**
- Stand 02.08.2026: **74,2 Mrd. USD**

Hashrate-Referenzen: 30-Tage-Mittel ~903 EH/s, Tageswert ~1.029 EH/s (01.08.2026);
30-Tage-Mittel April 2023: ~331 EH/s (Vergleichswert zur Erstfassung — die dort
genannten 409/363 EH/s stammten von BitInfoCharts mit anderer Messmethodik).

Weitere Snapshots: `defillama_stablecoins.json` (Stablecoin-Umlauf je Asset,
02.08.2026: USDT ~183,2 Mrd., USDC ~72,1 Mrd., USD-Stablecoins gesamt ~307 Mrd. USD)
und `defillama_chains.json` (TVL je Blockchain, 02.08.2026: Ethereum ~40,8 Mrd. USD
= ~55 % des Gesamt-TVL).

Protokoll-TVLs zum Stichtag 09.03.2023 (`defillama_protokolle_2023.json`, für die
Vergleichstabelle in Kap. 4.7; verwendete Slugs in Klammern, exakter Datenpunkt am
09.03.2023 vorhanden — kein Interpolationsbedarf):

| Protokoll | Slug | TVL 09.03.2023 (Mrd. USD) |
|---|---|---|
| Aave | `aave` | 4,70 |
| Compound | `compound-finance` | 1,89 |
| Uniswap | `uniswap` | 3,85 |
| PancakeSwap | `pancakeswap` | 2,49 |
| Curve | `curve-dex` | 4,85 |
| Nexus Mutual | `nexus-mutual` | 0,205 |
| Opyn | `opyn` | 0,0498 |

## defillama_kategorien.json (Stichtag: 03.08.2026)

Kategorien-Aggregation aus dem freien `/protocols`-Endpoint (der dedizierte
`/categories`-Endpoint ist seit 2026 kostenpflichtig, HTTP 402). Erzeugt via
`python abbildungen/snapshot_kategorien.py --refresh`. Referenzwerte
(TVL-Summe je Kategorie, ohne CEX/Bridges als DeFi-Kategorien):
Lending 40,5 Mrd · Liquid Staking 35,2 Mrd · RWA 26,7 Mrd · Dexs 11,2 Mrd ·
Staking Pool 10,4 Mrd · Restaking 8,0 Mrd · CDP 7,9 Mrd USD.
Wichtig: Lending liegt damit VOR Liquid Staking — die frühere Formulierung
„Liquid Staking ist die größte Kategorie" war zum Stichtag nicht mehr haltbar
(korrigiert am 03.08.2026 in 3.5.6, 4.6 und 6.2).
