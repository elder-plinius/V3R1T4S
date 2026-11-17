# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon @ 2.10GHz), 15 GB of memory, Python 3.13.16
with gmpy2 2.3.2, mpmath 1.3.0 and numpy 2.5.4 (`PY` pointed at a virtual environment holding them), gcc 13.3.0 as
`cc`. Every run was started from a copy of the package's object/ and verify-it-yourself/ folders (the only folders the
script reads) as `PY=<a Python with the three modules> PIDLOG=<file> nice -n 10 sh verify-it-yourself/run_checks.sh`
with the default `JOBS=4`. Start and end times from `date -u`, wall time from `date +%s`. The sha256 of the
run_checks.sh used for sections 1 and 2 is the one listed in `SHA256SUMS`; section 3 used a copy with one forged line.

## 1. Default mode, the package as shipped (exit 0, 531 s, 2026-11-07T11:06:32Z to 2026-11-07T11:15:23Z)

The panel's REPRODUCE jobs finished at 11:06 UTC; otherwise no other heavy job ran during this run.

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 26 <= k <= 28, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 4
step 1 object files: 23 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: search COMPLETE with 2 candidates, 0 exact-equal; 0 missing ratios for k = 26..28; both margin checkers 0 failures (58926 pairs); 4 shards, ratio counts 21262 + 16402 + 21262, product_solutions=0 everywhere, 1455391 window candidates: ok
python: 3.13.16 gmpy2 2.3.2 mpmath 1.3.0 numpy 2.5.4
step 3 tools: ok
  search677b 1100000 20261106: exit 0, 5 s, '# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=5s'; equal to object/out/search_N1.1e6.txt (times stripped)
  verify_cands.py: 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0'; equal to object/out/verify_N1.1e6.txt (times stripped)
  exact judge check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680: lcms differ, not a counterexample
  exact judge check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040: lcms differ, not a counterexample
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns (default): s27_0 rigm taskA
  finished taskA (object/taskA_ratio_audit_k.py 400 26 28): exit 0, 4 s
  finished rigm (object/rig_margin.py 26 28 1000000 1 1000): exit 0, 177 s
  finished s27_0 (object/shard_rig.py 27 27 1040 0.001 1000000): exit 0, 526 s
  taskA_ratio_audit_k.py 400 26 28: 'TOTAL missing over k=26..28: 0'; byte-identical to object/out/taskA_ratio_audit_k26-28.txt
  rig_margin.py 26 28 1000000 1 1000: 'TOTAL pairs=58926 failures=0 undecided=0'; equal to object/out/rig_margin_k26-28.txt (time_s stripped)
  shard 0 of 4, k=27: admissible_r=4101 enumerated_pairs(q(q rho-p)<U)=104170 window_candidates=102823 product_solutions=0: equal to the saved line
step 5 reruns: ratio audit, interval margin checker and the enumeration of k = 27 (shard 0 of 4) equal the saved outputs: ok
  (not rerun by default: the other shards and k values, and rig_margin_exact.py; use --all)
total time: 531 s
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s, 2026-11-07T09:39:28Z)

In a copy of the package, the middle ASCII digit of the first text file in object/ was changed, the same corruption
repo/kit/check_run.py applies to a copy of the package. The first file is object/PROOF.md; the change (from the
script that applied it):

```
object/PROOF.md line 63: digit 0 -> 1; sha256 09867be43b0578cd1c0ee006d2f07bde3f5188e410a19d13c0ef891467fd6a4b
context before: This covers every (n, k) with X := n + (k+1)/2 < 10^6 and k ≤ K*, because then n + k < 10^6 + (k−1)/2 ≤ 1.1·10^6.
context after:  This covers every (n, k) with X := n + (k+1)/2 < 11^6 and k ≤ K*, because then n + k < 10^6 + (k−1)/2 ≤ 1.1·10^6.
```

This run was made while the panel's REPRODUCE jobs were running; it stops at step 1, so their load does not matter.

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 26 <= k <= 28, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 4
problem: object/PROOF.md has sha256 09867be43b0578cd1c0ee006d2f07bde3f5188e410a19d13c0ef891467fd6a4b, the package records b461c7024f94a9487ab922b5558e017fcc747c56ce123b07d5083862307a2f81 (the file is not the one the panel read)
FAIL
```

## 3. Control: one count in a saved enumeration output changed and its recorded hash forged too (exit 1, 533 s from start to end time, 2026-11-07T11:15:45Z to 2026-11-07T11:24:38Z)

In another copy, the k = 27 `enumerated_pairs` count in object/out/deep_rig_shard0.txt was raised by one, and that
file's line in the copy's run_checks.sh (`SUMS`) was given the sha256 of the changed file, so that steps 1 and 2 pass
(step 2 sums only the admissible_r and window_candidates fields). Only the recomputation can catch this one, and it
does: the fresh enumeration of k = 27 on shard 0 gives 104170, as the original file does.

```
object/out/deep_rig_shard0.txt line 3: enumerated_pairs 104170 -> 104171 (k = 27); sha256 483fe91dd25377f41ac6c561971098c803d87446494964013e61a168df254737
context before: k=27 admissible_r=4101 enumerated_pairs(q(q rho-p)<U)=104170 window_candidates=102823 product_solutions=0 t=3581s
context after:  k=27 admissible_r=4101 enumerated_pairs(q(q rho-p)<U)=104171 window_candidates=102823 product_solutions=0 t=3581s
run_checks.sh line 34 now records 483fe91dd25377f41ac6c561971098c803d87446494964013e61a168df254737 for object/out/deep_rig_shard0.txt
```

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 26 <= k <= 28, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 4
step 1 object files: 23 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: search COMPLETE with 2 candidates, 0 exact-equal; 0 missing ratios for k = 26..28; both margin checkers 0 failures (58926 pairs); 4 shards, ratio counts 21262 + 16402 + 21262, product_solutions=0 everywhere, 1455391 window candidates: ok
python: 3.13.16 gmpy2 2.3.2 mpmath 1.3.0 numpy 2.5.4
step 3 tools: ok
  search677b 1100000 20261106: exit 0, 5 s, '# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=5s'; equal to object/out/search_N1.1e6.txt (times stripped)
  verify_cands.py: 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0'; equal to object/out/verify_N1.1e6.txt (times stripped)
  exact judge check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680: lcms differ, not a counterexample
  exact judge check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040: lcms differ, not a counterexample
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns (default): s27_0 rigm taskA
  finished taskA (object/taskA_ratio_audit_k.py 400 26 28): exit 0, 4 s
  finished rigm (object/rig_margin.py 26 28 1000000 1 1000): exit 0, 172 s
  finished s27_0 (object/shard_rig.py 27 27 1040 0.001 1000000): exit 0, 528 s
  taskA_ratio_audit_k.py 400 26 28: 'TOTAL missing over k=26..28: 0'; byte-identical to object/out/taskA_ratio_audit_k26-28.txt
  rig_margin.py 26 28 1000000 1 1000: 'TOTAL pairs=58926 failures=0 undecided=0'; equal to object/out/rig_margin_k26-28.txt (time_s stripped)
problem: shard 0, k=27: 'k=27 admissible_r=4101 enumerated_pairs(q(q rho-p)<U)=104170 window_candidates=102823 product_solutions=0' differs from the saved line 'k=27 admissible_r=4101 enumerated_pairs(q(q rho-p)<U)=104171 window_candidates=102823 product_solutions=0'
FAIL
```

## 4. Mode --all

Not run by the contributor with this script: the machine's 4 cores were held by the panel's REPRODUCE skeptic, which
ran the same commands that --all runs (all four shards for k = 26..28, and rig_margin_exact.py for each k) from a copy
of object/ between 09:20 and 11:06 UTC on 2026-11-07, and found every output equal to the saved one apart from the
time fields (`panel/reproduce.md`, "Computed steps rerun in full"). The four shards took 6282–6327 s each there,
with the three exact-margin jobs (2250–2862 s) running alongside.
