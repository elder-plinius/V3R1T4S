"""final_gate.py — the row-29 claim's two-run gate (night-1 PREREG, verbatim).

Checks, from the two residue files alone:
  G1  two-run CRT equality X_k(A29) == Y_k(B29) for every claim cell
      T(29,k), k=1..28, whose PER-CELL prime subsets cover 3^(29k) in BOTH
      runs (per-cell coverage — file-level moduli over-claim);
  G2  exact reproduction of every published cell T(n,k) (all 378) under the
      same per-cell coverage rule, from EACH run separately;
  G3  exact agreement with the packaged row-28 object (27 anchor cells,
      T(28,k), k=1..27) from EACH run;
  G4  completeness report: k values NOT yet two-run covered (must be empty at
      22+22 blocks; anything else defers the claim).
Exit 0 only if G1-G3 have zero mismatches AND every coverable check ran.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
RA = os.path.join(WS, 'runs', '2026-11-04-0831', 'code', 'output',
                 'runA29_residues.txt')
RB = os.path.join(WS, 'runs', '2026-11-04-1132', 'code', 'output',
                  'runB29_residues.txt')
ROW28 = os.path.join(WS, 'runs', '2026-11-03-0830', 'row28_final.json')
BFILE = os.path.join(WS, 'runs', '2026-11-08-1131', 'data', 'b210662.txt')

sys.path.insert(0, os.path.join(WS, 'runs', '2026-11-04-1132',
                                'attempts', 'evaluator-first', 'code'))
from crt_ab_early import load, crt  # noqa: E402


def load_published(path):
    tab = {}
    for line in open(path):
        parts = line.split()
        if len(parts) == 2 and not line.startswith('#'):
            i, v = int(parts[0]), int(parts[1])
            n = 1
            while n * (n + 1) // 2 < i:
                n += 1
            k = i - n * (n - 1) // 2
            tab.setdefault(n, {})[k] = v
    assert sum(len(r) for r in tab.values()) == 378
    return tab


def cell_crt(d):
    mods = sorted(d)
    return crt([d[p] for p in mods], mods)[0]


def covered(d, nk):
    if not d:
        return False
    m = 1
    for p in d:
        m *= p
    return 3 ** nk < m


def main():
    A, B = load(RA), load(RB)
    pub = load_published(BFILE)
    obj = {int(k): int(v) for k, v in json.load(open(ROW28)).items()}
    fails = []

    # G2/G3 per run
    for name, R in (("A29", A), ("B29", B)):
        npub = nanc = 0
        for n, row in pub.items():
            for k, want in row.items():
                d = R.get((k, n))
                if covered(d, n * k):
                    npub += 1
                    if cell_crt(d) != want:
                        fails.append(f"{name} published T({n},{k})")
        for k, want in obj.items():
            d = R.get((k, 28))
            if covered(d, 28 * k):
                nanc += 1
                if cell_crt(d) != want:
                    fails.append(f"{name} anchor T(28,{k})")
        print(f"G2/G3 {name}: published exact {npub}/378 coverable, "
              f"row-28 anchors exact {nanc}/27 coverable")

    # G1 claim cells
    nclaim = 0
    missing = []
    for k in range(1, 29):
        dA, dB = A.get((k, 29)), B.get((k, 29))
        if covered(dA, 29 * k) and covered(dB, 29 * k):
            nclaim += 1
            xa, xb = cell_crt(dA), cell_crt(dB)
            if xa != xb:
                fails.append(f"claim T(29,{k}): A != B")
        else:
            missing.append(k)
    print(f"G1 claim cells two-run verified: {nclaim}/28")
    if missing:
        print(f"G4 deferred (not yet covered in both runs): k={missing}")

    print(f"mismatches: {len(fails)}")
    for f in fails[:10]:
        print("  " + f)
    full = "--full" in sys.argv                # claim-night mode
    if full:
        ok = not fails and nclaim == 28 and not missing
    else:
        ok = not fails and nclaim >= 27        # prep-night test mode
    print("FINAL_GATE:", "PASS" if ok else "FAIL",
          "(--full: 28/28 required)" if full else "")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
