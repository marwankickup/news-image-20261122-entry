#!/usr/bin/env python3
"""Draw entry.png: "The World on Sunday" - a front-page poster summing up
the world news of Sunday 22 November 2026.

Run with the project venv:  ~/workspace/makefun/.venv/bin/python draw_image.py
Writes entry.png (1024x1024) next to this file. The grader never runs this
script; main.ts copies the finished entry.png to /output/entry.png.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor; the page is drawn at 2048 and shrunk to 1024
W = 1024

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

INK = (26, 26, 30)
PAPER = (248, 245, 238)
PANEL = (255, 255, 255)
RULE = (26, 26, 30)
RED = (168, 32, 40)
NAVY = (31, 58, 95)
GOLD = (198, 152, 40)
SLATE = (52, 60, 72)
GREY = (96, 96, 100)
STEEL = (46, 110, 160)
ORANGE = (232, 110, 30)


def F(path, size):
    return ImageFont.truetype(path, size * S)


def text_w(d, s, font):
    return d.textlength(s, font=font)


def wrap(d, s, font, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(d, t, font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def centered(d, cx, y, s, font, fill, tracking=0):
    """Draw one line centered at cx; returns its height."""
    if tracking:
        total = sum(text_w(d, ch, font) for ch in s) + tracking * S * (len(s) - 1)
        x = cx - total / 2
        for ch in s:
            d.text((x, y), ch, font=font, fill=fill)
            x += text_w(d, ch, font) + tracking * S
        return font.size
    w_ = text_w(d, s, font)
    d.text((cx - w_ / 2, y), s, font=font, fill=fill)
    return font.size


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- pictograms
# Each icon draws itself around (cx, cy) on its own transparent layer of
# 240x150 design units; render_icon() scales it into the panel.
def icon_globe_doc(d, cx, cy):
    """Globe behind a rejected document: climate talks end with no deal."""
    gx, gy, r = cx - 22, cy + 2, 47
    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=STEEL)
    d.ellipse([gx - r, gy - r, gx + r, gy + r], outline=(255, 255, 255), width=3 * S)
    d.ellipse([gx - 18, gy - r, gx + 18, gy + r], outline=(255, 255, 255), width=3 * S)
    d.line([gx - r, gy, gx + r, gy], fill=(255, 255, 255), width=3 * S)
    d.line([gx - r + 12, gy - 27, gx + r - 12, gy - 27], fill=(255, 255, 255),
           width=2 * S)
    d.line([gx - r + 12, gy + 27, gx + r - 12, gy + 27], fill=(255, 255, 255),
           width=2 * S)
    # the draft deal, held up at the front right, crossed out in red
    x0, y0, x1, y1 = cx + 12, cy - 30, cx + 66, cy + 36
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=3 * S)
    for i in range(3):
        ly = y0 + 12 + i * 11
        d.line([x0 + 8, ly, x1 - 8, ly], fill=(170, 170, 178), width=3 * S)
    d.line([x0 + 7, y0 + 40, x1 - 7, y1 - 6], fill=RED, width=5 * S)
    d.line([x0 + 7, y1 - 6, x1 - 7, y0 + 40], fill=RED, width=5 * S)


def icon_ruin(d, cx, cy):
    """An apartment block with one section collapsed; a drone overhead."""
    base = cy + 58
    # standing left section with lit windows
    d.rectangle([cx - 90, cy - 28, cx - 18, base], fill=SLATE)
    for r_ in range(4):
        for c_ in range(2):
            wx = cx - 80 + c_ * 26
            wy = cy - 18 + r_ * 19
            d.rectangle([wx, wy, wx + 13, wy + 10], fill=(240, 205, 110))
    # collapsed right section: a slab leaning down into rubble
    d.polygon([(cx - 18, cy - 28), (cx + 58, cy + 16), (cx + 58, base),
               (cx - 18, base)], fill=(104, 108, 118))
    d.line([cx - 18, cy - 28, cx + 58, cy + 16], fill=INK, width=3 * S)
    for dx, rr in [(30, 12), (56, 9), (6, 7)]:
        d.polygon([(cx + dx - rr, base), (cx + dx, base - rr), (cx + dx + rr, base)],
                  fill=(84, 88, 98))
    d.rectangle([cx - 96, base, cx + 96, base + 5], fill=INK)
    # quadcopter drone above the standing section: a solid body on four
    # arms, each arm ending in a flat rotor disc, camera slung underneath
    dx, dy = cx - 52, cy - 54
    for sx, sy in [(-22, -10), (22, -10), (-22, 10), (22, 10)]:
        d.line([dx, dy, dx + sx, dy + sy], fill=INK, width=3 * S)
        d.ellipse([dx + sx - 10, dy + sy - 4, dx + sx + 10, dy + sy + 4],
                  fill=INK)
    d.rounded_rectangle([dx - 13, dy - 6, dx + 13, dy + 6], radius=5 * S, fill=INK)
    d.ellipse([dx - 3, dy + 6, dx + 3, dy + 11], fill=RED)


def icon_ship(d, cx, cy):
    """A warship capsizing on waves as a sea drone closes in."""
    # waves first, hull over them
    for wy, amp in [(cy + 44, 8), (cy + 56, 6)]:
        pts = []
        for i in range(25):
            x = cx - 104 + i * 9
            pts.append((x, wy + amp * math.sin(i * 1.1 + wy)))
        d.line(pts, fill=STEEL, width=3 * S, joint="curve")
    # hull, bow high at the left, stern dipping to the right
    d.polygon([(cx - 88, cy + 2), (cx + 84, cy + 20), (cx + 66, cy + 40),
               (cx - 66, cy + 26)], fill=SLATE)
    d.rectangle([cx - 30, cy - 8, cx + 16, cy + 12], fill=(70, 78, 92))
    d.line([cx + 2, cy - 8, cx + 2, cy - 30], fill=INK, width=3 * S)
    d.polygon([(cx + 2, cy - 30), (cx + 20, cy - 24), (cx + 2, cy - 18)], fill=RED)
    # burst where the stern meets the water
    bx, by = cx + 74, cy + 30
    for i in range(8):
        ang = i * math.pi / 4 + 0.2
        d.line([bx, by, bx + 15 * math.cos(ang), by + 15 * math.sin(ang)],
               fill=ORANGE, width=3 * S)
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=GOLD)
    # sea drone skimming in from the left, wake behind it; drawn long and
    # high enough to stay visible against the wave lines
    sx, sy = cx - 102, cy + 28
    d.polygon([(sx, sy), (sx + 34, sy - 5), (sx + 38, sy + 4), (sx + 4, sy + 7)],
              fill=INK)
    d.rectangle([sx + 14, sy - 10, sx + 20, sy - 4], fill=INK)
    d.line([sx - 14, sy + 7, sx, sy + 4], fill=(255, 255, 255), width=2 * S)
    d.line([sx - 22, sy + 10, sx - 2, sy + 8], fill=(255, 255, 255), width=2 * S)



def icon_factory(d, cx, cy):
    """A factory with flames over the roof and smoke from its chimneys."""
    base = cy + 58
    # smoke puffs from the right-hand chimney
    for dx, dy, rr in [(66, -52, 10), (78, -62, 13), (94, -68, 9)]:
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=(168, 168, 175))
    # chimneys
    d.rectangle([cx + 44, cy - 34, cx + 58, base], fill=SLATE)
    d.rectangle([cx + 64, cy - 42, cx + 78, base], fill=SLATE)
    # main hall with a sawtooth roof
    d.rectangle([cx - 92, cy + 4, cx + 44, base], fill=(70, 78, 92))
    for i in range(3):
        x0 = cx - 92 + i * 45
        d.polygon([(x0, cy + 4), (x0 + 22, cy - 18), (x0 + 45, cy + 4)],
                  fill=(70, 78, 92))
    for i in range(4):  # windows
        wx = cx - 80 + i * 30
        d.rectangle([wx, cy + 22, wx + 16, cy + 38], fill=(240, 205, 110))
    # flames licking up from behind the roofline
    for fx, fh, col in [(-70, 34, RED), (-46, 46, ORANGE), (-22, 32, GOLD),
                        (2, 40, ORANGE)]:
        d.polygon([(cx + fx - 10, cy - 12), (cx + fx, cy - 12 - fh),
                   (cx + fx + 10, cy - 12)], fill=col)
    d.rectangle([cx - 98, base, cx + 98, base + 5], fill=INK)


def icon_capitol(d, cx, cy):
    """The US Capitol dome over a row of columns."""
    # dome and its lantern
    d.pieslice([cx - 50, cy - 46, cx + 50, cy + 30], 180, 360, fill=NAVY)
    d.line([cx, cy - 46, cx, cy - 58], fill=NAVY, width=4 * S)
    d.ellipse([cx - 5, cy - 64, cx + 5, cy - 54], fill=GOLD)
    d.rectangle([cx - 62, cy + 6, cx + 62, cy + 16], fill=NAVY)
    # columns
    for i in range(5):
        x = cx - 52 + i * 26
        d.rectangle([x, cy + 20, x + 10, cy + 48], fill=SLATE)
    # steps
    d.rectangle([cx - 68, cy + 48, cx + 68, cy + 55], fill=NAVY)
    d.rectangle([cx - 78, cy + 55, cx + 78, cy + 62], fill=NAVY)


def icon_trophy(d, cx, cy):
    """A champion's cup with a star, and a small chequered flag."""
    # chequered flag on a pole behind the cup, to the right
    px = cx + 52
    d.line([px, cy - 56, px, cy + 40], fill=INK, width=3 * S)
    sq = 11
    for r_ in range(3):
        for c_ in range(3):
            col = INK if (r_ + c_) % 2 == 0 else (255, 255, 255)
            d.rectangle([px + 2 + c_ * sq, cy - 56 + r_ * sq,
                         px + 2 + (c_ + 1) * sq, cy - 56 + (r_ + 1) * sq],
                        fill=col, outline=(200, 200, 205), width=S)
    # handles
    d.arc([cx - 58, cy - 40, cx - 16, cy + 2], 90, 270, fill=GOLD, width=6 * S)
    d.arc([cx + 16, cy - 40, cx + 58, cy + 2], 270, 90, fill=GOLD, width=6 * S)
    # bowl, stem and base
    d.polygon([(cx - 36, cy - 46), (cx + 36, cy - 46), (cx + 15, cy + 4),
               (cx - 15, cy + 4)], fill=GOLD)
    d.rectangle([cx - 36, cy - 50, cx + 36, cy - 44], fill=(170, 128, 30))
    star(d, cx, cy - 22, 13, (255, 255, 255))
    d.rectangle([cx - 6, cy + 4, cx + 6, cy + 20], fill=(170, 128, 30))
    d.rectangle([cx - 24, cy + 20, cx + 24, cy + 30], fill=(170, 128, 30))


def render_icon(img, icon, ccx, cy, max_w=205, max_h=86):
    """Draw an icon on its own layer, trim its transparent margins, and
    paste it scaled to fit a max_w x max_h box, centered at (ccx, cy)."""
    layer = Image.new("RGBA", (240 * S, 150 * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    icon(ld, 120 * S, 75 * S)
    bbox = layer.getbbox()
    if bbox:
        layer = layer.crop(bbox)
    scale = min(max_w * S / layer.width, max_h * S / layer.height)
    layer = layer.resize((round(layer.width * scale), round(layer.height * scale)),
                         Image.LANCZOS)
    img.paste(layer, (round(ccx * S - layer.width / 2), round(cy * S - layer.height / 2)),
              layer)


# ------------------------------------------------------------------- layout
STORIES = [
    ("CLIMATE \u00b7 ANTALYA", NAVY, icon_globe_doc,
     "COP31 ENDS WITH NO DEAL",
     "EU and others reject a final draft that never mentions fossil fuels."),
    ("WAR \u00b7 UKRAINE", RED, icon_ruin,
     "DRONE LEVELS FLATS NEAR KYIV",
     "Strike on Dymer kills at least 3; about 10 feared trapped in rubble."),
    ("WAR AT SEA \u00b7 LIBYA", RED, icon_ship,
     "SEA DRONES SINK RUSSIAN WARSHIP",
     "Corvette Merkury capsizes at Benghazi; a second ship is also hit."),
    ("DISASTER \u00b7 INDONESIA", NAVY, icon_factory,
     "36 MISSING AFTER FACTORY FIRE",
     "Cikande candy plant blaze kills 3; rescuers comb ruins on Sunday."),
    ("POLITICS \u00b7 USA", NAVY, icon_capitol,
     "BIGGEST HOUSE MAJORITY SINCE 1992",
     "258th seat: Hubbard beats Foxx in North Carolina recount by 330 votes."),
    ("SPORT \u00b7 PORTUGAL", GOLD, icon_trophy,
     "M\u00c1RQUEZ SEALS EIGHTH MOTOGP CROWN",
     "Eighth place in Portugal is enough; he ties Agostini on eight titles."),
]


def main():
    img = Image.new("RGB", (W * S, W * S), PAPER)
    d = ImageDraw.Draw(img)

    def X(v):
        return v * S

    # masthead
    d.rectangle([X(30), X(24), X(994), X(28)], fill=RULE)
    centered(d, X(512), X(36), "THE WORLD ON SUNDAY", F(SERIF_B, 54), INK, tracking=2)
    d.rectangle([X(30), X(106), X(994), X(110)], fill=RULE)

    # date band
    d.rectangle([X(30), X(120), X(994), X(182)], fill=INK)
    centered(d, X(512), X(129), "SUNDAY 22 NOVEMBER 2026", F(SANS_B, 48), (255, 255, 255),
             tracking=1)

    # panels: 2 cols x 3 rows, 192..980
    gx, gy = 14, 14
    px0, py0 = 30, 192
    pw = (1024 - 60 - gx) // 2
    ph = (980 - py0 - 2 * gy) // 3
    kick_f, head_f, sub_f = F(SANS_B, 18), F(SANS_B, 30), F(SANS, 21)
    worst = 0  # deepest panel text bottom, in design units from panel top
    for i, (kicker, accent, icon, head, sub) in enumerate(STORIES):
        cx0 = px0 + (i % 2) * (pw + gx)
        cy0 = py0 + (i // 2) * (ph + gy)
        d.rectangle([X(cx0), X(cy0), X(cx0 + pw), X(cy0 + ph)], fill=PANEL,
                    outline=(200, 195, 185), width=S)
        d.rectangle([X(cx0), X(cy0), X(cx0 + pw), X(cy0 + 6)], fill=accent)
        ccx = cx0 + pw // 2
        centered(d, X(ccx), X(cy0 + 11), kicker, kick_f, accent, tracking=2)
        render_icon(img, icon, ccx, cy0 + 71)
        y = cy0 + 116
        for line in wrap(d, head, head_f, X(pw - 36)):
            centered(d, X(ccx), X(y), line, head_f, INK)
            y += 36
        y += 4
        for line in wrap(d, sub, sub_f, X(pw - 44)):
            centered(d, X(ccx), X(y), line, sub_f, (60, 60, 66))
            y += 24
        text_bottom = y - 3
        worst = max(worst, text_bottom - cy0)
        if text_bottom > cy0 + ph - 12:
            raise SystemExit(f"panel {i} text overflows: bottom {text_bottom - cy0} of {ph}")

    # footer
    d.rectangle([X(30), X(988), X(994), X(991)], fill=RULE)
    centered(d, X(512), X(995),
             "SIX STORIES \u00b7 ONE DAY \u00b7 AS REPORTED BY REUTERS AND THE ASSOCIATED PRESS",
             F(SANS_B, 14), GREY, tracking=1)

    img = img.resize((W, W), Image.LANCZOS)
    print("deepest panel text bottom:", worst, "of panel height", ph)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
