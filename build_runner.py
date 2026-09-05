#!/usr/bin/env python3
"""Emit assets/runner.svg — an original 8-bit style runner sprite sprinting
across a scrolling scanline landscape, collecting commit-coins."""

PX = 7          # pixel scale
SX, SY = 452, 44   # sprite origin on canvas
W, H = 1000, 150

PAL = {
    'H': '#c9d6f5',   # helmet shell
    'V': '#00fff7',   # visor
    'W': '#e8f0ff',   # suit
    'P': '#ff2bd1',   # backpack
    'B': '#2b3358',   # boots
    'G': '#39ff88',   # accent light
}

# 12 wide x 13 tall. '.' = transparent
FRAME_A = [
    "....HHHH....",
    "...HVVVVH...",
    "...HVVVVH...",
    "...HHHHHH...",
    "PP.WWWWWW...",
    "PPWWWWWWWW..",
    "PPWWWWWWWWW.",
    "PP.WWWWWW...",
    "...WWWWWW...",
    "..WW....WW..",
    ".WW......WW.",
    ".BB......BB.",
    "............",
]

FRAME_B = [
    "....HHHH....",
    "...HVVVVH...",
    "...HVVVVH...",
    "...HHHHHH...",
    "PP.WWWWWWW..",
    "PPWWWWWWWW..",
    "PPWWWWWWWW..",
    "PP.WWWWWW...",
    "...WWWWWW...",
    "...WWWWWW...",
    "...WW..WW...",
    "..BB....BBB.",
    "............",
]

FRAME_C = [
    "....HHHH....",
    "...HVVVVH...",
    "...HVVVVH...",
    "...HHHHHH...",
    "PP.WWWWWW.G.",
    "PPWWWWWWWW..",
    "PPWWWWWWWW..",
    "PP.WWWWWW...",
    "...WWWWWW...",
    "...WWWWWW...",
    "..WW....WW..",
    ".BBB....BB..",
    "............",
]


def sprite(rows, gid, begin, dur):
    out = [f'<g id="{gid}">']
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            ch = row[x]
            if ch == '.':
                x += 1
                continue
            run = 1
            while x + run < len(row) and row[x + run] == ch:
                run += 1
            out.append(
                f'<rect x="{SX + x*PX}" y="{SY + y*PX}" width="{PX*run}" '
                f'height="{PX}" fill="{PAL[ch]}"/>'
            )
            x += run
    # frame visibility cycling
    out.append(
        f'<animate attributeName="opacity" values="1;0;0;1" '
        f'keyTimes="0;0.001;{dur-0.001};{dur}" dur="0.36s" '
        f'begin="{begin}s" repeatCount="indefinite" fill="freeze"/>'
    )
    out.append('</g>')
    return "\n".join(out)


def build():
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" role="img" aria-label="8-bit runner">')
    p.append('''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#080b1c"/><stop offset="100%" stop-color="#05070f"/>
  </linearGradient>
  <pattern id="brick" width="28" height="14" patternUnits="userSpaceOnUse">
    <rect width="28" height="14" fill="#1d2a52"/>
    <rect width="27" height="13" fill="#2b3358"/>
    <rect x="13" y="7" width="1" height="7" fill="#1d2a52"/>
  </pattern>
  <pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1.3" fill="#00fff7" opacity="0.06"/>
  </pattern>
  <filter id="rg" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <style>
    .m{font-family:"SFMono-Regular","Consolas","Liberation Mono","Courier New",monospace}
    .bob{animation:bob .36s steps(1) infinite}
    @keyframes bob{0%{transform:translateY(0)}33%{transform:translateY(-5px)}66%{transform:translateY(-2px)}}
  </style>
</defs>''')

    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

    # parallax stars (slow)
    p.append('<g fill="#cfe0ff">')
    for i, (cx, cy, r, d) in enumerate([(120, 22, 1.4, 9), (340, 14, 1.1, 12),
                                        (610, 28, 1.5, 8), (860, 18, 1.2, 11),
                                        (960, 40, 1.1, 14)]):
        p.append(f'<circle cy="{cy}" r="{r}" opacity="0.7">'
                 f'<animate attributeName="cx" values="{cx};{cx-1000}" dur="{d}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".2;.9;.2" dur="{2+i*0.4}s" repeatCount="indefinite"/>'
                 f'</circle>')
    p.append('</g>')

    # mid-layer: scrolling satellites / antennae silhouettes
    p.append('<g opacity="0.5" stroke="#7b5cff" fill="none" stroke-width="2">')
    for off, d in [(0, 5.5), (500, 5.5)]:
        p.append(f'<g><animateTransform attributeName="transform" type="translate" '
                 f'from="{off} 0" to="{off-1000} 0" dur="{d}s" repeatCount="indefinite"/>'
                 f'<path d="M180 96 L180 66 M168 66 L192 66 M174 58 L186 58"/>'
                 f'<rect x="172" y="72" width="16" height="10"/>'
                 f'<path d="M700 96 L700 74 M688 74 L712 74"/>'
                 f'<circle cx="700" cy="66" r="6"/></g>')
    p.append('</g>')

    # ground
    p.append(f'<rect x="0" y="{SY + 13*PX}" width="{W}" height="{H - (SY + 13*PX)}" fill="url(#brick)"/>')
    p.append(f'<rect x="0" y="{SY + 13*PX}" width="{W}" height="3" fill="#00fff7" opacity="0.65"/>')

    # scrolling ground rubble
    p.append('<g fill="#3a4570">')
    for off, d in [(0, 2.2), (1000, 2.2)]:
        p.append(f'<g><animateTransform attributeName="transform" type="translate" '
                 f'from="{off} 0" to="{off-1000} 0" dur="{d}s" repeatCount="indefinite"/>'
                 f'<rect x="90" y="{SY+13*PX+10}" width="18" height="6"/>'
                 f'<rect x="330" y="{SY+13*PX+18}" width="26" height="6"/>'
                 f'<rect x="640" y="{SY+13*PX+9}" width="14" height="6"/>'
                 f'<rect x="880" y="{SY+13*PX+20}" width="22" height="6"/></g>')
    p.append('</g>')

    # commit coins flying toward the runner
    p.append('<g>')
    for i, (start, y, d) in enumerate([(1030, 60, 2.6), (1240, 34, 3.1), (1480, 78, 2.3)]):
        p.append(
            f'<g filter="url(#rg)">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="{start} 0" to="{start-1500} 0" dur="{d}s" repeatCount="indefinite"/>'
            f'<ellipse cx="0" cy="{y}" rx="9" ry="12" fill="#ffd83d" stroke="#ff9d00" stroke-width="2">'
            f'<animate attributeName="rx" values="9;1.5;9" dur="0.5s" repeatCount="indefinite"/></ellipse>'
            f'</g>')
    p.append('</g>')

    # runner sprite (3-frame cycle, bobbing)
    p.append('<g class="bob">')
    p.append(sprite(FRAME_A, 'fa', 0.00, 0.3333))
    p.append(sprite(FRAME_B, 'fb', 0.12, 0.3333))
    p.append(sprite(FRAME_C, 'fc', 0.24, 0.3333))
    # jetpack puff
    p.append('<g fill="#00fff7" opacity="0.9">'
             f'<rect x="{SX-14}" y="{SY+6*PX}" width="10" height="6">'
             '<animate attributeName="width" values="6;24;6" dur="0.22s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values="1;0.2;1" dur="0.22s" repeatCount="indefinite"/>'
             f'<animate attributeName="x" values="{SX-14};{SX-38};{SX-14}" dur="0.22s" repeatCount="indefinite"/>'
             '</rect></g>')
    p.append('</g>')

    # dust kick
    p.append('<g fill="#6b7ba8">')
    for i, (dx, dy, d) in enumerate([(-30, -6, 0.5), (-52, -12, 0.7), (-72, -3, 0.6)]):
        p.append(f'<rect x="{SX+10}" y="{SY+13*PX-6}" width="8" height="5" opacity="0.8">'
                 f'<animate attributeName="x" values="{SX+10};{SX+10+dx}" dur="{d}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{SY+13*PX-6};{SY+13*PX-6+dy}" dur="{d}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.8;0" dur="{d}s" repeatCount="indefinite"/></rect>')
    p.append('</g>')

    # HUD
    p.append('<g class="m">'
             '<text x="20" y="26" font-size="13" fill="#00fff7" letter-spacing="2">SCORE 015+ PRs</text>'
             '<text x="220" y="26" font-size="13" fill="#ff2bd1" letter-spacing="2">WORLD 4-1</text>'
             '<text x="392" y="26" font-size="13" fill="#39ff88" letter-spacing="2">B.TECH 2024-2028</text>'
             '<text x="660" y="26" font-size="13" fill="#9fb2e0" letter-spacing="2">LIVES ∞</text>'
             '<text x="800" y="26" font-size="13" fill="#ffd83d" letter-spacing="2">TIME ►►</text>'
             '</g>')

    p.append(f'<rect width="{W}" height="{H}" fill="url(#sl)" pointer-events="none"/>')
    p.append('</svg>')
    return "\n".join(p)


if __name__ == "__main__":
    open("assets/runner.svg", "w").write(build())
    print("wrote assets/runner.svg")
