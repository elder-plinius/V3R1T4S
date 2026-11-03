#!/usr/bin/env python3
"""Independent 9x9 central-game checker, written from the definition.
Board: 81 holes, columns a..i, rows 1..9 ("Standard 9x9 notation", Bell). Start: every hole filled except e5.
A jump: a peg moves two holes orthogonally over an adjacent peg into an empty hole; the jumped peg is removed.
Input: one move per line, written as hole-hole-...-hole (a peg's consecutive jumps). Blank lines and lines starting
with '#' are ignored. The move count is the number of MAXIMAL runs of consecutive jumps by the same peg (so two lines
where the second starts where the first ended are counted as one move, and reported).
Verdict VALID iff every jump is legal and the final position is exactly one peg, at e5.
usage: check9.py solution.txt [--claim-max K]"""
import sys
def parse(h):
    c=ord(h[0])-ord('a'); r=int(h[1:])-1
    if not(0<=c<9 and 0<=r<9): raise ValueError("bad hole "+h)
    return (c,r)
def name(p): return "%s%d"%(chr(ord('a')+p[0]),p[1]+1)
def main():
    path=sys.argv[1]; kmax=None
    if '--claim-max' in sys.argv: kmax=int(sys.argv[sys.argv.index('--claim-max')+1])
    peg={(c,r):True for c in range(9) for r in range(9)}; peg[(4,4)]=False
    jumps=[]
    for ln,line in enumerate(open(path),1):
        line=line.strip()
        if not line or line.startswith('#'): continue
        hs=[parse(x) for x in line.split('-')]
        if len(hs)<2: print("ILLEGAL line %d: no jump"%ln); return 1
        for a,b in zip(hs,hs[1:]): jumps.append((a,b,ln))
    last=None; moves=0
    for i,(a,b,ln) in enumerate(jumps):
        dc,dr=b[0]-a[0],b[1]-a[1]
        if not ((abs(dc)==2 and dr==0) or (abs(dr)==2 and dc==0)):
            print("ILLEGAL jump %d (line %d) %s-%s: not an orthogonal distance-2 jump"%(i+1,ln,name(a),name(b))); return 1
        m=(a[0]+dc//2,a[1]+dr//2)
        if not peg[a]: print("ILLEGAL jump %d %s-%s: no peg at start"%(i+1,name(a),name(b))); return 1
        if not peg[m]: print("ILLEGAL jump %d %s-%s: no peg jumped over"%(i+1,name(a),name(b))); return 1
        if peg[b]: print("ILLEGAL jump %d %s-%s: landing hole occupied"%(i+1,name(a),name(b))); return 1
        peg[a]=False; peg[m]=False; peg[b]=True
        if last!=a: moves+=1
        last=b
    left=[p for p in peg if peg[p]]
    print("jumps=%d moves=%d pegs_left=%d final=%s"%(len(jumps),moves,len(left),",".join(name(p) for p in sorted(left))))
    if len(left)!=1 or left[0]!=(4,4): print("INVALID: final position is not a single peg at e5"); return 1
    if kmax is not None and moves>kmax: print("INVALID: %d moves > claimed max %d"%(moves,kmax)); return 1
    print("VALID central game e5->e5 in %d moves"%moves); return 0
if __name__=='__main__': sys.exit(main())
