# Rover in die Marslandschaft einpassen: Groesse, Licht, Kanten, Staub.
import os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

SP = sys.argv[1]
# Aufruf: montage_marslandschaft.py <ordner> [freigestelltes_png] [ausgabe_png]
QUELLE  = sys.argv[2] if len(sys.argv) > 2 else "rover_freigestellt.png"
AUSGABE = sys.argv[3] if len(sys.argv) > 3 else "montage2.png"
ZIEL = (1300, 900)
W, H = ZIEL

# ---------- Stellschrauben ----------
GROESSE   = 0.37    # Breite des Rovers als Anteil der Bildbreite (kleiner = weiter hinten)
BODEN     = 0.73    # Hoehe, auf der er aufsetzt (kleinerer Wert = weiter hinten)
EINSINKEN = 0.105   # wieviel er unter die Aufstandslinie rutscht, Anteil seiner Hoehe
VERGRABEN = 0.085   # Breite des Uebergangs, in dem er im Boden verschwindet
DUNST     = 0.20    # wieviel Hintergrundfarbe in den Rover gemischt wird (Luftperspektive)
SATT      = 0.80    # Farbigkeit des Rovers (1 = wie gerendert)
ABNUTZUNG = 0.60    # Staerke der Gebrauchsspuren (0 = fabrikneu)
WEICH     = 1.6     # Weichzeichnung der Silhouettenkante in Pixeln
LICHT     = (-1.0, -1.0)   # Sonnenrichtung in Bildkoordinaten: von oben links
STAUB     = 0.92    # Staerke der Staubwolke vor dem Rover
FAHNE     = 0.85    # Staerke der Staubfahne hinter dem Rover
SCHATTEN  = 0.70    # Tiefe des Wurfschattens: 0,62 = Kern auf 38 % Helligkeit
SCH_LANG  = 0.34    # Laenge des Wurfschattens, Anteil der Rover-Hoehe

hg = Image.open(os.path.join(SP, "hintergrund.png")).convert("RGB")


def gezogen(k, saat, streckung):
    """Rauschen, in X gestreckt -- das ergibt vom Wind gezogene Schlieren."""
    r = np.random.default_rng(saat)
    klein = r.random((max(2, H // k), max(2, int(W / (k * streckung))))).astype(np.float32)
    g = Image.fromarray((klein * 255).astype(np.uint8), "L").resize((W, H), Image.BICUBIC)
    return np.asarray(g, dtype=np.float32) / 255.0


def staub_auf(bild, maske):
    """Staub streut das Licht: er nimmt dem Untergrund die Zeichnung UND hellt ihn auf.
    Beides zusammen laesst ihn erst als Staub lesen, Aufhellen allein wirkt wie ein
    Schleier ueber dem Bild."""
    rgb_b = np.asarray(bild.convert("RGB"), dtype=np.float32) / 255.0
    weich = np.asarray(bild.convert("RGB").filter(ImageFilter.GaussianBlur(7)),
                       dtype=np.float32) / 255.0
    m = maske[..., None]
    rgb_b = rgb_b * (1 - m * 0.85) + weich * (m * 0.85)
    rgb_b = rgb_b * (1 - m) + np.array([0.80, 0.655, 0.555], dtype=np.float32) * m
    return Image.fromarray((np.clip(rgb_b, 0, 1) * 255).astype(np.uint8), "RGB")

# ---------- Rover vorbereiten ----------
rov = Image.open(os.path.join(SP, QUELLE)).convert("RGBA")
rov = rov.crop(rov.getchannel("A").getbbox())
bw = int(W * GROESSE)
bh = int(rov.size[1] * bw / rov.size[0])
rov = rov.resize((bw, bh), Image.LANCZOS)
px = (W - bw) // 2
# Ein Modell, das genau auf der Aufstandslinie endet, sieht aus, als schwebe es:
# echte Fahrzeuge verschwinden mit den Aufstandspunkten im Sand. Also ein Stueck
# darunter setzen, der Staub am Fuss deckt den Uebergang.
py = int(H * BODEN) - bh

rgb = np.asarray(rov.convert("RGB"), dtype=np.float32) / 255.0
alpha = np.asarray(rov.getchannel("A"), dtype=np.float32) / 255.0

# ---------- Licht: gerichteter Verlauf statt FreeCADs Kameralicht ----------
yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32)
nx = (xx / bw - 0.5) * 2.0
ny = (yy / bh - 0.5) * 2.0
lx, ly = LICHT
richt = -(nx * lx + ny * ly) / np.sqrt(lx * lx + ly * ly) / 2.0     # -1 .. +1
hell = 1.0 + richt * 0.24                                          # oben links heller
rgb *= hell[..., None]
rgb *= 0.90                                                        # Mars bekommt weniger Sonne
rgb *= np.array([1.075, 0.995, 0.885], dtype=np.float32)           # warmer Grundton

# ---------- Gebrauchsspuren ----------
# Ein CAD-Render hat makellose Flaechen; ein Geraet, das durch Marsstaub faehrt,
# nicht. Vier Lagen, alle aus demselben Rauschvorrat:
def feld(k, saat, sx=1.0, sy=1.0):
    r = np.random.default_rng(saat)
    klein = r.random((max(2, int(bh / (k * sy))), max(2, int(bw / (k * sx))))).astype(np.float32)
    g = Image.fromarray((klein * 255).astype(np.uint8), "L").resize((bw, bh), Image.BICUBIC)
    return np.asarray(g, dtype=np.float32) / 255.0

tief = yy / bh                                        # 0 oben, 1 unten
staub = np.array([0.72, 0.56, 0.45], dtype=np.float32)

# 1 Staubfilm -- unten dicker als oben, weil Staub von unten hochgeworfen wird
film = (0.09 + 0.26 * tief) * (0.62 + 0.38 * feld(9, 101)) * ABNUTZUNG
rgb = rgb * (1 - film[..., None]) + staub * film[..., None]

# 2 Schlieren -- in Y gezogenes Rauschen, wie herabgelaufener Staub
schlieren = (feld(7, 202, sx=0.3, sy=3.5) - 0.5) * 0.055 * ABNUTZUNG
rgb *= (1 + schlieren)[..., None]

# 3 feines Korn
rgb *= (1 + (feld(2, 303) - 0.5) * 0.05 * ABNUTZUNG)[..., None]

# 4 Schmutz in den Fugen: wo das Bild dunkler ist als seine weichgezeichnete
#   Fassung, liegt eine Kante oder ein Spalt -- dort setzt sich Dreck ab
g = rgb.mean(-1)
gw = np.asarray(Image.fromarray((np.clip(g, 0, 1) * 255).astype(np.uint8), "L")
                .filter(ImageFilter.GaussianBlur(2.5)), dtype=np.float32) / 255.0
fugen = np.clip(gw - g, 0, 1) * 0.9
rgb *= (1 - np.clip(fugen, 0, 0.15) * ABNUTZUNG)[..., None]
rgb = np.clip(rgb, 0, 1)

grau = (rgb * np.array([0.299, 0.587, 0.114], dtype=np.float32)).sum(-1, keepdims=True)
rgb = grau * (1.0 - SATT) + rgb * SATT

# ---------- Luftperspektive: Hintergrundfarbe einmischen ----------
umfeld = np.asarray(hg.crop((px, py, px + bw, py + bh)).filter(
    ImageFilter.GaussianBlur(40)), dtype=np.float32) / 255.0
rgb = rgb * (1.0 - DUNST) + umfeld * DUNST
rgb = np.clip(rgb, 0.0, 1.0)

rov = Image.fromarray((rgb * 255).astype(np.uint8), "RGB")
rov = rov.filter(ImageFilter.GaussianBlur(0.7))                    # Kanten nicht knackscharf

# Silhouette weichzeichnen, aber nicht aufblaehen
a = Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(WEICH))
a = a.point(lambda v: max(0, min(255, int((v - 40) * 255 / 190))))

# Unterhalb der Auflagelinie ausblenden. Das ist der eigentliche Grund, warum eine
# Montage schwebt: das eingesetzte Bild liegt immer VOLLSTAENDIG oben auf, es gibt
# keinen Boden davor. Erst wenn der Rover nach unten hin verschwindet, steckt er drin.
#
# Die Linie darf nicht waagerecht sein: in der isometrischen Ansicht ist die
# Standebene schraeg. Gesucht ist die Gerade, auf der das Modell wirklich aufliegt --
# also die untere konvexe Huelle seiner Silhouette, die genau die tiefsten Fuesse
# beruehrt und dazwischen gerade durchlaeuft.
fest = alpha > 0.5
hat = fest.any(axis=0)
unten = np.where(hat, bh - 1 - np.argmax(fest[::-1], axis=0), -1).astype(np.float64)
# Die Standebene ist in der Isometrie schraeg. Ihre Neigung steckt in den beiden
# Auflagepunkten: dem tiefsten Punkt der linken und dem der rechten Haelfte. Eine
# Gerade durch beide ist die Linie, auf der der Rover wirklich steht.
def tiefster(von, bis):
    i = [c for c in range(von, bis) if hat[c]]
    j = max(i, key=lambda c: unten[c])
    return float(j), unten[j]

xl, yl = tiefster(0, int(bw * 0.38))
xr, yr = tiefster(int(bw * 0.62), bw)
k = (yr - yl) / (xr - xl)
linie = k * (np.arange(bw, dtype=np.float64) - xl) + yl
print("   Auflagepunkte: links (%.0f, %.0f), rechts (%.0f, %.0f) -> Neigung %.2f"
      % (xl, yl, xr, yr, k))

band = max(2.0, bh * VERGRABEN)
schwelle = linie[None, :] - bh * EINSINKEN
verlauf = np.clip((schwelle + band - yy) / band, 0.0, 1.0)
a = Image.fromarray((np.asarray(a, dtype=np.float32) * verlauf).astype(np.uint8), "L")
rov.putalpha(a)

# ---------- Schlagschatten ----------
# Die Sonne steht oben links, der Schatten faellt also nach rechts unten. Er wird
# flachgedrueckt (Aufsicht auf den Boden), in Sonnenrichtung geschert und etwas
# verbreitert -- eine bloss gestauchte Silhouette sieht aus wie ein Fleck.
sh_h = max(1, int(bh * SCH_LANG))
sh_b = int(bw * 1.14)
flach = a.resize((sh_b, sh_h), Image.LANCZOS)
schere = sh_b * 0.55                                   # Versatz der hinteren Kante
flach = flach.transform((int(sh_b + schere), sh_h), Image.AFFINE,
                        (1, schere / sh_h, -schere, 0, 1, 0), resample=Image.BICUBIC)
sch = Image.new("L", ZIEL, 0)
sch.paste(flach, (px - int(bw * 0.03), int(H * BODEN) - sh_h // 2))
sch = sch.filter(ImageFilter.GaussianBlur(9))
# Kontaktschatten: schmaler, dunkler, direkt unter dem Fahrwerk
k_h = max(1, int(bh * 0.055))
kon = Image.new("L", ZIEL, 0)
kon.paste(a.crop((0, int(bh * 0.86), bw, bh)).resize((int(bw * 0.92), k_h), Image.LANCZOS),
          (px + int(bw * 0.055), int(H * BODEN) - k_h // 2))
kon = kon.filter(ImageFilter.GaussianBlur(4))
sch = Image.fromarray(np.maximum(np.asarray(sch), np.asarray(kon)), "L")
# Der Schatten dunkelt ab, statt eine dunkle Farbe darueberzulegen: unter dem Rover
# liegt im Originalfoto ohnehin schon dunkler Boden, dort geht ein aufgelegter Fleck
# unter. Multiplizieren wirkt auf hellem wie auf dunklem Untergrund.
s = np.asarray(sch, dtype=np.float32) / 255.0
bg = np.asarray(hg, dtype=np.float32) / 255.0
bg = bg * (1.0 - s[..., None] * SCHATTEN)
kuehl = np.array([0.30, 0.21, 0.19], dtype=np.float32)       # Schatten auf Mars bleibt rotbraun
bg = bg * (1 - 0.10 * s[..., None]) + kuehl * (0.10 * s[..., None])
bild = Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8), "RGB").convert("RGBA")
print("   Schatten: Kern auf %.0f %% Helligkeit, %.1f %% der Flaeche beruehrt"
      % (100 * (1 - s.max() * SCHATTEN), 100.0 * (s > 0.15).mean()))
# ---------- Staubfahne hinter dem Rover ----------
# Der Rover schaut nach links hinten, faehrt also dorthin; aufgewirbelter Staub
# bleibt zurueck und zieht nach rechts weg, steigt dabei und wird duenner.
# Sie wird VOR dem Rover aufgetragen, damit er davorsteht und nicht darin.
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
basis = H * BODEN
nf = gezogen(55, 41, 3.6) * 0.55 + gezogen(26, 47, 2.8) * 0.3 + gezogen(11, 53, 2.2) * 0.15
nf = (nf - nf.min()) / (nf.max() - nf.min())
x0 = px + bw * 0.72
d = np.clip(X - x0, 0, None)
mitte = basis - bh * 0.10 - 0.20 * d                       # die Fahne steigt
breite = bh * 0.13 + 0.26 * d                              # und wird breiter
fahne = np.exp(-d / (bw * 1.05)) * np.exp(-((Y - mitte) ** 2) / (2 * breite ** 2))
fahne *= (X > x0)
m_fahne = np.clip((nf - 0.40) / 0.45, 0, 1) ** 1.1 * fahne * FAHNE
m_fahne = np.clip(m_fahne, 0, 0.72)
print("   Staubfahne: Spitze %.2f, %.1f %% der Flaeche" % (m_fahne.max(), 100.0 * (m_fahne > 0.15).mean()))
bild = staub_auf(bild, m_fahne).convert("RGBA")

bild.alpha_composite(rov, (px, py))

# ---------- Staubwolke davor ----------
def rauschen(form, k, saat):
    r = np.random.default_rng(saat)
    klein = r.random((max(2, form[0] // k), max(2, form[1] // k))).astype(np.float32)
    g = Image.fromarray((klein * 255).astype(np.uint8), "L").resize((form[1], form[0]), Image.BICUBIC)
    return np.asarray(g, dtype=np.float32) / 255.0

n = (gezogen(70, 3, 3.2) * 0.5 + gezogen(34, 11, 2.6) * 0.32 + gezogen(14, 23, 2.0) * 0.18)
n = (n - n.min()) / (n.max() - n.min())

hoehe = np.exp(-np.clip(basis - Y, 0, None) ** 2 / (2 * (bh * 0.22) ** 2))   # nach oben auslaufend
hoehe *= np.exp(-np.clip(Y - basis, 0, None) ** 2 / (2 * (bh * 0.26) ** 2))  # nach unten auslaufend
# drei Schwaden statt einer gleichmaessigen Wolke
seite = np.zeros_like(X)
for mx, br, st in ((0.16, 0.34, 1.00), (0.58, 0.26, 0.82), (0.98, 0.20, 0.34)):
    seite = np.maximum(seite, st * np.exp(-((X - (px + bw * mx)) ** 2) / (2 * (bw * br) ** 2)))
maske = np.clip((n - 0.46) / 0.40, 0, 1) ** 1.1 * hoehe * seite * STAUB
maske = np.clip(maske, 0, 0.78)
print("   Staubmaske: Spitze %.2f, Flaeche ueber 0.2: %.1f%%"
      % (maske.max(), 100.0 * (maske > 0.2).mean()))

bild = staub_auf(bild, maske)

# ---------- Quellenangabe ----------
text = "Hintergrund: NASA/JPL-Caltech/MSSS \u2014 PIA20840, Murray Buttes, Gale-Krater"
schrift = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 17)
d = ImageDraw.Draw(bild)
tb = d.textbbox((0, 0), text, font=schrift)
tx, ty = W - (tb[2] - tb[0]) - 16, H - (tb[3] - tb[1]) - 20
for dx in (-1, 0, 1):
    for dy in (-1, 0, 1):
        if dx or dy:
            d.text((tx + dx, ty + dy), text, font=schrift, fill=(0, 0, 0))
d.text((tx, ty), text, font=schrift, fill=(240, 234, 228))

bild.save(os.path.join(SP, AUSGABE))
print("Rover %d x %d bei (%d, %d) -- fertig" % (bw, bh, px, py))
