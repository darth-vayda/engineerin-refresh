# Vibration Monitor

Ein Python-Projekt zur automatisierten Verarbeitung und Analyse von Beschleunigungsdaten. Als Versuchsobjekt dient ein mehrstufiger Ventilator; die Vibrationen werden mit dem Beschleunigungssensor eines Smartphones (Samsung Galaxy S20+ 5G) und der App [phyphox](https://phyphox.org/) aufgezeichnet.

Das Projekt dient dazu, meine praktische Erfahrung mit Python, Sensordaten, Signalverarbeitung und Git anhand eines realen Messproblems zu aktualisieren. Der aktuelle Stand bildet eine vollständige Pipeline vom ZIP-Export bis zum visualisierten Frequenzspektrum ab. Als nächster Schritt sollen charakteristische Frequenzmerkmale der Betriebsstufen automatisch extrahiert und verglichen werden.

## Versuchsaufbau

Das Smartphone wird ohne Schutzhülle mit dem Clip des Ventilators fest eingeklemmt. Dadurch werden die mechanischen Schwingungen auf das Smartphone und dessen Beschleunigungssensor übertragen. Aufgezeichnet wird die lineare Beschleunigung ohne Erdbeschleunigung in x-, y- und z-Richtung.

![Ventilator und Smartphone im Versuchsaufbau](Versuchsaufbau%20(3).jpg)

Untersucht werden fünf Zustände (`level0` bis `level4`) mit jeweils zehn unabhängigen Messungen. `level0` beschreibt den ausgeschalteten Ventilator und dient als Referenz.

Die aktuelle Messreihe umfasst:

- 50 Messungen in zehn Durchgängen
- ungefähr 100 Samples pro Sekunde
- drei Beschleunigungsachsen
- einen stabilen Auswertebereich von 5 bis 30 Sekunden
- eine maximal darstellbare Frequenz von ungefähr 50 Hz gemäß Nyquist-Grenze

Der Aufbau ist bewusst einfach gehalten. Die Messungen sind daher nicht als kalibrierte Zustandsüberwachung zu verstehen, sondern als reproduzierbarer Datensatz für die Entwicklung und Erprobung der Softwarepipeline.

### Messprotokoll

Ein Durchgang besteht aus je einer Messung aller fünf Zustände. Während eines Durchgangs bleiben Smartphone, Einspannung und Untergrund unverändert. Zwischen zwei Durchgängen wird das Smartphone vollständig herausgenommen und neu eingespannt; außerdem wird die phyphox-Messung neu gestartet. Damit entstehen zehn voneinander unabhängige Einspannungen und zehn Messungen pro Zustand.

Um Einflüsse durch Erwärmung, Akkuzustand oder Messzeit nicht systematisch mit einer bestimmten Lüfterstufe zu verknüpfen, wird die Reihenfolge der Zustände zwischen den Durchgängen ausbalanciert:

Der Akkustand des lüfters war zwischen 84% und 78%; Der des Handys zwischen 74% und 58%. Die gesamten Messungen wurden in einem Zeitraum von 3 Stunden aufgenommen.

| Durchgang | Reihenfolge der Zustände |
|---:|---|
| 1 | 0 → 1 → 2 → 3 → 4 |
| 2 | 1 → 2 → 3 → 4 → 0 |
| 3 | 2 → 3 → 4 → 0 → 1 |
| 4 | 3 → 4 → 0 → 1 → 2 |
| 5 | 4 → 0 → 1 → 2 → 3 |
| 6 | 4 → 3 → 2 → 1 → 0 |
| 7 | 3 → 2 → 1 → 0 → 4 |
| 8 | 2 → 1 → 0 → 4 → 3 |
| 9 | 1 → 0 → 4 → 3 → 2 |
| 10 | 0 → 4 → 3 → 2 → 1 |

Die Hauptmessungen finden auf einem Schreibtisch statt. Zusätzliche Durchgänge auf dem Boden und auf einem Fensterbrett werden als gesonderte Robustheitsmessungen gekennzeichnet. Der Untergrund wird innerhalb eines Durchgangs nicht verändert und gemeinsam mit der Session dokumentiert.

Für alle Aufnahmen gelten dieselben Einstellungen und dieselbe Messdauer. Zusätzlich werden Durchgang, Reihenfolge, Untergrund und besondere Abweichungen notiert. Die Dateinamen enthalten mindestens Zustand, Wiederholung und Session, beispielsweise:

```text
fan_level3_v04_session07_surface_desk
```

Bei der späteren Modellbewertung werden vollständige Sessions zusammengehalten. Messungen desselben Durchgangs dürfen nicht gleichzeitig in Trainings- und Testdaten vorkommen, da dies zu einer zu optimistischen Bewertung führen könnte.

## Verarbeitungspipeline

```text
phyphox-ZIP-Dateien
        ↓
CSV-Daten aus den Archiven einlesen
        ↓
stabilen Zeitabschnitt auswählen
        ↓
Gleichanteil der x-, y- und z-Achse entfernen
        ↓
Hann-Fenster anwenden
        ↓
einseitige FFT berechnen und amplitudenrichtig skalieren
        ↓
Zeit- und Frequenzdaten visualisieren
```

### 1. Datenimport

Alle ZIP-Dateien im Ordner `data/` werden automatisch gefunden. Aus jedem Archiv wird `Raw Data.csv` direkt eingelesen, ohne das Archiv vorher manuell entpacken zu müssen. Die Messungen werden als Dictionary aus Messungsname und pandas-DataFrame organisiert.

### 2. Auswahl des Zeitfensters

Start- und Stoppvorgänge können das Frequenzspektrum stark beeinflussen. Deshalb wird aus jeder Messung momentan der Bereich zwischen 5 und 30 Sekunden gewählt, in dem der Ventilator möglichst stationär läuft.

### 3. Entfernung des Gleichanteils

Von jeder Beschleunigungsachse wird ihr Mittelwert abgezogen. Dadurch liegen die Achsen um null und ein konstanter Offset dominiert nicht den Frequenzanteil bei 0 Hz.

### 4. Frequenzanalyse

Vor der FFT wird ein Hann-Fenster angewendet, um Spektralleckage an den Rändern des gewählten Zeitausschnitts zu reduzieren. Anschließend wird mit `numpy.fft.rfft` das einseitige Spektrum eines reellen Signals berechnet. Die Amplituden werden über die Summe des Fensters normiert und – mit Ausnahme von Gleichanteil und gegebenenfalls Nyquist-Bin – verdoppelt.

### Features
1. Gesamt-RMS im Zeitbereich
Berechne pro Messung einen gemeinsamen RMS-Wert über alle drei zentrierten Achsen:
\[
a_\mathrm{RMS} =
\sqrt{\operatorname{mean}(x^2+y^2+z^2)}
\]


### 5. Visualisierung

Für jede Messung werden die Spektren der drei Beschleunigungsachsen in einer gemeinsamen Abbildung dargestellt und als PNG im Ordner `results/` gespeichert.

## Projektstruktur

```text
vibration-monitor/
├── data/                    # phyphox-ZIP-Dateien (nicht in Git enthalten)
├── results/                 # erzeugte Grafiken (nicht in Git enthalten)
├── src/
│   ├── io_clem.py           # Datenimport und Auswahl einzelner Messungen
│   ├── signal_processing.py # Zeitfenster, DC-Korrektur und FFT
│   ├── plotting.py          # Visualisierung und Export der Grafiken
│   └── main.py              # Orchestrierung der Verarbeitungsschritte
├── tests/                   # automatisierte Tests (in Vorbereitung)
└── readme.md
```

## Installation

Vorausgesetzt werden Python 3.10 oder neuer und Git.

Repository klonen und in den Projektordner wechseln:

```powershell
git clone <URL-DES-REPOSITORY>
cd vibration-monitor
```

Virtuelle Umgebung erstellen und aktivieren:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Benötigte Bibliotheken installieren:

```powershell
python -m pip install -r requirements.txt
```

## Datenformat

Die Messdaten werden als phyphox-ZIP-Archive im Ordner `data/` abgelegt. Jedes Archiv muss eine Datei namens `Raw Data.csv` enthalten. Erwartet werden mindestens folgende Spalten:

```text
Time (s)
Linear Acceleration x (m/s^2)
Linear Acceleration y (m/s^2)
Linear Acceleration z (m/s^2)
```

Die aktuelle Dateibenennung folgt diesem Schema:

```text
fan_level<stufe>_v<wiederholung>
```

Beispiel:

```text
fan_level3_v02
```

Die Rohdaten sind wegen ihrer Größe und ihres lokalen Ursprungs nicht Teil des Repositorys.

## Ausführung

Das Programm wird aus dem Projektverzeichnis als Python-Modul gestartet:

```powershell
python -m src.main
```

Der aktuelle Ablauf in `main.py`:

1. lädt alle Messungen aus `data/`,
2. wählt den Bereich von 5 bis 30 Sekunden,
3. entfernt den Gleichanteil der drei Achsen,
4. berechnet die Frequenzspektren und
5. speichert die Grafiken in `results/`.

## Aktueller Stand und nächste Schritte

Bereits umgesetzt:

- automatischer Import mehrerer ZIP-Archive
- strukturierte Ablage der Messungen in DataFrames
- Auswahl stationärer Zeitbereiche
- Entfernung des Gleichanteils
- Hann-Fensterung
- normierte einseitige FFT für drei Achsen
- automatisierte Erstellung und Speicherung der Diagramme
- modulare Trennung von Datenimport, Signalverarbeitung und Darstellung

Geplante Weiterentwicklung:

- automatisierte Tests mit synthetischen Signalen
- Erkennung dominanter Frequenzspitzen
- Vergleich der Spektren zwischen Ventilatorstufen und Wiederholungsmessungen
- Extraktion geeigneter Merkmale, beispielsweise RMS-Wert, Peak-Frequenz und Energie in Frequenzbändern
- robuste Erkennung von Betriebszuständen und später von gezielt eingebrachten Systemveränderungen
- Erweiterung der Dokumentation um Ergebnisgrafiken und Interpretation

## Einordnung

Dieses Repository ist ein Lern- und Demonstrationsprojekt. Es zeigt den Aufbau einer nachvollziehbaren Sensordatenpipeline und wird schrittweise um Tests, Merkmalsextraktion und Zustandsklassifikation erweitert. Die Ergebnisse hängen vom Smartphone, seiner Sensorabtastrate, der mechanischen Kopplung und der Reproduzierbarkeit des Versuchsaufbaus ab.
