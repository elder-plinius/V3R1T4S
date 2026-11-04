# Receipts: real output of sh verify-it-yourself/run_checks.sh

started: Sun Nov  1 04:21:40 UTC 2026, finished Sun Nov  1 04:24:45 UTC 2026 (3 min 5 s wall, 16 threads for the slice, idle machine). The first line block is the script header echoed by the shell session. Lines longer than 400 characters are cut.

```
[04:21:40] step 1: sha256 of every file in object/
object/: 75 files, all sha256 match
[04:21:41] step 2: fetch the pinned public inputs and check their sha256
fetched and verified cert_B_08344.bin (81296166 bytes) and certB_test.bin from commit da956b11
[04:21:44] step 3: build the verifier
[04:21:50] step 4: Iv containment test (random operations against exact Fractions / mpmath.iv)
records checked: {'add': 20000, 'sub': 20000, 'mul': 20000, 'div0': 4147, 'sqr': 20000, 'sqrt': 20000, 'sin10': 20000, 'cos10': 20000, 'sin7': 20000, 'div': 15853, 'const:pi': 1, 'const:R5': 1, 'const:V3x0_0': 1, 'const:V3x0_1': 1, 'const:V5x0_1': 1, 'const:V5x0_2': 1, 'const:V5x0_3': 1, 'const:V5y0_2': 1, 'const:V5y0_3': 1, 'const:V5x0_4': 1, 'const:twopi5': 1, 'const:e11': 1, 'const:e12': 1}
violations: 0
max extra width over exact image (per op): {'add': 7.105427357601002e-14, 'sub': 4.529709940470639e-14, 'mul': 1.8688920727562166e-12, 'sqr': 4.5029801785375635e-12, 'sin10': 1.6653345369377348e-15, 'cos10': 1.4432899320127035e-15, 'sin7': 7.771561172376096e-16, 'div': 57267.54885823551, 'const:pi': 4.440892098500626e-16, 'const:R5': 1.1102230246251565e-16, 'const:V3x0_0': 1.1102230246251565e-16, 
[04:22:07] step 5: negative controls (valid author control must verify; header, bit-stream and threshold tampers must be refused)
seed 61 size 15410
bad_magic                exit=1 as expected
certB_test               exit=0 as expected
flip_first_bit           exit=1 as expected
flip_mid_bit             exit=1 as expected
inflate_negative         exit=1 as expected
inflate_zero             exit=1 as expected
real_job3431_tau83442    exit=1 as expected
real_job3431_unpatched   exit=0 as expected
tmax_0.60                exit=1 as expected
tmax_0.65                exit=1 as expected
trailing_byte            exit=1 as expected
truncated_block          exit=1 as expected
truncated_file           exit=1 as expected
controls: 13 run, unexpected []
[04:23:54] step 6: deterministic 1% slice of the real certificate on 16 threads (interval mode)
  jobs covered 43 of 3,596  (PARTIAL SLICE)
  failing leaves 0  (angular-order-certificate failures 0)
  interval child-covers-parent checks at every split (incl. seed splits and pre-walk): failures 0  => OK
RESULT: SLICE OK (not a full verification)
PASS
```
