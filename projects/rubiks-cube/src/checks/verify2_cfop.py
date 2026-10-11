from cube import *
S = solved()
def lower_bad(st): return [k for k,v in st.items() if k[0][1] <= 0 and v != S[k]]
def ypat(st):
    return "".join(("Y" if st[((x,1,z),FACE_N['U'])]=='Y' else ".") + ("\n" if x==1 else "") for z in (-1,0,1) for x in (-1,0,1))
# dot
a = "F R U R' U' F' f R U R' U' f'"
t = move(S, invert(a)); print("dot combo lower bad:", len(lower_bad(t))); print(ypat(t))
mid = move(t, "F R U R' U' F'"); print("after first alg:"); print(ypat(mid))
# PLL
names = {
 'Aa':"l' U R' D2 R U' R' D2 R2", 'Y':"F R U' R' U' R U R' F' R U R' U' R' F R F'",
 'Ua':"R2 U R U R' U' R' U' R' U R'", 'Ub':"R U' R U R U R U' R' U' R2",
 'H':"M2 U M2 U2 M2 U M2", 'Z':"M' U' M2 U' M2 U' M' U2 M2", 'T':"R U R' U' R' F R2 U' R' U' R U R' F'",
 'E':"R' U R' D2 R U' R' D2 R2",
}
home = {}
def piece_cols(st,p): return frozenset(st[(p,n)] for (pp,n) in st if pp==p)
U_POS = [(x,1,z) for x in (-1,0,1) for z in (-1,0,1) if (x,z)!=(0,0)]
def perm(st):
    h = {p: piece_cols(S,p) for p in U_POS}
    out = []
    for p in U_POS:
        src = [q for q in U_POS if h[q]==piece_cols(st,p)][0]
        if src!=p: out.append((src,p))
    return out
nm = {(1,1,1):'UFR',(-1,1,1):'UFL',(1,1,-1):'UBR',(-1,1,-1):'UBL',(0,1,1):'UF',(0,1,-1):'UB',(1,1,0):'UR',(-1,1,0):'UL'}
for k,a in names.items():
    try:
        t = move(S, a)
    except KeyError as e:
        print(k,"bad token",e); continue
    topok = all(t[((x,1,z),FACE_N['U'])]=='Y' for x in (-1,0,1) for z in (-1,0,1))
    print(k, "lower bad:",len(lower_bad(t)), "top yellow:",topok, "perm:", [(nm[a_],nm[b_]) for a_,b_ in perm(t)])
