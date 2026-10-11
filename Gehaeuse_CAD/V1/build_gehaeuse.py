# Erstentwurf Gehaeuse Mars Rover -- parametrisches FreeCAD-Skript
# Ausfuehren in FreeCAD (Dokument "MarsRover_Gehaeuse" muss existieren und
# das Objekt "Leiterplatte_Ref" enthalten). Alle selbst erzeugten Objekte werden
# bei jedem Lauf geloescht und neu gebaut.
#
# Koordinaten: X = rechts (0..70), Y = vorn (0..52), Z = oben.
#              Platinen-Unterseite liegt auf Z = 0.
import FreeCAD as App
import math
import Part

V = App.Vector
doc = App.getDocument("MarsRover_Gehaeuse")
for o in list(doc.Objects):
    if o.Name != "Leiterplatte_Ref":
        doc.removeObject(o.Name)


def B(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def CZ(x, y, r, z0, z1):
    return Part.makeCylinder(r, z1 - z0, V(x, y, z0), V(0, 0, 1))


def CY(x, z, r, y0, y1):
    return Part.makeCylinder(r, y1 - y0, V(x, y0, z), V(0, 1, 0))


def add(name, shape, color, transp=0):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    o.ViewObject.ShapeColor = color
    o.ViewObject.Transparency = transp
    return o


# ---------------- Parameter ----------------
BX, BY, BT = 70.0, 52.0, 1.0      # Platine
G = 0.3                           # Spiel Platine / Wand
ZF = -8.7                         # Unterkante Bodenschale
FLOOR = 1.2                       # Bodenstaerke
SENSOR_GAP = 3.0                  # TCRT5000 ueber dem Boden (Optimum 2,5; erlaubt 2..5)
ZGROUND = -7.2 - SENSOR_GAP       # Fahrbahn
AKKU = (30.0, 35.0, 5.0)          # LiPo 503035: X, Y, Dicke
XC = 12.0                         # Abstand Antriebsmitte von der Platinenkante
ZP = 5.3                          # Hoehe der Lagerzapfen
BRUSH = (12.0, 28.0, 4.0, 10.5)   # Buerstenkopf: Breite, Laenge, Plattendicke, Borstenlaenge
MAST = (35.0, BY + 6.2)           # Mastfuss vorn mittig, aussen an der Wand
W = 2.4                           # Wandstaerke
RTGX = 11.0                       # RTG links hinten (Mitte: Akkuschacht, MPU-6050)
MOT = (12.0, 15.5, 7.0, 5.0)      # Motor: Durchmesser, Koerperlaenge, Unwucht-Durchmesser, Unwucht-Dicke

XI0, XI1, YI0, YI1 = -G, BX + G, -G, BY + G     # Innenflaechen der Wand


def pt(side, a, s, z):
    """a = Abstand von der Wand-Innenflaeche nach innen, s = Position entlang der Wand."""
    if side == 'L':
        return V(XI0 + a, s, z)
    if side == 'R':
        return V(XI1 - a, s, z)
    if side == 'B':
        return V(s, YI0 + a, z)
    return V(s, YI1 - a, z)


def sbox(side, s0, s1, a0, a1, z0, z1):
    p, q = pt(side, a0, s0, z0), pt(side, a1, s1, z1)
    return B(min(p.x, q.x), max(p.x, q.x), min(p.y, q.y), max(p.y, q.y), z0, z1)


def prism(side, pts, s0, s1):
    w = Part.makePolygon([pt(side, a, s0, z) for a, z in pts + [pts[0]]])
    return Part.Face(w).extrude(pt(side, 0, s1, 0) - pt(side, 0, s0, 0))


# ---------------- Bodenschale ----------------
t = B(-W - G, BX + W + G, -W - G, BY + W + G, ZF, BT)
t = t.cut(B(XI0, XI1, YI0, YI1, ZF + FLOOR, 1.1))
t = t.cut(B(XI0, XI1, 43.2, YI1, ZF - 1, ZF + FLOOR + 0.1))        # Sensorfenster vorn
ax0 = 35 - AKKU[0] / 2 - 0.3
ax1 = 35 + AKKU[0] / 2 + 0.3
zr0, zr1 = ZF + FLOOR, ZF + FLOOR + AKKU[2]                        # Akku liegt -7,5 .. -2,5
t = t.cut(B(ax0, ax1, -3, -0.2, zr0, zr1 + 0.1))                   # Einschub von hinten
t = t.cut(CZ(35, 26, 6, ZF - 1, zr0 + 0.1))                        # Ausdrueckloch
rails = B(ax0 - 1.6, ax0, YI0, 39.2, zr0, zr1)
rails = rails.fuse(B(ax1, ax1 + 1.6, YI0, 39.2, zr0, zr1))
rails = rails.fuse(B(ax0, ax1, 37.6, 39.2, zr0, zr1))              # Anschlag vorn
rails = rails.cut(B(ax0 - 1.7, ax0 + 0.1, 7, 12, zr0, zr1 + 0.1))  # Kabelkanal zum JST
t = t.fuse(rails)
# Akkuriegel: Federzunge im Boden mit Rastnase hinter dem Akku (Akku liegt y 2,6 .. 37,6)
RX0, RX1, RYR, RNH = 30.0, 40.0, 16.0, 1.2                         # Zunge X von..bis, Wurzel bei Y, Nasenhoehe
for cutbox in (B(RX0 - 1, RX0, 0.4, RYR, ZF - 1, zr0 + 0.1), B(RX1, RX1 + 1, 0.4, RYR, ZF - 1, zr0 + 0.1),
               B(RX0 - 1, RX1 + 1, -0.4, 0.5, ZF - 1, zr0 + 0.1)):
    t = t.cut(cutbox)
w = [V(RX0 + 1, 0.7, zr0 - 0.1), V(RX0 + 1, 2.4, zr0 - 0.1), V(RX0 + 1, 2.4, zr0 + RNH), V(RX0 + 1, 1.9, zr0 + RNH)]
t = t.fuse(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(RX1 - RX0 - 2, 0, 0)))
LEDGES = [('L', 26), ('L', 47), ('R', 20), ('R', 44), ('F', 35), ('B', 24), ('B', 46)]
for side, s in LEDGES:                                             # Auflagen der Platine
    t = t.fuse(sbox(side, s - 4, s + 4, 0, 1.0, -1.2, 0))
HOOKS = [('F', 12), ('F', 58)]              # zwei Haken an der vorderen Laengsseite
HOOK_ANGLE = 3.0                              # Hakenunterseite 3 Grad geschraegt -> Platine wieder entnehmbar
NUT = [(18, 40), (53, 61)]                    # Nut an der hinteren Laengsseite (Abschnitte in X)
for s0, s1 in NUT:
    t = t.fuse(sbox('B', s0, s1, -W, 0, BT, BT + 1.4)).fuse(sbox('B', s0, s1, -0.01, 1.0, BT + 0.15, BT + 1.4))
for side, s in HOOKS:
    for d in (-4.6, 3.6):                                          # Schlitze -> Federzunge
        t = t.cut(sbox(side, s + d, s + d + 1.0, -W - 0.2, 0.1, -7.0, BT + 0.2))
    t = t.cut(sbox(side, s - 3.6, s + 3.6, -W - 0.2, -1.2, -7.0, BT + 0.2))   # Zunge auf 1,2 mm duennen
    t = t.fuse(prism(side, [(-0.2, BT + 0.1), (0.9, BT + 0.1 + 1.1 * math.tan(math.radians(HOOK_ANGLE))), (0.9, BT + 0.5), (-0.2, BT + 1.4)], s - 3, s + 3))
    t = t.fuse(sbox(side, s - 3, s + 3, -1.2, 0, BT - 0.1, BT + 1.4))          # Zunge bis Hakenoberkante


def plates(sign):
    sh = None
    xc = -XC if sign < 0 else BX + XC
    for y0 in (5.0, 44.0):
        if sign < 0:
            p = B(-XC - 9, -W - G, y0, y0 + 3, ZF, ZP + 7)
        else:
            p = B(BX + W + G, BX + XC + 9, y0, y0 + 3, ZF, ZP + 7)
        p = p.cut(CY(xc, ZP, 4.0, y0 - 1, y0 + 4))
        p = p.cut(B(xc - 3.3, xc + 3.3, y0 - 1, y0 + 4, ZF - 1, ZP))   # Gabel nach unten offen, Hals 6,6 < Tuelle 8
        sh = p if sh is None else sh.fuse(p)
    return sh


def bar(x0, x1, p, q, wd):
    """Steg in der YZ-Ebene von p=(y,z) nach q, Breite wd, von x0 bis x1."""
    dy, dz = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dy, dz)
    ny, nz = -dz / ln * wd / 2, dy / ln * wd / 2
    pts = [V(x0, p[0] + ny, p[1] + nz), V(x0, q[0] + ny, q[1] + nz), V(x0, q[0] - ny, q[1] - nz), V(x0, p[0] - ny, p[1] - nz)]
    return Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(V(x1 - x0, 0, 0))


def disc(x0, x1, p, r):
    return Part.makeCylinder(r, x1 - x0, V(x0, p[0], p[1]), V(1, 0, 0))


def rocker(sign):
    """Schwinge nach Curiosity-Vorbild (Rocker + Bogie) als Seitenwange aussen an den Auslegern."""
    xa = -XC - 12 if sign < 0 else BX + XC + 9
    xb = xa + 3
    zw = ZF + RW                                                   # Radmitte, Rad steht auf der Druckplatte
    P, Q = (30.0, 10.0), (15.0, 1.0)                               # Rocker-Drehpunkt, Bogie-Drehpunkt
    F, M, R = (45.5, zw), (24.0, zw), (6.5, zw)                    # vorn, Mitte, hinten
    sh = disc(xa, xb, P, 4.5).fuse(disc(xa, xb, Q, 3.5))
    for a, b in ((P, F), (P, Q), (Q, M), (Q, R)):
        sh = sh.fuse(bar(xa, xb, a, b, 4.0))
    for c in (F, M, R):                                            # Radscheiben mit Nabe
        sh = sh.fuse(disc(xa, xb, c, RW))
        xo = xa - 1.0 if sign < 0 else xb
        sh = sh.fuse(disc(xo, xo + 1.0, c, 2.2))
    return sh


RW = 5.0                                                           # Radius der Deko-Raeder
t = t.fuse(plates(-1)).fuse(plates(1)).fuse(rocker(-1)).fuse(rocker(1))
mx, my = MAST
ZMAST = 12.0
t = t.fuse(CZ(mx, my, 4.5, ZF, ZMAST)).cut(CZ(mx, my, 1.65, ZF + 1.5, ZMAST + 1))   # Mastfuss
w = Part.makePolygon([V(RTGX - 6, -W - G, zr1 + 0.1), V(RTGX - 6, -W - G, BT), V(RTGX - 6, -W - G - 3.4, BT), V(RTGX - 6, -W - G, zr1 + 0.1)])
t = t.fuse(Part.Face(w).extrude(V(12, 0, 0)))                      # Konsole fuer den RTG
t = t.removeSplitter()
add("Bodenschale", t, (0.85, 0.85, 0.82))

# ---------------- Antriebsmodule ----------------
def drive(sign, tag):
    xc = -XC if sign < 0 else BX + XC
    bw, bl, bp, bb = BRUSH
    zb = ZGROUND + bb + bp                                         # Oberkante Buerstenplatte
    c = B(xc - 7, xc + 7, 26 - bl / 2 - 2, 26 + bl / 2 + 2, zb, zb + 2.0)
    md, ml = MOT[0], MOT[1]
    zm = zb + 3.0 + md / 2                                         # Motorachse (liegt laengs, Y)
    ym = 26 - 9                                                    # Motorkoerper ym .. ym+ml
    for y0 in (ym + 1.5, ym + ml - 5.5):                           # zwei Klemmschellen
        ring = B(xc - 5, xc + 5, y0, y0 + 4, zb + 2, zm).fuse(CY(xc, zm, md / 2 + 1.4, y0, y0 + 4))
        ring = ring.cut(CY(xc, zm, md / 2 + 0.1, y0 - 1, y0 + 5)).cut(B(xc - 4.2, xc + 4.2, y0 - 1, y0 + 5, zm + 2.5, zm + 20))
        c = c.fuse(ring)
    for y0, y1, yh in [(2.4, 10.0, 2.4), (42.0, 49.6, 48.6)]:      # Lagerzapfen mit Kopf
        c = c.fuse(CY(xc, ZP, 2.0, y0, y1)).fuse(CY(xc, ZP, 2.8, yh, yh + 1.0))
    add("Buerstentraeger_" + tag, c.removeSplitter(), (0.9, 0.45, 0.1))
    for i, y0 in enumerate([5.0, 44.0]):                           # TPU-Tuellen mit zwei Bunden
        g = CY(xc, ZP, 4.0, y0, y0 + 3).fuse(CY(xc, ZP, 5.5, y0 - 1.2, y0)).fuse(CY(xc, ZP, 5.5, y0 + 3, y0 + 4.2))
        g = g.cut(CY(xc, ZP, 2.0, y0 - 2, y0 + 5))
        add("Tuelle_TPU_%s%d" % (tag, i + 1), g, (0.1, 0.1, 0.1))
    br = B(xc - bw / 2, xc + bw / 2, 26 - bl / 2, 26 + bl / 2, zb - bp, zb)
    br = br.fuse(B(xc - bw / 2 + 1, xc + bw / 2 - 1, 26 - bl / 2 + 1, 26 + bl / 2 - 1, ZGROUND, zb - bp))
    add("Buerstenkopf_Ref_" + tag, br, (0.3, 0.6, 0.9))


drive(-1, "L")
drive(1, "R")

# ---------------- Referenzteile ----------------
add("Akku_Ref", B(35 - AKKU[0] / 2, 35 + AKKU[0] / 2, 2.6, 2.6 + AKKU[1], zr0, zr1), (0.2, 0.3, 0.8))
add("Mast_CFK_Ref", CZ(mx, my, 1.5, ZF + 1.5, 63), (0.15, 0.15, 0.15))
add("Fahrbahn_Ref", B(-30, BX + 30, -30, BY + 20, ZGROUND - 0.2, ZGROUND), (0.7, 0.35, 0.2), 70)

# ---------------- Mastkopf (druckbar) ----------------
zk = 52.0
k = B(mx - 15, mx + 15, my - 5, my + 6, zk, zk + 14).cut(CZ(mx, my, 1.65, zk - 1, zk + 11.5))
k = k.cut(B(mx - 12.8, mx + 12.8, my + 2.0, my + 5.0, zk + 2, zk + 15))   # Schlitz fuer VL53L0X-Modul
k = k.cut(B(mx - 5, mx + 5, my + 4, my + 7, zk + 4, zk + 11))       # Sichtfenster nach vorn
for dx in (-10.5, 10.5):                                             # "Kameraaugen"
    k = k.fuse(Part.makeCylinder(3.2, 3, V(mx + dx, my + 6, zk + 7.5), V(0, 1, 0)))
    k = k.cut(Part.makeCylinder(2.2, 3.1, V(mx + dx, my + 6.5, zk + 7.5), V(0, 1, 0)))
add("Mastkopf", k.removeSplitter(), (0.92, 0.92, 0.9))

# ---------------- RTG (Deko, druckbar, wird auf die Konsole geklebt) ----------------
zrtg = BT + 7.5
r = CY(RTGX, zrtg, 4.5, -24, -1)
for y in range(-23, -3, 4):
    r = r.fuse(CY(RTGX, zrtg, 6.0, y, y + 1.2))
r = r.fuse(B(RTGX - 4, RTGX + 4, -W - G - 3.4, -G, BT, zrtg))
add("RTG_Deko", r.removeSplitter(), (0.35, 0.35, 0.38))

doc.recompute()
for n in ["Bodenschale", "Buerstentraeger_L", "Mastkopf", "RTG_Deko"]:
    s = doc.getObject(n).Shape
    print(n, "gueltig:", s.isValid(), "Koerper:", len(s.Solids), "Volumen cm3:", round(s.Volume / 1000, 2))
