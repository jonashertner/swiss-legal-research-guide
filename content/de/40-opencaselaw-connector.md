---
chapter: V
slug: opencaselaw-connector
title: "Anhang: OpenCaseLaw in Claude als Connector hinzufügen"
short_title: Connector
order: 40
description: "Schritt-für-Schritt-Anleitung, um OpenCaseLaw über die MCP-Schnittstelle direkt an Claude anzubinden — und damit Schweizer Erlasse und Entscheide in natürlicher Sprache zu durchsuchen."
---

*[[OpenCaseLaw|opencaselaw.ch]] als Connector in Claude einrichten.* Die Datenbank opencaselaw.ch lässt sich über eine sogenannte [[MCP]]-Schnittstelle (Model Context Protocol) direkt an Claude anschliessen. Damit kann direkt in Claude in natürlicher Sprache auf Schweizer Gerichtsentscheide und Erlasse zugegriffen werden, ohne dass die Plattform separat aufgerufen werden muss. Die Einrichtung erfolgt in wenigen Schritten und erfordert keine technischen Vorkenntnisse. Weitere Informationen finden Sie hier: <https://opencaselaw.ch/mcp/>. Bitte beachten Sie, dass Claude und OpenCaseLaw stetig weiterentwickelt werden, sodass sich die Oberfläche und genauen Schritte ändern können.

## Schritt 1: Claude öffnen

Rufen Sie <https://claude.ai> im Browser auf und melden Sie sich mit Ihrem Konto an. Die Einrichtung funktioniert auch auf dem kostenlosen Claude-Account.

## Schritt 2: Einstellungen öffnen

Klicken Sie in der linken Seitenleiste unten auf Ihr Profil und wählen Sie «Einstellungen».

## Schritt 3: Custom Connector hinzufügen

Klicken Sie auf «Konnektoren» und dann unten auf «Benutzerdefinierten Connector hinzufügen».

## Schritt 4: Verbindungsdaten eingeben

Es öffnet sich ein Dialogfeld mit zwei Feldern. Geben Sie die folgenden Daten ein:

- **Name:** OpenCaseLaw (oder ein beliebiger Name)
- **Remote MCP Server URL:** <https://mcp.opencaselaw.ch>

Erweiterte Einstellungen sind für OpenCaseLaw nicht erforderlich, da der Server keine Authentifizierung verlangt. Klicken Sie auf «Hinzufügen».

## Schritt 5: Konnektor aktivieren

Der Konnektor erscheint nun in Ihrer Konnektoren-Liste. Um ihn in einer Chat-Konversation zu verwenden, klicken Sie im Chatbot auf die «+»-Schaltfläche unten links im Chatfenster und wählen Sie «Konnektoren». Dort können Sie OpenCaseLaw für die aktuelle Konversation aktivieren.

## Schritt 6: Testen

Stellen Sie eine Frage, die eine Suche in der Datenbank auslöst, beispielsweise: «*Suche mir aktuelle Bundesgerichtsentscheide zum Thema Verhältnismässigkeit bei Tierhalteverboten.*» Wenn die Einrichtung erfolgreich war, greift Claude direkt auf die Datenbank zu und liefert Entscheide mit Aktenzeichen und Kurzzusammenfassung. Beim ersten Aufruf eines Tools fragt Claude um Erlaubnis, ob das Tool verwendet werden darf. Sie können die Nutzung einzeln bestätigen oder dauerhaft erlauben.

*Hinweis.* Dieselbe Einrichtung funktioniert auch in der Claude Desktop-App und in Claude Cowork. In der mobilen App (iOS/Android) können bereits eingerichtete Konnektoren verwendet, aber keine neuen hinzugefügt werden.

## Schritt 7: Funktionen

OpenCaseLaw umfasst verschiedene Tools, die für spezifische Rechercheanwendungsfälle optimiert sind. Sie können via Prompt aktiviert werden.

**23 Tools im Überblick** — jedes Tool ist für einen spezifischen Rechercheanwendungsfall optimiert. Volle Schemas via MCP-Protokoll-Tools-Liste, hier gruppiert nach Funktion:

| Gruppe | Tools |
| :--- | :--- |
| **Entscheide suchen & abrufen** | `search_decisions` · `get_decision` · `get_case_brief` · `list_courts` · `get_statistics` |
| **Doktrin & Studium** | `get_doctrine` · `get_commentary` · `search_commentaries` · `generate_exam_question` · `draft_mock_decision` |
| **Zitationsgraph** | `find_citations` · `find_appeal_chain` · `find_leading_cases` · `analyze_legal_trend` |
| **Gesetzestext** | `get_law` · `search_laws` · `get_legislation` · `search_legislation` · `browse_legislation_changes` |

\* \* \*
