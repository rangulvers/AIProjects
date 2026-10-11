from cube import *
import itertools, collections
S = solved()
C_POS = [(1,1,1),(-1,1,1),(1,1,-1),(-1,1,-1)]
E_POS = [(0,1,1),(0,1,-1),(1,1,0),(-1,1,0)]
def cc(st,p): return frozenset(st[(p,n)] for (pp,n) in st if pp==p)
def corners_solved_up_to_auf(st):
    for a in ["","U","U'","U2"]:
        t = move(st,a)
        if all(cc(t,p)==cc(S,p) for p in C_POS): return a
    return None
def edges_solved_up_to_auf(st):
    for a in ["","U","U'","U2"]:
        t = move(st,a)
        if all(cc(t,p)==cc(S,p) for p in E_POS): return a
    return None
A = "R' F R' B2 R F' R' B2 R2"; Y = "F R U' R' U' R U R' F' R U R' U' R' F R F'"
UA = "R2 U R U R' U' R' U' R' U R'"; UB = "R U' R U R U R U' R' U' R2"; H = "M2 U M2 U2 M2 U M2"; Z = "M' U M2 U M2 U M' U2 M2 U'"
T = "R U R' U' R' F R2 U' R' U' R U R' F'"
gens = [A, Y, UA, UB, H, Z, T, "U"]
def key(st):
    return tuple(sorted((p, tuple(sorted(st[(p,n)] for (pp,n) in st if pp==p))) for p in C_POS+E_POS)), tuple(st[((x,1,z),(0,1,0))] for x in (-1,0,1) for z in (-1,0,1))
# BFS all reachable LL permutation states
seen = {}
frontier = [S]
seen[key(S)] = S
while frontier:
    nf = []
    for st in frontier:
        for g in gens:
            t = move(st, g)
            k = key(t)
            if k not in seen:
                seen[k] = t; nf.append(t)
    frontier = nf
print("LL states:", len(seen))
def conj(alg, k):
    pre = ["","U","U2","U'"][k]; post = ["","U'","U2","U"][k]
    return (pre+" "+alg+" "+post).strip()
# Strategy: corner step. For each state find sequences of up to 2 corner-algs (A or Y, any rotation) solving corners.
res = collections.Counter(); details = {}
def hl_sides(st):
    out = []
    for f in "FRBL":
        n = FACE_N[f]
        ps = [p for p in C_POS if dot(p,n)==1]
        if st[(ps[0],n)]==st[(ps[1],n)]: out.append(f)
    return out
bad = 0
for k,st in seen.items():
    if corners_solved_up_to_auf(st) is not None:
        res['solved'] += 1; continue
    h = hl_sides(st)
    # rule: if headlights -> A with headlights at back (conjugate by U to rotate), else Y
    ok = False; trace = None
    for first in (["A","Y"]):
        for r in range(4):
            t = move(st, conj(A if first=="A" else Y, r))
            if corners_solved_up_to_auf(t) is not None:
                ok = True; trace=(first,r,len(h)); break
        if ok: break
    if not ok:
        # try A twice
        for r1 in range(4):
            t1 = move(st, conj(A, r1))
            for r2 in range(4):
                t2 = move(t1, conj(A, r2))
                if corners_solved_up_to_auf(t2) is not None:
                    ok=True; trace=("AA",r1,r2,len(h)); break
            if ok: break
    res[(trace[0] if trace else 'FAIL', len(h))] += 1
    if not ok: bad += 1
print(res, "fail:", bad)

print("---- mapping headlights side -> rotation r that works")
mp = collections.Counter()
for k,st in seen.items():
    if corners_solved_up_to_auf(st) is not None: continue
    h = hl_sides(st)
    if len(h)!=1: continue
    works = []
    for r in range(4):
        t = move(st, conj(A, r))
        if corners_solved_up_to_auf(t) is not None: works.append(r)
    mp[(h[0], tuple(works))] += 1
print(mp)
# A-perm: where are headlights in pre-state of A alone (inverse)?
pre = move(S, invert(A)); print("A pre headlights:", hl_sides(pre))
# After one A, does Y/no-headlights occur? also check edge step covers all
bad=0; cnt=collections.Counter()
for k,st in seen.items():
    t = st
    a = corners_solved_up_to_auf(t)
    if a is None:
        h = hl_sides(t)
        if h:
            # find correct r
            for r in range(4):
                t2 = move(t, conj(A,r))
                if corners_solved_up_to_auf(t2) is not None: t=t2; break
        else:
            for r in range(4):
                t2 = move(t, conj(Y,r))
                if corners_solved_up_to_auf(t2) is not None: t=t2; break
    a = corners_solved_up_to_auf(t)
    t = move(t, a)
    # now corners solved; edges: classify
    ea = edges_solved_up_to_auf(t)
    if ea is not None: cnt['edges solved']+=1; continue
    # edge step: try each of UA,UB,H,Z with rotation
    ok=False
    for name,alg in (("Ua",UA),("Ub",UB),("H",H),("Z",Z)):
        for r in range(4):
            t3 = move(t, conj(alg,r))
            a3 = corners_solved_up_to_auf(t3); e3 = edges_solved_up_to_auf(t3)
            # full solved up to AUF
            for au in ["","U","U'","U2"]:
                t4 = move(t3, au)
                if t4 == S:
                    ok=True; cnt[name]+=1; break
            if ok: break
        if ok: break
    if not ok: bad+=1; cnt['FAIL']+=1
print(cnt, "bad", bad)
