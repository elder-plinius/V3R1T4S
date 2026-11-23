#!/usr/bin/env python3
"""Audit of a Schutte CNF against Definition 2.1/2.2 of arXiv:2604.08790 (stdlib only, independent of the encoder).

Edge variables 1..E, E = m*C(n,2), in the order t, i, j (i < j): variable number of (t,i,j) is
1 + t*C(n,2) + (index of the pair (i,j) in lexicographic order); true means i -> j in T_t.
The audit finds every "domination" clause (all literals positive and above E) and checks, from the clauses alone:
  - each of its variables d occurs in exactly k binary clauses (-d or L) with L an edge literal, and nowhere else;
  - those k literals say "v beats u in T_t" for one (t, v) and a k-set U not containing v;
  - the clause's (t, v) pairs are exactly {(t, v): t < m, v not in U} for one U;
  - the U's of all domination clauses are exactly the C(n,k) k-subsets, each once.
Every other clause is reported as an added (symmetry-breaking) clause; it must not mention any d variable.
Prints AUDIT OK or AUDIT FAIL."""
import os, sys
from itertools import combinations
from collections import defaultdict

def main(path, m, k, n):
    pairs = list(combinations(range(n), 2)); P = len(pairs); E = m * P
    var_of = {}; edge = {}
    for t in range(m):
        for idx, (i, j) in enumerate(pairs):
            v = 1 + t * P + idx; var_of[t, i, j] = v; edge[v] = (t, i, j)
    def decode(lit):  # literal -> (t, winner, loser)
        t, i, j = edge[abs(lit)]
        return (t, i, j) if lit > 0 else (t, j, i)
    clauses = []
    with open(path) as f:
        for line in f:
            if line.startswith(("c", "p")) or not line.strip(): continue
            c = [int(x) for x in line.split()]; assert c[-1] == 0; clauses.append(c[:-1])
    occ = defaultdict(list)
    for ci, c in enumerate(clauses):
        for l in c: occ[abs(l)].append(ci)
    big = [ci for ci, c in enumerate(clauses) if all(l > E for l in c) and len(c) == m * (n - k)]
    seenU = set(); dvars = set(); base = set(big); errors = []
    for ci in big:
        Us = set(); tv = set()
        for d in clauses[ci]:
            dvars.add(d)
            others = [cj for cj in occ[d] if cj != ci]
            binl = []
            for cj in others:
                c = clauses[cj]
                if len(c) == 2 and -d in c:
                    L = c[0] if c[1] == -d else c[1]
                    if abs(L) <= E: binl.append(L); base.add(cj); continue
                errors.append(f"d={d} occurs in a non-defining clause {c[:6]}")
            if len(binl) != k: errors.append(f"d={d} has {len(binl)} defining clauses"); continue
            dec = [decode(L) for L in binl]
            ts = {x[0] for x in dec}; ws = {x[1] for x in dec}; U = frozenset(x[2] for x in dec)
            if len(ts) != 1 or len(ws) != 1 or len(U) != k: errors.append(f"d={d} not one (t,v) over a k-set"); continue
            t, v = ts.pop(), ws.pop()
            if v in U: errors.append(f"d={d}: dominator inside U")
            Us.add(U); tv.add((t, v))
        if len(Us) != 1: errors.append(f"clause {ci}: several U"); continue
        U = Us.pop()
        if tv != {(t, v) for t in range(m) for v in range(n) if v not in U}: errors.append(f"clause {ci}: wrong (t,v) set for U={sorted(U)}")
        if U in seenU: errors.append(f"U={sorted(U)} twice")
        seenU.add(U)
    allU = {frozenset(c) for c in combinations(range(n), k)}
    if seenU != allU: errors.append(f"k-sets covered {len(seenU)} of {len(allU)}")
    extra = [c for ci, c in enumerate(clauses) if ci not in base]
    bad_extra = [c for c in extra if any(abs(l) in dvars for l in c)]
    if bad_extra: errors.append(f"{len(bad_extra)} added clauses mention a domination variable")
    print(f"{os.path.basename(path)}: {len(clauses)} clauses; {len(big)} domination clauses over {len(seenU)} k-sets; "
          f"{len(base) - len(big)} defining clauses; {len(extra)} added clauses")
    if errors:
        print("first errors:", errors[:5]); print("AUDIT FAIL"); return 1
    print("AUDIT OK"); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))
