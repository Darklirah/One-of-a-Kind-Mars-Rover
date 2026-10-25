# Rover in die Marslandschaft einpassen: Groesse, Licht, Kanten, Staub.
import os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

SP = sys.argv[1]
ZIEL = (1300, 900)
W, H = ZIEL

# ---------- Stellschrauben ----------
GROESSE   = 0.44    # Breite des Rovers als Anteil der Bildbreite (kleiner = weiter hinten)
BODEN     = 0.80    # Hoehe, auf der er aufsetzt (hoeher im Bild = weiter hinten)
DUNST     = 0.20    # wieviel Hintergrundfarbe in den Rover gemischt wird (Luftperspektive)
SATT      = 0.80    # Farbigkeit des Rovers (1 = wie gerendert)
WEICH     = 1.6     # Weichzeichnung der Silhouettenkante in Pixeln
LICHT     = (-1.0, -1.0)   # Sonnenrichtung in Bildkoordinaten: von oben links
STAUB     = 0.80    # Staerke der Staubwolke

hg = Image.open(os.path.join(SP, "hintergrund.png")).convert("RGB")

# ---------- Rover vorbereiten ----------
rov = Image.open(os.path.join(SP, "rover_freigestellt.png")).convert("RGBA")
rov = rov.crop(rov.getchannel("A").getbbox())
bw = int(W * GROESSE)
bh = int(rov.size[1] * bw / rov.size[0])
rov = rov.resize((bw, bh), Image.LANCZOS)
px, py = (W - bw) // 2, int(H * BODEN) - bh

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
rov.putalpha(a)

# ---------- Schlagschatten nach rechts unten ----------
sh_h = max(1, int(bh * 0.15))
sch = Image.new("L", ZIEL, 0)
sch.paste(a.resize((bw, sh_h), Image.LANCZOS), (px + int(bw * 0.07), int(H * BODEN) - sh_h // 2))
sch = sch.filter(ImageFilter.GaussianBlur(15)).point(lambda v: int(v * 0.52))
# Kontaktschatten: schmaler, dunkler, direkt unter dem Fahrwerk
k_h = max(1, int(bh * 0.055))
kon = Image.new("L", ZIEL, 0)
kon.paste(a.crop((0, int(bh * 0.86), bw, bh)).resize((int(bw * 0.92), k_h), Image.LANCZOS),
          (px + int(bw * 0.055), int(H * BODEN) - k_h // 2))
kon = kon.filter(ImageFilter.GaussianBlur(5)).point(lambda v: int(v * 0.80))
sch = Image.fromarray(np.maximum(np.asarray(sch), np.asarray(kon)), "L")
bild = Image.composite(Image.new("RGB", ZIEL, (30, 18, 12)), hg, sch).convert("RGBA")
bild.alpha_composite(rov, (px, py))

# ---------- Staubwolke davor ----------
def rauschen(form, k, saat):
    r = np.random.default_rng(saat)
    klein = r.random((max(2, form[0] // k), max(2, form[1] // k))).astype(np.float32)
    g = Image.fromarray((klein * 255).astype(np.uint8), "L").resize((form[1], form[0]), Image.BICUBIC)
    return np.asarray(g, dtype=np.float32) / 255.0

def gezogen(k, saat, streckung):
    """Rauschen, in X gestreckt -- das ergibt vom Wind gezogene Schlieren."""
    r = np.random.default_rng(saat)
    klein = r.random((max(2, H // k), max(2, int(W / (k * streckung))))).astype(np.float32)
    g = Image.fromarray((klein * 255).astype(np.uint8), "L").resize((W, H), Image.BICUBIC)
    return np.asarray(g, dtype=np.float32) / 255.0

n = (gezogen(70, 3, 3.2) * 0.5 + gezogen(34, 11, 2.6) * 0.32 + gezogen(14, 23, 2.0) * 0.18)
n = (n - n.min()) / (n.max() - n.min())

Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
basis = H * BODEN
hoehe = np.exp(-np.clip(basis - Y, 0, None) ** 2 / (2 * (bh * 0.30) ** 2))   # nach oben auslaufend
hoehe *= np.exp(-np.clip(Y - basis, 0, None) ** 2 / (2 * (bh * 0.22) ** 2))  # nach unten auslaufend
# drei Schwaden statt einer gleichmaessigen Wolke
seite = np.zeros_like(X)
for mx, br, st in ((0.18, 0.30, 1.00), (0.62, 0.22, 0.85), (0.92, 0.26, 0.70)):
    seite = np.maximum(seite, st * np.exp(-((X - (px + bw * mx)) ** 2) / (2 * (bw * br) ** 2)))
maske = np.clip((n - 0.46) / 0.40, 0, 1) ** 1.1 * hoehe * seite * STAUB
maske = np.clip(maske, 0, 0.78)
print("   Staubmaske: Spitze %.2f, Flaeche ueber 0.2: %.1f%%"
      % (maske.max(), 100.0 * (maske > 0.2).mean()))

# Staub streut das Licht: er nimmt dem Untergrund die Zeichnung UND hellt ihn auf.
# Beides zusammen laesst ihn erst als Staub lesen, Aufhellen allein wirkt wie ein Schleier.
b = np.asarray(bild.convert("RGB"), dtype=np.float32) / 255.0
weich = np.asarray(bild.convert("RGB").filter(ImageFilter.GaussianBlur(7)),
                   dtype=np.float32) / 255.0
m = maske[..., None]
b = b * (1 - m * 0.85) + weich * (m * 0.85)
staub_farbe = np.array([0.80, 0.655, 0.555], dtype=np.float32)
b = b * (1 - m) + staub_farbe * m
bild = Image.fromarray((np.clip(b, 0, 1) * 255).astype(np.uint8), "RGB")

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

bild.save(os.path.join(SP, "montage2.png"))
print("Rover %d x %d bei (%d, %d) -- fertig" % (bw, bh, px, py))
