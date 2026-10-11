from cube import *
S = solved()
def show_U(st):
    # print U face as grid back->front
    for z in (-1,0,1):
        print("   ", " ".join(st[((x,1,z),(0,1,0))] for x in (-1,0,1)))
# basic sanity: each move ^4 = identity
for f in "UDLRFB":
    assert move(S, f+" "+f+" "+f+" "+f) == S
# sexy move order 6
assert move(S, "R U R' U' "*6) == S
print("sanity ok")

# --- Step 3 corners: corner at UFR above DFR. Generate the 3 orientations: apply inverse of (RUR'U')^k
for k in (1,3,5):
    st = move(S, invert(("R U R' U' "*k).strip()))
    # check where white of DFR corner piece is
    ufr = {f: st[((1,1,1),FACE_N[f])] for f in "UFR"}
    dfr_ok = all(st[((1,-1,1),FACE_N[f])] == FACE_COLOR[f] for f in "DFR")
    print("k=",k, "UFR corner:", ufr, "DFR solved?", dfr_ok)
    # check first layer other pieces intact after inverse? Verify solving: apply k reps -> solved
    assert move(st, ("R U R' U' "*k).strip()) == S

# --- Step 4 middle edges
right = "U R U' R' U' F' U F"
left = "U' L' U L U F U' F'"
for name, alg in (("right", right), ("left", left)):
    st = move(S, invert(alg))
    # locate edge pieces in U layer: print UF edge
    print(name, "UF edge: U=", st[((0,1,1),FACE_N['U'])], "F=", st[((0,1,1),FACE_N['F'])])
    # first two layers intact except target slot?
    bad = [k for k,v in st.items() if k[0][1] <= 0 and v != S[k]]
    print("  disturbed F2L stickers:", bad)
