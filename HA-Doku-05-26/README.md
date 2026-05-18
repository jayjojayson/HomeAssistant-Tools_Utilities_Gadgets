# Home Assistant Dokumentation als PDF erstellen

Dieses Projekt erstellt ein vollständiges PDF der offiziellen Home Assistant Dokumentation direkt aus dem GitHub-Repository.

## Voraussetzungen

### Systemanforderungen

- **macOS** (getestet), Linux oder Windows
- **Python 3.10+**
- **Git** (zum Klonen des Repositories)
- **Homebrew** (macOS, für Systembibliotheken)

### Benötigte Pakete

#### 1. Systembibliotheken (macOS)

WeasyPrint benötigt einige C-Bibliotheken. Unter macOS mit Homebrew installieren:

```bash
brew install glib pango gobject-introspection
```

#### 2. Python-Pakete

Es wird empfohlen, eine virtuelle Umgebung zu verwenden:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install weasyprint markdown
```

Benötigte Pakete im Detail:

| Paket | Zweck |
|-------|-------|
| `weasyprint` | HTML/CSS zu PDF Konvertierung |
| `markdown` | Markdown zu HTML Konvertierung |

## Installation und Ausführung

### Schritt-für-Schritt

```bash
# 1. Repository klonen oder Skript herunterladen
git clone <dein-repo>
cd <projekt-verzeichnis>

# 2. Virtuelle Umgebung erstellen und aktivieren
python3 -m venv .venv
source .venv/bin/activate

# 3. Abhängigkeiten installieren
pip install weasyprint markdown

# 4. Skript ausführen
python3 create_ha_pdf.py
```

### Was passiert beim Ausführen?

1. **Repository klonen** – Das offizielle Home Assistant Doku-Repository wird von GitHub geklont (`home-assistant.io`)
2. **Dateien finden** – Alle Markdown-Dateien aus den Dokumentationsverzeichnissen werden gesammelt
3. **Liquid-Tags verarbeiten** – Jekyll-spezifische Tags werden in sauberes Markdown konvertiert:
   - `{% example %}` → YAML Code-Blöcke
   - `{% details %}` → HTML Details/Summary
   - `{% include %}` → Inhalt wird eingebettet
   - `{% tip %}`, `{% note %}`, `{% warning %}` → Blockquotes
   - `{% configuration %}` → Tabellen
   - `{% my %}`, `{% term %}`, `{% icon %}` → Text-Ersetzungen
4. **Markdown kombinieren** – Alle Dateien werden zu einer einzigen Markdown-Datei zusammengeführt
5. **PDF erstellen** – Über Markdown → HTML → PDF mit WeasyPrint

## Verarbeitete Liquid-Tags

Das Skript konvertiert folgende Jekyll Liquid-Tags:

| Tag | Konvertierung |
|-----|---------------|
| `{% example %}...{% endexample %}` | Code-Block mit YAML-Syntax-Highlighting |
| `{% details "Titel" %}...{% enddetails %}` | HTML `<details>` Block (aufklappbar) |
| `{% include file.md %}` | Inhalt der Datei wird eingebettet |
| `{% tip %}...{% endtip %}` | Blockquote mit "💡 Tip:" Prefix |
| `{% note %}...{% endnote %}` | Blockquote mit "📝 Note:" Prefix |
| `{% important %}...{% endimportant %}` | Blockquote mit "⚠️ Important:" Prefix |
| `{% caution %}...{% endcaution %}` | Blockquote mit "🔶 Caution:" Prefix |
| `{% warning %}...{% endwarning %}` | Blockquote mit "🚨 Warning:" Prefix |
| `{% labs %}...{% endlabs %}` | Blockquote mit "🧪 Labs:" Prefix |
| `{% configuration %}...{% endconfiguration %}` | Markdown-Tabelle mit Optionen |
| `{% configuration_basic %}...{% endconfiguration_basic %}` | Einfache Markdown-Tabelle |
| `{% my integration title="..." %}` | Titel-Text |
| `{% term xyz %}` | Term-Text |
| `{% icon "mdi:xyz" %}` | Icon-Name als Code |
| `{% if %}...{% endif %}` | Wird entfernt (kein Kontext) |
| `{% for %}...{% endfor %}` | Wird entfernt (kein Kontext) |
| `{% assign ... %}` | Wird entfernt |

## Verarbeitete Verzeichnisse

Folgende Verzeichnisse werden in das PDF aufgenommen:

- `source/_docs` – Kerndokumentation
- `source/_includes` – Wiederverwendbare Inhalte
- `source/_actions` – Aktionen
- `source/_conditions` – Bedingungen
- `source/_triggers` – Trigger
- `source/_dashboards` – Dashboard-Dokumentation
- `source/_template_functions` – Template-Funktionen
- `source/installation` – Installationsanleitungen
- `source/getting-started` – Einstiegshilfen
- `source/common-tasks` – Häufige Aufgaben
- `source/dashboards` – Dashboards
- `source/voice_control` – Sprachsteuerung
- `source/faq` – FAQ
- `source/help` – Hilfe
- `source/cloud` – Nabu Casa Cloud
- `source/android` – Android App
- `source/ios` – iOS App
- `source/apps` – Apps
- `source/actions` – Aktionen
- `source/conditions` – Bedingungen
- `source/triggers` – Trigger
- `source/template-functions` – Template-Funktionen
- `source/more-info` – More-Info Seiten
- `source/developers` – Entwickler-Dokumentation
- `source/blueprints` – Blueprints

## Ausgeschlossene Verzeichnisse

Folgende Verzeichnisse werden **nicht** aufgenommen:

- Blog-Posts (`source/_posts`, `source/blog`)
- Integrationsbeschreibungen (`source/_integrations`, `source/integrations`)
- Bilder, Assets, Stylesheets, JavaScript
- Produktseiten (Green, Yellow, Voice PE, Connect)
- Changelogs, Konferenzen, Community-Seiten
- Rechtliches (Privacy, TOS, Security)

## Ausgabe

Das Skript erzeugt zwei Dateien:

| Datei | Beschreibung |
|-------|--------------|
| `combined_documentation.md` | Kombinierte Markdown-Datei (~5 MB) |
| `Home-Assistant-Dokumentation.pdf` | Fertiges PDF (~11 MB, ~2700 Seiten) |

## Bekannte Einschränkungen

1. **Dynamische Inhalte** – `{% if %}` und `{% for %}` Blöcke werden entfernt, da sie ohne Jekyll-Kontext nicht ausgewertet werden können
2. **Bilder** – Externe Bilder werden nicht heruntergeladen, nur lokale Referenzen bleiben erhalten
3. **Videos** – YouTube-Einbettungen werden nicht konvertiert
4. **Links** – Interne Links zeigen auf die Online-Dokumentation, nicht auf PDF-Anker
5. **Integrationen** – Die ~2000+ Integrationsbeschreibungen sind nicht enthalten (würde das PDF zu groß machen)

## Lizenz

Die Home Assistant Dokumentation ist unter **CC BY-NC-SA 3.0** lizenziert. Das erstellte PDF unterliegt denselben Lizenzbedingungen.

Quelle: https://github.com/home-assistant/home-assistant.io
