# How we built it

The object's code (object/code/par/main.go) is the code that found the bound. The thresholds came from
object/code/kcheck.py (exact binary search on the 10^-6 grid). object/code/verify_cert.py then certified them:

    ./par.exe N 6 > pN.txt              # N = 10, 12, 14, 16, 18, 20
    python kcheck.py pN.txt             # outputs: object/outputs/k18.txt, k20.txt
    python verify_cert.py p20.txt 263376  # object/outputs/verify_N20.txt

Exploration before the freeze is disclosed in PREREG.md. It covered NAW counts, Alm certificates, and the
canonical-geodesic criterion for N <= 16. PREREG.md also gives the frozen method, checker and thresholds. It names
0.21103 as the record; the panel later found 0.2522 (see panel/gate.md). No null test was needed, because the result
is a deterministic certificate.

Self-break checks (selfbreak/; outputs in selfbreak/outputs/):
- groundtruth.py A 300 (outputs/partA_300.txt). 300 random configurations, the true BFS parent tree, every tree
  path. Checks: the path is a NAW, every forced site is closed, and every child of the endpoint is a counted
  extension. Separately, two code mutations were run as negative controls, a reversed corner rule against the true
  tree and a loosened shortcut gap; both failed at once (outputs/VERDICT.md).
- groundtruth.py B 9 (outputs/b9.txt). The full N = 9 table from complete paths, equal to the enumerator's
  (outputs/go9.txt).
- groundtruth.py C N prefix. Full-depth subtrees below random prefixes, compared with par_prefix_main.go, a
  mechanical prefix-mode copy of the enumerator whose no-prefix output equals the enumerator's at N = 12:
  - N = 18: 10 of 10 random 10-step prefixes match (outputs/prefix_check_N18.txt);
  - N = 20: 10 of 10 random 12-step prefixes match (outputs/prefix_check_N20.txt).
- corner_rule_24.py (outputs/corner_rule_24.txt). All 24 ordered pairs of perpendicular steps. It compares the true
  BFS parent, the code's test and the PROOF.md definition: 0 disagreements, and the corner is forced in 12 of the 24
  cases.
- outputs/CHECKS.md and outputs/VERDICT.md: the self-break plan and verdict (SURVIVES).
