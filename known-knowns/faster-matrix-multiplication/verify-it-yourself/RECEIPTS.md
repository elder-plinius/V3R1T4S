# Current wrapper receipt (2026-10-15)

Real end-to-end run on Linux x86_64, Python 3.12.14, NumPy 2.3.5.
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`; exit code **0**.
Release inputs and checker sources were fetched from upstream commit
`371938deefd77b9e6a95d2a0c3e2d3c6ead7eaac` and verified against its Git blob IDs.
These are actual scientific checker outputs, not synthetic fixture output.

All seven shipped schemes and all three semantic negative controls ran.

Command (from this family directory, with the stated Python environment):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 sh verify-it-yourself/run_checks.sh
```

Exact source and output SHA-256:

- `run_checks.sh`: `361c216d4d66abc43f185be7711f41683a4a8723f8af7e61f85d00b9d3e139ba`
- `known-knowns/check_harness_contract.py`: `f0f43ba4ab6970001f228affb5a95f9ec5d37b115f8487c7ce4cc11ce9e5a070`
- Raw combined stdout/stderr below: `0d9cd10d3f6abe9d5cfeec4e505bb71591f47134ae2a3e153ef646d2bbaf53f3`

## Complete current output

```text
== 13x14x14_r1558_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 182*196*182 = 6492304 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 36.8
FMMCHECK PASS file=13x14x14_r1558_Q.json format=<13,14,14> sorted=<13,14,14> terms=1558 rank_nonzero_terms=1558 sha256=15e46337bdca5a92090021dbd11a6fcb9d57f352a396ea6b34e1f32888fe0702
rank 1558 as claimed
== 13x14x15_r1677_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 182*210*195 = 7452900 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 33.7
FMMCHECK PASS file=13x14x15_r1677_Q.json format=<13,14,15> sorted=<13,14,15> terms=1677 rank_nonzero_terms=1677 sha256=4230f61d432b627d0624105deb004451e8332ccca32c1834746cff2e11c7d6bc
rank 1677 as claimed
== 14x14x15_r1716_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 196*210*210 = 8643600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 33.7
FMMCHECK PASS file=14x14x15_r1716_Q.json format=<14,14,15> sorted=<14,14,15> terms=1716 rank_nonzero_terms=1716 sha256=83e880a0ecbab4bc6af7c0105365e9ee69aac2c2dc0ac272073249e856f34a56
rank 1716 as claimed
== 14x15x15_r1842_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 210*225*210 = 9922500 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 32.9
FMMCHECK PASS file=14x15x15_r1842_Q.json format=<14,15,15> sorted=<14,15,15> terms=1842 rank_nonzero_terms=1842 sha256=bb313b876ef9a14b57e72f4deafdae9085bcdad1d1f43d70067788f7e375c6b5
rank 1842 as claimed
== 14x15x15_r1843_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 210*225*210 = 9922500 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 32.9
FMMCHECK PASS file=14x15x15_r1843_Q.json format=<14,15,15> sorted=<14,15,15> terms=1843 rank_nonzero_terms=1843 sha256=c86dba238db8a26bef6a4e8f5e224e8524e5d61cd0b89625fe34b43e27813ac3
rank 1843 as claimed
== 15x16x16_r2180_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 240*256*240 = 14745600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 39.4
FMMCHECK PASS file=15x16x16_r2180_Q.json format=<15,16,16> sorted=<15,16,16> terms=2180 rank_nonzero_terms=2180 sha256=8365355f0f3ae6bc3efd445517fbd473c91477cd1c2b2aeb08c0b3b85182fd1d
rank 2180 as claimed
== 15x16x16_r2196_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 240*256*240 = 14745600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 39.5
FMMCHECK PASS file=15x16x16_r2196_Q.json format=<15,16,16> sorted=<15,16,16> terms=2196 rank_nonzero_terms=2196 sha256=11c2649664a1d8d4386b225bb0ba62f3a5f1c819b575f50ce9830c478fb67113
rank 2196 as claimed
== negative controls on the smallest scheme (each must FAIL)
HARNESS CONTROL PASS fmm: expected semantic rejection
control drop_term: expected semantic rejection
HARNESS CONTROL PASS fmm: expected semantic rejection
control bump_coeff: expected semantic rejection
HARNESS CONTROL PASS fmm: expected semantic rejection
control swap_vw: expected semantic rejection
ALL CHECKS PASSED
```

---

## Historical receipts

The records below are preserved from earlier runs of the former wrapper. Their
wrapper messages do not describe the current run; use the complete current
output above for the current wrapper contract. Historical comparison dates and
optional-runtime coverage remain those stated in the original records.

# Check results (fast matrix multiplication)

## 2026-10-12: the two new records

`python3 verify-it-yourself/fmmcheck.py` was run on the two new files from 2026-10-12T18:07:55Z to 18:08:33Z on the build
machine (macOS, python3 3.9.6, numpy 2.0.2). Both exit 0; both sha256 equal `INDEX.csv`.

| scheme | Brent equations checked | primes (p < 2^20) | log2 ∏p | log2 2L(S+1) | violations | rank (nonzero terms) | sha256 = INDEX.csv | verdict |
|---|---|---|---|---|---|---|---|---|
| <14,15,15> `14x15x15_r1842_Q.json` | 9 922 500 | 4 | 80.0 | 32.9 | 0 | 1842 | yes | PASS |
| <15,16,16> `15x16x16_r2180_Q.json` | 14 745 600 | 4 | 80.0 | 39.4 | 0 | 2180 | yes | PASS |

Comparison with the criterion sources as re-checked on 2026-10-12 (`the-record-we-beat/live_recheck_2026-10-12.json`):
1842 is 6 below the minimum 1848 for <14,15,15>, and 2180 is 43 below the minimum 2223 for <15,16,16>. The earlier
files `14x15x15_r1843_Q.json` and `15x16x16_r2196_Q.json` stay in `schemes/` (they are the parents of the new
schemes, and 1843 is also the parent of the <14,14,15>:1716); their release-time check is below. `run_checks.sh` now
checks all seven files.

Before release each new scheme was also checked by three separate reviewers with their own code (exact float64 or
int64 on the integer-scaled tensor, CRT over other primes, exact Fraction evaluation on random matrices), and its
derivation from the parent was certified in exact arithmetic (see `../HOW_WE_FOUND_IT.md`).

```
2026-10-12T18:07:55Z
Python 3.9.6
numpy 2.0.2
== schemes/14x15x15_r1842_Q.json
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 210*225*210 = 9922500 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 32.9
FMMCHECK PASS file=14x15x15_r1842_Q.json format=<14,15,15> sorted=<14,15,15> terms=1842 rank_nonzero_terms=1842 sha256=bb313b876ef9a14b57e72f4deafdae9085bcdad1d1f43d70067788f7e375c6b5
real 11.11
user 10.38
sys 0.15
exit 0
== schemes/15x16x16_r2180_Q.json
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 240*256*240 = 14745600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 39.4
FMMCHECK PASS file=15x16x16_r2180_Q.json format=<15,16,16> sorted=<15,16,16> terms=2180 rank_nonzero_terms=2180 sha256=8365355f0f3ae6bc3efd445517fbd473c91477cd1c2b2aeb08c0b3b85182fd1d
real 27.19
user 25.83
sys 0.33
exit 0
2026-10-12T18:08:33Z
```

## 2026-10-10: release-time run (five schemes)

`sh verify-it-yourself/run_checks.sh` was run on the shipped files from 2026-10-10T19:30:51Z to 19:37:03Z on the build machine
(macOS, python3 3.9, numpy 2.0.2, load average about 80–100 from other jobs). Exit code 0, last line
`ALL CHECKS PASSED`.

| scheme | Brent equations checked | primes (p < 2^20) | log2 ∏p | log2 2L(S+1) | violations | rank (nonzero terms) | sha256 = INDEX.csv | verdict |
|---|---|---|---|---|---|---|---|---|
| <14,15,15> `14x15x15_r1843_Q.json` | 9 922 500 | 4 | 80.0 | 32.9 | 0 | 1843 | yes | PASS |
| <13,14,14> `13x14x14_r1558_Q.json` | 6 492 304 | 4 | 80.0 | 36.8 | 0 | 1558 | yes | PASS |
| <15,16,16> `15x16x16_r2196_Q.json` | 14 745 600 | 4 | 80.0 | 39.5 | 0 | 2196 | yes | PASS |
| <14,14,15> `14x14x15_r1716_Q.json` | 8 643 600 | 4 | 80.0 | 33.7 | 0 | 1716 | yes | PASS |
| <13,14,15> `13x14x15_r1677_Q.json` | 7 452 900 | 4 | 80.0 | 33.7 | 0 | 1677 | yes | PASS |

Because ∏p exceeds 2·L·(S+1) in every case, "0 violations modulo every prime" implies every Brent equation holds
exactly over Q (see the docstring of `verify-it-yourself/fmmcheck.py`). Negative controls (`verify-it-yourself/mutate.py` on the <13,14,15>
scheme): a dropped term, a coefficient increased by 1, and two swapped v-factors are each reported
`FMMCHECK FAIL`.

Comparison with the criterion sources (2026-10-10T19:25:52Z, `the-record-we-beat/sources_2026-10-10T19-25-52Z.json`): every rank
is strictly below the minimum of the four sources (bars 1848, 1582, 2223, 1789, 1681; margins −5, −24, −27, −73, −4).

Earlier independent checks (not shipped): the author's exact big-integer checker (clears denominators, no modular
arithmetic), an independent reviewer's checker in exact Fraction mode and in CRT-bounded modular mode, and a final
pre-release modular Brent check over 4 primes, all with 0 violations and the same ranks.

## Raw output

```
2026-10-10T19:30:51Z
== 13x14x14_r1558_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 182*196*182 = 6492304 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 36.8
FMMCHECK PASS file=13x14x14_r1558_Q.json format=<13,14,14> sorted=<13,14,14> terms=1558 rank_nonzero_terms=1558 sha256=15e46337bdca5a92090021dbd11a6fcb9d57f352a396ea6b34e1f32888fe0702
rank 1558 as claimed
== 13x14x15_r1677_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 182*210*195 = 7452900 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 33.7
FMMCHECK PASS file=13x14x15_r1677_Q.json format=<13,14,15> sorted=<13,14,15> terms=1677 rank_nonzero_terms=1677 sha256=4230f61d432b627d0624105deb004451e8332ccca32c1834746cff2e11c7d6bc
rank 1677 as claimed
== 14x14x15_r1716_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 196*210*210 = 8643600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 33.7
FMMCHECK PASS file=14x14x15_r1716_Q.json format=<14,14,15> sorted=<14,14,15> terms=1716 rank_nonzero_terms=1716 sha256=83e880a0ecbab4bc6af7c0105365e9ee69aac2c2dc0ac272073249e856f34a56
rank 1716 as claimed
== 14x15x15_r1843_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 210*225*210 = 9922500 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 32.9
FMMCHECK PASS file=14x15x15_r1843_Q.json format=<14,15,15> sorted=<14,15,15> terms=1843 rank_nonzero_terms=1843 sha256=c86dba238db8a26bef6a4e8f5e224e8524e5d61cd0b89625fe34b43e27813ac3
rank 1843 as claimed
== 15x16x16_r2196_Q.json
sha256 matches INDEX.csv
  mod 1048573: violated Brent equations = 0
  mod 1048571: violated Brent equations = 0
  mod 1048559: violated Brent equations = 0
  mod 1048549: violated Brent equations = 0
  checked 240*256*240 = 14745600 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 39.5
FMMCHECK PASS file=15x16x16_r2196_Q.json format=<15,16,16> sorted=<15,16,16> terms=2196 rank_nonzero_terms=2196 sha256=11c2649664a1d8d4386b225bb0ba62f3a5f1c819b575f50ce9830c478fb67113
rank 2196 as claimed
== negative controls on the smallest scheme (each must FAIL)
control drop_term: FMMCHECK FAIL file=drop_term.json format... (expected)
control bump_coeff: FMMCHECK FAIL file=bump_coeff.json forma... (expected)
control swap_vw: FMMCHECK FAIL file=swap_vw.json format=<... (expected)
ALL CHECKS PASSED
sh verify-it-yourself/run_checks.sh  90.84s user 1.47s system 24% cpu 6:12.03 total
2026-10-10T19:37:03Z
```
