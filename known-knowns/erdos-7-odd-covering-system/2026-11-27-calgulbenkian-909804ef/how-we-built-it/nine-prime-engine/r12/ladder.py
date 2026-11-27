"""Independent nine-prime certificate engine, using only the stated caps and cutoffs."""
import ctypes as ct
import math
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
G = (3, 9, 27, 5, 15, 45, 135)
KAPPA = (11, 11, 9, 6, 3)
PINS = (0, 3, 1, 4)  # order in a physical tuple: 3q, 5q, 9q, 15q
ZERO = (0,) * 135
ONE = (1,) * 135
FULL = (None,) * 9
NORMAL = (7, 11, 13, 17, 19, 23, 29)
CAPS = (4, 4, 6, 8, 12, 16)
# support, maximum exponents, tau after 7, height cutoff, pin cutoff, stopping margin
SPECS = {
    "4_4_2": (NORMAL, (4, 4, 2) + FULL[3:], CAPS, (8, 6), (6, 2, 3), Q(1, 100)),
    "no17": ((7, 11, 13, 19, 23, 29, 31), FULL, (4, 4, 8, 10, 14, 18),
             (8, 6), (4, 2, 2), Q(1, 20)),
    "no19": ((7, 11, 13, 17, 23, 29, 31), FULL, (4, 4, 6, 10, 14, 18),
             (8, 6), (4, 2, 2), Q(1, 40)),
    "v11_1_v13_1": (NORMAL, (None, None, None, 1, 1, None, None, None, None), CAPS,
                      (8, 6), (4, 2, 2), Q(1, 40)),
    "v11_1_v17_1": (NORMAL, (None, None, None, 1, None, 1, None, None, None), CAPS,
                      (8, 6), (4, 2, 2), Q(1, 40)),
    "v13_17_19": (NORMAL, (None, None, None, None, 1, 1, 1, None, None),
                   (4, Q(9, 2), 8, 8, 12, 16), (11, 8), (6, 2, 3), Q(1, 100)),
}
lib = ct.CDLL(str(HERE / "geometry.dylib"))
ptr = ct.POINTER(ct.c_int32)
lib.geom_register.argtypes = [ptr, ptr]
lib.geom_batch.argtypes = [ct.c_int, ct.c_int, ptr, ptr]
CArray = ct.c_int32 * 135
geom_cache = {}


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
    return lib.geom_register(CArray(*a), CArray(*s))


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
        packed = (ct.c_int32 * (len(missing) * 9))(*(i for job in missing for i in job))
        results = (ct.c_int32 * len(missing))()
        if lib.geom_batch(layout, len(missing), packed, results):
            raise OverflowError("geometric numerator exceeds signed 32-bit bound")
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
        assert min(free) >= 0
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
    def __init__(self, name):
        self.q, self.exps, ts, self.cuts, self.pin, self.threshold = SPECS[name]
        self.axcaps = tuple(lowered(e, i) for e, i in zip(self.exps, (3, 1)))
        self.n = tuple(1 / series(p, e) for p, e in zip(self.q, self.exps[2:]))
        self.t = (self.n[0] / 3,) + tuple(map(Q, ts))
        self.beta = tuple(n - t for n, t in zip(self.n, self.t))
        self.c = tuple(n / b for n, b in zip(self.n, self.beta))
        self.w = tuple(n / p for n, p in zip(self.n, self.q))

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
        return tuple(self.stage(state, i, "ordinary", ()) for i in range(7))

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
            return reserve, tuple(self.stage(state, i, "spatial", xi) for i in range(7))
        raise KeyError(phase)
