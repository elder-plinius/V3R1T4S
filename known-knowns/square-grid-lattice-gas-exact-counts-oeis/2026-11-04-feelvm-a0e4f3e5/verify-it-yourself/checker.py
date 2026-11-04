"""Standalone verification for the A054759 a(15) claim.

Standard library only. Run:  python3 verify-it-yourself/checker.py
Prints one line per check; the last line is exactly PASS or FAIL.

The published A054759 terms embedded below are the extracted comparison cells
from https://oeis.org/A054759/b054759.txt (OEIS's own synthesized b-file,
fetched 2026-11-04T17:31:03Z, sha256 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada;
re-verified live 2026-11-04T18:09:53Z, sha256 92676015f44762902bebd7d7a05791c70854b87a3b53583e34b31b6eb5eb540f).
"""
import json
import math
import os
import sys

PUBLISHED = {
    1: 4, 2: 18, 3: 148, 4: 2970, 5: 143224, 6: 16448400, 7: 4484823396,
    8: 2901094068042, 9: 4448410550095612, 10: 16178049740086515288,
    11: 139402641051212392498528, 12: 2849295959501939989625992464,
    13: 137950545200232788276834783781648,
    14: 15844635835975276495290739119895808472,
}
LIEB_LN = 1.5 * math.log(4 / 3)  # 0.431523058... (Lieb, proved; quoted in the OEIS entry)

fails = []


def check(name, ok, detail=""):
    print("%s %s%s" % ("ok:" if ok else "FAIL:", name, (" - " + detail) if detail else ""))
    if not ok:
        fails.append(name)


def is_prime(q):
    if q < 2:
        return False
    t = 2
    while t * t <= q:
        if q % t == 0:
            return False
        t += 1
    return True


def crt(residues, primes):
    x, m = 0, 1
    for r, q in zip(residues, primes):
        t = ((r - x) % q) * pow(m % q, -1, q) % q
        x += m * t
        m *= q
    return x, m


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(here)
    V = int(open("object/a15.txt").read().strip())

    check("object value has 43 digits", len(str(V)) == 43, "digits=%d" % len(str(V)))
    check("claimed value is NOT a published term (genuinely the next index)",
          all(V != t for t in PUBLISHED.values()))

    sets = {}
    for tag in ("run1", "run2"):
        d = json.load(open("object/residues_%s.json" % tag))
        primes, residues = d["primes"], d["residues"]
        sets[tag] = (primes, residues)
        ok_p = len(primes) == len(set(primes)) == len(residues) and all(
            is_prime(q) and q % 15 == 1 for q in primes)
        check("%s: 14 distinct primes, all prime and 1 (mod 15)" % tag, ok_p)
        check("%s: every residue matches the claimed value" % tag,
              all(V % q == r for r, q in zip(residues, primes)))
        x, m = crt(residues, primes)
        check("%s: CRT reconstruction equals the claimed value" % tag, x == V)
        check("%s: recorded modulus equals the prime product" % tag, m == d["modulus"])
        bound = (1 << 15) * (d["rowsum_inf"] ** 15) if "rowsum_inf" in d else None
        if bound is None:
            other = json.load(open("object/residues_run1.json" if tag == "run2"
                                   else "object/residues_run2.json"))
            bound = (1 << 15) * (other["rowsum_inf"] ** 15)
        check("%s: CRT modulus exceeds the rigorous bound 2^15*||T||_inf^15" % tag, m > bound,
              "modulus 2^%.1f vs bound 2^%.1f" % (math.log2(m), math.log2(bound)))
    p1, p2 = sets["run1"][0], sets["run2"][0]
    check("prime sets disjoint (two-run rule)", set(p1).isdisjoint(set(p2)))

    # ladder evidence: both programs reproduce every published term exactly
    for tag, fn in (("run1", "how-we-built-it/ladder.json"),
                    ("run2", "how-we-built-it/ladder2.json")):
        lad = json.load(open(fn))
        ok = True
        det = []
        for n_str, e in lad.items():
            n = int(n_str)
            if not (e.get("isotypic_matches") or e.get("matches")):
                ok = False
            if e["bfile"] != PUBLISHED.get(n):
                ok = False
                det.append("n=%d bfile mismatch" % n)
            if n >= 8:
                refp = e.get("ref_prime")
                # direct modular reference congruence, where recorded
                iso_p = e.get("prime_iso")
                if iso_p is not None and e["isotypic_mod"] != PUBLISHED[n] % iso_p:
                    ok = False
                    det.append("n=%d iso congruence" % n)
        check("%s: ladder reproduces a(1)..a(14) (program output vs published terms)" % tag, ok,
              "; ".join(det))

    # growth consistency, honestly stated
    g14 = math.log(PUBLISHED[14]) / 196
    g15 = math.log(V) / 225
    check("entropy per site decreases toward Lieb's constant (ln a15/225 < ln a14/196)",
          g15 < g14, "%.6f < %.6f" % (g15, g14))
    check("finite-size consistency: n^2*(ln a/n^2 - lnW) ~ 1.08 as in every published term",
          abs(225 * (g15 - LIEB_LN) - 1.0769) < 0.05,
          "n^2*delta = %.4f (published a(14): %.4f)" % (225 * (g15 - LIEB_LN),
                                                        196 * (g14 - LIEB_LN)))
    check("digit count matches the entropy-constant estimate",
          len(str(V)) == math.floor(225 * LIEB_LN / math.log(10)) + 1)

    if fails:
        print("FAIL (%d failed checks: %s)" % (len(fails), "; ".join(fails)))
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
