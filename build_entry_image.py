#!/usr/bin/env python3
"""Assemble the front page for Wednesday 25 November 2026.

Build-time only.  No photographs are used: every panel is drawn with
Pillow from the story tables below (a coloured scene block with a big
category mark, then a navy caption bar), so the picture is fully
deterministic and needs no network.  The entry program (main.py) only
copies the finished picture out; it never runs this script.

Usage:  python3 build_entry_image.py
Needs Pillow and the DejaVu fonts in /usr/share/fonts/truetype/dejavu/.
"""

import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "entry.png"
FONTS = Path("/usr/share/fonts/truetype/dejavu")
CAP = 1048576
W = 1024

NAVY = (13, 38, 76)
GOLD = (198, 160, 60)
PALEGOLD = (214, 178, 84)
WHITE = (255, 255, 255)
DARK = (24, 24, 24)
MIST = (205, 214, 228)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GREEN = (34, 110, 60)
PURPLE = (88, 52, 130)
BROWN = (122, 74, 30)
SLATE = (70, 84, 104)
CRIMSON = (150, 20, 50)
ORANGE = (190, 90, 20)
STEEL = (40, 90, 140)
OLIVE = (100, 110, 40)

# (headline, standfirst, scene colour, big mark, scene label)
GRID = [
    ("HUAWEI CONVICTED IN US", "Guilty on 10 of 12 counts", STEEL, "HW", "COURT"),
    ("NVIDIA RALLY FADES", "Huang back, shares drop again", TEAL, "NV", "MARKETS"),
    ("TRUMP PARDONS TURKEYS", "Freedom & Feathers spared", BROWN, "T", "THANKSGIVING"),
    ("GIULIANI GETS MEDAL", "Highest US civilian honour", (140, 100, 15), "★", "WHITE HOUSE"),
    ("HAMAS SECURITY CHIEF KILLED", "Israeli strike on Gaza City", CRIMSON, "G", "GAZA"),
    ("RIYADH TOWER HIT AGAIN", "Saudi condemns 'terrorist attack'", RED, "R", "SAUDI ARABIA"),
    ("COP31 COLLAPSES", "No deal as producers block phaseout", GREEN, "31", "CLIMATE"),
    ("SENEGAL WIN AFCON BACK", "CAS overturns Morocco ruling", OLIVE, "AF", "FOOTBALL"),
    ("REAL MADRID 5-1 PSV", "Bellingham stunner, Mbappe brace", PURPLE, "5-1", "CHAMPIONS LEAGUE"),
    ("25 HOSTAGES IN COLOMBIA", "Gunmen seize Cartagena supermarket", SLATE, "25", "CARTAGENA"),
    ("CIA, ODNI BREACHED", "Unclassified data exposed, NYT says", NAVY, "CIA", "CYBER"),
    ("5 WOMEN KILLED EACH HOUR", "By relatives in 2025, UN says", CRIMSON, "5", "UNITED NATIONS"),
]

TICKER = [
    "IRAQ ORDERS SEIZURE OF KURDISH OILFIELDS",
    "RUSSIA CRIES 'TERRORISM' OVER DRONES",
    "GAZA DEATH TOLL 74,746, WAFA SAYS",
    "266M FACE ACUTE FOOD INSECURITY — WFP",
    "LANDMINE DEATHS HIT 5-YEAR HIGH: 7,000",
    "SHEIN TO PAY $100M IN FTC SETTLEMENT",
    "EXTREME FLOODING THREATENS CALIFORNIA",
    "SEOUL: RUSSIAN PLANES IN AIR ZONE",
    "DEMOCRATS TURN SIGHTS TO 2028",
    "FORT HOOD: LAST BID ON EXECUTION FAILS",
    "US SOLDIER ADMITS SELLING SECRETS",
    "MALAYSIA TO REPATRIATE MIGRANTS",
    "N KOREA THREATENS TO SHUT SWISS OFFICE",
    "CHINA COBALT RACE BEATS CONGO BAN",
    "DENMARK UPHOLDS 'GHETTO' EVICTIONS",
    "NIGERIA EMIR SUSPENDED OVER CLAIM",
    "REBELS PULL BACK IN DR CONGO",
    "BRITAIN SANCTIONS HOUTHIS, 4 OFFICIALS",
]

GEOM = dict(
    masthead_h=72, rule_h=4, lead_top=80, lead_h=164, lead_pic_w=620,
    lead_block_x=634, lead_block_w=382, grid_top=248, pic_h=70, cap_h=58,
    gap=6, col_w=332, col_x=(8, 346, 684), tick_rule_y=794, tick_top=804,
    tick_y0=832, tick_step=22, foot_y=978,
)


def F(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def lines_for(d, text, face, width):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=face) <= width or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def shrink_fit(d, text, sizes, width, max_lines=1):
    for size in sizes:
        face = F("DejaVuSans-Bold.ttf", size)
        wrapped = lines_for(d, text, face, width)
        if len(wrapped) <= max_lines:
            return face, wrapped
    face = F("DejaVuSans-Bold.ttf", sizes[-1])
    return face, lines_for(d, text, face, width)


def box(d, x0, y0, x1, y1, color):
    d.rectangle([x0, y0, x1, y1], fill=color)


def put_text(d, x, y, text, face, color, anchor=None):
    kw = {"font": face, "fill": color}
    if anchor:
        kw["anchor"] = anchor
    d.text((x, y), text, **kw)


def scene(d, x, y, w, h, color, mark, label):
    """Coloured scene block: big mark left, label strip at the bottom."""
    box(d, x, y, x + w, y + h, color)
    d.rectangle([x, y, x + w, y + 5], fill=GOLD)
    face, lines = shrink_fit(d, mark, (44, 38, 32, 26), w - 20)
    put_text(d, x + 12, y + 8, lines[0], face, WHITE)
    put_text(d, x + w - 10, y + h - 20, label,
             F("DejaVuSans-Bold.ttf", 11), PALEGOLD, anchor="ra")


def masthead(d):
    g = GEOM
    box(d, 0, 0, W, g["masthead_h"], NAVY)
    put_text(d, W // 2, 6, "THE WORLD IN ONE PICTURE",
             F("DejaVuSans-Bold.ttf", 40), WHITE, anchor="ma")
    put_text(d, W // 2, 48, "WEDNESDAY 25 NOVEMBER 2026  |  MORNING EDITION",
             F("DejaVuSans-Bold.ttf", 19), PALEGOLD, anchor="ma")
    box(d, 0, g["masthead_h"], W, g["masthead_h"] + g["rule_h"], GOLD)


def lead(d):
    g = GEOM
    top, h = g["lead_top"], g["lead_h"]
    scene(d, 8, top, g["lead_pic_w"], h, RED, "CHINA", "BEIJING • SHANGHAI")
    bx, bw = g["lead_block_x"], g["lead_block_w"]
    box(d, bx, top, bx + bw, top + h, NAVY)
    pad = 14
    put_text(d, bx + pad, top + 10, "THE LEAD  |  CHINA",
             F("DejaVuSans-Bold.ttf", 15), PALEGOLD)
    face, head_lines = shrink_fit(d, "POLITBURO CHIEF PROBED",
                                  (27,), bw - 2 * pad)
    y = top + 34
    for line in head_lines:
        put_text(d, bx + pad, y, line, face, WHITE)
        y += 32
    body = F("DejaVuSans.ttf", 15)
    blurb = ("Shanghai party chief Chen Jining under investigation; "
             "the fourth Politburo member probed since 2025.")
    for line in lines_for(d, blurb, body, bw - 2 * pad):
        put_text(d, bx + pad, y, line, body, WHITE)
        y += 19


def grid(d):
    g = GEOM
    sub = F("DejaVuSans.ttf", 12)
    for n, (head, stand, color, mark, label) in enumerate(GRID):
        row, col = divmod(n, 3)
        x = g["col_x"][col]
        y = g["grid_top"] + row * (g["pic_h"] + g["cap_h"] + g["gap"])
        scene(d, x, y, g["col_w"], g["pic_h"], color, mark, label)
        cap = y + g["pic_h"]
        box(d, x, cap, x + g["col_w"], cap + g["cap_h"], NAVY)
        face, head_lines = shrink_fit(d, head, (17, 16, 15, 14),
                                      g["col_w"] - 16)
        if len(head_lines) > 1:
            face, head_lines = shrink_fit(d, head, (15, 14),
                                          g["col_w"] - 16, 2)
        ty = cap + 5
        for line in head_lines:
            put_text(d, x + 8, ty, line, face, WHITE)
            ty += 19 if face.size == 17 else 18
        sy = max(cap + g["cap_h"] - 16, ty + 1)
        put_text(d, x + 8, sy, stand, sub, MIST)


def ticker(d):
    g = GEOM
    box(d, 0, g["tick_rule_y"], W, g["tick_rule_y"] + 4, GOLD)
    put_text(d, 8, g["tick_top"], "ALSO TODAY",
             F("DejaVuSans-Bold.ttf", 20), NAVY)
    dot = F("DejaVuSans-Bold.ttf", 12)
    face = F("DejaVuSans-Bold.ttf", 12)
    for n, item in enumerate(TICKER):
        col, row = divmod(n, 6)
        x = g["col_x"][col]
        y = g["tick_y0"] + row * g["tick_step"]
        shown = item
        while shown and d.textlength(shown, font=face) > 316:
            shown = shown.rsplit(" ", 1)[0]
        if shown != item:
            shown = shown.rstrip() + "…"
        put_text(d, x, y, "•", dot, GOLD)
        put_text(d, x + 14, y, shown, face, DARK)
    put_text(d, W // 2, g["foot_y"],
             "Sources: Reuters, AP, BBC, SCMP, The Hindu, The Guardian "
             "— as reported by 02:00 UTC, 25 November 2026",
             F("DejaVuSans.ttf", 13), DARK, anchor="ma")


def save(page):
    quality = 88
    while True:
        buf = io.BytesIO()
        page.save(buf, format="JPEG", quality=quality, optimize=True)
        if buf.tell() <= CAP or quality <= 60:
            OUT.write_bytes(buf.getvalue())
            return quality
        quality -= 4


def main():
    page = Image.new("RGB", (W, W), WHITE)
    d = ImageDraw.Draw(page)
    masthead(d)
    lead(d)
    grid(d)
    ticker(d)
    quality = save(page)
    size = OUT.stat().st_size
    print(f"wrote {OUT} ({size} bytes, JPEG quality {quality})")
    return 0 if size <= CAP else 1


if __name__ == "__main__":
    raise SystemExit(main())
