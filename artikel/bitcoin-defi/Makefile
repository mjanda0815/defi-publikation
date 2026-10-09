# Makefile — Build des Artikels „DeFi mit Bitcoin" (analog zur Whitepaper-Pipeline)
#
# artikel.md ist die alleinige Quelle des Fließtexts. Konvertiert wird ab der
# Zeile "**Zusammenfassung.**" (Titel/Autor setzt main-artikel.tex selbst);
# die manuelle Abschnittsnummerierung im Markdown ("## 1 …") wird entfernt,
# damit scrartcl nicht doppelt nummeriert.

PANDOC := pandoc
LATEXMK := latexmk
BUILD := build

STRIP_NUMBERING := sed -E 's/^(\#{1,4}) [0-9]+(\.[0-9]+)* /\1 /'

.PHONY: pdf tex pdf-en tex-en clean

$(BUILD):
	mkdir -p $(BUILD)

tex: $(BUILD)
	sed -n '/^\*\*Zusammenfassung\.\*\*/,$$p' artikel.md \
		| $(STRIP_NUMBERING) \
		| $(PANDOC) -f markdown -t latex --top-level-division=section --biblatex \
		--shift-heading-level-by=-1 \
		-o $(BUILD)/artikel-inhalt.tex

pdf: tex
	$(LATEXMK) -pdf -interaction=nonstopmode -outdir=$(BUILD) main-artikel.tex

# Englische Fassung: artikel-en.md ab "**Abstract.**", sonst identische Pipeline
tex-en: $(BUILD)
	sed -n '/^\*\*Abstract\.\*\*/,$$p' artikel-en.md \
		| $(STRIP_NUMBERING) \
		| $(PANDOC) -f markdown -t latex --top-level-division=section --biblatex \
		--shift-heading-level-by=-1 \
		-o $(BUILD)/artikel-inhalt-en.tex

pdf-en: tex-en
	$(LATEXMK) -pdf -interaction=nonstopmode -outdir=$(BUILD) main-artikel-en.tex

clean:
	rm -rf $(BUILD)
