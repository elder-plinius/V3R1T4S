"""Standalone checker for one Wieferich pair claim (Python standard library only).

Template (V3R1T4S skill): copy it to claim/verify.py, to the winning lens's code/verify_pair.py and to the package's
verify-it-yourself/. As written it checks partial win p1. For a full-win claim, change the base range to
3 <= b <= 10125 and the p bound to the live table limit (4.8e12 for 1053..10125).

Definition (V3R1T4S bank, wieferich-other-bases-fischer-table, partial win p1): a base b with 10125 < b < 65537 that
is not a perfect power, a prime p > 1e12 not dividing b, and b^(p-1) == 1 (mod p^2), checked exactly.
Primality: deterministic Miller-Rabin with the 12 prime bases 2..37, which is proven correct for every
n < 318665857834031151167461 (Jiang & Deng 2014; Sorenson & Webster 2015).
Usage: python3 verify.py object/pair.json      (last output line: PASS or FAIL; exit status 0 or 1)
"""
import json, sys

MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
MR_BOUND = 318665857834031151167461


def is_prime(n):
    if n < 2:
        return False
    for q in MR_BASES:
        if n % q == 0:
            return n == q
    if n >= MR_BOUND:
        raise SystemExit("p is outside the deterministic Miller-Rabin bound; a primality certificate is needed\nFAIL")
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


def main(path):
    obj = json.load(open(path, encoding="utf-8"))
    b, p = int(obj["b"]), int(obj["p"])
    checks = {
        "10125 < b < 65537": 10125 < b < 65537,
        "b is not a perfect power": not is_perfect_power(b),
        "p > 1e12": p > 10 ** 12,
        "p is prime (deterministic Miller-Rabin)": is_prime(p),
        "p does not divide b": b % p != 0,
        "b^(p-1) == 1 mod p^2": pow(b, p - 1, p * p) == 1,
    }
    for k, v in checks.items():
        print(f"{'ok  ' if v else 'FAIL'} {k}")
    print(f"b = {b}, p = {p}, Fermat quotient q_p(b) mod p = {((pow(b, p - 1, p * p) - 1) // p) % p}")
    ok = all(checks.values())
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "object/pair.json"))
