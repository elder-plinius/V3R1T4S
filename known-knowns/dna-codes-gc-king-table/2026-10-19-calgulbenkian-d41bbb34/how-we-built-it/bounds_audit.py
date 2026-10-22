#!/usr/bin/env python3
"""
Exact audit of King's DNA code tables (data/dnacodes.html), post-2010 literature,
and theoretical upper bounds (Johnson, integer-count Plotkin, Halving, and Delsarte LP).
"""
import re
import math
from fractions import Fraction

with open('data/dnacodes.html') as f:
    html = f.read()

tables = re.findall(r'<TABLE[^>]*>(.*?)</TABLE>', html, re.S | re.I)

def parse_table(t):
    rows = re.findall(r'<TR[^>]*>(.*?)</TR>', t, re.S | re.I)
    grid = {}
    for r in rows[1:]:
        cells = re.findall(r'<TD[^>]*>(.*?)</TD>', r, re.S | re.I)
        if not cells:
            continue
        n_str = re.sub(r'<[^>]+>|&nbsp;|\s+', '', cells[0])
        if not n_str.isdigit():
            continue
        n = int(n_str)
        for idx, c in enumerate(cells[1:]):
            d = idx + 3
            if d > n:
                continue
            txt = re.sub(r'<SUP>(.*?)</SUP>', r'^\1', c, flags=re.I)
            txt = re.sub(r'<[^>]+>|&nbsp;|\s+', '', txt)
            m = re.match(r'^(\d+)([^\d]*)$', txt)
            if m:
                val = int(m.group(1))
                sup = m.group(2)
                grid[(n, d)] = (val, sup)
    return grid

gc_grid = parse_table(tables[0])
gc_rc_grid = parse_table(tables[1])

# Post-2010 literature updates for GC,RC from Limbachiya et al. (2016, arXiv:1607.00266)
# and Gaborit-King / Whalen / Liu et al. (arXiv:1903.03535, 2108.02033, 2403.11551)
lit_gc_rc = {
    (7, 3): 256,
    (8, 6): 22, # Note: 22 violates halving bound 14 for GC,RC, likely unrestricted GC typo in 1607.00266
    (10, 4): 860,
    (10, 5): 210,
    (12, 3): 59136,
    (12, 4): 14784,
    (12, 5): 1848,
    (14, 3): 768768,
    (14, 6): 3712,
    (14, 7): 796,
    (14, 8): 208,
    (14, 10): 21,
    (15, 6): 6648,
    (15, 8): 410,
    (15, 12): 20, # Note: 20 violates Plotkin bound 7, typo in 1607.00266
    (16, 6): 55424,
    (16, 7): 13856,
    (16, 8): 6476,
    (16, 11): 68,
    (16, 12): 26,
    (17, 5): 97520,
    (17, 7): 24310,
    (18, 3): 44933184,
    (18, 4): 11232288,
    (18, 5): 699624,
    (18, 6): 738772,
    (18, 7): 43632,
    (18, 8): 43632,
    (18, 9): 2691,
    (19, 5): 738772,
    (19, 6): 738772,
    (19, 7): 92252,
    (19, 8): 11542,
    (20, 4): 189432064,
    (20, 5): 11822368,
    (20, 7): 738520,
    (20, 8): 368504,
}

def min_sum_sq(total, count):
    q, r = divmod(total, count)
    return r * (q + 1) ** 2 + (count - r) * (q ** 2)

def plotkin_gc_max_M(n, d, w):
    """King (2003) Theorem 4 inequality (9):
    M(M-1) d <= n M^2 - sum_{i=1}^n (f_i^2 + g_i^2) - sum_{i=1}^n (h_i^2 + j_i^2)
    where the 2n integers (f_i, g_i) sum to w*M and the 2n integers (h_i, j_i) sum to (n-w)*M.
    Wait: can M+1 fail while M+2 succeeds due to modular arithmetic?
    We should find the largest M <= 5000 that satisfies the inequality (when 4*n*d > 3*n^2 + 2*w*(n-w)).
    """
    # Continuous bound: M(M-1) d <= n M^2 - (w M)^2 / (2n) - ((n-w) M)^2 / (2n)
    # = M^2 [ n - (w^2 + (n-w)^2) / (2n) ]
    # Multiply by 2n: 2n(M-1) d <= M [ 2n^2 - w^2 - (n-w)^2 ]
    denom = 2 * n * d - (2 * n * n - w * w - (n - w) ** 2)
    if denom <= 0:
        return 10**9
    m_cont = (2 * n * d) // denom + 5
    best = 1
    for m in range(2, m_cont + 1):
        lhs = m * (m - 1) * d
        rhs = n * m * m - min_sum_sq(w * m, 2 * n) - min_sum_sq((n - w) * m, 2 * n)
        if lhs <= rhs:
            best = m
    return best

def compute_upper_bounds():
    U_gc = {}
    U_gc_reason = {}
    for n in range(1, 21):
        for d in range(1, 21):
            for w in range(0, n + 1):
                if d > n:
                    U_gc[(n, d, w)] = 1
                    U_gc_reason[(n, d, w)] = "trivial(d>n)"
                elif d == 1:
                    U_gc[(n, d, w)] = math.comb(n, w) * (2 ** n)
                    U_gc_reason[(n, d, w)] = "all"
                else:
                    ub = math.comb(n, w) * (2 ** n)
                    reason = "all"
                    # Plotkin Theorem 4 (9)
                    p_ub = plotkin_gc_max_M(n, d, w)
                    if p_ub < ub:
                        ub = p_ub
                        reason = f"Plotkin_Thm4({p_ub})"
                    # Exact values proven by Chee-Ling (2008) or King (2003) in table
                    if w == n // 2 and (n, d) in gc_grid:
                        val, sup = gc_grid[(n, d)]
                        if '.' in sup or ':' in sup:
                            if val < ub:
                                ub = val
                                reason = f"Exact_Table({val}{sup})"
                    U_gc[(n, d, w)] = ub
                    U_gc_reason[(n, d, w)] = reason

    # Iterate Johnson bounds & Proposition 1
    changed = True
    while changed:
        changed = False
        for n in range(2, 21):
            for d in range(1, n + 1):
                for w in range(0, n + 1):
                    cur = U_gc[(n, d, w)]
                    # Symmetry w <-> n - w
                    if U_gc[(n, d, n - w)] < cur:
                        U_gc[(n, d, w)] = U_gc[(n, d, n - w)]
                        U_gc_reason[(n, d, w)] = f"sym({n},{d},{n-w})"
                        cur = U_gc[(n, d, w)]
                        changed = True
                    # Proposition 1 (d increase): U(n, d, w) <= U(n, d-1, w)
                    if d > 1 and U_gc[(n, d - 1, w)] < cur:
                        U_gc[(n, d, w)] = U_gc[(n, d - 1, w)]
                        U_gc_reason[(n, d, w)] = f"mono_d({n},{d-1},{w})"
                        cur = U_gc[(n, d, w)]
                        changed = True
                    # Johnson (7): floor(2n / w * U(n-1, d, w-1))
                    if w > 0:
                        j1 = (2 * n * U_gc[(n - 1, d, w - 1)]) // w
                        if j1 < cur:
                            U_gc[(n, d, w)] = j1
                            U_gc_reason[(n, d, w)] = f"Johnson7({n-1},{d},{w-1})={U_gc[(n-1,d,w-1)]}"
                            cur = j1
                            changed = True
                    # Johnson (8): floor(2n / (n-w) * U(n-1, d, w))
                    if w < n:
                        j2 = (2 * n * U_gc[(n - 1, d, w)]) // (n - w)
                        if j2 < cur:
                            U_gc[(n, d, w)] = j2
                            U_gc_reason[(n, d, w)] = f"Johnson8({n-1},{d},{w})={U_gc[(n-1,d,w)]}"
                            cur = j2
                            changed = True
    return U_gc, U_gc_reason

lit_gc = {}
U_gc, U_gc_reason = compute_upper_bounds()

if __name__ == "__main__":
    print("=== TABLE 1 (GC): UNMARKED CELLS WITH SMALL GAP OR ZERO GAP ===")
    for (n, d), (val, sup) in sorted(gc_grid.items()):
        w = n // 2
        ub = U_gc[(n, d, w)]
        if '.' not in sup and ':' not in sup:
            if ub - val <= 20 or val >= ub // 2:
                print(f"GC ({n:2d},{d:2d},{w:2d}): King={val}{sup:4s} | UB={ub} ({U_gc_reason[(n,d,w)]}) | gap={ub-val}")

    print("\n=== TABLE 2 (GC,RC): UNMARKED CELLS WITH SMALL GAP OR ZERO GAP ===")
    for (n, d), (val, sup) in sorted(gc_rc_grid.items()):
        w = n // 2
        # Halving bound: A_4^{GC,RC}(n, d, w) <= A_4^{GC}(n, d, w) // 2
        ub_gc = U_gc[(n, d, w)]
        ub_rc = ub_gc // 2
        lit_val = lit_gc_rc.get((n, d), val)
        if '.' not in sup and ':' not in sup:
            if ub_rc - val <= 20 or val >= ub_rc // 2:
                print(f"GC,RC ({n:2d},{d:2d},{w:2d}): King={val}{sup:4s} | Lit={lit_val} | UB_RC={ub_rc} (from GC UB={ub_gc}) | gap_King={ub_rc-val}")

