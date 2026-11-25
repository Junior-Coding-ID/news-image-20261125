#!/usr/bin/env python3
"""Render THE GLOBAL BRIEF — Wednesday 25 November 2026 (news-image-20261125 v3).

36 dated stories, 6 regions, UTC timeline, 12 drawn pictogram scenes,
mini world map, how-sure labels, DATE CHECK footer.
Pure PIL, no network, deterministic. All stories from
research-25nov-v3.md (verified 25 Nov 2026 only); nothing from 24 Nov
or earlier is drawn.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 16

BG = (244, 247, 251)
INK = (17, 24, 39)
MUTED = (71, 85, 105)
FAINT = (100, 116, 139)
LINE = (203, 213, 225)
NAVY = (15, 23, 42)
WHITE = (255, 255, 255)
CREAM = (255, 251, 235)
BLUE = (37, 99, 235)
RED = (220, 38, 38)
AMBER = (217, 119, 6)
PURPLE = (124, 58, 237)
TEAL = (13, 148, 136)
ORANGE = (234, 88, 12)
GREEN = (22, 163, 74)
YELLOW = (251, 191, 36)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# (number, region_index, title, detail, how_sure)
# how_sure: ✓ verified 2+ sources | ◐ single source | ? unconfirmed | → scheduled
STORIES = [
    # R1 — SPACE & SCIENCE
    (1, 0, "SHENZHOU-24 LAUNCH",
     "00:18 UTC, Jiuquan; first Pakistani in orbit, first foreigner to Tiangong", "✓"),
    (2, 0, "SHENZHOU-24 DOCKS",
     "Docked with Tiangong hours after launch, Wednesday morning", "✓"),
    (3, 0, "HERA REVEAL TONIGHT",
     "ESA first Dimorphos close-ups, 19:45 CET livestream from Berlin", "→"),
    # R2 — MIDDLE EAST & GULF
    (4, 1, "HORMUZ TANKERS BURN",
     "IRGC: two oil tankers hit by sea mines, exploded and burned", "✓"),
    (5, 1, 'IRAN: "NOT WORRIED"',
     "VP Aref: no worry over US sea blockade; new surveillance in strait", "✓"),
    (6, 1, "RAS TANURA HIT?",
     "Houthis claim refinery strike, fire; coalition: 4 drones downed", "?"),
    (7, 1, "GAZA: HAMAS COLONEL KILLED",
     "Israeli strike kills Col. Abuelouf, wife + 2 children, Beach camp", "✓"),
    # R3 — RUSSIA–UKRAINE & EUROPE
    (8, 2, "REFINERIES ABLAZE",
     "Ukraine drones hit Rosneft Syzran & Kuibyshev refineries; both on fire, 1 dead", "✓"),
    (9, 2, "ODESA STRIKE",
     "Russian strike: 2 dead, 3 hurt incl. child; Kyiv apartment fire, 2 hurt", "✓"),
    (10, 2, "490,334 RUSSIAN DEAD",
     "BBC analysis of leaked Russian govt death data: 490,334+ soldiers since 2022", "✓"),
    (11, 2, "LIBYA VOWS REVENGE",
     "Libyan army vows revenge on Ukraine; 2 navy officers killed in Benghazi drone hit", "✓"),
    (12, 2, 'ITALY: "WRONG"',
     "FM Tajani: Ukraine wrong to hit Russian ship off Libya; warns against wider war", "✓"),
    (13, 2, "POLAND WANTS US TROOPS",
     "Poland pushes permanent US military presence after 2 airspace violations", "✓"),
    (14, 2, 'MERZ: RUSSIA "ESCALATING"',
     "Chancellor Merz accuses Russia of escalating threats to European security", "✓"),
    (15, 2, "GERMANY MEETS ON US PULLBACK",
     "Senior defence officials meet today on US military pullback from Europe", "◐"),
    (16, 2, "GERMANY GDP +0.1%",
     "Q3 GDP +0.1% QoQ (revised down from 0.2%), +1.1% YoY; exports -1.0%", "✓"),
    # R4 — ASIA–PACIFIC
    (17, 3, "AUSTRALIA CPI 4.9%",
     "CPI +4.9% YoY to Oct (from 4.3%); trimmed mean 3.8%; power +25.2%, fuel +32.5%", "✓"),
    (18, 3, "JAPAN SERVICES +4.2%",
     "Services PPI +4.2% YoY Oct, fastest since 1990; sea freight +120.4%", "✓"),
    (19, 3, "ASIA ROUT",
     "KOSPI -6.16% (Samsung -9.9%, SK Hynix -11.1%); Nikkei -2.78%; Taiwan ~-5%", "✓"),
    (20, 3, "SOLOMONS TREATY",
     "Solomons & Australia sign treaty: no foreign military bases; 2022 China pact not renewed", "✓"),
    (21, 3, "N. KOREA EXPELS SWISS",
     "Pyongyang orders Swiss diplomat Sylvain Astier out in 48 hours, office shut", "✓"),
    (22, 3, "QUAKE M5.9",
     "M5.9 Balleny Islands, Southern Ocean, 01:38 UTC, 10 km deep; USGS green alert", "✓"),
    (23, 3, "QUAKE M5.1",
     "M5.1 Antique, Philippines, 06:29 WIB; Intensity V in Valderrama; damage expected", "◐"),
    (24, 3, "STOKES TO IPL",
     "Ben Stokes enters IPL 2027 mini-auction at top base price", "✓"),
    # R5 — AMERICAS & US ECONOMY
    (25, 4, "US PCE 3.8%",
     "PCE inflation 3.8% YoY, core 3.3% (highest since Nov 2023); Oct data, 08:30 ET", "✓"),
    (26, 4, "US GDP 4.3%",
     "Q3 GDP revised up to 4.3% (from 3.4%); durable goods +0.2%; income +0.7%", "✓"),
    (27, 4, "DELL RECORD",
     "Dell Q3 revenue $54.9bn (+103% YoY); AI servers $22.0bn (+291%)", "✓"),
    (28, 4, "TUNGSTEN $2.45BN",
     "US signs tungsten contracts worth up to $2.45bn as foreign-source ban takes effect", "✓"),
    (29, 4, "USTR TARIFFS SOON",
     "USTR to announce tariff hikes on China, EU + 14 others after subsidy probe", "◐"),
    (30, 4, "ECUADOR OPS PAUSED",
     "Trump admin pauses joint military ops with Ecuador (paused since mid-Oct)", "◐"),
    (31, 4, "ABREGO GARCIA LEAVES",
     "Kilmar Abrego Garcia voluntarily leaves US for Spain; DHS: self-deported", "✓"),
    (32, 4, "AI TOO POWERFUL?",
     "Anthropic & OpenAI staff: unreleased internal models too powerful to release safely", "◐"),
    # R6 — AFRICA, ENERGY & WORLD
    (33, 5, "SUDAN: 19 KILLED",
     "RSF drone strikes kill 19 civilians incl. 6 women in Damazin & Roseires; 20 hurt", "✓"),
    (34, 5, "POPE ON COP31",
     "Pope Leo XIV dismayed COP31 failed to reach a deal; extreme weather more frequent", "✓"),
    (35, 5, "OIL",
     "Brent $90.96 (-0.5%), WTI $81.54 (-0.62%); Goldman raises 2027 outlook", "✓"),
    (36, 5, "CARTAGENA FREED",
     "Colombia forces storm Éxito supermarket in Cartagena, free all remaining hostages", "✓"),
]

REGIONS = [
    ("R1  SPACE & SCIENCE", PURPLE, 3),
    ("R2  MIDDLE EAST & GULF", RED, 4),
    ("R3  RUSSIA–UKRAINE & EUROPE", BLUE, 9),
    ("R4  ASIA–PACIFIC", TEAL, 8),
    ("R5  AMERICAS & US ECONOMY", ORANGE, 8),
    ("R6  AFRICA, ENERGY & WORLD", GREEN, 4),
]

# (hour_utc, label) for the timeline strip
TIMELINE = [
    (0.30, "00:18  SHENZHOU LAUNCH"),
    (0.50, "00:30  AUS CPI 4.9%"),
    (1.63, "01:38  BALLENY M5.9"),
    (7.00, "07:00  GERMAN GDP"),
    (13.50, "13:30  US PCE + GDP"),
    (18.75, "18:45  HERA REVEAL"),
]

# 12 drawn scenes: (story_no, kind) — kind selects the pictogram drawer
SCENES = [
    (1, "rocket"), (4, "tanker"), (8, "refinery"), (14, "parliament"),
    (19, "chartdown"), (20, "handshake"), (3, "asteroid"), (25, "dollar"),
    (27, "chip"), (22, "globe"), (36, "shield"), (33, "drone"),
]


def fit_text(draw, text, fnt, max_w):
    """Truncate text with an ellipsis so it fits max_w."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while len(text) > 4 and draw.textlength(text + "…", font=fnt) > max_w:
        text = text[:-1]
    return text + "…"


def draw_header(draw):
    draw.rectangle([0, 0, W, 88], fill=NAVY)
    draw.text((MARGIN, 8), "THE GLOBAL BRIEF",
              font=font(FB, 34), fill=WHITE)
    pill = "WEDNESDAY  •  25 NOVEMBER 2026"
    pf = font(FB, 16)
    pw = int(draw.textlength(pill, font=pf)) + 28
    px = W - MARGIN - pw
    draw.rounded_rectangle([px, 14, W - MARGIN, 14 + 34], radius=17, fill=WHITE)
    draw.text((px + 14, 22), pill, font=pf, fill=NAVY)
    draw.text((MARGIN, 48),
              "36 dated stories  •  6 regions  •  all events 25 Nov 2026 (any timezone)",
              font=font(FB, 15), fill=(203, 213, 225))
    draw.text((MARGIN, 68),
              "HOW SURE:   ✓ verified (2+ sources)      ◐ single source      ? unconfirmed claim      → scheduled tonight",
              font=font(FR, 12), fill=(148, 163, 184))


def draw_timeline(draw):
    y0, y1 = 92, 146
    draw.rectangle([0, y0, W, y1], fill=WHITE)
    draw.line([0, y1, W, y1], fill=LINE, width=1)
    axis_y = y0 + 38
    x0, x1 = MARGIN + 8, W - MARGIN - 8
    draw.line([x0, axis_y, x1, axis_y], fill=INK, width=2)
    for h in range(0, 25, 3):
        tx = x0 + (x1 - x0) * h / 24.0
        draw.line([tx, axis_y - 4, tx, axis_y + 4], fill=INK, width=2)
        lab = "%02d:00" % h
        lw = draw.textlength(lab, font=font(FR, 9))
        draw.text((tx - lw / 2, axis_y + 7), lab, font=font(FR, 9), fill=FAINT)
    # Three rows above the axis: the 00:18 / 00:30 / 01:38 cluster is only
    # ~66 px wide, so the three early labels must stack vertically.
    rows = [y0 + 2, y0 + 14, y0 + 26]
    labels = ["00:18 Shenzhou launch", "00:30 Aus CPI 4.9%",
              "01:38 Balleny M5.9", "07:00 German GDP",
              "13:30 US PCE + GDP", "18:45 Hera reveal"]
    for i, ((hour, _old), label) in enumerate(zip(TIMELINE, labels)):
        ex = x0 + (x1 - x0) * hour / 24.0
        draw.ellipse([ex - 5, axis_y - 5, ex + 5, axis_y + 5],
                     fill=RED, outline=WHITE, width=2)
        lf = font(FB, 10)
        lw = draw.textlength(label, font=lf)
        lx = min(max(ex, MARGIN), W - MARGIN - lw)
        draw.text((lx, rows[i % 3]), label, font=lf, fill=INK)
    # Antique note: 06:29 WIB = 23:29 UTC 24 Nov, but 25 Nov in Manila
    note = "Antique quake 06:29 WIB = 23:29 UTC 24 Nov (25 Nov Manila)"
    nf = font(FR, 10)
    nw = draw.textlength(note, font=nf)
    draw.text((W - MARGIN - nw, y0 + 2), note, font=nf, fill=FAINT)


# ---- pictogram scenes (simple PIL vector drawings, 30x30 box) ----

def icon_rocket(d, x, y, s=30):
    d.polygon([(x + s * 0.5, y), (x + s * 0.68, y + s * 0.45),
               (x + s * 0.5, y + s * 0.62), (x + s * 0.32, y + s * 0.45)],
              fill=WHITE, outline=INK)
    d.ellipse([x + s * 0.42, y + s * 0.30, x + s * 0.58, y + s * 0.46], fill=BLUE)
    d.polygon([(x + s * 0.32, y + s * 0.55), (x + s * 0.18, y + s * 0.78),
               (x + s * 0.32, y + s * 0.70)], fill=RED)
    d.polygon([(x + s * 0.68, y + s * 0.55), (x + s * 0.82, y + s * 0.78),
               (x + s * 0.68, y + s * 0.70)], fill=RED)
    d.polygon([(x + s * 0.42, y + s * 0.62), (x + s * 0.58, y + s * 0.62),
               (x + s * 0.50, y + s * 0.95)], fill=ORANGE)


def icon_tanker(d, x, y, s=30):
    d.rectangle([x + 1, y + s * 0.45, x + s - 1, y + s * 0.72], fill=INK)
    d.rectangle([x + s * 0.68, y + s * 0.28, x + s * 0.88, y + s * 0.45], fill=INK)
    d.line([x, y + s * 0.82, x + s, y + s * 0.82], fill=BLUE, width=3)
    d.polygon([(x + s * 0.30, y + s * 0.45), (x + s * 0.42, y + s * 0.12),
               (x + s * 0.54, y + s * 0.45)], fill=ORANGE)
    d.polygon([(x + s * 0.45, y + s * 0.45), (x + s * 0.55, y + s * 0.20),
               (x + s * 0.65, y + s * 0.45)], fill=RED)


def icon_refinery(d, x, y, s=30):
    d.rectangle([x + 2, y + s * 0.45, x + s * 0.42, y + s * 0.95], fill=INK)
    d.rectangle([x + s * 0.55, y + s * 0.60, x + s * 0.95, y + s * 0.95], fill=INK)
    d.polygon([(x + s * 0.10, y + s * 0.45), (x + s * 0.16, y + s * 0.10),
               (x + s * 0.22, y + s * 0.45)], fill=INK)
    d.polygon([(x + s * 0.28, y + s * 0.45), (x + s * 0.34, y + s * 0.18),
               (x + s * 0.40, y + s * 0.45)], fill=INK)
    d.polygon([(x + s * 0.60, y + s * 0.60), (x + s * 0.68, y + s * 0.35),
               (x + s * 0.76, y + s * 0.60)], fill=ORANGE)
    d.polygon([(x + s * 0.72, y + s * 0.60), (x + s * 0.80, y + s * 0.42),
               (x + s * 0.88, y + s * 0.60)], fill=RED)


def icon_drone(d, x, y, s=30):
    d.ellipse([x + s * 0.36, y + s * 0.40, x + s * 0.64, y + s * 0.60], fill=INK)
    for cx, cy in [(0.12, 0.22), (0.88, 0.22), (0.12, 0.78), (0.88, 0.78)]:
        px, py = x + s * cx, y + s * cy
        d.ellipse([px - 5, py - 5, px + 5, py + 5], outline=INK, width=2)
        d.line([x + s * 0.5, y + s * 0.5, px, py], fill=INK, width=2)
    d.ellipse([x + s * 0.44, y + s * 0.66, x + s * 0.56, y + s * 0.78], fill=RED)


def icon_parliament(d, x, y, s=30):
    d.polygon([(x + s * 0.08, y + s * 0.42), (x + s * 0.5, y + s * 0.08),
               (x + s * 0.92, y + s * 0.42)], fill=INK)
    d.rectangle([x + s * 0.08, y + s * 0.42, x + s * 0.92, y + s * 0.50], fill=INK)
    for cx in (0.20, 0.38, 0.62, 0.80):
        d.rectangle([x + s * cx - 2, y + s * 0.52, x + s * cx + 2,
                     y + s * 0.82], fill=INK)
    d.rectangle([x + s * 0.05, y + s * 0.82, x + s * 0.95, y + s * 0.92], fill=INK)
    d.rectangle([x + s * 0.44, y + s * 0.52, x + s * 0.56, y + s * 0.82],
                fill=WHITE)


def icon_chartdown(d, x, y, s=30):
    d.line([x + 2, y + s * 0.85, x + s - 2, y + s * 0.85], fill=INK, width=2)
    d.line([x + 2, y + s * 0.85, x + 2, y + s * 0.10], fill=INK, width=2)
    pts = [(x + 4, y + s * 0.25), (x + s * 0.32, y + s * 0.40),
           (x + s * 0.55, y + s * 0.32), (x + s * 0.78, y + s * 0.62),
           (x + s - 3, y + s * 0.78)]
    d.line(pts, fill=RED, width=3, joint="curve")
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.polygon([(x + s - 3, y + s * 0.78), (x + s - 10, y + s * 0.70),
               (x + s - 10, y + s * 0.82)], fill=RED)


def icon_handshake(d, x, y, s=30):
    d.polygon([(x + 2, y + s * 0.45), (x + s * 0.45, y + s * 0.45),
               (x + s * 0.55, y + s * 0.62), (x + s * 0.35, y + s * 0.80),
               (x + s * 0.15, y + s * 0.68)], fill=TEAL)
    d.polygon([(x + s - 2, y + s * 0.45), (x + s * 0.55, y + s * 0.45),
               (x + s * 0.65, y + s * 0.62), (x + s * 0.85, y + s * 0.68),
               (x + s * 0.65, y + s * 0.80)], fill=BLUE)
    d.line([x + s * 0.30, y + s * 0.55, x + s * 0.70, y + s * 0.55],
           fill=WHITE, width=2)


def icon_asteroid(d, x, y, s=30):
    d.polygon([(x + s * 0.15, y + s * 0.35), (x + s * 0.35, y + s * 0.12),
               (x + s * 0.70, y + s * 0.15), (x + s * 0.90, y + s * 0.40),
               (x + s * 0.80, y + s * 0.75), (x + s * 0.45, y + s * 0.92),
               (x + s * 0.15, y + s * 0.70)], fill=(100, 116, 139))
    d.ellipse([x + s * 0.30, y + s * 0.30, x + s * 0.48, y + s * 0.48],
              fill=(71, 85, 105))
    d.ellipse([x + s * 0.55, y + s * 0.55, x + s * 0.68, y + s * 0.68],
              fill=(71, 85, 105))
    for i in range(3):
        d.line([x + s * (0.55 + i * 0.12), y + s * 0.05,
                x + s * (0.65 + i * 0.12), y + s * 0.18], fill=YELLOW, width=2)


def icon_dollar(d, x, y, s=30):
    d.ellipse([x + 1, y + 1, x + s - 1, y + s - 1], fill=GREEN)
    d.text((x + s * 0.30, y + s * 0.10), "$", font=font(FB, 20), fill=WHITE)
    d.line([x + s * 0.05, y + s * 0.78, x + s * 0.95, y + s * 0.78],
           fill=GREEN, width=2)


def icon_chip(d, x, y, s=30):
    d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
                fill=INK)
    d.rectangle([x + s * 0.36, y + s * 0.36, x + s * 0.64, y + s * 0.64],
                fill=BLUE)
    for i in range(3):
        t = s * (0.32 + i * 0.18)
        d.line([x + t, y + s * 0.05, x + t, y + s * 0.22], fill=INK, width=2)
        d.line([x + t, y + s * 0.78, x + t, y + s * 0.95], fill=INK, width=2)
        d.line([x + s * 0.05, y + t, x + s * 0.22, y + t], fill=INK, width=2)
        d.line([x + s * 0.78, y + t, x + s * 0.95, y + t], fill=INK, width=2)


def icon_globe(d, x, y, s=30):
    d.ellipse([x + 1, y + 1, x + s - 1, y + s - 1], fill=(186, 230, 253),
              outline=BLUE, width=2)
    d.ellipse([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
              outline=BLUE, width=1)
    d.line([x + 1, y + s * 0.5, x + s - 1, y + s * 0.5], fill=BLUE, width=1)
    d.ellipse([x + s * 0.55, y + s * 0.55, x + s * 0.63, y + s * 0.63], fill=RED)
    d.ellipse([x + s * 0.45, y + s * 0.45, x + s * 0.73, y + s * 0.73],
              outline=RED, width=1)
    d.ellipse([x + s * 0.35, y + s * 0.35, x + s * 0.83, y + s * 0.83],
              outline=RED, width=1)


def icon_shield(d, x, y, s=30):
    d.polygon([(x + s * 0.5, y + 1), (x + s - 2, y + s * 0.22),
               (x + s - 2, y + s * 0.55), (x + s * 0.5, y + s - 1),
               (x + 2, y + s * 0.55), (x + 2, y + s * 0.22)],
              fill=GREEN)
    d.line([(x + s * 0.30, y + s * 0.50), (x + s * 0.45, y + s * 0.65),
            (x + s * 0.72, y + s * 0.35)], fill=WHITE, width=3, joint="curve")


ICONS = {
    "rocket": icon_rocket, "tanker": icon_tanker, "refinery": icon_refinery,
    "drone": icon_drone, "parliament": icon_parliament,
    "chartdown": icon_chartdown, "handshake": icon_handshake,
    "asteroid": icon_asteroid, "dollar": icon_dollar, "chip": icon_chip,
    "globe": icon_globe, "shield": icon_shield,
}

# Mini world map: simplified continent blobs in a (x, y, w, h) box.
# Coordinates are fractions of the box; dots are (lon_frac, lat_frac, region).
CONTINENTS = [
    [(0.02, 0.15), (0.10, 0.08), (0.20, 0.10), (0.24, 0.22), (0.18, 0.38),
     (0.12, 0.45), (0.06, 0.35), (0.02, 0.25)],            # N America
    [(0.22, 0.55), (0.28, 0.52), (0.31, 0.65), (0.27, 0.85), (0.23, 0.72)],  # S America
    [(0.46, 0.18), (0.52, 0.12), (0.56, 0.20), (0.52, 0.30), (0.46, 0.28)],  # Europe
    [(0.47, 0.38), (0.54, 0.34), (0.58, 0.45), (0.55, 0.62), (0.49, 0.58)],  # Africa
    [(0.58, 0.10), (0.75, 0.06), (0.90, 0.12), (0.95, 0.28), (0.85, 0.38),
     (0.72, 0.32), (0.62, 0.25)],                            # Asia
    [(0.82, 0.68), (0.90, 0.66), (0.92, 0.76), (0.84, 0.80)],  # Australia
]
MAP_DOTS = [
    (0.86, 0.22, 0),   # Jiuquan (Shenzhou)
    (0.60, 0.32, 1),   # Hormuz
    (0.52, 0.30, 1),   # Gaza
    (0.53, 0.18, 2),   # Odesa / Samara
    (0.49, 0.20, 2),   # Berlin
    (0.88, 0.72, 3),   # Canberra
    (0.92, 0.25, 3),   # Tokyo
    (0.09, 0.28, 4),   # Washington
    (0.24, 0.62, 4),   # Cartagena / Ecuador
    (0.52, 0.48, 5),   # Sudan
    (0.68, 0.92, 3),   # Balleny (Southern Ocean)
    (0.90, 0.35, 3),   # Manila
]
REGION_COLORS = [PURPLE, RED, BLUE, TEAL, ORANGE, GREEN]


def draw_bands(draw):
    """Six coloured region bands; one 15px line per story."""
    y = 146
    f_title = font(FB, 15)
    f_detail = font(FR, 15)
    f_mark = font(FB, 15)
    f_band = font(FB, 14)
    line_h = 18
    band_h = 21
    for ri, (name, color, _count) in enumerate(REGIONS):
        # band header: colour bar + name + story count
        draw.rectangle([0, y, W, y + band_h], fill=color)
        stories = [s for s in STORIES if s[1] == ri]
        draw.text((MARGIN, y + 3), name, font=f_band, fill=WHITE)
        cnt = "%d STORIES" % len(stories)
        cw = draw.textlength(cnt, font=f_band)
        draw.text((W - MARGIN - cw, y + 3), cnt, font=f_band, fill=WHITE)
        y += band_h
        for (num, _r, title, detail, mark) in stories:
            # number badge
            draw.rounded_rectangle([MARGIN, y + 1, MARGIN + 26, y + 16],
                                   radius=3, fill=color)
            nb = "%02d" % num
            nbw = draw.textlength(nb, font=font(FB, 11))
            draw.text((MARGIN + (26 - nbw) / 2, y + 3), nb,
                      font=font(FB, 11), fill=WHITE)
            tx = MARGIN + 32
            # how-sure mark at the far right
            mw = draw.textlength(mark, font=f_mark)
            mx = W - MARGIN - mw
            mcolor = GREEN if mark == "✓" else (AMBER if mark == "◐"
                                                 else (RED if mark == "?" else PURPLE))
            draw.text((mx, y), mark, font=f_mark, fill=mcolor)
            # title (bold) + detail (regular), truncated to fit
            tpart = title + " — "
            tw = draw.textlength(tpart, font=f_title)
            avail = mx - 8 - (tx + tw)
            dpart = fit_text(draw, detail, f_detail, avail)
            draw.text((tx, y), tpart, font=f_title, fill=INK)
            draw.text((tx + tw, y), dpart, font=f_detail, fill=INK)
            y += line_h
        draw.line([0, y, W, y], fill=LINE, width=1)
    return y


def draw_map_scenes(draw, y0):
    """Mini world map (left) + 12 pictogram scenes (right)."""
    y1 = y0 + 56
    draw.rectangle([0, y0, W, y1], fill=WHITE)
    draw.text((MARGIN, y0 + 3), "WORLD MAP", font=font(FB, 11), fill=MUTED)
    mx, my, mw, mh = MARGIN, y0 + 16, 300, 36
    for poly in CONTINENTS:
        pts = [(mx + fx * mw, my + fy * mh) for fx, fy in poly]
        draw.polygon(pts, fill=(203, 213, 225), outline=(100, 116, 139))
    for fx, fy, ri in MAP_DOTS:
        px, py = mx + fx * mw, my + fy * mh
        draw.ellipse([px - 3, py - 3, px + 3, py + 3],
                     fill=REGION_COLORS[ri], outline=WHITE, width=1)
    sx = 340
    draw.text((sx, y0 + 3), "12 SCENES  —  numbers match the stories",
              font=font(FB, 11), fill=MUTED)
    cell = (W - MARGIN - sx) / 12.0
    for i, (num, kind) in enumerate(SCENES):
        cx = sx + i * cell
        ICONS[kind](draw, cx + (cell - 26) / 2, y0 + 16, 26)
        lab = "%02d" % num
        lw = draw.textlength(lab, font=font(FB, 9))
        draw.text((cx + (cell - lw) / 2, y0 + 44), lab,
                  font=font(FB, 9), fill=MUTED)
    return y1


def draw_footer(draw, y0):
    draw.rectangle([0, y0, W, H], fill=NAVY)
    f1 = font(FB, 13)
    f2 = font(FR, 12)
    draw.text((MARGIN, y0 + 5),
              "DATE CHECK:  Every story happened or was first reported 25 Nov 2026.",
              font=f1, fill=WHITE)
    draw.text((MARGIN, y0 + 23),
              "Not in this picture: Huawei verdict, Riyadh tower strike, COP31 collapse, "
              "Nvidia CEO return (all 24 Nov or earlier).",
              font=f2, fill=(203, 213, 225))


def render():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_timeline(draw)
    y = draw_bands(draw)
    y = draw_map_scenes(draw, y)
    draw_footer(draw, y)
    return img


if __name__ == "__main__":
    out = os.environ.get("RENDER_OUTPUT") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, format="PNG")
    print("wrote", out)
