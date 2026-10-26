#!/usr/bin/env python3
"""
Generate an 840x880 terminal window SVG for Rishikesh Sharma (rishi-ascii.svg)
that perfectly pairs with stats.svg (also 840x880) at equal width (420px each).
Includes macOS title bar, cyber operator ASCII art, live typed identity dossier,
and a blinking terminal prompt. Fully XML-escaped for GitHub Camo proxy.
"""
import html
import os
import xml.etree.ElementTree as ET

OUT = os.path.join(os.path.dirname(__file__), "..", "rishi-ascii.svg")

W, H = 840, 880
PAD = 20
TITLEBAR_H = 30
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
GREEN = "#39d353"
CYAN = "#00D4FF"
PINK = "#FF006E"
INK = "#e6edf3"
PURPLE = "#8B5CF6"

ascii_lines = [
    r"  _____  _____  _____ _    _ _____ _  ________ _____ _    _ ",
    r" |  __ \|_   _|/ ____| |  | |_   _| |/ /  ____/ ____| |  | |",
    r" | |__) | | | | (___ | |__| | | | | ' /| |__ | (___ | |__| |",
    r" |  _  /  | |  \___ \|  __  | | | |  < |  __| \___ \|  __  |",
    r" | | \ \ _| |_ ____) | |  | |_| |_| . \| |________) | |  | |",
    r" |_|  \_\_____|_____/|_|  |_|_____|_|\_\______|_____/|_|  |_|",
]

dossier = [
    ("$ whoami --verbose", CYAN, True),
    ("operator      : Rishikesh Sharma [r00t_alpha]", INK, False),
    ("role          : Cybersecurity Engineer & AI Researcher", INK, False),
    ("education     : B.E. CS + Cybersecurity @ Chandigarh Univ", INK, False),
    ("rank          : Top 50 Internationally on CTFtime.org", GREEN, True),
    ("achievements  : 1st Place CyberStrike CTF & ZEAI Hackathon", GREEN, True),
    ("security_ops  : Web Exploitation · Network Forensics · Red Team", INK, False),
    ("ai_defense    : Protocol X — Zero-Trust AI LLM Firewall", CYAN, True),
    ("investigation : AI Forensic Time Machine (Incident Response)", CYAN, False),
    ("hardware_iot  : Nextron (5-Feature Gesture Smart Vehicle)", INK, False),
    ("digital_reach : 3,000,000+ Subscribers (YouTube Network)", PINK, True),
    ("base_coords   : Chandigarh, India [28°N 77°E]", INK, False),
    ("system_status : [ ONLINE ] — All defensive perimeters active", GREEN, False),
]

svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>',
    '  .t { opacity:0; animation:fade 0.5s ease-out both; }',
    '  .cursor { animation:blink 1s steps(2, start) infinite; }',
    '  @keyframes fade { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }',
    '  @keyframes blink { 0%, 100% { opacity:1; } 50% { opacity:0; } }',
    '</style>',
    '<defs>',
    '  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
    f'    <stop offset="0" stop-color="{BG2}"/>',
    f'    <stop offset="1" stop-color="{BG}"/>',
    '  </linearGradient>',
    '</defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

# macOS title dots
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    svg_parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')

svg_parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">rishi@github: ~$ whoami</text>'
)

# ASCII Header Banner (Escaped)
start_y = 65
for idx, line in enumerate(ascii_lines):
    delay = idx * 0.08
    safe_line = html.escape(line)
    svg_parts.append(
        f'<text class="t" style="animation-delay:{delay:.2f}s" x="{PAD+10}" y="{start_y + idx*16}" '
        f'fill="{GREEN}" font-size="11.5" font-weight="700" xml:space="preserve">{safe_line}</text>'
    )

# Separator line
sep_y = start_y + len(ascii_lines) * 16 + 18
svg_parts.append(f'<line x1="{PAD}" y1="{sep_y}" x2="{W-PAD}" y2="{sep_y}" stroke="{FRAME}" stroke-dasharray="4,4"/>')

# Dossier Lines (Escaped)
cur_y = sep_y + 36
line_h = 36
for idx, (text, color, is_bold) in enumerate(dossier):
    delay = 0.5 + idx * 0.12
    fw = "700" if is_bold else "400"
    fsize = "18" if text.startswith("$") else "16"
    safe_text = html.escape(text)
    svg_parts.append(
        f'<text class="t" style="animation-delay:{delay:.2f}s" x="{PAD+20}" y="{cur_y}" '
        f'fill="{color}" font-size="{fsize}" font-weight="{fw}">{safe_text}</text>'
    )
    cur_y += line_h

# Footer status line with blinking cursor
status_y = H - 35
svg_parts.append(f'<line x1="0" y1="{status_y - 20}" x2="{W}" y2="{status_y - 20}" stroke="{FRAME}"/>')
svg_parts.append(
    f'<text x="{PAD+10}" y="{status_y}" fill="{MUTED}" font-size="14">rishi@cyberdeck:~$ <tspan fill="{INK}">exec mission_active</tspan></text>'
)
svg_parts.append(
    f'<rect class="cursor" x="375" y="{status_y - 13}" width="9" height="17" fill="{GREEN}"/>'
)

svg_parts.append('</svg>')

svg = "".join(svg_parts)

# Verify valid XML before writing
ET.fromstring(svg)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"VALID XML! Wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
