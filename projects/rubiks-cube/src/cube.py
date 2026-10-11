"""Tiny Rubik's cube simulator (sticker model) + SVG renderer."""
import math

# Orientation used throughout the guide: Yellow up, White down, Blue front, Red right
FACE_N = {'U': (0, 1, 0), 'D': (0, -1, 0), 'R': (1, 0, 0), 'L': (-1, 0, 0), 'F': (0, 0, 1), 'B': (0, 0, -1)}
FACE_COLOR = {'U': 'Y', 'D': 'W', 'F': 'B', 'R': 'R', 'L': 'O', 'B': 'G'}
HEX = {'Y': '#FFD200', 'W': '#FFFFFF', 'B': '#1565D8', 'R': '#D7263D', 'O': '#FF7A00', 'G': '#16A34A',
       'X': '#A9AEB6'}


def add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def rot_cw(v, n):
    """Rotate v by 90 degrees clockwise as seen looking at the face with outward normal n."""
    c = cross(n, v)
    return add(mul(c, -1), mul(n, dot(n, v)))


def solved():
    st = {}
    for f, n in FACE_N.items():
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                # pos: cubie position; key is (pos, normal)
                if n[0]:
                    pos = (n[0], a, b)
                elif n[1]:
                    pos = (a, n[1], b)
                else:
                    pos = (a, b, n[2])
                st[(pos, n)] = FACE_COLOR[f]
    return st


def parse(alg):
    out = []
    for tok in alg.split():
        f = tok[0]
        if tok.endswith("2"):
            out += [f, f]
        elif tok.endswith("'"):
            out += [f, f, f]
        else:
            out += [f]
    return out


MOVE_DEF = {}
for _f, _n in FACE_N.items():
    MOVE_DEF[_f] = (_n, lambda p, n=_n: dot(p, n) == 1)
    MOVE_DEF[_f.lower()] = (_n, lambda p, n=_n: dot(p, n) >= 0)
MOVE_DEF['M'] = ((-1, 0, 0), lambda p: p[0] == 0)
MOVE_DEF['E'] = ((0, -1, 0), lambda p: p[1] == 0)
MOVE_DEF['S'] = ((0, 0, 1), lambda p: p[2] == 0)


def move(st, alg):
    for f in parse(alg):
        n, pred = MOVE_DEF[f]
        new = {}
        for (pos, nrm), col in st.items():
            if pred(pos):
                new[(rot_cw(pos, n), rot_cw(nrm, n))] = col
            else:
                new[(pos, nrm)] = col
        st = new
    return st


def invert(alg):
    out = []
    for tok in reversed(alg.split()):
        if tok.endswith("2"):
            out.append(tok)
        elif tok.endswith("'"):
            out.append(tok[0])
        else:
            out.append(tok + "'")
    return " ".join(out)


def sticker(st, pos, face):
    return st[(pos, FACE_N[face])]


def is_solved(st):
    return st == solved()


# ---------------------------------------------------------------- rendering
VIEWS = {
    'top': (0.62, 0.78, 1.0),       # see U, F, R
    'bottom': (0.62, -0.78, 1.0),   # see D, F, R
}


def camera(vdir):
    l = math.sqrt(dot(vdir, vdir))
    v = mul(vdir, 1 / l)
    up = (0, 1, 0)
    r = cross(up, v)
    rl = math.sqrt(dot(r, r))
    r = mul(r, 1 / rl)
    u = cross(v, r)
    return v, r, u


def proj(p, cam, scale, ox, oy):
    v, r, u = cam
    return (ox + dot(p, r) * scale, oy - dot(p, u) * scale)


def tangents(n):
    if n[0]:
        return (0, 1, 0), (0, 0, 1)
    if n[1]:
        return (1, 0, 0), (0, 0, 1)
    return (1, 0, 0), (0, 1, 0)


def lighten(hexcol, amt):
    h = hexcol.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * amt); g = int(g + (255 - g) * amt); b = int(b + (255 - b) * amt)
    return '#%02x%02x%02x' % (r, g, b)


def svg_cube(st, view='top', size=180, colors=None, dim=None, arrows=(), extra='', label=None,
             label_size=None):
    """colors: optional dict key->color letter override (e.g. 'X' for gray).
    dim: optional predicate(pos, normal) -> True if sticker should be faded.
    arrows: list of dicts {pts:[3d points], head:True}"""
    cam = camera(VIEWS[view])
    v = cam[0]
    scale = size / 5.3
    ox, oy = size / 2, size / 2
    parts = []
    # cube body faces
    for f, n in FACE_N.items():
        if dot(n, v) <= 0:
            continue
        t1, t2 = tangents(n)
        c = mul(n, 1.5)
        corners = [add(add(c, mul(t1, s1 * 1.5)), mul(t2, s2 * 1.5)) for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        pts = " ".join("%.2f,%.2f" % proj(p, cam, scale, ox, oy) for p in corners)
        parts.append('<polygon points="%s" fill="#1d1d1f" stroke="#1d1d1f" stroke-width="%.1f" stroke-linejoin="round"/>' % (pts, scale * 0.12))
    for (pos, n), col in st.items():
        if dot(n, v) <= 0:
            continue
        if colors and (pos, n) in colors:
            col = colors[(pos, n)]
        fill = HEX[col]
        if dim and dim(pos, n):
            fill = lighten(fill, 0.72)
        t1, t2 = tangents(n)
        c = add(pos, mul(n, 0.5))
        a = 0.41
        corners = [add(add(c, mul(t1, s1 * a)), mul(t2, s2 * a)) for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        pts = " ".join("%.2f,%.2f" % proj(p, cam, scale, ox, oy) for p in corners)
        parts.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%.1f" stroke-linejoin="round"/>' % (pts, fill, fill, scale * 0.08))
    for ar in arrows:
        parts.append(svg_arrow(ar, cam, scale, ox, oy))
    if extra:
        parts.append(extra)
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>' % (size, size, size, size, "".join(parts))


def svg_arrow(ar, cam, scale, ox, oy):
    pts2 = [proj(p, cam, scale, ox, oy) for p in ar['pts']]
    color = ar.get('color', '#111')
    w = ar.get('width', scale * 0.30)
    # shorten end for the head
    (x1, y1), (x2, y2) = pts2[-2], pts2[-1]
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    hl = w * 2.3
    hw = w * 1.75
    base = (x2 - ux * hl * 0.85, y2 - uy * hl * 0.85)
    body = pts2[:-1] + [base]
    d = "M " + " L ".join("%.2f %.2f" % p for p in body)
    tip = (x2, y2)
    b = (x2 - ux * hl, y2 - uy * hl)
    l = (b[0] - uy * hw, b[1] + ux * hw)
    r = (b[0] + uy * hw, b[1] - ux * hw)
    head = "%.2f,%.2f %.2f,%.2f %.2f,%.2f" % (tip[0], tip[1], l[0], l[1], r[0], r[1])
    out = []
    out.append('<path d="%s" fill="none" stroke="#fff" stroke-width="%.2f" stroke-linecap="round" stroke-linejoin="round"/>' % (d, w + scale * 0.22))
    out.append('<polygon points="%s" fill="#fff" stroke="#fff" stroke-width="%.2f" stroke-linejoin="round"/>' % (head, scale * 0.22))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" stroke-linejoin="round"/>' % (d, color, w))
    out.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1" stroke-linejoin="round"/>' % (head, color, color))
    return "".join(out)


# ---------------------------------------------------------------- flat top view (net around U)
def svg_top_net(st, size=170, gray_fn=None, rows=2, mark=None):
    """U face 3x3 in the middle; each side face's top row (and middle row if rows=2) folded out.
    gray_fn(pos, n) -> True to gray the sticker. mark: set of (pos, face) to outline."""
    cell = size / (3 + 2 * rows + 0.6)
    gap = cell * 0.08
    off = rows * cell + cell * 0.3
    parts = []

    def rect(x, y, w, h, col, key=None):
        fill = HEX[col]
        parts.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s" stroke="#1d1d1f" stroke-width="%.2f"/>' % (x + gap, y + gap, w - 2 * gap, h - 2 * gap, cell * 0.14, fill, cell * 0.07))

    def col_of(pos, face):
        n = FACE_N[face]
        c = st[(pos, n)]
        if gray_fn and gray_fn(pos, n):
            return 'X'
        return c

    # U face: x from -1..1 left->right, z from -1 (back, top of picture) to 1 (front, bottom)
    parts.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="#1d1d1f"/>' % (off - cell * 0.06, off - cell * 0.06, 3 * cell + cell * 0.12, 3 * cell + cell * 0.12, cell * 0.2))
    for xi, x in enumerate((-1, 0, 1)):
        for zi, z in enumerate((-1, 0, 1)):
            rect(off + xi * cell, off + zi * cell, cell, cell, col_of((x, 1, z), 'U'))
    for r in range(rows):
        y = 1 - r
        # Front: below U, row r further down
        for xi, x in enumerate((-1, 0, 1)):
            rect(off + xi * cell, off + 3 * cell + r * cell + cell * 0.12, cell, cell * 0.92, col_of((x, y, 1), 'F'))
        # Back: above U, mirrored x
        for xi, x in enumerate((-1, 0, 1)):
            rect(off + xi * cell, off - (r + 1) * cell - cell * 0.12, cell, cell * 0.92, col_of((x, y, -1), 'B'))
        # Left: to the left of U, z goes top->bottom
        for zi, z in enumerate((-1, 0, 1)):
            rect(off - (r + 1) * cell - cell * 0.12, off + zi * cell, cell * 0.92, cell, col_of((-1, y, z), 'L'))
        # Right
        for zi, z in enumerate((-1, 0, 1)):
            rect(off + 3 * cell + r * cell + cell * 0.12, off + zi * cell, cell * 0.92, cell, col_of((1, y, z), 'R'))
    total = off * 2 + 3 * cell
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" width="%d" height="%d">%s</svg>' % (total, total, size, size, "".join(parts))
