from cube import *
S = solved()
C = {'UFR':(1,1,1),'UFL':(-1,1,1),'UBR':(1,1,-1),'UBL':(-1,1,-1)}
def corner_cols(st,p):
    return frozenset(st[(p,n)] for (pp,n) in st if pp==p)
home = {k: corner_cols(S,p) for k,p in C.items()}
alg = "U R U' L' U R' U' L"
st = move(S, alg)
for k,p in C.items():
    cur = corner_cols(st,p)
    src = [kk for kk,v in home.items() if v==cur][0]
    print(k, "now holds piece from", src)
# rest intact?
bad = [k for k,v in st.items() if k[0][1] <= 0 and v != S[k]]
print("F2L disturbed:", len(bad))
edges_ok = all(st[k]==S[k] for k in st if k[0][1]==1 and sum(abs(c) for c in k[0])==2)
print("top edges intact:", edges_ok)

# orientation: (R' D' R D) x2 and x4 on UFR, D layer back after 6
x = "R' D' R D"
for k in (2,4,6):
    st = move(S, " ".join([x]*k))
    print(k, "UFR U-sticker:", st[((1,1,1),(0,1,0))], "D-layer ok:", all(st[q]==S[q] for q in st if q[0][1]==-1 ))
# full step-8 scenario: twist UFR cw & UBR ccw, solve with procedure
X = " ".join([x]*2) + " U " + " ".join([x]*4) + " U'"
st = move(S, X)
print("X restores all but 2 corners:", sum(1 for q in st if st[q]!=S[q]))
