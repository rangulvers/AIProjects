from cube import *
S = solved()
def lower_ok(st, skip=()):
    return [k for k,v in st.items() if k[0][1] <= 0 and v != S[k] and k[0] not in skip]
def ypat(st):
    return "".join(("Y" if st[((x,1,z),FACE_N['U'])]=='Y' else ".") + ("\n" if x==1 else "") for z in (-1,0,1) for x in (-1,0,1))
# sanity of new moves
assert move(S,"M M' ") == S and move(S,"f f'")==S and move(S,"r2 r2")==S
assert move(S,"M2 M2")==S
# M follows L: M == L R' x'.. check: r = R M'
assert move(S,"r") == move(S,"R M'"), "r != R M'"
assert move(S,"l'") == move(S,"L' M'")
assert move(S,"f") == move(S,"F S")
print("wide ok")
algs = {
 'OLL line':"F R U R' U' F'", 'OLL hook':"F U R U' R' F'", 'OLL dot':"f R U R' U' f'",
 'sune':"R U R' U R U2 R'", 'anti':"R U2 R' U' R U' R'",
 'H':"F R U R' U' R U R' U' R U R' U' F'", 'Pi':"R U2 R2 U' R2 U' R2 U2 R",
 'U':"R2 D R' U2 R D' R' U2 R'", 'T':"r U R' U' r' F R F'", 'L':"F R' F' r U R U' r'",
}
for k,a in algs.items():
    t = move(S, invert(a))
    print("==",k,a,"| lower layers disturbed:",len(lower_ok(t)))
    print(ypat(t))
    cross = all(t[((x,1,z),FACE_N['U'])]=='Y' for x,z in ((0,1),(0,-1),(1,0),(-1,0)))
    corners = sum(1 for x in (-1,1) for z in (-1,1) if t[((x,1,z),FACE_N['U'])]=='Y')
    print("cross done:",cross," yellow-up corners:",corners)
