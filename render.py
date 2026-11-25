#!/usr/bin/env python3
"""Render THE GLOBAL BRIEF — 25 November 2026 (news-image-20261125 v2).

Draws a 1024x1024 editorial briefing board from the verified 25 Nov 2026
stories in research-25nov-strict.md. Pure PIL, no network, deterministic.
Only figures present in the strict research file are shown; unverified
numbers from the v1 design brief ("3rd Tiangong trip", housing/electricity/
fuel micro-labels, "Ocean freight +120.4%") are deliberately left out.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
GUTTER = 12

# palette
BG = (244, 247, 251)
INK = (17, 24, 39)
MUTED = (71, 85, 105)
FAINT = (100, 116, 139)
LINE = (215, 223, 234)
NAVY = (15, 23, 42)
NAVY_SOFT = (30, 41, 59)
WHITE = (255, 255, 255)
CREAM = (255, 251, 235)
BLUE = (37, 99, 235)
RED = (220, 38, 38)
RED_SOFT = (254, 226, 226)
AMBER = (245, 158, 11)
AMBER_DARK = (180, 83, 9)
PURPLE = (124, 58, 237)
PURPLE_SOFT = (237, 233, 254)
TEAL = (15, 118, 110)
TEAL_SOFT = (204, 251, 241)
ORANGE = (234, 88, 12)
GREEN = (22, 163, 74)
GREEN_SOFT = (220, 252, 231)
GRAY = (148, 163, 184)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    """Draw wrapped text; return y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def panel(draw, box, fill, accent):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=LINE, width=2)
    draw.rectangle([x0 + 3, y0, x1 - 3, y0 + 7], fill=accent)


def pill(draw, x, y, text, fnt, fg, bg):
    w = int(draw.textlength(text, font=fnt)) + 24
    h = fnt.size + 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + 12, y + 7), text, font=fnt, fill=fg)
    return w


def header(draw):
    draw.rectangle([0, 0, W, 132], fill=NAVY)
    draw.text((MARGIN, 28), "THE GLOBAL BRIEF", font=font(FB, 46), fill=WHITE)
    pill_text = "WEDNESDAY  \u2022  25 NOVEMBER 2026"
    pf = font(FB, 21)
    pw = int(draw.textlength(pill_text, font=pf)) + 36
    px = W - MARGIN - pw
    draw.rounded_rectangle([px, 36, W - MARGIN, 36 + 42], radius=21, fill=WHITE)
    draw.text((px + 18, 46), pill_text, font=pf, fill=NAVY)
    draw.text((MARGIN, 94), "7 WORLD STORIES  \u2022  ALL FROM 25 NOV 2026",
              font=font(FB, 21), fill=(148, 163, 184))


def footer(draw):
    draw.rectangle([0, 956, W, H], fill=NAVY)
    draw.text((MARGIN, 974), "ALL STORIES ARE FROM 25 NOV 2026",
              font=font(FB, 17), fill=WHITE)
    right = "SCHEDULED MARKED  \u2022  SINGLE-SOURCE FLAGGED"
    rf = font(FB, 15)
    rw = draw.textlength(right, font=rf)
    draw.text((W - MARGIN - rw, 976), right, font=rf, fill=(148, 163, 184))


# ---- row 1: heroes (y 144..452) -------------------------------------------

def panel_shenzhou(draw):
    box = (MARGIN, 144, 584, 452)
    panel(draw, box, NAVY, BLUE)
    x, y = 44, 162
    draw.text((x, y), "SHENZHOU-24 LAUNCH", font=font(FB, 27), fill=WHITE)
    draw.text((x, 200), "07:18 WIB", font=font(FB, 40), fill=(251, 191, 36))
    draw.text((x, 248), "1st foreign astronaut", font=font(FB, 22), fill=WHITE)
    text_block(draw, x, 282,
               "China launched Shenzhou-24 today, sending Pakistan's "
               "Muhammad Zeeshan Ali as the first foreign astronaut to "
               "visit Tiangong.", font(FR, 21), (226, 232, 240), 512, leading=27)
    # visual band: orbit arc, upright rocket, station silhouette
    draw.arc([60, 380, 560, 470], start=200, end=340, fill=(100, 116, 139), width=3)
    # rocket body (upright)
    draw.rectangle([320, 380, 344, 424], fill=WHITE)
    draw.polygon([(320, 380), (344, 380), (332, 362)], fill=(251, 191, 36))
    draw.ellipse([326, 392, 338, 404], fill=BLUE)
    draw.polygon([(320, 424), (308, 440), (320, 432)], fill=(251, 191, 36))
    draw.polygon([(344, 424), (356, 440), (344, 432)], fill=(251, 191, 36))
    # flame
    draw.polygon([(324, 424), (340, 424), (332, 446)], fill=(249, 115, 22))
    # station silhouette: small modules
    draw.rectangle([452, 396, 540, 408], fill=(100, 116, 139))
    draw.rectangle([488, 384, 506, 420], fill=(148, 163, 184))
    draw.rectangle([452, 400, 470, 404], fill=(148, 163, 184))
    draw.text((60, 428), "Jiuquan", font=font(FB, 18), fill=(148, 163, 184))
    draw.text((420, 428), "Pakistan aboard", font=font(FB, 16), fill=(251, 191, 36))


def panel_stocks(draw):
    box = (596, 144, 1000, 452)
    panel(draw, box, CREAM, RED)
    x = 616
    draw.text((x, 162), "ASIA STOCKS SLIDE", font=font(FB, 26), fill=RED)
    rows = [("KOSPI", "\u22125.3%"), ("Taiwan", "\u22125.1%"), ("Nikkei", "\u22122.9%")]
    yy = 202
    for name, val in rows:
        draw.text((x, yy), name, font=font(FB, 24), fill=INK)
        vw = draw.textlength(val, font=font(FB, 24))
        draw.text((980 - vw, yy), val, font=font(FB, 24), fill=RED)
        yy += 34
    text_block(draw, x, 306,
               "Asian markets tumbled in early Wednesday trading.",
               font(FR, 19), MUTED, 364, leading=25)
    # falling line chart
    pts = [(620, 366), (680, 374), (740, 362), (800, 386), (860, 398), (920, 382),
           (976, 406)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    draw.polygon([(976, 406), (962, 394), (962, 406)], fill=RED)
    draw.text((x, 420), "MSCI Asia ex-Japan \u22122.3%", font=font(FB, 16), fill=RED)


# ---- row 2: support panels (y 464..716) ------------------------------------

def panel_australia(draw):
    box = (MARGIN, 464, 341, 716)
    panel(draw, box, WHITE, AMBER)
    x = 44
    draw.text((x, 482), "AUSTRALIA CPI 4.9%", font=font(FB, 22), fill=AMBER_DARK)
    draw.text((x, 514), "4.9%", font=font(FB, 54), fill=INK)
    # small Australia silhouette (simplified polygon) right of the number
    draw.polygon([(218, 528), (262, 520), (306, 534), (312, 556), (296, 574),
                  (268, 580), (240, 570), (220, 552)], fill=(253, 230, 138),
                 outline=AMBER)
    draw.text((x, 580), "Core 3.8%", font=font(FB, 21), fill=INK)
    text_block(draw, x, 612,
               "Australia's annual inflation rose to 4.9% in October; "
               "trimmed mean 3.8%.",
               font(FR, 18), MUTED, 277, leading=24)
    # house + lightning icons
    draw.polygon([(52, 700), (72, 684), (92, 700)], fill=AMBER)
    draw.rectangle([58, 700, 86, 714], fill=AMBER)
    draw.polygon([(116, 682), (104, 702), (114, 702), (106, 714), (126, 696),
                  (116, 696)], fill=AMBER)


def panel_japan(draw):
    box = (353, 464, 670, 716)
    panel(draw, box, WHITE, AMBER)
    x = 373
    draw.text((x, 482), "JAPAN SERVICES 4.2%", font=font(FB, 22), fill=AMBER_DARK)
    draw.text((x, 512), "4.2%", font=font(FB, 48), fill=INK)
    draw.text((x + 158, 528), "% y/y", font=font(FB, 22), fill=INK)
    draw.text((x, 576), "Fastest since 1990", font=font(FB, 20), fill=RED)
    text_block(draw, x, 610,
               "Service-sector prices rose 4.2% year on year in October, "
               "up from 3.8% in September.", font(FR, 18), MUTED, 277, leading=24)
    draw.text((x, 686), "Rate-hike expectations reinforced.",
              font=font(FB, 15), fill=MUTED)


def panel_hera(draw):
    box = (682, 464, 1000, 716)
    panel(draw, box, (250, 245, 255), PURPLE)
    x = 702
    draw.text((x, 482), "HERA TONIGHT", font=font(FB, 22), fill=PURPLE)
    draw.text((x, 514), "19:45 CET", font=font(FB, 32), fill=INK)
    draw.text((x, 552), "01:45 WIB", font=font(FB, 22), fill=MUTED)
    pill(draw, x, 576, "TONIGHT", font(FB, 17), WHITE, PURPLE)
    text_block(draw, x, 614,
               "ESA is set to reveal Hera's first close-up images of "
               "Dimorphos tonight.", font(FR, 18), MUTED, 278, leading=24)
    # asteroid + eclipse shadow (top-right corner)
    draw.ellipse([896, 500, 976, 580], fill=(100, 116, 139))
    draw.ellipse([920, 516, 952, 548], fill=(71, 85, 105))
    draw.ellipse([872, 556, 900, 584], fill=(148, 163, 184))
    draw.text((x, 692), "Scheduled reveal \u2022 Not released yet",
              font=font(FB, 13), fill=PURPLE)


# ---- row 3: wide panels (y 728..944) ----------------------------------------

def panel_balleney(draw):
    box = (MARGIN, 728, 506, 944)
    panel(draw, box, WHITE, TEAL)
    x = 44
    draw.text((x, 746), "BALLENY M5.9", font=font(FB, 23), fill=TEAL)
    draw.text((x, 778), "M5.9", font=font(FB, 42), fill=INK)
    draw.text((x + 128, 788), "08:38 WIB", font=font(FB, 22), fill=INK)
    draw.text((x + 128, 818), "Depth 10 km", font=font(FB, 20), fill=MUTED)
    text_block(draw, x, 844,
               "A shallow M5.9 quake struck the remote Balleny Islands "
               "region in the Southern Ocean.",
               font(FR, 18), MUTED, 300, leading=24)
    # south-pole globe slice with epicentre rings (right side)
    cx, cy = 420, 844
    draw.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=(240, 253, 250),
                 outline=TEAL, width=3)
    draw.arc([cx - 62, cy - 62, cx + 62, cy + 62], start=180, end=360,
             fill=TEAL, width=3)
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=TEAL, width=2)
    draw.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=TEAL, width=2)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    pill(draw, 352, 914, "USGS green alert", font(FB, 15), GREEN, GREEN_SOFT)
    draw.text((x, 916), "Remote ocean \u2022 Low impact", font=font(FB, 15), fill=MUTED)


def panel_antique(draw):
    box = (518, 728, 1000, 944)
    panel(draw, box, WHITE, ORANGE)
    x = 538
    draw.text((x, 746), "ANTIQUE M5.1", font=font(FB, 23), fill=ORANGE)
    draw.text((x, 778), "M5.1", font=font(FB, 42), fill=INK)
    draw.text((x + 128, 788), "07:29 PST", font=font(FB, 22), fill=INK)
    draw.text((x + 128, 818), "Intensity V", font=font(FB, 20), fill=MUTED)
    text_block(draw, x, 844,
               "A M5.1 quake hit Antique in the Philippines; PHIVOLCS "
               "reports Intensity V in Valderrama.",
               font(FR, 18), MUTED, 300, leading=24)
    # Philippines archipelago dots + quake rings (right side)
    cx, cy = 914, 844
    for dx, dy, r in [(0, -52, 7), (6, -30, 9), (-4, -8, 11), (4, 16, 9),
                      (-6, 38, 7), (2, 56, 5)]:
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=(254, 215, 170), outline=ORANGE)
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=RED, width=3)
    draw.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], outline=RED, width=2)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    # warning triangle
    draw.polygon([(556, 936), (570, 912), (584, 936)], fill=ORANGE)
    draw.text((565, 920), "!", font=font(FB, 16), fill=WHITE)
    pill(draw, 592, 910, "PHIVOLCS ONLY", font(FB, 15), WHITE, ORANGE)
    draw.text((752, 918), "Single official source", font=font(FB, 15), fill=MUTED)


def render():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    header(draw)
    panel_shenzhou(draw)
    panel_stocks(draw)
    panel_australia(draw)
    panel_japan(draw)
    panel_hera(draw)
    panel_balleney(draw)
    panel_antique(draw)
    footer(draw)
    return img


if __name__ == "__main__":
    out = os.environ.get("RENDER_OUTPUT") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, format="PNG")
    print("wrote", out)
