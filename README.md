# finanzfluss-sparplan-import

This script is intended for the German finance tracking tool [Finanzfluss Copilot](https://www.finanzfluss.de/user/). Therefore, the following text is written in German to facilitate understanding.

Mit diesem Tool kannst du Sparplan-Transaktionen automatisiert in den Finanzfluss Copilot einfügen, ohne jede Transaktion manuell eintragen zu müssen.

## Anwendungsfälle

- lange Sparplanhistorien
- keine API Schnittstelle zwischen Broker und Finanzfluss vorhanden
- keine API Schnittstelle zwischen Broker und Finanzfluss gewollt (Datenschutz)
- etc.

## Motivation

Als ich meinen Account eingerichtet habe, wollte ich mein Depot einpflegen, das meine Eltern während meiner Kindheit bespart haben. Das Depot war bei einer altmodischen Bank, und Finanzfluss bot keine Schnittstelle an. Daher habe ich dieses Skript geschrieben, um meine Transaktionen über die Wealth API zu importieren.

## Funktionen

- Anpassbare Sparplanintervalle (z.B. jeden Monat, jedes halbe Jahr)
- Anpassbares Ausführungsdatum (z.B. fünfter Tag des Monats)
- Berücksichtigt Wochenenden (https://github.com/timonrieger/finanzfluss-sparplan-import/issues/1)
- Berechnet die gekaufte Stückzahl basierend auf Sparrate und Asset-Preis zu dem Datum
- Kein Direktzugriff auf deinen Copilot-Account
- Logischerweise werden keine Daten irgendwo gespeichert
- Sehr anfängerfreundlich mit Video und keiner extra Software außer Python (natürlich auch mit git clone und einer IDE nutzbar)

## Einschränkungen

- Einfache Transaktionshistorien (Sparplan)
- Nur Kauforders
- Keine Transaktionsgebühren
- Keine Garantie auf Fehlerfreiheit
- Unterstützt nur Monatsintervalle, keine wöchentlichen Sparpläne

## Python installieren

Die einzige Voraussetzung ist der Download von Python. Wähle eine stabile Version zwischen 3.10 und 3.12. Achte auf das richtige Betriebssystem! [Windows](https://www.python.org/downloads/windows/), [Linux/UNIX](https://www.python.org/downloads/source/), [macOS](https://www.python.org/downloads/macos/), [Andere](https://www.python.org/download/other/)

## Ausführliche Erklärung (Youtube Video)

Hier wird ein Sparplan simuliert, der alle zwei Monate am achten Tag des Monats vom 1. April 2010 bis heute mit 100€ auf der ISIN DE0008476524 ausgeführt wird.

[![Watch the video](https://img.youtube.com/vi/e5dApx6lFcs/maxresdefault.jpg)](https://youtu.be/e5dApx6lFcs)
### Code-Befehle aus dem Video

1. Erstelle eine virtuelle Umgebung
```bash
python -m venv .venv
```
2. Aktiviere die virtuelle Umgebung
- For Mac:
```bash
source .venv/bin/activate
```
- For Windows:
```bash
.venv\Scripts\activate
```
3. Installiere die Code-Abhängigkeiten, die das Skript zur Ausführung braucht
```bash
pip install -r requirements.txt
```
4. Führe das Skript aus
```bash
python -m main
```

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die [LICENSE](LICENSE) Datei für Details.
