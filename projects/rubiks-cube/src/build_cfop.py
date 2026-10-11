import math, io, os, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build_layer_by_layer as B
from cube import *
from build_layer_by_layer import (masked, is_center, is_edge, is_corner, line, arc_front, ARROWS, Z, fmt, alg_text, goal, CSS)

HERE = os.path.dirname(os.path.abspath(__file__))
S = solved()
ARROWS.update({'f': ARROWS['F'], "f'": ARROWS["F'"], 'r': ARROWS['R'], "r'": ARROWS["R'"],
               'M': line((0, 1.15, Z), (0, -1.2, Z)), "M'": line((0, -1.15, Z), (0, 1.2, Z)),
               'B2': ARROWS['B'], 'D2': ARROWS['D'], 'L2': ARROWS['L']})
ARROWS['M2'] = ARROWS['M']

def icon(m, size=70):
    n, pred = MOVE_DEF[m[0]]
    dim = lambda pos, nrm: not pred(pos)
    badge = ''
    if m.endswith('2'):
        s = size
        badge = ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#111"/><text x="%.1f" y="%.1f" font-family="Inter" font-weight="800" font-size="%.1f" fill="#fff" text-anchor="middle">2×</text>'
                 % (s * 0.85, s * 0.14, s * 0.14, s * 0.85, s * 0.14 + s * 0.055, s * 0.14))
    return svg_cube(S, 'top', size, dim=dim, arrows=[{'pts': ARROWS[m]}], extra=badge)

def strip(alg, size=62, cls=''):
    items = []
    for i, m in enumerate(alg.split()):
        items.append('<div class="mv"><div class="mvnum">%d</div>%s<b>%s</b></div>' % (i + 1, icon(m, size), fmt(m)))
    return '<div class="strip %s">%s</div>' % (cls, "".join(items))

def mvbox(m, size=62):
    return '<div class="mv">%s<b>%s</b></div>' % (icon(m, size), fmt(m))

PH = {1: ('#1565D8', 'Cross'), 2: ('#D7263D', 'F2L'), 3: ('#E0A800', 'OLL'), 4: ('#16A34A', 'PLL')}
def head(i, title, sub, goalsvg, kicker):
    c = PH[i][0]
    return '''<div class="stephead" style="--c:%s"><div class="num">%s</div><div class="ht"><div class="kicker">%s</div><h1>%s</h1><div class="sub">%s</div></div><div class="goal">%s<span>So sieht es danach aus</span></div></div>''' % (c, PH[i][1][0] if i != 2 else 'F', kicker, title, sub, goalsvg)

# ---------------- images
def piece_pos(st, cols):
    cols = frozenset(cols)
    for p in set(k[0] for k in st):
        if frozenset(st[(p, n)] for (pp, n) in st if pp == p) == cols:
            return p

def cross_img(scr, size=170):
    st = move(S, scr)
    pe = piece_pos(st, 'WB')
    keep = lambda p, n, v: is_center(p) or p == pe or p in ((-1, -1, 0), (1, -1, 0), (0, -1, -1))
    return svg_cube(st, 'top', size, colors=masked(st, keep))

SLOT = {(1, -1, 1), (1, 0, 1)}
def f2l_img(alg, size=150):
    st = move(S, invert(alg))
    pc = piece_pos(st, 'WBR'); pe = piece_pos(st, 'BR')
    def keep(p, n, v):
        if p in (pc, pe): return True
        if is_center(p): return True
        return p[1] <= 0 and p not in SLOT
    return svg_cube(st, 'top', size, colors=masked(st, keep))

def oll_img(alg, size=150, pre=None):
    st = move(S, invert(alg)) if pre is None else pre
    return svg_top_net(st, size=size, gray_fn=lambda pos, n: st[(pos, n)] != 'Y', rows=1)

def pll_img(alg, size=150):
    st = move(S, invert(alg))
    return svg_top_net(st, size=size, rows=1)

def headlights(alg):
    st = move(S, invert(alg))
    names = {'F': 'vorne', 'R': 'rechts', 'B': 'hinten', 'L': 'links'}
    for f, nm in names.items():
        n = FACE_N[f]
        ps = [p for p in [(x, 1, z) for x in (-1, 1) for z in (-1, 1)] if dot(p, n) == 1]
        if st[(ps[0], n)] == st[(ps[1], n)]: return nm
    return None

# ---------------- algorithms (all verified in the simulator)
SEXY = "R U R' U'"
LINE = "F R U R' U' F'"; HOOK = "F U R U' R' F'"; DOT = "F R U R' U' F' f R U R' U' f'"
OLL7 = [('Sune', "R U R' U R U2 R'", 'Eine gelbe Ecke oben, vorne links.'),
        ('Anti-Sune', "R U2 R' U' R U' R'", 'Eine gelbe Ecke oben, hinten rechts.'),
        ('U-Form', "R2 D R' U2 R D' R' U2 R'", 'Zwei gelbe Ecken oben, nebeneinander hinten.'),
        ('Pi', "R U2 R2 U' R2 U' R2 U2 R", 'Keine gelbe Ecke oben. Vergleiche die gelben Streifen an der Seite.'),
        ('H', "F R U R' U' R U R' U' R U R' U' F'", 'Keine gelbe Ecke oben. Vergleiche die gelben Streifen an der Seite.'),
        ('T', "r U R' U' r' F R F'", 'Zwei gelbe Ecken oben, nebeneinander rechts.'),
        ('L', "F R' F' r U R U' r'", 'Zwei gelbe Ecken oben, über Kreuz.')]
PLLC = [('A-Perm', "R' F R' B2 R F' R' B2 R2", 'Ecken: ein Scheinwerfer.'), ('Y-Perm', "F R U' R' U' R U R' F' R U R' U' R' F R F'", 'Ecken: kein Scheinwerfer')]
PLLE = [('U-Perm a', "R2 U R U R' U' R' U' R' U R'", 'Kanten: eine fertige Seite hinten, Dreieck'), ('U-Perm b', "R U' R U R U R U' R' U' R2", 'Kanten: eine fertige Seite hinten, Dreieck andersrum'),
        ('H-Perm', "M2 U M2 U2 M2 U M2", 'Kanten: gegenüber tauschen'), ('Z-Perm', "M' U M2 U M2 U M' U2 M2 U'", 'Kanten: nebeneinander tauschen')]
F2L_EASY = [("R U R'", 'Kante hinten. Weiß der Ecke schaut nach rechts.'), ("R U' R'", 'Kante vorne. Ecke vorne links, Weiß schaut nach links.'),
            ("F' U' F", 'Kante links. Weiß der Ecke schaut nach vorne.'), ("F' U F", 'Kante rechts. Ecke hinten rechts, Weiß schaut nach hinten.'),
            ("U R U' R'", 'Pärchen steht nebeneinander. Weiß schaut nach vorne.'), ("U' F' U F", 'Pärchen steht nebeneinander. Weiß schaut nach rechts.')]
F2L_MORE = [("R U2 R' U' R U R'", 'Ecke vorne rechts, Weiß oben. Kante rechts.'), ("U' R U R' U R U' R'", 'Ecke hinten rechts, Weiß oben. Kante vorne.'),
            ("R U R' U' R U R'", 'Ecke steckt unten, Weiß rechts. Kante rechts oben.'), ("F' U' F U F' U' F", 'Ecke steckt unten, Weiß vorne. Kante vorne oben.'),
            ("R U' R' U R U' R'", 'Ecke steckt unten, Weiß vorne. Kante rechts oben.'), ("F' U F U' F' U F", 'Ecke steckt unten, Weiß rechts. Kante vorne oben.'),
            ("R U R' U' R U R' U' R U R'", 'Ecke vorne rechts, Weiß oben. Kante steckt in der Mitte.'), ("U F' U' F U' R U R'", 'Ecke vorne rechts, Weiß rechts. Kante steckt in der Mitte.')]
for _, a, _ in OLL7: pass

pages = []
# ================================================================= COVER
ov = [(1, 'Cross', 'Kreuz unten bauen', goal(2, 118)), (2, 'F2L', 'Ecke und Kante als Pärchen einsetzen', goal(4, 118)),
      (3, 'OLL', 'Oben alles gelb machen', svg_cube(S, 'top', 118, colors=masked(S, lambda p, n, v: is_center(p) or p[1] <= 0 or n == (0, 1, 0)))),
      (4, 'PLL', 'Oben alles an den Platz', goal(8, 118))]
ovh = "".join('<div class="ov"><div class="ovn" style="background:%s">%d</div>%s<span><b>%s</b><br>%s</span></div>' % (PH[i][0], i, g, nm, tx) for i, nm, tx, g in ov)
scr = move(S, "R U2 F' L D' B2 R' U F2 L' U' B")
pages.append('''<section class="page cover">
  <div class="covertop"><div class="covertext">
    <div class="eyebrow">Für Fortgeschrittene</div>
    <h1 class="title">Schneller mit<br>CFOP</h1>
    <p class="tag">Du kannst den Würfel schon Schicht für Schicht? Dann lernst du jetzt die Methode der Speedcuber. Weniger Züge, weniger Pausen und viel mehr Tempo.</p>
    <div class="owner">Dieser Plan gehört: <span class="blank"></span></div>
    <div class="owner">Meine Bestzeit: <span class="blank short"></span></div>
  </div><div class="coverpics"><div>%s</div><div class="cparrow">➜</div><div>%s</div></div></div>
  <h2 class="ovh">Dein Weg in 4 Phasen</h2>
  <div class="overview o4">%s</div>
  <div class="golden"><b>Gleiche Regel wie vorher:</b> Weiß ist unten, Gelb ist oben. Neu ist nur: Das Kreuz baust du gleich unten, ohne Gänseblümchen.</div>
</section>''' % (svg_cube(scr, 'top', 200), svg_cube(S, 'top', 200), ovh))

# ================================================================= WHAT IS CFOP
pages.append('''<section class="page">
  <h1 class="ptitle">Was ist CFOP?</h1>
  <p class="lead">CFOP ist die Methode, mit der die meisten Speedcuber der Welt lösen. Der Name sind einfach die Anfangsbuchstaben der vier Phasen.</p>
  <div class="cfop4">
    <div style="--c:#1565D8"><b>C</b><span>Cross</span><i>Kreuz</i></div>
    <div style="--c:#D7263D"><b>F2L</b><span>First Two Layers</span><i>die ersten zwei Schichten</i></div>
    <div style="--c:#E0A800"><b>O</b><span>Orient</span><i>oben alles gelb drehen</i></div>
    <div style="--c:#16A34A"><b>P</b><span>Permute</span><i>oben alles an den Platz</i></div>
  </div>
  <h2 class="h2">Was ist anders als Schicht für Schicht?</h2>
  <table class="cmp">
    <tr><th></th><th>Schicht für Schicht</th><th>CFOP</th></tr>
    <tr><td><b>Phasen</b></td><td>8 Schritte</td><td>4 Phasen</td></tr>
    <tr><td><b>Weiße Seite</b></td><td>Erst Kreuz, dann Ecken, dann Mitte</td><td>Kreuz, dann Ecke und Kante <b>gleichzeitig</b></td></tr>
    <tr><td><b>Gelbe Seite</b></td><td>4 Schritte</td><td>2 Schritte (OLL und PLL)</td></tr>
    <tr><td><b>Züge insgesamt</b></td><td>weit über 100</td><td>ungefähr 55 bis 60</td></tr>
    <tr><td><b>Denken</b></td><td>Anleitung abarbeiten</td><td>Schon vorausschauen, während du drehst</td></tr>
  </table>
  <h2 class="h2">Was du lernen musst</h2>
  <div class="learn">
    <div><b>Cross</b><p>Nichts auswendig. Du denkst dir die Züge selbst aus.</p></div>
    <div><b>F2L</b><p>Fast nichts auswendig. Du lernst ein Prinzip und ein paar Fälle.</p></div>
    <div><b>OLL</b><p>10 Formeln. Das ist die „2-look“-Variante.</p></div>
    <div><b>PLL</b><p>6 Formeln. Das ist die „2-look“-Variante.</p></div>
  </div>
  <div class="note"><b>2-look</b> heißt: Du schaust zweimal hin. Erst machst du das Kreuz oben gelb, dann die Ecken. Erst bringst du die Ecken an den Platz, dann die Kanten. Das sind wenige Formeln und trotzdem schon richtig schnell. Die Profis lernen später je 57 und 21 Formeln. Das musst du jetzt nicht.</div>
  <div class="tip"><b>Ehrlich gesagt:</b> Der Anfang ist langsamer als Schicht für Schicht. Das ist normal. Nach ein paar Wochen Üben bist du schneller als vorher.</div>
</section>''')

# ================================================================= NEW MOVES + WORDS
newm = "".join('<div class="nc">%s<div class="nl">%s</div><div class="ncap">%s</div></div>' % (icon(m, 118), fmt(m), c) for m, c in
                [('f', 'vordere <b>zwei</b> Schichten<br>im Uhrzeigersinn'), ('r', 'rechte <b>zwei</b> Schichten<br>wie R nach oben'), ("r'", 'rechte <b>zwei</b> Schichten<br>wie R&#39; nach unten'),
                 ('M', 'nur die <b>Mittelschicht</b><br>nach unten (wie L)'), ("M'", 'nur die <b>Mittelschicht</b><br>nach oben'), ('M2', 'Mittelschicht<br>2× drehen')])
pages.append('''<section class="page">
  <h1 class="ptitle">Neue Züge und neue Wörter</h1>
  <p class="lead">Alle Züge aus der ersten Anleitung gelten weiter (R, L, U, D, F, B, mit Strich und mit 2). Dazu kommen drei neue.</p>
  <div class="notgrid n3">%s</div>
  <div class="note">Ein <b>kleiner Buchstabe</b> (f, r) heißt: Drehe die Außenschicht <b>und</b> die Schicht dahinter zusammen. <b>M</b> ist die Mittelschicht zwischen L und R. Sie dreht wie L.</div>
  <h2 class="h2">Wörter aus der Cuber-Welt</h2>
  <div class="words">
    <div><b>Algorithmus</b><p>Eine feste Zugfolge, die immer dasselbe macht. Wie ein Zauberspruch aus der ersten Anleitung.</p></div>
    <div><b>Trigger</b><p>Ein kurzer Spruch, den deine Finger auswendig können. Der wichtigste ist der Sexy-Move.<br><span class="algtxt">%s</span></p></div>
    <div><b>AUF</b><p>Das heißt „Adjust U Face“. Am Ende der Phase drehst du oben noch kurz (U, U&#39; oder U2), bis alles passt.</p></div>
    <div><b>Lookahead</b><p>Vorausschauen. Du suchst das nächste Pärchen, <b>während</b> deine Hände noch das letzte einsetzen.</p></div>
    <div><b>Case</b><p>Ein Fall. Eine bestimmte Lage der Steine, für die du einen bestimmten Spruch kennst.</p></div>
    <div><b>Slot</b><p>Der Platz in der unteren Ecke, wo ein Pärchen hinein soll. Wir nehmen immer den Platz <b>vorne rechts</b>.</p></div>
  </div>
  <div class="trap"><b>Wichtig bei den Bildern:</b> Du hältst den Würfel immer so, wie das Bild gezeichnet ist. Gelb oben, Blau vorne, Rot rechts. Wenn dein Würfel anders aussieht, dreh ihn in der Hand (nicht mitten im Spruch!), bis das Bild passt.</div>
</section>''' % (newm, SEXY.replace("'", "<span class='str'>'</span>")))

# ================================================================= CROSS
cases = [("F2", 'Kante oben, Weiß oben', 'Drehe oben (<b>U</b>), bis die zweite Farbe der Kante <b>über ihrem Mittelstein</b> steht. Dann vorne 2×.', 'F2', "F2"),
         ("F'", 'Kante vorne rechts in der Mitte', 'Weiß schaut nach rechts. Dann reicht <b>ein</b> Zug: vorne einmal drehen. Das Weiß klappt nach unten.', 'F', "F'"),
         ("R F' R'", 'Kante oben rechts, Weiß schaut nach rechts', 'Erst die Kante nach unten holen, dann einsetzen. Drei Züge.', "R' F R", "R F' R'")]
cr = []
for scr_, t, d, alg, _ in [("F2", 'Kante oben, Weiß oben', 'Drehe oben (<b>U</b>), bis die zweite Farbe der Kante <b>über ihrem Mittelstein</b> steht. Dann vorne 2×.', "F2", ""),
                           ("F'", 'Kante vorne rechts in der Mitte', 'Weiß schaut nach rechts. Ein Zug reicht: vorne einmal drehen. Das Weiß klappt nach unten.', "F", ""),
                           ("R' F' R", 'Kante oben rechts, Weiß schaut nach rechts', 'Erst die Kante nach unten holen, dann einsetzen. Drei Züge.', "R' F R", "")]:
    cr.append('<div class="case">%s<h3>%s</h3><p>%s</p><div class="doit">%s</div></div>' % (cross_img(scr_, 170), t, d, "".join(mvbox(m, 58) for m in alg.split())))
pages.append('''<section class="page">%s
  <p class="lead">Bei Schicht für Schicht hast du erst ein Gänseblümchen gebaut. Das lässt du jetzt weg. Du holst jede weiße Kante <b>direkt</b> an ihren Platz unten.</p>
  <ol class="steps">
    <li>Halte den Würfel mit <b>Weiß unten</b>. Schau dir die vier weißen Kanten an und suche die, die schon fast richtig sitzt.</li>
    <li>Dreh den Würfel so, dass der Platz, wo die Kante hin muss, <b>vorne unten</b> ist.</li>
    <li>Hole die Kante mit wenigen Zügen dorthin. Diese drei Fälle brauchst du am häufigsten:</li>
  </ol>
  <div class="cases3">%s</div>
  <div class="tip"><b>Links geht es genauso, nur spiegelverkehrt:</b> Statt <b>R</b> nimmst du <b>L</b> und statt F ein F&#39;. Aus „R&#39; F R“ wird „L F&#39; L&#39;“.</div>
  <div class="tip"><b>Kante unten, aber falsch herum?</b> Drehe sie mit <b>F2</b> nach oben. Dann ist sie wieder einer der Fälle oben.</div>
  <div class="done"><b>Fertig, wenn:</b> Unten ein weißes Kreuz ist und jede Kante zu ihrem Mittelstein passt. Wie vorher. Aber jetzt in 4 bis 8 Zügen und ohne Gänseblümchen!</div>
  <div class="note"><b>Profi-Trick:</b> Schau dir den Würfel eine Weile an, <b>bevor</b> du den ersten Zug machst. Plane das ganze Kreuz im Kopf. Das nennt man <b>Inspektion</b> und ist der Schlüssel zu schnellen Zeiten.</div>
</section>''' % (head(1, 'Das Kreuz unten', 'Direkt am richtigen Platz, ohne Gänseblümchen', goal(2, 96), 'Phase 1 von 4'), "".join(cr)))

# ================================================================= F2L IDEA
e_sep = f2l_img("R U' R' U F' U' F", 175)
e_pair = f2l_img("U R U' R'", 175)
pages.append('''<section class="page">%s
  <p class="lead">Bei Schicht für Schicht hast du erst die weißen Ecken eingesetzt und danach die Kanten der Mitte. Bei F2L machst du <b>beides auf einmal</b>. Du nimmst eine Ecke und die Kante, die zu ihr gehört, als <b>Pärchen</b>.</p>
  <div class="pairidea">
    <div class="case">%s<h3>1. Finden</h3><p>Suche eine <b>weiße Ecke</b> und die Kante, die dieselben Farben hat. Hier: Weiß-Blau-Rot und Blau-Rot. Das ist ein Pärchen.</p></div>
    <div class="case">%s<h3>2. Verbinden</h3><p>Dreh oben und bewege die Ecke so, dass die beiden <b>nebeneinander</b> stehen und die gleichen Farben nach außen zeigen.</p></div>
    <div class="case">%s<h3>3. Einsetzen</h3><p>Setze das Pärchen mit einem kurzen Spruch zusammen in den Platz <b>vorne rechts</b> ein.</p></div>
  </div>
  <h2 class="h2">So gehst du vor</h2>
  <ol class="steps">
    <li>Halte den Würfel mit <b>Weiß unten</b> und dem Kreuz fertig. Wähle einen freien Platz unten, der noch kein Pärchen hat. Drehe den Würfel, bis dieser Platz <b>vorne rechts</b> ist.</li>
    <li>Suche die Ecke und die Kante für diesen Platz. Schau dir an, in welchem der Fälle auf den nächsten Seiten sie stehen.</li>
    <li>Mach den Spruch zu diesem Fall. Das Pärchen sitzt jetzt unten.</li>
    <li>Wiederhole das für alle vier Plätze. Drehe dazu den Würfel in der Hand.</li>
  </ol>
  <div class="trap"><b>Nicht auswendig lernen!</b> Die Sprüche sind nur Beispiele. Wenn du verstanden hast, <b>warum</b> sie funktionieren, kannst du dir viele selbst ausdenken. Das ist der Trick von F2L: <b>Ecke und Kante gehen immer gemeinsam, nie einzeln.</b></div>
  <div class="done withpic">%s<div><b>Fertig, wenn:</b> Die untere Schicht und die mittlere Schicht sind komplett fertig. Oben liegt alles noch durcheinander. Das ist derselbe Zustand wie am Ende von Schritt 4 der ersten Anleitung.</div></div>
</section>''' % (head(2, 'Die ersten zwei Schichten', 'Ecke und Kante gemeinsam als Pärchen', goal(4, 96), 'Phase 2 von 4'), e_sep, e_pair, goal(4, 175), goal(4, 130)))

# ================================================================= F2L CASES
def f2lcard(alg, hint, withstrip):
    return '<div class="ocase">%s<div class="small">%s</div><div class="aw">%s</div>%s</div>' % (f2l_img(alg, 150), hint, alg_text(alg), strip(alg, 44, 'tight') if withstrip else '')
easy = "".join(f2lcard(a, h, True) for a, h in F2L_EASY)
pages.append('''<section class="page"><h1 class="ptitle">F2L: die 6 leichten Fälle</h1>
  <p class="lead">Hier liegen Ecke und Kante <b>oben</b>. Die Bilder zeigen den Platz vorne rechts. Grau ist gerade egal. Gefärbt sind die zwei fertigen Schichten und das Pärchen.</p>
  <div class="ogrid g3">%s</div>
  <div class="tip"><b>Und die anderen Plätze?</b> Drehe den ganzen Würfel in der Hand, bis der Platz, den du füllen willst, <b>vorne rechts</b> ist. Dann gelten die Bilder wieder.</div>
</section>''' % easy)
more = "".join(f2lcard(a, h, False) for a, h in F2L_MORE)
pages.append('''<section class="page"><h1 class="ptitle">F2L: weitere Fälle</h1>
  <p class="lead">Jetzt wird es kniffliger. Hier steckt die Ecke schon unten im Platz, oder die Kante steckt in der Mitte. Auch das sind nur Beispiele. Du wirst mit der Zeit eigene Wege finden.</p>
  <div class="ogrid g4">%s</div>
  <div class="trap"><b>Etwas steckt falsch im Platz?</b> Dann hole es erst nach oben, mit <b>R U R&#39;</b> (oder R U&#39; R&#39;). Danach hast du wieder einen der Fälle, die du schon kennst. Nicht ärgern: Das gehört dazu!</div>
</section>''' % more)

# ================================================================= OLL
def ocard(name, alg, hint, img, extra=''):
    return '<div class="ocase">%s<h3>%s</h3><div class="small">%s</div><div class="aw">%s</div>%s</div>' % (img, name, hint, alg_text(alg), extra)
oc = ocard('Linie', LINE, 'Waagerecht halten: ein Strich von links nach rechts.', oll_img(LINE, 150)) + \
     ocard('Haken', HOOK, 'Haken hinten links, wie 9 Uhr und 12 Uhr.', oll_img(HOOK, 150)) + \
     ocard('Punkt', DOT, 'Nur der Mittelstein ist gelb. Mach beide Sprüche hintereinander.', oll_img(DOT, 150, pre=move(S, invert(DOT))))
pages.append('''<section class="page">%s
  <p class="lead">Jetzt soll oben alles gelb werden. Wir machen das in zwei Blicken. Erst das <b>Kreuz</b>, dann die <b>Ecken</b>. Schau auf die gelben Felder oben. Die Seitenstreifen zeigen dir, wo Gelb an der Seite liegt.</p>
  <h2 class="h2">Blick 1: Das gelbe Kreuz</h2>
  <p>Welche Form bilden die gelben Kanten? Drehe oben (<b>U</b>) und den Würfel, bis dein Bild genau so aussieht.</p>
  <div class="ogrid g3">%s</div>
  <div class="tip"><b>Bekannt?</b> Den Spruch für die Linie hast du schon in Schritt 5 der ersten Anleitung gelernt. Beim <b>Punkt</b> machst du zwei Sprüche hintereinander. Nach dem ersten entsteht ein Haken vorne rechts. Den macht der zweite Spruch (mit f) zum Kreuz. Dazu musst du nichts drehen.</div>
  <div class="done"><b>Fertig, wenn:</b> Oben ein gelbes Kreuz liegt. Die Ecken dürfen noch alles sein.</div>
  <div class="note">Hast du schon das Kreuz? Dann gleich weiter zu den Ecken auf der nächsten Seite.</div>
</section>''' % (head(3, 'Oben alles gelb', 'Erst das Kreuz, dann die Ecken', svg_cube(S, 'top', 96, colors=masked(S, lambda p, n, v: is_center(p) or p[1] <= 0 or n == (0, 1, 0))), 'Phase 3 von 4'), oc))
corn = "".join(ocard(n, a, h, oll_img(a, 140)) for n, a, h in OLL7)
pages.append('''<section class="page"><h1 class="ptitle">OLL, Blick 2: die Ecken</h1>
  <p class="lead">Jetzt hast du oben ein gelbes Kreuz. Ziel: Alle vier Ecken zeigen auch mit Gelb nach oben. Es gibt <b>7 Fälle</b>. Drehe oben (<b>U</b>) und den Würfel, bis dein Bild so aussieht wie eins hier.</p>
  <div class="ogrid g4">%s</div>
  <div class="tip"><b>Tipp zum Erkennen:</b> Zähle zuerst, wie viele Ecken <b>oben</b> gelb sind. Eine Ecke: Sune oder Anti-Sune. Zwei Ecken: U-Form, T oder L. Keine Ecke: Pi oder H. Dann vergleichst du nur noch die Bilder.</div>
  <div class="done"><b>Fertig, wenn:</b> Die ganze obere Seite ist gelb. Auch wenn die Seiten noch nicht passen.</div>
  <div class="note">Bleibt nach einem Spruch noch ein Fall übrig? Dann schaust du einfach nochmal hin. Das ist das <b>2-look</b>.</div>
</section>''' % corn)

# ================================================================= PLL
def pcard(name, alg, hint, img, extra=''):
    return '<div class="ocase">%s<h3>%s</h3><div class="small">%s%s</div><div class="aw">%s</div></div>' % (img, name, hint, extra, alg_text(alg))
hl = headlights(PLLC[0][1])
pc = "".join(pcard(n, a, h, pll_img(a, 150), (' Halte die Scheinwerfer <b>%s</b>.' % hl) if n == 'A-Perm' and hl else '') for n, a, h in PLLC)
pe = "".join(pcard(n, a, h, pll_img(a, 150)) for n, a, h in PLLE)
pages.append('''<section class="page">%s
  <p class="lead">Oben ist jetzt alles gelb. Aber die Steine sitzen noch nicht am richtigen Platz. Auch hier schaust du zweimal hin. Erst die <b>Ecken</b>, dann die <b>Kanten</b>.</p>
  <h2 class="h2">Blick 1: Die Ecken an den Platz</h2>
  <p>Suche einen <b>Scheinwerfer</b>: Zwei Ecken nebeneinander, die an der Seite die <b>gleiche Farbe</b> haben. Gibt es einen, halte ihn <b>hinten</b> und mach den A-Perm. Gibt es keinen, mach den Y-Perm (egal wie du hältst). Danach drehst du oben (<b>U</b>), bis alle Ecken zu ihren Mittelsteinen passen.</p>
  <div class="ogrid g2">%s</div>
  <h2 class="h2">Blick 2: Die Kanten an den Platz</h2>
  <p>Jetzt passen alle Ecken. Schau auf die Kanten. Welches Bild siehst du? Hat eine Seite schon <b>drei richtige Streifen</b>, halte sie hinten und nimm einen U-Perm. Passt das Bild noch nicht, drehe den Würfel in der Hand, bis es passt.</p>
  <div class="ogrid g4">%s</div>
  <div class="done"><b>Geschafft, wenn:</b> Alles passt. Drehe oben (<b>U</b>) noch kurz, bis die Seiten zu den Mittelsteinen passen (AUF).</div>
</section>''' % (head(4, 'Oben alles an den Platz', 'Erst die Ecken, dann die Kanten', goal(8, 96), 'Phase 4 von 4'), pc, pe))

# ================================================================= TRAINING
pages.append('''<section class="page">
  <h1 class="ptitle">So wirst du schneller</h1>
  <p class="lead">CFOP lernt man nicht an einem Tag. Mach es in kleinen Schritten. Jeden Tag 10 Minuten bringen mehr als einmal im Monat eine Stunde.</p>
  <h2 class="h2">Dein Plan für 4 Wochen</h2>
  <div class="plan">
    <div style="--c:#1565D8"><b>Woche 1</b><h3>Cross</h3><p>Löse nur das Kreuz unten. 10 Mal pro Tag. Versuche, es in unter 8 Zügen zu schaffen. Plane es vorher im Kopf.</p></div>
    <div style="--c:#D7263D"><b>Woche 2</b><h3>F2L</h3><p>Kreuz und dann ein Pärchen. Später zwei, drei, vier. Fang mit den leichten Fällen an.</p></div>
    <div style="--c:#E0A800"><b>Woche 3</b><h3>OLL</h3><p>Lerne die 3 Kreuz-Sprüche und die 7 Ecken-Sprüche. Lerne einen pro Tag.</p></div>
    <div style="--c:#16A34A"><b>Woche 4</b><h3>PLL</h3><p>Lerne die 6 Sprüche. Dann löse ganze Würfel von Anfang bis Ende.</p></div>
  </div>
  <h2 class="h2">Tricks, die wirklich helfen</h2>
  <div class="words">
    <div><b>Langsam ist schnell</b><p>Dreh am Anfang ruhig und sauber. Tempo kommt von ganz allein.</p></div>
    <div><b>Nicht absetzen</b><p>Mach zwischen den Phasen keine Pause. Dreh weiter, auch wenn du noch nicht weißt, was kommt.</p></div>
    <div><b>Vorausschauen</b><p>Such das nächste Pärchen, während du das aktuelle einsetzt. Das ist der größte Unterschied zu Anfängern.</p></div>
    <div><b>Zeit stoppen</b><p>Schreib deine Zeiten auf. Du wirst sehen, wie sie jede Woche sinken.</p></div>
    <div><b>Würfel pflegen</b><p>Ein leichtgängiger Würfel mit etwas Würfel-Öl macht das Drehen viel leichter.</p></div>
    <div><b>Mit anderen üben</b><p>Wettkämpfe in der Familie machen Spaß. Wer löst schneller, Mama oder Papa?</p></div>
  </div>
  <div class="win"><svg width="1" height="1"></svg><div><h2>Du schaffst das!</h2><p>Am Anfang stolperst du, das ist ganz normal. Mit Übung wirst du immer flüssiger. Viel Spaß beim Üben!</p></div></div>
</section>''')

# ================================================================= CHEAT SHEET
def mini(name, alg, img):
    return '<div class="mini">%s<b>%s</b><div class="aw">%s</div></div>' % (img, name, alg_text(alg))
ollcells = mini('Linie', LINE, oll_img(LINE, 100)) + mini('Haken', HOOK, oll_img(HOOK, 100)) + mini('Punkt', DOT, oll_img(DOT, 100, pre=move(S, invert(DOT)))) + "".join(mini(n, a, oll_img(a, 100)) for n, a, h in OLL7)
pllcells = "".join(mini(n, a, pll_img(a, 118)) for n, a, h in PLLC + PLLE)
pages.append('''<section class="page cheat"><h1 class="ptitle">Spickzettel CFOP</h1>
  <div class="mm"><b>1. Cross:</b> Weißes Kreuz unten, ohne Gänseblümchen. <b>2. F2L:</b> Ecke und Kante als Pärchen vorne rechts einsetzen. <b>3. OLL:</b> oben alles gelb (Kreuz, dann Ecken). <b>4. PLL:</b> oben alles an den Platz (Ecken, dann Kanten).</div>
  <h3 class="ch" style="color:#B58900">OLL: oben alles gelb</h3><div class="minigrid">%s</div>
  <h3 class="ch" style="color:#16A34A">PLL: oben alles an den Platz</h3><div class="minigrid g3">%s</div>
</section>''' % (ollcells, pllcells))

CSS2 = CSS + '''
.overview.o4 { grid-template-columns: repeat(4, 1fr); }
.cfop4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 8px 0 4px; }
.cfop4 div { background: #F4F6FA; border-top: 6px solid var(--c); border-radius: 14px; padding: 8px 10px; text-align: center; }
.cfop4 b { display: block; font-size: 36px; font-weight: 900; color: var(--c); line-height: 1.1; }
.cfop4 span { display: block; font-weight: 800; font-size: 13px; }
.cfop4 i { font-style: normal; font-size: 12.5px; color: #4b5563; }
.h2 { font-size: 20px; font-weight: 850; margin: 14px 0 6px; }
.cmp { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.cmp th { text-align: left; background: #1b1f27; color: #fff; padding: 6px 10px; }
.cmp th:first-child { border-radius: 10px 0 0 0; } .cmp th:last-child { border-radius: 0 10px 0 0; }
.cmp td { padding: 6px 10px; border-bottom: 2px solid #E5E7EB; }
.cmp td:last-child { background: #FDF2F8; }
.learn, .plan { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.learn div { background: #F4F6FA; border-radius: 14px; padding: 8px 10px; } .learn p { margin: 2px 0 0; font-size: 12.5px; }
.words { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; }
.words div { background: #F4F6FA; border-radius: 14px; padding: 8px 12px; } .words p { margin: 2px 0 0; font-size: 13px; }
.words .algtxt { font-size: 14px; }
.notgrid.n3 { grid-template-columns: repeat(3, 1fr); }
.pairidea { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 6px; }
.plan div { background: #F4F6FA; border-top: 6px solid var(--c); border-radius: 14px; padding: 8px 10px; }
.plan b { color: var(--c); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; } .plan p { font-size: 12.5px; margin: 0; }
.ogrid { display: grid; gap: 10px; margin: 6px 0; }
.ogrid.g2 { grid-template-columns: repeat(2, 1fr); } .ogrid.g3 { grid-template-columns: repeat(3, 1fr); } .ogrid.g4 { grid-template-columns: repeat(4, 1fr); }
.ocase { background: #F4F6FA; border-radius: 14px; padding: 8px 8px 10px; display: flex; flex-direction: column; align-items: center; text-align: center; }
.ocase h3 { margin: 4px 0 2px; font-size: 15px; } .ocase .small { font-size: 11.5px; margin-bottom: 4px; }
.aw { margin-top: auto; padding-top: 3px; } .aw .algtxt { white-space: normal; display: inline-block; font-size: 13.5px; line-height: 1.25; padding: 2px 6px; letter-spacing: .03em; }
.ogrid.g4 .aw .algtxt { font-size: 12px; }
.ocase .strip.tight { margin-top: 4px; gap: 0; } .ocase .strip .mv b { font-size: 11px; } .ocase .strip .mvnum { display: none; }
.minigrid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; } .minigrid.g3 { grid-template-columns: repeat(3, 1fr); } .minigrid.g3 .aw .algtxt { font-size: 11.5px; }
.mini { background: #F4F6FA; border-radius: 10px; padding: 4px 4px 6px; text-align: center; display: flex; flex-direction: column; align-items: center; font-size: 11.5px; }
.mini .aw .algtxt { font-size: 9.5px; padding: 1px 3px; border-width: 1.5px; letter-spacing: .01em; }
.ch { margin: 10px 0 4px; font-size: 16px; } .mm { background: #FFF6CC; border-radius: 12px; padding: 6px 12px; font-size: 13px; }
.win svg { display: none; }
.cover .title { font-size: 44px; }
'''
html = '<!doctype html><html lang="de"><head><meta charset="utf-8"><title>CFOP lernen</title><style>%s</style></head><body>%s</body></html>' % (CSS2, "\n".join(pages))
open(os.path.join(HERE, '..', 'guides', 'cfop.html'), 'w').write(html)
print("pages:", len(pages), "headlights A-perm:", hl)

