#!/usr/bin/env python3
"""Build the front-page image for Wednesday 25 November 2026.

Build-time only: draws a 1024x1024 newspaper front page with Pillow,
using flat coloured blocks and simple shapes only. No photos, no
network access, no external files. Run it once to produce entry.png
next to this script.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1024
HEIGHT = 1024
OUTPUT = Path(__file__).resolve().parent / "entry.png"

# Palette: deep navy masthead, warm paper background, strong accent
# colours so each story panel reads as a distinct coloured scene.
NAVY = (16, 32, 64)
NAVY_LIGHT = (28, 52, 96)
PAPER = (248, 244, 232)
INK = (18, 18, 18)
GREY = (90, 90, 90)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
LEAD_BG = (122, 20, 20)
LEAD_ACCENT = (232, 180, 60)
TICKER_BG = (20, 42, 78)

MASTHEAD_TITLE = "THE WORLD IN ONE PICTURE"
MASTHEAD_SUB = "WEDNESDAY 25 NOVEMBER 2026  |  MORNING EDITION"

LEAD_KICKER = "LEAD STORY  •  CHINA"
LEAD_HEADLINE = "Shanghai party chief under investigation"
LEAD_DECK = (
    "Chen Jining, a member of the Politburo, is being probed — "
    "the fourth Politburo member investigated since 2025."
)

# Twelve pictured stories: (category, headline, scene colour, mark)
PICTURED = [
    ("COURTS", "Huawei convicted in the US on 10 of 12 counts",
     (36, 68, 120), "§"),
    ("MARKETS", "Nvidia rally fades as Huang returns",
     (18, 110, 78), "$"),
    ("WHITE HOUSE", "Trump pardons turkeys Freedom and Feathers",
     (176, 96, 20), "★"),
    ("WASHINGTON", "Giuliani awarded the Medal of Freedom",
     (96, 58, 140), "✦"),
    ("GAZA", "Hamas security chief killed in Gaza City strike",
     (140, 40, 32), "▲"),
    ("RIYADH", "Tower hit a second time in a week",
     (58, 92, 110), "▮"),
    ("CLIMATE", "COP31 collapses with no deal",
     (28, 96, 66), "●"),
    ("FOOTBALL", "Senegal win the AFCON title back after a CAS ruling",
     (22, 112, 62), "⚽"),
    ("FOOTBALL", "Real Madrid 5–1 PSV",
     (200, 170, 30), "5"),
    ("COLOMBIA", "25 hostages taken at a Cartagena supermarket",
     (120, 40, 90), "!"),
    ("SECURITY", "CIA and ODNI hit by cybersecurity breach",
     (60, 60, 66), "⌘"),
    ("UNITED NATIONS", "Five women killed each hour by relatives in 2025",
     (150, 60, 90), "♥"),
]

TICKER = [
    "Iraq: Kurdish oilfields in focus",
    "Russia claims ship drones were “terrorism”",
    "Gaza toll reaches 74,746",
    "WFP: 266 million people food-insecure",
    "Landmine deaths hit a five-year high of 7,000",
    "Shein agrees $100m FTC settlement",
    "California hit by flooding",
    "Russian planes enter South Korea’s air zone",
    "Democrats look ahead to 2028",
    "Fort Hood execution bid advances",
    "US soldier accused of selling secrets",
    "Malaysia steps up repatriations",
    "North Korea opens a Swiss office",
    "China in the race for cobalt",
    "Denmark orders “ghetto” evictions",
    "Nigeria suspends an emir",
    "DR Congo rebels pull back",
    "Britain sanctions the Houthis",
]


def load_font(bold=False, size=20):
    """Pick a DejaVu font when present, else Pillow's built-in font."""
    names = (
        ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]
        if bold
        else ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]
    )
    for name in names:
        for base in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts"):
            path = Path(base) / name
            if path.exists():
                try:
                    return ImageFont.truetype(str(path), size)
                except OSError:
                    continue
    return ImageFont.load_default(size=size)


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit inside max_width pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_masthead(draw):
    """Navy band across the top with the paper's name and date line."""
    draw.rectangle([0, 0, WIDTH, 92], fill=NAVY)
    draw.rectangle([0, 88, WIDTH, 92], fill=GOLD)
    title_font = load_font(bold=True, size=44)
    sub_font = load_font(bold=False, size=19)
    title_w = draw.textlength(MASTHEAD_TITLE, font=title_font)
    draw.text(((WIDTH - title_w) / 2, 10), MASTHEAD_TITLE,
              font=title_font, fill=WHITE)
    sub_w = draw.textlength(MASTHEAD_SUB, font=sub_font)
    draw.text(((WIDTH - sub_w) / 2, 60), MASTHEAD_SUB,
              font=sub_font, fill=(205, 214, 232))


def draw_lead(draw):
    """The lead story: a wide red block with a big headline and deck."""
    x0, y0, x1, y1 = 12, 100, WIDTH - 12, 296
    draw.rectangle([x0, y0, x1, y1], fill=LEAD_BG)
    draw.rectangle([x0, y0, x1, y0 + 6], fill=LEAD_ACCENT)
    # Stylised skyline: a row of dark towers with lit windows.
    for i, tower_h in enumerate((58, 88, 66, 104, 74, 96, 60)):
        tx = x1 - 30 - i * 52
        draw.rectangle([tx, y1 - tower_h, tx + 38, y1],
                       fill=(64, 10, 10))
        for wy in range(y1 - tower_h + 10, y1 - 8, 16):
            draw.rectangle([tx + 8, wy, tx + 14, wy + 7],
                           fill=LEAD_ACCENT)
            draw.rectangle([tx + 22, wy, tx + 28, wy + 7],
                           fill=LEAD_ACCENT)
    kicker_font = load_font(bold=True, size=18)
    head_font = load_font(bold=True, size=40)
    deck_font = load_font(bold=False, size=20)
    draw.text((30, y0 + 20), LEAD_KICKER, font=kicker_font,
              fill=LEAD_ACCENT)
    head_lines = wrap_text(draw, LEAD_HEADLINE, head_font, 620)
    y = y0 + 48
    for line in head_lines:
        draw.text((30, y), line, font=head_font, fill=WHITE)
        y += 46
    deck_lines = wrap_text(draw, LEAD_DECK, deck_font, 620)
    for line in deck_lines:
        draw.text((30, y + 4), line, font=deck_font, fill=(238, 220, 200))
        y += 26


def draw_panels(draw):
    """Twelve pictured stories in a 4 by 3 grid of panels."""
    margin, gap = 12, 8
    panel_w = (WIDTH - 2 * margin - 3 * gap) // 4
    panel_h = 148
    top = 306
    cat_font = load_font(bold=True, size=13)
    head_font = load_font(bold=True, size=17)
    mark_font = load_font(bold=True, size=34)
    for index, (category, headline, colour, mark) in enumerate(PICTURED):
        row, col = divmod(index, 4)
        x0 = margin + col * (panel_w + gap)
        y0 = top + row * (panel_h + gap)
        x1, y1 = x0 + panel_w, y0 + panel_h
        draw.rectangle([x0, y0, x1, y1], fill=WHITE,
                       outline=(200, 196, 184))
        # Coloured scene strip across the top of the panel.
        draw.rectangle([x0, y0, x1, y0 + 52], fill=colour)
        draw.ellipse([x0 + 12, y0 + 8, x0 + 48, y0 + 44],
                     fill=(255, 255, 255))
        mark_w = draw.textlength(mark, font=mark_font)
        draw.text((x0 + 30 - mark_w / 2, y0 + 6), mark,
                  font=mark_font, fill=colour)
        # A simple horizon line and sun dot inside the scene strip.
        draw.rectangle([x0 + 64, y0 + 38, x1 - 12, y0 + 41],
                       fill=(255, 255, 255))
        draw.ellipse([x1 - 34, y0 + 10, x1 - 18, y0 + 26],
                     fill=(255, 240, 170))
        draw.text((x0 + 8, y0 + 60), category, font=cat_font, fill=RED)
        lines = wrap_text(draw, headline, head_font, panel_w - 16)
        y = y0 + 80
        for line in lines[:4]:
            draw.text((x0 + 8, y), line, font=head_font, fill=INK)
            y += 20


def draw_ticker(draw):
    """ALSO TODAY: eighteen one-line briefs in two columns."""
    y0 = 786
    draw.rectangle([0, y0, WIDTH, HEIGHT], fill=TICKER_BG)
    draw.rectangle([0, y0, WIDTH, y0 + 4], fill=GOLD)
    head_font = load_font(bold=True, size=20)
    item_font = load_font(bold=False, size=16)
    draw.text((16, y0 + 12), "ALSO TODAY", font=head_font, fill=GOLD)
    draw.line([16, y0 + 40, WIDTH - 16, y0 + 40],
              fill=(120, 140, 180))
    col_w = (WIDTH - 32) // 2
    for index, item in enumerate(TICKER):
        col, row = divmod(index, 9)
        x = 16 + col * col_w
        y = y0 + 50 + row * 20
        draw.text((x, y), "•  " + item, font=item_font, fill=WHITE)


def build():
    """Compose the whole page and save it as a PNG under 1 MiB."""
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw)
    draw_lead(draw)
    draw_panels(draw)
    draw_ticker(draw)
    # A thin rule and dateline at the very foot of the page.
    draw.text((16, HEIGHT - 4), "", font=load_font(size=10))
    image.save(OUTPUT, format="PNG", optimize=True)
    size = OUTPUT.stat().st_size
    print(f"wrote {OUTPUT} {WIDTH}x{HEIGHT} {size} bytes")
    if size > 1_048_576:
        raise SystemExit("entry.png is over the 1 MiB limit")
    return OUTPUT


if __name__ == "__main__":
    build()
