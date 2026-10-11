import math
from cube import *

S = solved()


def is_center(p): return sum(1 for c in p if c) == 1
def is_edge(p): return sum(1 for c in p if c) == 2
def is_corner(p): return sum(1 for c in p if c) == 3


def masked(st, keep):
    return {k: 'X' for k, v in st.items() if not keep(k[0], k[1], v)}


def paint(st, changes):
    st = dict(st)
    for (pos, face), col in changes.items():
        st[(pos, FACE_N[face])] = col
    return st


# ----------------------------------------------------------- arrows (3D points)
def line(a, b, n=2):
    return [tuple(a[i] + (b[i] - a[i]) * t / (n - 1) for i in range(3)) for t in range(n)]


def arc_front(a0, a1, r=1.02, z=1.53, steps=28):
    pts = []
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((r * math.cos(a), r * math.sin(a), z))
    return pts


Z = 1.53
ARROWS = {
    'R': line((1, -1.15, Z), (1, 1.2, Z)),
    "R'": line((1, 1.15, Z), (1, -1.2, Z)),
    'L': line((-1, 1.15, Z), (-1, -1.2, Z)),
    "L'": line((-1, -1.15, Z), (-1, 1.2, Z)),
    'U': line((1.15, 1, Z), (-1.2, 1, Z)),
    "U'": line((-1.15, 1, Z), (1.2, 1, Z)),
    'D': line((-1.15, -1, Z), (1.2, -1, Z)),
    "D'": line((1.15, -1, Z), (-1.2, -1, Z)),
    'F': arc_front(155, -120),
    "F'": arc_front(25, 300),
    'B': line((1.15, Z, -1), (-1.2, Z, -1)),
    "B'": line((-1.15, Z, -1), (1.2, Z, -1)),
}
ARROWS['U2'] = ARROWS['U']
ARROWS['F2'] = ARROWS['F']
ARROWS['R2'] = ARROWS['R']


def layer_of(m):
    return FACE_N[m[0]]


def move_icon(m, size=70, view='top'):
    n = layer_of(m)
    dim = lambda pos, nrm: dot(pos, n) != 1
    badge = ''
    if m.endswith('2'):
        s = size
        badge = ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#111"/>'
                 '<text x="%.1f" y="%.1f" font-family="Inter" font-weight="800" font-size="%.1f" fill="#fff" text-anchor="middle">2×</text>'
                 % (s * 0.85, s * 0.14, s * 0.14, s * 0.85, s * 0.14 + s * 0.055, s * 0.14))
    w = None
    return svg_cube(S, view, size, dim=dim, arrows=[{'pts': ARROWS[m]}], extra=badge)


def ring(points3d, view='top', size=180, color='#E11D8A', r=1.3):
    cam = camera(VIEWS[view])
    scale = size / 5.3
    out = []
    for p in points3d:
        x, y = proj(p, cam, scale, size / 2, size / 2)
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#fff" stroke-width="%.1f"/>' % (x, y, scale * r, scale * 0.30))
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%.1f" stroke-dasharray="%.1f %.1f"/>' % (x, y, scale * r, color, scale * 0.15, scale * 0.3, scale * 0.16))
    return "".join(out)


CAPTION = {
    'R': 'rechte Seite<br>nach oben', "R'": 'rechte Seite<br>nach unten',
    'L': 'linke Seite<br>nach unten', "L'": 'linke Seite<br>nach oben',
    'U': 'obere Schicht<br>nach links', "U'": 'obere Schicht<br>nach rechts',
    'D': 'untere Schicht<br>nach rechts', "D'": 'untere Schicht<br>nach links',
    'F': 'vordere Seite<br>im Uhrzeigersinn', "F'": 'vordere Seite<br>gegen Uhrzeigersinn',
    'B': 'hintere Seite:<br>oben läuft nach links', "B'": 'hintere Seite:<br>oben läuft nach rechts',
    'U2': 'obere Schicht<br>2× drehen', 'F2': 'vordere Seite<br>2× drehen',
}


def fmt(m):
    return m.replace("'", "<span class='str'>'</span>")


def strip(alg, size=62, cls=''):
    items = []
    for i, m in enumerate(alg.split()):
        items.append('<div class="mv"><div class="mvnum">%d</div>%s<b>%s</b></div>' % (i + 1, move_icon(m, size), fmt(m)))
    return '<div class="strip %s">%s</div>' % (cls, "".join(items))


def mvbox(m, size=62):
    return '<div class="mv">%s<b>%s</b></div>' % (move_icon(m, size), fmt(m))


def alg_text(alg):
    return '<span class="algtxt">%s</span>' % " ".join(fmt(m) for m in alg.split())


# ----------------------------------------------------------- states & images
X_TWIST = " ".join(["R' D' R D"] * 2) + " U " + " ".join(["R' D' R D"] * 4) + " U'"
SEXY = "R U R' U'"
RIGHT = "U R U' R' U' F' U F"
LEFT = "U' L' U L U F U' F'"
OLL = "F R U R' U' F'"
SUNE = "R U R' U R U2 R' U"
NIKLAS = "U R U' L' U R' U' L"
TWIST = "R' D' R D"

# goal images
def goal(i, size=86):
    if i == 1:
        st = move(S, "F2 R2 B2 L2 U")
        c = masked(st, lambda p, n, v: is_center(p) or (p[1] == 1 and is_edge(p) and n == (0, 1, 0) and v == 'W'))
        return svg_cube(st, 'top', size, colors=c)
    if i == 2:
        return svg_cube(S, 'bottom', size, colors=masked(S, lambda p, n, v: is_center(p) or (p[1] == -1 and is_edge(p))))
    if i == 3:
        return svg_cube(S, 'bottom', size, colors=masked(S, lambda p, n, v: is_center(p) or p[1] == -1))
    if i == 4:
        return svg_cube(S, 'top', size, colors=masked(S, lambda p, n, v: is_center(p) or p[1] <= 0))
    if i == 5:
        return svg_cube(S, 'top', size, colors=masked(S, lambda p, n, v: is_center(p) or p[1] <= 0 or (p[1] == 1 and is_edge(p) and n == (0, 1, 0))))
    if i == 6:
        return svg_cube(S, 'top', size, colors=masked(S, lambda p, n, v: is_center(p) or p[1] <= 0 or (p[1] == 1 and is_edge(p))))
    if i == 7:
        return svg_cube(move(S, X_TWIST), 'top', size)
    if i == 8:
        return svg_cube(S, 'top', size)


STEP_NAMES = ['Gänseblümchen', 'Weißes Kreuz', 'Weiße Ecken', 'Mittlere Schicht', 'Gelbes Kreuz',
              'Gelbe Kanten', 'Gelbe Ecken an ihren Platz', 'Gelbe Ecken drehen']
STEP_COLORS = ['#16A34A', '#1565D8', '#D7263D', '#FF7A00', '#E0A800', '#16A34A', '#1565D8', '#D7263D']


def top_grid(pattern, size=120):
    """Yellow-cross shapes: U face only, pattern = set of edge letters with yellow."""
    E = {'B': (0, 1, -1), 'L': (-1, 1, 0), 'R': (1, 1, 0), 'F': (0, 1, 1)}
    ch = {}
    for x in (-1, 0, 1):
        for z in (-1, 0, 1):
            ch[((x, 1, z), 'U')] = 'X'
    ch[((0, 1, 0), 'U')] = 'Y'
    for k in pattern:
        ch[(E[k], 'U')] = 'Y'
    return svg_top_net(paint(S, ch), size=size, rows=0)


def edge_net(edge_cols, size=190):
    """edge_cols: dict side->color letter shown on the top-row edge sticker of that side."""
    ch = {}
    for x in (-1, 1):
        for z in (-1, 1):
            p = (x, 1, z)
            for f in 'UFRBL':
                if (p, FACE_N[f]) in S:
                    ch[(p, f)] = 'X'
    pos = {'F': (0, 1, 1), 'R': (1, 1, 0), 'B': (0, 1, -1), 'L': (-1, 1, 0)}
    for side, col in edge_cols.items():
        ch[(pos[side], side)] = col
    return svg_top_net(paint(S, ch), size=size, rows=2)


def netwrap(svg):
    return '<div class="netwrap"><span class="nlab nt">hinten</span><span class="nlab nb">vorne</span><span class="nlab nl2">links</span><span class="nlab nr">rechts</span>%s</div>' % svg


def page_head(i, subtitle):
    return '''<div class="stephead" style="--c:%s">
  <div class="num">%d</div>
  <div class="ht"><div class="kicker">Schritt %d von 8</div><h1>%s</h1><div class="sub">%s</div></div>
  <div class="goal">%s<span>So sieht es danach aus</span></div>
</div>''' % (STEP_COLORS[i - 1], i, i, STEP_NAMES[i - 1], subtitle, goal(i, 96))


pages = []

# ======================================================================= COVER
overview = "".join('<div class="ov"><div class="ovn" style="background:%s">%d</div>%s<span>%s</span></div>' % (STEP_COLORS[i - 1], i, goal(i, 118), STEP_NAMES[i - 1]) for i in range(1, 9))
scr = move(S, "R U2 F' L D' B2 R' U F2 L' U' B")
pages.append('''<section class="page cover">
  <div class="covertop">
    <div class="covertext">
      <div class="eyebrow">Schicht für Schicht</div>
      <h1 class="title">Den Zauberwürfel<br>lösen</h1>
      <p class="tag">Eine Anleitung mit Bildern. Schritt für Schritt, Zug für Zug. Bis dein Würfel wieder ganz bunt sortiert ist.</p>
      <div class="owner">Dieser Würfel-Plan gehört: <span class="blank"></span></div>
      <div class="owner">Meine Bestzeit: <span class="blank short"></span></div>
    </div>
    <div class="coverpics"><div class="cp1">%s</div><div class="cparrow">➜</div><div class="cp2">%s</div></div>
  </div>
  <h2 class="ovh">Dein Weg in 8 Schritten</h2>
  <div class="overview">%s</div>
  <div class="golden"><b>Die goldene Regel:</b> Gelb ist oben, Weiß ist unten. Die ganze Anleitung lang! So musst du nie überlegen, wie du den Würfel hältst.</div>
</section>''' % (svg_cube(scr, 'top', 200), svg_cube(S, 'top', 200), overview))

# ======================================================================= PIECES
only = lambda f: masked(S, lambda p, n, v: f(p))
pages.append('''<section class="page">
  <h1 class="ptitle">Lerne deinen Würfel kennen</h1>
  <p class="lead">Dein Würfel hat drei Sorten von Steinen. Wenn du sie kennst, ist alles viel leichter.</p>
  <div class="pieces">
    <div class="piece">%s<h3>Mittelsteine</h3><p><b>1 Farbe.</b> Sie bewegen sich nie! Der Mittelstein sagt dir, welche Farbe diese Seite am Ende hat.</p></div>
    <div class="piece">%s<h3>Kanten</h3><p><b>2 Farben.</b> Sie sitzen zwischen zwei Mittelsteinen. Es gibt 12 Kanten.</p></div>
    <div class="piece">%s<h3>Ecken</h3><p><b>3 Farben.</b> Sie sitzen an den Ecken. Es gibt 8 Ecken.</p></div>
  </div>
  <div class="twocol">
    <div class="box">
      <h3>Gegenüber-Farben</h3>
      <p>Bei den meisten Würfeln liegen diese Farben gegenüber:</p>
      <div class="pairs">
        <div><span class="sw" style="background:#fff"></span><span class="sw" style="background:#FFD200"></span> Weiß und Gelb</div>
        <div><span class="sw" style="background:#1565D8"></span><span class="sw" style="background:#16A34A"></span> Blau und Grün</div>
        <div><span class="sw" style="background:#D7263D"></span><span class="sw" style="background:#FF7A00"></span> Rot und Orange</div>
      </div>
    </div>
    <div class="box">
      <h3>So hältst du den Würfel</h3>
      <p><b>Gelb oben, Weiß unten.</b> Die Seite, die dich anschaut, heißt <b>vorne</b>.</p>
      <p>Du darfst den Würfel zwischendurch in der Hand drehen, damit eine andere Seite vorne ist. Aber nie mitten in einem Zauberspruch!</p>
    </div>
  </div>
  <div class="twocol">
    <div class="box gray">
      <div class="legend"><span class="sw big" style="background:#A9AEB6"></span><div><h3>Grau heißt: egal</h3><p>In den Bildern sind manche Felder grau. Diese Farbe ist an der Stelle gerade unwichtig. Schau einfach nicht hin.</p></div></div>
    </div>
    <div class="box gray">
      <div class="legend"><span class="sw big ring"></span><div><h3>Pinker Kreis: hier schauen</h3><p>Der gestrichelte Kreis zeigt dir, um welchen Stein es gerade geht.</p></div></div>
    </div>
  </div>
  <div class="note">Dein Würfel hat die Farben vielleicht anders verteilt als die Bilder hier. Das macht nichts. Wichtig ist nur: Jeder Stein muss am Ende zu den Mittelsteinen passen.</div>
</section>''' % (svg_cube(S, 'top', 185, colors=only(lambda p: is_center(p))),
                  svg_cube(S, 'top', 185, colors=only(lambda p: is_edge(p))),
                  svg_cube(S, 'top', 185, colors=only(lambda p: is_corner(p)))))

# ======================================================================= NOTATION
cells = []
for m in ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'"]:
    cells.append('<div class="nc">%s<div class="nl">%s</div><div class="ncap">%s</div></div>' % (move_icon(m, 116), fmt(m), CAPTION[m]))
pages.append('''<section class="page">
  <h1 class="ptitle">Die Würfel-Sprache</h1>
  <p class="lead">Würfel-Profis auf der ganzen Welt schreiben Drehungen mit Buchstaben auf. Die Buchstaben kommen aus dem Englischen. Jeder Buchstabe ist eine Seite.</p>
  <div class="lettertable">
    <div><b>R</b><span>Right</span><i>rechts</i></div>
    <div><b>L</b><span>Left</span><i>links</i></div>
    <div class="warn"><b>U</b><span>Up</span><i>oben</i></div>
    <div><b>D</b><span>Down</span><i>unten</i></div>
    <div><b>F</b><span>Front</span><i>vorne</i></div>
    <div><b>B</b><span>Back</span><i>hinten</i></div>
  </div>
  <div class="trap"><b>Achtung, Falle!</b> <b>U</b> heißt <b>Up</b> und bedeutet <b>OBEN</b>. Nicht unten! Unten ist <b>D</b> wie Down.</div>
  <div class="rules">
    <div class="rule"><div class="rk">R</div><p><b>Nur der Buchstabe:</b> Drehe die Seite im Uhrzeigersinn. Stell dir vor, du schaust direkt auf diese Seite, wie auf eine Uhr. Dann drehst du so, wie die Zeiger laufen.</p></div>
    <div class="rule"><div class="rk">R<span class="str">'</span></div><p><b>Mit Strich</b> (sprich: „R Strich“): Andersrum drehen, also gegen den Uhrzeigersinn.</p></div>
    <div class="rule"><div class="rk">R2</div><p><b>Mit 2:</b> Zweimal drehen. Die Richtung ist dabei egal.</p></div>
  </div>
  <div class="notgrid">%s</div>
  <div class="note">Ein Zauberspruch wird gelesen wie ein Satz: von links nach rechts. <b>R U R<span class="str">'</span> U<span class="str">'</span></b> heißt also: 4 Drehungen, eine nach der anderen. Die helle Fläche im Bild bleibt stehen, nur der kräftige Teil dreht sich.</div>
</section>''' % "".join(cells))

# ======================================================================= STEP 1 DAISY
stA = move(S, "F2 L2 R")
imgA = svg_cube(stA, 'top', 185, colors=masked(stA, lambda p, n, v: is_center(p) or (p[1] == 1 and is_edge(p) and n == (0, 1, 0) and v == 'W') or p == (1, 0, 1)),
                extra=ring([(1, 0, 1.5)], 'top', 185, r=0.7))
stB = move(S, "L2 R2")
imgB = svg_cube(stB, 'bottom', 185, colors=masked(stB, lambda p, n, v: is_center(p) or p == (0, -1, 1)),
                extra=ring([(0, -1.5, 1)], 'bottom', 185, r=0.7))
stC = move(S, "L2 B2 R F'")
imgC = svg_cube(stC, 'top', 185, colors=masked(stC, lambda p, n, v: is_center(p) or (p[1] == 1 and is_edge(p) and n == (0, 1, 0) and v == 'W') or p == (0, 1, 1)),
                extra=ring([(0, 1, 1.5)], 'top', 185, r=0.7))
pages.append('''<section class="page">%s
  <p class="lead">Wir bauen eine Blume! Der <b>gelbe Mittelstein</b> ist die Blüte. Vier <b>weiße Kanten</b> werden die Blütenblätter. Gelb ist oben.</p>
  <p>Suche eine weiße Kante (2 Farben, eine davon ist Weiß). Wo steckt sie?</p>
  <div class="cases3">
    <div class="case"><div class="ctag">A</div>%s<h3>In der Mitte</h3><p>Die Kante steckt in der mittleren Schicht. Drehe die Seite daneben so, dass das Weiß nach <b>oben</b> klappt.</p><div class="doit">%s</div></div>
    <div class="case"><div class="ctag">B</div>%s<h3>Unten, Weiß zeigt nach unten</h3><p>Drehe diese Seite <b>2×</b>. Jetzt ist das Weiß oben.</p><p class="small">Das Bild zeigt den Würfel von unten.</p><div class="doit">%s</div></div>
    <div class="case"><div class="ctag">C</div>%s<h3>Weiß zeigt zur Seite</h3><p>Drehe diese Seite <b>1×</b>. Jetzt steckt die Kante in der Mitte. Weiter wie bei <b>A</b>.</p><div class="doit">%s<span class="then">dann</span>%s</div></div>
  </div>
  <div class="golden"><b>Ganz wichtig:</b> Bevor du ein Blatt nach oben holst, drehe oben (<b>U</b>), bis an dieser Stelle noch <b>kein</b> weißes Blatt sitzt. Sonst schubst du ein Blatt, das schon fertig war, wieder weg.</div>
  <div class="done withpic">%s<div><b>Fertig, wenn:</b> 4 weiße Blätter um den gelben Mittelstein sitzen. Die zweite Farbe der Blätter ist noch egal.<br><br><b>Tipp:</b> Das Gänseblümchen ist der Teil, bei dem du am meisten selbst tüfteln musst. Probier einfach aus. Kaputt machen kannst du nichts!</div></div>
</section>''' % (page_head(1, 'Vier weiße Blätter um die gelbe Blüte'), imgA, mvbox('R'), imgB, mvbox('F2'), imgC, mvbox('F'), mvbox('R'), goal(1, 130)))

# ======================================================================= STEP 2 WHITE CROSS
st2 = move(S, "F2 R2 B2 L2")
before = svg_cube(st2, 'top', 210, colors=masked(st2, lambda p, n, v: is_center(p) or (p[1] == 1 and is_edge(p) and n == (0, 1, 0)) or (p == (0, 1, 1))),
                  extra=ring([(0, 1.0, 1.5)], 'top', 210, r=0.7))
st2b = move(st2, "F2")
after = svg_cube(st2b, 'bottom', 210, colors=masked(st2b, lambda p, n, v: is_center(p) or p == (0, -1, 1)))
pages.append('''<section class="page">%s
  <p class="lead">Jetzt klappen wir die Blätter nach unten. Gelb bleibt oben.</p>
  <ol class="steps">
    <li>Schau dir das Blatt vorne an. Außer Weiß hat es noch eine <b>zweite Farbe</b> (im Bild: Blau).</li>
    <li>Drehe oben (<b>U</b>), bis diese Farbe genau <b>über dem gleichen Mittelstein</b> steht. Es sieht aus wie ein kleiner Strich in einer Farbe.</li>
    <li>Drehe die vordere Seite <b>2×</b> (<b>F2</b>). Das Blatt ist jetzt unten!</li>
    <li>Drehe den ganzen Würfel, bis das nächste Blatt vorne ist. Mach dasselbe. Insgesamt 4×.</li>
  </ol>
  <div class="flow">
    <div class="fbox">%s<span>Vorher: Blau über Blau</span></div>
    <div class="farrow">%s<b>F2</b><span>vorne 2× drehen</span></div>
    <div class="fbox">%s<span>Nachher (von unten gesehen)</span></div>
  </div>
  <div class="done withpic">%s<div><b>Fertig, wenn:</b> Unten ein weißes Kreuz ist. Und jede weiße Kante passt mit ihrer zweiten Farbe zum Mittelstein daneben. Kipp den Würfel kurz und schau nach!</div></div>
  <div class="tip"><b>Tipp:</b> Wenn eine Kante nicht passt, ist das nicht schlimm. Mach sie wieder hoch (2× drehen) und probier es nochmal.</div>
</section>''' % (page_head(2, 'Die Blätter klappen nach unten'), before, move_icon('F2', 96), after, goal(2, 130)))

# ======================================================================= STEP 3 WHITE CORNERS
ci = []
for k, txt in ((1, 'Weiß zeigt nach <b>rechts</b>'), (3, 'Weiß zeigt nach <b>oben</b>'), (5, 'Weiß zeigt nach <b>vorne</b>')):
    st = move(S, invert(" ".join([SEXY] * k)))
    img = svg_cube(st, 'top', 175, colors=masked(st, lambda p, n, v: is_center(p) or (p[1] == -1 and is_edge(p)) or p == (1, 1, 1)),
                   extra=ring([(1.5, 1.5, 1.5)], 'top', 175))
    ci.append('<div class="case sm">%s<p>%s</p><div class="times">%d×</div></div>' % (img, txt, k))
spec = paint(S, {((1, -1, 1), 'D'): 'R', ((1, -1, 1), 'F'): 'W', ((1, -1, 1), 'R'): 'B'})
specimg = svg_cube(spec, 'top', 140, colors=masked(spec, lambda p, n, v: is_center(p) or (p[1] == -1 and is_edge(p)) or p == (1, -1, 1)),
                   extra=ring([(1.5, -1.5, 1.5)], 'top', 140))
pages.append('''<section class="page">%s
  <p class="lead">Jetzt kommen die 4 weißen Ecken nach unten. Dafür lernst du den <b>wichtigsten Trick</b> des ganzen Würfels.</p>
  <div class="trick">
    <div class="trickhead"><span class="spell">Der Ecken-Trick</span>%s<span class="say">Hoch, links, runter, rechts</span></div>
    %s
  </div>
  <ol class="steps">
    <li>Suche <b>oben</b> eine Ecke mit Weiß. Lies ihre zwei anderen Farben (im Bild: Blau und Rot).</li>
    <li>Drehe oben (<b>U</b>), bis die Ecke genau <b>über ihrem Platz</b> steht: zwischen den Mittelsteinen mit ihren Farben.</li>
    <li>Drehe den ganzen Würfel, bis diese Ecke <b>vorne rechts oben</b> ist.</li>
    <li>Mach den Ecken-Trick immer wieder, bis die Ecke unten richtig sitzt. Wie oft? Das hängt davon ab, wohin das Weiß zeigt:</li>
  </ol>
  <div class="cases3">%s</div>
  <div class="special">%s<div><h3>Sonderfall: Ecke steckt unten, aber falsch</h3><p>Halte sie <b>vorne rechts unten</b> und mach den Ecken-Trick <b>1×</b>. Jetzt ist sie oben, und du machst ganz normal weiter.</p></div></div>
</section>''' % (page_head(3, 'Die ganze untere Schicht wird fertig'), alg_text(SEXY), strip(SEXY, 84), "".join(ci), specimg))

# ======================================================================= STEP 4 MIDDLE LAYER
def mid_img(alg, slot):
    st = move(S, invert(alg))
    sx = slot[0]
    arrow = [(0.5 * sx, 1.08, Z), (0.78 * sx, 0.95, Z), (0.98 * sx, 0.72, Z), (1.06 * sx, 0.42, Z)]
    keep = lambda p, n, v: is_center(p) or p[1] == -1 or (p[1] == 0 and p != slot) or p == (0, 1, 1)
    return svg_cube(st, 'top', 190, colors=masked(st, keep), arrows=[{'pts': arrow, 'color': '#E11D8A', 'width': 190 / 5.3 * 0.2}])

pages.append('''<section class="page">%s
  <p class="lead">Jetzt kommen 4 Kanten in die mittlere Schicht. Gelb bleibt oben. Wir brauchen dafür nur Kanten <b>ohne Gelb</b>.</p>
  <ol class="steps">
    <li>Suche oben eine Kante <b>ohne Gelb</b>.</li>
    <li>Drehe oben (<b>U</b>), bis die vordere Farbe der Kante zum vorderen Mittelstein passt. Dann siehst du vorne ein <b>umgedrehtes T</b> in einer Farbe.</li>
    <li>Schau jetzt auf die <b>obere</b> Farbe der Kante. Zu welchem Mittelstein passt sie: rechts oder links? Dorthin muss die Kante.</li>
  </ol>
  <div class="hcase">%s<div class="hc"><h3>Oben Rot? Die Mitte rechts ist Rot. Also muss die Kante <u>nach rechts</u>:</h3><div class="spellname">Der Nach-rechts-Spruch %s</div>%s</div></div>
  <div class="hcase">%s<div class="hc"><h3>Oben Orange? Die Mitte links ist Orange. Also muss die Kante <u>nach links</u>:</h3><div class="spellname">Der Nach-links-Spruch %s</div>%s</div></div>
  <div class="special"><div><h3>Sonderfall: Eine Kante steckt in der Mitte, aber falsch</h3><p>Halte sie <b>vorne rechts</b> und mach den Nach-rechts-Spruch einmal. Damit schubst du sie nach oben. Dann setzt du sie ganz normal ein.</p></div></div>
</section>''' % (page_head(4, 'Zwei Schichten sind fertig'), mid_img(RIGHT, (1, 0, 1)), alg_text(RIGHT), strip(RIGHT, 58, 'tight'),
                  mid_img(LEFT, (-1, 0, 1)), alg_text(LEFT), strip(LEFT, 58, 'tight')))

# ======================================================================= STEP 5 YELLOW CROSS
def ycase(pattern, title, txt, extra=''):
    return '<div class="ycase">%s<div class="front">vorne</div><h3>%s</h3><p>%s</p>%s</div>' % (top_grid(pattern, 140), title, txt, extra)

pages.append('''<section class="page">%s
  <p class="lead">Oben soll ein gelbes Kreuz entstehen. Schau nur auf die <b>gelben Kanten oben</b>. Die Ecken sind noch egal.</p>
  <div class="trick">
    <div class="trickhead"><span class="spell">Der Kreuz-Spruch</span>%s<span class="say">Vorne drehen, Ecken-Trick, vorne zurück</span></div>
    %s
  </div>
  <p>Schau von oben auf deinen Würfel. Welches Bild siehst du? Die Seite unten im Bild ist die Seite, die dich anschaut.</p>
  <div class="ygrid">
    %s%s%s%s
  </div>
  <div class="tip"><b>Tipp:</b> Der Kreuz-Spruch ist einfach der Ecken-Trick mit einer Drehung vorne davor (<b>F</b>) und einer danach (<b>F<span class="str">'</span></b>).</div>
</section>''' % (page_head(5, 'Ein gelbes Kreuz auf der Oberseite'), alg_text(OLL), strip(OLL, 80),
                  ycase('', 'Punkt', 'Kreuz-Spruch <b>1×</b>. Danach hast du einen Haken.'),
                  ycase('BL', 'Haken', 'Halte ihn <b>hinten links</b>, wie die Uhrzeiger um <b>9 Uhr</b>. Kreuz-Spruch <b>1×</b>. Danach hast du eine Linie.'),
                  ycase('LR', 'Linie', 'Halte sie <b>waagerecht</b>, also von links nach rechts. Kreuz-Spruch <b>1×</b>.'),
                  ycase('BFLR', 'Kreuz', '<b>Geschafft!</b> Weiter zu Schritt 6.')))

# ======================================================================= STEP 6 YELLOW EDGES
pages.append('''<section class="page">%s
  <p class="lead">Die gelben Kanten sollen zu ihren Seiten passen. Die Farbe an der Kante muss die <b>gleiche</b> sein wie der Mittelstein darunter.</p>
  <div class="trick">
    <div class="trickhead"><span class="spell">Der Kanten-Spruch</span>%s</div>
    %s
  </div>
  <div class="netinfo">In den Bildern schaust du von oben auf den Würfel. Die Seiten sind rundherum aufgeklappt, wie bei einem Bastelbogen. <b>Unten im Bild ist vorne.</b></div>
  <ol class="steps">
    <li>Drehe oben (<b>U</b>), bis <b>mindestens 2 Kanten</b> passen. Das geht immer!</li>
  </ol>
  <div class="cases2">
    <div class="case">%s<h3>Die 2 passenden sind nebeneinander</h3><p>Halte den Würfel so, dass sie <b>hinten</b> und <b>rechts</b> sind. Kanten-Spruch <b>1×</b>. Jetzt passen alle 4!</p></div>
    <div class="case">%s<h3>Die 2 passenden sind gegenüber</h3><p>Mach den Kanten-Spruch <b>1×</b>, egal wie du hältst. Dann wieder oben drehen, bis 2 nebeneinander passen. Weiter wie links.</p></div>
  </div>
  <div class="done"><b>Fertig, wenn:</b> Alle 4 gelben Kanten zu ihren Mittelsteinen passen.</div>
</section>''' % (page_head(6, 'Die gelben Kanten passen zu ihren Seiten'), alg_text(SUNE), strip(SUNE, 74),
                  netwrap(edge_net({'F': 'O', 'R': 'R', 'B': 'G', 'L': 'B'}, 215)),
                  netwrap(edge_net({'F': 'B', 'R': 'O', 'B': 'G', 'L': 'R'}, 215))))

# ======================================================================= STEP 7 CORNERS PERMUTE
st_ok = move(move(S, X_TWIST), invert(NIKLAS))
st_bad = move(S, "U' " + NIKLAS + " U")
keep7 = lambda p, n, v: not (is_corner(p) and p[1] == 1) or p == (1, 1, 1)
img_ok = svg_cube(st_ok, 'top', 190, colors=masked(st_ok, keep7), extra=ring([(1.5, 1.5, 1.5)], 'top', 190, '#16A34A'))
img_bad = svg_cube(st_bad, 'top', 190, colors=masked(st_bad, keep7), extra=ring([(1.5, 1.5, 1.5)], 'top', 190, '#D7263D'))
ok_cols = sorted(st_ok[((1, 1, 1), FACE_N[f])] for f in 'UFR')
bad_cols = sorted(st_bad[((1, 1, 1), FACE_N[f])] for f in 'UFR')
pages.append('''<section class="page">%s
  <p class="lead">Jetzt wandern die gelben Ecken an ihren richtigen Platz. Ob sie schon richtig herum gedreht sind, ist noch <b>egal</b>!</p>
  <div class="cases2">
    <div class="case">%s<h3 class="ok">✓ Richtiger Platz</h3><p>Die Ecke hat Gelb, Blau und Rot. Die Mittelsteine drumherum sind auch Gelb, Blau und Rot. Passt! Auch wenn sie verdreht ist.</p></div>
    <div class="case">%s<h3 class="bad">✗ Falscher Platz</h3><p>Die Ecke hat Grün und Orange. Aber hier gibt es keinen grünen und keinen orangen Mittelstein. Die Ecke gehört woanders hin.</p></div>
  </div>
  <div class="trick">
    <div class="trickhead"><span class="spell">Der Wander-Spruch</span>%s</div>
    %s
  </div>
  <ol class="steps">
    <li>Suche eine Ecke, die schon am <b>richtigen Platz</b> ist.</li>
    <li>Halte den Würfel so, dass diese Ecke <b>vorne rechts oben</b> ist.</li>
    <li>Mach den Wander-Spruch. Die anderen 3 Ecken tauschen ihre Plätze. Wiederhole ihn, bis alle 4 Ecken am richtigen Platz sind (1× oder 2×).</li>
  </ol>
  <div class="special"><div><h3>Keine Ecke ist am richtigen Platz?</h3><p>Mach den Wander-Spruch <b>1×</b>, egal wie du den Würfel hältst. Danach ist eine Ecke richtig.</p></div></div>
</section>''' % (page_head(7, 'Jede Ecke sitzt am richtigen Platz'), img_ok, img_bad, alg_text(NIKLAS), strip(NIKLAS, 74)))

# ======================================================================= STEP 8 CORNERS TWIST
st8 = move(S, X_TWIST)
img8 = svg_cube(st8, 'top', 175, extra=ring([(1.5, 1.5, 1.5)], 'top', 175))
mess = svg_cube(move(st8, " ".join([TWIST] * 2)), 'top', 150)
pages.append('''<section class="page">%s
  <p class="lead">Der letzte Schritt! Jetzt drehen wir die gelben Ecken richtig herum.</p>
  <div class="trap"><b>Ganz wichtig:</b> In diesem Schritt drehst du <b>nie den ganzen Würfel</b>. Gelb bleibt oben, vorne bleibt vorne. Du drehst nur die obere Schicht (<b>U</b>).</div>
  <div class="trick">
    <div class="trickhead"><span class="spell">Der Dreh-Trick</span>%s<span class="say">Runter, unten links, hoch, unten rechts</span></div>
    %s
  </div>
  <div class="s8">
    <div class="s8l">
      <ol class="steps">
        <li>Drehe oben (<b>U</b>), bis eine Ecke, bei der Gelb <b>nicht</b> oben ist, <b>vorne rechts oben</b> sitzt.</li>
        <li>Mach den Dreh-Trick immer wieder, bis bei <b>dieser Ecke</b> Gelb oben ist. Das sind 2× oder 4×.</li>
        <li>Drehe <b>nur oben</b> (<b>U</b>), bis die nächste falsche Ecke vorne rechts oben ist. Wieder Dreh-Trick.</li>
        <li>Wenn alle Ecken oben gelb sind: Drehe oben, bis alles passt.</li>
      </ol>
    </div>
    <div class="s8r">%s<span>Diese Ecke ist falsch gedreht</span></div>
  </div>
  <div class="panic">%s<div><h3>Keine Panik!</h3><p>Mittendrin sieht dein Würfel unten <b>kaputt</b> aus. Das ist richtig so! Mach einfach weiter. Wenn alle Ecken fertig sind, repariert sich der Rest von selbst.</p></div></div>
  <div class="win">%s<div><h2>Geschafft!</h2><p>Du hast den Zauberwürfel gelöst. Jetzt mischen und nochmal. Mit jedem Mal wirst du schneller!</p></div></div>
</section>''' % (page_head(8, 'Alle Ecken richtig herum: fertig!'), alg_text(TWIST), strip(TWIST, 84), img8, mess, svg_cube(S, 'top', 130)))

# ======================================================================= CHEAT SHEET
rows = [
    (1, 'Weiße Kanten um Gelb sammeln. Vorher oben drehen, damit der Platz frei ist.', ''),
    (2, 'Zweite Farbe über ihren Mittelstein drehen, dann vorne 2×.', 'F2'),
    (3, 'Ecke über ihren Platz, vorne rechts oben halten. Wiederholen: 1×, 3× oder 5×.', SEXY),
    (4, 'Umgedrehtes T vorne. Obere Farbe passt nach rechts:', RIGHT),
    (None, 'Obere Farbe passt nach links:', LEFT),
    (5, 'Haken hinten links, Linie waagerecht.', OLL),
    (6, '2 passende Kanten hinten und rechts halten.', SUNE),
    (7, 'Richtige Ecke vorne rechts oben halten.', NIKLAS),
    (8, 'Falsche Ecke vorne rechts oben. 2× oder 4×. Nur oben drehen!', TWIST),
]
trs = []
for i, txt, alg in rows:
    if i:
        left = '<td class="cn" style="background:%s">%d</td><td class="cg">%s</td><td class="cname"><b>%s</b><br>%s</td>' % (STEP_COLORS[i - 1], i, goal(i, 70), STEP_NAMES[i - 1], txt)
    else:
        left = '<td class="cn" style="background:%s"></td><td class="cg"></td><td class="cname">%s</td>' % (STEP_COLORS[3], txt)
    trs.append('<tr>%s<td class="calg">%s</td></tr>' % (left, alg_text(alg) if alg else '<span class="small">ohne Spruch, einfach ausprobieren</span>'))
pages.append('''<section class="page cheat">
  <h1 class="ptitle">Spickzettel</h1>
  <p class="lead">Alle Schritte auf einer Seite. Gelb oben, Weiß unten. <b>U</b> = oben, <b>D</b> = unten, <b>'</b> = andersrum, <b>2</b> = zweimal.</p>
  <table class="ctab">%s</table>
  <div class="minilegend">%s</div>
</section>''' % ("".join(trs), "".join('<div class="ml">%s<b>%s</b></div>' % (move_icon(m, 58), fmt(m)) for m in ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'"])))

import os
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'style.css')).read()
html = '<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Zauberwürfel lösen</title><style>%s</style></head><body>%s</body></html>' % (CSS, "\n".join(pages))
os.makedirs(os.path.join(HERE, '..', 'guides'), exist_ok=True)
open(os.path.join(HERE, '..', 'guides', 'schicht-fuer-schicht.html'), 'w').write(html)
print("ok", ok_cols, bad_cols)
