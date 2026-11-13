"""spot_fresh.py — the frozen fresh-prime spot check (panel-time gate 6).

The stash prime (runs/2026-11-04-1132/attempts/skeptic/output/fresh_prime.txt)
is in NEITHER run's set. For widths k in KS (default 21, 24, 27; the claim adds
28 when the workers have exited and RAM allows), sweep the R->L fast DP at the
stash prime and require residue equality with the two-run CRT value of T(29,k)
(per-cell coverage rule as always). Exit 0 only if every checked width matches.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WS, 'runs', '2026-11-04-1132',
                                'attempts', 'constructor', 'code'))
sys.path.insert(0, os.path.join(WS, 'runs', '2026-11-04-1132',
                                'attempts', 'evaluator-first', 'code'))
from runb29_r2l import sweep_r2l_fast, sweep_r2l_sliced_fast  # noqa: E402
from crt_ab_early import load, crt  # noqa: E402

RA = os.path.join(WS, 'runs', '2026-11-04-0831', 'code', 'output',
                 'runA29_residues.txt')
RB = os.path.join(WS, 'runs', '2026-11-04-1132', 'code', 'output',
                  'runB29_residues.txt')
FRESH_FILE = os.path.join(WS, 'runs', '2026-11-04-1132', 'attempts',
                          'skeptic', 'output', 'fresh_prime.txt')
KS = [int(x) for x in sys.argv[1:]] or [21, 24, 27]


def main():
    fresh = int(open(FRESH_FILE).read().strip())
    A, B = load(RA), load(RB)
    ok = True
    for k in KS:
        dA, dB = A.get((k, 29)), B.get((k, 29))
        mA = mB = 1
        for p in dA:
            mA *= p
        for p in dB:
            mB *= p
        if not (3 ** (29 * k) < mA and 3 ** (29 * k) < mB):
            print(f"k={k}: NOT two-run covered yet (A {len(dA)} primes / "
                  f"B {len(dB)} primes) — skipped")
            continue
        xa, _ = crt([dA[p] for p in sorted(dA)], sorted(dA))
        xb, _ = crt([dB[p] for p in sorted(dB)], sorted(dB))
        assert xa == xb
        r = (sweep_r2l_sliced_fast(k, 29, fresh) if k >= 27
             else sweep_r2l_fast(k, 29, fresh))[-1]
        good = r == xa % fresh
        print(f"k={k}: fresh-prime residue == T(29,{k}) mod fresh "
              f"({len(str(xa))}-digit value): {'OK' if good else 'FAIL'}")
        ok = ok and good
    print("SPOT_FRESH:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
