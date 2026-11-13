#!/usr/bin/env python3
"""Draw the scene wallpapers as SVG files: "Rain alley", "Sodium street",
"Rail line", "Harbor" and "Tunnel".

Two night scenes in the Neon Alley colors, drawn from simple shapes.
Signs carry made-up glyphs, not real text. The random seed is fixed,
so the same images come out every time.

Usage: python3 tools/scenes.py src/wallpapers/
Writes rain-alley.svg, sodium-street.svg, rail-line.svg, harbor.svg and
tunnel.svg into that folder.
"""
import os
import random
import sys

W, H = 1920, 1080
NEON = ["#ff6b1a", "#3de0ff", "#ff3fd2", "#b6ff3b", "#ffc83d", "#4da3ff"]


def defs_common():
    return (
        '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="4" result="b"/>'
        '<feGaussianBlur stdDeviation="12" result="c" in="SourceGraphic"/>'
        '<feMerge><feMergeNode in="c"/><feMergeNode in="b"/>'
        '<feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="24"/></filter>'
        '<filter id="streak"><feGaussianBlur stdDeviation="3 22"/></filter>'
        '<pattern id="rain" width="40" height="110" '
        'patternUnits="userSpaceOnUse" patternTransform="rotate(8)">'
        '<line x1="6" y1="0" x2="6" y2="30" stroke="#a9bcff" opacity="0.10"/>'
        '<line x1="27" y1="52" x2="27" y2="74" stroke="#a9bcff" '
        'opacity="0.07"/></pattern>'
    )


def glyphs(rng, x, y, w, h, color, vertical):
    """Made-up neon glyphs: two or three strokes on a 3 x 3 grid each."""
    n = max(2, int((h if vertical else w) // 30))
    size = (w - 14) if vertical else min(h - 12, (w - 14) / n - 6)
    pts = [(i, j) for i in range(3) for j in range(3)]
    d = []
    for k in range(n):
        gx, gy = ((x + 7, y + 8 + k * (h - 16) / n) if vertical
                  else (x + 8 + k * (w - 16) / n, y + (h - size) / 2))
        for _ in range(rng.choice([2, 3, 3])):
            (a, b), (c, e) = rng.sample(pts, 2)
            d.append(f"M{gx + a * size / 2:.1f} {gy + b * size / 2:.1f}"
                     f"L{gx + c * size / 2:.1f} {gy + e * size / 2:.1f}")
    return (f'<g filter="url(#glow)"><rect x="{x:.1f}" y="{y:.1f}" '
            f'width="{w:.1f}" height="{h:.1f}" rx="4" fill="#08070e" '
            f'stroke="{color}" stroke-width="2.5"/>'
            f'<path d="{"".join(d)}" stroke="{color}" stroke-width="2.6" '
            'stroke-linecap="round" fill="none"/></g>'
            f'<rect x="{x - 50:.1f}" y="{y - 50:.1f}" width="{w + 100:.1f}" '
            f'height="{h + 100:.1f}" fill="{color}" opacity="0.14" '
            'filter="url(#soft)"/>')


def lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------------
def rain_alley():
    """One-point perspective down a narrow alley."""
    rng = random.Random(1984)
    vx, vy = 960, 540                     # vanishing point
    near_l, near_r = -40, W + 40          # wall edges at the viewer
    far_l, far_r = 860, 1060              # wall edges at the alley's end
    top_near, ground = -80, 1120
    top_far, ground_far = 300, 640
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice">')
    p.append('<defs>' + defs_common() +
             '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#0a0a1c"/>'
             '<stop offset="1" stop-color="#3a1630"/></linearGradient>'
             '<radialGradient id="endglow" cx="0.5" cy="0.52" r="0.22">'
             '<stop offset="0" stop-color="#ff7a26" stop-opacity="0.55"/>'
             '<stop offset="1" stop-color="#ff7a26" stop-opacity="0"/>'
             '</radialGradient>'
             '<linearGradient id="wallL" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#05050a"/>'
             '<stop offset="1" stop-color="#12101e"/></linearGradient>'
             '<linearGradient id="wallR" x1="1" y1="0" x2="0" y2="0">'
             '<stop offset="0" stop-color="#05050a"/>'
             '<stop offset="1" stop-color="#12101e"/></linearGradient>'
             '<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#1a1220"/>'
             '<stop offset="1" stop-color="#040406"/></linearGradient>'
             '</defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    # distant street at the end of the alley
    p.append(f'<rect x="{far_l}" y="{top_far}" width="{far_r - far_l}" '
             f'height="{ground_far - top_far}" fill="#2a1424"/>')
    for i in range(14):
        x = far_l + 6 + i * 14
        p.append(f'<rect x="{x}" y="{ground_far - rng.randint(60, 200)}" '
                 f'width="10" height="300" fill="#140d1a"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#endglow)"/>')
    # walls
    p.append(f'<polygon points="{near_l},{top_near} {far_l},{top_far} '
             f'{far_l},{ground_far} {near_l},{ground}" fill="url(#wallL)"/>')
    p.append(f'<polygon points="{near_r},{top_near} {far_r},{top_far} '
             f'{far_r},{ground_far} {near_r},{ground}" fill="url(#wallR)"/>')
    # ground
    p.append(f'<polygon points="{near_l},{ground} {far_l},{ground_far} '
             f'{far_r},{ground_far} {near_r},{ground}" fill="url(#ground)"/>')

    # wall windows and building seams, in perspective
    def wall_point(side, t, h):
        """t: 0 at viewer, 1 at far end; h: 0 ground, 1 top."""
        xn, xf = (near_l, far_l) if side == "L" else (near_r, far_r)
        x = lerp(xn, xf, t)
        yt, yb = lerp(top_near, top_far, t), lerp(ground, ground_far, t)
        return x, lerp(yb, yt, h)

    for side in ("L", "R"):
        for k in range(1, 9):              # building seams
            t = 1 - (0.82 ** k)
            x1, y1 = wall_point(side, t, 1)
            x2, y2 = wall_point(side, t, 0)
            p.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" '
                     f'y2="{y2:.0f}" stroke="#1e1a2c" stroke-width="2"/>')
        # wall edges: roof line and the foot of the wall
        for hh in (1, 0):
            x1, y1 = wall_point(side, 0, hh)
            x2, y2 = wall_point(side, 1, hh)
            col = "#3de0ff" if hh == 1 else "#ff6b1a"
            p.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" '
                     f'y2="{y2:.0f}" stroke="{col}" stroke-width="2" '
                     'opacity="0.25"/>')
        # lit windows in floor rows and bay columns
        floors = [0.3 + 0.075 * i for i in range(9)]
        bays = [0.04 + 0.055 * i for i in range(16)]
        for h in floors:
            for t in bays:
                if rng.random() > 0.22:
                    continue
                dt, dh = 0.022 * (1 - t) + 0.005, 0.03
                pts = [wall_point(side, t, h), wall_point(side, t + dt, h),
                       wall_point(side, t + dt, h - dh), wall_point(side, t, h - dh)]
                col = rng.choice(["#ffc83d", "#ffd98a", "#9fe9ff", "#ff9a5c"])
                op = rng.choice([0.3, 0.45, 0.6])
                p.append('<polygon points="' + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
                         + f'" fill="{col}" opacity="{op}"/>')
        # fire escape rails
        for h in (0.55, 0.78):
            x1, y1 = wall_point(side, 0.0, h)
            x2, y2 = wall_point(side, 0.7, h)
            p.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" '
                     f'y2="{y2:.0f}" stroke="#2a2438" stroke-width="5"/>')

    # neon blade signs sticking out from the walls
    signs = []
    for side, ts in (("L", (0.18, 0.45, 0.7)), ("R", (0.12, 0.38, 0.62))):
        for t in ts:
            x, y = wall_point(side, t, rng.uniform(0.45, 0.7))
            scale = 1 - t * 0.85
            w, h = 44 * scale + 10, 230 * scale + 40
            if side == "R":
                x -= w
            col = rng.choice(NEON)
            signs.append((x, y, w, h, col))
            p.append(glyphs(rng, x, y, w, h, col, True))
    # horizontal sign over the far end
    p.append(glyphs(rng, far_l + 30, top_far + 60, 140, 34, "#ff3fd2", False))

    # overhead cables
    for k in range(6):
        y1 = rng.randint(60, 260)
        y2 = y1 + rng.randint(-40, 60)
        sag = rng.randint(30, 90)
        p.append(f'<path d="M-20 {y1} Q{W / 2} {y1 + sag} {W + 20} {y2}" '
                 'stroke="#0d0b14" stroke-width="3" fill="none"/>')

    # reflections of the signs on the wet ground
    for x, y, w, h, col in signs:
        gy = ground_far + (ground - ground_far) * ((y - top_far) / (ground - top_far)) ** 0.5
        p.append(f'<rect x="{x:.0f}" y="{max(gy, ground_far + 10):.0f}" '
                 f'width="{w:.0f}" height="{h * 1.2:.0f}" fill="{col}" '
                 'opacity="0.22" filter="url(#streak)"/>')
    # puddles and a steam vent
    for _ in range(9):
        cx, cy = rng.randint(500, 1420), rng.randint(760, 1040)
        rx, ry = rng.randint(60, 180), rng.randint(6, 18)
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
                 'fill="#3de0ff" opacity="0.05"/>')
    p.append('<ellipse cx="1240" cy="860" rx="90" ry="200" fill="#c9d6ff" '
             'opacity="0.05" filter="url(#soft)"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#rain)"/>')
    p.append('</svg>')
    return "".join(p)


# ---------------------------------------------------------------------
def sodium_street():
    """A street receding under sodium lamps."""
    rng = random.Random(1999)
    vx, vy = 1180, 600
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice">')
    p.append('<defs>' + defs_common() +
             '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#06060f"/>'
             '<stop offset="0.6" stop-color="#1c1022"/>'
             '<stop offset="1" stop-color="#5a2a12"/></linearGradient>'
             '<radialGradient id="lamp" cx="0.5" cy="0.5" r="0.5">'
             '<stop offset="0" stop-color="#ffb04a" stop-opacity="0.9"/>'
             '<stop offset="0.25" stop-color="#ff8a26" stop-opacity="0.35"/>'
             '<stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/>'
             '</radialGradient>'
             '<linearGradient id="road" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#22140e"/>'
             '<stop offset="1" stop-color="#07060a"/></linearGradient>'
             '</defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    # low buildings along the horizon
    x = -20
    while x < W + 20:
        w = rng.randint(60, 180)
        h = rng.randint(80, 260)
        p.append(f'<rect x="{x}" y="{vy - h}" width="{w}" height="{h + 4}" '
                 'fill="#0c0a14"/>')
        for _ in range(int(w * h / 1400)):
            if rng.random() < 0.35:
                wx = x + rng.randint(4, max(5, w - 12))
                wy = vy - h + rng.randint(8, max(9, h - 16))
                col = rng.choice(["#ffc83d", "#ffd98a", "#ff9a5c", "#9fe9ff"])
                p.append(f'<rect x="{wx}" y="{wy}" width="7" height="9" '
                         f'fill="{col}" opacity="0.6"/>')
        x += w + rng.randint(-4, 10)
    # a neon sign on one building
    p.append(glyphs(rng, 300, vy - 230, 150, 38, "#3de0ff", False))
    p.append(glyphs(rng, 1500, vy - 200, 36, 150, "#ff3fd2", True))
    # road in perspective
    p.append(f'<polygon points="{vx - 40},{vy} {vx + 40},{vy} {W + 400},{H} '
             f'{-500},{H}" fill="url(#road)"/>')
    p.append(f'<polygon points="0,{vy} {vx - 40},{vy} {-500},{H} 0,{H}" '
             'fill="#0b0910"/>')
    p.append(f'<polygon points="{vx + 40},{vy} {W},{vy} {W},{H} {W + 400},{H}" '
             'fill="#0b0910"/>')
    # lane markings
    for k in range(10):
        t1, t2 = (k / 10) ** 2, ((k + 0.45) / 10) ** 2
        y1, y2 = lerp(vy, H, t1), lerp(vy, H, t2)
        w1, w2 = lerp(1, 14, t1), lerp(1, 14, t2)
        p.append(f'<polygon points="{vx - w1:.0f},{y1:.0f} {vx + w1:.0f},{y1:.0f} '
                 f'{vx + w2:.0f},{y2:.0f} {vx - w2:.0f},{y2:.0f}" '
                 'fill="#ffc83d" opacity="0.5"/>')
    # power lines
    for k in range(3):
        y0 = 120 + k * 40
        p.append(f'<path d="M-20 {y0} Q{vx / 2} {y0 + 120} {vx} {vy - 160 + k * 8}" '
                 'stroke="#0a0810" stroke-width="2.5" fill="none"/>')
    # sodium lamps receding along the right kerb
    for k in range(8):
        t = 1 - (0.72 ** k)
        x = lerp(W + 120, vx + 60, t)
        base = lerp(H + 60, vy + 6, t)
        h = lerp(1100, 46, t ** 0.7)
        top = base - h
        arm = lerp(230, 12, t ** 0.7)
        r = lerp(130, 14, t ** 0.7)
        p.append(f'<line x1="{x:.0f}" y1="{base:.0f}" x2="{x:.0f}" y2="{top:.0f}" '
                 f'stroke="#0c0a10" stroke-width="{lerp(14, 2, t):.1f}"/>')
        p.append(f'<line x1="{x:.0f}" y1="{top:.0f}" x2="{x - arm:.0f}" '
                 f'y2="{top + 6:.0f}" stroke="#0c0a10" '
                 f'stroke-width="{lerp(9, 1.5, t):.1f}"/>')
        p.append(f'<circle cx="{x - arm:.0f}" cy="{top + 8:.0f}" r="{r:.0f}" '
                 'fill="url(#lamp)"/>')
        # pool of light on the road
        p.append(f'<ellipse cx="{x - arm:.0f}" cy="{lerp(base, base, 0) - 4:.0f}" '
                 f'rx="{r * 2.2:.0f}" ry="{r * 0.35:.0f}" fill="#ff8a26" '
                 'opacity="0.22" filter="url(#soft)"/>')
    # a traffic cone in the foreground, in the theme's cone orange
    cx, cy = 420, 1000
    p.append(f'<polygon points="{cx - 60},{cy} {cx + 60},{cy} {cx + 16},{cy - 170} '
             f'{cx - 16},{cy - 170}" fill="#ff6b1a"/>')
    p.append(f'<polygon points="{cx - 40},{cy - 60} {cx + 40},{cy - 60} '
             f'{cx + 30},{cy - 95} {cx - 30},{cy - 95}" fill="#f2efe6" opacity="0.9"/>')
    p.append(f'<rect x="{cx - 85}" y="{cy - 6}" width="170" height="16" rx="3" '
             'fill="#c4500f"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy + 14}" rx="140" ry="16" fill="#ff6b1a" '
             'opacity="0.18" filter="url(#soft)"/>')
    # haze
    p.append(f'<rect x="0" y="{vy - 140}" width="{W}" height="220" fill="#ff7a1a" '
             'opacity="0.10" filter="url(#soft)"/>')
    p.append('</svg>')
    return "".join(p)


# ---------------------------------------------------------------------
def _head(sky_top, sky_bottom, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" preserveAspectRatio="xMidYMax slice">'
            '<defs>' + defs_common() +
            '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{sky_top}"/>'
            f'<stop offset="1" stop-color="{sky_bottom}"/></linearGradient>'
            + extra + '</defs>'
            f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')


def _windows(rng, boxes, colors, share):
    """Lit windows for a list of (x, y, w, h) buildings, one path per color."""
    paths = {c: [] for c in colors}
    for x, y, w, h in boxes:
        for wy in range(int(y) + 12, int(y + h) - 10, 16):
            for wx in range(int(x) + 6, int(x + w) - 8, 12):
                if rng.random() < share:
                    paths[rng.choice(colors)].append(f"M{wx} {wy}h5v7h-5z")
    return "".join(f'<path d="{"".join(d)}" fill="{c}" opacity="0.55"/>'
                   for c, d in paths.items() if d)


def rail_line():
    """An elevated rail line crossing a green-lit district."""
    rng = random.Random(2077)
    green = ["#b6ff3b", "#3dff9a", "#2fd6c3"]
    p = [_head("#050b08", "#12301f",
               '<radialGradient id="haze" cx="0.5" cy="0.75" r="0.6">'
               '<stop offset="0" stop-color="#3dff9a" stop-opacity="0.22"/>'
               '<stop offset="1" stop-color="#3dff9a" stop-opacity="0"/>'
               '</radialGradient>')]
    p.append(f'<rect width="{W}" height="{H}" fill="url(#haze)"/>')
    # far skyline
    far = []
    x = -20
    while x < W:
        w, h = rng.randint(50, 120), rng.randint(160, 420)
        far.append((x, 760 - h, w, h)); x += w + rng.randint(2, 10)
    p.append('<path d="' + "".join(f"M{x} {y}h{w}v{h}h{-w}z" for x, y, w, h in far)
             + '" fill="#08140e"/>')
    p.append(_windows(rng, far, ["#3dff9a", "#b6ff3b", "#c8ffd8"], 0.07))
    # the elevated track: deck, rails and pillars
    p.append(f'<rect x="0" y="560" width="{W}" height="34" fill="#0a120d"/>')
    p.append(f'<rect x="0" y="556" width="{W}" height="4" fill="#3dff9a" opacity="0.5" filter="url(#glow)"/>')
    p.append('<path d="' + "".join(f"M{x} 594h28v{H - 594}h-28z" for x in range(60, W, 300))
             + '" fill="#07100b"/>')
    # a passing train with lit windows
    p.append('<rect x="420" y="508" width="900" height="50" rx="6" fill="#0d1a13"/>')
    p.append('<path d="' + "".join(f"M{x} 520h40v18h-40z" for x in range(440, 1300, 58))
             + '" fill="#c8ffd8" opacity="0.7"/>')
    p.append('<rect x="420" y="500" width="900" height="70" fill="#3dff9a" opacity="0.10" filter="url(#soft)"/>')
    # neon signs under the track and on the buildings
    signs = [(140, 300, 46, 180, green[0], True), (1700, 260, 46, 200, green[2], True),
             (760, 640, 220, 40, green[1], False), (1180, 340, 160, 36, green[0], False)]
    for x, y, w, h, c, v in signs:
        p.append(glyphs(rng, x, y, w, h, c, v))
    # wet street and reflections
    p.append(f'<rect x="0" y="758" width="{W}" height="{H - 758}" fill="#040806" opacity="0.9"/>')
    for x, y, w, h, c, v in signs:
        p.append(f'<rect x="{x}" y="780" width="{w}" height="{h * 1.1:.0f}" fill="{c}" '
                 'opacity="0.18" filter="url(#streak)"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#rain)"/>')
    p.append('</svg>')
    return "".join(p)


def harbor():
    """Cranes and container stacks over cold harbor water."""
    rng = random.Random(1999)
    ice = ["#4da3ff", "#9fe9ff", "#c9d6ff"]
    p = [_head("#04070f", "#10233a",
               '<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">'
               '<stop offset="0" stop-color="#0b1a2c"/>'
               '<stop offset="1" stop-color="#03060c"/></linearGradient>')]
    horizon = 700
    # container stacks along the quay
    boxes = []
    x = 0
    while x < W:
        w = rng.randint(70, 140); rows = rng.randint(2, 5)
        for r in range(rows):
            boxes.append((x, horizon - 30 * (r + 1), w, 28,
                          rng.choice(["#16263f", "#1c3050", "#1a2a44", "#223a5e"])))
        x += w + rng.randint(4, 30)
    for c in sorted({b[4] for b in boxes}):
        p.append('<path d="' + "".join(f"M{x} {y}h{w}v{h}h{-w}z" for x, y, w, h, cc in boxes if cc == c)
                 + f'" fill="{c}"/>')
    # gantry cranes
    for cx in (260, 980, 1560):
        h = rng.randint(330, 420)
        p.append(f'<path d="M{cx} {horizon}V{horizon - h}M{cx + 90} {horizon}V{horizon - h}'
                 f'M{cx - 160} {horizon - h}H{cx + 300}M{cx} {horizon - h + 60}L{cx + 90} {horizon - h}'
                 f'M{cx + 90} {horizon - h + 60}L{cx} {horizon - h}" stroke="#24385a" '
                 'stroke-width="12" fill="none"/>')
        p.append(f'<circle cx="{cx + 300}" cy="{horizon - h}" r="5" fill="#ff3b30" filter="url(#glow)"/>')
        p.append(f'<rect x="{cx - 160}" y="{horizon - h - 3}" width="460" height="3" fill="{ice[1]}" opacity="0.6" filter="url(#glow)"/>')
    # quay lights
    for x in range(40, W, 110):
        p.append(f'<circle cx="{x}" cy="{horizon - 4}" r="3" fill="{rng.choice(ice)}" filter="url(#glow)"/>')
    # signs on the warehouse
    for x, y, w, h, c, v in [(620, 470, 180, 36, ice[0], False), (1320, 430, 46, 190, ice[1], True), (90, 440, 46, 170, ice[2], True)]:
        p.append(glyphs(rng, x, y, w, h, c, v))
    # water with light streaks
    p.append(f'<rect x="0" y="{horizon}" width="{W}" height="{H - horizon}" fill="url(#water)"/>')
    for x in range(40, W, 110):
        p.append(f'<rect x="{x - 3}" y="{horizon + 6}" width="6" height="{rng.randint(120, 260)}" '
                 f'fill="{rng.choice(ice)}" opacity="0.25" filter="url(#streak)"/>')
    p.append('<path d="' + "".join(f"M{rng.randint(0, W)} {rng.randint(horizon + 20, H)}h{rng.randint(40, 160)}"
                                   for _ in range(40)) + '" stroke="#9fe9ff" stroke-width="1.5" opacity="0.12"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#rain)"/>')
    p.append('</svg>')
    return "".join(p)


def tunnel():
    """A road tunnel full of brake lights."""
    rng = random.Random(1982)
    vx, vy = 960, 560
    p = [_head("#0a0405", "#1c0709",
               '<radialGradient id="mouth" cx="0.5" cy="0.52" r="0.3">'
               '<stop offset="0" stop-color="#ff3344" stop-opacity="0.35"/>'
               '<stop offset="1" stop-color="#ff3344" stop-opacity="0"/>'
               '</radialGradient>')]
    # tunnel walls as rings receding to the vanishing point
    for k in range(10):
        t = 0.8 ** k
        w, h = 1100 * t + 120, 760 * t + 80
        op = 0.08 + 0.05 * (1 - t)
        p.append(f'<rect x="{vx - w / 2:.0f}" y="{vy - h * 0.62:.0f}" width="{w:.0f}" height="{h:.0f}" '
                 f'rx="{w * 0.18:.0f}" fill="none" stroke="#ff3344" stroke-width="{3 * t + 1:.1f}" opacity="{op:.2f}"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#mouth)"/>')
    # road
    p.append(f'<polygon points="{vx - 60},{vy + 40} {vx + 60},{vy + 40} {W + 200},{H} -200,{H}" fill="#0d0607"/>')
    p.append(f'<path d="M{vx} {vy + 50}L{vx} {H}" stroke="#ffc83d" stroke-width="4" stroke-dasharray="40 50" opacity="0.5"/>')
    # ceiling strip lights
    for k in range(14):
        t = 0.82 ** k
        y = vy - 470 * t
        p.append(f'<rect x="{vx - 160 * t - 8:.0f}" y="{y:.0f}" width="{320 * t + 16:.0f}" height="{6 * t + 2:.1f}" '
                 'fill="#ffd9d9" opacity="0.5" filter="url(#glow)"/>')
    # brake lights in pairs, receding
    lights = []
    for k in range(9):
        t = 0.78 ** k
        for lane in (-1, 1):
            cx = vx + lane * 260 * t + rng.uniform(-10, 10) * t
            cy = vy + 360 * t + 30
            sep, r = 70 * t + 6, 7 * t + 2
            lights.append((cx - sep, cy, r)); lights.append((cx + sep, cy, r))
    p.append('<g fill="#ff2a3a" filter="url(#glow)">' + "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}"/>' for x, y, r in lights) + '</g>')
    # streaks of the lights on the wet road
    p.append('<g fill="#ff2a3a" opacity="0.2" filter="url(#streak)">' + "".join(
        f'<rect x="{x - r:.0f}" y="{y + 10:.0f}" width="{2 * r:.0f}" height="{8 * r + 20:.0f}"/>'
        for x, y, r in lights) + '</g>')
    # neon signs on the walls
    for x, y, w, h, c, v in [(150, 280, 50, 230, "#ff3344", True), (1720, 300, 50, 210, "#ff6b1a", True), (840, 230, 240, 40, "#ff3344", False)]:
        p.append(glyphs(rng, x, y, w, h, c, v))
    p.append('</svg>')
    return "".join(p)


def main(out):
    os.makedirs(out, exist_ok=True)
    for name, fn in (("rain-alley", rain_alley), ("sodium-street", sodium_street),
                     ("rail-line", rail_line), ("harbor", harbor), ("tunnel", tunnel)):
        path = os.path.join(out, f"{name}.svg")
        svg = fn()
        with open(path, "w") as f:
            f.write(svg)
        print(f"Wrote {path} ({len(svg)} bytes)")


if __name__ == "__main__":
    main(sys.argv[1])
