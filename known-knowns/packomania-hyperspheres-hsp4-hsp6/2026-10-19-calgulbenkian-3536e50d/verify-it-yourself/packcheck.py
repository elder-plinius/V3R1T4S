#!/usr/bin/env python3
"""Standard-library checker for a packing of N equal balls (or spheres) in a container.

Definition checked (from the target's success criterion):
  r* = min( min_{i<j} |c_i - c_j| / 2 , wall ),
  wall = 1/2 - max_i max_k |c_ik|            for the cube [-1/2, 1/2]^3   (--kind cube)
  wall = 1 - max_i |c_i|                      for the unit ball            (--kind ball)
Coordinates are read as exact decimal fractions (scaled integers); every one of the N(N-1)/2
squared distances is computed exactly in integers; only the final square roots use decimal
arithmetic (60 digits). There is no tolerance and no floating-point screen.

Usage:
  python3 packcheck.py --kind cube|ball --dim D --object FILE [--expect-n N]
        [--table-radius R --margin M] [--posted FILE] [--iso-tol T]
Prints one line of key=value facts per item and a last line beginning with RESULT.
"""
import sys, math, argparse
from decimal import Decimal, getcontext
getcontext().prec = 60


def load(path, d):
    """Return (header, rows) with rows as lists of strings. Accepts an optional single-number
    header line, '#' comment lines, and an optional leading integer index column."""
    header = None
    rows = []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            t = line.split()
            if len(t) == 1 and not rows and header is None:
                header = t[0]
                continue
            is_index = t[0].lstrip('-').isdigit() and int(t[0]) == len(rows) + 1   # integer text, equals the row number
            if len(t) == d + 1 and is_index:
                t = t[1:]
            elif len(t) == d + 2 and is_index:
                t = t[1:-1]   # Packomania layout: index, d coordinates, radius
            elif len(t) == d and is_index:
                t = t[1:]     # index followed by only d-1 coordinates: reported as a column mismatch
            rows.append((ln, t))
    return header, rows


def scale_rows(rows, S):
    out = []
    for _, t in rows:
        r = []
        for x in t:
            neg = x.startswith('-')
            x = x.lstrip('+-')
            a, _, b = x.partition('.')
            v = int(a or '0') * 10 ** S + int((b + '0' * S)[:S] if len(b) <= S else b[:S])
            if len(b) > S:
                raise ValueError("internal scale error")
            r.append(-v if neg else v)
        out.append(r)
    return out


def sqrt_dec(n_int, S):
    """sqrt(n_int / 10^(2S)) as Decimal."""
    return Decimal(n_int).sqrt() / (Decimal(10) ** S)


def squared_distances(P):
    n = len(P)
    out = []
    for i in range(n):
        pi = P[i]
        for j in range(i + 1, n):
            pj = P[j]
            s = 0
            for a, b in zip(pi, pj):
                t = a - b
                s += t * t
            out.append(s)
    return out


def analyse(path, kind, d, S=None):
    header, rows = load(path, d)
    ncols = {len(t) for _, t in rows}
    if ncols != {d}:
        raise ValueError("%s: coordinate columns found %s, expected %d" % (path, sorted(ncols), d))
    maxdec = 1
    for _, t in rows:
        for x in t:
            if '.' in x:
                maxdec = max(maxdec, len(x.split('.')[1]))
    if S is None:
        S = maxdec
    P = scale_rows(rows, S)
    n = len(P)
    D2 = squared_distances(P)
    dmin2 = min(D2)
    rpair = sqrt_dec(dmin2, S) / 2
    if kind == 'cube':
        half = Decimal(1) / 2
        wall = half - Decimal(max(abs(x) for p in P for x in p)) / (Decimal(10) ** S)
    else:
        mx = max(sum(x * x for x in p) for p in P)
        wall = 1 - sqrt_dec(mx, S)
    r = min(rpair, wall)
    return dict(header=header, N=n, S=S, npairs=len(D2), r_pair=rpair, wall=wall, r_star=r,
                binding='wall' if wall < rpair else 'pair', D2=D2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kind', required=True, choices=['cube', 'ball'])
    ap.add_argument('--dim', required=True, type=int)
    ap.add_argument('--object', required=True)
    ap.add_argument('--expect-n', type=int)
    ap.add_argument('--table-radius')
    ap.add_argument('--margin')
    ap.add_argument('--posted')
    ap.add_argument('--baseline-radius')
    ap.add_argument('--iso-tol', default='1e-8')
    a = ap.parse_args()
    d = a.dim
    ok = True
    iso_note = ''
    res = analyse(a.object, a.kind, d)
    N = res['N']
    print("object_points N=%d dim=%d decimals_scale=%d" % (N, d, res['S']))
    print("pairs_examined=%d pairs_expected=%d" % (res['npairs'], N * (N - 1) // 2))
    if res['npairs'] != N * (N - 1) // 2:
        ok = False
    if a.expect_n is not None and N != a.expect_n:
        print("N_mismatch expected=%d" % a.expect_n)
        ok = False
    if res['header'] is not None:
        print("object_header_radius=%s" % res['header'])
    print("r_pair_half_min_distance=%s" % format(res['r_pair'], '.30f'))
    print("r_wall=%s" % format(res['wall'], '.30f'))
    print("r_star=%s" % format(res['r_star'], '.30f'))
    print("binding=%s" % res['binding'])
    if res['r_star'] <= 0:
        ok = False
    if a.table_radius:
        tr = Decimal(a.table_radius)
        gain = res['r_star'] - tr
        print("table_radius=%s" % a.table_radius)
        print("gain_over_table=%s" % format(gain, '.15e'))
        if a.margin:
            m = Decimal(a.margin)
            good = gain >= m
            print("gain_at_least_margin(%s)=%s" % (a.margin, good))
            ok = ok and good
    if a.baseline_radius:
        b = Decimal(a.baseline_radius)
        print("baseline_radius=%s" % a.baseline_radius)
        print("gain_over_baseline=%s" % format(res['r_star'] - b, '.15e'))
        ok = ok and (res['r_star'] > b)
        print("greater_than_baseline=%s" % (res['r_star'] > b))
    if a.posted:
        try:
            ph, prows = load(a.posted, d)
            pc = {len(t) for _, t in prows}
            if pc != {d}:
                print("posted_file_columns=%s expected=%d: isometry comparison NOT possible" % (sorted(pc), d))
                posted_ok = None
                iso_note = ' (isometry test with the posted file not possible: column mismatch)'
            else:
                S2 = max(res['S'], 12)
                # rescale both to a common scale
                S = max(res['S'], max(len(x.split('.')[1]) for _, t in prows for x in t if '.' in x))
                A = analyse(a.object, a.kind, d, S)
                B = analyse(a.posted, a.kind, d, S)
                print("posted_points N=%d posted_header_radius=%s posted_r_star=%s" % (B['N'], B['header'], format(B['r_star'], '.15f')))
                if A['N'] != B['N']:
                    print("posted_point_count_differs (object %d, posted %d): sorted distance multisets differ" % (A['N'], B['N']))
                    posted_ok = True
                else:
                    sa = sorted(A['D2']); sb = sorted(B['D2'])
                    scale2 = float(10) ** (2 * S)
                    mxd = 0.0
                    for x, y in zip(sa, sb):
                        diff = abs(math.sqrt(x / scale2) - math.sqrt(y / scale2))
                        if diff > mxd:
                            mxd = diff
                    print("max_abs_sorted_distance_difference=%.6e" % mxd)
                    posted_ok = mxd > float(a.iso_tol)
                    print("differs_from_posted_by_more_than_%s=%s" % (a.iso_tol, posted_ok))
        except ValueError as e:
            print("posted_comparison_error: %s" % e)
            posted_ok = None
        if posted_ok is False:
            ok = False
    print("RESULT %s%s" % ("PASS" if ok else "FAIL", iso_note))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
