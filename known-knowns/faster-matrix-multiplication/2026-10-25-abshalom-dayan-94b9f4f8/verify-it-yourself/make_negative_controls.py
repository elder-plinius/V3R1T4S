#!/usr/bin/env python3
"""Make two altered copies of the joined object for testing the checkers (standard library only).
Usage: make_negative_controls.py ASSEMBLED_DIR OUT_DIR
ASSEMBLED_DIR holds u.txt, v.txt, w.txt (what run_checks.sh joins); OUT_DIR gets neg_delete/ and neg_coef/.
neg_delete: term 1000 removed from all three files and the '# rank' header lowered by one.
neg_coef:   in u.txt the coefficient of the first entry of term 7 is replaced by that coefficient + 1 (an integer or p/q)."""
import sys, os
from fractions import Fraction
src, dst = sys.argv[1], sys.argv[2]
def load(w):
    lines = open(os.path.join(src, w + ".txt"), encoding="ascii").read().split("\n")
    if lines and lines[-1] == "": lines.pop()
    head = [l for l in lines if l.startswith("#")]
    body = [l for l in lines if not l.startswith("#")]
    return head, body
def save(d, w, head, body):
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, w + ".txt"), "w", encoding="ascii").write("\n".join(head + body) + "\n")
K = 1000
for w in "uvw":
    head, body = load(w)
    n = len(body)
    head2 = [("# rank %d" % (n - 1)) if h.startswith("# rank ") else h for h in head]
    save(os.path.join(dst, "neg_delete"), w, head2, body[:K] + body[K + 1:])
    if w == "u":
        t = body[7].split(" "); idx, c = t[0].split(":")
        t[0] = "%s:%s" % (idx, Fraction(c) + 1)
        b2 = list(body); b2[7] = " ".join(t)
        save(os.path.join(dst, "neg_coef"), w, head, b2)
    else:
        save(os.path.join(dst, "neg_coef"), w, head, body)
print("wrote", os.path.join(dst, "neg_delete"), "and", os.path.join(dst, "neg_coef"))
