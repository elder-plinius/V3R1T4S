#!/usr/bin/env python3
"""Coverage verifier that does not trust any tree enumerator (PREREG.v4):
for one certificate file of order n, (1) every line is a tree on n vertices with a labeling that passes
check_sem.check (bijection onto {1..n}, consecutive edge sums); (2) AHU centre-rooted canonical codes are pairwise distinct; (3) their number equals
A000055(n). Distinct isomorphism classes, all of them trees on n vertices, as many as A000055(n): every class is covered.
Canonical codes are stored as blake2b digests to bound memory."""
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
    nn, es, ls = line.rstrip("\n").split(";")[:3]
    nn = int(nn); n0 = n0 or nn
    if nn != n0: wrong_n += 1; continue
    edges = [tuple(map(int, x.split("-"))) for x in es.split(",")]
    if not is_tree(nn, edges): bad_tree += 1; continue
    h = hashlib.blake2b(canon(adj_of(nn, edges)).encode(), digest_size=16).digest()
    if h in seen: dup += 1
    seen.add(h)
    if not ls: nolab += 1; continue
    if not check(nn, edges, list(map(int, ls.split(","))))[0]: fails += 1
good = len(seen) == A[n0] == lines and not (bad_tree or nolab or fails or dup or wrong_n)
print("n=%d lines=%d distinct_canonical=%d A000055=%d not_tree=%d wrong_n=%d dup=%d unlabeled=%d label_failures=%d -> %s"
      % (n0, lines, len(seen), A[n0], bad_tree, wrong_n, dup, nolab, fails, "PASS" if good else "FAIL"))
