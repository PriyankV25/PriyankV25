#!/usr/bin/env python3
"""Generate the personalized animated neofetch-style GitHub profile card."""

from pathlib import Path
from html import escape

WIDTH, HEIGHT = 820, 390
OUTPUT = Path(__file__).with_name("info-card.svg")
GREEN = "#39ff88"
DIM_GREEN = "#1f9d5c"
DARK = "#07110b"
GRID = "#0d2417"
TEXT = "#d7ffe5"

PROFILE = [
    ("role", "Software Engineer"),
    ("focus", "Automation • DevOps • Development • GenAI • Cloud"),
    ("os", "Windows / macOS / Linux"),
    ("scripting", "Python / PowerShell / Bash / CMD / C#"),
    ("editor", "VS Code"),
    ("automation", "Endpoint • Remediation • Installers • Agentic • Workflows"),
    ("pipelines", "Patch Intelligence • CI/CD • Observability • Deployments"),
]

def esc(value):
    return escape(str(value))

def svg_text(x, y, value, size=15, fill=TEXT, weight="400", anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="monospace" '
            f'font-size="{size}px" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}">{esc(value)}</text>')

def build_svg():
    s = []
    s.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="PriyankV25 developer profile">

<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#030804"/>
    <stop offset="100%" stop-color="{DARK}"/>
  </linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="2.2" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
    <path d="M22 0 L0 0 L0 22" fill="none" stroke="{GRID}" stroke-width="1"/>
  </pattern>
  <clipPath id="cardClip"><rect x="10" y="10" width="800" height="370" rx="14"/></clipPath>
</defs>
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>
<rect x="10" y="10" width="800" height="370" rx="14" fill="url(#grid)" stroke="{DIM_GREEN}" stroke-width="1.5"/>
''')
    s.append('<circle cx="32" cy="32" r="6" fill="#ff5f56"/>')
    s.append('<circle cx="52" cy="32" r="6" fill="#ffbd2e"/>')
    s.append('<circle cx="72" cy="32" r="6" fill="#27c93f"/>')
    s.append(svg_text(100, 38, "PriyankV25@github.com", 14, DIM_GREEN, "700"))
    s.append(svg_text(795, 38, "NEOFETCH", 12, DIM_GREEN, "700", "end"))
    s.append(f'''<g transform="translate(38 78)" fill="{GREEN}" filter="url(#glow)"
font-family="monospace" font-size="14px" font-weight="700">
  <text x="0" y="0">       ██████</text>
  <text x="0" y="17">     ██      ██</text>
  <text x="0" y="34">    ██  ◉  ◉  ██</text>
  <text x="0" y="51">    ██   &gt;    ██</text>
  <text x="0" y="68">     ██  ──  ██</text>
  <text x="0" y="85">       ██████</text>
  <text x="0" y="102">      ╱████╲</text>
  <text x="0" y="119">     ╱  ██  ╲</text>
  <text x="0" y="136">    ╱___██___╲</text>
</g>''')
    s.append(f'<g transform="translate(235 78)"><text x="0" y="0" font-family="monospace" font-size="17px" font-weight="700" fill="{GREEN}">PriyankV25<tspan fill="{DIM_GREEN}"> ─────────────────────</tspan></text>')
    y = 29
    for key, value in PROFILE:
        s.append(svg_text(0, y, f"{key:<11}", 14, GREEN, "700"))
        s.append(svg_text(125, y, value, 14, TEXT))
        y += 31
    s.append("</g>")
    s.append(f'''<g transform="translate(38 342)">
{svg_text(0, 0, "$ whoami", 14, GREEN, "700")}
{svg_text(92, 0, "Software Engineer", 14, TEXT)}
<rect x="255" y="-14" width="9" height="17" fill="{GREEN}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
</g>
<rect x="10" y="10" width="800" height="2" fill="{GREEN}" opacity="0.18" clip-path="url(#cardClip)"><animate attributeName="y" values="10;378;10" dur="5.5s" repeatCount="indefinite"/></rect>
<rect x="10" y="10" width="800" height="370" rx="14" fill="none" stroke="{GREEN}" stroke-width="0.7" opacity="0.25"><animate attributeName="opacity" values="0.15;0.35;0.15" dur="2.8s" repeatCount="indefinite"/></rect>
</svg>''')
    return "\n".join(s)

if __name__ == "__main__":
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Generated: {OUTPUT}")
