#!/usr/bin/env python3
"""
Standalone Exact Rational Verifier 2 (Python 3 stdlib `fractions.Fraction`, zero floating-point).
Independently verifies that every finite covering system of Z with pairwise distinct odd moduli > 1
has least common multiple L >= 168,131,152,814,625.
"""
import sys
import math
from fractions import Fraction

CLAIMED_LOWER_BOUND = 168131152814625
MAX_EXCLUDED_LCM = CLAIMED_LOWER_BOUND - 1
EGEOZTURK_FORUM_BOUND = 11486475
SCHROEDER_ZENODO_BOUND = 9704539845


def fail(reason: str) -> None:
    sys.stderr.write(f"VERIFY_PY ERROR: {reason}\n")
    print("FAIL")
    sys.exit(1)


def generate_odd_primes(limit_count: int) -> list[int]:
    primes: list[int] = []
    candidate = 3
    while len(primes) < limit_count:
        if all(candidate % q != 0 for q in primes):
            primes.append(candidate)
        candidate += 2
    return primes


def parse_strict_positive_int(token: str) -> int:
    if not token or not token.isdigit():
        fail(f"invalid integer token: {token!r}")
    val = int(token)
    if val <= 0:
        fail(f"non-positive integer token: {token!r}")
    return val


def load_certificate_tsv(tsv_path: str) -> dict[tuple[int, ...], tuple[int, tuple[int, ...], Fraction]]:
    try:
        with open(tsv_path, "r", encoding="utf-8") as fh:
            raw_lines = fh.read().splitlines()
    except OSError as exc:
        fail(f"unable to read certificate TSV: {exc}")

    if not raw_lines:
        fail("empty certificate TSV")
    if raw_lines[0] != "exponents\tk0\tm_over_32\texact_upper_bound":
        fail(f"unexpected header: {raw_lines[0]!r}")

    records: dict[tuple[int, ...], tuple[int, tuple[int, ...], Fraction]] = {}
    prev_key = None
    for line_no, line in enumerate(raw_lines[1:], start=2):
        parts = line.split("\t")
        if len(parts) != 4:
            fail(f"line {line_no}: expected 4 tab-separated columns, got {len(parts)}")
        ex_str, k0_str, ms_str, bound_str = parts
        exps = tuple(parse_strict_positive_int(tok) for tok in ex_str.split(","))
        if len(exps) < 2:
            fail(f"line {line_no}: exponent tuple length < 2")
        if prev_key is not None and exps <= prev_key:
            fail(f"line {line_no}: rows not strictly canonically ordered")
        prev_key = exps

        k0 = parse_strict_positive_int(k0_str)
        if k0 >= len(exps):
            fail(f"line {line_no}: k0={k0} out of range for rank {len(exps)}")

        ms = tuple(parse_strict_positive_int(tok) for tok in ms_str.split(","))
        if len(ms) != len(exps) - k0:
            fail(f"line {line_no}: expected {len(exps) - k0} cap numerators, got {len(ms)}")

        if "/" not in bound_str or bound_str.count("/") != 1:
            fail(f"line {line_no}: malformed fraction {bound_str!r}")
        n_str, d_str = bound_str.split("/")
        b_num = parse_strict_positive_int(n_str)
        b_den = parse_strict_positive_int(d_str)
        if math.gcd(b_num, b_den) != 1:
            fail(f"line {line_no}: fraction {bound_str} is not reduced")
        frac = Fraction(b_num, b_den)
        if frac >= 1:
            fail(f"line {line_no}: fraction {bound_str} is >= 1")
        records[exps] = (k0, ms, frac)

    return records


def pure_deletion_upper_bound(primes: list[int], exps: tuple[int, ...]) -> Fraction:
    prod_term = Fraction(1, 1)
    sum_term = Fraction(0, 1)
    for p, e in zip(primes, exps):
        pe = p ** e
        s_m = ((p - 2) * pe + 1) // (p - 1)
        theta = Fraction((pe - 1) // (p - 1), s_m)
        prod_term *= (1 + theta)
        sum_term += theta
    return prod_term - 1 - sum_term


def distortion_upper_bound(primes: list[int], exps: tuple[int, ...], k0: int, ms: tuple[int, ...]) -> Fraction:
    rank = len(exps)
    prod_base = Fraction(1, 1)
    sum_base = Fraction(0, 1)
    dist: dict[int, Fraction] = {1: Fraction(1, 1)}

    for m in range(k0):
        p = primes[m]
        e = exps[m]
        pe = p ** e
        s_m = ((p - 2) * pe + 1) // (p - 1)
        if ((p - 2) * pe + 1) % (p - 1) != 0:
            fail("s_m not exact integer")
        theta = Fraction((pe - 1) // (p - 1), s_m)
        prod_base *= (1 + theta)
        sum_base += theta

        tails = [Fraction(1, 1)] + [Fraction(p ** (e - t), s_m) for t in range(1, e + 1)] + [Fraction(0, 1)]
        new_dist: dict[int, Fraction] = {}
        for t in range(e + 1):
            prob = tails[t] - tails[t + 1]
            if prob < 0:
                fail("negative probability in base coordinate")
            if prob > 0:
                mult = 1 + t
                for mv, pv in dist.items():
                    new_dist[mv * mult] = new_dist.get(mv * mult, Fraction(0, 1)) + pv * prob
        if sum(new_dist.values()) != 1:
            fail("base distribution does not sum to 1")
        dist = new_dist

    total = prod_base - 1 - sum_base

    for idx, i in enumerate(range(k0, rank)):
        p = primes[i]
        e = exps[i]
        pe = p ** e
        rho_pure = Fraction(pe - 1, (p - 1) * pe)
        c_cap = Fraction(ms[idx], 32)
        if not (1 < c_cap <= p):
            fail(f"cap C_i={c_cap} outside (1, {p}]")
        delta = 1 - Fraction(1, c_cap)
        if delta < rho_pure:
            fail(f"delta={delta} < rho_pure={rho_pure}")

        stage_loss = Fraction(0, 1)
        for mv, pv in dist.items():
            alpha = rho_pure * mv
            if alpha > delta:
                stage_loss += pv * c_cap * (alpha - delta)
        total += stage_loss

        if i < rank - 1:
            tails = [Fraction(1, 1)] + [min(Fraction(1, 1), c_cap / (p ** t)) for t in range(1, e + 1)] + [Fraction(0, 1)]
            new_dist = {}
            for t in range(e + 1):
                prob = tails[t] - tails[t + 1]
                if prob < 0:
                    fail("negative probability in distortion coordinate")
                if prob > 0:
                    mult = 1 + t
                    for mv, pv in dist.items():
                        new_dist[mv * mult] = new_dist.get(mv * mult, Fraction(0, 1)) + pv * prob
            if sum(new_dist.values()) != 1:
                fail("stage distribution does not sum to 1")
            dist = new_dist

    return total


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: verify_lcm_bound_py.py <certificate.tsv>")

    primes = generate_odd_primes(20)

    # Sanity check 1: Erdos 1950 covering {0 mod 2, 0 mod 3, 1 mod 4, 5 mod 6, 7 mod 12}
    erdos_cov = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
    if not all(any(x % n == a for a, n in erdos_cov) for x in range(12)):
        fail("Erdos 1950 covering check failed")
    if pure_deletion_upper_bound([2, 3], (2, 1)) < 1:
        fail("soundness error on L=12")

    # Sanity check 2: Factorization and abundancy of 168,131,152,814,625
    sharp_exps = (4, 3, 2, 2, 1, 1, 1, 1, 1)
    sharp_val = 1
    sig_num, sig_den = 1, 1
    for p, e in zip(primes, sharp_exps):
        pe = p ** e
        sharp_val *= pe
        sig_num *= (pe * p - 1) // (p - 1)
        sig_den *= pe
    if sharp_val != CLAIMED_LOWER_BOUND or sig_num < 2 * sig_den:
        fail("sharp frontier factorization or abundancy mismatch")
    if CLAIMED_LOWER_BOUND <= EGEOZTURK_FORUM_BOUND or CLAIMED_LOWER_BOUND <= SCHROEDER_ZENODO_BOUND:
        fail("claimed lower bound does not exceed prior records")

    certs = load_certificate_tsv(sys.argv[1])

    # Iterative stack enumeration of all initial-prime abundant profiles <= MAX_EXCLUDED_LCM
    all_abundant: list[tuple[int, tuple[int, ...]]] = []
    stack: list[tuple[int, int, tuple[int, ...], int, int]] = [(0, 1, (), 1, 1)]
    while stack:
        idx, cur_val, cur_exps, s_num, s_den = stack.pop()
        if idx > 0 and s_num >= 2 * s_den:
            all_abundant.append((cur_val, cur_exps))
        if idx >= len(primes):
            continue
        p = primes[idx]
        if cur_val * p > MAX_EXCLUDED_LCM:
            continue
        pe = p
        e = 1
        while cur_val * pe <= MAX_EXCLUDED_LCM:
            psum = (pe * p - 1) // (p - 1)
            stack.append((idx + 1, cur_val * pe, cur_exps + (e,), s_num * psum, s_den * pe))
            pe *= p
            e += 1

    band_map: dict[int, tuple[int, ...]] = {
        val: exps for val, exps in all_abundant if 3 * val > MAX_EXCLUDED_LCM
    }

    # Verify every abundant profile <= MAX_EXCLUDED_LCM scales by 3^k into band_map
    for val, _ in all_abundant:
        scaled = val
        while 3 * scaled <= MAX_EXCLUDED_LCM:
            scaled *= 3
        if scaled not in band_map:
            fail(f"abundant profile {val} failed 3^k band scaling")

    seen_certs: set[tuple[int, ...]] = set()
    bff_count = 0
    cert_count = 0
    worst_bound = Fraction(0, 1)
    worst_bff = Fraction(0, 1)

    for val, exps in band_map.items():
        bff_val = pure_deletion_upper_bound(primes, exps)
        if bff_val < 1:
            if exps in certs:
                fail(f"BFF-refuted profile {exps} present in certificate")
            if bff_val > worst_bff:
                worst_bff = bff_val
            bff_count += 1
        else:
            if exps not in certs:
                fail(f"band profile {exps} (L*={val}) missing from certificate")
            k0, ms, expected_frac = certs[exps]
            actual_frac = distortion_upper_bound(primes, exps, k0, ms)
            if actual_frac != expected_frac:
                fail(f"fraction mismatch on {exps}: got {actual_frac}, expected {expected_frac}")
            if actual_frac >= 1:
                fail(f"upper bound >= 1 on {exps}: {actual_frac}")
            if actual_frac > worst_bound:
                worst_bound = actual_frac
            seen_certs.add(exps)
            cert_count += 1

    if len(seen_certs) != len(certs):
        fail("extra unused rows in certificate TSV")

    print(f"[Verifier 2 - Python Exact Fractions] Certified lower bound L at least {CLAIMED_LOWER_BOUND} (168,131,152,814,625)")
    print(f"  sharp_frontier_factorization                      = 3^4 * 5^3 * 7^2 * 11^2 * 13 * 17 * 19 * 23 * 29")
    print(f"  max_excluded_lcm                                  = {MAX_EXCLUDED_LCM} (168,131,152,814,624)")
    print(f"  band_lower_threshold_floor_B0_div_3               = {MAX_EXCLUDED_LCM // 3}")
    print(f"  total_initial_prime_abundant_profiles_below_bound = {len(all_abundant)}")
    print(f"  band_profiles_checked                             = {len(band_map)}")
    print(f"  refuted_by_pure_deletion_bff                      = {bff_count}")
    print(f"  max_pure_deletion_bff_measure                     = {worst_bff.numerator}/{worst_bff.denominator}")
    print(f"  refuted_by_distortion_certificate                 = {cert_count}")
    print(f"  max_certified_covered_measure                     = {worst_bound.numerator}/{worst_bound.denominator}")
    print(f"  min_certified_uncovered_numerator_surplus         = {worst_bound.denominator - worst_bound.numerator}")
    print(f"  ratio_over_egeozturk_11486475                     = {CLAIMED_LOWER_BOUND // EGEOZTURK_FORUM_BOUND}x")
    print(f"  ratio_over_schroeder_9704539845                   = {CLAIMED_LOWER_BOUND // SCHROEDER_ZENODO_BOUND}x")
    print("VERIFY_PY: PASS")


if __name__ == "__main__":
    main()
