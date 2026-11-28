"""Independent checker: is the grid a domatic / idomatic / total domatic K-partition of the n x n queens graph?
Two distinct squares are adjacent iff they share a row, a column or a diagonal (any distance).
dom : every class C dominates: each square is in C or adjacent to a member of C.
idom: dom + each class is independent (no two members adjacent).
tdom: every square (members included) is adjacent to some OTHER member of C.
Usage: python -I check.py grid.txt dom|idom|tdom   (grid: n lines of n integer labels; K = number of labels)"""
import sys

def adj(a, b):
    (r1, c1), (r2, c2) = a, b
    return a != b and (r1 == r2 or c1 == c2 or r1 - c1 == r2 - c2 or r1 + c1 == r2 + c2)

def main():
    rows = [l.split() for l in open(sys.argv[1]) if l.strip()]
    kind = sys.argv[2]
    n = len(rows)
    assert all(len(r) == n for r in rows), 'not square'
    lab = {(r, c): int(rows[r][c]) for r in range(n) for c in range(n)}
    labels = sorted(set(lab.values()))
    classes = {L: [s for s in lab if lab[s] == L] for L in labels}
    bad = []
    for L, C in classes.items():
        for t in lab:
            if kind == 'tdom':
                ok = any(adj(s, t) for s in C)
            else:
                ok = lab[t] == L or any(adj(s, t) for s in C)
            if not ok:
                bad.append(('undominated', L, t))
                break
        if kind == 'idom' and any(adj(a, b) for i, a in enumerate(C) for b in C[i + 1:]):
            bad.append(('not independent', L))
    print('n=%d kind=%s K=%d classes sizes=%s' % (n, kind, len(labels), sorted(len(C) for C in classes.values())))
    print('PASS' if not bad else 'FAIL %s' % bad[:5])

main()
