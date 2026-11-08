"""V3R1T4S — exact checker for a Wieferich pair, written from the bank definition (evaluator-first).

A pair (b, p) passes when 3 <= b <= 10125, b is not a perfect power, p is a proven prime not dividing b, and
pow(b, p-1, p^2) == 1.  The table part (p above the base's live limit, absent from its row) is checked separately.
Primality proof: deterministic Miller-Rabin with the 12 prime bases 2..37, proven correct for every
n < 318665857834031151167461 (~3.2e23; Jiang & Deng 2014, Sorenson & Webster 2015) — KNOWN result, used only below
that bound.  BPSW (gmpy2) runs as an independent second opinion when available.
Usage: python wieferich_check.py <b> <p> [bmin bmax]   or   python wieferich_check.py --selftest
"""
import sys

MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
MR_BOUND = 318665857834031151167461


def is_prime_proven(n):
    if n < 2:
        return False
    for q in MR_BASES:
        if n % q == 0:
            return n == q
    if n >= MR_BOUND:
        raise ValueError("outside the deterministic Miller-Rabin bound; needs ECPP")
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_perfect_power(n):
    if n < 4:
        return False
    for k in range(2, n.bit_length() + 1):
        r = round(n ** (1.0 / k))
        for c in (r - 1, r, r + 1):
            if c > 1 and c ** k == n:
                return True
    return False


def check(b, p, bmin=3, bmax=10125):
    out = {"b": b, "p": p, "base_in_range": bmin <= b <= bmax, "base_not_perfect_power": not is_perfect_power(b),
           "p_proven_prime": is_prime_proven(p)}
    try:
        import gmpy2
        out["p_bpsw"] = bool(gmpy2.is_bpsw_prp(p))
    except Exception:
        out["p_bpsw"] = "n/a"
    x = pow(b, p - 1, p * p)
    out["p_not_dividing_b"] = b % p != 0
    out["wieferich"] = x == 1
    out["fermat_quotient_mod_p"] = ((x - 1) // p) % p
    out["PASS"] = all(out[k] is True for k in ("base_in_range", "base_not_perfect_power", "p_proven_prime",
                                                 "p_not_dividing_b", "wieferich"))
    return out


def selftest():
    nxt = 4572343153717 + 2
    while not is_prime_proven(nxt):
        nxt += 2
    cases = [
        ("positive: table row 3626", 3626, 4572343153717, True),
        ("positive: table row 9223", 9223, 4572201984841, True),
        ("range rule: base 2, p=1093 must FAIL (arithmetic pair, base out of range)", 2, 1093, False),
        ("negative: 3626 with the next prime", 3626, nxt, False),
        ("negative: composite p", 3626, 4572343153717 * 3, False),
        ("negative: perfect-power base 1089 = 33^2", 1089, 1000003, False),
    ]
    ok = True
    for name, b, p, expect in cases:
        r = check(b, p)
        good = r["PASS"] == expect
        ok &= good
        print(f"{'ok  ' if good else 'FAIL'} {name}: {r}")
    ok &= check(2, 1093)["wieferich"] is True
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(0 if selftest() else 1)
    args = [int(x) for x in sys.argv[1:]]
    print(check(*args))
