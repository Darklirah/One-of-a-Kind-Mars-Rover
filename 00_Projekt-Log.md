# Projekt-Log: One-of-a-Kind Mars Rover

Laufendes Protokoll. Neueste Einträge oben.

---

## Offene Punkte für den Projektabschluss

Stehendes Verzeichnis, kein Tagebucheintrag. Hier landet, was bewusst
aufgeschoben wurde, weil es jetzt keinen stört und am Ende in einem Zug
erledigt werden kann.

- [ ] **HowTo-Datei** mit allen benutzten Schnittstellen und Werkzeugen und
      wie man sie einrichtet — PlatformIO samt der Umgebungsvariablen und
      dem Zertifikatsbündel, der KiCAD-MCP-Server, KiCadRoutingTools mit
      seinen zwei nicht-optionalen Schaltern, ESP Web Tools und
      GitHub Pages, die Datenblattquellen aus
      [Doku/10](Doku/10_Datenblaetter.md).
- [ ] **Fertiger Prompt für Claude**, der all diese Schritte ermöglicht,
      mit ausführlicher Erklärung jedes einzelnen — gedacht für jemanden
      mit leerer Sitzung und leerem Rechner.
- [ ] **Weboberfläche des Flashers eindeutschen.** ESP Web Tools kann das
      nicht von sich aus: im Bundle gibt es kein i18n, die einzige
      durchgereichte Anpassung ist `overrides.checkSameFirmware`, die
      Dialogtexte (`Connect`, `Erasing flash…`, `Installation complete!`)
      stehen fest im Code. Machbar ist es über eine **Übersetzungsschicht
      zur Laufzeit**: der Shadow-Root des Dialogs ist `mode:"open"`, ein
      `MutationObserver` kann die Texte ersetzen, sobald sie erscheinen —
      rund 40 Zeilen in unserer eigenen `docs/index.html`. Die Alternative
      wäre eine eigene gepatchte Kopie der 310 kB; dann gäbe es kein
      Aufblitzen, aber wir würden auf Dauer fremden Code mitschleppen und
      keine Korrekturen mehr von oben bekommen. **Empfehlung: die
      Übersetzungsschicht.**
- [ ] **`esp-web-tools` auf eine feste Version nageln.** `docs/index.html`
      lädt heute `esp-web-tools@10`, und das heißt „die neueste 10.x" —
      der Flasher kann sich jederzeit ändern, ohne dass jemand etwas
      anfasst. Das trifft auch die Übersetzungsschicht darüber. Also eine
      genaue Version eintragen und bewusst hochziehen; dann ist auch
      reproduzierbar, was ein Nachbauer bekommt.
- [ ] **Bilder in der Doku** auf den dann endgültigen Stand bringen.

---

## Nächste Platinenrevision — Befundliste (Nutzer, 21.10.2026)

Stehendes Verzeichnis. **Das sind keine Ideen, sondern am Muster gefundene
Fehler und beschlossene Änderungen.** Alles kommt in eine **neue,
nummerierte Revision; die alten Daten bleiben erhalten.**

### Verpolt oder falsch herum

- [ ] **Akkuanschluss J2 ist verpolt** → Footprint **180° drehen**
- [ ] **Stiftleiste MPU-6050 (U6)** → **180° drehen**
- [ ] **Stiftleiste U7 (VL53L0X)** → **180° drehen** *und* **SCK/SDA
      tauschen**

> Drei Teile falsch herum ist kein Zufall. Für die neue Revision gilt:
> **Pin 1 gegen den Aufdruck des echten Moduls prüfen, nicht gegen das
> Datenblatt** — bei den China-Modulen weicht die Reihenfolge oft ab. Der
> 1:1-Ausdruck unten ist genau dafür die richtige Gegenprobe.

### An die tatsächlich gekauften Module anpassen

- [ ] **U2 — neues Lademodul**: Pinbelegung anpassen, dazu **zwei Lötpads
      für OUT+ / OUT− als Befestigungspunkte** anlegen
- [ ] **U5 — DC/DC-Wandler**: Anschlussleiste an das Modul anpassen
- [ ] **S1 — Schalter neu entwerfen**, anderes Footprint

### Bibliotheks- und Entwurfsarbeit

- [ ] **Alle Module als 3D-Modelle erzeugen**, soweit möglich auch
      **Schaltpläne für die Module** anlegen
- [ ] **Prüfen, wie sich die Module ins KiCad-Design aufnehmen lassen** —
      eventuell je Modul ein eigener Plan (hierarchische Blätter?)
- [ ] **Prüfen, wie sich die Leiterplatte verkleinern lässt.** Ein
      **ESP32-Modul mit USB-C** wäre gut, und der **USB-Anschluss muss
      auch im eingebauten Zustand erreichbar** sein — dafür gegebenenfalls
      das 3D-Modell des Gehäuses anpassen.

### Hinweis des Nutzers an sich selbst

> **Alle Anschlüsse prüfen. Layout 1:1 ausdrucken und mit den echten
> Modulen gegenprüfen.**

---

## Offene Fragen für die nächste Sitzung (Gehäuse, Stand 11.10.2026)

Stehendes Verzeichnis wie oben. Jede Frage blockiert einen Teil des
Gehäuseentwurfs oder der Doku, bis sie am echten Teil beantwortet ist.

**Am Teil nachsehen oder messen**

- [ ] **Hat der Akku eine eigene Schutzplatine?** (meist unter dem gelben
      Klebeband am Kabelende). Wenn nein: TP4056-Modul **mit**
      Schutzschaltung und sechs Anschlüssen beschaffen. Wenn ja: an `U2`
      Pin 3 und Pin 5 brücken, siehe [Doku/05](Doku/05_Pinbelegung.md).
- [ ] **MT3608: Sitzen die vier Lötaugen wirklich an den Ecken?** Davon
      hängt ab, wie das Modul auf die vierpolige Leiste `U5` kommt.
- [ ] **Wie sitzen MPU-6050, TP4056 und MT3608 tatsächlich** (stehend,
      liegend, in welche Richtung)? Im Modell angenommen; zwischen
      RTG-Tasche und MPU-6050 bleiben nur 0,4 mm.
- [ ] **ESP32 auf Buchsenleisten oder direkt eingelötet?** Und wie weit
      stehen die Stifte unter der Platine über? (im STEP-Modell 4,9 mm)
- [ ] **Motor wiegen und Strom bei 3 V messen.** Danach Massebudget und
      Laufzeit in [Doku/02](Doku/02_SMD-vs-THT-Wirtschaftlichkeit.md)
      nachziehen — beide rechnen noch mit dem Münzmotor.
- [ ] **Bürstenkopf: Plattendicke und Borstenlänge einzeln messen.**
      Angenommen sind 6 mm und 12 mm (zusammen die gemessenen 18 mm).
- [ ] **Maße nachmessen**, die bisher Katalogwerte sind: Motorkörper
      (Ø 12 × 15,5 mm), GY-521 (21 × 16 mm), TP4056 (25 × 19 mm).

**Entscheiden**

- [ ] **Gewicht abspecken?** Gerechnet 76–92 g gesamt, die Bodenschale
      allein bis 34 g. Kandidaten: Boden öffnen oder ausdünnen, Wangen und
      Ausleger schlanker.
- [ ] **Akkutasche verriegeln?** Bisher hält der Akku nur durch Neigung und
      Reibung.
- [ ] **Rover-Optik ausbauen** anhand der beiden Vorlagen (jakkra/Mars-Rover,
      NASA-Modell von Curiosity) — beide noch nicht ausgewertet. Denkbar:
      Roboterarm, höhere Schwingen, Deckdetails.
- [ ] **Probedruck.** Erst danach lässt sich sagen, ob Rasthaken, Nut,
      Tüllensitze und die Druckeinstellungen aus
      [Gehaeuse_CAD](Gehaeuse_CAD/README.md) stimmen.

**Ideen, nicht entschieden**

- **Revision 2: Module auf die Hauptplatine integrieren.** ESP32-WROOM
  direkt (mit USB-Seriell-Chip, USB-C, zwei Tastern, 3,3-V-Regler),
  Laderegler mit Schutz-IC (Variante 2a der Stückliste), MT3608 diskret.
  Der VL53L0X bleibt ein Modul auf dem Mast; den MPU-6050 eher als flach
  aufgelötetes Modul lassen (QFN ist nichts für den Lötkolben).
  Erwartet: geschätzt 9–11 g leichter, Bauhöhe ca. 4 mm statt 39 mm, keine
  wackelnden Module, die Anschlussprobleme an `U2`/`U5` entfallen.
  Preis: Bauteile etwa gleich (ca. 11–13 € statt ca. 11 €), aber die
  SMD-Seite muss bestückt werden lassen — bei 5 Stück grob 8–15 € je
  Platine zusätzlich (geschätzt), ab etwa 10 Stück gleicht es sich an.
  Aufwand: neuer Schaltplanteil mit 35–45 Bauteilen und neues Routing;
  Firmware und Pinplan bleiben. **Erst sinnvoll, wenn die jetzige Platine
  gelaufen ist** und sich zeigt, dass der Rover zu schwer ist.
- **Anderes Rechenboard mit Akkuladung an Bord** (statt DevKitC + TP4056).
  Anforderung des Nutzers: günstig und in Deutschland gut erhältlich.
  - **LOLIN32 / LOLIN32 Lite** — klassischer ESP32, also dieselbe Firmware
    mit neuem Pinplan. Lader TP4054 bis 500 mA, Akkuanschluss JST-PH 2.0,
    ca. 49 × 25 mm, 26 Pins, rund 6–11 € (BerryBase 6,40 €, AZ-Delivery
    6,39–10,99 €, Amazon ca. 14 €). **Am 11.10.2026 bei BerryBase nicht
    lieferbar, bei AZ-Delivery teils „ausverkauft"** — vor dem Bestellen
    prüfen. Kein Akkuschutz erwähnt, Ladestrom fest 500 mA (= 1 C für die
    500-mAh-Zelle, die Doku wollte 255 mA), kein Schalter.
  - **Seeed XIAO ESP32-C3** — 21 × 17,8 mm, 8,10 € bei BerryBase, Laden
    100/350 mA. Aber nur 11 Pins (der Rover braucht 10), anderer Chip
    (ESP32-C3), drei Boot-Pins, externe Antenne. Entspricht Variante C in
    [Doku/02](Doku/02_SMD-vs-THT-Wirtschaftlichkeit.md).
  - **ESP32-C3 „SuperMini"** (Amazon B0FKGZLZGH, 5er-Pack, 4 MB Flash) —
    ca. 23 × 18 mm, wenige Gramm, sehr günstig. *Dafür:* üblicherweise 13
    nutzbare Pins (Bedarf 10), fünf Analogeingänge, die mit WLAN arbeiten,
    von PlatformIO mit dem bisherigen Arduino-Kern unterstützt. *Dagegen:*
    kein Lader an Bord (TP4056 und MT3608 bleiben), Pinplan neu, drei
    Boot-Pins (GPIO 2, 8, 9), WLAN-Reichweite streut wegen der winzigen
    Antenne von Board zu Board.
  - **ESP32 „D1 Mini"** (Amazon B0DP9WYJNY, 5er-Pack, USB-C, CH9102F) —
    ca. 39 × 31 mm. *Dafür:* klassischer ESP32, Firmware bleibt bis auf den
    Pinplan. *Dagegen:* kein Lader erkennbar, spart also kein Modul;
    Doppelreihen-Stiftleisten.
  - **ESP32-C6 Mini** (Amazon B0FKH2M99L, 3er-Pack) — klein wie der C3.
    *Dagegen:* braucht den neueren Arduino-Kern (3.x), den die
    Standard-Plattform von PlatformIO für den C6 nicht ohne Weiteres
    mitbringt; kein Lader. Von allen Kandidaten der höchste
    Firmware-Aufwand, ohne Vorteil für dieses Projekt.
  - **Waveshare ESP32-C3-Zero / „ESP32-C3 Mini"** (Eckstein WS25532,
    5,50 €, lieferbar am 11.10.2026) — der bisher beste Kandidat. Laut
    Waveshare-Wiki 15 GPIO, 4 MB Flash, USB-C, RGB-LED an GPIO 10, und der
    5-V-Anschluss nimmt **3,7–6 V** an: das Board ließe sich also direkt aus
    dem LiPo versorgen, der MT3608 wäre nur noch für die Motoren nötig oder
    entfiele ganz. Kein Lader an Bord.
    **Probe-Build am 11.10.2026 bestanden:** Firmware unverändert bis auf
    zehn Pinnummern, `espressif32@6.9.0`, Board `esp32-c3-devkitm-1`,
    Schalter `ARDUINO_USB_MODE=1` und `ARDUINO_USB_CDC_ON_BOOT=1`.
    0 Fehler, 0 Warnungen, RAM 14,3 %, Flash 71,8 %. Gebaut in einer Kopie
    außerhalb des Repos; **nicht auf Hardware gelaufen**.
    Verwendeter Pinplan: Motoren 6/7, Liniensensoren 0/1, I²C 8/9 (beides
    Boot-Pins, die beim Start hoch liegen müssen — die Pull-ups der
    Sensormodule sorgen dafür), LEDs 3/4/5/20. Frei bleiben 21, bedingt 2
    (Boot-Pin) und 10 (RGB-LED); 18/19 gehören dem USB. Der Pinplan stammt
    aus dem Wiki und meinem Wissen über den Chip, nicht vom Schaltplan des
    Boards — vor einem Platinenentwurf dort gegenprüfen.
  - **Waveshare ESP32-S3-Zero / „ESP32-S3 Mini"** (Eckstein WS25517,
    7,95 €, lieferbar am 11.10.2026) — die Variante mit Reserve. Laut
    Wiki 24 GPIO (davon 14/15/16 nur als Lötflächen), zwei Kerne, 4 MB
    Flash + 2 MB PSRAM, Versorgung ebenfalls 3,7–6 V, RGB-LED an GPIO 21.
    *Dafür:* genug Pins für Akkumessung, Betriebsart-Taster und
    Erweiterungen; weniger Rücksicht auf Boot-Pins. *Dagegen:* 2,45 €
    teurer, voraussichtlich höherer Stromverbrauch, Rechenleistung und RAM
    braucht der Rover nicht. **Kein Probe-Build gemacht.**
  - **Vormerkung für Version 2 (Nutzer, 11.10.2026):** C3-Zero, wenn der
    Rover genau das können soll wie heute; S3-Zero, wenn Akkumessung oder
    Erweiterungen dazukommen. **Antenne:** das Board so setzen, dass das
    Antennenende über die Platinenkante hinausragt, kein Kupfer und keine
    Bauteile darunter, weg von Motoren, Akku und Step-Up-Drossel.
  - **Platzierung des Funkmoduls (für Version 2), nach Wirkung sortiert:**
    1. Antennenende über die Platinenkante hinausragen lassen; darunter
       und direkt daneben kein Kupfer, keine Bahn, keine Massefläche, kein
       Bauteil.
    2. Nichts Metallisches davor oder daneben: weg vom Akku (wirkt wie
       eine Metallplatte), von den Motoren und von der Drossel des Step-Up.
    3. So hoch wie möglich — der Rover fährt am Boden, das Handy ist etwa
       einen Meter höher.
    4. PETG stört kaum, solange es nicht massiv an der Antenne anliegt.
    Für den Rover: **vorn in der Mitte, Antenne nach vorn über die
    Vorderkante**, ein Stück seitlich neben dem Mast (CFK leitet und
    schirmt). Die USB-Buchse liegt dann zur Platinenmitte und muss von oben
    erreichbar bleiben. Die Reichweite ist kein enger Punkt (reduzierte
    Sendeleistung, Bedienung aus wenigen Metern); Regel 1 und 2 dürften
    reichen.
  - **Idee: externe Antenne.** Braucht ein Board mit Antennenstecker
    (U.FL/IPEX), z. B. das XIAO ESP32-C3; die Waveshare-Zero-Boards haben
    nur die Keramikantenne. Bauformen, klein nach groß:
    Folienantenne (FPC, ca. 30–45 × 7 mm, unter 1 g, zum Aufkleben) —
    Drahtstück 31 mm (λ/4 bei 2,45 GHz) — Stabantenne mit
    U.FL-auf-SMA-Kabel (3–10 g, 5–11 cm). Eine Stabantenne reicht
    elektrisch mehr als aus, ist für dieses Fahrzeug aber unnötig schwer;
    die Folienantenne am Mastkopf wäre die leichte Lösung. **Nicht direkt
    am CFK-Stab entlangführen** — dann lieber einen GFK-Stab als Mast.

    | Bauform | Größe | Gewicht | Einordnung |
    |---|---|---|---|
    | Folienantenne (FPC) mit Kabel und Stecker | ca. 30–45 × 7 mm, flach | unter 1 g | zum Aufkleben, die leichte Lösung |
    | Drahtstück | 31 mm | fast nichts | braucht eine Massefläche als Gegenpol, muss sauber angelötet sein |
    | Stabantenne mit Adapterkabel | 5–11 cm | 3–10 g | beste Reichweite, für dieses Fahrzeug zu schwer |

    Typische Werte, keine Daten eines bestimmten Produkts. **Empfehlung:**
    Folienantenne oben am Mastkopf, quer zum Stab. Dem XIAO liegt nach
    meinem Wissen eine solche Antenne bei (nicht geprüft). Zu beachten:
    jedes Gramm am Mastkopf lässt den Mast stärker schwingen, und das
    Antennenkabel braucht wie die Sensorlitzen eine Schlaufe am Mastfuß.
    **Reihenfolge:** erst die eingebaute Antenne ausprobieren, richtig
    platziert; die externe nur nachrüsten, wenn die Verbindung abreißt.

  | Board | Firmware-Aufwand | Größe | Spart Module | Preis |
  |---|---|---|---|---|
  | LOLIN32 | gering (gleicher Chip) | etwas kleiner als heute | Laderegler | 6–11 € |
  | ESP32 D1 Mini | gering (gleicher Chip) | kleiner | nein | 5er-Pack |
  | XIAO ESP32-C3 | mittel | sehr klein | Laderegler | 8,10 € |
  | ESP32-C3 SuperMini | mittel | sehr klein | nein | 5er-Pack |
  | Waveshare ESP32-C3-Zero | mittel, **Probe-Build bestanden** | sehr klein | evtl. den Step-Up | 5,50 € |
  | Waveshare ESP32-S3-Zero | mittel, nicht gebaut | sehr klein | evtl. den Step-Up | 7,95 € |
  | ESP32-C6 Mini | am höchsten | sehr klein | nein | 3er-Pack |

  Angaben zu den Amazon-Boards stammen aus den Titeln der Angebote; Pinzahl,
  Maße und Preise standen im lesbaren Teil der Seiten nicht.
  - Die **5-V-Schiene wird damit entbehrlich**: das Board läuft direkt aus
    dem Akku, die Motoren können am Akku hängen (3,0–4,2 V). Der MT3608
    lässt sich trotzdem zusätzlich anbauen und versorgt dann nur die
    Motoren — konstante Motorkraft unabhängig vom Ladestand.
  - In jedem Fall eine **neue Platine**; die jetzige passt nur zum DevKitC.
    Pin- und Boot-Pin-Angaben zum XIAO stammen nicht vom Datenblatt und
    sind vor einem Entwurf zu prüfen.


---

## 2026-10-21 — Leiterplattendaten als „in Bearbeitung" gekennzeichnet

Die Befundliste von heute Vormittag stand bisher nur im Log. Wer von außen
in den Ordner `Fertigung/` schaut, hätte dort einwandfreie Gerber gefunden,
ein DRC mit 0 Fehlern — und hätte sie bestellt. Das ist genau der Fall, den
man nicht dem Zufall überlassen darf: die Fehler stecken nicht im Layout,
sondern in der Zuordnung zu den echten Modulen, und davon sieht man in den
Daten nichts.

Die Warnung steht jetzt an jeder Stelle, an der jemand einsteigen könnte:

| Ort | Form |
|---|---|
| [`Fertigung/README.md`](Fertigung/README.md) | `> [!CAUTION]`-Block ganz oben, Stand-Zeile auf „in Bearbeitung" |
| [`pcb/README.md`](pcb/README.md) | neu angelegt; Befundtabelle, Dateiübersicht, Arbeitsregel zur Sperrdatei |
| [`Fertigung/WARNUNG-NICHT-BESTELLEN.txt`](Fertigung/WARNUNG-NICHT-BESTELLEN.txt) | reiner Text, ohne Umlaute, für Leser ohne Markdown |
| [`Doku/03`](Doku/03_Stueckliste-BOM.md), [`Doku/04`](Doku/04_PCB-Layout-Empfehlung.md) | derselbe Block, weil beide die Platine beschreiben |
| [Bauanleitung](Doku/Ich_baue_meinen_Marsrover.md) | derselbe Block — hier würde jemand anfangen zu löten |

Der wichtigste Teil ist die Textdatei: `erzeuge_fertigungsdaten.sh` legt sie
jetzt **in beide ZIP-Archive** mit hinein. Ein Archiv wandert weiter, die
README bleibt zurück — wer nur das ZIP bekommt, hätte die Warnung sonst nie
gesehen. Nachgeprüft: Gerber-Archiv 15 Dateien, Schablonen-Archiv 6, die
Warnung in beiden.

In allen vier Markdown-Fassungen steht derselbe Satz, weil er der
eigentliche Grund für die ganze Übung ist: **dass das DRC sauber durchläuft,
sagt über diese Fehler nichts aus.** Es prüft, ob das Layout *in sich*
stimmig ist — Abstände, Netze, Kurzschlüsse. Ob Pin 1 einer Stiftleiste dort
liegt, wo das echte Modul ihn hat, kann es nicht wissen. Die Gegenprobe
steht in der Befundliste und heißt: Layout 1:1 ausdrucken und mit den
Modulen vergleichen.

Die **Firmware ist davon nicht betroffen**, und das ist überall mit
vermerkt. Sie läuft auf einem nackten DevKit, 0.5.2 liegt im Web-Installer,
und daran ändert das Platinenlayout nichts.

---

## 2026-10-21 — Bilder und Beschreibung auf den Stand 0.5.2 gebracht

**Nichts neu zu übersetzen.** Seit 0.5.2 hat sich am Quelltext nichts
geändert; ein Neubau ergab ein **bitgleiches** Abbild
(SHA-256 `e09462c2…`, 1 037 216 Byte). Statt eine Version hochzuzählen,
hinter der nichts steckt, ist das nachgeprüft und so geblieben.

**Die Bilder in der Doku zeigten noch den alten Aufbau** — drei
Betriebsarten, Nothalt am Seitenende, Programmeditor ohne Startleiste.
Alle sechs neu aufgenommen, dazu ein siebtes:

| Bild | zeigt |
|---|---|
| `app_test.jpg` | **neu** — Funktionstest mit der Kompassrose |
| `app_fahren.jpg` | Startansicht mit der Zeile Freigeben + NOTHALT und vier Betriebsarten |
| `app_programm.jpg` | Programmeditor mit der Startleiste oben |
| `app_befehle.jpg` | Befehlsliste mit zugeklappten Gruppen — und darüber beide klebenden Leisten im Scrollzustand |
| `app_dialog.jpg` | Befehlsdialog beim Ändern eines Schritts |
| `app_name.jpg` | Namensabfrage |

[Doku/06](Doku/06_Fernsteuerung-App.md) hat jetzt einen eigenen Abschnitt
*Funktionstest mit Kompassrose*, samt dem Hinweis, was eine falsch
laufende Nadel bedeutet.

**Dazu die Arbeitsstände aus den Zwischensitzungen aufgenommen:** die vier
Bestückungspläne als PDF, die beiden Druckdateien `Platte1_PETG.3mf` und
`Platte1_TPU.3mf`, die Stückliste `pcb/MarsRover.csv` und die geänderten
Spalteneinstellungen des Stücklisten-Dialogs in `MarsRover.kicad_pro`.

> Vor dem Aufnehmen geprüft, weil das Repo öffentlich ist: **keine der
> Dateien enthält einen lokalen Pfad** — weder die PDFs noch die
> 3MF-Dateien.

---

## 2026-10-21 — Beide Leisten kleben jetzt (0.5.2)

Der Nothalt scrollte noch mit weg. Jetzt klebt die obere Zeile
(**Freigeben · NOTHALT**) am Fensterrand, und die Startleiste des
Fahrprogramms klebt **an deren Unterkante** statt am Fensterrand — sonst
schöbe sie sich darunter und der Startknopf wäre verdeckt. Genau das war
gemeint mit „der Programmstartknopf fehlt noch in der Ansicht".

Die Höhe der oberen Leiste lässt sich nicht fest eintragen, sie hängt an
Schriftgröße und Gerät. Sie wird beim Start gemessen und als `--topH`
hinterlegt, bei Größen- und Lagewechsel neu.

**Nachgemessen bei 1200 px Scrollweg:** obere Leiste 0 bis 78 px,
Startleiste klebt bei 78 px, Überlappung **0 px**, beide vollständig im
Bild, keine Skriptfehler. `--topH` steht auf 78 px.

Firmware **0.5.2**: RAM 16,2 %, Flash 73,6 %.

---

## 2026-10-21 — Nothalt nach oben, Programmknopf entkoppelt (0.5.1)

**Nothalt steht jetzt oben neben der Freigabe**, beide in einer Zeile. Er
saß am Seitenende — genau dort, wo man ihn nicht findet, wenn es eilt.

Dabei ein Darstellungsproblem gelöst, das sonst entstanden wäre: bei
freigegebenen Motoren heißt der linke Knopf *Motoren sperren* und ist
**gefüllt rot**. Zwei gleich aussehende rote Flächen nebeneinander wären
im Ernstfall genau die falsche Wahlhilfe. Der Nothalt ist deshalb nur
**umrandet** und füllt sich erst beim Drücken. Aufteilung 1,35 zu 1 — die
Freigabe ist der Knopf des Normalbetriebs.

**Der Programmknopf war schon einer.** `bRun` schaltet seit jeher
Beschriftung, Farbe *und* Funktion um; da war nichts zu trennen oder
zusammenzuführen.

Eine Schwachstelle steckte aber darin: der Knopf las seinen Zustand aus der
**eigenen Beschriftung** zurück —

```js
var running = E("bRun").textContent.indexOf("stoppen") > 0;
```

Wer den Text ändert, bricht damit stillschweigend die Funktion: der Knopf
schickt dann `B,1` statt `B,0`. Jetzt kommt der Zustand aus der Telemetrie
(`progRunning` aus dem Feld `pr`).

**Geprüft:** beide Zustände durchgeschaltet und mitgehört, was hinausgeht —
gestoppt → `B,1` mit grünem *„▶ Programm starten"*, laufend → `B,0` mit
rotem *„■ Programm stoppen"*. Keine Skriptfehler.

Firmware **0.5.1**: RAM 16,2 %, Flash 73,5 %.

---

## 2026-10-21 — Vier Betriebsarten, Kompassrose, Startleiste oben (0.5.0)

**Funktionstest ist jetzt eine Betriebsart.** Er steckte als Karte weit
unten in der Seite, wo ihn niemand sucht. Die Wahl hat jetzt vier Flächen
in der Reihenfolge, in der man die Dinge tut: **Funktionstest ·
Linienfolger · Selbst fahren · Programm**.

Technisch ist er weiterhin keine Betriebsart — in der Hauptschleife gilt
„Diagnose geht vor Betriebsart", der Test läuft quer zu allem anderen.
Deshalb trennt die Bedienung jetzt zwei Begriffe: `view` (was die Seite
zeigt) und `mode` (was der Roboter fährt). Beim Umschalten auf den
Funktionstest bleibt die Betriebsart, wie sie war, und es geht kein `M,…`
hinaus. Läuft der Test, springt die Ansicht von selbst dorthin — und die
Telemetrie wirft einen nicht mehr heraus, während man hinsieht.

**Kompassrose statt nur einer Gradzahl.** Beim Drehtest sagt eine Zahl
nicht, ob sich der Rover in die *richtige* Richtung dreht. Jetzt eine Rose
mit **0° oben, im Uhrzeigersinn** — so, wie auch der Drehwinkel in den
Fahrbefehlen gezählt wird. 24 Teilstriche, Beschriftung innen zwischen den
Ringen (außen lag sie auf den Strichen und war durchgestrichen).

Dafür war **keine Firmware-Änderung nötig**: das Feld `hd` steckt längst in
jeder Telemetriezeile.

**Start und Stop bleiben oben.** Die Leiste mit *Programm starten/stoppen*
klebt jetzt am Kopf des Programmbereichs. Vorher saß sie unter der
Schrittliste — bei 48 Schritten über 2000 px tiefer. Einen Roboter, der
gerade vom Tisch fährt, scrollt man nicht erst zum Stoppknopf.

**Geprüft** in der Vorschau: keine Skriptfehler, Rose auf 138° bei `hd:138`,
24 Striche, Leiste bei 900 px Scrollweg weiterhin oben (`top: 0`), Knopf
schaltet bei `pr:1` auf rot und „■ Programm stoppen" mit „Schritt 3 von 6".

Firmware **0.5.0**: RAM 16,2 %, Flash 73,5 %.

**Nebenbei:** in Doku/07 noch ein zerschossenes Unicode-Escape gefunden
(`2013` statt eines Gedankenstrichs) und die Stelle korrigiert, die den
Funktionstest noch „ganz unten" verortete.

---

## 2026-10-11 — Gehäuse und Fahrwerk: erster CAD-Entwurf (V2), Bauanleitung

**Gemacht**

- Neuer Ordner [Gehaeuse_CAD/](Gehaeuse_CAD/README.md): parametrische
  FreeCAD-Skripte, Druckteile als STL/STEP, einfache Modelle der Zukaufteile.
- [Doku/11](Doku/11_Gehaeuse-und-Fahrwerk.md) mit fünf Ansichten aus dem Modell.
- [Ich baue meinen Marsrover](Doku/Ich_baue_meinen_Marsrover.md):
  Bauanleitung in 17 Schritten mit Bildern.

**Entscheidungen**

- **Offenes Gehäuse**, die Platine bleibt sichtbar. Befestigung: Nut an der
  hinteren Längsseite, zwei Rasthaken vorn mit 3° geschrägter Unterseite,
  damit die Platine wieder herausgeht.
- **Antriebe seitlich neben der Platine**, nicht darunter. Ein ungekürzter
  Bürstenkopf ist 18 mm hoch, die Platinenunterseite liegt wegen der
  TCRT5000 aber nur 10,2 mm über dem Boden.
- **Entkopplung über vier TPU-Tüllen.** Der Bürstenträger hängt nur an zwei
  Zapfen, starren Kontakt zum Gehäuse gibt es nicht.
- **Akku in der RTG-Tasche am Heck** statt unter der Platine — dort lag er
  0,5 mm unter den Lötstiften. Der Stand mit Akku unter der Platine ist als
  `Gehaeuse_CAD/V1/` eingefroren.
- **Unwucht über der Bürstenmitte**, beide Motoren gleich herum, bei einem
  die Litzen vertauscht (gegenläufig, gegen Seitendrift).

**Offen**

- **Nichts davon ist gedruckt oder gebaut.** Geprüft ist nur am Modell:
  gültige Körper, keine Überschneidungen, Überhänge höchstens 45°.
- **Masse:** gerechnet 76–92 g gesamt, die Druckteile allein bis 46 g.
  [Doku/02](Doku/02_SMD-vs-THT-Wirtschaftlichkeit.md) nennt 40 g als Risiko.
- **Gekaufte Teile weichen von der Stückliste ab:** Zylindermotor
  12 × 22,5 mm statt Münzmotor; TP4056 mit Mini-USB und **ohne
  Schutzschaltung**; MT3608 mit 36 × 17 mm. In [Stückliste](Doku/03_Stueckliste-BOM.md) und
  [Pinbelegung](Doku/05_Pinbelegung.md) nachgetragen, samt der aus der Platine gelesenen
  Belegung von U2/U5/U6/U7. **Nicht** nachgezogen: Massebudget und Laufzeit in Doku/02 (rechnen
  noch mit dem Münzmotor) und der Nennstrom des neuen Motors bei 3 V (nicht gemessen).
- Einbaulage von MPU-6050, TP4056 und MT3608 ist angenommen, mehrere
  Modulmaße sind Katalogwerte.

---

## 2026-10-11 — Die Seite kommt von selbst: mDNS und eine Weiche im Anmeldefenster (0.4.0)

**Die Frage war,** ob sich die Bedienseite beim Öffnen des Browsers von
selbst laden lässt. Teilweise ging das schon: der DNS zeigt jeden Namen auf
den Roboter, also landet **jede `http://`-Adresse** bei ihm. Zwei Dinge
standen im Weg:

- **Startseiten sind heute `https://`.** Dafür bräuchte der Roboter ein
  gültiges Zertifikat für eine fremde Domain — das wäre ein Angriff, und
  der Browser würde es zu Recht melden. Nicht lösbar.
- **Das Anmeldefenster ist nicht der richtige Browser.** iOS öffnet dafür
  eine eingeschränkte WebView, in der **WebSockets oft nicht laufen**. Der
  Roboter lieferte dort bisher die volle Oberfläche aus — sie erschien, der
  Joystick tat nichts, und es sah nach einem Defekt aus.

**Drei Änderungen**

1. **mDNS.** Der Roboter ist jetzt unter einem Namen erreichbar, abgeleitet
   aus dem Netznamen: klein geschrieben, Unterstrich zu Bindestrich.
   `MarsRover_Petra` → `http://marsrover-petra.local`. Immer aus dem WLAN
   ableitbar, in das man gerade gegangen ist, und zwei Rover stoßen nicht
   zusammen.
2. **Weiche statt Bedienung im Anmeldefenster.** Eine knapp 1 kB große
   Seite mit einem Knopf *Bedienung öffnen* — läuft auch in der
   eingeschränkten Ansicht — und mit dem Hinweis, was zu tun ist, falls der
   Joystick dort nicht reagiert.
3. **Erkennung am Host statt an URL-Listen.** Gilt die Anfrage
   `192.168.4.1` oder `<name>.local`, kommt die Bedienung; bei jedem
   fremden Namen die Weiche. Das sind genau die Prüfadressen, mit denen
   Android, iOS und Windows testen, ob ein Netz ins Internet kommt — und
   die ändern sich je nach Hersteller und Version, eine fest eingetragene
   Liste veraltet.

**Kosten:** RAM 15,2 → 16,2 %, Flash 70,8 → 73,1 %. Das ist die
mDNS-Bibliothek; dafür muss niemand mehr eine IP abtippen.

**Nachgemessen statt geschätzt:** die Weichenseite ist mit kurzem Netznamen
977 Byte, mit einem ausgereizten rund 1030. Der Puffer stand auf 1100 —
`snprintf` hätte bei einem langen Namen stillschweigend abgeschnitten und
eine halbe Seite ausgeliefert. Jetzt 1400.

Sauberer Durchlauf von Null: **0 Fehler, 0 Warnungen.**

---

## 2026-10-11 — Befehlsdialog, und Schritte lassen sich endlich ändern (0.3.0)

**Die Lücke:** ein gespeichertes Programm war nur zum Teil bearbeitbar.
Schritte ließen sich verschieben und löschen, aber **ihre Werte nicht
ändern** — aus „geradeaus mit 60 %" wurden 25 % nur über Löschen und neu
Einfügen.

**Ein Fenster für beides.** Die acht Einstellblöcke sind aus dem
Befehlsbaukasten in einen Dialog gewandert. Der geht auf zwei Wegen auf:

| Antippen von … | Überschrift | rechter Knopf |
|---|---|---|
| einem Befehl in der Liste | Name des Befehls | **Einfügen** |
| dem Text eines Schritts im Ablauf (✎) | Name des Befehls | **Änderung speichern** |

Dazu je ein Satz, was der Befehl tut — beim Fahrprogramm steht man sonst
vor einem Schieberegler und weiß nicht, was er bewirkt.

**Warum ein Fenster und kein Scrollbereich mit festem Einfügeknopf:**

- **13 der 14 Befehle brauchen eine Einstellung** (nur „anhalten" nicht).
  Es gibt also nie „antippen und fertig"; ein dauerhaft sichtbarer
  Einfügeknopf hätte so getan, als wäre es ein Schritt.
- Im Scrollbereich scrollt der gewählte Befehl weg, während man unten den
  Drehwinkel einstellt — man sieht den Regler, aber nicht mehr, wozu er
  gehört.
- Verschachteltes Scrollen ist auf dem Handy heikel: liegt der Finger über
  dem inneren Bereich, scrollt die Seite nicht.
- **Abbrechen** gab es vorher gar nicht; ein Antippen war endgültig.
- Es passt zur schon vorhandenen Namensabfrage — ein Muster statt zwei.

**Gruppen klappen zu.** *Fahren* steht offen, die drei übrigen zugeklappt.
Die Liste schrumpft damit von 755 auf **584 px**, der ganze Block von 935
auf 584 px.

**Billig umzusetzen war das, weil `bAdd` die Werte erst beim Drücken über
`E("aSpd").value` las** — es ist ihm egal, wo die Felder stehen. Neu sind
nur `readForm()` und sein Gegenstück `fillForm()`, das die Regler aus einem
vorhandenen Schritt füllt und dabei `input` auslöst, damit die
Beschriftungen nachziehen.

**Geprüft** in der Vorschau, nicht nur angesehen: fünf Befehle eingefügt,
dann Schritt 1 von 60 auf 25 % geändert, Schritt 3 erst mit *Abbrechen*
(bleibt 2,0 s) und dann mit *Speichern* (wird 5,0 s), und der LED-Schritt
mit seinen zwei Auswahlfeldern auf „alle vier LEDs blinken". Schrittzahl
bleibt dabei konstant, keine Skriptfehler.

**Doku nachgezogen:** [Doku/06](Doku/06_Fernsteuerung-App.md) mit drei
neuen Bildschirmfotos (Editor, Befehlsliste mit zugeklappten Gruppen,
Dialog), [Doku/08](Doku/08_Fahrprogramm.md) mit dem neuen Schritt 5
„Werte nachträglich ändern".

Firmware **0.3.0**: RAM 15,2 %, Flash 70,8 %.

**Nachtrag: Boot-Taste und zwei vertagte Punkte**

Die Installerseite und [Doku/07](Doku/07_Inbetriebnahme-und-Tuning.md) sagen
jetzt beide, dass die **BOOT-Taste gedrückt bleiben muss, bis das Flashen
beginnt** — zu früh losgelassen bricht es mit `Failed to connect to ESP32`
ab, und das sah bisher nach einem Defekt aus.

Beim Nachsehen, ob sich der Flasher auch auf Deutsch stellen lässt, kamen
zwei Punkte heraus, die **bewusst auf den Projektabschluss vertagt** sind
(siehe „Offene Punkte für den Projektabschluss" oben):

- **ESP Web Tools kann keine Sprachumschaltung.** Im ausgelieferten Bundle
  gibt es kein i18n; die einzige durchgereichte Anpassung ist
  `overrides.checkSameFirmware`. Die Dialogtexte stehen fest im Code.
- **`esp-web-tools@10` ist keine feste Version**, sondern „die neueste
  10.x". Der Flasher kann sich also jederzeit ändern, ohne dass wir etwas
  anfassen.

---

## 2026-10-08 — Befehlsauswahl mit eigener Liste (Firmware 0.2.1)

Die Gruppen *Fahren / Zeit / Licht / Ablauf* steckten in einem nativen
`<select>`. Dessen `optgroup`-Beschriftungen zeichnet das **Betriebssystem**:
Android und iOS öffnen einen eigenen Auswahldialog, der jede Formatierung
der Seite ignoriert. Per CSS wäre „hellgelb und fett" dort nie angekommen.

**Deshalb eine selbst gebaute Liste:**

- Das `<select>` bleibt als Datenspeicher stehen, nur ausgeblendet — alles
  andere liest unverändert `E("aOp").value`, kein Risiko an den drei
  Stellen, die davon abhängen.
- Die sichtbare Liste **erzeugt sich aus eben diesem `<select>`**. Die
  Befehle stehen weiter nur an einer Stelle im Markup; ein neuer Eintrag
  taucht automatisch an der richtigen Stelle auf.
- Gruppenüberschrift 15 px fett in `#ffe08a`, der gewählte Befehl blau
  hervorgehoben statt in einem zugeklappten Feld zu verschwinden.

**Geprüft:** fünf Befehle quer durch alle vier Gruppen angeklickt, jedes Mal
kommt der richtige Wert an und es erscheinen genau die passenden
Einstellfelder.

**Bewusst in Kauf genommen:** die Liste ist immer ausgeklappt, gut 600 px
statt eines zugeklappten Feldes. Dafür ist alles auf einen Blick sichtbar.

Firmware **0.2.1** gebaut und veröffentlicht: RAM 15,2 %, Flash 70,4 %.
Online gegengeprüft — das Abbild auf GitHub Pages ist bitgleich mit dem
gebauten (995 440 Byte).

**Nachtrag am selben Tag: die Bildschirmfotos sind da.** Die Rückfrage hat
sich erledigt — gemeint war die Oberfläche. [Doku/06](Doku/06_Fernsteuerung-App.md)
hat jetzt einen Abschnitt „So sieht sie aus" mit **vier** Aufnahmen:
Hauptansicht mit Joystick, Namensabfrage, Programmeditor mit den drei
farbigen Bereichen und die Befehlsliste mit den Gruppenüberschriften. Sie
entstehen aus `.preview/index.html` und sind mit einem Lauf neu erzeugt,
falls sich an der Oberfläche noch etwas ändert.

## 2026-10-08 — Firmware 0.2.0 gebaut und für den Installer bereitgelegt

**Gebaut:** `pio run -e esp32dev_core2`, sauberer Durchlauf von Null.
**0 Fehler, 0 Warnungen** mit `-Wall`. RAM 15,2 %, Flash **70,3 %**
(vorher 69,8 % — die neue Oberfläche kostet gut 6 kB).

**Zwei Hürden, beide auf diesem Rechner, beide jetzt im Skript abgefangen**

1. **TLS.** Der Build brach mit `CERTIFICATE_VERIFY_FAILED` ab: zwischen
   PlatformIO und GitHub sitzt ein Scanner, der TLS aufbricht, und dessen
   Wurzelzertifikat kennt Pythons `requests` nicht. `UV_SYSTEM_CERTS` half
   nicht — das gilt nur für `uv`, hier scheiterte PlatformIOs eigener
   Download. Gelöst, ohne die Prüfung abzuschalten: aus dem
   Windows-Zertifikatsspeicher wird ein Bündel erzeugt (81 Zertifikate,
   dazu `certifi`) und über `REQUESTS_CA_BUNDLE` untergeschoben.
2. **Cache-Pfad.** `PLATFORMIO_CACHE_DIR='C:\pioc'` legt unter Git Bash
   einen relativen Ordner `Firmware/pioc/` an statt `C:\pioc` zu benutzen.
   Mit Vorwärtsschrägstrichen stimmt es.

**Neues Skript
[`Firmware/baue_und_veroeffentliche.sh`](Firmware/baue_und_veroeffentliche.sh)**

Zwischen „kompiliert" und „mit dem Installer installierbar" liegen zwei
Schritte, die man leicht vergisst. Das Skript nimmt sie mit:

| Offset | Teil |
|---|---|
| `0x01000` | Bootloader |
| `0x08000` | Partitionstabelle |
| `0x0e000` | `boot_app0` |
| `0x10000` | die Anwendung |

Das `manifest.json` nennt **einen** Teil bei Offset 0 — also muss alles in
ein zusammengefügtes Abbild. Nur `firmware.bin` hochzuladen hieße: Gerät
ohne Bootloader, bootet nicht mehr. Dazu zieht das Skript auf Wunsch die
Version im Manifest nach.

**Ergebnis:** `docs/firmware/marsrover-esp32.bin`, 993 376 Byte, Aufbau
Byte für Byte gegen das bisher veröffentlichte Abbild geprüft.
Manifest auf **0.2.0**.

> **Sichtbar wird das erst nach einem Push.** Der Installer liest die
> Dateien von `darklirah.github.io`.

## 2026-10-08 — Der Roboter heißt überall Mars Rover

Bisher stand „Bristlebot" verstreut in Doku, Firmware und Ordnernamen, weil
der Begriff am 05.10. ausdrücklich als Bauartbezeichnung stehenbleiben
sollte. **Diese Regel ist aufgehoben.** Der Begriff steht jetzt nur noch in
**je einem erklärenden Absatz** in [README](README.md) und
[Doku/00](Doku/00_Projektbeschreibung.md), der die Verwandtschaft nett und
verständlich beschreibt — mit einer kleinen Gegenüberstellung, was der Mars
Rover mehr kann. Überall sonst heißt er Mars Rover.

**Umbenannt**

| vorher | nachher |
|---|---|
| `Firmware/bristlebot/` | `Firmware/MarsRover/` |
| `bristlebot.ino` | `MarsRover.ino` |
| `src_dir = bristlebot` in `platformio.ini` | `src_dir = MarsRover` |
| Kopfkommentare in 12 Firmware-Dateien | auf `MarsRover` |
| Pfadangaben in Doku 05, 06, 07 und README | auf den neuen Ordner |

> **Für den nächsten Build:** der Ordnername hat sich geändert, PlatformIO
> baut deshalb einmal komplett neu. `Firmware/.pio/` darf dafür weg, muss
> aber nicht — es ist ohnehin gitignoriert.
>
> Der Ordnername musste mitwandern, weil die Arduino IDE verlangt, dass
> Ordner und `.ino`-Datei gleich heißen.

**Zwei echte Fehler gefunden, nicht nur Namen**

Beim Durchgehen fiel auf, dass die Dokumentation an zwei Stellen ein
**Passwort nannte, das die Firmware gar nicht mehr benutzt**:

| Stelle | stand da | richtig ist |
|---|---|---|
| [Doku/06 §Benutzung](Doku/06_Fernsteuerung-App.md) | WLAN `Bristlebot`, Passwort `bristlebot` | WLAN `MarsRover_…`, Passwort `marsrover` |
| [docs/index.html](docs/index.html) (Web-Installer) | Passwort `bristlebot` | Passwort `marsrover` |

In `Config.h` steht seit Längerem `AP_PREFIX = "MarsRover"` und
`AP_PASSWORD = "marsrover"`. Wer sich an die Doku gehalten hätte, wäre nicht
ins WLAN gekommen. Ebenfalls nachgezogen: das Code-Beispiel in Doku/06 zeigte
noch ein `AP_SSID`, das es nicht mehr gibt, und die erwartete
Konsolenausgabe in [Doku/07](Doku/07_Inbetriebnahme-und-Tuning.md).

**Nicht angefasst: die älteren Einträge in diesem Log.** Das Repo hieß
damals wirklich `Darklirah/Bristlebot` und das Verzeichnis `Bristlebot/` —
ein Protokoll, das rückwirkend umgeschrieben wird, ist als Protokoll
wertlos. Der Eintrag vom 05.10., der die alte Regel festlegte, hat einen
Nachtrag bekommen, der auf ihre Aufhebung verweist.

---

## 2026-10-07 — Wärmefallen an der Massefläche

Die Massefläche hing **fest** an den Pads (`connect_pads yes`, vom Router so
gesetzt). Eine 70 × 52 mm große Kupferfläche zieht beim Handlöten die Wärme
schneller ab, als ein Lötkolben sie nachliefert — das Ergebnis sind kalte
Lötstellen, die beim Messen oft noch leitend wirken und erst bei Vibration
ausfallen. Auf diesem Gerät also garantiert.

Umgestellt auf **Wärmefallen**: Spalt 0,4 mm, vier Stege à 0,5 mm. Die
vorhandenen Werte waren mit je 0,2 mm zu knapp und wurden ohnehin nicht
benutzt.

| | |
|---|---|
| Betroffen | die **20 bedrahteten** Masse-Pads, die die Fläche direkt berühren |
| Nicht betroffen | die **16 SMD-Masse-Pads** auf der Oberseite — sie hängen über eine kurze Leitung und eine Durchkontaktierung an der Fläche, berühren sie also gar nicht |
| Elektrisch | vier Stege à 0,5 mm auf 35 µm tragen zusammen rund 6 A. Größter Verbraucher ist der Step-Up mit knapp 0,8 A, und der hat zwei Pads — Faktor fünfzehn Reserve |
| Geprüft | DRC 0 unverbundene Elemente, 0 Abstandsverstöße. Das B.Cu-Gerber wuchs um 38 KB, genau die zusätzliche Geometrie der Freistellungen |

Fertigungsdaten neu erzeugt — das B.Cu-Gerber hat sich geändert.

---

## 2026-10-07 — Siebdruck aufgeräumt, Fertigungsdaten erzeugt

**Bestückungsdruck: von 96 Verstößen auf null**

| | vorher | nachher |
|---|---|---|
| `silk_overlap` | 60 | **0** |
| `text_height` | 32 | **0** |
| `silk_over_copper` | 4 | **0** |
| `silk_edge_clearance` | 0 | **0** |

Drei Eingriffe:

1. **45 Wertefelder ausgeblendet.** Der Wert steht in der Stückliste; auf dem
   Siebdruck kostet er nur Platz. Das Wertefeld von U1 lag auf dem Pad von C7.
2. **Die 38 Pinnamen des DevKitC-Footprints auf F.Fab verschoben.** Sie stehen
   auf 2,54 mm Raster, sind 0,7 mm hoch — unter der 0,8-mm-Regel — und jeder
   Name ist länger als sein Rastermaß. Gedruckt gäbe das einen Schmierer, und
   das aufgesteckte Modul deckt sie ohnehin zu; auf dem Modul selbst stehen
   dieselben Namen lesbar drauf. Auf F.Fab bleiben sie in der
   Bestückungszeichnung erhalten.
3. **Alle 45 Referenzen** auf 0,8 mm gesetzt und neu platziert. Die Suche
   probiert ein dichtes Raster um das Bauteil, nach Abstand sortiert, und
   nimmt den nächstgelegenen Platz, der weder ein Pad noch eine andere
   Siebdruckspur noch den Platinenrand berührt. Feste Ringe reichten nicht:
   in den Ecken sprang ein 0,4-mm-Schritt über die letzte Lücke hinweg.

**Drei Durchkontaktierungen vergrößert**, von 0,5/0,3 auf 0,7/0,4 — 0,1 mm
Restring war die Untergrenze der günstigen Fertiger. Eine davon musste bei
0,6/0,4 bleiben, sonst kam sie einer Signalleitung auf 0,175 mm nahe.

**Fertigungsdaten unter [`Fertigung/`](Fertigung/README.md)**

Gerber (9 Lagen), beide Bohrdateien mit Bohrplänen, Stückliste,
Bestückungsdaten, Pastenschablone (nur Oberseite, 44 Öffnungen auf 21
Bauteile — unten sitzt kein SMD) und das STEP-Modell der nackten Platine.
Erzeugt von [`erzeuge_fertigungsdaten.sh`](Fertigung/erzeuge_fertigungsdaten.sh),
damit es nach jeder Platinenänderung wiederholbar ist.

Das vollständige STEP **mit** Bauteilen (23 MB) bleibt lokal unter
`local_Step Files/` — es enthält Fremdmodelle aus den KiCad- und
Espressif-Bibliotheken.

**Offen: die Oberfläche.** HASL oder ENIG ist noch nicht entschieden. Bei 21
SMD-Bauteilen über eine Pastenschablone spricht einiges für ENIG, weil HASL
eine ungleichmäßige Lotbeule auf jedem Pad hinterlässt und die Schablone
darauf kippelt.

---

## 2026-10-07 — U5 blockierte den USB; Routingwerkzeug dauerhaft eingerichtet

**Gemacht**

- **U5 an die Hinterkante.** Pad 1 von U1 ist 3V3 (Antennenende), Pad 19 ist
  5V — der Micro-USB sitzt also am +x-Ende bei x ≈ 154, mittig auf der
  Modulbreite bei y = 85. U5 stand mit y 81,2…88,8 **genau davor**. Jetzt
  y 97,0…104,62, Gehäusevorderkante 95,2, gut 4 mm Luft zum Steckergehäuse.
- Dafür mussten **R16/R17** (Spannungsteiler VBAT → GPIO39) von x 156,5/160,5
  nach x 150/154 wandern. Als 0805 dürfen sie überall in den hinteren Streifen.
- Neu geroutet: 27/27 Netze, 91/91 Padpaare, 91 Durchkontaktierungen,
  **0 unverbundene Elemente, 0 Abstandsverstöße, 0 lose Leitungsenden**.

**Werkzeug dauerhaft eingerichtet** (gehört in die HowTo-Datei)

| | |
|---|---|
| CLI + Quelle | `C:\Users\Frank-PC-AMD\Tools\KiCadRoutingTools` |
| KiCad-Plugin | `~\Documents\KiCad\10.0\3rdparty\plugins\KiCadRoutingTools` |
| Aufruf in KiCad | **Tools → External Plugins → KiCadRoutingTools** |
| Nachinstalliert in KiCads Python | `scipy`, `shapely` (numpy und Pillow waren da) |

Damit lässt sich das Routing auch **aus dem offenen PCB-Editor heraus**
starten — das Ergebnis steht danach direkt im Editor, mit Undo.

---

## 2026-10-07 — Platine geroutet: 27 von 27 Netzen, null unverbundene Elemente

**Gemacht**

- Platzierung nachgezogen: J2 als **liegender** Stecker
  (`JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal`) auf die **Unterseite**, weil der
  Akku unter die Platine kommt und ein stehender Stecker in den 5-mm-Spalt
  ragen würde; OS1/OS2 auf optimalen Abstand; U6 hinten mittig; S1 daneben.
- **Geroutet** mit [KiCadRoutingTools](https://github.com/drandyhaas/KiCadRoutingTools)
  (A\*-Router mit Rust-Kern, MIT, headless auf der `.kicad_pcb`).
  Ergebnis: **27/27 Netze, 91/91 Padpaare, 101 Durchkontaktierungen,
  0 unverbundene Elemente, 0 Abstandsverstöße, 0 Kurzschlüsse.**
- Massefläche auf **B.Cu**, eine zusammenhängende Insel, 1,0 mΩ über 86 mm.

**Entscheidungen**

- **Sensorabstand OS1/OS2:** Die Fototransistoren zeigen nach innen und stehen
  12,5 mm auseinander. Maßgeblich ist aber der **optische Messfleck**, der
  jeweils mittig zwischen LED und Transistor liegt — die stehen damit
  **18 mm** auseinander und liegen im von [Doku/04](Doku/04_PCB-Layout-Empfehlung.md)
  geforderten Fenster 15–20 mm für ein 19-mm-Band.
- **Kein Ausschnitt für den MPU-6050.** Ein Gyroskop misst die Drehrate eines
  starren Körpers an jedem Punkt gleich; nur der Beschleunigungsmesser sieht
  Zentrifugalterme, und die betragen bei 180 °/s und 30 mm Abstand 0,03 g —
  zwei Größenordnungen unter der Motorvibration. Ein 22 × 17-mm-Loch mitten in
  einer 1 mm dünnen Platte hätte also Steifigkeit und Massefläche gekostet,
  ohne messbar etwas zu bringen. Damit ist Regel 1 aus Doku/04 §6 („nahe der
  Drehachse") die **schwächste** der drei; Regel 2 (weit weg von den Motoren)
  und Regel 3 (weich ankoppeln) bleiben.
- **Keine Durchkontaktierung in einem Pad.** Der erste Lauf setzte 16 Vias
  mitten in SMD-Pads. Das verlangt IPC-4761 Typ VII (gefüllt und überplattet);
  beim Handlöten saugt es sonst das Lot in die Hülse. Mit
  `--same-net-pad-clearance 0.2` sind es null.

**Zwei Fehlschläge, beide Platzierung statt Routing**

- R2 Pad 1 hatte links und rechts je **0,8 mm** Padabstand — genau die Breite,
  die eine 0,4-mm-Leitung mit zweimal 0,2 mm Abstand braucht, also null
  Spielraum. Daran scheiterten beide Router. R2 um 0,5 mm und Q2 um 0,6 mm
  nach außen hat es gelöst. *(Erster Versuch mit 1 mm war zu viel und legte
  R2 Pad 2 auf das Massepad von Q2 — vom DRC gefunden.)*
- J2 deckte in der ersten Stellung die Unterseiten-Pads von LED3 und R11 ab.
  Auf der Unterseite ist das kein Gehäuse-, sondern ein **Löt**problem.

**Abweichungen von der Breitenvorgabe, bewusst**

| Netz | Soll | Dünnste Stelle | Länge dort |
|---|---|---|---|
| +5V | 1,0 mm | 0,40 mm | 10,3 von 194 mm |
| +3V3 | 0,8 mm | 0,40 mm | 5,6 von 177 mm |
| GND (Zuleitungen) | 1,0 mm | 0,33 mm | 33 von 66 mm |
| Net-(D1-A) | 1,0 mm | 0,40 mm | 15,7 von 35 mm |

Das sind **Einschnürungen am Pad**: eine 1-mm-Leitung passt nicht in ein
0805-Pad von 1,2 mm Breite, wenn der Nachbar 0,8 mm entfernt ist. 0,4 mm auf
35 µm tragen nach IPC-2221 **1,23 A** bei 10 K Erwärmung; die Motoren ziehen
zusammen rund 0,3 A. +3V3 wurde bewusst mit 0,8 statt 1,0 mm angefordert — es
trägt nur die Sensorik (gut 40 mA), und 1 mm hätte Querungen gefressen, die
die Signale brauchen.

**Offen**

- Siebdruck: 58 Überlappungen und 32 zu kleine Texte. Rein kosmetisch, aber
  vor der Bestellung aufzuräumen.
- 21 Courtyard-Überlappungen und 4 THT-Pads im Courtyard: alle unter dem
  gesockelten DevKit, also gewollt.

---

## 2026-10-07 — MT3608 bekommt einen Festteiler statt des Potis

**Gemacht**

- [Doku/07](Doku/07_Inbetriebnahme-und-Tuning.md): Schritt 1 in **1a und 1b**
  geteilt. 1a beschreibt den Modulumbau, 1b nur noch das Nachmessen.
- [Doku/03](Doku/03_Stueckliste-BOM.md): U5 ist jetzt als Umbauteil
  gekennzeichnet, die zwei Teilerwiderstände stehen als referenzlose Position
  in der Liste (sie gehören aufs Modul, nicht auf die Platine). Einkaufsfalle 3
  umformuliert.
- [Doku/04](Doku/04_PCB-Layout-Empfehlung.md): Siebdruck-Hinweis angepasst —
  „SET 5V0 neben dem Trimmer" stimmt nicht mehr, der Trimmer ist weg.

**Entscheidung: Trimmpoti am MT3608 auslöten, 110 kΩ / 15 kΩ einsetzen**

Zwei Gründe, der zweite ist der wichtigere:

1. Das Poti ist das höchste Bauteil des Moduls und steht im Weg, sobald das
   Modul als senkrechte Finne montiert wird.
2. Ein Schleifkontakt auf einem Fahrzeug, dessen Antriebsprinzip Vibration
   ist, verstellt sich. Verstellt er sich nach oben, hängt das DevKit an
   mehr als 5 V.

Gerechnet über die 0,6-V-Referenz des MT3608:
0,6 V × (1 + 110 kΩ / 15 kΩ) = 0,6 × 8,333 = **5,00 V**.

**Fallstrick, der dokumentiert ist:** Der werkseitige untere
Rückkopplungswiderstand des Moduls muss raus. Bleibt er liegen, steht er
parallel zu den 15 kΩ und die Ausgangsspannung steigt.

**Geprüft**

- Schaltplan nach der Nutzer-Bearbeitung gegengerechnet: Netzliste Knoten für
  Knoten gegen den Vorstand verglichen, **keine Abweichung außer den von mir
  nachträglich eingefügten Entkoppelkondensatoren**. ERC: 0 Fehler,
  2 bekannte kosmetische Warnungen an D1/D2.

---

## 2026-10-06 — Schaltplan neu aufgebaut: Bereiche und gezeichnete Leitungen

**Gemacht**

- Schaltplan vollstaendig neu aufgebaut, Blatt jetzt **A2** statt A3:
  **175 gezeichnete Leitungen, 25 Knotenpunkte, null Netzlabels**
- Fuenf beschriftete Bereiche: Rechenkern · Motortreiber · Sensoren
  Linienerkennung · Sensoren Lage und Abstand · Signal-LEDs · Akku und
  Ladevorrichtung
- Neues Werkzeug `pcb/build_schematic.py`. Die acht Lagen (vier Drehungen,
  zwei Spiegelungen) sind am lebenden KiCad **ausgemessen**, nicht geraten;
  das Skript prueft am Ende selbst, ob jede Koordinate auf dem
  1,27-mm-Raster liegt.
- `pcb/gen_schematic.py` ist **gesperrt** — ein Lauf bricht jetzt mit einer
  Meldung ab, statt den Schaltplan mit der alten Fassung zu ueberschreiben.
  Die Datei bleibt als Beleg der Netzliste liegen.
- Geprueft: ERC **0 Fehler**, keine verwaisten Leitungen, keine
  Ueberlappungen, Netzliste knotengenau gegen den Entwurf abgeglichen.
- Zwei echte Zeichenfehler gefunden und behoben: Leitungen liefen quer
  durch die Gehaeuse von U2 und U5 hindurch.

**Entscheidungen**

- **Keine MOSFETs fuer die LEDs.** Nachgesehen im ESP32-WROOM-32-Datenblatt
  v3.8, Tabelle 14: I_OH typisch **40 mA** je Pin in der Domaene
  VDD3P3_RTC, bei mehreren gleichzeitig treibenden Pins noch rund 29 mA
  (Fussnote 2). Alle vier LED-Pins — GPIO 14, 25, 26, 27 — liegen in dieser
  Domaene. Vorwiderstand bleibt **220 Ohm**, rund 5 mA je LED.
  Das spart zwoelf Bauteile auf einer Platine, deren groesstes Risiko die
  Masse ist. Die 40 mA gelten allerdings nur bei maximaler Treiberstaerke;
  die Voreinstellung von Arduino und ESP-IDF ist Stufe 2 mit etwa 20 mA.
- **Versorgung ueber Power-Symbole**, nicht als durchgezogene Leitung.
  GND, +5V und +3V3 quer ueber ein A2-Blatt zu ziehen waere unleserlicher,
  nicht lesbarer. Je Netz ein PWR_FLAG an der Quelle.
- **Netznamen** sind jetzt automatisch vergeben (`Net-(D1-A)` statt
  `MOT_L_D`). Fuer das Platinenlayout waeren sprechende Namen nuetzlich —
  ein Label auf einer bereits gezeichneten Leitung *benennt* nur, es
  *verbindet* nicht. Offen, siehe unten.
- Verbleibende Kreuzungen sind gewollt und ohne Knotenpunkt, also
  elektrisch nicht verbunden: zwei am I2C-Bus (bei zwei Teilnehmern an
  einem Zweidrahtbus nicht vermeidbar), zwei im Akkubereich, weil BAT+
  zwischen zwei Massepins des Lademoduls liegt.

**Offen**

- [ ] Sprechende Netznamen? Nur benennend, die Verdrahtung bleibt gezeichnet
- [ ] Zwei ERC-Warnungen `lib_symbol_mismatch` an D1/D2 — kosmetisch, Folge
      des Aufloesens der Symbolvererbung (1N5819 erbt von SB120)

**Als Naechstes**

Review durch den Nutzer in KiCad, dann das Platinenlayout.

---

## 2026-10-05 (7) — KiCad-MCP-Server, Schaltplan wird neu aufgebaut

**Gemacht**

- Schaltplan-Entwurf durchgesehen und **verworfen**: Bauteile wild über das
  Blatt verteilt, Verbindungen ausschließlich über Netzlabels
- [KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) v2.8.2
  (MIT) nach `C:\Users\Frank-PC-AMD\Tools\KiCAD-MCP-Server` installiert und
  in `~/.claude.json` unter dem Projekt „HA Claude" eingetragen.
  Geprüft: 244 Werkzeuge, `pcbnew 10.0.0` startet sauber
- KiCads Sperrdatei `*.lck` aus der Versionierung genommen — war versehentlich
  eingecheckt. Ebenso ignoriert: `.history/`, `pcb/Bilder/`

**Entscheidungen**

- **Der Schaltplan wird in Bereiche gegliedert:** Rechenkern, Motortreiber,
  Sensorik, Akku und Ladevorrichtung. Innerhalb der Bereiche **gezeichnete
  Leitungen**, keine Netzlabels. Vorgabe des Nutzers, nicht verhandelbar.
- **Werkzeugwechsel:** `pcb/gen_schematic.py` wird **nicht mehr ausgeführt**.
  Es erzeugt die Datei komplett neu und überschreibt damit jede Handarbeit.
  Es bleibt als Beleg der Netzliste liegen. Künftig gezielte Einzeleingriffe
  über den MCP-Server — dadurch überleben manuelle Änderungen im
  Schaltplaneditor.
- **Regel für die Zusammenarbeit an der Datei: immer nur einer schreibt.**
  Vor jedem Schreibzugriff wird geprüft, ob eine `*.lck` im `pcb/`-Ordner
  liegt; dann hat KiCad die Datei offen und sie wird nicht angefasst.
  Ungespeicherte Änderungen im Editor sind von außen unsichtbar — erst
  speichern, dann übergeben.
- KiCad **10** bleibt. Kein Wechsel auf 11: das ist derzeit ein Nightly, das
  Dateiformat ist eine Einbahnstraße, und das Platinenlayout läuft auf 10
  bereits live über die IPC-Schnittstelle.
- Der Review-Screenshot bleibt **lokal**, kommt nicht ins Repo.

**Offen — zum Projektabschluss, vom Nutzer bestellt**

- [ ] **HowTo-Datei** mit allen benutzten Schnittstellen und ihrer
      Einrichtung, damit Nachbauer dieselbe Umgebung herstellen können.
      Mindestens: PlatformIO samt der drei nötigen Umgebungsvariablen
      (`UV_SYSTEM_CERTS`, `UV_NATIVE_TLS`, `PLATFORMIO_CACHE_DIR`), der
      KiCAD-MCP-Server samt Konfiguration, ESP Web Tools und GitHub Pages,
      die Datenblattquellen aus [Doku/10](Doku/10_Datenblaetter.md)
- [ ] **Fertiger Prompt für Claude**, der alle benötigten Werkzeuge und
      Schritte ermöglicht, um diese Arbeiten durchzuführen — mit
      ausführlicher Erklärung jedes einzelnen Schritts. So geschrieben,
      dass jemand mit leerer Claude-Sitzung und leerem Rechner bis zum
      fahrenden Roboter kommt und dabei versteht, *warum* jeder Schritt
      nötig ist. Gehört mit der HowTo-Datei zusammen gedacht: die eine
      beschreibt die Umgebung, der andere setzt sie in Gang.

**Als Nächstes**

Schaltplan neu aufbauen, Bereich für Bereich, mit gezeichneten Leitungen.
Danach ERC, SVG zum Durchsehen, dann das Platinenlayout.

---

## 2026-10-05 (6) — MOSFET statt Bipolartransistor, Datenblätter, KiCad-Start

**Frage:** Wäre ein MOSFET als Ersatz für den BC337 nicht sinnvoller?

**Antwort: ja — aber nicht wegen des Wirkungsgrads.** Der entscheidende
Punkt ist der Spannungsabfall. Der BC337 frisst 0,25 V von der 5-V-Schiene,
das sind rund **8 % der Motorspannung**, die nicht in Vibration umgesetzt
werden. Bei einem Roboter, dessen größtes Risiko „zu schwer, fährt
vielleicht nur kriechend" lautet, wirkt das direkt auf die Schwachstelle.

**Entschieden: AO3400A** (SOT-23, 28 mΩ bei 4,5 V Gate, 5,7 A, ~10 ct).
Verworfen: IRLZ44N in TO-220 — elektrisch top, aber 2 g je Stück bei einem
Roboter, bei dem um Gramm gekämpft wird.

Gewarnt und dokumentiert: **2N7000, BS170 und IRF540 taugen hier nicht.**
Ihr R_DS(on) ist für 10 V Gate-Spannung spezifiziert; an 3,3 V sind sie kaum
durchgesteuert. Klassischer Anfängerfehler, steht jetzt in Review B10.

Nachgezogen: Stückliste, Netzliste (Gate/Drain/Source statt Basis/Kollektor/
Emitter), Pinbelegung, Layoutempfehlung, Datenblattliste, README und das
Generator-Skript. Gate-Widerstand 100 Ω statt 1 kΩ, Pulldown 100 kΩ statt
10 kΩ. **Die Firmware ändert sich nicht.**

**Datenblätter.** `docs/` ist der von GitHub Pages veröffentlichte Ordner,
keine Dokumentenablage — das dort abgelegte AZ-Datenblatt ist nach
`Datasheets/` gewandert und per `.gitignore` aus dem Repo gehalten.
Stattdessen eine Linkliste ([Doku 10](Doku/10_Datenblaetter.md)): jeder kommt
an jedes Dokument, und zwar an die aktuelle Fassung beim Hersteller statt an
eine eingefrorene Kopie.

**KiCad.** Live-Verbindung zur laufenden Instanz steht (IPC-API, `kipy`).
Ordner `pcb/` mit eigener Bibliothek (TCRT5000-Symbol, von KiCad geprüft)
und der offiziellen Espressif-Bibliothek. Generator-Skript für den
Schaltplan angelegt, Stufe 1 (Rechenkern + Motorstufe) ist beschrieben.

**Nächster Schritt:** Generator laufen lassen, Format gegen ERC prüfen, dann
die restlichen rund 30 Bauteile ergänzen.

---

---

## 2026-10-05 (5) — Umbenannt, kompiliert, Web-Installer

**Projekt heißt jetzt „One-of-a-Kind Mars Rover".** „Bristlebot" bleibt in
der Technikdoku als Bezeichnung der Bauart stehen.

> *Nachtrag vom 08.10.2026: diese Regel ist aufgehoben. Der Begriff steht
> jetzt nur noch in je einem erklärenden Absatz in README und
> Projektbeschreibung, sonst heißt der Roboter überall Mars Rover.*

**Erfolgreich kompiliert — erstmals.**

```
RAM:   15.2 % (49.784 von 327.680 Bytes)
Flash: 69.8 % (914.437 von 1.310.720 Bytes)
0 Fehler, 0 Warnungen (mit -Wall)
```

Gebaut gegen `espressif32@6.9.0` (offizielle Plattform, Arduino-Core 2.x),
neue Umgebung `esp32dev_core2` in der `platformio.ini`. Damit ist auch der
Core-2.x-Pfad der Firmware bestätigt.

**Drei Hürden auf dem Weg dahin — alle in der Umgebung, keine im Code:**

1. **`uv` lehnt GitHub-Zertifikate ab** (`invalid peer certificate:
   UnknownIssuer`), während `curl` dieselbe Adresse mit HTTP 200 erreicht.
   Klassische Signatur eines TLS-aufbrechenden Virenscanners oder Proxys.
   Abhilfe: `UV_SYSTEM_CERTS=1` **und** `UV_NATIVE_TLS=1` (ältere
   uv-Versionen kennen nur die zweite). Die Plattform verschluckt den
   Fehler zusätzlich, weil sie die uv-Ausgabe nach DEVNULL wirft.
2. **Windows-Pfadgrenze**, exakt 260 Zeichen erreicht beim Entpacken von
   `esp32-arduino-libs`. `LongPathsEnabled` steht auf 0. Abhilfe ohne
   Registry-Eingriff: `PLATFORMIO_CACHE_DIR=C:\pioc`.
3. **Der pioarduino-Fork** (Plattform 55.03.37) scheitert reproduzierbar an
   seiner penv-Einrichtung, auch nachdem die Pakete manuell erfolgreich
   installiert wurden. Deshalb der Ausweichweg über die offizielle
   Plattform. Ungeklärt, aber umgangen.

**Neu: eindeutiger Netzname je Gerät.** Ab Werk `MarsRover_<MAC-Kennung>`,
damit mehrere Rover nebeneinander funktionieren, ohne dass jemand etwas
einstellt. Im Experten-Bereich lässt sich ein eigener Name vergeben
(`MarsRover_Petra`), gespeichert im NVS, aktiv nach einem Neustart, den die
Oberfläche gleich mit auslöst. Neue Protokollbefehle `N|<name>` und `Z`.

**Neu: Web-Installer.** `docs/` enthält eine Installationsseite mit ESP Web
Tools, `manifest.json` und die zusammengeführte Binärdatei
(`marsrover-esp32.bin`, 986 KB, Offset 0x0). GitHub Pages muss noch
eingeschaltet werden. Web Serial gibt es nur in Chrome, Edge und Opera auf
dem Desktop — nicht auf Handys, nicht in Firefox und Safari.

**Neu: `Doku/00_Projektbeschreibung.md`** — ausführliche Beschreibung des
Projekts und aller Funktionen, mit einem langen Kapitel zum Programmieren
(Zeitmodell, alle Befehle, Vorgehen, vier Beispiele vom Lichtspiel bis zum
selbsttätigen Ausweichen, typische Fehler, Grenzen).

**Nächste Sitzung:**

- [ ] GitHub Pages einschalten, Installationsseite prüfen
- [ ] Repo und lokalen Ordner auf `One-of-a-Kind-Mars-Rover` umbenennen
- [ ] 3D-Basismodul entwerfen — Anforderungen stehen in
      [Doku 00 §8](Doku/00_Projektbeschreibung.md). **Platine und Basismodul
      gehören zusammen entworfen**, der endgültige Platinenumriss ist bis
      dahin offen
- [ ] Bauanleitung mit Bildern, entsteht beim Bau des ersten Exemplars
- [ ] Teile bestellen, aufbauen, Funktionstest fahren

---

## 2026-10-05 (4) — Stromversorgung geprüft, LiPo bestätigt

**Frage:** Spart ein Halter mit Schalter für 3× AAA plus Buck-Boost Gewicht?

**Antwort: nein, er kostet ~36 g.** 3× AAA samt Halter wiegen ≈ 52 g gegen
≈ 14 g der LiPo-Lösung; die Gesamtmasse stiege von ~45 g auf ~85 g. Dazu
schlechtere Energiedichte (doppelte Energie für 3,7-fache Masse) und
0,9 Ω Innenwiderstand in Reihe, was bei den 1-A-Spitzen des ESP32 um 0,9 V
einbricht. Vollständige Rechnung in [Doku 02 §7](Doku/02_SMD-vs-THT-Wirtschaftlichkeit.md).

**Entscheidung des Auftraggebers:** LiPo bleibt wie geplant. Über den
**Buck-Boost direkt auf 3,3 V** (≈ 90 % statt ≈ 56 % Wirkungsgrad, rund ein
Drittel mehr Laufzeit, kein Mehrgewicht) wird erst entschieden, **wenn der
erste Aufbau fährt** — die Massefrage ist bislang gerechnet, nicht gemessen.

**Nicht erledigt, bewusst offen:**

- [ ] Buck-Boost auf 3,3 V nach dem ersten Fahrversuch bewerten. Haken dabei:
      Rückwärtseinspeisung in den AMS1117 des DevKits, USB und Akku dürfen
      dann nicht gleichzeitig anliegen
- [ ] Sicherheitsvorgabe für den Aufbau: geschützte Zelle, vollständig im
      Gehäuse, keine freien Kontakte, Laden nicht unbeaufsichtigt

---

---

## 2026-10-05 (3) — Lagesensor und Abstandssensor

**Frage des Auftraggebers:** Bringt ein MPU-6050 Genauigkeit? Und wäre ein
GY-511 (LSM303DLHC) auf einem Mast wie bei Curiosity besser?

**Antwort und Entscheidung**

- MPU-6050: **ja, für Drehungen — nein, für Strecken.** Zweifache Integration
  der Beschleunigung ist auf einem vibrationsgetriebenen Roboter binnen ein
  bis zwei Sekunden unbrauchbar.
- LSM303DLHC **abgelehnt**: hat kein Gyroskop, sondern Beschleunigung +
  Magnetometer. Für „drehe um 90°" braucht es die Drehrate. Der Mast wäre
  physikalisch richtig gedacht (Störfeld fällt mit 1/r³, 20 → 80 mm sind
  64× weniger), löst aber ein Problem, das bei Manövern von Sekunden gar
  nicht auftritt: die Gyro-Drift liegt dabei unter 1°.
- Stattdessen: **MPU-6050 flach aufs Chassis + VL53L0X auf den Mast.** Der
  ToF-Sensor verträgt die Mastschwingung, weil er über sein Messfenster
  mittelt — ein Magnetometer dagegen verlöre dort seine Ausrichtung, und
  die ist bei einem Kompass die Messgröße.

**Umgesetzte Funktionen** (vom Auftraggeber ausgewählt)

Lagesensor: Drehen nach Winkel · Geradeauslauf halten · Kipp- und
Aufheb-Erkennung. Kursgeführte Liniensuche wurde verworfen.
Abstandssensor: fahren bis Hindernis · drehen bis frei · warten bis frei,
dazu ein abschaltbarer Hindernis-Stopp als Schutzfunktion.

**Gebaut**

- `Imu.*` — MPU-6050 ohne Fremdbibliothek. DLPF auf 21 Hz und Messbereiche
  bewusst grob (±8 g), weil ein übersteuernder MEMS-Sensor unter Vibration
  einen Gleichanteil erzeugt, der wie echte Neigung aussieht
- `Distance.*` — VL53L0X über die Pololu-Bibliothek. Gelesen wird nur, wenn
  der Chip ein Ergebnis gemeldet hat, sonst würde der Lesebefehl bis zu
  33 ms in der Hauptschleife stehen
- vier Warte-Flags im Interpreter zu **einem** Zustand `Await`
  zusammengefasst, bevor die Zustandsmaschine unübersichtlich wurde
- Funktionstest um beide Sensoren erweitert — er dreht sich dabei selbst
  einmal nach rechts und einmal nach links und prüft damit auch die
  **Drehrichtung** des Kreisels. Ein um 180° verdreht montierter Sensor
  fällt sonst erst beim ersten Fahrprogramm auf und sieht dort wie ein
  Programmierfehler aus
- Urteile im Klartext unter dem Testknopf

**Beide Sensoren sind optional.** Fehlen sie, läuft alles weiter: Drehbefehle
fallen auf eine Zeitschätzung zurück, Abstandsbefehle enden nach ihrer
Zeitgrenze. Die Oberfläche sagt das auch.

**Massefolge:** +4,5 g auf ~45 g, davon 2 g oben auf dem Mast. Das verschärft
das Hauptrisiko aus Doku 02 §4. Die dortige Abspeckliste holt ~6,5 g zurück.

**Weiterhin ungetestet** — nichts davon lief je auf Hardware.

---

---

## 2026-10-05 (2) — Fahrprogramm und Funktionstest

**Entscheidungen (vom Auftraggeber bestätigt)**

| Frage | Entscheidung |
|---|---|
| Zeitmodell | eigener `warte`-Befehl; Fahrbefehle setzen nur den Zustand |
| Kurvenradius | Stufe 1 = engste Kurve, Stufe 10 = weite Kurve |
| Speicherung | vier Slots im ESP32-Flash, je 48 Schritte |
| Editor | Baukasten mit Auswahlfeldern, kein Texteditor |
| Geschwindigkeit | **am Fahrbefehl**, kein eigener Tempo-Befehl (Korrektur im Nachgang) |
| Oberfläche | einfach bedienbar, geeignet ab 14 Jahren |

**Gebaut**

- `Program.*` — Parser mit Klartext-Fehlermeldungen, vier NVS-Slots,
  Interpreter mit Schrittbudget gegen Blockieren der Hauptschleife
- `SelfTest.*` — eingebauter Funktionstest: LEDs einzeln, alle blinkend,
  Motor links und rechts als Rampe. Bewusst **kein** Fahrprogramm: einzelne
  Motoren und Rampen lassen sich mit der Programmsprache nicht ausdrücken,
  und ein Diagnosewerkzeug soll keinen Speicherplatz belegen
- `Leds.*` um Override erweitert; Sicherheitsanzeigen behalten Vorrang
- dritter Modus in `bristlebot.ino`, neue Protokollbefehle `B`, `L`, `W`, `S`
- Oberfläche: drei Betriebsarten, Baukasten-Editor mit Schrittzähler je
  Slot, Farbcodierung, grüne Markierung des laufenden Schritts,
  Experten-Bereich zugeklappt
- Beispielprogramm „Achter" wird beim ersten Start automatisch angelegt
- Doku 08 neu, 06 und 07 nachgezogen

**Methodik**

Die Oberfläche wurde vor dem Festschreiben mit einem Daten-Stub im Browser
gerendert und am Bildschirm abgenommen (`.preview/`, gitignoriert).

**Weiterhin ungetestet** — nichts davon lief je auf Hardware.

---

## 2026-10-05 — Entwurf geprüft, Firmware und Doku gebaut

**Entscheidungen (vom Auftraggeber bestätigt)**

| Frage | Entscheidung | Verworfene Alternativen |
|---|---|---|
| Fernsteuerung | WLAN-AP + eigene Web-App | BLE + fertige App (Dabble/Bluefruit); beides parallel |
| Liniensensorik | 2× TCRT5000 analog | 1× Fototransistor; 5-Kanal-Array |
| ESP32-Bauform | DevKit 30-Pin THT, gesteckt | ESP32-WROOM-32E SMD; ESP32-C3-MINI-1 SMD |

**Geprüft und geändert** (Details: [Doku/01](Doku/01_Schaltplan-Review.md))

Fünf Blocker im Ausgangsentwurf:

1. `BluetoothSerial` ist klassisches SPP und auf iOS ohne MFi-Lizenz nicht
   nutzbar → WLAN-AP
2. dem Fototransistor fehlte die beleuchtende IR-LED → TCRT5000
3. ein einzelner Sensor kann nicht differentiell lenken → zwei Sensoren
4. GPIO 12 ist Strapping-Pin MTDI und kann das Booten verhindern → Motoren auf
   GPIO 32/33
5. USB-C ohne 2× 5,1 kΩ an CC1/CC2 bekommt keine 5 V → nachgetragen

Dazu neun Verbesserungen: Basis-Pulldowns gegen Motorzucken beim Booten,
Schottky statt 1N4148, zusätzliche Entkopplung, R_prog an die Zellgröße,
Akku 500 statt 150 mAh, Schalterposition hinter dem Ladepfad, Duty-Begrenzung
für 3-V-Motoren an der 5-V-Schiene.

**Gebaut**

- Firmware, modular: `Config.h`, `RobotState.h`, `Motors.*`, `LineSensor.*`,
  `Leds.*`, `RemoteControl.*`, `WebUI.h`, `bristlebot.ino`
- Web-App komplett inline im Flash (kein CDN — im AP-Betrieb gibt es kein
  Internet), Captive Portal, Totmannschalter, Live-Tuning, Telemetriebalken
- Doku 01–07 plus Netzliste als KiCad-Vorlage
- `platformio.ini` als Alternative zur Arduino IDE

**Bewusst offengelassen**

- Motoren hängen wie vom Auftraggeber entworfen an der **5-V-Schiene**. Die
  bessere Variante (an VBAT, entlastet den knappen MT3608 um 1 W und hält die
  Motorspitzen aus der ESP32-Versorgung) ist dokumentiert und in `Config.h` eine
  Zeile — aber nicht eigenmächtig umgesetzt, weil es den Schaltplan ändert.
- Der 56-%-Wirkungsgrad des Pfads MT3608 → AMS1117 bleibt. Abhilfe wäre ein
  3,3-V-Buck-Boost, der aber das Auslöten des bordeigenen Reglers erfordert.

**Größtes Risiko**

Masse ≈ 40 g. Funktionierende Bristlebots liegen bei 10–25 g. Es wird fahren,
aber kriechen, und die Lenkautorität ist bei hoher Masse gering. Abspeckliste
in [Doku/02 §4](Doku/02_SMD-vs-THT-Wirtschaftlichkeit.md); sofort umsetzbar
und kostenlos: PCB in 1,0 mm statt 1,6 mm bestellen, LEDs 3 mm statt 5 mm.

**Nichts davon ist in Hardware getestet.**

**Nächste Schritte**

- [ ] Teile bestellen (Stückliste [Doku/03](Doku/03_Stueckliste-BOM.md))
- [ ] Firmware einmal probeweise kompilieren, damit die Toolchain-Seite geklärt ist
- [ ] Schaltplan und Layout in KiCad zeichnen, Vorlage: [Netzliste](Hardware/Netzliste.md)
- [ ] Entscheidung Motoren an VBAT statt 5 V
- [ ] Inbetriebnahme nach [Doku/07](Doku/07_Inbetriebnahme-und-Tuning.md),
      Schritt für Schritt — nicht alles auf einmal einschalten
- [ ] Bewährte Kp/Kd/Grundvibration in `Config.h` zurückschreiben

---

## 2026-10-05 — Projekt angelegt

**Gemacht**

- Verzeichnis `Bristlebot/` im Ordner „HA Claude" erstellt
- Grundgerüst: `README.md`, `00_Projekt-Log.md`, `.gitignore`, `LICENSE` (GPL-3.0)
- Öffentliches GitHub-Repo `Darklirah/Bristlebot` angelegt und ersten Commit gepusht

**Entscheidungen**

- Sichtbarkeit: **öffentlich**, wie die anderen Projekte
- Lizenz: **GPL-3.0**
- Struktur: zunächst nur Grundgerüst, Projektart offen gelassen
