#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Is a claimed configuration a near copy, deletion or insertion of a published one? Python 3.8+, standard library only.

    python3 derivation_check.py CLAIM REF [REF ...] [--dim D] [--container box|ball|none] [--tol T | --rel-tol R]
                                [--share S] [--rotation-budget B]

Each file lists one point (sphere or circle centre) per line. Lines starting with # are skipped, and only rows with
the most common count of numbers are read, so a radius line drops out. A leading integer counter column and a
trailing constant column are removed (Packomania writes "index x y z radius"); the first D remaining numbers are the
coordinates (D from --dim, else all remaining columns of the claim file).

For every reference file it reports the share of claimed points that lie within the tolerance of a reference point,
and the share of reference points matched, under
  - the identity: deletion, insertion and a local polish keep most points in place;
  - every symmetry of the container about the origin (box: the 2^D D! signed coordinate permutations; ball: any
    rotation or reflection, found by the search described below);
  - the same after mapping each file to its own bounding box (a translated or rescaled copy).
When the two files have the same number of points it also compares their sorted pairwise distances, which no isometry
changes (a copy rotated by any angle, e.g. in a ball); they must agree to --iso-tol (default 1e-6) of the diameter,
because two different packings of the same N can agree to a few per cent. The default tolerance is 0.1 times the
reference's minimum point distance, so a match means the same structural position, not the same digits.

With --container ball both files must have the ball's centre at the origin. The search matches an anchor point of the
claim and its D-1 nearest neighbours to a reference point and D-1 of its neighbours with the same distances to the
origin and the same mutual distances (within twice the tolerance). Anchors whose distance to the origin is rare in the
reference go first. A proposal that matches half of a 12-point sample is refined by an orthogonal least-squares fit on
its matched pairs and scored on all points. At most --rotation-budget proposals (default 4000, 0 = off) are tried per
reference; the output gives the number tried and says when the budget was reached.

A share at or above --share (default 0.95) for both files is flagged as copy-like, deletion-like or insertion-like.
A flag is not a verdict. It means the claim should name that file as its starting point and credit its author,
and the bar is that file's value, not a new search. Lattice-like packings share positions by construction, so a flag
between two of them is weak evidence. Not covered: a rotated copy in a container other than a ball centred at the
origin (with --container none, rotations are not searched), and a copy moved by more than the tolerance at more than
1 - --share of its points.

Last line: "DERIVATION_CHECK: FLAG (<n>)" or "DERIVATION_CHECK: NONE". Exit status 0, or 2 with --strict on a flag.
"""
import argparse, bisect, itertools, math, os, re, sys

NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def number_rows(path):
    """Rows of numbers of a coordinate file, as strings: lines starting with # are skipped, and only rows of the most
    common length (at least 2 numbers) are kept, so a radius line or a count line drops out. A leading integer counter
    column and a trailing constant column are removed (Packomania writes 'index x y z radius')."""
    rows = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                nums = NUM.findall(s)
                if len(nums) >= 2:
                    rows.append(nums)
    if not rows:
        return []
    lengths = {}
    for r in rows:
        lengths[len(r)] = lengths.get(len(r), 0) + 1
    n = max(lengths, key=lambda k: (lengths[k], k))
    rows = [r for r in rows if len(r) == n]
    first = [r[0] for r in rows]
    if n > 2 and all(re.fullmatch(r"\d+", v) for v in first) and \
            [int(v) for v in first] == list(range(int(first[0]), int(first[0]) + len(first))):
        rows = [r[1:] for r in rows]
    if len(rows[0]) > 2 and len(rows) > 2 and len({float(r[-1]) for r in rows}) == 1:
        rows = [r[:-1] for r in rows]
    return rows


def guess_dim(path):
    rows = number_rows(path)
    if not rows:
        raise SystemExit("no coordinate rows in %s; pass --dim" % path)
    return len(rows[0])


def read_points(path, dim):
    rows = number_rows(path)
    if rows and len(rows[0]) < dim:
        raise SystemExit("%s has %d coordinate columns, fewer than --dim %d" % (path, len(rows[0]), dim))
    return [tuple(float(v) for v in r[:dim]) for r in rows]


def dist(p, q):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def min_distance(pts):
    """Smallest pairwise distance (grid search, about linear time for packings)."""
    n = len(pts)
    if n < 2:
        return float("inf")
    d = len(pts[0])
    lo = [min(p[k] for p in pts) for k in range(d)]
    hi = [max(p[k] for p in pts) for k in range(d)]
    span = max(h - l for l, h in zip(lo, hi)) or 1.0
    h = span / max(1.0, n ** (1.0 / d))
    best = float("inf")
    while True:
        grid = {}
        for i, p in enumerate(pts):
            grid.setdefault(tuple(int(math.floor((p[k] - lo[k]) / h)) for k in range(d)), []).append(i)
        offs = list(itertools.product((-1, 0, 1), repeat=d))
        for key, idx in grid.items():
            for o in offs:
                nb = grid.get(tuple(a + b for a, b in zip(key, o)))
                if not nb:
                    continue
                for i in idx:
                    for j in nb:
                        if j > i:
                            best = min(best, dist(pts[i], pts[j]))
        if best <= h:
            return best
        h *= 2.0  # no pair closer than the cell size found yet: widen the cells and retry


class Index:
    """Points hashed on a grid with cell size 2 tol, for 'is there a point within tol?' queries. A point within tol of
    p lies, along each axis, in p's cell or in the neighbouring cell on the side of p's nearer cell boundary, so 2^d
    cells are searched."""

    def __init__(self, pts, tol):
        self.pts, self.tol = pts, tol
        self.size = 2.0 * tol
        self.d = len(pts[0])
        self.grid = {}
        for i, p in enumerate(pts):
            self.grid.setdefault(tuple(int(math.floor(v / self.size)) for v in p), []).append(i)

    def nearest(self, p):
        axes = []
        for v in p:
            x = v / self.size
            c = int(math.floor(x))
            axes.append((c, c - 1) if x - c < 0.5 else (c, c + 1))
        best, bi = None, -1
        for key in itertools.product(*axes):
            for i in self.grid.get(key, ()):
                dd = dist(p, self.pts[i])
                if dd <= self.tol and (best is None or dd < best):
                    best, bi = dd, i
        return bi, best


def box_symmetries(d):
    for perm in itertools.permutations(range(d)):
        for signs in itertools.product((1, -1), repeat=d):
            yield perm, signs


def apply(sym, p):
    if isinstance(sym, list):  # an orthogonal matrix from the rotation search
        return tuple(sum(row[k] * p[k] for k in range(len(p))) for row in sym)
    perm, signs = sym
    return tuple(signs[k] * p[perm[k]] for k in range(len(p)))


def bbox_normalise(pts):
    d = len(pts[0])
    lo = [min(p[k] for p in pts) for k in range(d)]
    hi = [max(p[k] for p in pts) for k in range(d)]
    mid = [(a + b) / 2 for a, b in zip(lo, hi)]
    s = max(b - a for a, b in zip(lo, hi)) or 1.0
    return [tuple((p[k] - mid[k]) / s for k in range(d)) for p in pts]


def match(claim, index, sym=None):
    hit_claim, hit_ref, shift = 0, set(), 0.0
    for p in claim:
        q = apply(sym, p) if sym else p
        i, dd = index.nearest(q)
        if i >= 0:
            hit_claim += 1
            hit_ref.add(i)
            shift = max(shift, dd)
    return hit_claim, len(hit_ref), shift


def matched_pairs(claim, index, sym):
    pairs = []
    for i, p in enumerate(claim):
        j, _ = index.nearest(apply(sym, p))
        if j >= 0:
            pairs.append((i, j))
    return pairs


def kind_of(hc, hr, nc, nr, share):
    """The flag for hc of nc claim points and hr of nr reference points matched, or None."""
    if hc / nc >= share and hr / nr >= share:
        return "copy-like" if nc == nr else ("deletion-like" if nc < nr else "insertion-like")
    if nc < nr and hc / nc >= share:
        return "deletion-like (%d of the reference's points not used)" % (nr - hr)
    if nc > nr and hr / nr >= share:
        return "insertion-like (%d claim points not in the reference)" % (nc - hc)
    return None


def mat_inv(a):
    """Inverse of a small square matrix (Gauss-Jordan with partial pivoting), or None if it is singular."""
    n = len(a)
    m = [[float(v) for v in row] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[piv][c]) < 1e-300:
            return None
        m[c], m[piv] = m[piv], m[c]
        f = m[c][c]
        m[c] = [v / f for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                g = m[r][c]
                m[r] = [x - g * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def orthogonal_fit(src, dst):
    """The orthogonal matrix Q (a rotation or a reflection about the origin) that minimises the sum of |Q s - t|^2 over
    the pairs (s, t): the orthogonal polar factor of sum(t s^T), by the scaled Newton iteration
    Q <- (g Q + Q^-T / g) / 2 with g = sqrt(|Q^-1| / |Q|) (Frobenius norms).
    None when the pairs do not fix Q (fewer than d independent directions)."""
    d = len(src[0])
    m = [[sum(t[i] * s[j] for s, t in zip(src, dst)) for j in range(d)] for i in range(d)]
    norm = math.sqrt(sum(v * v for row in m for v in row))
    if norm == 0.0:
        return None
    q = [[v / norm for v in row] for row in m]
    for _ in range(100):
        inv = mat_inv(q)
        if inv is None:
            return None
        fro_q = math.sqrt(sum(v * v for row in q for v in row))
        g = math.sqrt(math.sqrt(sum(v * v for row in inv for v in row)) / fro_q)
        nq = [[(g * q[i][j] + inv[j][i] / g) / 2 for j in range(d)] for i in range(d)]  # scaled Newton (Higham)
        step = max(abs(nq[i][j] - q[i][j]) for i in range(d) for j in range(d))
        q = nq
        if step < 1e-15:
            break
    if max(abs(sum(q[k][i] * q[k][j] for k in range(d)) - (i == j)) for i in range(d) for j in range(d)) > 1e-9:
        return None
    return q


def neighbours(pts, h):
    """For each point, the (distance, index) pairs of the other points within h, nearest first."""
    d = len(pts[0])
    keys = [tuple(int(math.floor(v / h)) for v in p) for p in pts]
    grid = {}
    for i, key in enumerate(keys):
        grid.setdefault(key, []).append(i)
    offs = list(itertools.product((-1, 0, 1), repeat=d))
    out = []
    for i, p in enumerate(pts):
        near = []
        for o in offs:
            for j in grid.get(tuple(a + b for a, b in zip(keys[i], o)), ()):
                if j != i:
                    dd = dist(p, pts[j])
                    if dd <= h:
                        near.append((dd, j))
        near.sort()
        out.append(near)
    return out


def rotation_search(claim, ref, tol, md, share, budget=4000, anchors=12):
    """Search the rotations and reflections about the origin (the symmetries of a ball) for the best match of claim to
    ref. Each proposal comes from a local correspondence: an anchor point of the claim and its d-1 nearest neighbours,
    matched to a reference point and d-1 of its neighbours with the same distances to the origin and the same mutual
    distances (within 2 tol). A proposal that matches half of a small sample is refined on its matched pairs and scored
    on all points. Anchors with rare distances to the origin are tried first. Returns (score, Q, hc, hr, shift,
    proposals tried); score and Q are 0 and None when nothing matched."""
    d = len(claim[0])
    none = (0.0, None, 0, 0, 0.0, 0)
    if len(claim) < d or len(ref) < d:
        return none
    h = 1.6 * md
    nc, nr = neighbours(claim, h), neighbours(ref, h)
    norm_c = [math.sqrt(sum(v * v for v in p)) for p in claim]
    norm_r = [math.sqrt(sum(v * v for v in p)) for p in ref]
    order = sorted(range(len(ref)), key=lambda i: norm_r[i])
    keys = [norm_r[i] for i in order]
    w = 2 * tol

    def same_norm(x):
        return order[bisect.bisect_left(keys, x - w):bisect.bisect_right(keys, x + w)]

    cands = [i for i in range(len(claim)) if len(nc[i]) >= d - 1 and norm_c[i] > w]
    cands.sort(key=lambda i: (len(same_norm(norm_c[i])), i))
    chosen = []
    for i in cands:
        if all(dist(claim[i], claim[j]) >= 2 * md for j in chosen):
            chosen.append(i)
            if len(chosen) == anchors:
                break
    idx = Index(ref, tol)
    quick = claim[::max(1, len(claim) // 12)][:12]

    def sample_hits(q):  # matched points of the sample, stopping once half can no longer be reached
        hits, misses, cap = 0, 0, len(quick) - (len(quick) + 1) // 2
        for p in quick:
            if idx.nearest(apply(q, p))[0] >= 0:
                hits += 1
            else:
                misses += 1
                if misses > cap:
                    break
        return hits
    best, tried = none, 0
    for a in chosen:
        na = [j for _, j in nc[a][:d - 1]]
        src = [claim[a]] + [claim[j] for j in na]
        for b in same_norm(norm_c[a]):
            nb = [j for _, j in nr[b]]
            stack = [[]]
            while stack:
                sel = stack.pop()
                t = len(sel)
                if t < d - 1:
                    c = na[t]
                    for j in nb:
                        if j in sel or abs(norm_r[j] - norm_c[c]) > w or \
                                abs(dist(ref[b], ref[j]) - dist(claim[a], claim[c])) > w:
                            continue
                        if any(abs(dist(ref[j], ref[s]) - dist(claim[c], claim[na[u]])) > w for u, s in enumerate(sel)):
                            continue
                        stack.append(sel + [j])
                    continue
                tried += 1
                dst = [ref[b]] + [ref[j] for j in sel]
                q = orthogonal_fit(src, dst)
                if q is not None and all(dist(apply(q, x), y) <= tol for x, y in zip(src, dst)) and \
                        sample_hits(q) * 2 >= len(quick):
                    for _ in range(3):
                        pairs = matched_pairs(claim, idx, q)
                        q2 = orthogonal_fit([claim[i] for i, _ in pairs], [ref[j] for _, j in pairs]) \
                            if len(pairs) >= d else None
                        if q2 is None:
                            break
                        q = q2
                    hc, hr, sh = match(claim, idx, q)
                    score = min(hc / len(claim), hr / len(ref))
                    if score > best[0]:
                        best = (score, q, hc, hr, sh, tried)
                        if kind_of(hc, hr, len(claim), len(ref), share):
                            return best[:5] + (tried,)
                if tried >= budget:
                    return best[:5] + (tried,)
    return best[:5] + (tried,)


def sorted_pair_distances(pts):
    out = [dist(p, q) for p, q in itertools.combinations(pts, 2)]
    out.sort()
    return out


def fingerprint_gap(a, b):
    """Largest difference between the sorted pairwise distances of a and b: raw, and after scaling each list by its
    own largest distance. Also returns b's largest distance (its diameter)."""
    da, db = sorted_pair_distances(a), sorted_pair_distances(b)
    raw = max(abs(x - y) for x, y in zip(da, db))
    sa, sb = da[-1] or 1.0, db[-1] or 1.0
    scaled = max(abs(x / sa - y / sb) for x, y in zip(da, db))
    return raw, scaled, sb


def check(claim_path, ref_paths, dim=None, container="box", tol=None, rel_tol=0.1, share=0.95, iso_tol=1e-6,
          out=sys.stdout, max_pairs=2_000_000, rotation_budget=4000):
    dim = dim or guess_dim(claim_path)
    claim = read_points(claim_path, dim)
    if not claim:
        raise SystemExit("no points read from %s" % claim_path)
    print("claim: %s (%d points, dim %d)" % (claim_path, len(claim), dim), file=out)
    flags, md_claim = [], None
    for rp in ref_paths:
        ref = read_points(rp, dim)
        if not ref:
            print("ref %s: no points read, skipped" % rp, file=out)
            continue
        md = min_distance(ref)
        if md == 0 and not tol:
            print("ref %s: two reference points coincide, so --rel-tol gives no tolerance; pass --tol" % rp, file=out)
            continue
        t = tol if tol else rel_tol * md
        print("ref %s (%d points, min distance %.6g, tolerance %.3g)" % (rp, len(ref), md, t), file=out)
        best = None
        frames = [("identity", claim, ref, [None])]
        if container == "box":
            frames.append(("box symmetry", claim, ref, list(box_symmetries(dim))[1:]))
        cb, rb = bbox_normalise(claim), bbox_normalise(ref)
        t_b = (tol / max(max(p) - min(p) for p in zip(*ref)) if tol else rel_tol * min_distance(rb))
        frames.append(("bounding box", cb, rb, [None] + (list(box_symmetries(dim))[1:] if container == "box" else [])))
        for name, c, r, syms in frames:
            idx = Index(r, t if name != "bounding box" else t_b)
            for sym in syms:
                hc, hr, sh = match(c, idx, sym)
                score = min(hc / len(c), hr / len(r))
                if best is None or score > best[0]:
                    best = (score, name, sym, hc, hr, sh)
        score, name, sym, hc, hr, sh = best
        if container == "ball" and rotation_budget > 0 and not kind_of(hc, hr, len(claim), len(ref), share):
            if md_claim is None:
                md_claim = min_distance(claim)
            rs, q, rhc, rhr, rsh, tried = rotation_search(claim, ref, t, max(md, md_claim), share, rotation_budget)
            note = "%d proposals%s" % (tried, ", budget reached" if tried >= rotation_budget else "")
            if q is not None and rs > score:
                score, name, sym, hc, hr, sh = rs, "rotation or reflection about the origin (%s)" % note, None, \
                    rhc, rhr, rsh
            else:
                print("   rotations about the origin: no better match (%s)" % note, file=out)
        how = name + ("" if sym is None else " perm=%s signs=%s" % (list(sym[0]), list(sym[1])))
        print("   best: %s: %d/%d claim points matched (%.3f), %d/%d reference points (%.3f), largest shift %.3g"
              % (how, hc, len(claim), hc / len(claim), hr, len(ref), hr / len(ref), sh), file=out)
        kind = kind_of(hc, hr, len(claim), len(ref), share)
        if len(claim) == len(ref) >= 2 and len(claim) * (len(claim) - 1) // 2 <= max_pairs:
            raw, scaled, diam = fingerprint_gap(claim, ref)
            print("   sorted pairwise distances: largest gap %.3g (raw), %.3g (both scaled to unit diameter)"
                  % (raw, scaled), file=out)
            if kind is None and (raw <= iso_tol * diam or scaled <= iso_tol):
                kind = "isometric copy (sorted pairwise distances agree)" if raw <= iso_tol * diam else \
                    "similar copy (sorted pairwise distances agree after scaling)"
                score = 1.0
        if kind:
            flags.append((rp, kind, score))
            print("   FLAG: %s" % kind, file=out)
    if len(flags) > 1:
        top = max(flags, key=lambda f: f[2])
        print("closest reference: %s (matched share %.3f)" % (top[0], top[2]), file=out)
    if flags:
        print("DERIVATION_CHECK: FLAG (%d)" % len(flags), file=out)
    else:
        print("DERIVATION_CHECK: NONE", file=out)
    return flags


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("claim")
    ap.add_argument("refs", nargs="+")
    ap.add_argument("--dim", type=int)
    ap.add_argument("--container", choices=("box", "ball", "none"), default="box")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--tol", type=float, help="absolute tolerance (default: --rel-tol times the min distance)")
    g.add_argument("--rel-tol", type=float, default=0.1)
    ap.add_argument("--share", type=float, default=0.95)
    ap.add_argument("--iso-tol", type=float, default=1e-6,
                    help="isometry test: largest gap of the sorted pairwise distances, relative to the diameter")
    ap.add_argument("--rotation-budget", type=int, default=4000,
                    help="--container ball: most proposals tried by the rotation search per reference (0 = off)")
    ap.add_argument("--strict", action="store_true", help="exit 2 when anything is flagged")
    a = ap.parse_args(argv)
    for p in [a.claim] + a.refs:
        if not os.path.isfile(p):
            raise SystemExit("no such file: %s" % p)
    flags = check(a.claim, a.refs, a.dim, a.container, a.tol, a.rel_tol, a.share, a.iso_tol,
                  rotation_budget=a.rotation_budget)
    return 2 if (flags and a.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
