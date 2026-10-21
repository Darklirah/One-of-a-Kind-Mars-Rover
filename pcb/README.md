# Leiterplatte — KiCad-Quelldaten

> [!CAUTION]
> ## Revision 1 ist **nicht voll funktionsfähig** und wird überarbeitet
>
> Die Platine ist gebaut, und am Muster sind Fehler aufgefallen. **Diese
> Dateien enthalten sie noch.** Bitte nichts davon bestellen und keine
> Module danach verlöten.
>
> | Bauteil | Befund |
> |---|---|
> | **J2** Akkuanschluss | **verpolt**, muss 180° gedreht werden |
> | **U6** MPU-6050 | Stiftleiste 180° verdreht |
> | **U7** VL53L0X | Stiftleiste 180° verdreht, zusätzlich **SCK/SDA vertauscht** |
> | **U2** Lademodul | Pinbelegung passt nicht zum gekauften Modul; zwei Lötpads für OUT+/OUT− fehlen |
> | **U5** DC/DC-Wandler | Anschlussleiste passt nicht zum Modul |
> | **S1** Schalter | falsches Footprint |
>
> Vollständige Liste samt der geplanten Arbeiten:
> [Projekt-Log → Nächste Platinenrevision](../00_Projekt-Log.md#nächste-platinenrevision--befundliste-nutzer-21102026)
>
> **Das DRC läuft sauber durch — das sagt nichts über diese Fehler aus.**
> Es prüft, ob das Layout *in sich* stimmig ist: Abstände, Netze,
> Kurzschlüsse. Ob Pin 1 einer Stiftleiste dort liegt, wo das echte Modul
> ihn hat, kann es nicht wissen. Deshalb steht in der Befundliste als
> Gegenprobe: **Layout 1:1 ausdrucken und mit den Modulen vergleichen.**
>
> Die **Firmware ist nicht betroffen** — sie läuft auf einem nackten
> ESP32-DevKit.

---

## Was hier liegt

| Datei | Inhalt |
|---|---|
| `MarsRover.kicad_sch` | Schaltplan, A2, in Bereiche gegliedert, mit gezeichneten Leitungen |
| `MarsRover.kicad_pcb` | Layout, 70 × 52 mm, 2 Lagen, 1,0 mm |
| `MarsRover.kicad_pro` | Projekt samt Netzklassen und Entwurfsregeln |
| `MarsRover.kicad_sym`, `lib/`, `sym-lib-table` | eigene Symbole und Fußabdrücke |
| `build_schematic.py` | erzeugt den Schaltplan; die acht Lagen sind am lebenden KiCad ausgemessen |
| `gen_schematic.py` | **gesperrt** — überschriebe den Schaltplan mit der alten, labelverdrahteten Fassung. Liegt nur als Netzlisten-Beleg hier |
| `MarsRover.csv` | Stückliste aus dem KiCad-Dialog |

Die fertigen Gerber, Bohrdaten, Bestückungsdaten und die Pastenschablone
stehen in [`../Fertigung/`](../Fertigung/README.md) und werden von
`Fertigung/erzeuge_fertigungsdaten.sh` erzeugt — **nicht von Hand ändern.**

## Arbeitsregel

**Es schreibt immer nur einer.** Vor jedem Schreibzugriff prüfen, ob eine
Sperrdatei `~MarsRover.kicad_*.lck` in diesem Ordner liegt: dann hat KiCad
die Dateien offen, und von außen wird nichts angefasst. Ungespeicherte
Änderungen im Editor sind von außen ohnehin nicht sichtbar.
