# Zukaufteile als einfache 3D-Modelle: jedes Teil wird als STEP in Bauteile/
# abgelegt und im Dokument "MarsRover_Gehaeuse" an seinem Einbauort platziert.
# Nach build_gehaeuse.py ausfuehren.
#
# ACHTUNG: Masse mit (*) sind Katalog-/Erfahrungswerte, nicht am Teil gemessen.
import os
import FreeCAD as App
import Part

V = App.Vector
DOC = "MarsRover_Gehaeuse_V2" if "MarsRover_Gehaeuse_V2" in App.listDocuments() else "MarsRover_Gehaeuse"
HERE = os.path.dirname(App.getDocument(DOC).FileName)   # Ordner der FreeCAD-Datei
OUT = os.path.join(HERE, "Bauteile")
os.makedirs(OUT, exist_ok=True)
doc = App.getDocument(DOC)
for n in ("Akku_Ref", "Mast_CFK_Ref", "Mast_Holz_Ref", "Buerstenkopf_Ref_L", "Buerstenkopf_Ref_R"):
    if doc.getObject(n):
        doc.removeObject(n)


def B(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def CZ(x, y, r, z0, z1):
    return Part.makeCylinder(r, z1 - z0, V(x, y, z0), V(0, 0, 1))


def CY(x, z, r, y0, y1):
    return Part.makeCylinder(r, y1 - y0, V(x, y0, z), V(0, 1, 0))


def export(name, shape):
    shape.exportStep(os.path.join(OUT, name + ".step"))


def place(name, shape, pos, rot=None, color=(0.5, 0.5, 0.5)):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    o.Placement = App.Placement(V(*pos), rot or App.Rotation())
    o.ViewObject.ShapeColor = color
    return o


# ---- 1  Vibrationsmotor (sourcing map, 22,5 x 12 mm, 1,5-3 V, 140 mA) ----
# Achse = +Y, Koerper y 0..15,5 (*), Unwucht D7 x 5 am Wellenende
mot = CY(0, 0, 6.0, 0, 15.5).fuse(CY(0, 0, 0.75, 15.5, 22.5))
ecc = CY(0, 0, 3.5, 17.5, 22.5).cut(B(-4, 4, 17, 23, -4, 0))
mot = mot.fuse(ecc).fuse(B(-3, -2, -1.5, 0, 3, 5)).fuse(B(2, 3, -1.5, 0, 3, 5))   # Loetfahnen
export("Vibrationsmotor_12x22.5", mot)

# ---- 2  MPU-6050 Modul (GY-521, 21 x 16 mm (*)) ----
mpu = B(0, 21, 0, 16, 0, 1.6).fuse(B(8.5, 12.5, 6, 10, 1.6, 2.5))
for i in range(8):
    mpu = mpu.cut(CZ(1.6 + 2.54 * i, 1.3, 0.5, -1, 3))
for x in (3.0, 18.0):
    mpu = mpu.cut(CZ(x, 13.0, 1.5, -1, 3))
export("MPU-6050_GY-521", mpu)

# ---- 3  VL53L0X Modul (25 x 10,67 mm, Lochabstand 19,304 mm) ----
tof = B(-12.5, 12.5, 0, 10.67, 0, 1.6).fuse(B(-2.2, 2.2, 5.0, 7.4, 1.6, 2.6))
for x in (-9.652, 9.652):
    tof = tof.cut(CZ(x, 7.5, 1.5, -1, 3))
for i in range(6):
    tof = tof.cut(CZ(-6.35 + 2.54 * i, 1.3, 0.5, -1, 3))
export("VL53L0X_Modul", tof)

# ---- 4  TP4056 Lademodul Mini-USB, ohne Schutzschaltung (25 x 19 mm (*)) ----
tp = B(0, 25, 0, 19, 0, 1.6).fuse(B(-1.0, 8.2, 5.65, 13.35, 1.6, 5.5))      # Mini-USB-Buchse
tp = tp.fuse(B(12, 17, 7.5, 11.5, 1.6, 3.1))                                # TP4056 SOP-8
export("TP4056_MiniUSB", tp)

# ---- 5  MT3608 Step-Up-Modul (36 x 17 mm, Poti bereits entfernt) ----
mt = B(0, 36, 0, 17, 0, 1.6).fuse(B(13, 19, 5.5, 11.5, 1.6, 4.6))           # Drossel
mt = mt.fuse(B(22, 25, 7, 10, 1.6, 2.8)).fuse(B(5, 9, 6, 11, 1.6, 3.6))
for x in (1.5, 34.5):
    for y in (1.5, 15.5):
        mt = mt.cut(CZ(x, y, 0.6, -1, 3))
export("MT3608_StepUp", mt)

# ---- 6  LiPo 503035, 500 mAh ----
ak = B(-15, 15, 0, 35, 0, 5)
ak = ak.makeFillet(1.5, [e for e in ak.Edges if abs(e.Length - 35) < 0.01])
export("LiPo_503035", ak)

# ---- 7  Zahnbuerstenkopf (50 x 15 x 18 mm gemessen; Platte 6 / Borsten 12 angenommen) ----
bk = B(-7.5, 7.5, -25, 25, 12.0, 18.0)
bk = bk.makeFillet(5.0, [e for e in bk.Edges if abs(e.Length - 6) < 0.01])
bk = bk.fuse(B(-6.5, 6.5, -24, 24, 0, 12.0))
export("Zahnbuerstenkopf", bk)

# ---- 8  Mast: Holz-Schaschlikspiess D3, auf 70 mm abgelaengt ----
# Spiesse sind zum Ende hin leicht verjuengt und angespitzt; das stumpfe Ende kommt
# in den Mastfuss. Hier als glatter Zylinder D3 -- das Loch im Fuss ist D3,3.
cfk = CZ(0, 0, 1.5, 0, 70)
export("Holzspiess_3x70", cfk)

# ---------------- Einbau ----------------
RZ, RX, RY = V(0, 0, 1), V(1, 0, 0), V(0, 1, 0)
for tag, xc in (("L", -13.5), ("R", 83.5)):
    place("Motor_" + tag, mot, (xc, 6.0, 16.8), color=(0.75, 0.75, 0.78))
    place("Buerstenkopf_" + tag, bk, (xc, 26.0, -10.2), color=(0.3, 0.6, 0.9))
# Akku steht quer in der RTG-Tasche am Heck (Taschen-Koordinaten wie in build_gehaeuse.py)
ak2 = ak.copy()
ak2.transformShape(App.Matrix(0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1))   # x<-y, y<-z, z<-x
ak2.translate(V(17.5, -1.5 - 5.0, 1.2 + 15.0))
ak2.rotate(V(0, 0, 0), V(1, 0, 0), 25.0)
ak2.translate(V(0, -2.7, -8.7 + 4.0))
akpl = ak2.Placement
place("Akku_503035", ak2, (0, 0, 0), color=(0.2, 0.3, 0.8)).Placement = akpl
place("Mast_Holz", cfk, (35, 58.2, -7.2), color=(0.78, 0.62, 0.38))
place("VL53L0X", tof, (35, 58.2 + 2.2, 52 + 2.2), App.Rotation(RZ, 180).multiply(App.Rotation(RX, 90)), (0.5, 0.1, 0.6))   # Loetaugen unten
place("MPU6050", mpu, (40.41, 10.3, 3.55), App.Rotation(RZ, 180), (0.1, 0.25, 0.7))
place("TP4056", tp, (2.7, 14.5, 3.55), App.Rotation(RZ, 90).multiply(App.Rotation(RX, 90)), (0.1, 0.25, 0.7))
place("MT3608", mt, (66.0, 19.7, 3.55), App.Rotation(RZ, 180).multiply(App.Rotation(RY, -90)), (0.1, 0.25, 0.7))
doc.recompute()
print("Bauteile:", sorted(os.listdir(OUT)))
