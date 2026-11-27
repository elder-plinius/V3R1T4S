"""Second exact verifier for the odd-covering certificate tables.

Compile the accompanying finite_geometry.cpp as described in ALTERNATE.md.
"""
import ctypes as ct
import math
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

import verify_scalar


G = (3, 9, 27, 5, 15, 45, 135)
KAPPA = (11, 11, 9, 6, 3)
PINS = (0, 3, 1, 4)  # order in a physical tuple: 3q, 5q, 9q, 15q
ZERO = (0,) * 135
ONE = (1,) * 135
lib = None
CArray = ct.c_int64 * 135
geom_cache = {}


def load_geometry(path):
    global lib
    lib = ct.CDLL(str(path.resolve()))
    ptr = ct.POINTER(ct.c_int64)
    lib.hinge_register.argtypes = [ptr, ptr]
    lib.hinge_register.restype = ct.c_int
    lib.hinge_batch.argtypes = [ct.c_int, ct.c_int, ptr, ptr]
    lib.hinge_batch.restype = ct.c_int


def series(p, e):
    """Sum p^-j over the allowed positive depths."""
    return Q(1, p - 1) if e is None else (1 - Q(1, p**e)) / (p - 1)


def lowered(e, d):
    return None if e is None else e - d


@lru_cache(None)
def core(a, b, r):
    return tuple(x for x in range(135)
                 if x % 3 and x % 5 and x % 9 != 1 and x % 27 != b
                 and x % 15 != a and x % 45 != r)


@lru_cache(None)
def indicator(g, r):
    return tuple(int(x % g == r) for x in range(135))


@lru_cache(None)
def counts(indices, residues):
    projections = [indicator(G[i], r) for i, r in zip(indices, residues)]
    return tuple(map(sum, zip(*projections)))


@lru_cache(None)
def register(a, s):
    if len(a) != 135 or len(s) != 135 or min(a) < 0 or sum(a) > 10**6 or min(s) < 0 or max(s) > 4:
        raise ValueError("geometric layout exceeds the integer bounds")
    index = lib.hinge_register(CArray(*a), CArray(*s))
    if index < 0:
        raise ValueError("invalid within-column offset or heaviest-child invariant")
    return index


@lru_cache(None)
def lin(a):
    """Total weight and largest residue-section weight for each category."""
    best = []
    for g in G:
        sections = [0] * g
        for x, weight in enumerate(a):
            sections[x % g] += weight
        best.append(max(sections))
    return sum(a), tuple(best)


def query(layout, jobs):
    cache = geom_cache.setdefault(layout, {})
    missing = list(dict.fromkeys(job for job in jobs if job not in cache))
    if missing:
        if any(any(abs(x) > 10**8 for x in job) or min(job[1:]) < 0 for job in missing):
            raise ValueError("geometric query exceeds the integer bounds")
        packed = (ct.c_int64 * (len(missing) * 9))(*(i for job in missing for i in job))
        results = (ct.c_int64 * len(missing))()
        if lib.hinge_batch(layout, len(missing), packed, results):
            raise OverflowError("geometric numerator exceeds the exact kernel bound")
        cache.update(zip(missing, results))
    return [cache[job] for job in jobs]


@lru_cache(None)
def depth(p, cap, cut, positive):
    """Return explicit atoms and full mass and first moment on this depth region."""
    if not positive:
        return ((0, Q(1)),), Q(1), Q(0)
    if cap == 0:
        return (), Q(0), Q(0)
    points = []
    for j in range(1, cut):
        if cap is None or j <= cap:
            atom = Q(1, p**j) if cap == j else Q(p - 1, p**(j + 1))
            points.append((j, atom))
    return tuple(points), Q(1, p), series(p, cap)


def category(u, v):
    return (1, 1, 1 + u, 1 + v, 1 + v, 1 + v, (1 + u) * (1 + v))


@lru_cache(None)
def region_heights(caps, cuts, pos3, pos5):
    us, pu, mu = depth(3, caps[0], cuts[0], pos3)
    vs, pv, mv = depth(5, caps[1], cuts[1], pos5)
    mass = pu * pv
    vweight = pu * (pv + mv)
    coefficients = (mass, mass, (pu + mu) * pv, vweight, vweight, vweight,
                    (pu + mu) * (pv + mv))
    cells = [(u, v, wu * wv, category(u, v)) for u, wu in us for v, wv in vs]
    return mass, coefficients, cells


@lru_cache(None)
def anchor(e3, e5, state):
    """Reserve, four integer comparison fields, and the full per-cell masses."""
    a, b, c, r, j, d, k, hit, z = state
    three = series(3, lowered(e3, 3)) if z >= 0 else Q(0)
    five = series(5, lowered(e5, 2)) / 5
    active = core(a, b, r)
    column_loss = [Q(h == c, 5) + five * (h == j) for h in range(5)]
    reserve = 135 * (1 - series(3, e3) - series(5, e5))
    lost15 = 3 * (a == 1) + (b % 3 == a % 3) + three * (z % 3 == a % 3)
    reserve += lost15 + (9 - lost15) * column_loss[a]
    if r >= 0:
        lost45 = (b % 9 == r % 9) + three * (z % 9 == r % 9)
        reserve += lost45 + (3 - lost45) * column_loss[r % 5]
    child75 = Q(1, 5) - five * hit
    if d:
        retained = sum(1 - three * (x % 27 == z) for x in active
                       if x % 3 == d and x % 5 == k)
        reserve += Q(9, 5) - retained * child75

    col0 = [Q(4, 5) - column_loss[x % 5] - child75 * (x % 3 == d and x % 5 == k)
            for x in active]
    first3 = Q(0) if e3 == 3 else Q(1, 3)
    row0 = [1 - first3 - three * (x % 27 == z) for x in active]
    regions = []
    for pos3, pos5 in product(range(2), repeat=2):
        weights = [(1 if pos3 else r0) * (1 if pos5 else c0)
                   for r0, c0 in zip(row0, col0)]
        den = math.lcm(*(Q(w).denominator for w in weights))
        raw = [0] * 135
        for x, weight in zip(active, weights):
            raw[x] = int(weight * den)
        regions.append((tuple(raw), den, pos3, pos5))
    actual = [Q(0)] * 135
    for x, r0, c0 in zip(active, row0, col0):
        actual[x] = (r0 + first3) * (c0 + Q(1, 5))
    return reserve, tuple(regions), tuple(actual)


@lru_cache(None)
def geometry_region(a, s):
    mass, sections = lin(a)
    fixed = sum(weight * n for weight, n in zip(a, s))
    return register(a, s), mass, sections, fixed


def layer_jobs(cells, t, alpha, indices):
    """Encode the normalized hinge (1-t + free load + alpha*s)_+ as integers."""
    den = math.lcm(t.denominator, alpha.denominator)
    take = int(alpha * den)
    base = den - int(t * den)
    jobs = []
    for _, _, _, coefficients in cells:
        free = [w * den for w in coefficients]
        for k in indices:
            free[k] -= take
        if min(free) < 0:
            raise ValueError("fixed class exceeds its available coefficient")
        jobs.append((base, *free, take))
    return den, jobs


@lru_cache(None)
def integral(layout, A, h, fixed, caps, cuts, pos3, pos5, t, alpha, indices):
    """Use the full linear load outside the evaluated rectangle of heights."""
    mass, moments, cells = region_heights(caps, cuts, pos3, pos5)
    correction = alpha * (fixed - sum(h[k] for k in indices))
    total = mass * (A + correction) + sum(w * b for w, b in zip(moments, h))
    den, jobs = layer_jobs(cells, t, alpha, indices)
    for best, (_, _, prob, coefficients) in zip(query(layout, jobs), cells):
        full = A + sum(w * b for w, b in zip(coefficients, h)) + correction
        total += prob * (Q(best, den) - full)
    return total


@lru_cache(None)
def law(qs, exps, cs, mode, limit):
    """Small atoms of M=product(1+J_p), plus its unrestricted mass and first moment."""
    small = {1: Q(1)}
    mass = mean = Q(1)
    for p, e, c in zip(qs, exps, cs):
        zero = 1 - c / p
        atoms = {1: zero}
        for j in range(1, limit):
            if e is not None and j > e:
                break
            atoms[j + 1] = c * (Q(1, p**j) if e == j else Q(p - 1, p**(j + 1)))
        prime_mass = Q(1)
        prime_mean = 1 + c * series(p, e)
        if p == 7 and mode == "zero":
            # The J_7=0 mass is already included in the spatial cell field.
            atoms = {1: Q(1)}
            prime_mass = prime_mean = Q(1)
        if p == 7 and mode == "positive":
            atoms.pop(1)
            prime_mass -= zero
            prime_mean -= zero
        combined = {}
        for m, weight in small.items():
            for n, atom in atoms.items():
                if m * n < limit:
                    combined[m * n] = combined.get(m * n, Q(0)) + weight * atom
        small = combined
        mass *= prime_mass
        mean *= prime_mean
    return small, mass, mean


@lru_cache(None)
def field(raw, den, scale):
    if scale is not None:
        raw = tuple(w * s for w, s in zip(raw, scale))
        den *= 14
    gcd = math.gcd(*raw)
    return tuple(x // gcd for x in raw), Q(gcd, den)


@lru_cache(None)
def region_stage(layout, A, h, fixed, caps, cuts, pos3, pos5, t, alpha, indices, law_key):
    small, mass, mean = law(*law_key)
    prob_height, moments, _ = region_heights(caps, cuts, pos3, pos5)
    full = prob_height * A + sum(w * x for w, x in zip(moments, h))
    correction = prob_height * alpha * (fixed - sum(h[k] for k in indices))
    small_mass = small_mean = total = Q(0)
    for m, prob in small.items():
        if m < t:
            small_mass += prob
            small_mean += m * prob
            value = integral(layout, A, h, fixed, caps, cuts, pos3, pos5,
                             t / m, alpha / m, indices)
            total += prob * m * value
    # For m >= t, the hinge is affine everywhere, even at unbounded heights.
    total += (mean - small_mean) * full + (mass - small_mass) * (correction - t * prob_height * A)
    return total


class Engine:
    def __init__(self, primes, exponents, thresholds, cuts):
        self.q, self.exps, self.cuts = primes[2:], exponents, cuts
        ts = thresholds
        self.axcaps = tuple(lowered(e, i) for e, i in zip(self.exps, (3, 1)))
        self.n = tuple(1 / series(p, e) for p, e in zip(self.q, self.exps[2:]))
        self.t = (self.n[0] / 3,) + tuple(map(Q, ts))
        self.beta = tuple(n - t for n, t in zip(self.n, self.t))
        self.c = tuple(n / b for n, b in zip(self.n, self.beta))
        self.w = tuple(n / p for n, p in zip(self.n, self.q))
        if not all(0 < t < n and 1 < c <= p and w <= 1
                   for p,n,t,c,w in zip(self.q,self.n,self.t,self.c,self.w)):
            raise ValueError("invalid anchored stage thresholds")
        if self.t[0] < 1 + self.w[0]:
            raise ValueError("insufficient stage-seven threshold")

    def measure(self, state):
        return anchor(*self.exps[:2], state)

    @lru_cache(None)
    def stage(self, state, i, mode7, xi):
        _, regions, _ = self.measure(state)
        s = counts(PINS, xi) if xi else ZERO
        scale = tuple(KAPPA[n] for n in s) if xi and i else None
        indices = PINS if i == 0 and mode7 != "ordinary" else ()
        offset = ZERO
        if indices:
            offset = ONE if mode7 == "coarse" else s
        alpha = self.w[0] if indices else Q(0)
        t = self.t[i]
        modes = ("zero", "positive") if scale else ("ordinary",)
        total = Q(0)
        for mode in modes:
            law_key = (self.q[:i], self.exps[2:2+i], self.c[:i], mode, math.ceil(t))
            for raw, den, pos3, pos5 in regions:
                a, factor = field(raw, den, scale if mode == "zero" else None)
                metrics = geometry_region(a, offset)
                part = region_stage(*metrics, self.axcaps, self.cuts, pos3, pos5,
                                    t, alpha, indices, law_key)
                if indices:
                    # On omitted heights the coarse hinge is bounded by the residual
                    # load, and the spatial hinge by that load plus alpha*s.
                    prob_height, _, cells = region_heights(self.axcaps, self.cuts, pos3, pos5)
                    outside = prob_height - sum(term[2] for term in cells)
                    baseline = 1 + (alpha if mode7 == "coarse" else 0)
                    part -= outside * metrics[1] * baseline
                total += factor * part
        return total / self.beta[i]

    @lru_cache(None)
    def ordinary(self, state):
        return tuple(self.stage(state, i, "ordinary", ()) for i in range(len(self.q)))

    def eval(self, phase, key):
        state, xi = tuple(key[:9]), tuple(key[9:])
        reserve, _, actual = self.measure(state)
        if phase in ("basic", "mixed", "basic75"):
            return reserve + Q(phase == "basic75", 5), self.ordinary(state)
        if phase == "coarse":
            s = counts(PINS, xi)
            extra = self.c[0] / 7 * sum(a * (n - 1) for a, n in zip(actual, s) if n > 1)
            current = self.stage(state, 0, "coarse", ()) + extra
            return reserve, (current,) + self.ordinary(state)[1:]
        if phase in ("spatial", "pure3"):
            return reserve, tuple(self.stage(state, i, "spatial", xi) for i in range(len(self.q)))
        raise KeyError(phase)


@lru_cache(None)
def selected_difference(ordinary, pinned, caps, pos3, pos5, tau, w, indices, law_key, bounds):
    """Exact difference of two maxima on the same retained finite layers."""
    mmax, umax, vmax = bounds
    _, _, cells = region_heights(caps, (umax + 1, vmax + 1), pos3, pos5)
    if not cells:
        return Q(0)
    weights = [term[2] for term in cells]
    distribution, _, _ = law(*law_key)
    saving = Q(0)
    for m, prob in distribution.items():
        if m >= tau or m > mmax:
            continue
        den0, jobs0 = layer_jobs(cells, tau / m, Q(0), ())
        den1, jobs1 = layer_jobs(cells, tau / m, w / m, indices)
        free_values = query(ordinary, jobs0)
        fixed_values = query(pinned, jobs1)
        difference = sum(weight * (Q(x, den0) - Q(y, den1))
                         for weight, x, y in zip(weights, free_values, fixed_values))
        if difference < 0:
            raise ValueError("a fixed projection increases the free maximum")
        saving += m * prob * difference
    return saving


def mixed(a, b, c):
    representatives = {}
    for r in range(45):
        if r % 3 and r % 5 and r % 9 != 1 and r % 15 != a:
            signature = (r % 3, r % 9 == b % 9, r % 5 == a, r % 5 == c)
            representatives.setdefault(signature, r)
    for r, d, k in product(representatives.values(), (1, 2), range(1, 5)):
        if (d, k) != (a, a):
            for j, hit in ((1, 0), (2, 0), (3, 0), (4, 0), (k, 1)):
                yield (a, b, c, r, j, d, k, hit, -1)


def legal15(a):
    return tuple(y for y in range(15) if y % 3 and y % 5 and y != a)


def four_projections(a):
    return product((1, 2), range(1, 5), (2, 4, 5, 7, 8), legal15(a))


def check_tree(rows):
    used = set()
    def find(phase,keys):
        keys = list(keys)
        wanted = {(phase,k) for k in keys}
        if wanted <= rows.keys():
            used.update(wanted)
            return True
        return False
    for a,b,c in product((1,2),(2,4),(1,2)):
        roots=[(a,b,c,-1,j,0,0,0,-1) for j in range(1,5)]
        if find("basic",roots) or b==2 and find("basic75",roots): continue
        for st in mixed(a,b,c):
            if find("mixed",[st]): continue
            for xi in four_projections(a):
                if find("coarse",[st+xi]) or find("spatial",[st+xi]): continue
                for z in range(27):
                    if z%3 == 0 or z%9 == 1 or z==b: continue
                    key=st[:-1]+(z,)+xi
                    if find("pure3",[key]): continue
                    if not find("fixed165",[key+eta for eta in ((y,) for y in legal15(a))]):
                        raise ValueError(f"open leaf {key}")
    if used != rows.keys():
        raise ValueError("unused rows")


def fixed165(eng,key):
    st,xi,eta=key[:9],key[9:13],key[13:]
    R,base=eng.eval("pure3",key[:13])
    _,regions,_=eng.measure(st)
    kappa=tuple(KAPPA[n] for n in counts(PINS,xi))
    offset=counts((4,),eta)
    t,w=eng.t[1], eng.w[1]
    bounds=math.ceil(t)-1,eng.cuts[0]-1,eng.cuts[1]-1
    saving=Q(0)
    for mode in ("zero","positive"):
        law_key=(eng.q[:1],eng.exps[2:3],eng.c[:1],mode,math.ceil(t))
        for raw,den,pos3,pos5 in regions:
            a,scale=field(raw,den,kappa if mode=="zero" else None)
            saving += scale * selected_difference(register(a,ZERO),register(a,offset),eng.axcaps,
                        pos3,pos5,t,w,(4,),law_key,bounds)
    return R,sum(base) - saving / eng.beta[1]



MODEL_COLUMNS = "phase\tkey\tR_exact\tS_exact"
HEADER_KEYS = {"format", "id", "primes", "exps", "C7", "taus_later", "U_cut", "V_cut", "part", "columns"}


def manifest(package):
    index = json.loads((package / "MANIFEST.json").read_text())
    names = [f"thmA_8p.part{i:02}.tsv" for i in range(1, 7)]
    names.extend(("nine_finite.tsv", "global_anchored.tsv", "scalar_lemma_u.tsv"))
    expected = {"certs/" + name for name in names}
    if index["L_target"] != verify_scalar.BOUND or index["format"] != "erdos7_package_manifest_v1":
        raise ValueError("wrong target or manifest format")
    declared = index["files"]
    if len(declared) != len(expected) or {item["path"] for item in declared} != expected:
        raise ValueError("unexpected or missing certificate file")
    total_bytes = 0
    for item in declared:
        raw = (package / item["path"]).read_bytes()
        if len(raw) > 1_000_000 or len(raw) != item["bytes"] or hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("byte count or digest differs for " + item["path"])
        total_bytes += len(raw)
    if index["total_files"] != len(expected) or index["total_bytes"] != total_bytes or total_bytes > 50_000_000:
        raise ValueError("incorrect certificate inventory")
    return package / "certs"


def read_model_blocks(path):
    header, rows = {}, {}
    for line in path.read_text().splitlines():
        if not line:
            continue
        if line == "# --- model ---":
            if header or rows:
                yield header, rows
            header, rows = {}, {}
        elif line.startswith("# "):
            key, sep, value = line[2:].partition(":")
            if not sep or rows or key in header:
                raise ValueError("invalid header in " + path.name)
            header[key] = value.strip()
        else:
            phase, key, reserve, loss = line.split("\t")
            ident = phase, tuple(map(int, key.split(",")))
            if ident in rows:
                raise ValueError("duplicate geometric row in " + path.name)
            rows[ident] = Q(reserve), Q(loss)
    if header or rows:
        yield header, rows


def parse_models(paths, role):
    allowed_ids = {"A8"} if role == "A8" else {
        (f"F9_{i:02}" if role == "F9" else f"G{i:02}") for i in range(1, 24 if role == "F9" else 14)
    }
    cases = {}
    for i, path in enumerate(paths, 1):
        blocks = list(read_model_blocks(path))
        if role == "A8" and len(blocks) != 1:
            raise ValueError("each A8 part must contain one block")
        for header, rows in blocks:
            if set(header) != HEADER_KEYS or header["columns"] != MODEL_COLUMNS or header["format"] != "anchored_cert_v1":
                raise ValueError("invalid anchored header in " + path.name)
            name = header["id"]
            if name not in allowed_ids or header["part"] != f"{i}/{len(paths)}":
                raise ValueError("incorrect model or part identifier")
            primes = tuple(map(int, header["primes"].split(",")))
            exps = tuple(None if x == "inf" else int(x) for x in header["exps"].split(","))
            thresholds = tuple(map(Q, header["taus_later"].split(",")))
            cuts = int(header["U_cut"]), int(header["V_cut"])
            rank = len(primes)
            if len(exps) != rank or len(thresholds) != rank-3 or min(cuts) < 1:
                raise ValueError("inconsistent model dimensions")
            if primes != tuple(p for _,p in zip(range(rank), verify_scalar.odd_primes())):
                raise ValueError("incorrect sequence of odd primes")
            if any(e is not None and e < 1 for e in exps) or Q(header["C7"]) != Q(3, 2):
                raise ValueError("invalid cap or unsupported first-stage density")
            if (exps[0] is not None and exps[0] < 3) or (exps[1] is not None and exps[1] < 2):
                raise ValueError("missing anchor depths")
            if role == "A8" and (rank != 8 or any(e is not None for e in exps)):
                raise ValueError("Theorem A needs eight unrestricted coordinates")
            if role == "F9" and (rank != 9 or any(phase != "basic" for phase, _ in rows)):
                raise ValueError("nine-prime certificate has the wrong form")
            if role == "G" and (rank not in (10, 11) or any(e is None for e in exps)):
                raise ValueError("invalid residual model")
            # The TSV format requires each finite terminal height inside its rectangle.
            if any(e is not None and cut <= e-base for cut,e,base in zip(cuts,exps[:2],(3,1))):
                raise ValueError("a finite terminal height exceeds the declared rectangle")
            if min(thresholds) < 1:
                raise ValueError("later thresholds must be at least one")
            params = primes, exps, thresholds, cuts
            if name in cases:
                previous, existing = cases[name]
                if role != "A8" or previous != params or rows.keys() & existing.keys():
                    raise ValueError("contradictory model blocks")
                existing.update(rows)
            else:
                cases[name] = params, rows
    if cases.keys() != allowed_ids:
        raise ValueError("incomplete set of " + role + " model identifiers")
    return cases


def verify_anchored(cases, role):
    least = None
    total_rows = 0
    caps = set()
    for name, (params, rows) in cases.items():
        primes, exps, thresholds, cuts = params
        if (primes, exps) in caps:
            raise ValueError("duplicated exponent model")
        caps.add((primes, exps))
        check_tree(rows)
        engine = Engine(primes, exps, thresholds, cuts)
        for (phase, key), declared in rows.items():
            if phase == "fixed165":
                actual = fixed165(engine, key)
            else:
                reserve, stages = engine.eval(phase, key)
                actual = reserve, sum(stages)
            margin = actual[0] - actual[1]
            if actual != declared or margin <= 0:
                raise ValueError(f"invalid inequality in {name}: {phase} {key}")
            least = margin if least is None else min(margin, least)
        total_rows += len(rows)
    if total_rows != {"A8": 28057, "F9": 736, "G": 692}[role]:
        raise ValueError("unexpected number of anchored rows in " + role)
    print(f"{role}: {len(cases)} models, {total_rows} exact rows, least surplus {least}", flush=True)
    return caps


def check_completion():
    mixed = (15, 45, 75, 21, 35, 63, 105, 165)
    totals = []
    for m in mixed:
        divisors = {d for d in mixed if d < m and m % d == 0}
        for p in (3, 5, 7, 11):
            d = p
            while m % d == 0:
                divisors.add(d)
                d *= p
        totals.append(sum(Q(1,d) for d in divisors))
    if max(totals) != Q(86,105):
        raise ValueError("incorrect mixed completion divisor sum")
    # For a pure power the proper-divisor sum is bounded by 1/(p-1).
    first14 = tuple(p for _,p in zip(range(14), verify_scalar.odd_primes()))
    if math.prod(first14) != 307_444_891_294_245_705 or math.prod(first14) <= verify_scalar.BOUND:
        raise ValueError("failed the first-fourteen-primes bound")


def verify_all(package, library):
    check_completion()
    load_geometry(library)
    certs = manifest(package)
    three_groups = (
        ("A8", sorted(certs.glob("thmA_8p.part*.tsv"))),
        ("F9", (certs / "nine_finite.tsv",)),
        ("G", (certs / "global_anchored.tsv",)),
    )
    closed = {}
    for role, paths in three_groups:
        closed[role] = verify_anchored(parse_models(paths, role), role)
    nine = tuple(p for _,p in zip(range(9), verify_scalar.odd_primes()))
    count = 0
    for vector in verify_scalar.exponent_vectors(nine, verify_scalar.BOUND):
        if not any(pp == nine and len(cap) == 9 and all(h is None or x <= h for x,h in zip(vector,cap))
                   for pp,cap in closed["F9"]):
            raise ValueError(f"undominated nine-prime vector {vector}")
        count += 1
    if count != 5028 or closed["G"] != verify_scalar.anchored_caps(certs / "global_anchored.tsv"):
        raise ValueError("incorrect finite coverage")
    print(f"{count} nine-prime vectors dominated", flush=True)
    verify_scalar.main(certs)


if __name__ == "__main__":
    try:
        if len(sys.argv) > 3:
            raise ValueError("usage: python3 check_alternate.py [package-directory [shared-library]]")
        here = Path(__file__).resolve().parent
        package = Path(sys.argv[1]) if len(sys.argv) > 1 else here
        library = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "finite_geometry.so"
        verify_all(package, library)
    except Exception as exc:
        print(exc)
        print("FAIL")
        sys.exit(1)
    print("PASS")
