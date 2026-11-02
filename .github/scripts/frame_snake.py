"""Wrap the snk-generated snake SVG in the profile's cyberpunk frame.

usage: python frame_snake.py <snake.svg> <out.svg>
"""
import re
import sys

BG, Y, C, R, D = "#0a0a12", "#f3e600", "#5ef6ff", "#ff3b5c", "#6a6a7e"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
W, PAD, TOP, BOTTOM = 1200, 40, 64, 56

src, out = sys.argv[1], sys.argv[2]
snake = open(src).read()

m = re.search(r"<svg\b([^>]*)>", snake)
attrs = m.group(1)
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', attrs).group(1).split()]
inner_w = W - 2 * PAD
inner_h = round(inner_w * vb[3] / vb[2])
H = TOP + inner_h + BOTTOM

# re-root the snake as a nested <svg> placed inside the frame
body = snake[m.end():snake.rindex("</svg>")]
nested = (f'<svg x="{PAD}" y="{TOP}" width="{inner_w}" height="{inner_h}" '
          f'viewBox="{" ".join(f"{v:g}" for v in vb)}">{body}</svg>')

frame = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs><pattern id="fx-scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".035"/></pattern></defs>
  <style>
    .fx-m {{ font-family: {MONO}; font-size: 12px; letter-spacing: 3px; white-space: pre; }}
    .fx-blink {{ animation: fx-blink 1s steps(1) infinite; }}
    @keyframes fx-blink {{ 50% {{ opacity: 0; }} }}
    .fx-sweep {{ animation: fx-sweep 4s linear infinite; }}
    @keyframes fx-sweep {{ from {{ transform: translateX(0); }} to {{ transform: translateX({inner_w}px); }} }}
    @media (prefers-reduced-motion: reduce) {{ .fx-blink, .fx-sweep, svg * {{ animation: none !important; }} }}
  </style>
  <path d="M1 1 H{W - 25} L{W - 1} 25 V{H - 1} H25 L1 {H - 25} Z" fill="{BG}" stroke="{Y}" stroke-opacity=".5"/>
  <path d="M1 1 H{W - 25} L{W - 1} 25 V{H - 1} H25 L1 {H - 25} Z" fill="url(#fx-scan)"/>
  <rect x="1" y="1" width="6" height="60" fill="{Y}"/>
  <text x="{PAD}" y="38" class="fx-m" fill="{R}">TRACE://THELOL3882</text>
  <text x="{W - PAD}" y="38" class="fx-m" fill="{D}" text-anchor="end">COMMITS CONSUMED · LAST 12 MONTHS</text>
  <path d="M{PAD} 48 H{W - PAD}" stroke="{Y}" stroke-opacity=".15"/>
  {nested}
  <rect x="{PAD}" y="{TOP - 6}" width="2" height="{inner_h + 12}" fill="{C}" opacity=".18" class="fx-sweep"/>
  <path d="M{PAD} {H - 40} H{W - PAD}" stroke="{Y}" stroke-opacity=".15"/>
  <text x="{PAD}" y="{H - 18}" class="fx-m" fill="{C}">SNAKE.EXE RUNNING<tspan class="fx-blink">_</tspan></text>
  <text x="{W - PAD}" y="{H - 18}" class="fx-m" fill="{D}" text-anchor="end">LESS <tspan fill="#161620">■</tspan> <tspan fill="#3b1420">■</tspan> <tspan fill="#6b1c2a">■</tspan> <tspan fill="{R}">■</tspan> <tspan fill="{C}">■</tspan> MORE</text>
</svg>
'''
open(out, "w").write(frame)
