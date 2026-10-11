from cube import *
import itertools
S = solved()
moves = ["U","U'","U2","F","F'","F2","R","R'","R2","L","L'","L2","B","B'","B2"]
need = [(( -1,-1,0),'D'),((1,-1,0),'D'),((0,-1,-1),'D')]
def okthree(st):
    return all(st[(p,FACE_N[f])]==S[(p,FACE_N[f])] for p,f in need) and all(st[(p,FACE_N[ff])]==S[(p,FACE_N[ff])] for p,f in need for ff in "LRFB" if (p,FACE_N[ff]) in S)
seen = {}
for L in range(1,4):
    for seq in itertools.product(moves, repeat=L):
        # skip same-face consecutive
        if any(seq[i][0]==seq[i+1][0] for i in range(L-1)): continue
        st = move(S, " ".join(seq))
        if not okthree(st): continue
        # DF edge piece: colors W,B
        for (p,n),c in st.items():
            pass
        pe = [p for p in set(k[0] for k in st) if sum(1 for c in p if c)==2 and frozenset(st[(p,n)] for (pp,n) in st if pp==p)==frozenset('WB')][0]
        wf = [n for (pp,n) in st if pp==pe and st[(pp,n)]=='W'][0]
        key = (pe, wf)
        if key not in seen: seen[key] = " ".join(seq)
for k,v in sorted(seen.items()): print(k, "scramble:", v, " -> solution:", invert(v))
