#!/usr/bin/env python3
"""Draw the built-in "Neon skyline" wallpaper as an SVG.

A city at night in the rain: three layers of towers with lit
windows, neon signs in the Neon Alley colors (made-up glyphs, no
real text), sodium haze on the horizon and a wet street that
reflects it all. The random seed is fixed, so the same image comes
out every time.

Usage: python3 tools/skyline.py src/wallpapers/neon-skyline.svg
"""
import random
import sys

W, H = 1920, 1080
HORIZON = 872
NEON = ["#ff6b1a", "#3de0ff", "#ff3fd2", "#b6ff3b", "#ffc83d", "#4da3ff"]
WARM = ["#ffc83d", "#ffd98a", "#ffe9c2", "#ff9a5c"]
COOL = ["#9fe9ff", "#3de0ff", "#c9d6ff"]
rng = random.Random(2077)

# Windows are collected per color and opacity and drawn as one path
# each, which keeps the file small.
windows = {}


def window(x, y, w, h, color, op):
    key = (color, op)
    windows.setdefault(key, []).append(
        f"M{x:.0f} {y:.0f}h{w:.0f}v{h:.0f}h{-w:.0f}z")


def light_tower(x, y, w, h, cell_w, cell_h, lit, warm_share, layer):
    """Fill a tower with windows: whole floors dark or busy, some
    columns lit as a stripe, so it does not look like a tiled grid."""
    ww, wh = max(2, round(cell_w * 0.5)), max(2, round(cell_h * 0.45))
    cols = max(1, int((w - 8) // cell_w))
    rows = max(1, int((h - 14) // cell_h))
    off_x = x + (w - cols * cell_w) / 2 + (cell_w - ww) / 2
    stripe = rng.randrange(cols) if rng.random() < 0.25 else None
    for r in range(rows):
        floor = rng.random()
        floor_lit = lit * (0.15 if floor < 0.2 else 2.0 if floor > 0.9 else 1)
        for c in range(cols):
            p = 0.85 if c == stripe else floor_lit
            if rng.random() < p:
                pal = WARM if rng.random() < warm_share else COOL
                op = rng.choice(layer)
                window(off_x + c * cell_w, y + 10 + r * cell_h, ww, wh,
                       rng.choice(pal), op)


def towers(x0, x1, h_range, w_range, gap=(-6, 4)):
    out, x = [], x0
    while x < x1:
        w = rng.randint(*w_range)
        out.append((x, w, rng.randint(*h_range)))
        x += w + rng.randint(*gap)
    return out


parts = []
add = parts.append

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'width="{W}" height="{H}" preserveAspectRatio="xMidYMax slice">')
add('<defs>'
    '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#070818"/>'
    '<stop offset="0.4" stop-color="#110f2a"/>'
    '<stop offset="0.66" stop-color="#24133a"/>'
    '<stop offset="0.8" stop-color="#3a1428"/>'
    '<stop offset="0.9" stop-color="#6a2614"/>'
    '<stop offset="1" stop-color="#8a3a10"/></linearGradient>'
    '<radialGradient id="haze" cx="0.5" cy="0.84" r="0.55" '
    'gradientTransform="translate(0 0.32) scale(1 0.62)">'
    '<stop offset="0" stop-color="#ff7a26" stop-opacity="0.5"/>'
    '<stop offset="1" stop-color="#ff7a26" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="hazeC" cx="0.14" cy="0.72" r="0.38">'
    '<stop offset="0" stop-color="#3de0ff" stop-opacity="0.16"/>'
    '<stop offset="1" stop-color="#3de0ff" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="hazeF" cx="0.86" cy="0.7" r="0.38">'
    '<stop offset="0" stop-color="#ff3fd2" stop-opacity="0.16"/>'
    '<stop offset="1" stop-color="#ff3fd2" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#2a1530" stop-opacity="0"/>'
    '<stop offset="1" stop-color="#4a2030" stop-opacity="0.55"/>'
    '</linearGradient>'
    '<linearGradient id="tower" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#030308"/>'
    '<stop offset="1" stop-color="#08070f"/></linearGradient>'
    '<linearGradient id="street" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#120c14"/>'
    '<stop offset="1" stop-color="#030305"/></linearGradient>'
    '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#fff" stop-opacity="0.7"/>'
    '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    f'<mask id="streetMask"><rect x="0" y="{HORIZON}" width="{W}" '
    f'height="{H - HORIZON}" fill="url(#fade)"/></mask>'
    '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="4" result="b"/>'
    '<feGaussianBlur stdDeviation="12" result="c" in="SourceGraphic"/>'
    '<feMerge><feMergeNode in="c"/><feMergeNode in="b"/>'
    '<feMergeNode in="SourceGraphic"/></feMerge></filter>'
    '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%">'
    '<feGaussianBlur stdDeviation="22"/></filter>'
    '<filter id="reflect"><feGaussianBlur stdDeviation="2 16"/></filter>'
    '<pattern id="rain" width="40" height="110" patternUnits="userSpaceOnUse" '
    'patternTransform="rotate(10)">'
    '<line x1="6" y1="0" x2="6" y2="30" stroke="#a9bcff" opacity="0.09"/>'
    '<line x1="27" y1="52" x2="27" y2="74" stroke="#a9bcff" opacity="0.06"/>'
    '</pattern></defs>')

add(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#haze)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#hazeC)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#hazeF)"/>')

city = []
cadd = city.append

# Far layer: low, hazy blocks
for x, w, h in towers(-20, W + 20, (90, 300), (34, 96)):
    y = HORIZON - h
    cadd(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1a1530"/>')
    light_tower(x, y, w, h, 8, 11, 0.16, 0.85, [0.35, 0.5])
cadd(f'<rect x="0" y="{HORIZON - 300}" width="{W}" height="300" '
     'fill="url(#mist)"/>')
city.append("@@WINDOWS@@")      # far windows sit under the mid layer



def mid_layer():
    out = []
    for x, w, h in towers(-30, W + 30, (180, 520), (56, 150)):
        if 560 < x < 1360 and h > 430:
            h = rng.randint(250, 420)   # keep the center lower
        y = HORIZON - h
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                   'fill="#0d0b19"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="2" '
                   'fill="#3de0ff" opacity="0.12"/>')
        light_tower(x, y, w, h, 12, 16, 0.26, 0.7, [0.55, 0.75, 0.9])
        if rng.random() < 0.35:                      # spire with light
            sx, sh = x + w // 2, rng.randint(30, 100)
            out.append(f'<rect x="{sx - 1}" y="{y - sh}" width="3" '
                       f'height="{sh}" fill="#0d0b19"/>')
            out.append(f'<circle cx="{sx}" cy="{y - sh}" r="2.4" '
                       'fill="#ff3b30" filter="url(#glow)"/>')
        elif rng.random() < 0.3:                     # rooftop box
            bw = rng.randint(14, max(15, w // 3))
            out.append(f'<rect x="{x + rng.randint(4, max(5, w - bw - 4))}" '
                       f'y="{y - 12}" width="{bw}" height="12" '
                       'fill="#0d0b19"/>')
    return out


def glyph_sign(sx, sy, sw, sh, color, vertical):
    """A neon sign of made-up glyphs: each glyph is two or three
    strokes on a 3 x 3 grid, so it reads as signage, not as words."""
    g = [f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4" '
         f'fill="#08070e" stroke="{color}" stroke-width="2.5"/>']
    n = max(2, (sh if vertical else sw) // 30)
    size = (sw - 14) if vertical else min(sh - 12, (sw - 14) / n - 6)
    pts = [(i, j) for i in range(3) for j in range(3)]
    strokes = []
    for k in range(n):
        if vertical:
            gx, gy = sx + 7, sy + 8 + k * (sh - 16) / n
        else:
            gx, gy = sx + 8 + k * (sw - 16) / n, sy + (sh - size) / 2
        for _ in range(rng.choice([2, 3, 3])):
            (a, b), (c, d) = rng.sample(pts, 2)
            strokes.append(
                f"M{gx + a * size / 2:.1f} {gy + b * size / 2:.1f}"
                f"L{gx + c * size / 2:.1f} {gy + d * size / 2:.1f}")
    g.append(f'<path d="{"".join(strokes)}" stroke="{color}" '
             'stroke-width="2.6" stroke-linecap="round" fill="none"/>')
    return (f'<g filter="url(#glow)">{"".join(g)}</g>'
            f'<rect x="{sx - 40}" y="{sy - 40}" width="{sw + 80}" '
            f'height="{sh + 80}" fill="{color}" opacity="0.13" '
            'filter="url(#soft)"/>')


def near_layer():
    out, signs, taken = [], [], []
    plan = [(-10, 150, 720), (128, 118, 560), (236, 176, 800),
            (404, 104, 440), (1424, 118, 480), (1534, 168, 780),
            (1694, 106, 600), (1792, 150, 840)]
    for x, w, h in plan:
        y = HORIZON - h
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                   'fill="url(#tower)"/>')
        rim = "#3de0ff" if x < W / 2 else "#ff3fd2"
        edge = x + w - 2 if x < W / 2 else x
        out.append(f'<rect x="{edge}" y="{y}" width="2" height="{h}" '
                   f'fill="{rim}" opacity="0.35"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="2" '
                   f'fill="{rim}" opacity="0.4"/>')
        light_tower(x, y, w, h, 16, 21, 0.14, 0.6, [0.5, 0.7])
        for _ in range(rng.choice([1, 2, 2])):
            color = rng.choice(NEON)
            vertical = rng.random() < 0.55
            if vertical:
                sw, sh = rng.randint(30, 38), rng.randint(130, 240)
                sx = x + (w - 6 if rng.random() < 0.5 else -sw + 6)
            else:
                sw, sh = rng.randint(90, 160), rng.randint(34, 44)
                sx = x + rng.randint(-14, max(-13, w - sw + 14))
            for _try in range(20):
                sy = rng.randint(y + 50, HORIZON - sh - 70)
                box = (sx - 12, sy - 12, sx + sw + 12, sy + sh + 12)
                if not any(box[0] < b[2] and b[0] < box[2] and
                           box[1] < b[3] and b[1] < box[3] for b in taken):
                    taken.append(box)
                    signs.append(glyph_sign(sx, sy, sw, sh, color,
                                            vertical))
                    break
    return out, signs


def win_paths():
    s = "".join(f'<path d="{"".join(d)}" fill="{c}" opacity="{op}"/>'
                for (c, op), d in windows.items())
    windows.clear()
    return s


far_windows = win_paths()
city[city.index("@@WINDOWS@@")] = far_windows
mid = mid_layer()
city.extend(mid)
city.append(win_paths())
near, signs = near_layer()
city.extend(near)
city.append(win_paths())
city.extend(signs)

add('<g id="city">' + "".join(city) + '</g>')

# Wet street: the city mirrored, blurred and fading out
add(f'<rect x="0" y="{HORIZON}" width="{W}" height="{H - HORIZON}" '
    'fill="url(#street)"/>')
add('<g mask="url(#streetMask)"><g filter="url(#reflect)" opacity="0.75">'
    f'<use href="#city" transform="translate(0 {2 * HORIZON}) scale(1 -1)"/>'
    '</g></g>')
for i in range(8):
    add(f'<rect x="0" y="{HORIZON + 10 + i * i * 3.4:.1f}" width="{W}" '
        f'height="1" fill="#ff9a5c" opacity="{0.07 - i * 0.007:.3f}"/>')
add(f'<rect x="0" y="{HORIZON - 1}" width="{W}" height="2" fill="#ff6b1a" '
    'opacity="0.45" filter="url(#glow)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#rain)"/>')
add('</svg>')

svg = "".join(parts)
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Wrote {sys.argv[1]} ({len(svg)} bytes)")
