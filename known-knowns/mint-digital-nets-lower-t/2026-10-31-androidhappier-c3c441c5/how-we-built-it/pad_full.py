#!/usr/bin/env python3
"""Complete each block of first-k rows (F_2) to a full m x m nonsingular generator matrix by appending unit
vectors e_c (in increasing c) that are not in the current row span. Rows 1..k are unchanged, so the t-value
(which depends only on rows 1..m-t) is unchanged.  Usage: pad_full.py IN OUT m s"""
import sys
inp,outp=sys.argv[1],sys.argv[2]; m,s=int(sys.argv[3]),int(sys.argv[4])
hdr=[];blocks=[];cur=[]
for line in open(inp):
    l=line.strip()
    if l.startswith('#'): hdr.append(l); continue
    if not l:
        if cur: blocks.append(cur); cur=[]
        continue
    cur.append(l)
if cur: blocks.append(cur)
assert len(blocks)==s
def tov(r): return int(r[::-1],2)
def tos(v): return ''.join('1' if v>>c&1 else '0' for c in range(m))
out=[]
for b in blocks:
    basis={}
    def red(v):
        while v:
            p=v.bit_length()-1
            if p not in basis: return v
            v^=basis[p]
        return 0
    rows=list(b)
    for r in rows:
        v=red(tov(r)); assert v, "first k rows dependent"
        basis[v.bit_length()-1]=v
    c=0
    while len(rows)<m:
        v=red(1<<c)
        if v: basis[v.bit_length()-1]=v; rows.append(tos(1<<c))
        c+=1
    out.append(rows)
with open(outp,'w') as f:
    f.write("# Generator matrices C_1..C_%d of a digital net over F_2, m = %d. Each block = one m x m matrix, row r = r-th row\n"%(s,m))
    f.write("# (row r gives digit r of the coordinate: digit_r(x_i) = <row_r(C_i), n> over F_2, n = digit vector of the point index).\n")
    f.write("# Rows 1..k are from the greedy construction; rows k+1..m are unit vectors completing C_i to a nonsingular matrix.\n")
    f.write("# source header: "+" | ".join(hdr)+"\n")
    for rows in out:
        for r in rows: f.write(r+'\n')
        f.write('\n')
