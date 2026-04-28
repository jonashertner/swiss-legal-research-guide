---
chapter: II
slug: erlasse
title: Suchen, Lesen und Analysieren von Erlassen
short_title: Erlasse
order: 10
description: "Erlasse finden, ihren typischen Aufbau verstehen und sie mit Blick auf eine konkrete Rechtsfrage zielorientiert lesen — mit und ohne KI."
---

**Weiterführende Literatur:** Forstmoser Peter / Ogorek Regina / Schindler Benjamin, *Juristisches Arbeiten, eine Anleitung für Studierende*, 7. Aufl., Zürich 2023, § 10; Reimer Franz, *Juristische Methodenlehre*, 2. Aufl., Baden-Baden 2020, Rz. 157 ff.; Wyss Martin / Kummer Franz / Häcki Rafael, *Suchen — Finden — Überzeugen, Arbeitstechniken im juristischen Alltag*, 2. Aufl., Bern 2013, S. 19 ff.; Bundesamt für Justiz, *Gesetzgebungsleitfaden*, 5. Aufl., Bern 2025.

## Suchen von Erlassen

*Was sind [[Erlass|Erlasse]]?* Unter einem Erlass versteht man eine Mehrheit *generell-abstrakter* Rechtsnormen des geschriebenen Rechts, die von einem Gemeinwesen verabschiedet, in Kraft gesetzt und publiziert worden sind. Eine generell-abstrakte Rechtsnorm regelt für eine unbestimmte Vielzahl von Personen (generell) eine unbestimmte Anzahl von Sachverhalten (abstrakt). Durch ihren generell-abstrakten Charakter unterscheiden sich Erlasse von der individuell-konkreten [[Verfügung]] und dem gerichtlichen Urteil.[^1] Zudem sind sie einerseits von privat gesetzten Rechtsnormen abzugrenzen, andererseits von staatlichen Rechtsnormen, die noch nicht oder nicht mehr in Kraft sind. Erlasse existieren sodann in unterschiedlichen Formen, namentlich als Verfassung, Gesetz und Verordnung. In der Schweiz als Bundesstaat ist ferner zwischen den Erlassen verschiedener Gemeinwesen — Bund, Kantonen und Gemeinden — zu unterscheiden. Daneben enthalten rechtsetzende Verträge zwischen Gemeinwesen Rechtsnormen. Sie werden als interkantonale oder ‑kommunale Verträge, Konkordate respektive völkerrechtliche Verträge (zwischen Staaten) bezeichnet.

*Wie sind Erlasse publiziert?* Erlasse gelten erst und nur dann, wenn sie korrekt veröffentlicht wurden.[^2] Geheimrecht ist unvereinbar mit dem Legalitätsprinzip. Neue oder geänderte Erlasse des Bundes werden laufend und chronologisch in der [Amtlichen Sammlung des Bundesrechts](https://www.fedlex.admin.ch/de/cc) ([[AS]]) publiziert. Die Kantone kennen ähnliche Sammlungen. Zudem werden Erlasse des Bundes in ihrer jeweils gültigen Fassung in der [Systematischen Sammlung des Bundesrechts](https://www.fedlex.admin.ch/de/cc) ([[SR]]) nach Sachgebieten geordnet wiedergegeben. In den Kantonen existieren analoge Sammlungen. Die Systematische Sammlung des Bundes und aller Kantone sind heute online abrufbar. Kommunale Erlasse und rechtsetzende Verträge sind teilweise nur in gedruckter Form verfügbar.

*Wie findet man Erlasse?* Geltende Erlasse findet man am besten online über die Systematische Sammlung des Bundes, des fraglichen Kantons und seinen Gemeinden. [Lex-find.ch](https://www.lexfind.ch/) (ein Projekt im Auftrag der schweizerischen Staatsschreiberkonferenz) bietet eine nützliche Suchmaske, um alle geltenden Erlasse von Bund und Kantonen zu durchsuchen. Wo Erlasse bloss in gedruckter Form existieren, ist man auf Kopien angewiesen, die bisweilen von kantonalen Staatskanzleien zur Verfügung gestellt werden können. Andernfalls ist noch immer (und hoffentlich nicht mehr lange) der Gang ins entsprechende Archiv erforderlich.

*Erlasssuche mittels KI.* Eine Rechtsfrage ist häufig in unterschiedlichen Erlassen (Verfassung, Gesetz, Verordnung) verschiedener Gemeinwesen (Bund, Kanton, Gemeinde) geregelt. So finden sich bspw. Regeln zum Bauen auf kommunaler Stufe in Bau- und Zonenordnungen und in Kanton und Bund in Bau- und Raumplanungsgesetzen und den dazugehörigen Verordnungen.[^3] Das Zusammentragen der verschiedenen Erlasse für einen konkreten Fall ist traditionell zeitaufwändig, weil mühsame Handarbeit. Die KI-unterstützte Erlasssuche eröffnet hier neue Möglichkeiten, indem sie einzelne Schritte dieser Arbeit automatisiert. Verschiedene (kommerzielle) LegalTech-Anbieter bieten solche Suchen an. Es existieren aber auch kostenlose Angebote, die unseres Erachtens mindestens so leistungsstark sind. Namentlich lässt sich die frei zugängliche Datenbank [opencaselaw.ch](https://opencaselaw.ch/) über eine sogenannte [[MCP]]-Schnittstelle direkt an KI-Anwendungen wie Claude anschliessen. Dadurch können Erlasse von Bund und Kantonen in natürlicher Sprache ge- und durchsucht werden (zur Anleitung für die Einrichtung dieser Schnittstelle unten [Kapitel V](../opencaselaw-connector/)). Für die Erlasse des Bundes existiert die Alternative [Fedlex-Connector](https://www.fedlex.admin.ch/), die — ähnlich wie OpenCaseLaw — an Claude angeschlossen werden kann. Tools zur KI-unterstützten Suche werden zwar immer besser, eine Kontrolle anhand der Originalerlasse bleibt jedoch unverzichtbar (dazu auch unten [Kapitel IV](../ki-konzepte/)). Eine isolierte Lektüre von Rechtsnormen vermittelt auch mit KI zu oft ein unvollständiges Bild. Das «Suchlesen» in den einschlägigen Erlassen bleibt oft aufschlussreich und kann mithilfe von KI nur bedingt vereinfacht werden.

| Prompts zur Inspiration |
| :--- |
| ‣ *Welche Voraussetzungen stellt das Bundesrecht und das kantonale Recht Graubündens an die Einschläferung eines gewalttätigen Hundes?* |
| ‣ *Welche Unterschiede und Gemeinsamkeiten bestehen in Bund und Kantonen hinsichtlich der Regelung der Abwahl und Abberufung von Regierungsräten? Bilde Gruppen.* |
| ‣ *Erkläre unter Angaben der massgeblichen Artikel die Regelung des Fristbeginns in [[ZPO]],[^4] [[StPO]],[^5] [[VwVG]][^6] und [[BGG]][^7]?* |

## Aufbau von Erlassen

*Wie sind Erlasse aufgebaut?* In einem Erlass kodifizierte Rechtsnormen können prinzipiell beliebig gegliedert werden. Durchgesetzt hat sich ein typischer Aufbau, den das Bundesamt für Justiz wie folgt beschreibt:[^8]

| Abschnitt | Inhalte |
| :--- | :--- |
| **Einleitung** | Ziel/Zweck · Geltungsbereich · Begriffsbestimmungen |
| **Hauptteil** (innerhalb des Hauptteils wird vorwiegend nach sachlichen Gliederungskriterien strukturiert) | Organisation · Verfahren · Finanzierung · Kosten · Gebühren · Strafbestimmungen |
| **Schlussbestimmungen** | Vollzug · Aufhebung und Änderung anderer Erlasse · Übergangsrecht · Referendum · Inkrafttreten |

Vor allem die Gliederung des Hauptteils von Erlassen richtet sich nach dem spezifischen Regelungsgegenstand, weshalb nur bedingt verallgemeinerbare Aussagen zur näheren Gliederung möglich sind.[^9]

## Lesen und Analysieren von Erlassen

*Wie liest man Erlasse?* Erlasse zählen — wie auch Gerichtsentscheide[^10] — zur Gattung juristischer Texte. Ähnlich wie ein Gedicht (Schönheit), eine Tageszeitung (Information) oder ein Krimi (Unterhaltung) werden auch Erlasse mit einem bestimmten Fokus gelesen.

*Zielorientierte Rechtsnormsuche.* In der Regel liest man Erlasse mit Blick auf eine konkrete Rechtsfrage. Sie formt das Ziel der Lektüre erheblich. In der Regel sind dafür unterschiedliche Erlasse (Verfassung, Gesetz, Verordnung) verschiedener Gemeinwesen (Bund, Kanton, Gemeinde) in Betracht zu ziehen und einander zuzuordnen. Diese Abstimmungs- oder Koordinationsarbeit ist Interpretationsarbeit.[^11]

*Akteurorientiertes Lesen von Erlassen.* Das Lesen von Erlassen erfolgt üblicherweise in einer bestimmten Rolle, welche die Lektüre entscheidend mitbestimmt. Ein Gericht liest denselben Erlass — zum Beispiel ein Verfahrensgesetz — anders als eine Partei, diese wiederum anders als der Gesetzgeber oder die Verwaltung.

*Zielorientierte Erlasslektüre.* Rechtsnormsuche und Erlasslektüre bleiben ein wechselseitiger Prozess: Eine zielorientierte Rechtsnormsuche setzt voraus, dass man eine Rechtsnorm im Kontext ihrer Erlasse liest. Ein Erlass wird meist mit Fokus auf bestimmte Rechtsnormen oder Rechtsnormgruppen gelesen.

*Wie analysiert man Erlasse?* Ähnlich wie bei Gerichts- und Verwaltungsentscheiden stellen sich auch bei der Erlassanalyse typische Grundfragen, die sich mithilfe von KI-Tools beantworten lassen. Sie können auch als Musterprompts verwendet werden. Unter anderem durch folgende Prompts:

| Prompts zur Inspiration |
| :--- |
| ‣ *Auf welchen Bundeskompetenzen beruht ein Bundesgesetz und inwiefern belässt es Raum für kantonale Rechtsetzung?* |
| ‣ *Der Erfüllung welcher Staatsaufgaben dient der Erlass?* |
| ‣ *Was sind Ziel und Zweck des Erlasses und inwiefern werden sie genauer geregelt?* |
| ‣ *Wie ist der sachliche, räumliche und zeitliche Geltungsbereich des Erlasses geregelt?* |
| ‣ *Wie regelt der Erlass Vollzug und Rechtsschutz?* |
| ‣ *Existieren intertemporalrechtliche Vorschriften und, wenn ja, welche?* |

[^1]: Vgl. z. B. Forstmoser Peter / Ogorek Regina / Schindler Benjamin, *Juristisches Arbeiten, eine Anleitung für Studierende*, 7. Aufl., Zürich 2023, S. 215 ff.
[^2]: Vgl. für den Bund: Art. 8 Abs. 1 des Bundesgesetzes vom 18. Juni 2004 über die Sammlungen des Bundesrechts und das Bundesblatt ([[PublG]]; SR 170.512).
[^3]: Für den Bund: Bundesgesetz über die Raumplanung ([[RPG]]; SR 700) und Raumplanungsverordnung (RPV; SR 700.1).
[^4]: Schweizerische Zivilprozessordnung vom 19. Dezember 2008 (ZPO; SR 272).
[^5]: Schweizerische Strafprozessordnung vom 5. Oktober 2007 (StPO; SR 312.0).
[^6]: Bundesgesetz vom 20.12.1968 über das Verwaltungsverfahren (VwVG; SR 172.021).
[^7]: Bundesgesetz über das Bundesgericht vom 17. Juni 2005 (BGG; SR 173.110).
[^8]: Die folgende Tabelle ist entnommen aus Bundesamt für Justiz, *Gesetzgebungsleitfaden*, 5. Aufl., Bern 2025, Rz. 602.
[^9]: Bundesamt für Justiz, *Gesetzgebungsleitfaden*, 5. Aufl., Bern 2025, Rz. 602 ff.
[^10]: Vgl. dazu unten [Kapitel III.3](../gerichtsentscheide/#lesen-von-gerichtsentscheiden).
[^11]: Ehrenzeller Kaspar, in: Ehrenzeller Bernhard / Egli Patricia / Hettich Peter / Hongler Peter / Schindler Benjamin / Schmid Stefan G. / Schweizer Rainer J. (Hrsg.), *Die schweizerische Bundesverfassung*, 4. Aufl., Zürich/St. Gallen 2023, *Verfassungsinterpretation*, Rz. 105 ff.
