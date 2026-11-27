"""Recompute the finite scalar part of the lower bound on an odd covering's period."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import count
from math import isqrt, prod
from pathlib import Path
import sys

BOUND = 6_557_114_959_770_375


def odd_primes():
    for n in count(3, 2):
        if all(n % d for d in range(3, isqrt(n) + 1, 2)):
            yield n


def exponent_vectors(primes, bound):
    """Factor the possible multipliers of the squarefree kernel by trial division."""
    kernel = prod(primes)
    for multiplier in range(1, (bound - 1) // kernel + 1):
        rest = multiplier
        exponents = []
        for p in primes:
            exponent = 1
            while rest % p == 0:
                exponent += 1
                rest //= p
            exponents.append(exponent)
        if rest == 1:
            yield tuple(exponents)


def prime_supports(bound):
    primes = []
    for prime in odd_primes():
        primes.append(prime)
        if prod(primes) >= bound:
            break
        if len(primes) >= 10:
            yield tuple(primes)


def scalar_rows(path):
    """Read the tab-separated scalar witnesses and require canonical prime supports."""
    groups = {}
    ids = set()
    header = {}
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        if line.startswith("# "):
            field, _, value = line[2:].partition(":")
            if field in header:
                raise ValueError(f"repeated scalar header on line {number}")
            header[field] = value.strip()
            continue
        key, rank, primes, heights, prefix, caps, stored = line.split("\t")
        primes = tuple(map(int, primes.split(",")))
        heights = tuple(map(int, heights.split(",")))
        caps = tuple(map(Q, caps.split(",")))
        rank, prefix = int(rank), int(prefix)
        if primes not in groups:
            if primes not in tuple(prime_supports(BOUND)):
                raise ValueError(f"unexpected prime list on line {number}")
            groups[primes] = {}
        if rank != len(primes) or len(heights) != rank or min(heights) < 1:
            raise ValueError(f"invalid exponent vector on line {number}")
        if not 1 <= prefix < rank or len(caps) != rank - prefix:
            raise ValueError(f"invalid scalar prefix on line {number}")
        if key in ids or heights in groups[primes]:
            raise ValueError(f"duplicated scalar certificate on line {number}")
        ids.add(key)
        groups[primes][heights] = (prefix, caps, Q(stored))
    if header.get("format") != "lemma_u_v1" or header.get("L_target") != str(BOUND):
        raise ValueError("wrong scalar format or target")
    if len(ids) != 738:
        raise ValueError(f"expected 738 scalar certificates, received {len(ids)}")
    return groups


def evaluate(primes, heights, prefix, caps):
    """Apply Proposition 4.1 by summing the positive hinge over the entire product law."""
    rho = tuple(Q(p**e - 1, (p - 1) * p**e) for p, e in zip(primes, heights))
    theta = tuple(x / (1 - x) for x in rho[:prefix])
    result = prod(1 + x for x in theta) - 1 - sum(theta)
    if not all(1 < c <= p for c, p in zip(caps, primes[prefix:])):
        raise ValueError("distortion cap outside the range of Proposition 4.1")

    # 'counts' gives an integer numerator for every atom of M, with one denominator.
    counts = {1: 1}
    denominator = 1
    for i, (p, e) in enumerate(zip(primes, heights)):
        if i < prefix:
            scale = 1 / (1 - rho[i])
        else:
            scale = caps[i - prefix]
            delta = 1 - 1 / scale
            a = rho[i].numerator * delta.denominator
            b = delta.numerator * rho[i].denominator
            positive = sum(n * max(0, a * m - b) for m, n in counts.items())
            result += scale * Q(positive, denominator * rho[i].denominator * delta.denominator)
        if i + 1 == len(primes):
            break
        atoms, atom_den = integer_atoms(p, e, scale)
        nxt = {}
        for m, n in counts.items():
            for multiplier, weight in atoms:
                product_value = m * multiplier
                nxt[product_value] = nxt.get(product_value, 0) + n * weight
        counts = nxt
        denominator *= atom_den
    return result


@lru_cache(None)
def integer_atoms(p, e, scale):
    """The differences of Pr(T>=j)=scale/p**j, as integer weights of 1+T."""
    a, b = scale.numerator, scale.denominator
    den = b * p**e
    weights = [den - a * p**(e-1)]
    weights.extend(a * (p-1) * p**(e-j-1) for j in range(1, e))
    weights.append(a)
    if min(weights) < 0 or sum(weights) != den:
        raise ValueError("invalid finite height law")
    return tuple((v,n) for v,n in enumerate(weights, 1) if n), den


def dominated(e, cap):
    return len(e) == len(cap) and all(x <= y for x,y in zip(e,cap))


def anchored_caps(path):
    """Read only the prime and exponent headers of the finite anchored models."""
    models = set()
    primes = None
    for line in path.read_text().splitlines():
        if line.startswith("# primes:"):
            primes = tuple(map(int, line.partition(":")[2].strip().split(",")))
        if line.startswith("# exps:"):
            cap = tuple(map(int, line.partition(":")[2].strip().split(",")))
            if primes is None or len(cap) != len(primes) or (primes,cap) in models:
                raise ValueError("invalid anchored model header")
            models.add((primes,cap))
            primes = None
    return models


def main(directory):
    groups = scalar_rows(directory / "scalar_lemma_u.tsv")
    maxima = []
    wanted = set()
    certificate_count = 0
    residual_count = 0
    direct_count = 0
    for primes in prime_supports(BOUND):
        witnesses = groups[primes]
        for cap, (prefix, scales, recorded) in witnesses.items():
            for p, e, c in zip(primes[prefix:], cap[prefix:], scales):
                rho = Q(p**e - 1, (p - 1) * p**e)
                if c <= 1 or 1 - 1/c < rho:
                    raise ValueError("stored scalar parameters violate the file convention")
            value = evaluate(primes, cap, prefix, scales)
            if value != recorded or value >= 1:
                raise ValueError(f"scalar bound under caps {cap}: computed {value}, stored {recorded}")
            maxima.append((value, cap))
            certificate_count += 1

        # A smaller model inherits an excluded cap. Also recompute B at the actual
        # vector, with the nearest dominating witness or, if none, a nearby witness.
        remaining = []
        certified = 0
        direct = 0
        vectors = list(exponent_vectors(primes, BOUND))
        expected = {10: 1484, 11: 248, 12: 21, 13: 1}
        if len(vectors) != expected[len(primes)]:
            raise ValueError("unexpected number of exponent vectors below the bound")
        for e in vectors:
            above = [cap for cap in witnesses if dominated(e, cap)]
            if above:
                selected = min(above, key=lambda cap: (sum(cap), cap))
                certified += 1
            else:
                remaining.append(e)
                selected = min(witnesses, key=lambda cap: (sum(abs(x-y) for x,y in zip(e,cap)), cap))
            prefix, scales, _ = witnesses[selected]
            direct_B = evaluate(primes, e, prefix, scales)
            if above and direct_B >= 1:
                raise ValueError(f"direct scalar regression at {e}: {direct_B}")
            direct += int(direct_B < 1)
        wanted.update((primes, e) for e in remaining
                      if not any(e != f and dominated(e, f) for f in remaining))
        residual_count += len(remaining)
        direct_count += direct
        print(f"{len(primes)} primes: {len(vectors)} vectors, {certified} by scalar caps, "
              f"{direct} directly below 1 with the selected parameters, {len(remaining)} for anchored bounds")
    if anchored_caps(directory / "global_anchored.tsv") != wanted:
        raise ValueError("anchored caps differ from the maximal residual vectors")
    if residual_count != 18 or len(wanted) != 13 or certificate_count != 738:
        raise ValueError("unexpected scalar or residual census")
    value, cap = max(maxima)
    print(f"Greatest of {certificate_count} stored scalar bounds: {value} at {cap}")
    print(f"Direct scalar exclusions: {direct_count}. The {residual_count} residual vectors "
          f"have exactly the {len(wanted)} declared maximal anchored caps.")


if __name__ == "__main__":
    try:
        directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("certs")
        main(directory)
    except Exception as exc:
        print(exc)
        print("FAIL")
        sys.exit(1)
    print("PASS")
