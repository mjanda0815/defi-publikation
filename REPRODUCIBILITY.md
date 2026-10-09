# REPRODUCIBILITY — Artikel „DeFi mit Bitcoin" (v1.1, DE + EN)

Exakte Befehle, Abhängigkeiten und Grenzen der Reproduzierbarkeit. Alle
Pfade relativ zum Projektroot. Datenstichtag der Marktzahlen: **08.10.2026**
(MESZ); Quellenprüfungen danach (bis 09.10.2026) sind in den Anmerkungen
der Bibliographie (`urldate`, `note`) datiert ausgewiesen.

## Abhängigkeiten

| Komponente | Version (getestet) | Hinweis |
|---|---|---|
| Python | 3.x | `python3` (auf dem Build-System existiert kein `python`) |
| matplotlib | 3.10.9 | `pip install -r requirements.txt`; Serifenschrift Latin Modern wird über `stil.py` gewählt (Fallback DejaVu Serif) |
| Pandoc | 2.9.2.1 (lokal) / 2.19 (CI) | Tabellenbreiten über Trennzeilen-Proportionen, kein Lua-Filter (Versionsrobustheit) |
| TeX Live (pdfTeX, latexmk, biber) | 2023+ | `scrartcl`, `biblatex` (biber), `newunicodechar`, `xurl` |
| poppler-utils | – | nur für die Sichtprüfung (`pdftoppm`, `pdfinfo`, `pdffonts`) |

Keine API-Schlüssel, Tokens oder Konten nötig: alle Datenquellen sind
öffentliche, unauthentifizierte Endpunkte.

## 1. Datensnapshots (eingefroren, versioniert)

Rohdaten: `abbildungen/daten/{bitcoin_bruecken,rootstock_tvl,rootstock_protokolle}.json`
(Schema und Endpunkte: `abbildungen/daten/README.md`, Abschnitt „Artikel"). Die
JSON-Dateien enthalten je Wert die Quelle (`quellen`-Block) und den Stichtag.

```bash
# NUR zur Fortschreibung auf einen neuen Stichtag — überschreibt die Snapshots!
python3 abbildungen/snapshot_bitcoin.py --refresh
# Bericht über den vorhandenen Snapshot (ohne Abruf):
python3 abbildungen/snapshot_bitcoin.py
```

Abrufzeitpunkte: Commit-Historie der Snapshot-Dateien (`git log -- abbildungen/daten/`).
Der Gaspreis (`rsk_min_gaspreis_wei`) stammt aus `eth_gasPrice` des öffentlichen
Rootstock-Knotens; DeFiLlama-Werte aus `api.llama.fi` (Protokoll-, Chain- und
Preis-Endpunkte), L-BTC aus der Blockstream-Esplora-API, sBTC aus der Hiro-API,
Lightning-Kapazität von mempool.space, BTC-Umlauf von blockchain.info.

## 2. Zahlenprüfung (Gate C)

```bash
make verify-data          # = python3 abbildungen/verify_snapshot.py
```

Prüft 39 Werte: Tabelle 1 (USD-Umrechnungen mit dem Snapshot-Kurs 81.610,60),
Abschnitt 4.2/4.3 (Protokollsummen, Promille-Anteil, Kurs- und
Summenanstieg, Marktwert), 4.1 (Gebühr aus Gaspreis), Abschnitt 6
(450 + 300 = 750, 600 + 150 = 750, LTV 62 %, Rechenbeispiel 10 BTC /
100.000 USD / 500.000 USD → 62.500 USD, 80 %, −37,5 %). Exit-Code 1 bei
einem FAIL. Stand 09.10.2026: **39/39 PASS**.

## 3. Abbildungen

```bash
python3 abbildungen/bitcoin_bruecken.py        # Abb. 1 (DE)   --en für EN
python3 abbildungen/bitcoin_defi_stack.py      # Abb. 2        --en
python3 abbildungen/rootstock_tvl.py           # Abb. 3        --en
python3 abbildungen/miner_finanzierung.py      # Abb. 4 + 5    --en
```

Ausgabe: `abbildungen/out/<name>[_en].pdf|svg` (Vektorgrafik). Abb. 1 und 3
lesen ausschließlich die Snapshots; Abb. 2, 4 und 5 sind datenfreie
Eigenanfertigungen (Abb. 5 parametrisch aus den Konstanten im Skript).

## 4. PDF-Builds

```bash
cd artikel/bitcoin-defi
make pdf       # deutsche Fassung  → build/main-artikel.pdf
make pdf-en    # englische Fassung → build/main-artikel-en.pdf
```

Pipeline: `artikel.md` / `artikel-en.md` → Pandoc (ab „**Zusammenfassung.**"
bzw. „**Abstract.**", manuelle Abschnittsnummern entfernt) →
`build/artikel-inhalt[-en].tex` → `latexmk` mit `main-artikel[-en].tex`;
Bibliographie `literatur.bib` (DE) bzw. `literatur-en.bib` (EN, gleiche
Einträge, englische Anmerkungen). Sichtprüfung nach jedem Build:
`pdftoppm -png -r 90 build/main-artikel-en.pdf <ziel>/seite`.

## 5. Grenzen der Reproduzierbarkeit

- **Live-Endpunkte driften.** Ein `--refresh` liefert andere Zahlen als der
  eingefrorene Snapshot; reproduzierbar ist der Artikel nur aus den
  versionierten JSON-Dateien. DeFiLlama kann Protokolleinträge nachträglich
  umklassifizieren (Protokollsumme ≠ Chain-TVL, vgl. Abschnitt 4.2).
- **Heterogene Messgrößen.** Tabelle „Messgrößen-Hinweise" (Abschnitt 1)
  definiert, was jede Zahl misst; die Werte sind keine kommensurable Rangfolge.
- **Liquid-Buchbestand.** `lbtc_btc` ist die Netto-Buchgröße der
  Chain-Statistik (Peg-ins − Peg-outs − Burns), keine geprüfte Reserve; der
  Fehlbetrag nach dem Vorfall vom 06.09.2026 ist nur über den
  Blockstream-Bericht (23.09.2026) belegt.
- **Nicht aus Snapshots reproduzierbar** (externe Dokumente, datiert zitiert):
  MARA-SEC-Filings, Merged-Mining-Bericht Q2 2026, bip119monitor-Auswertung,
  Rootstock-Dokumentation, Blockstream-Incident-Report, ESMA Q&A 2671.
- Pandoc 2.9 vs. 2.19 setzen Tabellen minimal unterschiedlich (Seitenzahl
  ±1); inhaltlich identisch.
