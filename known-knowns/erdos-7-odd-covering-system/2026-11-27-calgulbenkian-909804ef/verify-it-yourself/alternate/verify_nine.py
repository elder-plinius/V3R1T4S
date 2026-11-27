"""Exact Python check of the basic 135-cell inequalities for the nine-prime bound."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import ceil, gcd, lcm, prod
from pathlib import Path
import json
import sys

PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29)
BOUND = 6_557_114_959_770_375
SUBSETS = tuple(tuple(s for s in range(8) if s & k == s) for k in range(8))


def positive_sum(p, e):
    return Q(1, p - 1) if e is None else (1 - Q(1, p**e)) / (p - 1)


def remaining(e, first):
    return None if e is None else e - first


@lru_cache(None)
def profile(n, u, v, threshold):
    """Hinge sums in one column of a ternary branch, with nested ternary residues."""
    den = threshold.denominator
    out = []
    for has5, pure in product(range(2), range(8)):
        by_mask = []
        for mixed in range(8):
            whole = 1 + (pure & 1) + (1 + v) * (has5 + (mixed & 1))
            band = whole + bool(pure & 2) + (1 + v) * bool(mixed & 2)
            row = band + (1 + u) * (bool(pure & 4) + (1 + v) * bool(mixed & 4))
            def hinge(value):
                return max(0, den * value - threshold.numerator)
            by_mask.append((n - 3) * hinge(whole) + 2 * hinge(band) + hinge(row))
        out.append(tuple(by_mask))
    return tuple(out)


@lru_cache(maxsize=65536)
def branch_values(n, weights, u, v, threshold):
    total, fixed, other = weights
    all_profiles = profile(n, u, v, threshold)
    branches = []
    for pure in range(8):
        ordinary = all_profiles[pure]
        selected = all_profiles[pure + 8]
        base = fixed * selected[0] + (total - fixed) * ordinary[0]
        here = tuple(fixed * (v1 - selected[0]) for v1 in selected)
        there = tuple(other * (v0 - ordinary[0]) for v0 in ordinary)
        branches.append(tuple(base + max(here[s] + there[t ^ s] for s in SUBSETS[t])
                              for t in range(8)))
    return tuple(branches)


@lru_cache(maxsize=65536)
def maximum(shape, u, v, threshold):
    n1, n2, columns = shape
    # The 5-class chooses a common column. Split the other six classes
    # between ternary branches and compare every allocation.
    best = 0
    for w1, w2 in columns:
        left = branch_values(n1, w1, u, v, threshold)
        right = branch_values(n2, w2, u, v, threshold)
        best = max(best, max(left[p][s] + right[7 ^ p][7 ^ s]
                             for p in range(8) for s in range(8)))
    return Q(best, threshold.denominator)


@lru_cache(None)
def geometry(a, b, column_weights):
    den = lcm(*(w.denominator for w in column_weights))
    integers = [int(w * den) for w in column_weights]
    divisor = gcd(*integers)
    integers = [w // divisor for w in integers]
    n = tuple(9 - 3 * (r == 1) - (b % 3 == r) for r in (1, 2))
    rows = [[0 if a == r == j else w for j, w in enumerate(integers, 1)] for r in (1, 2)]
    row_sums = list(map(sum, rows))
    fields = [tuple((row_sums[t], row[j], max(w for k, w in enumerate(row) if k != j))
                    for j in range(4)) for t, row in enumerate(rows)]
    columns = tuple(sorted(set(zip(*fields))))
    mass = sum(m * s for m, s in zip(n, row_sums))
    largest_row = max(row_sums)
    largest_weight = max(map(max, rows))
    sections = (max(m * s for m, s in zip(n, row_sums)), 3 * largest_row, largest_row,
                max(sum(m * w for m, w in zip(n, col)) for col in zip(*rows)),
                max(m * max(row) for m, row in zip(n, rows)), 3 * largest_weight, largest_weight)
    return (n[0], n[1], columns), mass, sections, Q(divisor, den)


@lru_cache(None)
def heights(p, e, cutoff, positive):
    """Mass, first moment, and retained atoms of one anchor-height region."""
    if not positive:
        return 1, 0, ((0, Q(1)),)
    if e == 0:
        return 0, 0, ()
    atoms = tuple((i, Q(1, p**i) if i == e else Q(p - 1, p**(i + 1)))
                  for i in range(1, cutoff) if e is None or i <= e)
    return Q(1, p), positive_sum(p, e), atoms


def coefficients(u, v):
    return 1, 1, 1 + u, 1 + v, 1 + v, 1 + v, (1 + u) * (1 + v)


@lru_cache(None)
def layers(geometry_data, height3, height5, tau, small, mean):
    shape, mass, sections, scale = geometry_data
    p, eu, us = height3
    q, ev, vs = height5
    pq = p * q
    if not pq:
        return Q(0)
    linear_moments = (pq, pq, (p + eu)*q, p*(q + ev), p*(q + ev), p*(q + ev),
                      (p + eu)*(q + ev))
    linear = pq * mass + sum(x * y for x, y in zip(linear_moments, sections))
    total = mean * linear - (1 - sum(prob for m, prob in small)) * tau * pq * mass
    for m, prob in small:
        correction = Q(0)
        for (u, pu), (v, pv) in product(us, vs):
            full = mass + sum(x * y for x, y in zip(coefficients(u, v), sections))
            correction += pu * pv * (maximum(shape, u, v, tau/m) - full)
        total += prob * m * correction
    return scale * total


def small_products(primes, exps, scales, threshold):
    limit = ceil(threshold)
    law = {1: Q(1)}
    for p, e, c in zip(primes, exps, scales):
        atoms = {1: 1 - c / p}
        for j in range(1, limit):
            if e is not None and j > e:
                break
            atoms[j+1] = c * (Q(1,p**j) if j == e else Q(p-1,p**(j+1)))
        nxt = {}
        for m, pm in law.items():
            for k, pk in atoms.items():
                if m*k < threshold:
                    nxt[m*k] = nxt.get(m*k, 0) + pm * pk
        law = nxt
    return tuple(sorted(law.items()))


def check_model(exps, rows, taus, cuts):
    if len(exps) != 9 or any(e is not None and (type(e) is not int or e < 1) for e in exps):
        raise ValueError("invalid nine-prime caps")
    if (exps[0] is not None and exps[0] < 3) or (exps[1] is not None and exps[1] < 2):
        raise ValueError("missing anchor depths")
    e3, e5 = exps[:2]
    tails = PRIMES[2:]
    n = tuple(1 / positive_sum(p, e) for p, e in zip(tails, exps[2:]))
    ts = (n[0]/3,) + taus
    cap = tuple(x/(x-t) for x,t in zip(n,ts))
    if not all(0<t<x and 1<c<=p for p,x,t,c in zip(tails,n,ts,cap)):
        raise ValueError("invalid stage parameters")
    stages = []
    for i,t in enumerate(ts):
        small = small_products(tails[:i], exps[2:2+i], cap[:i], t)
        mean = prod(1 + c / x for c,x in zip(cap[:i], n[:i]))
        stages.append((t, small, mean, n[i]-t))
    T = positive_sum(5, remaining(e5, 2))/5
    seen = {}
    for phase,key,expected_R,expected_S in rows:
        a,b,c,r,j,d,k,h,z = key
        if phase != "basic" or (r,d,k,h,z) != (-1,0,0,0,-1) or (a,b,c,j) in seen:
            raise ValueError("invalid basic row")
        loss_columns = tuple(Q(y == c,5) + T*(y == j) for y in range(1,5))
        lost_rows = 3*(a == 1) + (b % 3 == a)
        R = 135*(1-positive_sum(3,e3)-positive_sum(5,e5)) + lost_rows + (9-lost_rows)*loss_columns[a-1]
        S = Q(0)
        for up,vp in product(range(2),repeat=2):
            row_scale = Q(2,3) if not up and e3 != 3 else Q(1)
            w = tuple(Q(1) if vp else Q(4,5)-loss for loss in loss_columns)
            g = geometry(a,b,w)
            hu = heights(3,remaining(e3,3),cuts[0],up)
            hv = heights(5,remaining(e5,1),cuts[1],vp)
            S += row_scale * sum(layers(g,hu,hv,t,small,mean)/beta for t,small,mean,beta in stages)
        if R != Q(expected_R) or S != Q(expected_S) or R <= S:
            raise ValueError(f"wrong basic inequality at {exps}, {key}: {R}, {S}")
        seen[a,b,c,j] = R-S
    if set(seen) != set(product((1,2),(2,4),(1,2),range(1,5))):
        raise ValueError("incomplete basic hierarchy")
    return min(seen.values())


def model_inputs(path):
    if path.suffix == ".json":
        data = json.loads(path.read_text())
        if data["bound"] != BOUND or tuple(data["primes"]) != PRIMES or Q(data["C7"]) != Q(3,2):
            raise ValueError("wrong theorem or first stage")
        for model in data["certificates"]:
            yield tuple(model["exps"]), model["rows"], tuple(map(Q,data["taus_later"])), (data["U"],data["V"])
        return

    def decode(header, rows):
        if header.get("format") != "anchored_cert_v1" or header.get("part", "1/1") != "1/1":
            raise ValueError("invalid basic model format")
        primes = tuple(map(int,header["primes"].split(",")))
        if primes != PRIMES or Q(header["C7"]) != Q(3,2):
            raise ValueError("wrong prime support or first stage")
        exps = tuple(None if e=="inf" else int(e) for e in header["exps"].split(","))
        thresholds = tuple(map(Q,header["taus_later"].split(",")))
        cuts = int(header["U_cut"]), int(header["V_cut"])
        if min(cuts) < 1:
            raise ValueError("invalid height cutoff")
        # The TSV format requires all finite heights to be explicit.
        if any(e is not None and cut <= e-base for cut,e,base in zip(cuts,exps[:2],(3,1))):
            raise ValueError("a finite terminal height exceeds the declared rectangle")
        if not thresholds or min(thresholds) < 1:
            raise ValueError("invalid later thresholds")
        return exps, rows, thresholds, cuts

    header, rows = {}, []
    for line in path.read_text().splitlines():
        if not line:
            continue
        if line == "# --- model ---":
            if header or rows:
                yield decode(header, rows)
            header, rows = {}, []
        elif line.startswith("# "):
            k, _, v = line[2:].partition(":")
            if rows or k in header:
                raise ValueError("misplaced or duplicated model header")
            header[k] = v.strip()
        else:
            phase, key, R, S = line.split("\t")
            rows.append((phase,tuple(map(int,key.split(","))),R,S))
    if header or rows:
        yield decode(header, rows)


def main(path):
    models = {}
    for exps,rows,taus,cuts in model_inputs(path):
        if len(taus) != 6 or min(cuts) < 1 or any(type(v) is not int for v in cuts):
            raise ValueError("invalid thresholds or cutoffs")
        if exps in models:
            raise ValueError("duplicate model")
        models[exps] = check_model(exps,rows,taus,cuts)
    # Generate exactly the products below BOUND, by nondecreasing extra primes.
    def visit(exps, value, first):
        if not any(all(y is None or x<=y for x,y in zip(exps,cap)) for cap in models):
            raise ValueError(f"uncovered exponent vector {exps}")
        count = 1
        for i in range(first,len(PRIMES)):
            new_value = value*PRIMES[i]
            if new_value >= BOUND:
                break
            new = list(exps)
            new[i] += 1
            count += visit(tuple(new),new_value,i)
        return count
    vectors = visit((1,)*9,prod(PRIMES),0)
    print(f"Nine-prime branch: {len(models)} basic models, {32*len(models)} rows, {vectors} vectors")
    print(f"Least surplus in 135-cells: {min(models.values())}")

if __name__ == "__main__":
    try:
        default = Path(__file__).with_name("certs") / "nine_finite.tsv"
        if not default.exists():
            default = Path(__file__).with_name("nine-finite.json")
        main(Path(sys.argv[1]) if len(sys.argv)>1 else default)
    except Exception as exc:
        print(exc)
        print("FAIL")
        sys.exit(1)
    print("PASS")
