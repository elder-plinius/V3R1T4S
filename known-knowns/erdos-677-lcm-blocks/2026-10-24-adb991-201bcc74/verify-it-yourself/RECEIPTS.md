# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon @ 2.10GHz), 15 GB of memory, Python 3.13.16
with gmpy2 2.3.2, mpmath 1.3.0 and numpy 2.5.4 (`PY` pointed at a virtual environment holding them), gcc 13.3.0 as
`cc`. No other heavy job ran on the machine during these runs. Every run was started from a copy of the package folder as
`PY=<a Python with the three modules> nice -n 10 sh verify-it-yourself/run_checks.sh [--all]` with the default
`JOBS=3`, so at most three Python jobs ran at once; the script runs each job at `nice -n 10` as well. Start and end
times from `date -u`, wall time from `date +%s`. The sha256 of the run_checks.sh used for sections 1, 2 and 4 is the
one listed in `SHA256SUMS`.

## 1. Default mode, the package as shipped (exit 0, 164 s, 2026-10-24T13:29:02Z to 2026-10-24T13:31:46Z)

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 1 <= k <= 25, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 3
step 1 object files: 19 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: search COMPLETE with 2 candidates, 0 exact-equal; 0 missing ratios; both margin checkers 'TOTAL pairs=63041 failures=0 undecided=0'; deep_rig k = 3..25 product_solutions=0, 1174616 window candidates: ok
python: 3.13.16 gmpy2 2.3.2 mpmath 1.3.0 numpy 2.5.4
step 3 tools: ok
  search677b 1100000 4242: exit 0, 4 s, '# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=4s'; equal to object/out/search_N1.1e6.txt (times stripped)
  verify_cands.py: 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0'; equal to object/out/verify_N1.1e6.txt (times stripped)
  exact judge check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680: lcms differ, not a counterexample
  exact judge check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040: lcms differ, not a counterexample
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns (default): rigm deep_15-16 deep_3-13 deep_14-14 taskA
  finished deep_15-16 (object/deep_rig.py 15 16 1040 0.001 1000000): exit 0, 54 s
  finished deep_3-13 (object/deep_rig.py 3 13 1040 0.001 1000000): exit 0, 55 s
  finished taskA (object/taskA_ratio_audit.py 3000): exit 0, 4 s
  finished deep_14-14 (object/deep_rig.py 14 14 1040 0.001 1000000): exit 0, 55 s
  finished rigm (object/rig_margin.py 3 25 1000000 1 1000): exit 0, 159 s
  taskA_ratio_audit.py 3000: 'TOTAL missing over k=3..25: 0', total 970; r outside sets: 0; byte-identical to object/out/taskA_ratio_audit_NB3000.txt
  rig_margin.py 3 25 1000000 1 1000: 'TOTAL pairs=63041 failures=0 undecided=0'; equal to object/out/rig_margin_k3-25_X1e6_eta1e-3.txt (time_s stripped)
  k=15: admissible_r=283 enumerated_pairs(q(q rho-p)<U)=2418 window_candidates=2365 product_solutions=0: equal to the saved line
  k=16: admissible_r=202 enumerated_pairs(q(q rho-p)<U)=7884 window_candidates=1884 product_solutions=0: equal to the saved line
  deep_rig.py 15 16: 'TOTAL window candidates=4249 product solutions=0 (X0=1000000, QMAX=10^495)'
  k=3: admissible_r=1 enumerated_pairs(q(q rho-p)<U)=0 window_candidates=0 product_solutions=0: equal to the saved line
  k=4: admissible_r=1 enumerated_pairs(q(q rho-p)<U)=4 window_candidates=2 product_solutions=0: equal to the saved line
  k=5: admissible_r=7 enumerated_pairs(q(q rho-p)<U)=13 window_candidates=13 product_solutions=0: equal to the saved line
  k=6: admissible_r=4 enumerated_pairs(q(q rho-p)<U)=25 window_candidates=8 product_solutions=0: equal to the saved line
  k=7: admissible_r=22 enumerated_pairs(q(q rho-p)<U)=43 window_candidates=43 product_solutions=0: equal to the saved line
  k=8: admissible_r=13 enumerated_pairs(q(q rho-p)<U)=149 window_candidates=39 product_solutions=0: equal to the saved line
  k=9: admissible_r=31 enumerated_pairs(q(q rho-p)<U)=108 window_candidates=107 product_solutions=0: equal to the saved line
  k=10: admissible_r=37 enumerated_pairs(q(q rho-p)<U)=551 window_candidates=137 product_solutions=0: equal to the saved line
  k=11: admissible_r=157 enumerated_pairs(q(q rho-p)<U)=799 window_candidates=780 product_solutions=0: equal to the saved line
  k=12: admissible_r=121 enumerated_pairs(q(q rho-p)<U)=2745 window_candidates=678 product_solutions=0: equal to the saved line
  k=13: admissible_r=472 enumerated_pairs(q(q rho-p)<U)=3388 window_candidates=3343 product_solutions=0: equal to the saved line
  deep_rig.py 3 13: 'TOTAL window candidates=5150 product solutions=0 (X0=1000000, QMAX=10^495)'
  k=14: admissible_r=337 enumerated_pairs(q(q rho-p)<U)=10984 window_candidates=2734 product_solutions=0: equal to the saved line
  deep_rig.py 14 14: 'TOTAL window candidates=2734 product solutions=0 (X0=1000000, QMAX=10^495)'
step 5 reruns: ratio audit, interval margin checker and the enumeration for k = 3..16 equal the saved outputs: ok
  (not rerun by default: deep_rig.py k = 17..25 and rig_margin_exact.py; use --all)
total time: 164 s
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s, 2026-10-24T13:31:46Z)

In a copy of the package, the middle ASCII digit of the first text file in object/ was changed, the same corruption
repo/kit/check_run.py applies to a copy of the package. The first file is object/PROOF.md; the change (from the
script that applied it):

```
object/PROOF.md line 62: digit 1 -> 0; sha256 24ceb08ca73e9bc4eef8937c1e73636277432e081a232f187a9f0b9bb5b60626
context before: This covers every (n, k) with X := n + (k+1)/2 < 10^6 and k ≤ K*, because then n + k < 10^6 + (k−1)/2 ≤ 1.1·10^6.
context after:  This covers every (n, k) with X := n + (k+1)/2 < 10^6 and k ≤ K*, because then n + k < 10^6 + (k−1)/2 ≤ 1.0·10^6.
```

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 1 <= k <= 25, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 3
problem: object/PROOF.md has sha256 24ceb08ca73e9bc4eef8937c1e73636277432e081a232f187a9f0b9bb5b60626, the package records 201bcc74dfe80bd57d43eb3f97330d8dc702623df9808c6ebc00f27b21b01e83 (the file is not the one the panel read)
FAIL
```

## 3. Control: one digit of a saved output changed and its recorded hash forged too (exit 1, 161 s, 2026-10-24T13:31:46Z to 2026-10-24T13:34:27Z)

In another copy, the middle ASCII digit of object/out/rig_margin_k3-25_X1e6_eta1e-3.txt was changed, and that file's
line in the copy's run_checks.sh (`SUMS`) was given the sha256 of the changed file, so that steps 1 and 2 pass. Only
the recomputation can catch this one, and it does: the fresh output of rig_margin.py says r=65/63 for k = 16, as the
original file does.

```
object/out/rig_margin_k3-25_X1e6_eta1e-3.txt line 15: digit 3 -> 1; sha256 cf1e81cf1c1b247053f9db1a762b0caf4edc9493caf861441cabf737c5d9560f
context before: k=16 pairs=202 proved=202 failures=0 undecided=0 time_s=0.4 worst_rel_margin_lower_bound=0.99999998 at r=65/63
context after:  k=16 pairs=202 proved=202 failures=0 undecided=0 time_s=0.4 worst_rel_margin_lower_bound=0.99999998 at r=65/61
42:cf1e81cf1c1b247053f9db1a762b0caf4edc9493caf861441cabf737c5d9560f object/out/rig_margin_k3-25_X1e6_eta1e-3.txt
```

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 1 <= k <= 25, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 3
step 1 object files: 19 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: search COMPLETE with 2 candidates, 0 exact-equal; 0 missing ratios; both margin checkers 'TOTAL pairs=63041 failures=0 undecided=0'; deep_rig k = 3..25 product_solutions=0, 1174616 window candidates: ok
python: 3.13.16 gmpy2 2.3.2 mpmath 1.3.0 numpy 2.5.4
step 3 tools: ok
  search677b 1100000 4242: exit 0, 5 s, '# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=5s'; equal to object/out/search_N1.1e6.txt (times stripped)
  verify_cands.py: 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0'; equal to object/out/verify_N1.1e6.txt (times stripped)
  exact judge check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680: lcms differ, not a counterexample
  exact judge check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040: lcms differ, not a counterexample
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns (default): rigm deep_15-16 deep_3-13 deep_14-14 taskA
  finished deep_3-13 (object/deep_rig.py 3 13 1040 0.001 1000000): exit 0, 55 s
  finished deep_15-16 (object/deep_rig.py 15 16 1040 0.001 1000000): exit 0, 56 s
  finished taskA (object/taskA_ratio_audit.py 3000): exit 0, 4 s
  finished deep_14-14 (object/deep_rig.py 14 14 1040 0.001 1000000): exit 0, 52 s
  finished rigm (object/rig_margin.py 3 25 1000000 1 1000): exit 0, 155 s
  taskA_ratio_audit.py 3000: 'TOTAL missing over k=3..25: 0', total 970; r outside sets: 0; byte-identical to object/out/taskA_ratio_audit_NB3000.txt
problem: rig_margin.py 3 25 1000000 1 1000: output differs from object/out/rig_margin_k3-25_X1e6_eta1e-3.txt (time_s stripped)
FAIL
```

## 4. Mode --all (exit 0, 5179 s, 2026-10-24T12:02:19Z to 2026-10-24T13:28:38Z)

Run by the contributor on the otherwise idle machine, with 3 jobs, from a copy of the package's object/ and
verify-it-yourself/ folders (the only folders the script reads). It reruns the five enumeration commands of
how-we-built-it/claim/REPRODUCE.md and the exact-rational margin checker for every k = 3..25. The panel's REPRODUCE
skeptic had rerun the exact margin checker for k = 3..24 only (panel/reproduce.md); this run also covers k = 25.

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 1 <= k <= 25, 0 <= n <= 10^494, any m >= n + k
mode: all, parallel jobs: 3
step 1 object files: 19 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: search COMPLETE with 2 candidates, 0 exact-equal; 0 missing ratios; both margin checkers 'TOTAL pairs=63041 failures=0 undecided=0'; deep_rig k = 3..25 product_solutions=0, 1174616 window candidates: ok
python: 3.13.16 gmpy2 2.3.2 mpmath 1.3.0 numpy 2.5.4
step 3 tools: ok
  search677b 1100000 4242: exit 0, 5 s, '# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=5s'; equal to object/out/search_N1.1e6.txt (times stripped)
  verify_cands.py: 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0'; equal to object/out/verify_N1.1e6.txt (times stripped)
  exact judge check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680: lcms differ, not a counterexample
  exact judge check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040: lcms differ, not a counterexample
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns (all): deep_24-24 deep_19-22 rigx deep_25-25 deep_23-23 deep_3-18 rigm taskA
  finished deep_19-22 (object/deep_rig.py 19 22 1040 0.001 1000000): exit 0, 2855 s
  finished rigx (object/rig_margin_exact.py 3 25 1000000 1 1000): exit 0, 3448 s
  finished deep_24-24 (object/deep_rig.py 24 24 1040 0.001 1000000): exit 0, 3603 s
  finished deep_3-18 (object/deep_rig.py 3 18 1040 0.001 1000000): exit 0, 483 s
  finished rigm (object/rig_margin.py 3 25 1000000 1 1000): exit 0, 159 s
  finished taskA (object/taskA_ratio_audit.py 3000): exit 0, 4 s
  finished deep_25-25 (object/deep_rig.py 25 25 1040 0.001 1000000): exit 0, 1981 s
  finished deep_23-23 (object/deep_rig.py 23 23 1040 0.001 1000000): exit 0, 1725 s
  taskA_ratio_audit.py 3000: 'TOTAL missing over k=3..25: 0', total 970; r outside sets: 0; byte-identical to object/out/taskA_ratio_audit_NB3000.txt
  rig_margin.py 3 25 1000000 1 1000: 'TOTAL pairs=63041 failures=0 undecided=0'; equal to object/out/rig_margin_k3-25_X1e6_eta1e-3.txt (time_s stripped)
  rig_margin_exact.py 3 25 1000000 1 1000: 'TOTAL pairs=63041 failures=0 undecided=0'; equal to object/out/rig_margin_exact_k3-25_X1e6_eta1e-3.txt (time_s stripped)
  k=24: admissible_r=9841 enumerated_pairs(q(q rho-p)<U)=822422 window_candidates=202516 product_solutions=0: equal to the saved line
  deep_rig.py 24 24: 'TOTAL window candidates=202516 product solutions=0 (X0=1000000, QMAX=10^495)'; whole output equal to object/out/deep_rig_final_k24-24_d1040.txt (times stripped)
  k=19: admissible_r=5467 enumerated_pairs(q(q rho-p)<U)=79038 window_candidates=77951 product_solutions=0: equal to the saved line
  k=20: admissible_r=3037 enumerated_pairs(q(q rho-p)<U)=191057 window_candidates=46823 product_solutions=0: equal to the saved line
  k=21: admissible_r=3280 enumerated_pairs(q(q rho-p)<U)=53594 window_candidates=52854 product_solutions=0: equal to the saved line
  k=22: admissible_r=4252 enumerated_pairs(q(q rho-p)<U)=286131 window_candidates=70683 product_solutions=0: equal to the saved line
  deep_rig.py 19 22: 'TOTAL window candidates=248311 product solutions=0 (X0=1000000, QMAX=10^495)'; whole output equal to object/out/deep_rig_final_k19-22_d1040.txt (times stripped)
  k=25: admissible_r=16402 enumerated_pairs(q(q rho-p)<U)=372097 window_candidates=367031 product_solutions=0: equal to the saved line
  deep_rig.py 25 25: 'TOTAL window candidates=367031 product solutions=0 (X0=1000000, QMAX=10^495)'; whole output equal to object/out/deep_rig_final_k25-25_d1040.txt (times stripped)
  k=23: admissible_r=16402 enumerated_pairs(q(q rho-p)<U)=318320 window_candidates=314109 product_solutions=0: equal to the saved line
  deep_rig.py 23 23: 'TOTAL window candidates=314109 product solutions=0 (X0=1000000, QMAX=10^495)'; whole output equal to object/out/deep_rig_final_k23-23_d1040.txt (times stripped)
  k=3: admissible_r=1 enumerated_pairs(q(q rho-p)<U)=0 window_candidates=0 product_solutions=0: equal to the saved line
  k=4: admissible_r=1 enumerated_pairs(q(q rho-p)<U)=4 window_candidates=2 product_solutions=0: equal to the saved line
  k=5: admissible_r=7 enumerated_pairs(q(q rho-p)<U)=13 window_candidates=13 product_solutions=0: equal to the saved line
  k=6: admissible_r=4 enumerated_pairs(q(q rho-p)<U)=25 window_candidates=8 product_solutions=0: equal to the saved line
  k=7: admissible_r=22 enumerated_pairs(q(q rho-p)<U)=43 window_candidates=43 product_solutions=0: equal to the saved line
  k=8: admissible_r=13 enumerated_pairs(q(q rho-p)<U)=149 window_candidates=39 product_solutions=0: equal to the saved line
  k=9: admissible_r=31 enumerated_pairs(q(q rho-p)<U)=108 window_candidates=107 product_solutions=0: equal to the saved line
  k=10: admissible_r=37 enumerated_pairs(q(q rho-p)<U)=551 window_candidates=137 product_solutions=0: equal to the saved line
  k=11: admissible_r=157 enumerated_pairs(q(q rho-p)<U)=799 window_candidates=780 product_solutions=0: equal to the saved line
  k=12: admissible_r=121 enumerated_pairs(q(q rho-p)<U)=2745 window_candidates=678 product_solutions=0: equal to the saved line
  k=13: admissible_r=472 enumerated_pairs(q(q rho-p)<U)=3388 window_candidates=3343 product_solutions=0: equal to the saved line
  k=14: admissible_r=337 enumerated_pairs(q(q rho-p)<U)=10984 window_candidates=2734 product_solutions=0: equal to the saved line
  k=15: admissible_r=283 enumerated_pairs(q(q rho-p)<U)=2418 window_candidates=2365 product_solutions=0: equal to the saved line
  k=16: admissible_r=202 enumerated_pairs(q(q rho-p)<U)=7884 window_candidates=1884 product_solutions=0: equal to the saved line
  k=17: admissible_r=1822 enumerated_pairs(q(q rho-p)<U)=20404 window_candidates=20134 product_solutions=0: equal to the saved line
  k=18: admissible_r=850 enumerated_pairs(q(q rho-p)<U)=42369 window_candidates=10382 product_solutions=0: equal to the saved line
  deep_rig.py 3 18: 'TOTAL window candidates=42649 product solutions=0 (X0=1000000, QMAX=10^495)'; whole output equal to object/out/deep_rig_final_k3-18_d1040.txt (times stripped)
step 5 reruns: ratio audit, both margin checkers and the enumeration for every k = 3..25 equal the saved outputs: ok
total time: 5179 s
PASS
```
