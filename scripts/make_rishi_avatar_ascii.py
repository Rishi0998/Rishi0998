#!/usr/bin/env python3
"""
Convert Rishikesh Sharma's avatar (current_avatar.png) into a clean, monochrome
animated ASCII-art terminal SVG (rishi-ascii.svg) matching the exact dimensions
(840 x 880) and aesthetics of stats.svg.
"""
import html
import os
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "current_avatar.png")
OUT = os.path.join(HERE, "..", "rishi-ascii.svg")
OUT_DOSSIER = os.path.join(HERE, "..", "profile-dossier.svg")

COLS = 160
ART_W_TARGET = 800
CELL_W = ART_W_TARGET / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)
RAMP = " .`:-=+*cs#%@"

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = 840.0
CANVAS_H = 880.0

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
GREEN = "#39d353"
CYAN = "#00D4FF"
CURSOR = "#39d353"

ROW_DUR = 5.2 / ROWS
STAGGER = ROW_DUR

# Load image and clean background
im_raw = Image.open(SRC).convert("RGB")
arr = np.array(im_raw, dtype=float)

# Background mask: where color is close to [114, 89, 119]
bg_dist = np.sqrt(np.sum((arr - [114, 89, 119])**2, axis=-1))
is_bg = bg_dist < 28

gray = np.mean(arr, axis=-1)
gray[is_bg] = 255.0  # background becomes white / blank in ascii ramp

im_gray = Image.fromarray(gray.astype(np.uint8)).resize((COLS, ROWS), Image.LANCZOS)
px = np.array(im_gray)

rows_txt = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        val = px[y, x]
        if val > 235:
            chars.append(" ")
            continue
        idx = int((1.0 - val / 235.0) * (len(RAMP) - 1) + 0.5)
        idx = max(0, min(len(RAMP) - 1, idx))
        chars.append(RAMP[idx])
    rows_txt.append("".join(chars))

art_top = TITLEBAR_H + PAD * 0.35

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
)
parts.append(
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient></defs>'
)

parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(
    f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">rishi@github: ~$ ./portrait.sh</text>'
)

font_size = CELL_H * 0.86
for ry, line in enumerate(rows_txt):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    safe = html.escape(line)
    text = (
        f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
        f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>'
    )

    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W}" height="{CELL_H-2}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

# Status bar
status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
    f'rishi@github:~$ whoami <tspan fill="{CYAN}">Rishikesh Sharma</tspan></text>'
)
status_chars = len("rishi@github:~$ whoami Rishikesh Sharma ")
parts.append(
    f'<rect x="{PAD + status_chars * 13 * 0.6:.1f}" y="{status_y-12:.1f}" width="8" height="14" fill="{GREEN}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>'
)

parts.append("</svg>")
svg = "".join(parts)

# Validate XML strictly
ET.fromstring(svg)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
with open(OUT_DOSSIER, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"SUCCESS! Wrote {OUT} and {OUT_DOSSIER}: {CANVAS_W} x {CANVAS_H}, {len(svg)//1024} KB")
