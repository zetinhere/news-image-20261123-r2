#!/usr/bin/env python3
"""Draw one image summing up the world's news of Monday 23 November 2026.

Layout (1024x1024, my own design): a deep-navy poster with a gold masthead,
one lead story (COP31 collapse) with a drawn globe, a 2x3 grid of story cards
each with a small drawn icon, and a bottom ticker of shorter items.
Deterministic: no network, no randomness, no timestamps.
Run: python3 draw.py  ->  entry.png
"""
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (11, 29, 51)
CARD = (20, 48, 79)
CARD_EDGE = (52, 96, 140)
GOLD = (217, 164, 65)
PAPER = (245, 239, 224)
MUTED = (178, 196, 216)
RED = (198, 64, 46)
TEAL = (64, 178, 164)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def globe(d, cx, cy, r):
    """Stylised globe: circle, meridians, and a crack across the top."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(23, 58, 92))
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=GOLD, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=GOLD, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340,
          fill=TEAL, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 20, 160,
          fill=TEAL, width=3)
    # crack: jagged gold-red line across the upper globe
    pts = [(cx - r * 0.7, cy - r * 0.55), (cx - r * 0.3, cy - r * 0.75),
           (cx, cy - r * 0.45), (cx + r * 0.35, cy - r * 0.7),
           (cx + r * 0.7, cy - r * 0.5)]
    d.line(pts, fill=RED, width=4, joint="curve")


def flame(d, x, y, s, color=RED):
    """Simple flame: two stacked teardrops."""
    d.polygon([(x, y - s), (x + s * 0.55, y - s * 0.1), (x + s * 0.3, y + s * 0.55),
               (x - s * 0.3, y + s * 0.55), (x - s * 0.55, y - s * 0.1)],
              fill=color)
    d.polygon([(x, y - s * 0.1), (x + s * 0.28, y + s * 0.2),
               (x, y + s * 0.55), (x - s * 0.28, y + s * 0.2)],
              fill=GOLD)


def tanker(d, x, y, s):
    """Small oil tanker on waves."""
    d.rectangle([x - s, y - s * 0.25, x + s, y + s * 0.25], fill=PAPER)
    d.rectangle([x - s * 0.55, y - s * 0.7, x - s * 0.1, y - s * 0.25],
                fill=RED)
    d.rectangle([x + s * 0.35, y - s * 0.55, x + s * 0.6, y - s * 0.25],
                fill=GOLD)
    for k in range(3):
        d.arc([x - s + k * s * 0.7, y + s * 0.45, x - s * 0.3 + k * s * 0.7,
               y + s * 0.8], 0, 180, fill=TEAL, width=3)


def building(d, x, y, s):
    """Apartment block with a blast star at its corner."""
    d.rectangle([x - s * 0.7, y - s * 0.8, x + s * 0.7, y + s * 0.8],
                fill=PAPER)
    for r in range(3):
        for c in range(3):
            d.rectangle([x - s * 0.5 + c * s * 0.35, y - s * 0.6 + r * s * 0.5,
                         x - s * 0.25 + c * s * 0.35, y - s * 0.35 + r * s * 0.5],
                        fill=NAVY)
    cx, cy = x + s * 0.7, y - s * 0.8
    for a in range(8):
        ang = a * math.pi / 4
        r = s * 0.55 if a % 2 == 0 else s * 0.3
        d.line([cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang)],
               fill=RED, width=4)


def cuffs(d, x, y, s):
    """Two linked handcuff rings."""
    d.ellipse([x - s * 0.85, y - s * 0.45, x - s * 0.05, y + s * 0.35],
              outline=GOLD, width=5)
    d.ellipse([x + s * 0.05, y - s * 0.45, x + s * 0.85, y + s * 0.35],
              outline=GOLD, width=5)
    d.line([x - s * 0.05, y, x + s * 0.05, y], fill=GOLD, width=5)
    d.line([x - s * 0.45, y - s * 0.05, x - s * 0.15, y + s * 0.15],
           fill=GOLD, width=3)


def scales(d, x, y, s):
    """Scales of justice."""
    d.line([x, y - s * 0.8, x, y + s * 0.7], fill=GOLD, width=4)
    d.line([x - s * 0.7, y - s * 0.8, x + s * 0.7, y - s * 0.8],
           fill=GOLD, width=4)
    d.polygon([(x - s * 0.85, y - s * 0.1), (x - s * 0.45, y - s * 0.1),
               (x - s * 0.65, y + s * 0.35)], outline=GOLD, width=3)
    d.polygon([(x + s * 0.45, y - s * 0.1), (x + s * 0.85, y - s * 0.1),
               (x + s * 0.65, y + s * 0.35)], outline=GOLD, width=3)
    d.line([x - s * 0.7, y - s * 0.8, x - s * 0.65, y - s * 0.1],
           fill=GOLD, width=2)
    d.line([x + s * 0.7, y - s * 0.8, x + s * 0.65, y - s * 0.1],
           fill=GOLD, width=2)
    d.rectangle([x - s * 0.45, y + s * 0.7, x + s * 0.45, y + s * 0.8],
                fill=GOLD)


def capitol(d, x, y, s):
    """Capitol dome on a plinth."""
    d.arc([x - s * 0.5, y - s * 0.8, x + s * 0.5, y + s * 0.1], 180, 360,
          fill=PAPER, width=4)
    d.rectangle([x - s * 0.55, y - s * 0.05, x + s * 0.55, y + s * 0.15],
                fill=PAPER)
    for c in range(3):
        d.rectangle([x - s * 0.45 + c * s * 0.35, y + s * 0.15,
                     x - s * 0.25 + c * s * 0.35, y + s * 0.6], fill=PAPER)
    d.rectangle([x - s * 0.7, y + s * 0.6, x + s * 0.7, y + s * 0.75],
                fill=GOLD)


ICONS = {"flame": flame, "tanker": tanker, "building": building,
         "cuffs": cuffs, "scales": scales, "capitol": capitol}


def card(d, x, y, w, h, tag, headline, body, icon):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=CARD_EDGE, width=2)
    # top row: small icon at left, section tag beside it
    ICONS[icon](d, x + 30, y + 30, 22)
    tf = font(SANS_B, 17)
    d.text((x + 62, y + 16), tag, font=tf, fill=GOLD)
    # headline below the tag row, full card width
    hf = font(SANS_B, 24)
    lines = wrap(d, headline, hf, w - 28)
    ly = y + 50
    for ln in lines[:2]:
        d.text((x + 14, ly), ln, font=hf, fill=PAPER)
        ly += 29
    # body below the headline, at most two lines
    bf = font(SANS, 18)
    blines = wrap(d, body, bf, w - 28)
    by = y + 50 + len(lines[:2]) * 29 + 6
    for ln in blines[:2]:
        d.text((x + 14, by), ln, font=bf, fill=MUTED)
        by += 23


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.text((W // 2, 30), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=GOLD, anchor="ma")
    d.text((W // 2, 62), "THE WORLD IN ONE DAY", font=font(SERIF, 58),
           fill=PAPER, anchor="ma")
    d.line([60, 140, W - 60, 140], fill=GOLD, width=3)
    d.text((W // 2, 150), "The day's most consequential news, from every region",
           font=font(SANS, 21), fill=MUTED, anchor="ma")

    # --- lead story: COP31 ---
    ly = 196
    d.rounded_rectangle([36, ly, W - 36, ly + 148], radius=12, fill=(24, 58, 92),
                        outline=GOLD, width=2)
    globe(d, 118, ly + 74, 56)
    d.text((196, ly + 14), "CLIMATE  •  ANTALYA, TURKEY",
           font=font(SANS_B, 18), fill=GOLD)
    d.text((196, ly + 38), "COP31 COLLAPSES — NO DEAL",
           font=font(SERIF, 40), fill=PAPER)
    lead = ("After a record two weeks of talks, nearly 200 nations reject the "
            "final pact: it never mentions fossil fuels.")
    bf = font(SANS, 21)
    by = ly + 92
    for ln in wrap(d, lead, bf, W - 36 - 196 - 24):
        d.text((196, by), ln, font=bf, fill=MUTED)
        by += 26

    # --- story grid ---
    stories = [
        ("GULF ON EDGE", "Iran strikes Bahrain; tankers hit near Hormuz",
         "Tehran's Guards say they hit US bases; two tankers struck off Oman.",
         "tanker"),
        ("UKRAINE", "Drone destroys flats in Dymer; 14 missing",
         "A Russian drone hits a five-storey block near Kyiv as rescuers "
         "search the rubble.", "building"),
        ("MEXICO", "\u2018El Chapo Isidro\u2019 captured in Sinaloa raid",
         "Troops seize FBI most-wanted cartel boss Fausto Isidro Meza "
         "Flores; 11 die in the raid.", "cuffs"),
        ("THE HAGUE", "Myanmar guilty of genocide, World Court rules",
         "Judges find the 2017 campaign against the Rohingya was genocide.",
         "scales"),
        ("INDONESIA", "Factory fire kills 3; 36 workers missing",
         "A candy factory burns in Cikande, Banten; dozens still missing.",
         "flame"),
        ("WASHINGTON", "Democrats take largest House majority since 1992",
         "The party wins 258+ seats in the House, its biggest majority "
         "in more than three decades.", "capitol"),
    ]
    gx, gy = 36, 372
    cw, ch, gap = 464, 178, 24
    for i, (tag, head, body, icon) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        card(d, x, y, cw, ch, tag, head, body, icon)

    # --- bottom ticker ---
    ty = 962
    d.line([36, ty, W - 36, ty], fill=GOLD, width=2)
    tick = ("ALSO:  Verstappen wins Las Vegas GP  •  Seoul minister quits in AI "
            "exam scandal  •  Lethal-AI arms talks open")
    d.text((W // 2, ty + 12), tick, font=font(SANS, 18), fill=MUTED,
           anchor="ma")
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
    print("entry.png written")
