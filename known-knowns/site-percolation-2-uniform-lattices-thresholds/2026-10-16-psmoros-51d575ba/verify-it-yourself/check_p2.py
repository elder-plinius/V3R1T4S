#!/usr/bin/env python3
"""Standalone checker for the p2 claim on row #22 (bond) of Wikipedia's 2-uniform percolation table.

Python 3 standard library only. Run from the package folder:

    python3 -I -B verify-it-yourself/check_p2.py            (default: roots for W = 2..6)
    python3 -I -B verify-it-yourself/check_p2.py --wmax 7   (adds W = 7: about 5x the time of W = 2..6)

Written from the definitions, not from the claim's code:
  1. builds the row tiling TSS on a torus and counts vertex configurations from the faces of the embedded graph;
  2. computes the eigenvalue form of the Jacobsen-Scullard critical polynomial with its own transfer matrix
     (Lambda_open(p) = Lambda_closed(p) on W x infinity cylinders, Jacobsen 2015, arXiv 1507.03027, eq. 13), first on
     exact cases (square bond 1/2, triangular bond 2 sin(pi/18)), then the TSS roots p(W), compared with
     object/TSS_bond_roots.tsv to 1e-12 (and that file's state-count columns with this checker's state spaces), and
     the claim's calibration roots of the elongated triangular lattice (word TS, how-we-built-it/data/tm/TS_bond.tsv);
  3. checks that the tsv sequence is the one in object/p2_value.json, string for string;
  4. recomputes the PREREG rule-4 extrapolation and the PREREG.v2 error bar from the sequence and compares them with
     the JSON, and the TS calibration value against Scullard and Jacobsen's published 0.41964035886369(2);
  5. checks sigma <= 5e-8 and prints the comparison with the table value 0.44528611(40);
  6. checks the object files against the package's SHA256SUMS and INDEX.csv.
The last line is PASS only if every check holds, else FAIL.
"""
import hashlib
import json
import math
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

TSV = os.path.join("object", "TSS_bond_roots.tsv")
JSN = os.path.join("object", "p2_value.json")
CELL = os.path.join("the-record-we-beat", "cell.json")
TABLE_VALUE, TABLE_SIGMA = "0.44528611", "0.00000040"   # row #22 bond cell, "0.44528611(40) [citation needed]"
P2_SIGMA_MAX = 5e-8                                       # PREREG rule 9: stated sigma <= 5e-8 ("7 digits")
V2_FACTOR = Decimal("2.87")                               # PREREG.v2
TS_TSV = os.path.join("how-we-built-it", "data", "tm", "TS_bond.tsv")   # the claim's calibration roots (word TS)
# elongated triangular (3^3,4^2) = word TS, bond: 0.41964035886369(2), Scullard and Jacobsen 2020 (arXiv 1910.12376),
# Table I, "frieze" lattice, as quoted in the claim and read from the paper by the REPRODUCE skeptic
TS_REF = "0.41964035886369"

FAILS = []


def check(ok, msg):
    print(("ok    " if ok else "FAIL  ") + msg)
    if not ok:
        FAILS.append(msg)
    return ok


# ---------------------------------------------------------------------------------------------------------------
# The lattice: rows y, columns x = 0..W-1 (periodic). Every row has (x,y)-(x+1,y). A gap S between rows y and y+1
# adds (x,y)-(x,y+1); a gap T adds (x,y)-(x,y+1) and (x+1,y)-(x,y+1). Each edge carries its column displacement on
# the universal cover (old -> new for gap edges, x -> x+1 for row edges).

def gap_edges(g, W):
    """Edges of a gap: (old column, new column, displacement old->new in cover columns)."""
    out = [(x, x, 0) for x in range(W)]
    if g == "T":
        out += [((x + 1) % W, x, -1) for x in range(W)]
    elif g != "S":
        raise ValueError(g)
    return out


def row_edges(W):
    return [(x, (x + 1) % W, 1) for x in range(W)]


def vertex_configurations(word, W, periods):
    """Embed the periodic tiling on a W x (periods*len(word)) torus, trace faces, and classify vertices."""
    R = periods * len(word)
    # horizontal offset of row y in a drawing with regular polygons: crossing a T gap shifts by 1/2
    shift = [Fraction(0)]
    for y in range(R):
        shift.append(shift[-1] + (Fraction(1, 2) if word[y % len(word)] == "T" else 0))
    vid = lambda x, y: (y % R) * W + (x % W)
    darts = []   # (tail, head, gx, gy)
    for y in range(R):
        for a, b, d in row_edges(W):
            darts.append((vid(a, y), vid(b, y), Fraction(d), 0))
        for a, b, d in gap_edges(word[y % len(word)], W):
            darts.append((vid(a, y), vid(b, y + 1), d + shift[y + 1] - shift[y], 1))
    E = len(darts)
    darts += [(h, t, -gx, -gy) for (t, h, gx, gy) in darts]
    V = W * R
    rot = {v: [] for v in range(V)}
    for i, (t, h, gx, gy) in enumerate(darts):
        rot[t].append((math.atan2(gy, float(gx)), i))
    for v in rot:
        rot[v].sort()
        rot[v] = [i for _, i in rot[v]]
    rev = lambda i: i + E if i < E else i - E
    pos = {}
    for v in rot:
        for j, i in enumerate(rot[v]):
            pos[i] = (v, j)
    face_of, sizes = {}, []
    for start in range(2 * E):
        if start in face_of:
            continue
        f, i, n = len(sizes), start, 0
        while i not in face_of:
            face_of[i] = f
            n += 1
            v, j = pos[rev(i)]                      # at the head of dart i, its reverse sits at position j
            i = rot[v][(j - 1) % len(rot[v])]       # next dart clockwise: keeps the face on the left
        if i != start:
            raise RuntimeError("face tracing did not close")
        sizes.append(n)
    configs = {}
    angle_ok = True
    for v in range(V):
        seq = [sizes[face_of[i]] for i in rot[v]]
        cands = []
        for s in (seq, seq[::-1]):
            for k in range(len(s)):
                cands.append(tuple(s[k:] + s[:k]))
        c = min(cands)
        runs = []
        for a in c:
            if runs and runs[-1][0] == a:
                runs[-1][1] += 1
            else:
                runs.append([a, 1])
        name = ".".join("%d^%d" % (a, m) if m > 1 else "%d" % a for a, m in runs)
        configs[name] = configs.get(name, 0) + 1
        # interior angles of regular k-gons around the vertex must add to 360 degrees
        if sum(Fraction(180 * (k - 2), k) for k in seq) != 360:
            angle_ok = False
    return V, E, len(sizes), sorted(set(sizes)), configs, angle_ok


# ---------------------------------------------------------------------------------------------------------------
# Transfer matrix on the W x infinity cylinder (time = rows). A state is the connectivity of the live vertices
# (frontier) through the past.
#   closed sector: each live vertex also carries an integer lift k (its copy on the universal cover, cover column
#     X = x + W k); vertices of one cluster carry consistent lifts. An edge joining two vertices of the same cluster
#     with an inconsistent lift closes a non-contractible cycle: that history is killed (no cluster may wrap).
#   open sector: one marked cluster is connected to the far past; a history is killed when the marked cluster has no
#     live vertex left. (While it lives, no other cluster can wind around the cylinder, by planarity.)
# Lambda_closed and Lambda_open are the leading eigenvalues of the one-period transfer matrices (each edge present
# with probability p). The critical-polynomial root p(W) solves Lambda_open(p) = Lambda_closed(p).

def build_ops(word, W):
    """Operation list for one period of the word: ('add', pos), ('edge', i, j, wreq), ('del', i)."""
    order = lambda v: (0 if v[0] == "n" else 1, v[1])
    live = [("o", x) for x in range(W)]
    ops = []

    def edge(u, v, d):
        cu, cv = u[1], v[1]
        if (cu + d - cv) % W:
            raise RuntimeError("bad displacement")
        ops.append(("edge", live.index(u), live.index(v), (cu + d - cv) // W))

    for g in word:
        ge = gap_edges(g, W)
        last_use = {}
        for a, b, d in ge:
            last_use[a] = max(last_use.get(a, -1), b)
        for b in range(W):
            nv = ("n", b)
            live = sorted(live + [nv], key=order)
            ops.append(("add", live.index(nv)))
            for a, bb, d in ge:
                if bb == b:
                    edge(("o", a), nv, d)
            if b >= 1:
                edge(("n", b - 1), nv, 1)
            for a in range(W):
                if ("o", a) in live and last_use[a] <= b:
                    ops.append(("del", live.index(("o", a))))
                    live.remove(("o", a))
        if any(v[0] == "o" for v in live):
            raise RuntimeError("old vertex left over")
        edge(("n", W - 1), ("n", 0), 1)            # the seam edge of the new row
        live = [("o", v[1]) for v in live]
    if live != [("o", x) for x in range(W)]:
        raise RuntimeError("frontier layout changed over a period")
    return ops


# closed-sector states: tuple (label0, lift0, label1, lift1, ...), labels by first appearance, lift 0 at the first
# vertex of each cluster. open-sector states: tuple of labels, marked cluster = label 0, others by first appearance.

def canon_closed(labs, lifts):
    rl, base, out = {}, {}, []
    for l, k in zip(labs, lifts):
        if l not in rl:
            rl[l] = len(rl)
            base[l] = k
        out.append(rl[l])
        out.append(k - base[l])
    return tuple(out)


def canon_open(labs, mark):
    rl, out = {mark: 0}, []
    for l in labs:
        if l not in rl:
            rl[l] = len(rl)
        out.append(rl[l])
    return tuple(out)


def step_closed(op, s):
    labs, lifts = list(s[0::2]), list(s[1::2])
    if op[0] == "add":
        labs.insert(op[1], max(labs, default=-1) + 1)
        lifts.insert(op[1], 0)
        return canon_closed(labs, lifts)
    if op[0] == "del":
        del labs[op[1]]
        del lifts[op[1]]
        return canon_closed(labs, lifts)
    _, i, j, w = op
    li, lj = labs[i], labs[j]
    if li == lj:
        return s if lifts[j] - lifts[i] == w else None    # None: a non-contractible cycle closed
    sh = lifts[i] + w - lifts[j]
    for t in range(len(labs)):
        if labs[t] == lj:
            labs[t] = li
            lifts[t] += sh
    return canon_closed(labs, lifts)


def step_open(op, s):
    labs = list(s)
    if op[0] == "add":
        labs.insert(op[1], max(labs, default=-1) + 1)
        return canon_open(labs, 0)
    if op[0] == "del":
        del labs[op[1]]
        if 0 not in labs:
            return None                                    # the marked cluster died
        return canon_open(labs, 0)
    _, i, j, w = op
    li, lj = labs[i], labs[j]
    if li == lj:
        return s
    keep, gone = (li, lj) if li < lj else (lj, li)          # label 0 (marked) survives a merge
    labs = [keep if l == gone else l for l in labs]
    return canon_open(labs, 0)


class Sector:
    def __init__(self, word, W, kind):
        self.kind = kind
        ops = build_ops(word, W)
        step = step_closed if kind == "closed" else step_open
        init = canon_closed(list(range(W)), [0] * W) if kind == "closed" else tuple([0] * W)

        def images(op, s):
            t = step(op, s)
            if op[0] == "edge":
                return [s] + ([t] if t is not None else [])
            return [t] if t is not None else []

        # all period-boundary states reachable from the initial one
        S0, frontier = {init}, {init}
        while frontier:
            cur = frontier
            for op in ops:
                nxt = set()
                for s in cur:
                    nxt.update(images(op, s))
                cur = nxt
            frontier = cur - S0
            S0 |= frontier
        L0 = sorted(S0)
        self.n = len(L0)
        index0 = {s: i for i, s in enumerate(L0)}
        prog, cur = [], L0
        self.max_states = len(L0)
        for op in ops:
            if op[0] == "add":
                cur = [step(op, s) for s in cur]           # a bijection: indices unchanged
                continue
            if op[0] == "edge":
                nxt, where, src, dst = list(cur), {s: i for i, s in enumerate(cur)}, [], []
                for i, s in enumerate(cur):
                    t = step(op, s)
                    if t is None:
                        continue
                    if t not in where:
                        where[t] = len(nxt)
                        nxt.append(t)
                    src.append(i)
                    dst.append(where[t])
                prog.append(("edge", len(nxt), src, dst))
            else:
                nxt, where, src, dst = [], {}, [], []
                for i, s in enumerate(cur):
                    t = step(op, s)
                    if t is None:
                        continue
                    if t not in where:
                        where[t] = len(nxt)
                        nxt.append(t)
                    src.append(i)
                    dst.append(where[t])
                prog.append(("del", len(nxt), src, dst))
            cur = nxt
            self.max_states = max(self.max_states, len(cur))
        self.final = [index0[s] for s in cur]
        self.prog = prog
        self.vec = [1.0 / self.n] * self.n

    def apply(self, v, p):
        q = 1.0 - p
        for kind, nout, src, dst in self.prog:
            if kind == "edge":
                pv = [p * x for x in v]
                w = [q * x for x in v]
                if nout > len(w):
                    w.extend([0.0] * (nout - len(w)))
                for s, d in zip(src, dst):
                    w[d] += pv[s]
            else:
                w = [0.0] * nout
                for s, d in zip(src, dst):
                    w[d] += v[s]
            v = w
        out = [0.0] * self.n
        for x, d in zip(v, self.final):
            out[d] += x
        return out

    def leading(self, p, maxit=5000):
        """Perron eigenvalue by power iteration (warm start from the last call)."""
        v, lam_old, calm = self.vec, None, 0
        for _ in range(maxit):
            w = self.apply(v, p)
            lam = math.fsum(w)
            v = [x / lam for x in w]
            if lam_old is not None and abs(lam - lam_old) <= 1e-15 * lam:
                calm += 1
                if calm >= 3:
                    break
            else:
                calm = 0
            lam_old = lam
        else:
            raise RuntimeError("power iteration did not settle")
        self.vec = v
        return lam


def critical_root(word, W, p0, p1, tol=1e-15):
    """Root of Lambda_open(p) - Lambda_closed(p) by the secant method from p0, p1."""
    op_, cl_ = Sector(word, W, "open"), Sector(word, W, "closed")
    f = lambda p: op_.leading(p) - cl_.leading(p)
    f0, f1 = f(p0), f(p1)
    if not (f0 < 0 < f1):
        raise RuntimeError("no sign change of Lambda_open - Lambda_closed on [%r, %r]" % (p0, p1))
    for _ in range(60):
        p2 = p1 - f1 * (p1 - p0) / (f1 - f0)
        if abs(p2 - p1) <= tol:
            p1 = p2
            break
        p0, f0, p1, f1 = p1, f1, p2, f(p2)
        if f1 == 0.0:
            break
    else:
        raise RuntimeError("secant did not converge")
    return p1, (cl_.n, op_.n, cl_.max_states, op_.max_states)


# ---------------------------------------------------------------------------------------------------------------
# PREREG rule 4 and PREREG.v2 (Decimal arithmetic, 50 digits)

def fit3(Ws, ps):
    """Exact three-point fit p = pc + a W^-D; returns (pc, D)."""
    (w1, w2, w3), (p1, p2, p3) = [Decimal(w) for w in Ws], ps
    r = (p1 - p2) / (p2 - p3)
    lw1, lw2, lw3 = w1.ln(), w2.ln(), w3.ln()

    def g(D):
        a, b, c = (-D * lw1).exp(), (-D * lw2).exp(), (-D * lw3).exp()
        return (a - b) / (b - c) - r

    lo, hi = Decimal("0.01"), Decimal("60")
    glo, ghi = g(lo), g(hi)
    if glo * ghi > 0:
        raise RuntimeError("no exponent D fits %s" % (Ws,))
    for _ in range(170):
        mid = (lo + hi) / 2
        gm = g(mid)
        if (gm < 0) == (glo < 0):
            lo, glo = mid, gm
        else:
            hi = mid
    D = (lo + hi) / 2
    b, c = (-D * lw2).exp(), (-D * lw3).exp()
    a = (p2 - p3) / (b - c)
    return p3 - a * c, D


def solve_exact(Ws, ps, powers):
    """pc of the exact solve p(W) = pc + sum_k A_k W^-k over len(Ws) points (Fractions)."""
    rows = [[Fraction(1)] + [Fraction(1, w ** k) for k in powers] + [Fraction(p)] for w, p in zip(Ws, ps)]
    n = len(rows)
    for c in range(n):
        piv = next(r for r in range(c, n) if rows[r][c] != 0)
        rows[c], rows[piv] = rows[piv], rows[c]
        for r in range(n):
            if r != c and rows[r][c] != 0:
                f = rows[r][c] / rows[c][c]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[c])]
    return Decimal(rows[0][n].numerator) / Decimal(rows[0][n].denominator)


def sig3(x):
    return float("%.3e" % x)


def same_to_print(v, exact):
    """True if the JSON number v equals exact rounded to the decimals v is printed with."""
    t = repr(v)
    if "e" in t or "." not in t:
        return False
    n = len(t.split(".")[1])
    return abs(Decimal(t) - exact) <= Decimal(5) * Decimal(10) ** (-n - 1) + Decimal("1e-30")


# ---------------------------------------------------------------------------------------------------------------

def read_tsv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 5:
                raise ValueError("tsv line with %d columns" % len(parts))
            W, p, secs, n1, n2 = parts
            rows.append((int(W), p, float(secs), int(n1), int(n2)))
    return rows


def main():
    wmax = 6
    if "--wmax" in sys.argv:
        wmax = int(sys.argv[sys.argv.index("--wmax") + 1])
    t_start = time.time()
    print("V3R1T4S p2 checker: bond threshold of row #22, (2/3)(3^3,4^2) + (1/3)(4^4), row word TSS")
    print("python %s" % sys.version.split()[0])

    # 0. integrity of the object files against the package's own manifests
    print("\n[0] object files")
    sums = {}
    if os.path.isfile("SHA256SUMS"):
        for line in open("SHA256SUMS", encoding="utf-8"):
            parts = line.split()
            if len(parts) == 2:
                sums[os.path.normpath(parts[1].lstrip("*"))] = parts[0]
    for path in (TSV, JSN):
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        print("      %s sha256 %s" % (path, h))
        check(sums.get(os.path.normpath(path)) == h, "%s matches SHA256SUMS" % path)
    if os.path.isfile("INDEX.csv"):
        lines = open("INDEX.csv", encoding="utf-8").read().splitlines()
        head, row = lines[0].split(","), lines[1].split(",")
        rec = dict(zip(head, row))
        h = hashlib.sha256(open(JSN, "rb").read()).hexdigest()
        check(rec.get("file") == "object/p2_value.json" and rec.get("sha256") == h, "INDEX.csv sha256 of object/p2_value.json")
    else:
        check(False, "INDEX.csv present")

    obj = json.load(open(JSN, encoding="utf-8"))
    tsv = read_tsv(TSV)

    # 1. lattice identity
    print("\n[1] lattice identity: row tiling TSS built from its definition")
    V, E, F, fsizes, configs, angle_ok = vertex_configurations("TSS", 6, 2)
    fr = {k: Fraction(v, V) for k, v in configs.items()}
    print("      torus W=6 x 6 rows: V=%d E=%d F=%d face sizes %s" % (V, E, F, fsizes))
    print("      vertex configurations %s" % {k: str(v) for k, v in sorted(fr.items())})
    print("      z-bar = 2E/V = %s" % Fraction(2 * E, V))
    check(V - E + F == 0, "Euler characteristic V - E + F = 0 (torus)")
    check(fsizes == [3, 4] and angle_ok, "faces are triangles and squares, 360 degrees at every vertex")
    check(fr == {"3^3.4^2": Fraction(2, 3), "4^4": Fraction(1, 3)},
          "fractions (2/3) 3^3.4^2 + (1/3) 4^4, as in row #22")
    check(Fraction(2 * E, V) == Fraction(14, 3), "z-bar = 14/3 (table: 4 2/3)")
    check(obj.get("table_num") == 22 and obj.get("row_word") == "TSS" and obj.get("lattice") == "(2/3)(3^3,4^2) + (1/3)(4^4)",
          "JSON names table row 22, word TSS, lattice (2/3)(3^3,4^2) + (1/3)(4^4)")
    check(obj.get("target") == "site-percolation-2-uniform-lattices-thresholds" and obj.get("partial_win") == "p2"
          and obj.get("kind") == "p2", "JSON names bank target site-percolation-2-uniform-lattices-thresholds, partial win p2")
    for w, name in (("S", "4^4"), ("T", "3^6"), ("TS", "3^3.4^2")):
        c = vertex_configurations(w, 6, 2 if len(w) == 1 else 1)[4]
        check(list(c) == [name], "control: word %s gives only %s" % (w, name))

    # 2. transfer matrix: exact cases first, then the TSS roots
    print("\n[2] transfer matrix (Lambda_open = Lambda_closed on W x infinity cylinders)")
    exact = [("S", 0.5, "1/2", 0.45, 0.55, (2, 3, 4, 5)),
             ("T", 2 * math.sin(math.pi / 18), "2 sin(pi/18)", 0.33, 0.36, (2, 3, 4))]
    for word, val, label, lo, hi, Ws in exact:
        name = "square" if word == "S" else "triangular"
        for W in Ws:
            t0 = time.time()
            r, ns = critical_root(word, W, lo, hi)
            check(abs(r - val) <= 1e-12, "%s bond W=%d root %.17f vs %s = %.17f (diff %.1e, %.1fs)"
                  % (name, W, r, label, val, r - val, time.time() - t0))
    tsv_row = {row[0]: row for row in tsv}
    for W in range(2, wmax + 1):
        t0 = time.time()
        r, ns = critical_root("TSS", W, 0.4451, 0.4454)
        ref = float(tsv_row[W][1])
        check(abs(r - ref) <= 1e-12, "TSS bond W=%d root %.17f vs tsv %s (diff %.1e; %.1fs)"
              % (W, r, tsv_row[W][1], r - ref, time.time() - t0))
        # implementation-level cross-check: the tsv's last two columns are the largest intermediate state spaces of
        # the open and closed sectors; this checker, processing the edges in the same order, finds the same sizes
        check((tsv_row[W][3], tsv_row[W][4]) == (ns[3], ns[2]),
              "TSS W=%d largest state spaces open %d, closed %d = tsv columns 4-5 (%d, %d); period states %d"
              % (W, ns[3], ns[2], tsv_row[W][3], tsv_row[W][4], ns[0]))
    ts_rows = read_tsv(TS_TSV)
    ts_row = {row[0]: row for row in ts_rows}
    for W in (2, 3, 4):
        t0 = time.time()
        r, ns = critical_root("TS", W, 0.4185, 0.4205)
        ref = float(ts_row[W][1])
        check(abs(r - ref) <= 1e-12, "calibration TS bond W=%d root %.17f vs %s %s (diff %.1e; %.1fs)"
              % (W, r, TS_TSV, ts_row[W][1], r - ref, time.time() - t0))

    # 3. tsv sequence = JSON sequence, string for string
    print("\n[3] object/TSS_bond_roots.tsv against object/p2_value.json")
    seq = [(d["W"], d["p"]) for d in obj["sequence_tm"]]
    check(seq == [(W, p) for W, p, _, _, _ in tsv], "sequence_tm equals the tsv (W and p strings), %d widths" % len(seq))
    check([W for W, _ in seq] == list(range(2, 2 + len(seq))) and len(seq) >= 4, "widths are consecutive from 2")
    check(all(s >= 0 and n1 > 0 and n2 > 0 for _, _, s, n1, n2 in tsv), "tsv columns 3-5 are non-negative times and state counts")

    # 4. PREREG rule 4 and PREREG.v2
    print("\n[4] PREREG rule 4 and PREREG.v2 from the sequence")
    Ws = [W for W, _ in seq]
    ps = [Decimal(p) for _, p in seq]
    Wm = Ws[-1]
    d = [ps[i + 1] - ps[i] for i in range(len(ps) - 4, len(ps) - 1)]
    main_branch = (all(x < 0 for x in d) or all(x > 0 for x in d)) and abs(d[0]) > abs(d[1]) > abs(d[2])
    print("      last four widths %s: differences %s" % (Ws[-4:], ", ".join("%.4e" % x for x in d)))
    check(main_branch, "last four monotone with shrinking steps: rule 4 main branch")
    E1w = {}
    for k in range(0, 4):
        E1w[Wm - k] = fit3(Ws[-3 - k:len(Ws) - k], ps[-3 - k:len(ps) - k])
    E1, D1 = E1w[Wm]
    E2, D2 = E1w[Wm - 1]
    E3 = solve_exact(Ws[-4:], [p for _, p in seq][-4:], (4, 6, 8))
    sB = max(abs(E1 - E2), abs(E1 - E3))
    drift3 = max(abs(E1 - E1w[Wm - k][0]) for k in (1, 2, 3))
    sv2 = max(sB, drift3, V2_FACTOR * sB)
    print("      E1 (W=%d..%d) = %.15f  D = %.4f" % (Wm - 2, Wm, E1, D1))
    print("      E2 (W=%d..%d) = %.15f  D = %.4f" % (Wm - 3, Wm - 1, E2, D2))
    print("      E3 (pc + A W^-4 + B W^-6 + C W^-8, W=%d..%d) = %.15f" % (Wm - 3, Wm, E3))
    print("      sigma_B = max(|E1-E2| %.4e, |E1-E3| %.4e) = %.4e" % (abs(E1 - E2), abs(E1 - E3), sB))
    print("      E1 by window end W=%s: %s" % (",".join(str(Wm - k) for k in (3, 2, 1, 0)),
                                             ", ".join("%.15f" % E1w[Wm - k][0] for k in (3, 2, 1, 0))))
    print("      drift_3 = %.4e   2.87 sigma_B = %.4e   sigma_v2 = %.4e" % (drift3, V2_FACTOR * sB, sv2))
    b = obj["bond"]
    check(same_to_print(b["value"], E1), "JSON value %r = E1 to its printed digits (diff %.1e)" % (b["value"], Decimal(repr(b["value"])) - E1))
    check(b["sigma_rule4"] == sig3(sB), "JSON sigma_rule4 %r = sigma_B rounded (%.3e)" % (b["sigma_rule4"], sB))
    check(b["sigma_v2"] == sig3(sv2), "JSON sigma_v2 %r = sigma_v2 rounded (%.3e)" % (b["sigma_v2"], sv2))
    check(b["sigma"] == b["sigma_v2"], "JSON sigma is the PREREG.v2 sigma")
    m = b.get("method", "")
    check(m.startswith("E1 of PREREG rule 4 ") and "W=%d,%d,%d" % (Wm - 2, Wm - 1, Wm) in m and m.endswith("sigma by PREREG.v2"),
          "JSON method: E1 of PREREG rule 4 on W=%d,%d,%d, sigma by PREREG.v2" % (Wm - 2, Wm - 1, Wm))
    # calibration of the same pipeline: rule-4 E1 of the claim's TS roots against the published frieze value
    tseq = [(W, p) for W, p, _, _, _ in ts_rows]
    tW, tp = [W for W, _ in tseq], [Decimal(p) for _, p in tseq]
    tE1, tD = fit3(tW[-3:], tp[-3:])
    print("      calibration: TS E1 (W=%d..%d) = %.15f  D = %.4f; reference %s" % (tW[-3], tW[-1], tE1, tD, TS_REF))
    cal = obj.get("calibration_same_pipeline", {}).get("TS_bond", {})
    try:
        delta = Decimal(repr(cal["value"])) - Decimal(TS_REF)
        check(same_to_print(cal["value"], tE1), "JSON TS calibration value %r = E1 of %s to its printed digits" % (cal["value"], TS_TSV))
        check(cal["reference"] == TS_REF + "(2) Scullard-Jacobsen 2020", "JSON TS reference %r" % cal["reference"])
        check(cal["delta"] == sig3(delta) and abs(delta) <= Decimal("5e-8"),
              "JSON TS calibration delta %r = value - reference (%.3e), within 5e-8 (PREREG rule 9)" % (cal["delta"], delta))
    except (KeyError, ValueError, AttributeError, TypeError) as e:
        check(False, "JSON TS calibration block readable (%s)" % e)

    # 5. the p2 bar and the comparison with the table
    print("\n[5] p2 bar and table comparison")
    tv, ts = Decimal(TABLE_VALUE), Decimal(TABLE_SIGMA)
    if os.path.isfile(CELL):
        cell = json.load(open(CELL, encoding="utf-8"))
        check(cell.get("table_value") == "0.44528611(40)", "the-record-we-beat/cell.json table value 0.44528611(40)")
    check(obj.get("table_value", "").startswith("0.44528611(40)"), "JSON table_value 0.44528611(40)")
    check(sv2 <= Decimal(repr(P2_SIGMA_MAX)), "stated sigma %.3e <= 5e-8 (PREREG rule 9, '7 digits')" % sv2)
    delta = E1 - tv
    comb = (sv2 * sv2 + ts * ts).sqrt()
    print("      this value  %.9f(%d)   [E1 = %.15f, sigma %.3e]" % (E1, int((sv2 * Decimal("1e9")).quantize(Decimal("1"))), E1, sv2))
    print("      table value %s(40)  [Wikipedia, row #22 bond, 'citation needed']" % TABLE_VALUE)
    print("      delta = %+.4e   combined sigma = %.4e   delta / combined = %.3f" % (delta, comb, delta / comb))
    print("      |delta| / table sigma = %.3f   (|delta| %s the table's stated 4e-7)" % (abs(delta) / ts, ">" if abs(delta) > ts else "<="))
    print("      reading: %s 3 combined sigma (rule 9 '%s'); difference %s the table's stated error bar"
          % ("within" if abs(delta) <= 3 * comb else "beyond", "confirms" if abs(delta) <= 3 * comb else "discrepancy",
             "larger than" if abs(delta) > ts else "within"))

    print("\nchecks failed: %d   time %.0f s" % (len(FAILS), time.time() - t_start))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:  # any crash is a FAIL
        print("FAIL  checker stopped: %s: %s" % (type(e).__name__, e))
        rc = 1
    print("PASS" if rc == 0 else "FAIL")
    sys.exit(rc)
