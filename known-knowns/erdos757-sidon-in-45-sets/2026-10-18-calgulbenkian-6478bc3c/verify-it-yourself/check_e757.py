"""Independent Erdos 757 check, written from the definition (standard library only).

Usage: python3 check_e757.py SET.json [--expect-s S] [--expect-n N]
SET.json has the integer set under the key "A" (other keys are ignored).

Computed:
 (1) the (4,5)-property: every 4-subset has at least 5 distinct values among its six absolute differences (exhaustive);
 (2) the exact maximum Sidon subset size s(A), by TWO independent exact methods:
     (a) bitmask branch-and-bound over the forbidden relations (a+b = c+d with {a,b} != {c,d}, a = b allowed);
     (b) exhaustive enumeration of all 2^n subsets, testing each against the same relations
         (the relations are listed from the sums directly; method (b) does not use any bound).
     No ILP solver is used in this package.
 (3) the ratio s/|A| as a fraction, compared with 4/7 and 9/17.
"""
import json, sys
from itertools import combinations
from fractions import Fraction

def load(path):
    A = sorted(json.load(open(path))['A'])
    assert len(set(A)) == len(A), "repeated element"
    return A

def four_five(A):
    bad = 0
    for q in combinations(A, 4):
        if len({abs(a - b) for a, b in combinations(q, 2)}) < 5:
            bad += 1
    return bad

def relations(A):
    """Bitmasks of the index sets {i,j,k,l} (or 3 indices when a=b) such that A[i]+A[j] = A[k]+A[l] for two distinct pairs."""
    n = len(A)
    sums = {}
    for i in range(n):
        for j in range(i, n):
            sums.setdefault(A[i] + A[j], []).append((i, j))
    rel = set()
    for prs in sums.values():
        for p, q in combinations(prs, 2):
            rel.add((1 << p[0]) | (1 << p[1]) | (1 << q[0]) | (1 << q[1]))
    return sorted(rel)

def sidon_bb(A, rel):
    """(a) branch and bound. Elements are decided in index order; a relation mask is violated once all of its bits are chosen."""
    n = len(A)
    by_top = [[] for _ in range(n)]   # relations whose highest index is i
    for r in rel:
        by_top[r.bit_length() - 1].append(r)
    best = [0]
    def rec(i, chosen, cnt):
        if cnt + (n - i) <= best[0]:
            return
        if i == n:
            best[0] = cnt
            return
        m = chosen | (1 << i)
        if all((r & m) != r for r in by_top[i]):
            rec(i + 1, m, cnt + 1)
        rec(i + 1, chosen, cnt)
    rec(0, 0, 0)
    return best[0]

def sidon_exhaustive(A, rel):
    """(b) all 2^n subsets, no pruning on size other than skipping subsets no larger than the best seen (which cannot change the maximum)."""
    n = len(A)
    best = 0
    for m in range(1 << n):
        c = bin(m).count('1')
        if c <= best:
            continue
        ok = True
        for r in rel:
            if (r & m) == r:
                ok = False
                break
        if ok:
            best = c
    return best

def analyse(A, with_exhaustive=True):
    n = len(A)
    bad = four_five(A)
    rel = relations(A)
    s_bb = sidon_bb(A, rel)
    s_ex = sidon_exhaustive(A, rel) if with_exhaustive else None
    return n, bad, len(rel), s_bb, s_ex

def main():
    args = sys.argv[1:]
    A = load(args[0])
    exp_s = int(args[args.index('--expect-s') + 1]) if '--expect-s' in args else None
    exp_n = int(args[args.index('--expect-n') + 1]) if '--expect-n' in args else None
    n, bad, nrel, s_bb, s_ex = analyse(A)
    ratio = Fraction(s_bb, n)
    print(f"n={n} bad_4_subsets={bad} relations={nrel} s_branch_and_bound={s_bb} s_exhaustive_2^n={s_ex} ratio={ratio} "
          f"n_multiple_of_14={n % 14 == 0} ratio<4/7={ratio < Fraction(4,7)} ratio==4/7={ratio == Fraction(4,7)} ratio>=9/17={ratio >= Fraction(9,17)}")
    ok = bad == 0 and s_bb == s_ex and ratio >= Fraction(9, 17)
    if exp_s is not None: ok = ok and s_bb == exp_s
    if exp_n is not None: ok = ok and n == exp_n
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
