#!/usr/bin/env python3
from pathlib import Path
import argparse, html, random
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

CHARS = "@%#*+=-:. "

def build_ascii(image_path, cols=86):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    crop = img.crop((int(w*.12), int(h*.02), int(w*.88), int(h*.92)))
    gray = ImageOps.grayscale(crop)
    gray = ImageEnhance.Contrast(gray).enhance(1.45)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))
    rows = max(40, int(cols * gray.height / gray.width * .50))
    small = gray.resize((cols, rows), Image.Resampling.LANCZOS)
    result = []
    for y in range(rows):
        row = []
        for x in range(cols):
            v = (small.getpixel((x, y)) / 255.0) ** .82
            row.append(CHARS[min(len(CHARS)-1, int(v*(len(CHARS)-1)))])
        result.append("".join(row))
    return result

def make_svg(lines, output):
    cols = max(len(x) for x in lines)
    font_size, char_w, line_h = 7.2, 7.2, 9.0
    width = cols * char_w + 24
    height = len(lines) * line_h + 24
    rng = random.Random(42)
    spans = []
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == " ":
                continue
            opacity = .62 + rng.random()*.30
            delay = rng.random()*3.5
            duration = 1.8 + rng.random()*2.8
            spans.append(
                f'<text x="{12+x*char_w:.1f}" y="{17+y*line_h:.1f}" class="c" '
                f'style="--o:{opacity:.2f};--d:{delay:.2f}s;--t:{duration:.2f}s">'
                f'{html.escape(ch)}</text>'
            )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}"
viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="Animated ASCII portrait">
<defs>
<filter id="glow"><feGaussianBlur stdDeviation=".55" result="b"/><feMerge>
<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#fff" stop-opacity="0"/>
<stop offset=".48" stop-color="#fff" stop-opacity=".08"/>
<stop offset=".50" stop-color="#fff" stop-opacity=".40"/>
<stop offset=".52" stop-color="#fff" stop-opacity=".08"/>
<stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<style>
.c {{ font-family:"DejaVu Sans Mono","Liberation Mono",monospace; font-size:{font_size}px;
fill:#b7ffcf; opacity:var(--o); filter:url(#glow);
animation:flicker var(--t) ease-in-out var(--d) infinite alternate; }}
@keyframes flicker {{ 0%,100%{{opacity:calc(var(--o)*.72)}} 50%{{opacity:calc(var(--o)*1.15)}} }}
.scan {{ animation:scan 4.8s linear infinite; }}
@keyframes scan {{ from{{transform:translateY(-{height:.0f}px)}} to{{transform:translateY({height:.0f}px)}} }}
</style></defs>
<rect width="100%" height="100%" rx="8" fill="#0b0f0d"/>
<g>{''.join(spans)}</g>
<rect class="scan" x="0" y="0" width="{width:.0f}" height="{height:.0f}"
fill="url(#scan)" pointer-events="none"/>
</svg>'''
    Path(output).write_text(svg, encoding="utf-8")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--columns", type=int, default=86)
    args = p.parse_args()
    make_svg(build_ascii(args.input, args.columns), args.output)
    print(f"Generated {args.output}")
