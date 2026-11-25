#!/usr/bin/env python3
"""THE WORLD TODAY - front page for Wednesday 25 November 2026.
Deterministic: fixed seed, no timestamps, no network. PIL only.
Writes entry.png (1200x1720) next to this script's parent dir.
Structure (playbook): 3 leads + 10 secondary + 22 briefs = 35 stories,
timeline, markets strip, numbered world map, DATE CHECK box.
All 35 stories first reported on 25 Nov 2026; see NEWS.md for sources.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "entry.png"

W, H = 1200, 1800
MARGIN = 44
CW = W - 2 * MARGIN  # 1112

PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (158, 27, 27)
GREY = (85, 85, 85)
LIGHT_GREY = (120, 115, 105)
NAVY = (28, 42, 68)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

RNG = random.Random(20261125)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip() if cur else w
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(path, text, max_size, max_w, min_size=10):
    size = max_size
    while size > min_size:
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def draw_centered(d, y, text, fnt, fill=INK):
    d.text((W / 2, y), text, font=fnt, fill=fill, anchor="ma")


def draw_wrapped(d, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, y, x0, x1, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)
d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

y = 24

# ---------------------------------------------------------------- masthead
mast_f = fit_font(SERIF_B, "THE WORLD TODAY", 78, CW)
draw_centered(d, y, "THE WORLD TODAY", mast_f)
y += int(mast_f.size * 1.06)

date_f = font(SANS_B, 25)
draw_centered(d, y, "WEDNESDAY,  25  NOVEMBER  2026", date_f)
y += 34

tag_f = font(SANS, 15)
draw_centered(d, y, "THE DAY'S WORLD NEWS  —  IN ONE PAGE  •  35 STORIES, ALL FIRST REPORTED TODAY",
              tag_f, fill=GREY)
y += 22

rule(d, y, MARGIN, W - MARGIN, width=4, fill=RED)
y += 7
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 12

# ---------------------------------------------------------------- timeline strip
d.text((MARGIN, y), "THE DAY IN TIME  (WIB)", font=font(SANS_B, 15), fill=RED)
tl = ("06:59  WHO evacuates Congo staff  •  07:18  Shenzhou-24 lifts off  •  "
      "07:41  Tariff findings due  •  10:36  US sanctions Turkish firm")
draw_wrapped(d, MARGIN, y + 20, tl, font(SANS, 15), CW, leading=19)
y += 40
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 10

# ---------------------------------------------------------------- LEAD 1: Shenzhou-24
d.text((MARGIN, y), "SPACE  •  LEAD STORY", font=font(SANS_B, 17), fill=RED)
y += 22
lead_f = font(SERIF_B, 42)
d.text((MARGIN, y), "PAKISTAN REACHES ORBIT AS", font=lead_f, fill=INK)
y += 48
d.text((MARGIN, y), "SHENZHOU-24 BLASTS OFF", font=lead_f, fill=INK)
y += 50
deck_f = font(SERIF, 20)
deck = ("China launches three astronauts to its Tiangong station — Muhammad "
        "Zeeshan Ali, 40, becomes the first Pakistani in orbit and the first "
        "foreigner ever to visit the Chinese station.")
y = draw_wrapped(d, MARGIN, y, deck, deck_f, CW, leading=24)
y += 8

# --- illustration: rocket launch at dawn over Jiuquan
box_x0, box_y0 = MARGIN, y
box_x1, box_y1 = W - MARGIN, y + 150
bw, bh = box_x1 - box_x0, box_y1 - box_y0
horizon = box_y0 + bh - 34
# dawn sky gradient
sky_top = (18, 28, 58)
sky_low = (232, 148, 72)
for i in range(horizon - box_y0):
    t = i / max(1, horizon - box_y0 - 1)
    c = tuple(int(sky_top[k] + (sky_low[k] - sky_top[k]) * t) for k in range(3))
    d.line([(box_x0, box_y0 + i), (box_x1, box_y0 + i)], fill=c)
# stars
for _ in range(46):
    sx = box_x0 + RNG.randint(4, bw - 4)
    sy = box_y0 + RNG.randint(4, 70)
    r = RNG.randint(1, 2)
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(240, 240, 220))
# distant moon
d.ellipse([box_x1 - 90, box_y0 + 16, box_x1 - 46, box_y0 + 60], fill=(238, 232, 210))
d.ellipse([box_x1 - 80, box_y0 + 26, box_x1 - 66, box_y0 + 40], fill=(214, 206, 184))
# desert ground
d.rectangle([box_x0, horizon, box_x1, box_y1], fill=(58, 44, 34))
d.rectangle([box_x0, horizon, box_x1, horizon + 4], fill=(90, 70, 52))
# launch gantry (thin, left of the rocket)
gx0 = box_x0 + 90
d.line([(gx0, horizon - 88), (gx0, horizon)], fill=(40, 40, 46), width=5)
d.line([(gx0, horizon - 88), (gx0 + 70, horizon - 88)], fill=(40, 40, 46), width=4)
d.line([(gx0 + 70, horizon - 88), (gx0 + 70, horizon - 60)], fill=(40, 40, 46), width=3)
d.rectangle([gx0 - 14, horizon - 6, gx0 + 84, horizon], fill=(52, 48, 44))
# --- rocket (centre-right, rising)
rx = box_x0 + bw // 2 + 130
ry_top = box_y0 + 8
ry_bot = horizon - 26
rwid = 42
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
# exhaust flame below the body
for r, col in [(26, (255, 90, 10, 255)), (19, (255, 150, 30, 255)),
               (12, (255, 210, 80, 255)), (7, (255, 240, 180, 255))]:
    od.ellipse([rx - r, ry_bot + 2, rx + r, ry_bot + 2 + 2 * r], fill=col)
# smoke puffs at pad
for i, r in enumerate([16, 20, 24]):
    jx = rx - 60 + i * 26 + RNG.randint(-4, 4)
    jy = horizon - 8 - i * 4
    od.ellipse([jx - r, jy - r, jx + r, jy + r], fill=(200, 196, 190, 120))
# body
od.rectangle([rx - rwid // 2, ry_top + 26, rx + rwid // 2, ry_bot], fill=(235, 236, 238, 255))
od.polygon([(rx - rwid // 2, ry_top + 26), (rx, ry_top), (rx + rwid // 2, ry_top + 26)],
           fill=(158, 27, 27, 255))
# window + flag band
od.ellipse([rx - 7, ry_top + 44, rx + 7, ry_top + 58], fill=(28, 42, 68, 255))
od.rectangle([rx - rwid // 2, ry_top + 72, rx + rwid // 2, ry_top + 82], fill=(158, 27, 27, 255))
# fins
od.polygon([(rx - rwid // 2, ry_bot - 34), (rx - rwid // 2 - 22, ry_bot),
            (rx - rwid // 2, ry_bot)], fill=(158, 27, 27, 255))
od.polygon([(rx + rwid // 2, ry_bot - 34), (rx + rwid // 2 + 22, ry_bot),
            (rx + rwid // 2, ry_bot)], fill=(158, 27, 27, 255))
# "TIANGONG" station silhouette top-left
sx0, sy0 = box_x0 + 120, box_y0 + 26
od.rectangle([sx0, sy0 + 8, sx0 + 150, sy0 + 18], fill=(200, 204, 210, 255))
od.rectangle([sx0 + 60, sy0, sx0 + 90, sy0 + 26], fill=(170, 176, 184, 255))
od.rectangle([sx0 - 26, sy0 + 4, sx0, sy0 + 22], fill=(60, 90, 160, 255))
od.rectangle([sx0 + 150, sy0 + 4, sx0 + 176, sy0 + 22], fill=(60, 90, 160, 255))
od.text((sx0 + 8, sy0 + 26), "TIANGONG", font=font(SANS_B, 12), fill=(240, 240, 230, 255))
ov_c = ov.crop((box_x0, box_y0, box_x1, box_y1))
img.paste(ov_c, (box_x0, box_y0), ov_c)
d = ImageDraw.Draw(img)
d.rectangle([box_x0, box_y0, box_x1, box_y1], outline=INK, width=2)
# caption
cap_f = font(SANS, 13)
d.text((MARGIN, box_y1 + 6),
       "Long March 2F lifts off from Jiuquan, 08:18 Beijing time. Crew: Tang Hongbo, Wu Yi, Muhammad Zeeshan Ali — 5–10 days aboard Tiangong.",
       font=cap_f, fill=GREY)
y = box_y1 + 26
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 12

# ---------------------------------------------------------------- LEADS 2 & 3 (two columns)
col_w = (CW - 28) // 2
col2_x = MARGIN + col_w + 28
lead23_y0 = y

def mini_tariff(d, x0, y0, w, h):
    """Brick tariff wall with rising bars."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 210), outline=INK, width=2)
    # bars
    vals = [("15%", 0.55), ("19%", 0.72), ("25%", 0.95)]
    bw2 = 40
    gap = (w - 3 * bw2 - 40) // 2
    bx = x0 + 22
    for lab, frac in vals:
        bh2 = int((h - 36) * frac)
        d.rectangle([bx, y0 + h - 12 - bh2, bx + bw2, y0 + h - 12], fill=RED)
        d.text((bx + bw2 // 2, y0 + h - 12 - bh2 - 16), lab, font=font(SANS_B, 13),
               fill=INK, anchor="ma")
        bx += bw2 + gap
    d.text((x0 + w // 2, y0 + 4), "16 PARTNERS", font=font(SANS_B, 12), fill=GREY, anchor="ma")


def mini_clinic(d, x0, y0, w, h):
    """Field hospital tent with red cross, DRC. All art inside the box."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 228, 214), outline=INK, width=2)
    d.text((x0 + 8, y0 + 4), "ITURI, DR CONGO", font=font(SANS_B, 12), fill=GREY)
    # ground
    gy = y0 + h - 14
    d.rectangle([x0, gy, x0 + w, y0 + h], fill=(120, 96, 66))
    # tent: apex just below the label, base on the ground
    tx, ty = x0 + w // 2, gy
    apex = y0 + 20
    d.polygon([(tx - 66, ty), (tx, apex), (tx + 66, ty)], fill=(244, 240, 226),
              outline=INK)
    d.polygon([(tx - 15, ty), (tx, ty - 18), (tx + 15, ty)], fill=(60, 60, 60))
    # small flag on the apex, inside the box
    d.line([(tx, apex), (tx, apex - 12)], fill=INK, width=2)
    d.rectangle([tx, apex - 12, tx + 18, apex - 2], fill=(255, 255, 255), outline=INK)
    d.rectangle([tx + 6, apex - 11, tx + 12, apex - 3], fill=RED)
    d.rectangle([tx + 3, apex - 8, tx + 15, apex - 6], fill=RED)
    # red cross on the tent
    cy = apex + 14
    d.rectangle([tx - 5, cy - 8, tx + 5, cy + 8], fill=RED)
    d.rectangle([tx - 11, cy - 3, tx + 11, cy + 3], fill=RED)


# --- Lead 2: tariffs
d.text((MARGIN, lead23_y0), "TRADE", font=font(SANS_B, 15), fill=RED)
hf = font(SERIF_B, 27)
d.text((MARGIN, lead23_y0 + 21), "NEW US TARIFFS", font=hf, fill=INK)
d.text((MARGIN, lead23_y0 + 52), "DUE ON 16 PARTNERS", font=hf, fill=INK)
y2 = draw_wrapped(d, MARGIN, lead23_y0 + 88,
                  "Section 301 findings expected today: duties of 15–25% on "
                  "China, the EU and 14 more — stacked on existing tariffs.",
                  font(SANS, 16), col_w, leading=20)
mini_tariff(d, MARGIN, y2 + 6, col_w, 70)
lead2_bot = y2 + 6 + 92

# --- Lead 3: WHO / Ebola
d.text((col2_x, lead23_y0), "HEALTH", font=font(SANS_B, 15), fill=RED)
d.text((col2_x, lead23_y0 + 21), "WHO PULLS EBOLA", font=hf, fill=INK)
d.text((col2_x, lead23_y0 + 52), "STAFF FROM CONGO", font=hf, fill=INK)
y3 = draw_wrapped(d, col2_x, lead23_y0 + 88,
                  "Teams evacuated from an Ituri hospital after three days "
                  "sheltering from fighting. Outbreak toll: 5,775 dead of "
                  "11,762 cases.",
                  font(SANS, 16), col_w, leading=20)
mini_clinic(d, col2_x, y3 + 6, col_w, 70)
lead3_bot = y3 + 6 + 92

y = max(lead2_bot, lead3_bot) + 8
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 8

# ---------------------------------------------------------------- markets strip
d.text((MARGIN, y), "THE MARKETS — TUESDAY'S CLOSE, IN TODAY'S WRAPS",
       font=font(SANS_B, 16), fill=INK)
y += 22
mk = [("DOW", "50,018.70  +0.85%"), ("S&P 500", "7,201.09  −0.50%"),
      ("NASDAQ", "23,733.54  −1.48%"), ("BRENT", "$91.40  +2.27%"),
      ("WTI", "$82.05  +2.35%"), ("GOLD", "$3,556  −2.2%"),
      ("BITCOIN", "~$59,600"), ("NVIDIA", "−5.9%")]
mx = MARGIN
seg_w = CW // 4
for i, (k, v) in enumerate(mk):
    cx = MARGIN + (i % 4) * seg_w
    cy = y + (i // 4) * 26
    kf = font(SANS_B, 15)
    d.text((cx, cy), f"{k} ", font=kf, fill=RED)
    d.text((cx + kf.getlength(f"{k} "), cy), v, font=font(SANS, 15), fill=INK)
y += 50
d.text((MARGIN, y),
       "PCE inflation + Q3 GDP due tonight, 21:30 WIB  •  US consumer confidence 103.3, highest since Jan 2025  •  Dec Fed hike odds 96–97%",
       font=font(SANS, 14), fill=GREY)
y += 18
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 8

# ---------------------------------------------------------------- secondary 10 (numbered 4–13)
d.text((MARGIN, y), "THE REST OF THE DAY — IN BRIEF", font=font(SANS_B, 18), fill=INK)
y += 26
sec = [
    ("4", "Lukashenko offers to fly with Zelenskiy to Moscow for talks."),
    ("5", "Moscow summons Latvia's diplomat; Riga weighs closing its border."),
    ("6", "Iran's rial falls to an all-time low after fresh US sanctions."),
    ("7", "US sanctions a Turkish firm over Iran's covert banking network."),
    ("8", "Senate probes VP Vance over alleged Vitol Venezuela oil-deal ties."),
    ("9", "UK warns defence suppliers to brace for Russian sabotage."),
    ("10", "EU urges stricter visa rules for Russians; no 5-year passports."),
    ("11", "Ipsos reports a major incident in its internal systems."),
    ("12", "Australia AI report: mandatory incident reporting, licensing."),
    ("13", "Army to detonate the entire US lead-azide stockpile in Iowa today."),
]
sec_row_h = 38
for i, (num, text) in enumerate(sec):
    sx = MARGIN + (i % 2) * (col_w + 28)
    sy = y + (i // 2) * sec_row_h
    nf = font(SANS_B, 17)
    d.text((sx, sy), num, font=nf, fill=RED)
    nw = nf.getlength(num + "  ")
    draw_wrapped(d, sx + nw, sy, text, font(SANS, 16), col_w - nw, leading=20)
y += 5 * sec_row_h + 2
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 8

# ---------------------------------------------------------------- world map (numbered pins)
d.text((MARGIN, y), "WHERE IT HAPPENED", font=font(SANS_B, 18), fill=INK)
y += 26
map_x0, map_y0 = MARGIN, y
map_x1, map_y1 = W - MARGIN, y + 168
d.rectangle([map_x0, map_y0, map_x1, map_y1], fill=(222, 232, 238), outline=INK, width=2)
mw, mh = map_x1 - map_x0, map_y1 - map_y0
# rough continents (equirectangular blobs, code-drawn)
SEA = (222, 232, 238)
LAND = (168, 178, 150)
# North America
OX, OY = map_x0, map_y0
def P(pts):
    return [(OX + x, OY + y) for x, y in pts]
d.polygon(P([(70, 28), (150, 18), (230, 26), (260, 44), (250, 70), (190, 84),
           (150, 96), (96, 78), (60, 52)]), fill=LAND)
# South America
d.polygon(P([(300, 96), (340, 92), (368, 112), (352, 150), (322, 142), (296, 118)]), fill=LAND)
# Europe
d.polygon(P([(520, 22), (580, 16), (620, 30), (610, 52), (560, 56), (520, 44)]), fill=LAND)
# Africa
d.polygon(P([(540, 66), (600, 62), (630, 84), (616, 122), (576, 128), (548, 100)]), fill=LAND)
# Asia
d.polygon(P([(640, 20), (760, 12), (880, 20), (960, 34), (980, 56), (920, 72),
           (840, 78), (760, 70), (680, 62), (636, 44)]), fill=LAND)
# Australia
d.polygon(P([(880, 122), (950, 118), (972, 136), (930, 150), (884, 140)]), fill=LAND)
# graticule
for gx in range(map_x0 + 90, map_x1, 90):
    d.line([(gx, map_y0), (gx, map_y1)], fill=(200, 212, 220), width=1)
for gy in range(map_y0 + 42, map_y1, 42):
    d.line([(map_x0, gy), (map_x1, gy)], fill=(200, 212, 220), width=1)

# pins: (num, label, x, y) in map coords
pins = [
    ("1", "JIUQUAN", 905, 52), ("2", "WASHINGTON", 188, 44),
    ("3", "ITURI", 590, 104), ("4", "MOSCOW", 626, 22),
    ("5", "RIGA", 558, 18), ("6", "TEHRAN", 668, 56),
    ("7", "ANKARA", 620, 54), ("8", "LONDON", 536, 34),
    ("9", "CANBERRA", 928, 136), ("10", "IOWA", 118, 74),
]
for num, lab, px, py in pins:
    d.ellipse([map_x0 + px - 11, map_y0 + py - 11, map_x0 + px + 11, map_y0 + py + 11],
              fill=RED, outline=(255, 255, 255), width=2)
    tf = font(SANS_B, 11)
    tw = tf.getlength(num)
    d.text((map_x0 + px - tw / 2, map_y0 + py - 7), num, font=tf, fill=(255, 255, 255))
y = map_y1 + 6
key = ("1 JIUQUAN   2 WASHINGTON   3 ITURI   4 MOSCOW   5 RIGA   6 TEHRAN   "
       "7 ANKARA   8 LONDON   9 CANBERRA   10 IOWA")
d.text((MARGIN, y), key, font=font(SANS, 13), fill=GREY)
y += 16
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 8

# ---------------------------------------------------------------- briefs 22: ALSO ON 25 NOVEMBER
d.text((MARGIN, y), "ALSO ON 25 NOVEMBER", font=font(SANS_B, 18), fill=INK)
y += 20
briefs = [
    "BJP–SAD ally for 2027 Punjab polls",
    "India to buy 76 naval helicopters, ₹15,000 Cr",
    "US blacklists Singapore chip firm Megaspeed",
    "Zelenskiy turns to new Congress for aid",
    "Dev Deepawali lights Varanasi; Murmu at Bali Jatra",
    "German-African Business Summit opens in Ghana",
    "CILAC forum in Brasília; Solar Expo in Chennai",
    "Gaza: 3 killed in strikes, incl. UN worker",
    "Russia pummels Ukraine: 8 killed, bridges hit",
    "Fears grow of all-out US–Iran war",
    "Iran revises tanker-convoy claims",
    "India extends mining accreditation to 5 years",
    "J&K police stop Mehbooba Mufti at Chandanwari",
    "SP names its UP 2027 candidates",
    "India denies defence breach; orders cyber audit",
    "Delhi hosts first India–EU Maritime Roundtable",
    "Priyansh Arya hits 181 in SMAT — top Indian T20 score",
    "NATO plans early-warning aircraft for Poland",
    "UN flags Gaza humanitarian strain",
    "Russia, Ukraine trade UN accusations on Black Sea",
    "Germany releases detailed Q3 GDP today (+0.2%)",
    "US markets shut Thu for Thanksgiving; PCE due tonight",
]
bf = font(SANS, 15)
row_h = 18
for i, text in enumerate(briefs):
    bx = MARGIN + (i % 2) * (col_w + 28)
    by = y + (i // 2) * row_h
    d.text((bx, by), "▪", font=bf, fill=RED)
    d.text((bx + 16, by), text, font=bf, fill=INK)
y += 11 * row_h + 4
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 8

# ---------------------------------------------------------------- DATE CHECK box
box_y0 = y
d.rectangle([MARGIN, box_y0, W - MARGIN, box_y0 + 118], fill=(238, 230, 214),
            outline=RED, width=2)
d.text((MARGIN + 12, box_y0 + 8), "DATE CHECK — BIG STORIES THAT ARE NOT 25 NOVEMBER",
       font=font(SANS_B, 15), fill=RED)
dc = [
    "Riyadh tower, 2nd Houthi strike, 11 hurt — 24 Nov",
    "CIA/ODNI breach first reported — 24 Nov",
    "Nepal quake M5.3 (Nepal says 5.6) — 24 Nov",
    "Suryavanshi 204 off 53, 28 sixes — 24 Nov",
    "Anmer Hall arrests — 24 Nov (break-in 23 Nov)",
    "Huawei guilty, 10 of 12 counts — verdict 24 Nov",
    "Iran strikes on US bases, Bahrain — 21 Nov",
    "COP31 ends with no deal — 23 Nov",
    "Shanghai chief Chen Jining probed — 24 Nov",
    "England beat Australia, 2nd T20I — 24 Nov",
]
dcf = font(SANS, 14)
for i, text in enumerate(dc):
    bx = MARGIN + 12 + (i % 2) * ((CW - 24) // 2)
    by = box_y0 + 30 + (i // 2) * 17
    d.text((bx, by), "✕  " + text, font=dcf, fill=INK)
y = box_y0 + 118 + 6
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 6

# ---------------------------------------------------------------- footer
foot_f = font(SANS_B, 13)
draw_centered(d, y, "THE WORLD TODAY  •  WEDNESDAY 25 NOVEMBER 2026  •  SOURCES: REUTERS, XINHUA, AP, AAP, AL JAZEERA",
              foot_f, fill=GREY)
y += 20
print("final y:", y, "canvas H:", H)
assert y <= H - 24, f"overflow: y={y} > {H}"

img.save(OUT, format="PNG", optimize=True)
print("saved", OUT, img.size)
