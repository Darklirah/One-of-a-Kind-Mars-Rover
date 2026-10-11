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
W = 2.4                           # Wandstaerke
XC = 13.5                         # Abstand Antriebsmitte von der Platinenkante
BRUSH = (15.0, 50.0, 6.0, 12.0)   # Buerstenkopf 50 x 15 x 18 (gemessen); Aufteilung Platte 6 / Borsten 12 ist ANNAHME
ZP = ZGROUND + BRUSH[2] + BRUSH[3] + 1.0   # Lagerzapfen in Traegermitte
PLY = (-W - G - 3.0, BY + W + G)  # Y-Lage der beiden Ausleger (hinter der Rueckwand, vor der Vorderwand)
MAST = (35.0, BY + 6.2)           # Mastfuss vorn mittig, aussen an der Wand
RTG_TILT = 25.0                   # Neigung der Akkutasche (RTG) nach hinten, Grad
RTG_DEPTH = 26.0                  # Taschenhoehe; Akku (30 mm) steht 5 mm ueber
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
LEDGES = [('L', 26), ('L', 47), ('R', 20), ('R', 44), ('F', 35), ('B', 36), ('B', 60)]
for side, s in LEDGES:                                             # Auflagen der Platine
    t = t.fuse(prism(side, [(-0.01, 0), (1.0, 0), (1.0, -0.4), (-0.01, -1.4)], s - 4, s + 4))   # Unterseite 45 Grad
HOOKS = [('F', 12), ('F', 58)]              # zwei Haken an der vorderen Laengsseite
HOOK_ANGLE = 3.0                              # Hakenunterseite 3 Grad geschraegt -> Platine wieder entnehmbar
NUT = [(18, 40), (53, 61)]                    # Nut an der hinteren Laengsseite (Abschnitte in X)
for s0, s1 in NUT:
    t = t.fuse(sbox('B', s0, s1, -W, 0, BT, BT + 1.4))
    t = t.fuse(prism('B', [(-0.01, BT + 0.15), (0.5, BT + 0.15), (1.0, BT + 0.65), (1.0, BT + 1.4), (-0.01, BT + 1.4)], s0, s1))   # Nut: 0,5 flach, dann 45 Grad
for side, s in HOOKS:
    for d in (-4.6, 3.6):                                          # Schlitze -> Federzunge
        t = t.cut(sbox(side, s + d, s + d + 1.0, -W - 0.2, 0.1, -7.0, BT + 0.2))
    t = t.cut(sbox(side, s - 3.6, s + 3.6, -W - 0.2, -1.2, -7.0, BT + 0.2))   # Zunge auf 1,2 mm duennen
    t = t.fuse(prism(side, [(-0.2, BT + 0.1), (0.9, BT + 0.1 + 1.1 * math.tan(math.radians(HOOK_ANGLE))), (0.9, BT + 0.5), (-0.2, BT + 1.4)], s - 3, s + 3))
    t = t.fuse(sbox(side, s - 3, s + 3, -1.2, 0, BT - 0.1, BT + 1.4))          # Zunge bis Hakenoberkante


def plates(sign):
    sh = None
    xc = -XC if sign < 0 else BX + XC
    for y0 in PLY:                                                 # Ausleger als Querbalken an Rueck-/Vorderwand
        if sign < 0:
            p = B(-XC - 11, 7.0, y0, y0 + 3, ZF, ZP + 7).cut(B(-W - G - 0.01, 8, y0 - 1, y0 + 4, BT, ZP + 8))
        else:
            p = B(BX - 7.0, BX + XC + 11, y0, y0 + 3, ZF, ZP + 7).cut(B(BX - 8, BX + W + G + 0.01, y0 - 1, y0 + 4, BT, ZP + 8))
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
    """Schwinge nach Curiosity-Vorbild als Seitenwange. Unter den Stegen gefuellt, Fenster als
    45-Grad-Zelte -> steht ohne Ueberhang auf der Druckplatte."""
    xa = -XC - 14 if sign < 0 else BX + XC + 11
    xb = xa + 3
    zw = ZF + RW
    P, Q = (30.0, ZP + 4.0), (12.0, 2.0)                           # Rocker-Drehpunkt, Bogie-Drehpunkt
    F, M, R = (PLY[1] + 1.5, zw), (22.0, zw), (PLY[0] + 1.5, zw)   # vorn, Mitte, hinten
    sh = disc(xa, xb, P, 4.5).fuse(disc(xa, xb, Q, 3.5))
    for a, b in ((P, F), (P, Q), (Q, M), (Q, R)):
        sh = sh.fuse(bar(xa, xb, a, b, 4.0))
        w = [V(xa, a[0], a[1]), V(xa, b[0], b[1]), V(xa, b[0], ZF), V(xa, a[0], ZF)]
        sh = sh.fuse(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(3, 0, 0)))
    for c, sg in ((F, 1), (R, -1)):                                # Radenden: oben rund, unten bis zur Platte
        sh = sh.fuse(disc(xa, xb, c, RW)).fuse(B(xa, xb, min(c[0], c[0] + sg * RW), max(c[0], c[0] + sg * RW), ZF, zw))
    for apex, hw in (((39.0, 3.3), 9.5), ((8.0, -2.4), 3.8)):      # Fenster: Dach 45 Grad
        w = [V(xa - 1, apex[0] - hw, apex[1] - hw), V(xa - 1, apex[0] + hw, apex[1] - hw), V(xa - 1, apex[0], apex[1])]
        sh = sh.cut(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(5, 0, 0)))
    xo, dr = (xa, V(-1, 0, 0)) if sign < 0 else (xb, V(1, 0, 0))
    for c in (F, M, R):                                            # Raeder als flache 45-Grad-Kegel aufgesetzt
        sh = sh.fuse(Part.makeCone(RW, RW - 1.0, 1.0, V(xo, c[0], c[1]), dr))
        sh = sh.fuse(Part.makeCone(2.4, 1.6, 0.8, V(xo + dr.x * 1.0, c[0], c[1]), dr))
    return sh


RW = 5.0                                                           # Radius der Deko-Raeder
t = t.fuse(plates(-1)).fuse(plates(1)).fuse(rocker(-1)).fuse(rocker(1))
mx, my = MAST
ZMAST = 12.0
t = t.fuse(CZ(mx, my, 4.5, ZF, ZMAST)).cut(CZ(mx, my, 1.65, ZF + 1.5, ZMAST + 1))   # Mastfuss
# Kabeloese am Mastfuss (Zugentlastung fuer die 4 Litzen zum VL53L0X), seitlich geschlitzt zum Einclipsen
ex0, ex1, ez0 = mx + 3.5, mx + 9.5, ZMAST - 3.0
oe = B(ex0, ex1, my - 2.5, my + 2.5, ez0, ZMAST)
w = [V(ex0, my - 2.5, ez0), V(ex1, my - 2.5, ez0), V(ex0, my - 2.5, ez0 - 6.0)]
oe = oe.fuse(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(0, 5, 0)))        # 45-Grad-Stuetze, druckbar ohne Support
oe = oe.cut(CZ(mx + 6.8, my, 1.6, ez0 - 7, ZMAST + 1)).cut(B(mx + 6.8, ex1 + 1, my - 0.5, my + 0.5, ez0 - 7, ZMAST + 1))
t = t.fuse(oe)


# ---------------- RTG = Akkutasche am Heck (V2) ----------------
def rtg_place(sh):
    """Taschen-Koordinaten (y nach vorn ab Wand-Aussenflaeche, z ab Drehpunkt) -> Modell."""
    sh.rotate(V(0, 0, 0), V(1, 0, 0), RTG_TILT)
    sh.translate(V(0, -W - G, ZF + 4.0))
    return sh


PW = AKKU[1] + 0.6                                                 # Akku quer: 35 mm in X
PT = AKKU[2] + 0.6
px0, px1 = 35 - PW / 2 - 1.2, 35 + PW / 2 + 1.2
pk = B(px0, px1, -PT - 2.4, 0, -8.0, RTG_DEPTH)                    # reicht bis unter die Schale -> keine Unterseite in der Luft
for i in range(7):                                                 # Kuehlrippen laengs, wie am RTG
    xr = px0 + 2.0 + i * (px1 - px0 - 5.2) / 6
    pk = pk.fuse(B(xr, xr + 1.2, -PT - 3.9, -PT - 2.4, -8.0, RTG_DEPTH - 1.0))
t = t.fuse(rtg_place(pk))
# Uebergang Tasche -> Gehaeuse: Keil ausgefuellt und mit Radien ausgerundet (steifer, ohne Kanten)
tanT, sinT, cosT = math.tan(math.radians(RTG_TILT)), math.sin(math.radians(RTG_TILT)), math.cos(math.radians(RTG_TILT))
yw, zt2 = -W - G, BT + 1.4
yf = yw - (zt2 - (ZF + 4.0)) * tanT                                # Taschen-Vorderflaeche auf Hoehe zt2
w = [V(px0, yw + 0.01, ZF + 4.0), V(px0, yw + 0.01, zt2), V(px0, yf, zt2)]
t = t.fuse(Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(px1 - px0, 0, 0)))
RF = 4.0                                                           # Radius oben zwischen Wandoberkante und Tasche
LF = RF / math.tan(math.radians((90 + RTG_TILT) / 2))
w = [V(px0, yf, zt2), V(px0, yf + LF, zt2), V(px0, yf + LF, zt2 + RF), V(px0, yf - LF * sinT, zt2 + LF * cosT)]
fil = Part.Face(Part.makePolygon(w + [w[0]])).extrude(V(px1 - px0, 0, 0))
t = t.fuse(fil.cut(Part.makeCylinder(RF, px1 - px0 + 2, V(px0 - 1, yf + LF, zt2 + RF), V(1, 0, 0))))
RS = 5.0                                                           # Radius seitlich zwischen Rueckwand und Tasche
for xs, sg in ((px0, -1), (px1, 1)):
    kite = B(min(xs, xs + sg * RS), max(xs, xs + sg * RS), yw - RS, yw, ZF, BT)
    t = t.fuse(kite.cut(CZ(xs + sg * RS, yw - RS, RS, ZF - 1, BT + 1)))
t = t.cut(rtg_place(B(px0 + 1.2, px1 - 1.2, -PT - 1.2, -1.2, 1.2, RTG_DEPTH + 5)))
t = t.cut(B(px0 - 8, px1 + 8, -40, 3, ZF - 12, ZF))                # nichts unter der Schalenunterkante
t = t.cut(B(px0 + 1.4, px0 + 10.4, -W - G - 2.6, -G + 0.1, -5.2, -0.4))   # Kabel + JST-Stecker in die Schale
t = t.removeSplitter()
add("Bodenschale", t, (0.85, 0.85, 0.82))

# ---------------- Antriebsmodule ----------------
def drive(sign, tag):
    xc = -XC if sign < 0 else BX + XC
    bw, bl, bp, bb = BRUSH
    zb = ZGROUND + bb + bp                                         # Oberkante Buerstenplatte
    c = B(xc - bw / 2 - 1, xc + bw / 2 + 1, PLY[0] + 3 + 1.7, PLY[1] - 1.7, zb, zb + 2.0)
    md, ml = MOT[0], MOT[1]
    zm = zb + 3.0 + md / 2                                         # Motorachse (liegt laengs, Y)
    ym = 26 - (ml + 2.0 + MOT[3] / 2)                             # Unwuchtmitte liegt ueber der Buerstenmitte (y = 26)
    for y0 in (ym + 1.5, ym + ml - 5.5):                           # zwei Klemmschellen
        ring = B(xc - 5, xc + 5, y0, y0 + 4, zb + 2, zm).fuse(CY(xc, zm, md / 2 + 1.4, y0, y0 + 4))
        ring = ring.cut(CY(xc, zm, md / 2 + 0.1, y0 - 1, y0 + 5)).cut(B(xc - 4.2, xc + 4.2, y0 - 1, y0 + 5, zm + 2.5, zm + 20))
        c = c.fuse(ring)
    for y0, y1, yh in [(PLY[0] - 2.4, PLY[0] + 5, PLY[0] - 2.4), (PLY[1] - 2, PLY[1] + 5.4, PLY[1] + 4.4)]:   # Lagerzapfen mit Kopf
        c = c.fuse(CY(xc, ZP, 2.0, y0, y1)).fuse(CY(xc, ZP, 2.8, yh, yh + 1.0))
    c = c.cut(B(xc - 12, xc + 12, PLY[0] - 6, PLY[1] + 9, zb - 6, zb))   # Zapfen unten abgeflacht -> Traeger liegt plan auf der Druckplatte
    add("Buerstentraeger_" + tag, c.removeSplitter(), (0.9, 0.45, 0.1))
    for i, y0 in enumerate(PLY):                                   # TPU-Tuellen, Bunde als 45-Grad-Kegel (stehend druckbar)
        g = CY(xc, ZP, 4.0, y0, y0 + 3).fuse(Part.makeCone(5.2, 4.0, 1.2, V(xc, y0 - 1.2, ZP), V(0, 1, 0)))
        g = g.fuse(Part.makeCone(4.0, 5.2, 1.2, V(xc, y0 + 3, ZP), V(0, 1, 0)))
        g = g.cut(CY(xc, ZP, 2.0, y0 - 2, y0 + 5))
        add("Tuelle_TPU_%s%d" % (tag, i + 1), g, (0.1, 0.1, 0.1))
    br = B(xc - bw / 2, xc + bw / 2, 26 - bl / 2, 26 + bl / 2, zb - bp, zb)
    br = br.fuse(B(xc - bw / 2 + 1, xc + bw / 2 - 1, 26 - bl / 2 + 1, 26 + bl / 2 - 1, ZGROUND, zb - bp))
    add("Buerstenkopf_Ref_" + tag, br, (0.3, 0.6, 0.9))


drive(-1, "L")
drive(1, "R")

# ---------------- Referenzteile ----------------
add("Mast_CFK_Ref", CZ(mx, my, 1.5, ZF + 1.5, 63), (0.15, 0.15, 0.15))
add("Fahrbahn_Ref", B(-30, BX + 30, -30, BY + 20, ZGROUND - 0.2, ZGROUND), (0.7, 0.35, 0.2), 70)

# ---------------- Mastkopf (druckbar) ----------------
zk = 52.0
k = B(mx - 15, mx + 15, my - 5, my + 6, zk, zk + 14).cut(CZ(mx, my, 1.65, zk - 1, zk + 11.5))
k = k.cut(B(mx - 12.8, mx + 12.8, my + 2.0, my + 5.0, zk + 2, zk + 15))   # Schlitz fuer VL53L0X-Modul
k = k.cut(B(mx - 5, mx + 5, my + 4, my + 7, zk + 4, zk + 11))       # Sichtfenster nach vorn
k = k.cut(B(mx + 4, mx + 11, my + 2.0, my + 5.0, zk - 1, zk + 2.1))   # Kabelauslass nach unten (Loetaugen des Moduls unten)
for dx in (-10.5, 10.5):                                             # "Kameraaugen": 45-Grad-Kegel, druckbar ohne Support
    k = k.fuse(Part.makeCone(3.6, 2.4, 1.2, V(mx + dx, my + 6, zk + 7.5), V(0, 1, 0)))
    k = k.cut(Part.makeCylinder(1.6, 3.5, V(mx + dx, my + 4.9, zk + 7.5), V(0, 1, 0)))
add("Mastkopf", k.removeSplitter(), (0.92, 0.92, 0.9))

doc.recompute()
for n in ["Bodenschale", "Buerstentraeger_L", "Mastkopf"]:
    s = doc.getObject(n).Shape
    print(n, "gueltig:", s.isValid(), "Koerper:", len(s.Solids), "Volumen cm3:", round(s.Volume / 1000, 2))
