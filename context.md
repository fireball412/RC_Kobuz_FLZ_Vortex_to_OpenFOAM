# Projektkontext Kobuz von FLZ Vortex zu OpenFOAM

Stand: 11. Oktober 2026. Diese Datei fasst das Projekt für Menschen und KI-Assistenten zusammen. Sie ermöglicht die Fortsetzung ohne Zugriff auf den ursprünglichen Chat. Maßgeblich für eine Rechnung sind die tatsächlichen OpenFOAM-Eingabedateien; die Zahlen unten beschreiben den dokumentierten Ausgangsfall.

## Inhaltsverzeichnis

- [1 Projekt und bisheriger Ablauf](#projekt)
- [2 Einstieg für einen neuen KI-Assistenten](#einstieg)
- [3 Ordnerstruktur und Dateibeschreibungen](#dateien)
- [4 Klonen und Nachrechnen](#nachrechnen)
- [5 Geometrie und Koordinatensystem](#geometrie)
- [6 Strömung und Anstellwinkel](#stroemung)
- [7 Netz und numerische Einstellungen](#netz)
- [8 Referenzergebnisse und Grenzen](#ergebnisse)
- [9 Fortschritt und ParaView](#darstellung)
- [10 Varianten und nächste Schritte](#fortsetzung)
- [11 Dokumentation weiterführen](#dokumentation)

<a id="projekt"></a>
## 1 Projekt und bisheriger Ablauf

Repository: https://github.com/fireball412/RC_Kobuz_FLZ_Vortex_to_OpenFOAM

Ziel ist die Untersuchung eines Kobuz-Modellflugzeugs aus einer vorhandenen FLZ_VORTEX-Auslegung. Die Geometrie wurde aus `kobuz.flz` in ein parametrisches Fusion-360-Modell überführt, als STL exportiert, geprüft und mit OpenFOAM berechnet. ParaView stellt Druckverteilung und Randwirbel dar. Die deutsche Anleitung ist für einen Beitrag in RC-Network erstellt worden.

Die CAD-Erstellung und die Einrichtung der Rechnung erfolgten mit KI-Unterstützung. Fusion wurde über eine MCP-Schnittstelle und die Fusion-API gesteuert. Der Nutzer musste die Rechenbefehle nicht selbst eingeben. Die Schnittstelle ist jedoch keine Voraussetzung zum Nachrechnen des bereitgestellten Falls und wird nicht durch dieses Repository installiert.

Der ursprüngliche Flügel bestand aus sechs soliden Loft-Segmenten. Ein Export ohne Vereinigung erzeugte doppelte innere Flächen. Die Segmente wurden deshalb im CAD zu einem Flügelkörper vereinigt. Höhen- und Seitenleitwerk wurden anschließend ergänzt. Das vollständige Modell hat drei solide Körper und 41 Benutzerparameter.

Das veröffentlichte Modell enthält Flügel und Leitwerke, aber keinen Rumpf. Ein später im Chat erwähnter Rumpfentwurf sowie spätere Formenbau- und Leitwerksänderungen sind in diesem Datenstand nicht enthalten. Dieser Fall ist eine stationäre CFD-Untersuchung, keine FEM-Strukturberechnung.

<a id="einstieg"></a>
## 2 Einstieg für einen neuen KI-Assistenten

1. Diese Datei und [die vollständige Anleitung](Anleitung_Kobuz_OpenFOAM.md) lesen.
2. Mit `git status --short` vorhandene Nutzeränderungen feststellen und erhalten.
3. Zuerst die tatsächlichen Dateien `0/U`, `system/controlDict`, `system/fvSolution` und `system/snappyHexMeshDict` unter `Kobuz_Beispiel/Kobuz` prüfen. Referenzzahlen nicht ungeprüft auf einen geänderten Fall übertragen.
4. Arbeitsziel unterscheiden: Dokumentation bearbeiten, CAD verändern, Referenzfall reproduzieren oder einen neuen Betriebspunkt untersuchen.
5. Neue Rechnungen in einer eigenen Fallkopie durchführen. Die veröffentlichten Referenzergebnisse dienen als Vergleich und sollen nicht mit neuen Ergebnissen vermischt werden.
6. Vor einem Solverlauf Geometrie, Maßeinheit und Netz prüfen. Nach dem Lauf Residuen, Kräfteverlauf und yPlus beurteilen.

Die vollständigen erzeugten Felder, das Volumennetz und die ursprünglichen CAD-Erstellungsskripte sind nicht im Repository enthalten. Das CAD-Archiv bewahrt die Modellhistorie; die STL und die OpenFOAM-Dictionaries reichen zum Wiederaufbau des Rechenfalls. Die Bilder sind keine ladbaren Strömungsdaten.

<a id="dateien"></a>
## 3 Ordnerstruktur und Dateibeschreibungen

```text
.
├── context.md
├── .gitattributes
├── Anleitung_Kobuz_OpenFOAM.md
├── Anleitung_Kobuz_OpenFOAM.pdf
├── 00_Fusion_Modell.png
├── 01_Druckverteilung.png
├── 02_Randwirbel.png
├── 03_Konvergenz.png
├── 04_FLZ_Ausgangsmodell.png
└── Kobuz_Beispiel/
    ├── LIESMICH.txt
    ├── CAD/
    │   ├── kobuz.flz
    │   └── Kobuz_Fluegel_und_Leitwerke.f3d
    ├── Kobuz/
    │   ├── 0/                    U p k omega nut
    │   ├── constant/
    │   │   ├── geometry/kobuz.stl
    │   │   ├── physicalProperties
    │   │   └── momentumTransport
    │   ├── system/               acht Dictionaries
    │   ├── run.sh
    │   ├── solve.sh
    │   ├── Auswertung.py
    │   ├── Create_Vortex_View.py
    │   ├── progress_server.py
    │   ├── progress.html
    │   └── Kobuz.foam
    └── Referenzergebnisse/
        ├── Results.json
        ├── Force_History.csv
        ├── log.foamRun
        ├── log.checkMesh
        ├── Kobuz_Complete_Surface_Check.txt
        └── Kobuz_Complete_Repair_Details.json
```

Alle Pfade in den folgenden Tabellen sind relativ zur Repository-Wurzel.

### Dokumentation und Bilder

| Datei | Bedeutung |
| --- | --- |
| `context.md` | Diese Übergabedokumentation für das Fortsetzen des Projekts. |
| `.gitattributes` | Automatische Erkennung von Textdateien und LF-Normalisierung durch Git. Die Arbeitskopie kann abhängig von der Git-Konfiguration trotzdem CRLF enthalten. |
| `Anleitung_Kobuz_OpenFOAM.md` | Bearbeitbarer deutscher Beitrag mit Installation, CAD-Aufbau, STL-Prüfung, Rechnung und Auswertung. |
| `Anleitung_Kobuz_OpenFOAM.pdf` | Gesetzte Fassung der Anleitung; beim Erstellen dieser Kontextdatei 15 Seiten. |
| `00_Fusion_Modell.png` | Ursprüngliches vollständiges Fusion-Modell mit Flügel und Leitwerken. |
| `01_Druckverteilung.png` | Berechneter Relativdruck in Pascal auf den Körperoberflächen. |
| `02_Randwirbel.png` | Q-Isosurface des Nachlaufs, eingefärbt nach Wirbelstärke. |
| `03_Konvergenz.png` | Entwicklung von CL und CD im ursprünglichen Rechenlauf. |
| `04_FLZ_Ausgangsmodell.png` | Originaler FLZ_VORTEX-Screenshot; in der Anleitung beim Modellaufbau vor der Fusion-Ansicht eingefügt. |
| `Kobuz_Beispiel/LIESMICH.txt` | Kurzanleitung zum Beispiel. Die Pfadangaben zum Entpacken beziehen sich auf die frühere ZIP-Verteilung; bei einem Git-Clone die Struktur oben verwenden. |

### CAD und Geometrie

| Datei | Bedeutung |
| --- | --- |
| `Kobuz_Beispiel/CAD/kobuz.flz` | Originale Auslegung einschließlich eingebetteter Profilkoordinaten. Textdatei, für die damalige Verarbeitung als Windows-1252 gelesen. Nennt Stefan als Konstrukteur. |
| `Kobuz_Beispiel/CAD/Kobuz_Fluegel_und_Leitwerke.f3d` | Parametrisches Fusion-Archiv des ursprünglichen vollständigen Modells. In Fusion öffnen, um die Geometrie weiterzubearbeiten. |
| `Kobuz_Beispiel/Kobuz/constant/geometry/kobuz.stl` | Abschließend bereinigte, geschlossene CFD-Oberfläche in **Metern**, mit drei getrennten Körpern und 22 668 Dreiecken. Bereits skaliert; nicht nochmals mit 0,001 multiplizieren. |

### Anfangsfelder und Materialmodell

Die nachstehenden Pfade liegen unter `Kobuz_Beispiel/Kobuz/`.

| Datei | Bedeutung |
| --- | --- |
| `0/U` | Geschwindigkeit einschließlich Anströmrichtung und Randbedingungen. |
| `0/p` | Kinematischer Druck mit Referenzwert null am Austritt. |
| `0/k` | Turbulente kinetische Energie und ihre Randbedingungen. |
| `0/omega` | Spezifische turbulente Dissipationsrate und ihre Randbedingungen. |
| `0/nut` | Turbulente kinematische Viskosität einschließlich Wandfunktion. |
| `constant/physicalProperties` | Konstante kinematische Viskosität der Luft. |
| `constant/momentumTransport` | Stationäres RAS-Turbulenzmodell `kOmegaSST`. |

### Dictionaries und Skripte

Auch diese Pfade liegen unter `Kobuz_Beispiel/Kobuz/`.

| Datei | Bedeutung |
| --- | --- |
| `system/blockMeshDict` | Außenbereich, Hintergrundnetz und äußere Patches. |
| `system/surfaceFeaturesDict` | Extraktion scharfer Geometriekanten. |
| `system/snappyHexMeshDict` | Oberflächenanpassung, Verfeinerungsboxen, Fluid-Auswahlpunkt und Wandschichten. |
| `system/meshQualityDict` | Qualitätsgrenzen; bindet zusätzlich die Foundation-Vorgaben ein. |
| `system/decomposeParDict` | Zerlegung des Netzes für vier MPI-Prozesse. |
| `system/fvSchemes` | Diskretisierungsverfahren und stationäre Zeitableitung. |
| `system/fvSolution` | Lineare Solver, SIMPLE-Verfahren, Relaxation und Residuenkriterien. |
| `system/controlDict` | Solver-Modul, Schreibintervalle, Iterationsgrenze sowie `forceCoeffs` und yPlus. |
| `run.sh` | Erzeugt das Netz, prüft `Mesh OK`, rechnet auf vier Prozessen und rekonstruiert den letzten Stand. |
| `solve.sh` | Rechnet mit einem bereits vorhandenen Netz und rekonstruiert den letzten Stand. Erzeugt und prüft selbst kein Netz. Mit der vorhandenen Steuerung wird ab Startzeit 0 gerechnet; es ist kein automatisches Fortsetzen der letzten Iteration. |
| `Auswertung.py` | Liest die aktuelle `postProcessing/coefficients/*/forceCoeffs.dat`, berechnet Kräfte und äquivalente Gleitwerte und schreibt `Aktuell_Ergebnisse.json` sowie `Aktuell_Kraftverlauf.csv`. Benötigt nur Python-Standardbibliothek. |
| `Create_Vortex_View.py` | Liest die neu berechneten Felder, berechnet Vorticity und Q, erzeugt `Kobuz_Vortices.pvsm` und `Kobuz_Vortices.png`. Benötigt `pvpython` aus ParaView. |
| `progress_server.py` | Lokaler Fortschrittsserver auf `127.0.0.1:8766`, liest Stufe, Logs und zuletzt ausgegebene Beiwerte. |
| `progress.html` | Browseroberfläche für den Fortschrittsserver. |
| `Kobuz.foam` | Absichtlich leere Datei, über die ParaView den Fall erkennt. |

### Gespeicherte Referenzergebnisse

Diese Dateien liegen unter `Kobuz_Beispiel/Referenzergebnisse/` und gehören zum ursprünglichen Betriebspunkt.

| Datei | Bedeutung |
| --- | --- |
| `Results.json` | Numerische Zusammenfassung der ersten konvergierten Rechnung. |
| `Force_History.csv` | Verlauf von Iteration, Cm, CD, CL und den zusätzlich ausgegebenen CL-Anteilen. |
| `log.foamRun` | Solverprotokoll mit Residuen, Kontinuitätsfehlern, Beiwerthistorie und Konvergenzmeldung. |
| `log.checkMesh` | Abschließende Topologie- und Qualitätsprüfung des ursprünglichen Netzes. |
| `Kobuz_Complete_Surface_Check.txt` | Abschließende Prüfung der bereinigten STL: geschlossen, drei getrennte Teile, keine gemeldete Selbstüberschneidung. |
| `Kobuz_Complete_Repair_Details.json` | Bericht zur numerischen STL-Bereinigung und zur maximalen Punktverschiebung. |

<a id="nachrechnen"></a>
## 4 Klonen und Nachrechnen

### Voraussetzungen

Verwendet wurden Windows mit WSL 2, Ubuntu 24.04 LTS, **OpenFOAM Foundation 14** und ParaView 5.11.2. Die Installationsschritte stehen in der Anleitung. Andere OpenFOAM-Ausgaben sind nicht automatisch kompatibel. Dieser Fall verwendet `foamRun` mit `incompressibleFluid`, nicht den älteren Aufruf `simpleFoam`.

Unter Ubuntu müssen Git, OpenFOAM, dessen MPI-Umgebung, Python 3 und für die Darstellung ParaView verfügbar sein. Die KI sollte das zuerst durch verfügbare Programme und Versionsausgaben prüfen. Ein früherer Versuch auf dem älteren Rechner mit Ubuntu 26.04 scheiterte an `Illegal instruction`; die dokumentierte Kombination mit Ubuntu 24.04 funktionierte.

### Beispiel eines frischen Nachbaus in Ubuntu oder WSL

```bash
mkdir -p ~/Kobuz-Projekt
cd ~/Kobuz-Projekt
git -c core.autocrlf=input clone \
  https://github.com/fireball412/RC_Kobuz_FLZ_Vortex_to_OpenFOAM.git
cd RC_Kobuz_FLZ_Vortex_to_OpenFOAM
git status --short
git rev-parse HEAD

source /opt/openfoam14/etc/bashrc
foamRun -help

mkdir -p ~/OpenFOAM/Kobuz-Laeufe
cp -a Kobuz_Beispiel/Kobuz ~/OpenFOAM/Kobuz-Laeufe/referenz-01
cd ~/OpenFOAM/Kobuz-Laeufe/referenz-01

# Besonders bei einer unter Windows ausgecheckten Vorlage:
sed -i 's/\r$//' run.sh solve.sh

surfaceCheck -checkSelfIntersection constant/geometry/kobuz.stl
bash run.sh
python3 Auswertung.py
```

Zielordner müssen neu sein. Bei bereits vorhandenen Verzeichnissen einen anderen Laufnamen wählen, statt alte Ergebnisse unbemerkt zu überschreiben. Beim Klonen wird keine OpenFOAM-Installation und keine Fusion-Schnittstelle eingerichtet. Der Betrieb im Linux-Dateisystem ist für viele kleine Dateien meist zweckmäßig; eine Kopie von `/mnt/c/...` funktioniert ebenfalls.

`run.sh` schreibt seine Ausgabe in `log.*` und den aktuellen Arbeitsschritt in `stage.txt`. Das Skript ist an vier Prozesse angepasst. Eine Änderung der Prozesszahl erfordert die gleiche Zahl in `system/decomposeParDict` und im MPI-Aufruf.

Neu erzeugt werden unter anderem `constant/polyMesh/`, Kantendateien, `processor0/` bis `processor3/`, numerische Zeitordner, `postProcessing/`, `stage.txt`, `log.*` und die Auswertedateien. Diese Daten sind nicht Bestandteil der ursprünglichen Eingabevorlage. Das Repository enthält derzeit keine `.gitignore`; große Laufdaten deshalb in der separaten Arbeitskopie belassen oder bei einer späteren Repository-Erweiterung bewusst behandeln.

<a id="geometrie"></a>
## 5 Geometrie und Koordinatensystem

- X zeigt von der Nasenleiste zur Endleiste und weiter zum Leitwerk.
- Y verläuft entlang der Spannweite; Z zeigt nach oben.
- Ursprung: Nasenleiste in der Hauptflügelmitte.
- Projizierte Spannweite: ungefähr 2,55963 m.
- Hauptflügel: je Seite 60 mm mit null Grad V-Form, danach zweimal 610 mm mit einem Grad V-Form. Tiefen 255, 255, 180 und 105 mm an Mitte und Stationen.
- Originalprofile: `MH-30mod_PK`, `MHSD-3003mod_PK`, `SD7003mod_PK`. Die modifizierten eingebetteten Koordinaten übernehmen, nicht nur ähnlich benannte Standardprofile.
- Höhenleitwerk: Position (0,720; 0; 0) m, Spannweite 0,570 m, Tiefen 0,140 und 0,100 m, HD800, Einstellwinkel minus ein Grad.
- Seitenleitwerk: Position (0,650; 0; 0,020) m, Höhe 0,230 m, Tiefen 0,220 und 0,140 m, NACA0012.

Die Profilstationen des Hauptflügels wurden als gerade Loft-Übergänge mit vertikalen Schnittebenen und ebenen Spitzenabschlüssen aufgebaut. Das vollständige CAD-Modell bewahrt diese Konstruktion. Die genaue Spline-Interpolation ist relevant; Tabellenmaße allein bestimmen nicht jede Oberflächeneinzelheit.

Die STL wurde von Millimeterzahlen in Meter umgerechnet, mit hoher Präzision geschrieben und numerisch bereinigt. Elf Vertices wurden minimal verschoben, maximal etwa 8,15 Nanometer. Das beseitigte Schnittmeldungen an gemeinsamen Punkten oder Kanten innerhalb der Exportpräzision. Diese konkrete Maßnahme ist kein allgemeines Verfahren zum Reparieren echter Löcher oder CAD-Überlappungen. Neue Geometrie immer erneut prüfen.

<a id="stroemung"></a>
## 6 Strömung und Anstellwinkel

| Größe | Referenzeinstellung |
| --- | --- |
| Geschwindigkeit V | 15,72207 m/s |
| Anstellwinkel alpha | 4,03997 Grad |
| Schiebewinkel | 0 Grad |
| Anströmvektor U | (15,6830029333; 0; 1,1076570217) m/s |
| Luftdichte für Kraftauswertung | 1,225 kg/m³ |
| Kinematische Viskosität | 0,000015 m²/s |
| Turbulenzmodell | Stationäres RAS mit kOmegaSST |
| Eintrittsturbulenz | Intensität 0,5 Prozent, Längenskala 0,02 m |
| Bezugsfläche Aref | 0,4698 m², nur die Hauptflügelfläche |
| Bezugslänge lRef | 0,194623243934 m |
| Momentenbezugspunkt CofR | (0,07636; 0; 0) m |
| Nickmomentachse | (0; 1; 0) |

**Der Anstellwinkel wird über die Anströmung modelliert, nicht durch Drehen des CAD-Modells.** Es gilt `Ux = V*cos(alpha)` und `Uz = V*sin(alpha)`. Winkel für die trigonometrische Berechnung in Radiant umrechnen. Der positive Z-Anteil bedeutet eine Anströmung leicht von unten gegen den Hauptflügel. Das Höhenleitwerk besitzt zusätzlich seinen geometrischen Einstellwinkel; der örtliche wirksame Winkel hängt auch vom Abwind ab.

Die Kräfteauswertung in `controlDict` verwendet:

```text
dragDir ( 0.9975151448  0  0.0704523655);
liftDir (-0.0704523655  0  0.9975151448);
```

Widerstand wird parallel zur Anströmung, Auftrieb senkrecht dazu bestimmt. Die Patchgruppe `aircraft` umfasst alle drei Körper. Obwohl Leitwerkskräfte mitintegriert werden, ist die Normierungsfläche ausschließlich die Hauptflügelfläche.

U verwendet einen festen Eintritt, `inletOutlet` am Austritt, Fernfeldbedingungen auf den übrigen äußeren Grenzen und `noSlip` an den Körpern. p ist **kinematischer Druck in m²/s²**. Für die Druckabbildung in Pascal wurde `1.225*p` verwendet. Das ist Relativdruck, kein absoluter Umgebungsdruck. `freestreamPressure` enthält in diesem Fall sowohl `freestreamValue` als auch `value`; der erste Eintrag darf nicht beim Übertragen verloren gehen.

<a id="netz"></a>
## 7 Netz und numerische Einstellungen

- Außenbereich: X von minus 2 bis plus 6 m, Y von minus 4 bis plus 4 m, Z von minus 3 bis plus 3 m.
- Hintergrundnetz: 50 mal 50 mal 38 Zellen.
- Oberflächenverfeinerung: Stufen 4 bis 5; scharfe Kanten: Stufe 5.
- Körpernahe Box: Stufe 3; Nachlaufbox: Stufe 2.
- Gewünschte Wandschichten: fünf mit Wachstumsfaktor 1,2; relative Schichtdicke.
- `insidePoint` liegt im äußeren Fluidbereich. Im Inneren der soliden Körper soll nicht gerechnet werden.
- Endgültiges ursprüngliches Netz: 884 609 Zellen, größte Nichtorthogonalität etwa 62,32 Grad, größte Skewness etwa 3,957.
- Prüfung: `checkMesh -allTopology -meshQuality`, Abschluss `Mesh OK`.

Ein erster Netzversuch war auffällig. Unter anderem wurden `minFaceWeight` auf 0,05 und `maxBoundarySkewness` auf 4 gesetzt und das Netz neu erzeugt. `Mesh OK` gilt für die tatsächlich verwendeten Prüfungen und Grenzwerte. Es ist kein Nachweis der Netzunabhängigkeit; erweiterte Diagnosen hatten auch konkave Zellen ausgewiesen.

Die Rechnung ist stationär. `Time = 193s` ist hier ein Iterationsstand mit der vorgegebenen Schrittweite, keine simulierte Flugzeit von 193 Sekunden. Die Obergrenze beträgt 400 Iterationen. Die SIMPLE-Residuenkriterien sind p kleiner als 1e-6, U kleiner als 1e-5 und k sowie omega kleiner als 1e-6. Der ursprüngliche Lauf konvergierte nach 193 Iterationen.

<a id="ergebnisse"></a>
## 8 Referenzergebnisse und Grenzen

| Größe | Dokumentierter Endstand |
| --- | --- |
| CL | 0,53648326969 |
| CD | 0,035608632632 |
| Cm | minus 0,012245785752 |
| Auftrieb | 38,1588 N |
| Widerstand | 2,53276 N |
| Nickmoment | minus 0,169520 Nm |
| L zu D | 15,0661 |
| Äquivalenter Gleitwinkel | 3,79739 Grad |
| Äquivalentes Sinken | 1,04125 m/s |

Der gezeigte FLZ-Stand ergab eine Gleitzahl von 24,9564, einen Gleitwinkel von 2,29461 Grad und ein Sinken von 0,62998 m/s. In FLZ war Profil-Blasenwiderstand aktiviert; Rumpf- und Interferenzwiderstand waren null. Die CFD verwendet eine andere Widerstandsmodellierung. Der FLZ-Auftriebsbeiwert darf ohne Prüfung seines Flächenbezugs nicht direkt mit dem CFD-CL gleichgesetzt werden.

Die CFD-Ergebnisse sind ein konvergierter einzelner Betriebspunkt, **keine abgesicherte Flugleistung des kompletten Flugzeugs**:

- Der Rumpf fehlt.
- Bei der aus FLZ abgeleiteten Masse von 3,97 kg beträgt die Gewichtskraft etwa 38,9457 N; Gewichtsbalance und Trimmung sind noch nicht hergestellt. Das Nickmoment ist nicht null.
- Eine Polare, beste Gleitzahl, geringstes Sinken und maximale Auftriebszahl sind noch nicht bestimmt.
- yPlus streut ungefähr von 0,95 bis 164 bei einem Mittel von 14,6. Die wandnahe Auflösung ist für belastbaren Reibungswiderstand zu verbessern.
- Das Modell ist vollständig turbulent und enthält keine eigens berechnete laminar-turbulente Transition. Die mittlere Reynolds-Zahl liegt etwa bei 204 000.
- Netz- und Außenbereichsunabhängigkeit sind noch nicht untersucht.
- Das FLZ-`vs` bezeichnet hier Sinken, nicht Stallgeschwindigkeit.

Die abgeleiteten Gleitwerte beruhen auf `E = CL/CD`, `gamma = atan(CD/CL)` und `vs = V*sin(gamma)`. Erst bei passender Gewichtsbalance und Trimmung wären sie stationäre Gleitflugwerte. Kleine Änderungen der Beiwerte am Laufende belegen numerische Stabilisierung, nicht die Genauigkeit des physikalischen Modells.

<a id="darstellung"></a>
## 9 Fortschritt und ParaView

In einem zweiten Terminal den laufenden Fall öffnen und je nach Stufe beobachten:

```bash
cat stage.txt
tail -f log.snappyHexMesh
# Nach Beginn des Solvers:
tail -f log.foamRun
```

Strg+C beendet bei `tail -f` die Logansicht. Optional in einem weiteren Terminal `python3 progress_server.py` starten und `http://127.0.0.1:8766` öffnen. Dieser Server läuft nur lokal; die Browseroberfläche benötigt ihn. Bei belegtem Port einen passenden freien Port verwenden.

Nach erfolgreichem Lauf und Rekonstruktion:

```bash
paraview --data="$PWD/Kobuz.foam"
```

Für Druck `patch/kobuz` wählen, `internalMesh` ausblenden, p aktivieren, `Apply` und den letzten gespeicherten Stand auswählen. Ein Calculator mit `1.225*p` auf den Zelldaten erzeugt die Pascal-Darstellung. Für die veröffentlichte Abbildung wurde die Farbskala minus 190 bis plus 150 Pa verwendet.

Für Wirbel:

```bash
QT_QPA_PLATFORM=offscreen pvpython Create_Vortex_View.py
paraview --state=Kobuz_Vortices.pvsm
```

Der Filterweg lautet: `internalMesh` mit U, `Gradient` mit Vorticity und Q-Kriterium, `Cell Data to Point Data`, dann `Contour` auf Q = 50 1/s². Eingefärbt wird nach dem Betrag der Vorticity von 0 bis 500 1/s. Die Körper werden zusätzlich grau dargestellt. Die Q-Hülle hängt vom Schwellwert ab. Die stationäre RAS-Rechnung stellt die berechnete mittlere Strömung dar, keine zeitaufgelöste Wirbelablösung.

<a id="fortsetzung"></a>
## 10 Varianten und nächste Schritte

Bei geändertem **Anstellwinkel oder Tempo** gemeinsam prüfen beziehungsweise anpassen:

1. `0/U`: internes Feld sowie Eintritts-, Austritts- und Fernfeldwerte.
2. `0/k` und `0/omega`: konsistente Eintrittsturbulenz bei geändertem Tempo oder Turbulenzansatz.
3. `system/controlDict`: `magUInf`, `dragDir` und `liftDir` passend zum neuen Winkel und Tempo. Bei Flächen-, Bezugslängen- oder Schwerpunktänderung auch `Aref`, `lRef` und `CofR`.
4. Auswertung und Bildlegenden: tatsächliche Dichte, Normierung und Betriebspunkt verwenden.

Nur `0/U` zu ändern würde eine inkonsistente Kräfteauswertung hinterlassen. Auch `Auswertung.py` verwendet die Werte der aktuellen Steuerung und der Koeffizientendatei; nachträgliche Änderungen der Steuerung zu älteren Feldern vermeiden.

Bei geänderten **Randbögen oder Leitwerken** eine CAD-Variante sichern, neue STL exportieren, Maßeinheit prüfen, geschlossene Hüllen und Selbstüberschneidungen kontrollieren, Verfeinerungsbereiche anpassen und das Netz neu erzeugen. Geometrieänderungen sind kein Grund, ein altes Volumennetz ungeprüft weiterzuverwenden. Fusion kann das `.f3d`-Archiv öffnen; eine MCP-Verbindung für weitere KI-Konstruktion muss in der jeweiligen Umgebung eigens verfügbar sein.

Sinnvolle fachliche Fortsetzung:

1. Referenzfall reproduzieren und Unterschiede zum gespeicherten Lauf erklären.
2. Mindestens drei systematisch verfeinerte Netze sowie einen größeren Außenbereich vergleichen.
3. Wandauflösung und yPlus gezielt zum Wandmodell passend gestalten; Widerstand besonders prüfen.
4. Profilpolaren und Behandlung der Transition bei den Modellflug-Reynolds-Zahlen untersuchen.
5. Anstellwinkel- und Geschwindigkeitsreihe mit Trimmung und Gewichtsbalance aufbauen.
6. Rumpf und relevante Anbauteile ergänzen, bevor Flugleistungen des vollständigen Flugzeugs angegeben werden.
7. Erst auf dieser Grundlage Varianten wie Randbögen vergleichen. Relative Unterschiede sind ebenfalls auf Netzabhängigkeit und Modellfehler zu prüfen.

<a id="dokumentation"></a>
## 11 Dokumentation weiterführen

Für jeden neuen Lauf Git-Commit der Vorlage, Softwareversionen, Änderungen, Geometrie, Netzstatistik, Residuen, Kraftverlauf, yPlus und Auswertebedingungen festhalten. Einen eindeutigen Laufnamen und getrennte Ergebnisse verwenden. Die ursprünglichen Dateien unter `Referenzergebnisse` bleiben der dokumentierte Ausgangsstand.

Bei Änderungen an der Anleitung Markdown, PDF, Bildunterschriften und Abbildungsnummern zusammen prüfen. Ein Generator für die ursprüngliche PDF ist nicht in diesem Repository enthalten. Eine neue PDF muss daher mit einem geeigneten Dokumentwerkzeug erstellt und visuell geprüft werden; bloßes Ändern der Markdown-Datei aktualisiert die PDF nicht.

Die Quelle zur ursprünglichen Auslegung ist `Kobuz_Beispiel/CAD/kobuz.flz`. Weitere offizielle Dokumentationslinks und die detaillierte Installation stehen in der Anleitung. Diese Kontextdatei bei einer fachlichen Fortsetzung ebenfalls aktualisieren, insbesondere bei einem Rumpfmodell, neuen Referenzläufen, geänderter Software oder verbesserten Netz- und Turbulenzansätzen.
