-- Pandoc-Pipe-Tables leiten die LaTeX-Spaltenbreiten aus der Laenge der
-- Trennstriche in der Header-Trennzeile ab, nicht aus dem tatsaechlichen
-- Zellinhalt. Das fuehrt bei kurzen Kopfspalten mit langen Zellinhalten zu
-- zu schmalen Spalten und ueberlappendem Text. Diese Filter-Funktion
-- berechnet die Breiten stattdessen aus dem tatsaechlichen Inhalt
-- (laengstes Wort je Spalte fuer die Mindestbreite, Gesamtlaenge je Spalte
-- fuer die Restverteilung). Rein mechanischer Layout-Fix, kein Eingriff in
-- Formulierungen/Zahlen/Quellen.
function Table(tbl)
  local ncol = #tbl.widths
  if ncol == 0 then return tbl end

  local maxword = {}
  local total = {}
  for i = 1, ncol do
    maxword[i] = 0
    total[i] = 0
  end

  local function scan(cells)
    for i, cell in ipairs(cells) do
      local text = pandoc.utils.stringify(cell)
      total[i] = total[i] + #text
      for word in text:gmatch("%S+") do
        if #word > maxword[i] then maxword[i] = #word end
      end
    end
  end

  scan(tbl.headers)
  for _, row in ipairs(tbl.rows) do
    scan(row)
  end

  -- Gewicht je Spalte: laengstes Wort (verhindert Overflow) + halbes
  -- Gewicht der Gesamtlaenge (fuer sinnvolle Restverteilung/Umbruch).
  local weight = {}
  local sumweight = 0
  for i = 1, ncol do
    weight[i] = maxword[i] + 0.5 * (total[i] / math.max(1, #tbl.rows + 1))
    sumweight = sumweight + weight[i]
  end
  if sumweight == 0 then return tbl end

  local target = 0.98
  local widths = {}
  for i = 1, ncol do
    widths[i] = (weight[i] / sumweight) * target
  end
  tbl.widths = widths
  return tbl
end
