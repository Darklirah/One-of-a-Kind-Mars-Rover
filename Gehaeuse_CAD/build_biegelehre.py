# Biegelehre fuer die Zahnbuerstenkoepfe -- parametrisches FreeCAD-Skript.
#
# WOZU
# Die gekauften Koepfe haben gerade Borsten. Ein Bristlebot faehrt aber in die
# Richtung, in die die Borsten geneigt sind -- mit geraden Borsten hat er keine
# Vorzugsrichtung und laeuft seitwaerts. Die Borsten muessen also dauerhaft
# geneigt werden, Spitzen nach VORN (zum Mast hin), und beide Koepfe gleich.
#
# WIE ES BENUTZT WIRD
#   1. Borstenfeld 20..30 s in etwa 90 Grad heisses Wasser halten.
#   2. Kopf mit den Borsten nach unten in den Schlitz schieben, bis er am
#      Anschlag steht. Der Schlitz ist niedriger als die Borsten lang sind --
#      sie werden dabei zusammengedrueckt und von der Reibung am Boden
#      entgegen der Schubrichtung umgelegt.
#   3. Lehre samt Kopf unter kaltes Wasser halten, bis alles kalt ist.
#   4. Kopf durch das Fenster im Anschlag mit einem Stift herausschieben.
#
# WICHTIG: die Spitzen zeigen hinterher entgegen der Schubrichtung. Der Pfeil
# auf der Seitenwand zeigt zum Anschlag; die spaetere FAHRTRICHTUNG des Rovers
# ist dem Pfeil ENTGEGENGESETZT. Deshalb steht der Pfeil fuer "so schieben",
# nicht fuer "so faehrt er".
#
# Koordinaten: X quer, Y = Schubrichtung (0 = Einschuboeffnung), Z = hoch,
#              Z = 0 ist die Pressflaeche, auf der die Borsten aufliegen.
import FreeCAD as App
import math
import Part

V = App.Vector

# ---------------- Bauteilmasse (aus build_bauteile.py, Teil 7) ----------------
KOPF_B   = 15.0      # Breite der Kopfplatte
KOPF_L   = 50.0      # Laenge des Kopfes
KOPF_D   = 6.0       # Dicke der Kopfplatte
BORST_L  = 12.0      # Laenge der Borsten
BORST_B  = 13.0      # Breite des Borstenfeldes

# ---------------- Einstellungen ----------------
WINKEL   = 25.0      # Formwinkel in Grad. Ziel sind 15..20 Grad; Nylon federt
                     # zurueck, deshalb 5 Grad steiler formen.
SPIEL    = 0.4       # Spiel in der Breite, damit der nasse Kopf noch gleitet
WAND     = 4.0       # Seitenwandstaerke
BODEN    = 4.0       # Materialstaerke unter der Pressflaeche
LIPPE    = 2.6       # wie weit die Haltelippe oben nach innen greift
LIPPE_D  = 4.0       # Dicke der Haltelippe
RAMPE    = 14.0      # Laenge der Einfuehrschraege
LUFT     = 2.0       # um wieviel die Schraege am Eingang hoeher anfaengt

# ---------------- Abgeleitet ----------------
# Der Schlitz ist genau so hoch, dass eine um WINKEL geneigte Borste
# hineinpasst: Fusspunkt oben, Spitze unten auf der Pressflaeche.
SPALT    = BORST_L * math.cos(math.radians(WINKEL))   # Boden .. Plattenunterseite
DECKE    = SPALT + KOPF_D                             # Boden .. Lippenunterseite
KANAL_B  = KOPF_B + SPIEL
GES_B    = KANAL_B + 2 * WAND
KANAL_L  = KOPF_L + RAMPE + 4.0                       # Platz zum Einschieben
GES_L    = KANAL_L + WAND                             # mit Anschlusswand
GES_H    = DECKE + LIPPE_D
FINGER_B = KANAL_B - 2 * LIPPE                        # Schlitz oben zum Nachschieben

doc = App.getDocument("MarsRover_Biegelehre") if "MarsRover_Biegelehre" in App.listDocuments() \
      else App.newDocument("MarsRover_Biegelehre")
for o in list(doc.Objects):
    doc.removeObject(o.Name)


def B(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


# ---------------- Grundkoerper ----------------
t = B(-GES_B / 2, GES_B / 2, 0, GES_L, -BODEN, GES_H)

# Kanal: vom Eingang bis zum Anschlag, Boden bis Lippenunterseite
t = t.cut(B(-KANAL_B / 2, KANAL_B / 2, -1, KANAL_L, 0, DECKE))

# Fingerschlitz im Dach -- zum Nachschieben und als Sicht auf den Kopf
t = t.cut(B(-FINGER_B / 2, FINGER_B / 2, -1, GES_L + 1, DECKE, GES_H + 1))

# Einfuehrschraege unter den Lippen: der Schlitz faengt am Eingang hoeher an
# und sinkt auf DECKE ab. Ohne sie muesste man die Borsten blind einfaedeln.
w = [V(-GES_B, 0, DECKE), V(-GES_B, RAMPE, DECKE), V(-GES_B, 0, DECKE + LUFT)]
t = t.cut(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(2 * GES_B, 0, 0)))

# Fenster im Anschlag: zum Herausschieben mit einem Stift. Es sitzt auf Hoehe
# der Kopfplatte, nicht der Borsten -- geschoben wird gegen die Platte.
t = t.cut(B(-4.0, 4.0, KANAL_L - 1, GES_L + 1, SPALT + 1.0, DECKE))

# Wasserrille in der Pressflaeche. Das Borstenfeld ist 13 mm breit und
# ueberspannt die 2 mm muehelos; das Wasser laeuft zum Eingang heraus.
t = t.cut(B(-1.0, 1.0, -1, KANAL_L, -0.8, 0.0))

# Anfasung an der Einschuboeffnung, damit nichts haengenbleibt
for sx in (-1, 1):
    w = [V(sx * KANAL_B / 2, 0, -0.01), V(sx * (KANAL_B / 2 + 2.0), 0, -0.01),
         V(sx * KANAL_B / 2, 0, 2.0)]
    t = t.cut(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(0, 2.0, 0)))

# Pfeil oben auf der Seitenwand: Schubrichtung. Erhaben, damit er auch im
# Druck sichtbar bleibt.
ax = KANAL_B / 2 + WAND / 2
for y0 in (18.0, 34.0, 50.0):
    w = [V(ax - 1.6, y0, GES_H), V(ax + 1.6, y0, GES_H), V(ax, y0 + 5.0, GES_H)]
    t = t.fuse(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(0, 0, 0.8)))

t = t.removeSplitter()

o = doc.addObject("Part::Feature", "Biegelehre")
o.Shape = t
o.ViewObject.ShapeColor = (0.35, 0.65, 0.45)

# ---------------- Referenz: der Kopf in Sollage ----------------
# Nur zum Ansehen, wird nicht gedruckt.
# Er steht hier in der Endlage, also am Anschlag -- so sieht man den
# Vorschubweg, den die Spitzen gegenueber der Platte zurueckbleiben.
KOPF_Y0 = KANAL_L - KOPF_L
bk = B(-KOPF_B / 2, KOPF_B / 2, KOPF_Y0, KANAL_L, SPALT, SPALT + KOPF_D)
bor = B(-BORST_B / 2, BORST_B / 2, KOPF_Y0, KANAL_L, 0.0, SPALT)
r = doc.addObject("Part::Feature", "Buerstenkopf_Ref")
r.Shape = bk.fuse(bor)
r.ViewObject.ShapeColor = (0.30, 0.60, 0.90)
r.ViewObject.Transparency = 55

doc.recompute()
print("Formwinkel %.0f Grad -> Spalt %.2f mm, Schlitzhoehe %.2f mm" % (WINKEL, SPALT, DECKE))
print("Aussenmasse %.1f x %.1f x %.1f mm" % (GES_B, GES_L, GES_H + BODEN))
print("Biegelehre gueltig:", t.isValid(), "Koerper:", len(t.Solids),
      "Volumen cm3:", round(t.Volume / 1000, 2))
