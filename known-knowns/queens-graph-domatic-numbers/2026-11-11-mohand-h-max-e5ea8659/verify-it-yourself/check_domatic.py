"""Standalone checker (Python standard library): is the grid a domatic partition of the n x n queens graph?
Definition: squares (r, c); two distinct squares are adjacent iff same row, same column or same diagonal
(|r - r'| = |c - c'|). A class D dominates iff every square is in D or adjacent to a square of D.
Usage: python3 check_domatic.py GRID EXPECTED_N EXPECTED_K EXPECTED_SHA256   (exit code 0 only on PASS)"""
import hashlib, sys

path, n_expected, k_expected, sha_expected = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
raw = open(path, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
print("sha256", sha, "OK" if sha == sha_expected else "MISMATCH")
ok = sha == sha_expected
try:
    rows = [[int(x) for x in line.split()] for line in raw.decode("ascii").splitlines() if line.strip()]
except ValueError:
    rows = []
n = len(rows)
ok = ok and n == n_expected and all(len(r) == n for r in rows)
labels = {}
if ok:
    for r in range(n):
        for c in range(n):
            labels.setdefault(rows[r][c], []).append((r, c))
    print("n =", n, "classes =", len(labels), "sizes =", sorted(len(v) for v in labels.values()))
    ok = len(labels) == k_expected and sum(len(v) for v in labels.values()) == n * n
    for lab, members in sorted(labels.items()):
        for r in range(n):
            for c in range(n):
                if not any((r, c) == (a, b) or r == a or c == b or abs(r - a) == abs(c - b) for a, b in members):
                    print("class", lab, "does not dominate square", (r, c))
                    ok = False
                    break
            else:
                continue
            break
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
