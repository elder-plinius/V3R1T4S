# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon @ 2.10GHz), 15 GB of memory, Python 3.13.16,
with other jobs running on the machine at the same time. Every run was started from the package folder (or from a
copy of it) as `nice -n 10 sh verify-it-yourself/run_checks.sh`; the script runs the recomputation itself at
`nice -n 10` as well. Start and end times from `date -u`, wall time from `date +%s`.

## 1. The package as shipped (exit 0, 142 s, 2026-10-24T08:56:12Z to 2026-10-24T08:58:34Z)

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 0 <= n <= 5871 k
python3: 3.13.16
  a6c79becb3858a3d64648aa138040aa7f8411f1c98af00787e85c5b8f2312210  object/PROOF.md
  b83f0f45f0324da37bbe56575555560cdc7317fc04df92253a74c80a9a291824  object/range_nCk.py
  84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14  object/out/range_nCk_C5871.txt
step 1 object files: sha256 equal to the claim's record: ok
step 2 saved output: counterexamples found (n, m, k): [], last line 'RESULT: no counterexample with n <= 5871 k': ok
  fresh run of object/range_nCk.py 5871: exit 0, 142 s, sha256 84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14
step 3 recomputation: byte-identical to object/out/range_nCk_C5871.txt, last line 'RESULT: no counterexample with n <= 5871 k': ok
  near-miss check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680, lcms differ: rejected as expected
  near-miss check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040, lcms differ: rejected as expected
  positive control check677.py 4 13 3 --allow-different-length 2: M(4,3) = 210, M(13,2) = 210: accepted as expected
step 4 exact judge: ok
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s, 2026-10-24T08:58:43Z)

In a copy of the package, the middle ASCII digit of the first text file in object/ was changed, the same corruption
repo/kit/check_run.py applies to a copy of the package. The first file is object/PROOF.md; the change (from the
script that applied it):

```
object/PROOF.md line 84: digit 2 -> 1; sha256 fa2469eb09742751266f44708668d3b09e62b0b13dbfdc2fe9bc7b33048b80b7
context before: - (b) m + k ≤ 2.8260·5872·k (S1 with N ≤ 5872·k).
context after:  - (b) m + k ≤ 1.8260·5872·k (S1 with N ≤ 5872·k).
```

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 0 <= n <= 5871 k
python3: 3.13.16
problem: object/PROOF.md has sha256 fa2469eb09742751266f44708668d3b09e62b0b13dbfdc2fe9bc7b33048b80b7, the claim records a6c79becb3858a3d64648aa138040aa7f8411f1c98af00787e85c5b8f2312210 (the file is not the one the panel read)
FAIL
```

## 3. Control: one digit of the saved output changed and its recorded hash forged too (exit 1, 162 s, 2026-10-24T08:58:43Z to 2026-10-24T09:01:25Z)

In another copy, the middle ASCII digit of object/out/range_nCk_C5871.txt was changed, and the value SHA_OUT in that
copy's run_checks.sh was replaced by the sha256 of the changed file, so that step 1 passes. Only the recomputation can
catch this one, and it does: the fresh output is byte-identical to the original file, not to the changed one.

```
object/out/range_nCk_C5871.txt line 4: digit 0 -> 1; sha256 23b0e727200645b3c47f8a81989fe3f315a696cf9e67a042d874559a9322f46d
context before: max gap G (primes <= 2010960) = 148 -> k <= 147 -> m < min(c(C+1)(G-1), 2010760) = 2010760
context after:  max gap G (primes <= 2010961) = 148 -> k <= 147 -> m < min(c(C+1)(G-1), 2010760) = 2010760
SHA_OUT=23b0e727200645b3c47f8a81989fe3f315a696cf9e67a042d874559a9322f46d
```

```
package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 0 <= n <= 5871 k
python3: 3.13.16
  a6c79becb3858a3d64648aa138040aa7f8411f1c98af00787e85c5b8f2312210  object/PROOF.md
  b83f0f45f0324da37bbe56575555560cdc7317fc04df92253a74c80a9a291824  object/range_nCk.py
  23b0e727200645b3c47f8a81989fe3f315a696cf9e67a042d874559a9322f46d  object/out/range_nCk_C5871.txt
step 1 object files: sha256 equal to the claim's record: ok
step 2 saved output: counterexamples found (n, m, k): [], last line 'RESULT: no counterexample with n <= 5871 k': ok
  fresh run of object/range_nCk.py 5871: exit 0, 162 s, sha256 84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14
- object/out/range_nCk_C5871.txt differ: char 208, line 4
problem: the fresh output differs from object/out/range_nCk_C5871.txt
FAIL
```
