#!/usr/bin/env python3
"""Coverage verifier that does not trust any tree enumerator (the rule frozen in the run's PREREG.md):
for one certificate file of order n, (1) every line is a tree on n vertices with a labeling that passes
check_sem.check; (2) AHU centre-rooted canonical codes are pairwise distinct; (3) their number equals
A000055(n). Distinct isomorphism classes, all of them trees on n vertices, as many as A000055(n): every class is covered.
A malformed line or an out-of-range vertex id counts as not_tree. Canonical codes are stored as blake2b digests to
bound memory. Standard library only. Usage: python3 verify_sem_coverage.py A000055_FILE CERT_FILE"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_sem import check
from verify_cert import canon, adj_of, is_tree
bfile, cf = sys.argv[1], sys.argv[2]
A = {int(l.split()[0]): int(l.split()[1]) for l in open(bfile) if l.strip() and not l.startswith("#")}
seen = set(); lines = 0; bad_tree = 0; nolab = 0; fails = 0; dup = 0; n0 = None; wrong_n = 0
for line in open(cf):
    if not line.strip(): continue
    lines += 1
    try:
        nn, es, ls = line.rstrip("\n").split(";")[:3]
        nn = int(nn)
        edges = [tuple(map(int, x.split("-"))) for x in es.split(",")]
        if any(len(e) != 2 for e in edges): raise ValueError("bad edge")
        labels = list(map(int, ls.split(","))) if ls else None
    except ValueError:
        bad_tree += 1; continue
    n0 = n0 or nn
    if nn != n0: wrong_n += 1; continue
    if not is_tree(nn, edges): bad_tree += 1; continue
    h = hashlib.blake2b(canon(adj_of(nn, edges)).encode(), digest_size=16).digest()
    if h in seen: dup += 1
    seen.add(h)
    if labels is None: nolab += 1; continue
    if not check(nn, edges, labels)[0]: fails += 1
good = n0 in A and len(seen) == A[n0] == lines and not (bad_tree or nolab or fails or dup or wrong_n)
print("n=%d lines=%d distinct_canonical=%d A000055=%d not_tree=%d wrong_n=%d dup=%d unlabeled=%d label_failures=%d -> %s"
      % (n0 or -1, lines, len(seen), A.get(n0, -1), bad_tree, wrong_n, dup, nolab, fails, "PASS" if good else "FAIL"))
sys.exit(0 if good else 1)
