<!-- Überarbeitete Fassung (Session 4, Stand: 02.08.2026). Basis: Original-PDF (2023), Seiten 13–36.
     Wesentliche Änderungen: Restrukturierung nach Erstgutachten (Hash-Funktionen als neuer Abschnitt 2.2
     VOR ihrer Verwendung; PoW-Mechanik einmalig in 2.4 konsolidiert statt doppelt; Glossar 2.7 aufgelöst —
     Begriffe bei Erstnennung integriert, Rest im Anhang-Glossar), Buterin-Faktenkorrektur, Halving/Hashrate
     aktualisiert (blockchain.com-Zeitreihe), Merkle-Baum neu mit durchgerechnetem Beispiel und eigener
     Abbildung, PoW-Darstellung ausbalanciert. Zitate auf [vgl. @key] umgestellt. Details: CHANGELOG.md. -->

# 2 Blockchain-Grundlagen

## 2.1 Theoretische Grundlagen

Blockchain lässt sich in die unterliegende Datenstruktur und das zugehörige Verwaltungssystem unterscheiden. Die Blockchain ist nach Condos et al. (2016) ein elektronisches Register für digitale Datensätze, Ereignisse oder Transaktionen [vgl. @condos2016]. In dieser Datenbank erfolgen Einträge in Blöcken, die in chronologischer Reihenfolge verknüpft sind. Die Verknüpfung erfolgt durch kryptografische Verfahren, wodurch jeder Block die Transaktionen, die seit dem Hinzufügen des letzten Blocks entstanden sind, enthält. Im Kontrast zu zentralen Datenbanken übernimmt ein dezentrales Verwaltungssystem die Verifikation des Netzwerkstatus. Blockchain-Verwaltungssysteme basieren auf Kryptografie und Peer-to-Peer-Prinzipien (P2P).

Peer-to-Peer bezeichnet eine dezentrale Kommunikationsarchitektur, bei der einzelne Knoten („Peers“) direkt miteinander kommunizieren, statt über zentrale Server. Jeder Peer nimmt dabei zugleich die Rolle eines Clients und eines Servers ein und stellt dem Netzwerk Hardware-Ressourcen wie Bandbreite, Speicherplatz oder Rechenleistung zur Verfügung — diese bereitgestellten Ressourcen sind die Leistungsgrundlage jedes dezentralen Netzwerks. Während in klassischen Netzwerken eine zentrale Instanz für die Kommunikation zwischen den Teilnehmern sorgt, erfolgt der Datenaustausch in P2P-Netzwerken direkt zwischen den Teilnehmern, ohne zentrale Koordinations- und Kommunikationsinstanz [vgl. @schlatt2016]. Bekannte Anwendungen dieser Architektur sind File-Sharing-Systeme wie BitTorrent — und eben Blockchains wie Bitcoin. Der Verzicht auf zentrale Punkte macht solche Netzwerke widerstandsfähig gegen Ausfälle und Angriffe auf einzelne Stellen; er bedeutet aber auch, dass Sicherheit und Vertrauen ohne zentrale Kontrollinstanz hergestellt werden müssen — die zentrale Herausforderung, die in diesem Kapitel Schritt für Schritt entwickelt wird.

## 2.2 Kryptografische Grundlagen: Hash-Funktionen

Bevor die Funktionsweise der Blockchain erläutert wird, werden die kryptografischen Bausteine eingeführt, auf denen sie beruht — allen voran die Hash-Funktion, die in nahezu jedem der folgenden Abschnitte eine Rolle spielt.

Eine Hash-Funktion ist ein mathematischer Algorithmus, der Daten beliebiger Länge (Eingabe) auf eine Ausgabe fester Länge (Hash-Wert) abbildet. Kryptografische Hash-Funktionen haben dabei folgende Eigenschaften [vgl. @stallings2016]:

- **Determinismus:** Für dieselbe Eingabe wird immer derselbe Hash-Wert erzeugt.
- **Effizienz:** Die Berechnung des Hash-Werts ist schnell und effizient möglich.
- **Einwegfunktion:** Es ist praktisch unmöglich, vom Hash-Wert auf die ursprünglichen Daten zu schließen — die Funktion ist nicht umkehrbar.
- **Avalanche-Effekt:** Selbst kleinste Änderungen der Eingabe führen zu einem völlig anderen Hash-Wert.
- **Kollisionsresistenz:** Es ist praktisch unmöglich, zwei unterschiedliche Eingaben zu finden, die denselben Hash-Wert ergeben.

Im Bitcoin-Netzwerk kommt die Hash-Funktion SHA-256 („Secure Hash Algorithm“, 256 Bit) aus der SHA-2-Familie zum Einsatz. Sie erzeugt aus beliebigen Eingaben einen 256-Bit-Wert, der üblicherweise als 64-stellige Hexadezimalzahl dargestellt wird [vgl. @stallings2016; @wu2018]. Der Avalanche-Effekt lässt sich daran unmittelbar zeigen: Die Eingabe „Blockchain“ ergibt einen SHA-256-Wert, der mit `625da44e…` beginnt; ändert man nur den Anfangsbuchstaben zu „blockchain“, beginnt der Wert mit `ef7797e1…` — die beiden Ausgaben haben nichts erkennbar Gemeinsames.

Neben Hash-Funktionen nutzt Bitcoin digitale Signaturen: Jeder Teilnehmer besitzt ein Schlüsselpaar aus privatem und öffentlichem Schlüssel. Mit dem privaten Schlüssel werden Transaktionen signiert; jeder andere Teilnehmer kann die Signatur mit dem öffentlichen Schlüssel prüfen, ohne den privaten Schlüssel zu kennen. So ist sichergestellt, dass ausschließlich der Inhaber einer Bitcoin-Adresse über deren Guthaben verfügen kann [vgl. @nakamoto2008].

Diese beiden Bausteine — Hash-Funktionen und digitale Signaturen — genügen, um die im Folgenden beschriebene Funktionsweise der Blockchain vollständig nachzuvollziehen.

## 2.3 Funktionsweise der Blockchain

Die grundlegende Funktionsweise der Blockchain lässt sich am Beispiel der Bitcoin-Blockchain erklären. Die Bitcoin-Blockchain wurde 2008 von Satoshi Nakamoto in dem Paper „Bitcoin: A Peer-to-Peer Electronic Cash System“ [vgl. @nakamoto2008] eingeführt. Das Problem, das die Bitcoin-Blockchain zu lösen versuchte: Handel im Internet ist auf Finanzinstitutionen angewiesen, um Vertrauen zwischen Käufer- und Verkäuferseite einer Transaktion herzustellen. Die Finanzinstitutionen als Intermediäre erhöhen die Transaktionskosten, was kleine Transaktionen unrentabel macht. Um Vertrauen zwischen den Vertragsparteien herstellen zu können, benötigen sie zudem vermehrt persönliche Daten ihrer Kunden. Die Bitcoin-Blockchain löst dieses Problem, indem Dritte aus dem Prozess herausgelöst werden und die Vertrauensbasis durch Kryptografie hergestellt wird, wodurch die Vertragsparteien direkt miteinander handeln können [vgl. @nakamoto2008].

### 2.3.1 Das Double-Spend-Problem

Ein Problem, das normalerweise von zentralen Instanzen bewältigt wird und nun der Blockchain obliegt, ist das Double-Spend-Problem. Es beschreibt die Anforderung, dass digitales Geld nicht mehrfach ausgegeben werden darf. Der Verkäufer einer Ware kann bei rein digitalem Geld nicht ohne Weiteres verifizieren, ob der Käufer dieselbe Geldeinheit bereits zuvor ausgegeben hat. In zentralisierten Systemen obliegt diese Prüfung einer zentralen Instanz: Sie emittiert das Geld, führt die Konten und bürgt für die Gültigkeit jeder Zahlung. In einem dezentralen System muss dieselbe Aufgabe ohne vertrauenswürdige zentrale Instanz gelöst werden.

Bitcoin adressiert das Problem durch eine dezentrale, verteilte Architektur, in der mehrere Schlüsselelemente zusammenwirken:

1. **Dezentralisierung:** Bitcoin setzt auf ein P2P-Netzwerk (Abschnitt 2.1), in dem sämtliche Teilnehmer (Knoten) direkt miteinander interagieren. Hierdurch entfällt die Notwendigkeit einer zentralen Instanz oder eines Vermittlers.

2. **Blockchain:** Die Blockchain ist ein öffentlich einsehbares, digitales Hauptbuch, das sämtliche bestätigten Transaktionen in chronologischer Reihenfolge erfasst. Jeder vollständige Knoten im Netzwerk verfügt über eine Kopie der Blockchain, wodurch Transparenz und Nachvollziehbarkeit gewährleistet werden.

3. **Unabhängige Validierung:** Jeder Knoten prüft jede empfangene Transaktion selbstständig gegen die Konsensregeln des Netzwerks: Ist die digitale Signatur gültig (Abschnitt 2.2)? Existieren die auszugebenden Geldeinheiten, und wurden sie nicht bereits ausgegeben? Nur Transaktionen, die diese Prüfungen bestehen, werden weitergeleitet und können in Blöcke aufgenommen werden. Die Gültigkeit einer Transaktion wird also nicht durch das Mining hergestellt, sondern durch die unabhängige Prüfung aller Knoten [vgl. @antonopoulos2014].

4. **Konsensmechanismus:** Bitcoin nutzt den Proof-of-Work-Mechanismus (im Detail in Abschnitt 2.4): Miner konkurrieren darum, neue Transaktionsblöcke an die Blockchain anzuhängen, und werden dafür mit neu erzeugten Bitcoin belohnt — seit dem Halving im April 2024 mit 3,125 Bitcoin je Block [@blockchaininfo2026]. Der Konsensmechanismus legt fest, in welcher Reihenfolge Transaktionen in die gemeinsame Historie eingehen — und macht es damit mit jeder weiteren Bestätigung unwahrscheinlicher, dass dieselbe Geldeinheit ein zweites Mal ausgegeben werden kann (probabilistische Endgültigkeit, Abschnitte 2.4 und 2.5.4).

5. **Kryptografische Verkettung:** Die Blöcke sind über Hash-Werte miteinander verkettet (Abschnitt 2.5.2). Einmal bestätigte Transaktionen können dadurch nicht mehr unbemerkt verändert werden.

Diese Kombination aus Dezentralisierung, unabhängiger Validierung, Konsensmechanismus und kryptografischer Verkettung ermöglicht, dass das Bitcoin-Netzwerk ohne zentrale Instanz funktioniert und dabei ein hohes Maß an Sicherheit und Vertrauen bietet.

### 2.3.2 Das Konsensproblem in verteilten Systemen

Das byzantinische Generalsproblem (BGP) ist ein fundamentales Konsensproblem in verteilten Systemen, das die Schwierigkeiten bei der Koordination und Kommunikation zwischen unterschiedlichen Teilnehmern eines dezentralen Netzwerks veranschaulicht. In diesem hypothetischen Szenario müssen Generäle, die von verschiedenen Standorten aus operieren, einen gemeinsamen Angriffsplan koordinieren [vgl. @lamport1982, S. 382–384]. Die Herausforderung entsteht durch die Möglichkeit, dass einige Generäle unzuverlässig oder sogar feindlich gesinnt sein könnten, und dadurch, dass die Kommunikation zwischen den Generälen über unsichere Kanäle stattfindet. In Abbildung \ref{fig:bgp} ist die Absicht eines abtrünnigen Generals durch den roten Pfeil dargestellt, der nicht auf das gemeinsame Angriffsziel gerichtet ist. Die Folge wäre eine Schwächung des Angriffs und daraus resultierend ein mögliches Scheitern.

![Das byzantinische Generalsproblem: Konsens trotz unzuverlässiger Teilnehmer und unsicherer Kommunikationskanäle. Eigene Darstellung. \label{fig:bgp}](abbildungen/out/byzantiner.pdf){ width=93% }

Das Hauptziel bei der Lösung des BGP besteht darin, einen Konsens unter den Teilnehmern eines verteilten Systems zu erreichen, selbst wenn einige Knoten im Netzwerk fehlerhaft oder bösartig sind. Um dieses Problem effektiv zu lösen, muss das System zwei Bedingungen erfüllen:

1. Alle ehrlichen Knoten müssen sich auf denselben Wert einigen.
2. Eine kleine Anzahl bösartiger Knoten darf das System nicht kompromittieren können.

Da Bitcoin ein dezentrales Netzwerk ist, in dem die Knoten unabhängig voneinander arbeiten und potenziell Fehlinformationen oder bösartige Angriffe auftreten können, ist das BGP hier von zentraler Bedeutung. Bitcoins Antwort darauf ist der Proof-of-Work-Mechanismus: Wer einen Block anhängen will, muss dafür nachweisbar Rechenaufwand investieren. Wie dieser Mechanismus im Einzelnen funktioniert und warum er zugleich das ökonomische Fundament des Netzwerks bildet, erläutert der folgende Abschnitt.

## 2.4 Mining, Proof of Work und das ökonomische Anreizsystem

Mining ist der Prozess, der im Bitcoin-Netzwerk neue Blöcke erzeugt, Transaktionen in die gemeinsame Historie aufnimmt und dabei zugleich neue Bitcoin in Umlauf bringt. Miner sind Teilnehmer, die Rechenleistung einsetzen, um das kryptografische Rätsel des Proof-of-Work-Mechanismus zu lösen [vgl. @narayanan2016].

**Der Proof-of-Work-Mechanismus.** Das „Rätsel“ besteht darin, einen Blockheader (Abschnitt 2.5.1) so zu vervollständigen, dass sein SHA-256-Hash-Wert unter einem vom Protokoll vorgegebenen Schwellenwert liegt. Dazu variiert der Miner die sogenannte Nonce — ein Freifeld im Blockheader: Er setzt einen Wert ein, berechnet den Hash des Headers und prüft das Ergebnis (in der Praxis werden bei erschöpftem Nonce-Raum zusätzlich Felder wie der Zeitstempel und die Coinbase-Transaktion variiert). Wegen des Avalanche-Effekts (Abschnitt 2.2) führt jede Änderung der Nonce zu einem völlig anderen Hash-Wert; nach heutigem Kenntnisstand existiert kein effizienteres Verfahren als systematisches Ausprobieren. Ein gültiger Hash lässt sich daher nur durch massenhaftes Ausprobieren finden — das erfordert Rechenleistung und damit Zeit und Energie —, während jeder andere Knoten mit einer einzigen Hash-Berechnung überprüfen kann, dass die gefundene Lösung korrekt ist [vgl. @fill2020]. Der Schwellenwert wird vom Protokoll regelmäßig angepasst, sodass die durchschnittliche Blockzeit bei etwa zehn Minuten bleibt, auch wenn sich die Gesamtrechenleistung des Netzwerks stark verändert. Hat ein Miner eine gültige Lösung gefunden, propagiert er den Block an alle Netzwerkteilnehmer; diese prüfen den Block und seine Transaktionen und beginnen, auf dem neuen Block aufbauend am nächsten zu arbeiten.

![Der Proof-of-Work-Zyklus: Nonce variieren, hashen, gegen die Zielschwelle prüfen. Eigene Darstellung. \label{fig:pow}](abbildungen/out/pow_schema.pdf){ width=93% }

**Das Anreizsystem.** Für die erfolgreiche Lösung wird der Miner über die sogenannte Coinbase-Transaktion belohnt — einen speziellen Transaktionstyp, der neue Coins erzeugt und ohne vorherige Transaktionseingänge an eine vom Miner definierte Adresse sendet; zusätzlich sammelt sie die Transaktionsgebühren des Blocks ein. Diese Belohnung setzt den Anreiz, Rechenleistung bereitzustellen und ehrlich zu agieren. Zugleich steuert sie die Geldschöpfung des Systems: Die anfängliche Belohnung betrug 50 Bitcoin pro Block und halbiert sich alle 210.000 Blöcke — bei etwa zehn Minuten Blockzeit entspricht das rund vier Jahren. Dieses Ereignis ist als „Halving“ bekannt [vgl. @nakamoto2008; @antonopoulos2014]. Zuletzt wurde die Belohnung im April 2024 (Block 840.000) auf aktuell 3,125 Bitcoin halbiert; die nächste Halbierung wird turnusgemäß für das Frühjahr 2028 erwartet [@blockchaininfo2026]. Der Prozess wird fortgesetzt, bis alle 21 Millionen Bitcoin geschöpft sind. Ökonomisch war das Mining ursprünglich als Mechanismus zur breiten Verteilung neuer Einheiten angelegt; mit der Industrialisierung des Minings hat sich diese Verteilungswirkung relativiert (vgl. die Pool-Konzentration unten). Erhalten geblieben ist die zweite Funktion: eine kontrollierte, im Voraus planbare Geldmengenentwicklung.

**Hashrate und Netzwerksicherheit.** Die Gesamthashrate bezeichnet die kombinierte Rechenleistung aller Miner, gemessen in Hashes pro Sekunde (H/s) bzw. deren Vielfachen bis hin zu Exahashes pro Sekunde (1 EH/s = 10^18 H/s). Abbildung \ref{fig:hashrate} zeigt ihre Entwicklung seit 2016: Im April 2023 lag das 30-Tage-Mittel bei rund 330 EH/s; bis August 2026 hat es sich auf rund 900 EH/s nahezu verdreifacht, Tageswerte überschritten zeitweise 1.000 EH/s (Stand: 01.08.2026) [@blockchaininfo2026].

![Entwicklung der Bitcoin-Hashrate seit 2016 (Tageswerte und 30-Tage-Mittel) mit den Halving-Zeitpunkten. Eigene Darstellung; Datenquelle: blockchain.com [@blockchaininfo2026]. \label{fig:hashrate}](abbildungen/out/hashrate.pdf){ width=93% }

Die Hashrate ist ein Indikator für die Angriffskosten auf das Netzwerk: Ein Angreifer, der die Transaktionshistorie umschreiben oder eigene Double-Spends durchsetzen wollte, müsste dauerhaft mehr als die Hälfte der gesamten Rechenleistung kontrollieren — ein sogenannter 51-%-Angriff [vgl. @narayanan2016]. Die Hardware- und Energiekosten eines solchen Angriffs steigen proportional zur Gesamthashrate: Bei einem 30-Tage-Mittel von rund 900 EH/s müsste ein Angreifer eine Rechenleistung aufbauen und dauerhaft betreiben, die die gesamte übrige Mining-Industrie übertrifft. Selbst ein erfolgreicher Angriff wäre zudem für jeden Beobachter sichtbar und würde das Vertrauen in das System — und damit den Wert der erbeuteten Coins und der Mining-Ausrüstung des Angreifers — untergraben. Da Miner erhebliche Ressourcen investieren, haben sie einen starken wirtschaftlichen Anreiz, das Netzwerk zu schützen statt es anzugreifen. Aus der hohen Hashrate folgt allerdings nur die Sicherheit gegen diese Klasse von Angriffen auf die Transaktionshistorie: Risiken wie Protokollfehler, der Diebstahl privater Schlüssel oder die Konzentration großer Teile der Hashrate in wenigen Mining-Pools bleiben davon unberührt. Die verbreitete Einschätzung, Bitcoin sei das sicherste dezentrale Transaktionssystem, ist in diesem eingeschränkten Sinn zu verstehen — als Aussage über die Kosten eines Historien-Angriffs, nicht als pauschale Sicherheitsgarantie.

**Energieverbrauch und Alternativen.** Der Arbeitsnachweis hat seinen Preis: Das Cambridge Centre for Alternative Finance schätzt den jährlichen Stromverbrauch des Bitcoin-Netzwerks auf rund 170–180 TWh (annualisierte Schätzung, Stand: Anfang 2026) — gut ein halbes Prozent der weltweiten Stromerzeugung und in der Größenordnung des Jahresverbrauchs mittelgroßer Industriestaaten [@ccaf2026]. Dieser Ressourceneinsatz ist kein Nebeneffekt, sondern der Kern des Sicherheitsmodells — genau deshalb ist PoW jedoch umstritten. Als energiesparsame Alternative hat sich Proof of Stake (PoS) etabliert: Statt Rechenleistung hinterlegen Validatoren dort Kapital in Form von Token („Stake“) und werden in Abhängigkeit von ihrem Einsatz zufällig ausgewählt, den nächsten Block zu erzeugen; Fehlverhalten wird durch den Verlust des Einsatzes sanktioniert [vgl. @saleh2020]. Die Erzeugung neuer Einheiten erfolgt hier nicht durch Mining, sondern wird als Minting bezeichnet und ist deutlich weniger rechen- und energieintensiv [vgl. @antonopoulos2018]. Prominentester Vertreter ist Ethereum, das sein Konsensverfahren im September 2022 („Merge“) von PoW auf PoS umgestellt hat [vgl. @wackerow2022; @draht2023]. Der Vergleich beider Verfahren — Sicherheit durch externe Ressourcen (Energie) versus Sicherheit durch internes Kapital — wird in Kapitel 3 und 5 wieder aufgegriffen, da die meisten DeFi-Anwendungen auf PoS-Blockchains laufen.

## 2.5 Aufbau der Bitcoin-Blockchain

Die Struktur der Bitcoin-Blockchain basiert auf kryptografisch gesicherten, chronologisch verknüpften Datenblöcken, die Transaktionen enthalten und eine unveränderliche Aufzeichnung aller jemals stattgefundenen Transaktionen im Netzwerk ermöglichen. Die folgenden Abschnitte erläutern die Schlüsselkomponenten im Detail.

### 2.5.1 Blöcke

Ein Block ist die grundlegende Einheit der Bitcoin-Blockchain und besteht aus drei Hauptelementen:

1. **Blockheader:** Der Blockheader enthält wichtige Metadaten, wie die Version des Blocks, den Zeitstempel, den aktuellen Schwierigkeitsgrad des kryptografischen Rätsels, die Nonce (Abschnitt 2.4) und den Hash des vorherigen Blocks, wodurch die Verkettung der Blöcke entsteht.

2. **Merkle-Root:** Die Merkle-Root ist der Hash-Wert, der aus den Hash-Werten aller im Block enthaltenen Transaktionen erzeugt wird (im Detail in Abschnitt 2.5.3). Dieser Wert wird im Blockheader gespeichert und ermöglicht eine effiziente Überprüfung der Transaktionen innerhalb des Blocks.

3. **Transaktionsliste:** Die Transaktionsliste enthält alle im Block enthaltenen Bitcoin-Transaktionen. Jede Transaktion besteht aus Informationen wie den Eingangs- und Ausgangsadressen, den Beträgen und den kryptografischen Signaturen der Beteiligten.

### 2.5.2 Verkettung der Blöcke

Die Bitcoin-Blockchain erhält ihre Integrität und Unveränderlichkeit durch die Verkettung der Blöcke mittels kryptografischer Hash-Funktionen: Jeder Block enthält den Hash-Wert des vorherigen Blocks in seinem Blockheader, wodurch eine chronologische Kette entsteht.

![Verkettung der Blöcke über den Hash des Vorgängerblocks. Eigene Darstellung. \label{fig:blockkette}](abbildungen/out/blockchain_kette.pdf){ width=95% }

Eine nachträgliche Änderung in einem Block würde dessen Hash-Wert verändern (Avalanche-Effekt, Abschnitt 2.2) — und damit die Verweise aller nachfolgenden Blöcke ungültig machen. Ein Angreifer müsste also nicht nur den betroffenen Block, sondern auch sämtliche darauf folgenden Blöcke neu berechnen, und das schneller, als das ehrliche Netzwerk die Kette verlängert. Die Verkettung macht Manipulationen dadurch nicht unmöglich, aber mit wachsender Tiefe eines Blocks exponentiell aufwendiger — hier greifen Datenstruktur (dieser Abschnitt) und Konsensmechanismus (Abschnitt 2.4) ineinander.

### 2.5.3 Der Merkle-Baum

Innerhalb eines Blocks werden die Transaktionen nicht einzeln im Blockheader referenziert, sondern in einer Baumstruktur zusammengefasst, dem Merkle-Baum. Das Prinzip lässt sich an einem kleinen Beispiel vollständig durchrechnen. Angenommen, ein Block enthält vier Transaktionen:

<!-- Raw-LaTeX statt Pipe-Tabelle: Pandoc setzt Pipe-Tabellen als longtable,
     und longtable rechnet den Seitenumbruch falsch, wenn auf derselben Seite
     ein Float (Abb. 2.4) steht — Text lief in die Fußzeile. -->
```{=latex}
\begin{center}
\begin{tabular}{@{}lll@{}}
\toprule
Transaktion & Inhalt & SHA-256-Wert (gekürzt)\\
\midrule
T1 & Alice zahlt Bob 5 BTC & \texttt{cd3ee612\ldots}\\
T2 & Bob zahlt Carol 2 BTC & \texttt{2521f323\ldots}\\
T3 & Carol zahlt Dave 1 BTC & \texttt{bc9ff84d\ldots}\\
T4 & Dave zahlt Alice 3 BTC & \texttt{1a772b6a\ldots}\\
\bottomrule
\end{tabular}
\end{center}
```

Im ersten Schritt wird jede Transaktion einzeln gehasht (H1 bis H4, die „Blätter“ des Baums). Anschließend werden die Hash-Werte paarweise zusammengefügt und erneut gehasht: Aus H1 und H2 entsteht H12 (`9b63d12d…`), aus H3 und H4 entsteht H34 (`14a0103f…`). Im letzten Schritt werden H12 und H34 zusammengefügt und ein letztes Mal gehasht — das Ergebnis ist die Merkle-Root (`717b1b8f…`), ein einziger Hash-Wert, der sämtliche Transaktionen des Blocks repräsentiert und im Blockheader gespeichert wird (Abbildung \ref{fig:merkle}). Bei mehr Transaktionen wird das Verfahren einfach über mehr Ebenen fortgesetzt; bei ungerader Anzahl wird der letzte Hash-Wert dupliziert. Bitcoin verwendet dabei statt des hier zur Vereinfachung gezeigten einfachen SHA-256 eine doppelte Anwendung der Hash-Funktion; im Beispiel werden zudem die hexadezimalen Darstellungen der Hash-Werte verkettet [vgl. @antonopoulos2014].

![Merkle-Baum mit vier Transaktionen und durchgerechneten (gekürzten) SHA-256-Werten. Hervorgehoben ist der Nachweispfad für T3: Zum Existenznachweis genügen H4 und H12 sowie die Merkle-Root. Eigene Darstellung. \label{fig:merkle}](abbildungen/out/merkle.pdf){ width=93% }

Der Nutzen dieser Konstruktion liegt in drei Eigenschaften:

- **Kompaktheit:** Eine beliebig große Zahl von Transaktionen wird in einem einzigen Hash-Wert zusammengefasst; der Blockheader bleibt dadurch konstant klein.
- **Effiziente Nachweise:** Um zu belegen, dass eine bestimmte Transaktion in einem Block enthalten ist, genügt der Pfad von der Transaktion zur Wurzel. Im Beispiel reicht für den Nachweis von T3 die Kenntnis von H4 und H12: Daraus lassen sich H34 und die Merkle-Root nachrechnen und mit dem Blockheader vergleichen — zwei Hash-Werte statt aller vier Transaktionen, und der Vorteil wächst mit der Blockgröße, da der Aufwand nur logarithmisch mit der Transaktionszahl steigt. Genau darauf beruhen Simplified-Payment-Verification-Clients (SPV): leichtgewichtige Anwendungen wie Smartphone-Wallets, die nur die Blockheader speichern und die Existenz einzelner Transaktionen überprüfen können, ohne die gesamte Blockchain zu laden [vgl. @nakamoto2008].
- **Manipulationssicherheit:** Ändert sich auch nur ein Zeichen einer Transaktion, ändert sich ihr Hash — und kaskadierend alle Werte bis zur Merkle-Root, die dann nicht mehr zum Blockheader passt.

Die Verlässlichkeit des gesamten Verfahrens steht und fällt dabei mit der Kollisionsresistenz der Hash-Funktion (Abschnitt 2.2): Gelänge es einem Angreifer, zwei unterschiedliche Transaktionen mit demselben Hash-Wert zu konstruieren, könnte er eine bestätigte Transaktion unbemerkt gegen eine andere austauschen, ohne dass sich die Merkle-Root ändert — sämtliche Integritätsgarantien wären hinfällig. Die Sicherheit der Blockchain reduziert sich an dieser Stelle vollständig auf die Sicherheit der verwendeten Hash-Funktion; für SHA-256 sind bis heute (Stand: August 2026) keine praktikablen Kollisionsangriffe bekannt [vgl. @stallings2016]. Dass diese Annahme nicht zeitlos gilt, zeigt die Vorgängerfunktion SHA-1, für die 2017 die erste praktische Kollision demonstriert wurde [vgl. @stevens2017].

### 2.5.4 Forks und die längste Kette

In einigen Fällen kann es vorkommen, dass zwei Miner gleichzeitig gültige Blöcke finden und an die Blockchain anhängen. Dies führt zu einer vorübergehenden Abspaltung der Kette, die als Fork bezeichnet wird. In solchen Situationen arbeiten die Miner an derjenigen Kette weiter, die die meiste Proof-of-Work-Anstrengung aufweist — die „längste Kette“. Schließlich wird einer der Zweige länger als der andere, und die Miner, die am kürzeren Zweig gearbeitet haben, wechseln zur längeren Kette. Der kürzere Zweig wird verworfen, und die darin enthaltenen Transaktionen kehren in den Mempool zurück, um in zukünftige Blöcke aufgenommen zu werden. Dieser Mechanismus stellt sicher, dass die Bitcoin-Blockchain eine konsistente und einheitliche Aufzeichnung aller Transaktionen beibehält [vgl. @nakamoto2008; @antonopoulos2014].

## 2.6 Bitcoin und das Vertrauensproblem

Das grundlegende Problem, das ein dezentrales Transaktionssystem wie Bitcoin lösen muss, ist das Vertrauensproblem. In der klassischen Finanzwelt wird dieses Problem durch Intermediäre gelöst.

Bei einer Kreditkartenzahlung übermittelt der Kunde seine Kreditkartendaten (Kreditkartennummer, Gültigkeitsdatum und Kartenprüfnummer) an den Händler. Die Daten werden anschließend zur Autorisierung und Genehmigung an einen sogenannten Kreditkarten-Acquirer weitergeleitet. Acquirer sind Institutionen, die für den Händler die Autorisierung und Abrechnung von Kreditkartenzahlungen abwickeln.

Bei erfolgreicher Autorisierung wird ein Autorisierungscode ausgegeben, der bestätigt, dass das Kreditkartenkonto existiert und belastet werden kann. Der Acquirer bucht anschließend den Betrag vom Kreditkartenkonto des Kunden ab und schreibt ihn, abzüglich des vereinbarten Entgelts (Disagio), dem Händlerkonto gut. Das Disagio setzt sich aus dem — in der EU seit der Verordnung (EU) 2015/751 auf 0,3 % (Kreditkarten) bzw. 0,2 % (Debitkarten) gedeckelten — Interbankenentgelt, den Systementgelten der Kartenorganisationen und der Marge des Acquirers zusammen; es liegt im europäischen Handel typischerweise im niedrigen einstelligen Prozentbereich und variiert nach Branche, Umsatz und Kartenprodukt [vgl. @eu2015interchange].

![Ablauf einer Kreditkartenzahlung mit Intermediären (vereinfacht). Eigene Darstellung in Anlehnung an ibi research [vgl. @ibiresearch2009]. \label{fig:kreditkarte}](abbildungen/out/kreditkarte.pdf){ width=94% }

In der dezentralen Ökonomie übernimmt die Blockchain die Aufgabe, Vertrauen zwischen den Parteien herzustellen, um Transaktionen ohne Intermediäre wie Banken oder Kreditkarteninstitute zu vollziehen. Eine solche Transaktion läuft wie folgt ab: Zunächst erstellt ein Benutzer mithilfe seines Wallets eine Transaktion, um Bitcoin an eine andere Bitcoin-Adresse zu senden. Das Wallet signiert diese Transaktion mit dem privaten Schlüssel des Senders (Abschnitt 2.2). Anschließend wird die Transaktion über das Netzwerk verbreitet; die Knoten validieren sie unabhängig (Abschnitt 2.3.1). Miner nehmen die Transaktion in einen Block auf und suchen per Proof of Work nach einer gültigen Lösung (Abschnitt 2.4). Wird sie gefunden, prüfen die übrigen Knoten den Block und bauen auf ihm auf — sie drücken damit ihre Zustimmung aus. Nachdem mehrere weitere Blöcke angehängt wurden — üblich ist die Konvention von sechs Bestätigungen —, gilt die Transaktion als endgültig bestätigt [vgl. @antonopoulos2014, S. 34–35].

Obwohl die Bitcoin-Blockchain als Pionier für dezentrale Finanztransaktionen diente, sind ihre Anwendungsmöglichkeiten aufgrund der eingeschränkten Programmierbarkeit begrenzt. Bitcoins integrierte Skriptsprache kann nur einfache Bedingungen wie zeitverzögerte Transaktionen abbilden; sie kennt insbesondere keine Schleifen oder allgemeinen Kontrollstrukturen. Um komplexere Szenarien umzusetzen, ist eine Turing-vollständige Programmiersprache erforderlich — also eine Sprache, die (abgesehen von Ressourcengrenzen) jede berechenbare Funktion ausdrücken kann [vgl. @turing1937; @grincalaitis2019]. Wie eine Blockchain mit einer solchen Sprache kombiniert werden kann und welche neuen Anwendungen daraus entstehen, zeigt der folgende Abschnitt.

## 2.7 Smart Contracts

### 2.7.1 Einführung {#smart-contracts-einfuehrung}

Vitalik Buterin — Mitgründer des Fachmagazins Bitcoin Magazine (2011) und Autor des Ethereum-Whitepapers — erkannte frühzeitig das Potenzial einer Turing-vollständigen Skriptsprache in Verbindung mit einer Blockchain. Den ersten Entwurf des Whitepapers „Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform“ veröffentlichte er im November 2013; die im Literaturverzeichnis geführte kanonische Fassung datiert auf 2014 [vgl. @buterin2014]. Auf dieser Grundlage entstand die Ethereum-Blockchain: eine Plattform, die die Blockchain-Technologie mit einer Turing-vollständigen Programmierumgebung kombiniert und bis heute das führende Ökosystem für dezentrale Finanzanwendungen ist — auf Ethereum entfallen rund 55 % des gesamten in DeFi-Protokollen gebundenen Kapitals (Stand: 02.08.2026) [@defillama2026chains] (Kapitel 3). Die zugehörige native Kryptowährung Ether (ETH) ist das Gegenstück zu Bitcoin auf der Bitcoin-Blockchain: Sie dient als Zahlungsmittel und wird darüber hinaus benötigt, um die Ausführung von Smart Contracts zu bezahlen, insbesondere wenn diese schreibende, zustandsändernde Operationen beinhalten.

Das Konzept, auf dem Ethereum aufbaut, ist älter als die Blockchain selbst: Nick Szabo prägte bereits 1994 den Begriff der „Smart Contracts“ — in digitaler Form spezifizierte Versprechen samt der Protokolle, in denen die Parteien diese Versprechen erfüllen [vgl. @szabo1994]. Die heute übliche Zusatzeigenschaft — automatische, nach Bereitstellung nicht mehr änderbare Ausführung — kam erst mit der Blockchain als Ausführungsumgebung hinzu. Smart Contracts sind digitale, sich selbst ausführende Verträge, die nicht auf zentralen Servern, sondern auf einer Blockchain liegen und dort ausgeführt werden [vgl. @fill2020]. Die Software-Entwicklung erfolgt bei Ethereum über die eigens dafür entwickelte, Turing-vollständige Programmiersprache Solidity. Transaktionen auf der Ethereum-Blockchain lassen sich im Grunde mit denen der Bitcoin-Blockchain vergleichen — sie enthalten jedoch nicht nur den Transfer einer virtuellen Währung, sondern können zusätzlich Vertragsbedingungen formal erfassen, die ohne den Einfluss Dritter ausgeführt und durchgesetzt werden. Dabei kann es sich beispielsweise um den Verkauf virtueller Güter oder die Erfassung und Übertragung des Eigentums virtuell abgebildeter realer Güter handeln. In der Regel erfolgt der Transfer automatisch anhand vordefinierter Bedingungen, die im Smart Contract festgelegt sind [vgl. @fill2020].

Durch Smart Contracts können komplexe Abläufe modelliert werden, die auf Zustände und Zustandsänderungen der Blockchain reagieren. Ein Beispiel ist die Ausgabe und Verwaltung eigener Token unter vordefinierten Bedingungen. Eine weitere Einsatzmöglichkeit ist die Programmierung dezentraler Anwendungen (dApps), die beispielsweise traditionelle Finanzdienstleistungen auf der Blockchain anbieten und automatisiert ausführen können [vgl. @fill2020].

### 2.7.2 Token: Klassifikation und Standards

Token sind digitale Einheiten, die mithilfe von Smart Contracts erstellt werden, um Werte oder Rechte abzubilden — etwa Unternehmensanteile, Besitzverhältnisse, Nutzungsrechte oder digitale Identitäten [vgl. @fill2020]. Ein Coin ist demgegenüber die digitale Geldeinheit einer Kryptowährung: Alle Coins sind Token, aber nicht alle Token sind Coins, da Token über den reinen Werttransfer hinaus zusätzliche Rechte abbilden können [vgl. @fill2020].

Gemäß Oliveira et al. (2018) lassen sich Token in drei Klassen einteilen [vgl. @oliveira2018]:

**Payment Token** wie Bitcoin dienen ausschließlich als Tauschmittel für dezentrale Transaktionen im Zahlungsverkehr.

**Security Token** sind digitale Wertpapiere, die als Investitionsverträge oder Vermögenswerte fungieren und ihren Besitzern bestimmte Rechte gewähren — etwa Stimmrechte bei Unternehmensentscheidungen oder Ansprüche auf zukünftige Gewinne. Sie repräsentieren traditionelle Finanzinstrumente auf einer dezentralen Plattform.

**Utility Token** sind mit einer digitalen Dienstleistung auf der Blockchain verbunden und beschreiben Mitglieds- und Mitwirkungsrechte in einem Protokoll oder Ökosystem. Sie ermöglichen es Benutzern, bestimmte Dienstleistungen innerhalb des Ökosystems zu erwerben oder zu nutzen, und können auch als Belohnung für Beiträge zum Netzwerk dienen [vgl. @oliveira2018].

Neben dieser Klassifikation lassen sich Token nach technischen Standards untergliedern; die Ethereum-Standards tragen die Bezeichnung ERC (Ethereum Request for Comments) nach dem Verfahren, in dem sie vorgeschlagen werden. Als Basis dienen hier die Standards der für DeFi-Applikationen meistgenutzten Blockchain Ethereum (rund 55 % des DeFi-TVL, Stand: 02.08.2026 [@defillama2026chains]) [vgl. @diangelo2020].

Auf Ethereum abgebildete Coins, Payment Token und Utility Token verwenden in der Regel den **ERC-20**-Standard, der die Erstellung und Verwaltung fungibler Token vereinheitlicht und vereinfacht [vgl. @fill2020]. Er ist der am häufigsten eingesetzte Standard und bildet einfache Funktionalitäten wie den Token-Transfer auf Ethereum-kompatiblen Blockchains ab.

Der **ERC-721** Non-Fungible Token Standard beschreibt Token, die einzigartig und voneinander unterscheidbar sind. Dieser Standard ermöglicht die Nachverfolgung unterscheidbarer Vermögenswerte; Eigentumsverhältnisse an individuellen Assets wie Kunstwerken, Grundstücken oder Immobilien lassen sich damit eindeutig abbilden [vgl. @diangelo2020].

Der **ERC-777**-Standard (2017) baut auf ERC-20 auf und führt Callback-Funktionen („Hooks“) ein, mit denen Sender und Empfänger automatisiert auf Transfers reagieren können — etwa um Transaktionen bestimmter Adressen abzulehnen; das zweistufige Freigabeverfahren von ERC-20 entfällt dadurch [vgl. @dafflon2015]. Diese Hooks erwiesen sich in der Praxis jedoch als Angriffsfläche: Über den Empfänger-Hook des ERC-777-Tokens imBTC wurden im April 2020 ein Uniswap-V1-Pool und die Kreditplattform Lendf.me (Verlust rund 25 Mio. US-Dollar) per Reentrancy angegriffen [vgl. @zhou2023sok]; der Standard hat sich deshalb nicht auf breiter Front durchgesetzt.

Der **ERC-1155** Multi Token Standard kombiniert ERC-20 und ERC-721: Fungible und nicht-fungible Token können in einem einzigen Smart Contract verwaltet und mehrere Tokenarten mit einer Transaktion transferiert werden [vgl. @diangelo2020]. Während bei ERC-20 und ERC-721 jeder Erwerb in einer einzelnen Transaktion abgebildet wird, erlaubt ERC-1155 das Bündeln von Elementen: Der Tausch von zehn Assets gegen zehn andere benötigt nicht 20 Transaktionen, sondern zwei. Dies entlastet das Netzwerk und steigert die Effizienz [vgl. @radomski2018].

### 2.7.3 Beispiel eines Smart Contracts

Als Beispiel dient ein Smart Contract im E-Commerce-Bereich in Verbindung mit einem Logistikunternehmen: Wenn ein Endverbraucher Ware bei einem Verkäufer bestellt, liefert dieser die Ware an das Logistikunternehmen. Auf den ersten Blick unterscheiden sich diese Schritte nicht von einem konventionellen Geschäftsprozess. Der Unterschied besteht in einer vertraglichen Vereinbarung, die die Zahlung des Kaufpreises an den Verkäufer erst freigibt, sobald der Paketdienstleister die Ware ausgeliefert hat. Der Vorteil für den Endkunden: Er muss das Geld nicht im Voraus überweisen und geht kein Vorleistungsrisiko ein. Der Händler wiederum erhält das Geld sicher und unmittelbar nach der Lieferung. Heute wird dieses Risiko häufig durch einen zusätzlichen Zahlungsdienstleister abgedeckt, der sich diese Absicherung bezahlen lässt; durch Smart Contracts entfällt dieser Kostenfaktor [vgl. @rauscher2018].

![Ablauf eines Smart Contracts im E-Commerce: Treuhand ohne zusätzlichen Zahlungsdienstleister. Eigene Darstellung. \label{fig:smartcontract}](abbildungen/out/smart_contract.pdf){ width=93% }

**Zwischenfazit.** Für die weitere Untersuchung sind aus diesem Kapitel drei Eigenschaften zentral: Erstens entsteht Vertrauen in Blockchains nicht durch einen Intermediär, sondern durch unabhängige Validierung und ein ökonomisches Anreizsystem — das ist der Referenzpunkt für Merkmal M1 (Intermediärfunktion) des in Abschnitt 1.3 eingeführten Analyserasters. Zweitens sind die Sicherheitsgarantien eng umgrenzt und kostenbasiert, nicht absolut — darauf baut die Risikoanalyse (M5) in den Kapiteln 4 und 5 auf. Drittens machen Smart Contracts aus einer reinen Zahlungsinfrastruktur eine Programmierplattform — die technische Voraussetzung dafür, dass sich klassische Finanzdienstleistungen ohne Intermediär abbilden lassen. Kapitel 3 setzt genau hier an.

<!-- Aufgelöstes Glossar 2.7 des Originals: Mining, PoW, Hash-Funktion, SHA-256, Gesamthashrate, PoS,
     Minting, Ether, Merkle Tree, Token, Coin und P2P sind in die Abschnitte 2.1, 2.2, 2.4, 2.5.3 und 2.7
     integriert. Oracle sowie Layer 1/Layer 2 werden im Anhang-Glossar geführt (kapitel/90-glossar.md),
     bis Kapitel 3 sie bei Erstnennung einführt. Zitierweise: vollständig auf [vgl. @key] umgestellt. -->
