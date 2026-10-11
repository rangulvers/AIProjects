from cube import *
S = solved()
SLOT = {(1,-1,1),(1,0,1)}
def bad(st):  # bottom two layers wrong, ignoring FR slot pieces
    return [k for k,v in st.items() if k[0][1] <= 0 and v != S[k] and k[0] not in SLOT]
def show(st):
    # where are corner DFR piece and edge FR piece (by colours)?
    cc = frozenset(['W','B','R']); ec = frozenset(['B','R'])
    pc = [p for p in set(k[0] for k in st) if sum(1 for c in p if c)==3 and frozenset(st[(p,n)] for (pp,n) in st if pp==p)==cc][0]
    pe = [p for p in set(k[0] for k in st) if sum(1 for c in p if c)==2 and frozenset(st[(p,n)] for (pp,n) in st if pp==p)==ec][0]
    wf = [ (n) for (pp,n) in st if pp==pc and st[(pp,n)]=='W'][0]
    return pc, wf, pe
cands = ["R U R'","R U' R'","F' U' F","F' U F","U R U' R'","U' F' U F","R U2 R' U' R U R'","R U R' U' R U R'","F' U' F U F' U' F","R U' R' U R U' R'",
 "U R U' R' U' F' U F","U' R U R' U R U' R'","R U R' U2 R U' R'","R U2 R' U R U' R'","U' R U' R' U R U R'","R U' R' U2 F' U' F","F' U' F U2 R U R'","U F' U' F U' R U R'", "R U R' U' R U R' U' R U R'", "U' F' U2 F U' F' U F", "F' U F U' F' U F","R U' R' U' R U R'","R U R' U R U' R'","U R U R' U' R U' R'","U' R U2 R' U R U' R'","F R' F' R U R U' R'","R U' R' U F' U' F","U R U2 R' U' R U R'","U' R U R' U F' U' F"]
for a in cands:
    t = move(S, invert(a))
    b = bad(t)
    pc, wf, pe = show(t)
    print("%-28s bad=%d corner@%s white-face %s edge@%s" % (a, len(b), pc, wf, pe))
