# Run it yourself

All commands run in a fresh shell from this package folder. You need Python 3 (standard library only),
`sha256sum` (or `shasum`), `cmp` and the usual POSIX tools. One core, about 0.2 GB of memory, no network access.

## 1. The check

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (exit status 0). The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`
(142 s on the contributor's machine). The lines that carry the result:

```
step 1 object files: sha256 equal to the claim's record: ok
step 2 saved output: counterexamples found (n, m, k): [], last line 'RESULT: no counterexample with n <= 5871 k': ok
step 3 recomputation: byte-identical to object/out/range_nCk_C5871.txt, last line 'RESULT: no counterexample with n <= 5871 k': ok
  near-miss check677.py 4 13 3 (n m k): M(n,k) = 210, M(m,k) = 1680, lcms differ: rejected as expected
  near-miss check677.py 18 53 4 (n m k): M(n,k) = 87780, M(m,k) = 1580040, lcms differ: rejected as expected
step 4 exact judge: ok
PASS
```

`sh verify-it-yourself/run_checks.sh --help` prints the header.

## 2. What it does

1. Compares the sha256 of `object/PROOF.md`, `object/range_nCk.py` and `object/out/range_nCk_C5871.txt` with the
   values recorded in the claim (`how-we-built-it/claim/CLAIM.md`): the files are the ones the panel read.
2. Checks that the saved output reports `counterexamples found (n, m, k): []` and ends with
   `RESULT: no counterexample with n <= 5871 k`.
3. Reruns `python3 -I object/range_nCk.py 5871` at `nice -n 10` and compares its output byte for byte with the saved
   output (the program is deterministic: a sieve, integer arithmetic and exact big-integer lcm).
4. Runs the exact judge `verify-it-yourself/check677.py` (written from the definition; the same bytes as the claim's
   `checker/check677.py`, sha256 03ecd782d3cfb3437f7b3915b504547b8506a74e39e88bae232e766f94760239) on the two known
   near-misses (n, m, k) = (4, 13, 3) and (18, 53, 4), which must be rejected because their lcms differ, and on
   Erdős's different-length coincidence M(4,3) = M(13,2) = 210, which it must accept.

What the script cannot check: the two cited theorems (Rosser–Schoenfeld 1962, Schoenfeld 1976) and the argument in
`object/PROOF.md` that makes the enumeration complete for every m. Read the proof; the steps S0–S3 are short.

## 3. By hand

```sh
python3 -I object/range_nCk.py 5871 > my_range_nCk_C5871.txt      # a few minutes, one core
cmp my_range_nCk_C5871.txt object/out/range_nCk_C5871.txt && echo IDENTICAL
tail -n 1 my_range_nCk_C5871.txt                                    # RESULT: no counterexample with n <= 5871 k
python3 -I verify-it-yourself/check677.py 4 13 3                    # arguments n m k; last line FAIL (lcms differ)
```

`python3 -I object/range_nCk.py C` works for other constants C as long as 2.8260·(C + 1) < 16597 (the program
asserts this); 5871 is the largest such C. Commands used in the run: `how-we-built-it/COMMANDS.md`.
