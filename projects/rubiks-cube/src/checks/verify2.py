from cube import *
import random
S = solved()
E = {'B':(0,1,-1),'L':(-1,1,0),'R':(1,1,0),'F':(0,1,1)}
def pat(st):
    return "".join(sorted(k for k,p in E.items() if st[(p,(0,1,0))]=='Y'))
oll = "F R U R' U' F'"
seen = {}
random.seed(1)
for i in range(400):
    st = S
    seq = " ".join(random.choice([oll, "U", "U'", "U2"]) for _ in range(random.randint(1,8)))
    st = move(S, seq)
    a = pat(st); b = pat(move(st, oll))
    seen.setdefault(a,set()).add(b)
for k in sorted(seen): print("before", k or "dot", "-> after", seen[k])

# step 6: Sune + U on edges. Which edges matched -> result
sune = "R U R' U R U2 R' U"
def edge_match(st):
    side = {'F':((0,1,1),'F'),'R':((1,1,0),'R'),'B':((0,1,-1),'B'),'L':((-1,1,0),'L')}
    return "".join(k for k,(p,f) in side.items() if st[(p,FACE_N[f])]==FACE_COLOR[f])
# generate states: random sequences of sune and U on solved; all keep F2L and cross
res = {}
for i in range(600):
    seq = " ".join(random.choice([sune, "U", "U'", "U2", "R U R' U R U2 R'"]) for _ in range(random.randint(1,10)))
    st = move(S, seq)
    a = edge_match(st); b = edge_match(move(st, sune))
    res.setdefault(a,set()).add(b)
for k in sorted(res): print("edges matched", k or "none", "-> after sune+U:", res[k])
