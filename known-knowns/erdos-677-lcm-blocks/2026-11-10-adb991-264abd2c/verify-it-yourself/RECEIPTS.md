# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores, 15 GB of memory, Python 3.13.16 with gmpy2 2.3.2,
mpmath 1.3.0 and numpy 2.5.4 (`PY` pointed at a virtual environment holding them), gcc 13.3.0 as `cc`. Every run was
started from a copy of the package's object/ and verify-it-yourself/ folders (the only folders the script reads) as
`PY=<a Python with the three modules> sh verify-it-yourself/run_checks.sh` (sections 1 and 3 under `nice -n 10`),
with the default `JOBS=4`. Start and end times from `date -u`. Sections 1 and 3 ran at the same time.

## 1. Default mode, the package as shipped (exit 0, 342 s, 2026-11-10T11:11:54Z to 2026-11-10T11:17:36Z)

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with k = 29, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 4
step 1 object files: 29 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: search COMPLETE with 2 candidates, k=29 cand=0, 0 exact-equal; 114817 ratios, 0 missing; interval margin and 4 exact-margin shards 0 failures (114817 pairs); 4 enumeration shards, ratio counts add up to 114817, product_solutions=0 everywhere, 3288852 window candidates: ok
python: 3.13.16 gmpy2 2.3.2 mpmath 1.3.0 numpy 2.5.4
step 3 tools: ok
  search677b 1100000 20261109: exit 0, 4 s, '# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=3s'; equal to object/out/search_N1.1e6.txt (times stripped)
  verify_cands.py: 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0'; equal to object/out/verify_N1.1e6.txt (times stripped)
  exact judge check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680: lcms differ, not a counterexample
  exact judge check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040: lcms differ, not a counterexample
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns (default): rigm taskA
  finished taskA (object/taskA_ratio_audit_k.py 400 29 29): exit 0, 18 s
  finished rigm (object/rig_margin.py 29 29 1000000 1 1000): exit 0, 337 s
  taskA_ratio_audit_k.py 400 29 29: 'TOTAL missing over k=29..29: 0'; byte-identical to object/out/taskA_ratio_audit_k29.txt
  rig_margin.py 29 29 1000000 1 1000: 'TOTAL pairs=114817 failures=0 undecided=0'; equal to object/out/rig_margin_k29.txt (time_s stripped)
step 5 reruns: ratio audit and interval margin checker (whole ratio list) equal the saved outputs: ok
  (not rerun by default: the exact-margin shards and the enumeration, about 2.5 h on 4 cores; use --all)
total time: 342 s
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s, 2026-11-10T11:12:25Z)

In a copy of the package, the middle ASCII digit of the first text file in object/ was changed, the same corruption
repo/kit/check_run.py applies to a copy of the package (from the script that applied it):

```
object/PROOF.md line 86: digit 0 -> 1; sha256 060bc238b52510c085b5b5c2f56870a61a307058e2a74cd7014f0befd9981599
context before: symmetric about 0; e_{k−2} = −s with s = k(k²−1)/24). For a constant C > 0 put Y_C(X) = ρX − C/X and
context after:  symmetric about 1; e_{k−2} = −s with s = k(k²−1)/24). For a constant C > 0 put Y_C(X) = ρX − C/X and
```

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with k = 29, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 4
problem: object/PROOF.md has sha256 060bc238b52510c085b5b5c2f56870a61a307058e2a74cd7014f0befd9981599, the package records 264abd2c67286ea32fdde54b1b01e2a956b4ac9891ee229f22665e0dec71e132 (the file is not the one the panel read)
FAIL
```

## 3. Control: one value of a saved output changed and its recorded hash forged too (exit 1, 340 s, 2026-11-10T11:12:25Z to 2026-11-10T11:18:05Z)

In another copy, the worst relative margin in object/out/rig_margin_k29.txt was changed and that file's line in the
copy's run_checks.sh (`SUMS`) was given the sha256 of the changed file, so that steps 1 and 2 pass. Only the
recomputation can catch this one, and it does.

```
object/out/rig_margin_k29.txt line 2: worst_rel_margin_lower_bound 0.99999994 -> 0.99999995; sha256 64bb53a975336b29edfc40e1a05d7262c6e286ace3ed610d00e37b661f289108
run_checks.sh SUMS line for object/out/rig_margin_k29.txt now records 64bb53a975336b29edfc40e1a05d7262c6e286ace3ed610d00e37b661f289108, so steps 1 and 2 pass
```

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with k = 29, 0 <= n <= 10^494, any m >= n + k
mode: default, parallel jobs: 4
step 1 object files: 29 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: search COMPLETE with 2 candidates, k=29 cand=0, 0 exact-equal; 114817 ratios, 0 missing; interval margin and 4 exact-margin shards 0 failures (114817 pairs); 4 enumeration shards, ratio counts add up to 114817, product_solutions=0 everywhere, 3288852 window candidates: ok
python: 3.13.16 gmpy2 2.3.2 mpmath 1.3.0 numpy 2.5.4
step 3 tools: ok
  search677b 1100000 20261109: exit 0, 4 s, '# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=4s'; equal to object/out/search_N1.1e6.txt (times stripped)
  verify_cands.py: 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0'; equal to object/out/verify_N1.1e6.txt (times stripped)
  exact judge check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680: lcms differ, not a counterexample
  exact judge check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040: lcms differ, not a counterexample
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns (default): rigm taskA
  finished taskA (object/taskA_ratio_audit_k.py 400 29 29): exit 0, 20 s
  finished rigm (object/rig_margin.py 29 29 1000000 1 1000): exit 0, 335 s
  taskA_ratio_audit_k.py 400 29 29: 'TOTAL missing over k=29..29: 0'; byte-identical to object/out/taskA_ratio_audit_k29.txt
problem: rig_margin.py 29 29 1000000 1 1000: output differs from object/out/rig_margin_k29.txt (time_s stripped)
FAIL
```

## 4. Mode --all

Not run by the contributor with this script. The panel's REPRODUCE skeptic ran the same commands that --all runs (the
4 enumeration shards and the 4 exact-margin shards, plus the ratio audit and the interval margin) from a copy of
object/ on 2026-11-10 and found every output identical to the saved one apart from times (`panel/reproduce.md`):
about 3950-3980 s per enumeration shard and 2592-2608 s per exact-margin shard on that machine.
