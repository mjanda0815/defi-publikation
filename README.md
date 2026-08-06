# Decentralized Finance — Quellen und Datenstände der Veröffentlichungen

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21815634.svg)](https://doi.org/10.5281/zenodo.21815634)

Dieses Repository enthält die Quelltexte, Abbildungsskripte und eingefrorenen
Datenstände zu zwei Veröffentlichungen von Martin Janda:

1. **Whitepaper: „Decentralized Finance und die Zukunft des Finanzwesens"**
   (überarbeitete und aktualisierte Fassung der an der AKAD University
   angenommenen Diplomarbeit; Stand: August 2026)
   → [Beitrag mit PDF-Download](https://www.janda.io/veroeffentlichungen/whitepaper-decentralized-finance)
2. **Artikel: „DeFi mit Bitcoin — wie weit trägt die Basis ohne Altcoins?"**
   (Begleitartikel, Version 1.0, August 2026; Marktdaten-Stichtag: 05.08.2026)
   → [Beitrag mit PDF-Download](https://www.janda.io/veroeffentlichungen/defi-mit-bitcoin)

Zweck des Repositories ist die **Reproduzierbarkeit**: Alle datenbasierten
Abbildungen und die daraus im Text abgeleiteten Marktzahlen lassen sich aus den
hier eingecheckten API-Snapshots regenerieren; jede Zahl in den Texten trägt
Quelle und Stichtag.

## Struktur

```
kapitel/            Whitepaper-Quelltext (Markdown, Kapitel 1–6 + Glossar)
main.tex, Makefile  Whitepaper-Build (Pandoc → LaTeX → PDF, Bibliographie: literatur.bib)
artikel/bitcoin-defi/  Artikel-Quelltext, eigene Bibliographie und eigener Build
abbildungen/        Abbildungsskripte (Python/matplotlib) + daten/ (eingefrorene Snapshots)
```

## Reproduktion

Voraussetzungen: TeX Live (mit latexmk und biber), Pandoc, Python 3 mit
matplotlib. Der CI-Workflow (`.github/workflows/build.yml`) dokumentiert eine
funktionierende Umgebung.

```sh
# Abbildungen aus den eingecheckten Datenständen erzeugen, z. B.:
python3 abbildungen/tvl.py
python3 abbildungen/bitcoin_bruecken.py

# Whitepaper bauen:
make pdf              # → build/main.pdf

# Artikel bauen:
cd artikel/bitcoin-defi && make pdf   # → build/main-artikel.pdf
```

**Hinweis zu den Datenständen:** Die JSON-Dateien unter `abbildungen/daten/`
sind bewusst eingefrorene Snapshots mit den in den Texten ausgewiesenen
Stichtagen (Whitepaper: 02.08.2026, Artikel: 05.08.2026). Die
`snapshot_*.py`-Skripte laden mit `--refresh` **neue** Datenstände von den
jeweiligen APIs (DeFiLlama, Blockstream, Hiro, mempool.space, Blockchain.com)
und überschreiben die Snapshots — für die Reproduktion der veröffentlichten
Fassungen also nicht ausführen.

## Herkunft und Abgrenzung

Das Whitepaper basiert auf der 2023 eingereichten und angenommenen
Diplomarbeit; für die Veröffentlichung wurden Marktdaten und regulatorischer
Stand aktualisiert und einzelne Kapitel überarbeitet. Prüfungsbezogene
Bestandteile und interne Arbeitsdokumente sind nicht Teil dieses Repositories.

## Zitieren

DOI (alle Versionen): [10.5281/zenodo.21815634](https://doi.org/10.5281/zenodo.21815634) — Zitierangaben siehe [CITATION.cff](CITATION.cff).

## Lizenz

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.de) — siehe
[LICENSE](LICENSE). Kontakt: martin@janda.io
