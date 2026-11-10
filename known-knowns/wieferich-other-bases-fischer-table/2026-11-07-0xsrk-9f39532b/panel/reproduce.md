role: REPRODUCE
context: claude code Task subagent (fresh context, saw only claim/)

# REPRODUCE: pair (b, p) = (28910, 1011548897263), partial win p1

Verdict: reproduced. The object in claim/object/pair.json has every mathematical property in the p1 definition. I proved
this with my own code, written before I opened claim/verify.py. claim/verify.py agrees with my code on the claim and on six
negative controls. Every run was repeated at least twice and gave byte-identical output. The OEIS clause is outside this
role: the OEIS response is not saved under claim/, so NOVELTY has to re-fetch it.

## Definition (quoted verbatim from claim/claim.md, "criterion for p1")

> New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked
> exactly, and absent from both Fischer tables and OEIS.

A Wieferich pair also needs p to be prime and not to divide b. The full criterion, quoted in the same file, says "a proven
prime p not dividing b". I checked that as well.

## Order of work
1. I read claim/claim.md and claim/object/pair.json, and looked at the head and tail of the four files in claim/inputs/
   to learn their layout.
2. I wrote my own checker, panel/work-reproduce/my_check.py, using the standard library only, and a GMP cross-check,
   panel/work-reproduce/gmp_crosscheck.py. Only after that did I open claim/REPRODUCE.md, claim/verify.py and
   claim/status_sources.md.
3. Runs:
   - my checker 3 times (python3 twice, the workspace venv interpreter once);
   - the GMP cross-check twice;
   - claim/verify.py 3 times;
   - the one-liner from claim/REPRODUCE.md twice;
   - 7 control objects through claim/verify.py, twice.
   I compared all outputs by sha256.

Paths are shown relative to the run folder. The real commands used absolute paths and `2>&1 | tee` into panel/work-reproduce/.

## Results at a glance

| property | my routes (my_check.py, gmp_crosscheck.py) | claim/verify.py | agree |
|---|---|---|---|
| 10125 < b < 65537 | exact integer comparisons | ok | yes |
| b not a perfect power | 28910 = 2 * 5 * 7^2 * 59, exponent gcd 1; exact integer k-th roots for k = 2..15; GMP is_power False | ok | yes |
| p > 1e12 | exact integer comparison, p - 10^12 = 11548897263 | ok | yes |
| p prime | proof 1: trial division by every integer up to isqrt(p) = 1005757. Proof 2: Lucas certificate with a = 3 and p-1 = 2 * 3^2 * 15937 * 3526207, each factor proved prime by trial division. Also deterministic Miller-Rabin below the Jaeschke bound, and GMP is_prime and BPSW | ok | yes |
| p does not divide b | b mod p = 28910, gcd 1 | ok | yes |
| b^(p-1) == 1 mod p^2 | residue 1 from built-in pow, two hand-written exponentiations and GMP powmod; b^((p-1)/2) = +1 mod p^2, with (b/p) = +1 from reciprocity; Fermat-quotient additivity gives a sum of exactly 2p; the residue mod p^3 also reduces to 1 | ok, q_p(b) mod p = 0 | yes |
| absent from both Fischer tables | in the saved copies, whose sha256 match the fetch record: no row for 28910, and p occurs nowhere, neither as a number, nor inside a longer number, nor with separators | not checked by verify.py (REPRODUCE.md asks for a manual search) | n/a |
| absent from OEIS | not checkable from saved files | not checked | out of role (NOVELTY) |

## 1. My checker, run 1, full output
Command: `python3 -B panel/work-reproduce/my_check.py claim 2>&1 | tee panel/work-reproduce/my_check_run1.txt`
```
REPRODUCE independent checker (standard library only)
python 3.14.7
== 0. claim folder inventory: relative path, bytes, sha256 (__pycache__ folders skipped) ==
claim/REPRODUCE.md  958  b2733098d6c79d276d1463ad19275d5eba46c627a59f65b996ab2a510abddc54
claim/claim.md  1774  10f9eaa6bb4cb438d1d3c0e265b2ffa7eb8263b7d236f32c846597820026d9d9
claim/status_sources.md  1805  122a84831265287c4f5ad19d5195ae5ab5e1057312cfb1e5f781f0e31e9ab28a
claim/verify.py  2370  991d0c0f01f695e615c871a283bde85def2a1f0de8758494df25933b184d02e7
claim/inputs/ErstBasen.txt  115771  e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820
claim/inputs/ErstPBasen.txt  81696  3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362
claim/inputs/FermQ_Sorg.txt  288459  35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
claim/inputs/FermQ_Sort.txt  33141  bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
claim/object/pair.json  106  9f39532bfc7ab17685cc172f0e2ff2ca917a21bc1f5a51ba702cddb75e644383
[PASS] present: claim/claim.md
[PASS] present: claim/object/pair.json
[PASS] present: claim/verify.py
[PASS] present: claim/REPRODUCE.md
[PASS] present: claim/status_sources.md
[PASS] present: claim/inputs/FermQ_Sorg.txt
[PASS] present: claim/inputs/FermQ_Sort.txt
== 1. object: claim/object/pair.json ==
raw: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28910, "p": 1011548897263}
[PASS] pair.json has exactly the keys b, p, partial_win, target_id :: ['b', 'p', 'partial_win', 'target_id']
[PASS] b is a JSON integer :: 28910
[PASS] p is a JSON integer :: 1011548897263
[PASS] target_id == wieferich-other-bases-fischer-table :: wieferich-other-bases-fischer-table
[PASS] partial_win == p1 :: p1
b = 28910
p = 1011548897263
== 2. claim/claim.md states the same numbers as the object ==
[PASS] claim.md sentence names p and b :: ('1011548897263', '28910')
[PASS] claim.md congruence is b^(p-1) == 1 (mod p^2) with these b, p :: ('28910', '1011548897262', '1011548897263')
[PASS] claim.md range statement names b :: ('28910',)
[PASS] claim.md partial win is p1 :: ('p1',)
[PASS] claim.md target_id matches the object :: ('wieferich-other-bases-fischer-table',)
== 3. base range: 10125 < b < 65537 ==
[PASS] 10125 < b :: 28910
[PASS] b < 65537 :: 28910
== 4. b is not a perfect power ==
factorisation of b (trial division): 2 * 5 * 7^2 * 59
[PASS] factorisation multiplies back to b
[PASS] every factor of b is prime (trial division)
[PASS] gcd of the exponents == 1, so b is not a perfect power :: gcd = 1
integer k-th roots r = floor(b^(1/k)) for k = 2..15: 2:170, 3:30, 4:13, 5:7, 6:5, 7:4, 8:3, 9:3, 10:2, 11:2, 12:2, 13:2, 14:2, 15:1
[PASS] no k in 2..bit_length(b) has r^k == b (2^bit_length(b) > b, so larger k need r = 1) :: exact k-th powers at k = []
== 5. p above 1e12 ==
[PASS] p > 10**12 (exact integer comparison) :: p - 10**12 = 11548897263
== 6. p is prime ==
[PASS] isqrt(p) is the exact floor square root :: isqrt(p) = 1005757
[PASS] 6a proof: full trial division, no integer d in [2, isqrt(p)] divides p :: 1005756 divisors tested
[PASS] 6b p < 3474749660383 (Jaeschke 1993: bases 2,3,5,7,11,13 are then a deterministic test)
[PASS] 6b strong probable prime to bases 2,3,5,7,11,13
[PASS] 6b strong probable prime to the first 12 primes 2..37
factorisation of p-1 (trial division): 2 * 3^2 * 15937 * 3526207
[PASS] 6c factorisation of p-1 multiplies back to p-1
[PASS] 6c factor 2 of p-1 is prime (trial division up to its isqrt)
[PASS] 6c factor 3 of p-1 is prime (trial division up to its isqrt)
[PASS] 6c factor 15937 of p-1 is prime (trial division up to its isqrt)
[PASS] 6c factor 3526207 of p-1 is prime (trial division up to its isqrt)
[PASS] 6c no Fermat witness of compositeness among the bases tried
[PASS] 6c Lucas certificate: a^(p-1) == 1 and a^((p-1)/q) != 1 (mod p) for every prime q | p-1 :: a = 3
   a = 3: a^(p-1) mod p = 1
   a^((p-1)/2) mod p = 1011548897262
   a^((p-1)/3) mod p = 923634957738
   a^((p-1)/15937) mod p = 282943967462
   a^((p-1)/3526207) mod p = 455395794549
== 7. p does not divide b ==
[PASS] b mod p != 0 :: b mod p = 28910
[PASS] gcd(b, p) == 1
== 8. b^(p-1) == 1 (mod p^2), exact integer arithmetic ==
p^2 = 1023231171553991328891169
8a built-in pow(b, p-1, p^2)       = 1
8b own right-to-left exponentiation = 1
8c own left-to-right exponentiation = 1
[PASS] 8a residue == 1
[PASS] 8b residue == 1
[PASS] 8c residue == 1
8d b^((p-1)/2) mod p^2 = 1 ; Jacobi symbol (b/p) by reciprocity = 1
[PASS] 8d b^((p-1)/2) == (b/p) exactly mod p^2 (the only square roots of 1 mod p^2 are +1 and -1)
8e Fermat-quotient additivity: q_p(b) == sum of e*q_p(r) over the prime powers r^e of b (mod p)
[PASS] 8e r = 2: r^(p-1) == 1 (mod p)
   r = 2, e = 1: r^(p-1) mod p^2 = 758261268309278366571138, q_p(r) = 749604166799
[PASS] 8e r = 5: r^(p-1) == 1 (mod p)
   r = 5, e = 1: r^(p-1) mod p^2 = 255560911180672123912222, q_p(r) = 252643161267
[PASS] 8e r = 7: r^(p-1) == 1 (mod p)
   r = 7, e = 2: r^(p-1) mod p^2 = 9604882979041944260272, q_p(r) = 9495223617
[PASS] 8e r = 59: r^(p-1) == 1 (mod p)
   r = 59, e = 1: r^(p-1) mod p^2 = 1013430397659948278778439, q_p(r) = 1001860019226
   sum of e*q_p(r) mod p = 0 ; q_p(b) = (b^(p-1) mod p^2 - 1)/p = 0
[PASS] 8e sum of e*q_p(r) == 0 (mod p)
[PASS] 8e q_p(b) agrees with the sum (mod p)
[PASS] 8f residue mod p^3, reduced mod p^2, == 1
   informational: (b^(p-1) - 1)/p^2 mod p = 711009428776 (0 would mean p^3 divides b^(p-1) - 1)
== 9. absence from both Fischer tables (saved copies under claim/inputs/) ==
claim/inputs/FermQ_Sorg.txt: 288459 bytes, sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4, 10167 lines, 44745 digit tokens
   line: Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125
   line: Die Basen sind gegenwaertig durchsucht bis 4.8E+12
   line: 21.10.2026  Richard Fischer
[PASS] FermQ_Sorg.txt: table header line found
   rows after the header (line 13): 10000 row labels, smallest 2, largest 10125, strictly increasing: True
[PASS] FermQ_Sorg.txt: no table row labelled b
[PASS] FermQ_Sorg.txt: b never occurs as a whole number :: count = 0
[PASS] FermQ_Sorg.txt: p never occurs as a whole number :: count = 0
[PASS] FermQ_Sorg.txt: p's digit string never occurs, even inside a longer number :: count = 0
[PASS] FermQ_Sorg.txt: p never occurs with separators between its digits :: count = 0
claim/inputs/FermQ_Sort.txt: 33141 bytes, sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b, 1033 lines, 4707 digit tokens
   line: Die gefundenen Primzahlen der Fermatquotienten von der Basis 2 bis 1052
   line: Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
   line: Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
   line: 21.10.2026  Richard Fischer
[PASS] FermQ_Sort.txt: table header line found
   rows after the header (line 12): 982 row labels, smallest 2, largest 65537, strictly increasing: False
[PASS] FermQ_Sort.txt: no table row labelled b
[PASS] FermQ_Sort.txt: b never occurs as a whole number :: count = 0
[PASS] FermQ_Sort.txt: p never occurs as a whole number :: count = 0
[PASS] FermQ_Sort.txt: p's digit string never occurs, even inside a longer number :: count = 0
[PASS] FermQ_Sort.txt: p never occurs with separators between its digits :: count = 0
claim/inputs/ErstBasen.txt: 115771 bytes, sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820, 1270 lines, 10379 digit tokens
   line: 27.09.2025  Richard Fischer
   info (not part of the p1 criterion): b as whole number 0 times, p as whole number 0 times, p digit string 0 times, p with separators 0 times
claim/inputs/ErstPBasen.txt: 81696 bytes, sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362, 973 lines, 7315 digit tokens
   line: 27.07.2024  Richard Fischer
   info (not part of the p1 criterion): b as whole number 0 times, p as whole number 0 times, p digit string 0 times, p with separators 0 times
== 10. OEIS ==
files under claim/ whose name mentions oeis: 0. OEIS absence is not checkable offline by this checker; it is a NOVELTY matter (fetch record: claim/status_sources.md).
== summary ==
checks failed: 0
REPRODUCE_CHECK PASS
OUTPUT_DIGEST sha256=d9f2552d50152ed11093456d6a92c9a06b276b26531c92f673388e1c9e5b9bcc
```
Runs 2 (python3) and 3 (venv interpreter) ended with the same `OUTPUT_DIGEST sha256=d9f2552d50152ed11093456d6a92c9a06b276b26531c92f673388e1c9e5b9bcc`.
Their files are byte-identical to run 1 (section 6).

The "strictly increasing: False" line for FermQ_Sort.txt is a parser artifact. My row regex also matched a footnote after the
65537 row:
```
non-increasing at line 1031 : '9, 25, 27, 36, ..., die die gleichen Primzahlen haben, wie deren Grundbasen.' previous label 65537 line 1025
```
It does not affect the result: b and p never occur as numbers anywhere in the file.

## 2. GMP cross-check, a third arithmetic implementation (workspace venv interpreter, run twice)
Command: `<venv python> -B panel/work-reproduce/gmp_crosscheck.py claim 2>&1 | tee panel/work-reproduce/gmp_run1.txt`
```
gmpy2 2.3.2
b = 28910  p = 1011548897263
is_prime(p, 50) = True
is_strong_bpsw_prp(p) = True
is_power(b) = False
b mod p = 28910
powmod(b, p-1, p^2) = 1
powmod(b, (p-1)/2, p^2) = 1  legendre(b, p) = 1
Fermat quotient (powmod(b, p-1, p^2) - 1)/p = 0
GMPY2_CROSSCHECK PASS
```

## 3. Re-derivation of the additivity step, without reducing the sum
Fermat quotients are additive: q_p(b) == q_p(2) + q_p(5) + 2*q_p(7) + q_p(59) (mod p). The unreduced sum is exactly 2p.
```
q_p(2), q_p(5), q_p(7), q_p(59) = 749604166799 252643161267 9495223617 1001860019226
unreduced sum q_p(2)+q_p(5)+2*q_p(7)+q_p(59) = 2023097794526
sum // p = 2  sum % p = 0  2*p = 2023097794526
2*5*7**2*59 = 28910
```
None of the four prime factors of b is a Wieferich base for p (each q_p(r) is nonzero). The congruence holds only for the
product, which is consistent with the claim.

## 4. claim/verify.py and the one-liner, as given in claim/REPRODUCE.md
claim/REPRODUCE.md says to run `python3 verify.py object/pair.json` from inside claim/. The workspace's command rules
forbid `cd` combined with a pipe, so I passed the same file by path:
`python3 -B claim/verify.py claim/object/pair.json 2>&1 | tee panel/work-reproduce/verify_run1.txt`.
verify.py reads only the path it is given. Output, identical in all 3 runs:
```
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 28910, p = 1011548897263, Fermat quotient q_p(b) mod p = 0
PASS
exit status of verify.py: 0
```
One-liner from claim/REPRODUCE.md, `python3 -B -c "p=1011548897263; print(pow(28910, p-1, p*p))"`, run twice:
```
1
1
```
Review of claim/verify.py:
- Primality uses Miller-Rabin with the 12 prime bases 2..37 below the stated bound 318665857834031151167461. This is a
  valid deterministic test for p of this size.
- The perfect-power test checks the rounded float root plus or minus 1 for every k up to bit_length. That is exact for
  numbers this small.
- The congruence is computed with exact integer pow.
- There is no randomness and no network access.

## 5. Negative controls: claim/verify.py must fail bad pairs and agree with my primitives check by check
Command: `python3 -B panel/work-reproduce/neg_controls.py claim 2>&1 | tee panel/work-reproduce/neg_controls_run1.txt`.
The controls are panel/work-reproduce/controls/control_1..7.json. The run was repeated, with identical output.
```
== control_1.json: nc1 base off by one (b = 28911, p = 1011548897263)
   verify.py last line: FAIL ; exit status 1
   10125 < b < 65537                          verify.py=True  mine=True  agree=True
   b is not a perfect power                   verify.py=True  mine=True  agree=True
   p > 1e12                                   verify.py=True  mine=True  agree=True
   p is prime (deterministic Miller-Rabin)    verify.py=True  mine=True  agree=True
   p does not divide b                        verify.py=True  mine=True  agree=True
   b^(p-1) == 1 mod p^2                       verify.py=False mine=False agree=True
   overall: mine=FAIL, verify.py=FAIL, agree=True
== control_2.json: nc2 p+2, a multiple of 5 (b = 28910, p = 1011548897265)
   verify.py last line: FAIL ; exit status 1
   10125 < b < 65537                          verify.py=True  mine=True  agree=True
   b is not a perfect power                   verify.py=True  mine=True  agree=True
   p > 1e12                                   verify.py=True  mine=True  agree=True
   p is prime (deterministic Miller-Rabin)    verify.py=False mine=False agree=True
   p does not divide b                        verify.py=True  mine=True  agree=True
   b^(p-1) == 1 mod p^2                       verify.py=False mine=False agree=True
   overall: mine=FAIL, verify.py=FAIL, agree=True
== control_3.json: nc3 perfect power 13^4 inside the range (b = 28561, p = 1011548897263)
   verify.py last line: FAIL ; exit status 1
   10125 < b < 65537                          verify.py=True  mine=True  agree=True
   b is not a perfect power                   verify.py=False mine=False agree=True
   p > 1e12                                   verify.py=True  mine=True  agree=True
   p is prime (deterministic Miller-Rabin)    verify.py=True  mine=True  agree=True
   p does not divide b                        verify.py=True  mine=True  agree=True
   b^(p-1) == 1 mod p^2                       verify.py=False mine=False agree=True
   overall: mine=FAIL, verify.py=FAIL, agree=True
== control_4.json: nc4 base 10125, the range edge (b = 10125, p = 1011548897263)
   verify.py last line: FAIL ; exit status 1
   10125 < b < 65537                          verify.py=False mine=False agree=True
   b is not a perfect power                   verify.py=True  mine=True  agree=True
   p > 1e12                                   verify.py=True  mine=True  agree=True
   p is prime (deterministic Miller-Rabin)    verify.py=True  mine=True  agree=True
   p does not divide b                        verify.py=True  mine=True  agree=True
   b^(p-1) == 1 mod p^2                       verify.py=False mine=False agree=True
   overall: mine=FAIL, verify.py=FAIL, agree=True
== control_5.json: nc5 true Wieferich pair with p below 1e12 (20403 = 2*101^2 + 1) (b = 20403, p = 101)
   verify.py last line: FAIL ; exit status 1
   10125 < b < 65537                          verify.py=True  mine=True  agree=True
   b is not a perfect power                   verify.py=True  mine=True  agree=True
   p > 1e12                                   verify.py=False mine=False agree=True
   p is prime (deterministic Miller-Rabin)    verify.py=True  mine=True  agree=True
   p does not divide b                        verify.py=True  mine=True  agree=True
   b^(p-1) == 1 mod p^2                       verify.py=True  mine=True  agree=True
   overall: mine=FAIL, verify.py=FAIL, agree=True
== control_6.json: nc6 composite strong pseudoprime to bases 2..13 (3474749660383) (b = 28910, p = 3474749660383)
   verify.py last line: FAIL ; exit status 1
   10125 < b < 65537                          verify.py=True  mine=True  agree=True
   b is not a perfect power                   verify.py=True  mine=True  agree=True
   p > 1e12                                   verify.py=True  mine=True  agree=True
   p is prime (deterministic Miller-Rabin)    verify.py=False mine=False agree=True
   p does not divide b                        verify.py=True  mine=True  agree=True
   b^(p-1) == 1 mod p^2                       verify.py=False mine=False agree=True
   overall: mine=FAIL, verify.py=FAIL, agree=True
== control_7.json: positive control: the claimed pair (b = 28910, p = 1011548897263)
   verify.py last line: PASS ; exit status 0
   10125 < b < 65537                          verify.py=True  mine=True  agree=True
   b is not a perfect power                   verify.py=True  mine=True  agree=True
   p > 1e12                                   verify.py=True  mine=True  agree=True
   p is prime (deterministic Miller-Rabin)    verify.py=True  mine=True  agree=True
   p does not divide b                        verify.py=True  mine=True  agree=True
   b^(p-1) == 1 mod p^2                       verify.py=True  mine=True  agree=True
   overall: mine=PASS, verify.py=PASS, agree=True
controls run: 7
NEG_CONTROLS ALL AGREE
```

## 6. Determinism, and the saved inputs against the fetch record
Command: `python3 -B panel/work-reproduce/compare_runs.py claim 2>&1 | tee panel/work-reproduce/compare_runs.txt`
```
== (1) run outputs ==
72b371aa99fadaffabfba2259790907709a0e72dd1c9dbfc0071ffebf3c3f3b0  my_check_run1.txt
72b371aa99fadaffabfba2259790907709a0e72dd1c9dbfc0071ffebf3c3f3b0  my_check_run2.txt
72b371aa99fadaffabfba2259790907709a0e72dd1c9dbfc0071ffebf3c3f3b0  my_check_run3_venv.txt
   my_check (python3 x2, venv python x1): identical = True
b9ca7b710fca699047a907142ee4945179cb6133251bc1aedbdce9aa91fba4e2  gmp_run1.txt
b9ca7b710fca699047a907142ee4945179cb6133251bc1aedbdce9aa91fba4e2  gmp_run2.txt
   gmp_crosscheck (x2): identical = True
b4c1a7bd46e16f8929a7f048250e63ae9faad3ac3bcff840755f3114ffee30a8  verify_run1.txt
b4c1a7bd46e16f8929a7f048250e63ae9faad3ac3bcff840755f3114ffee30a8  verify_run2.txt
b4c1a7bd46e16f8929a7f048250e63ae9faad3ac3bcff840755f3114ffee30a8  verify_run3_venv.txt
   claim/verify.py (python3 x2, venv python x1): identical = True
f1b2f662800122bed0ff255693df89c4487fbdcf453d3524a42d4ec20c3d9c04  oneliner_run1.txt
f1b2f662800122bed0ff255693df89c4487fbdcf453d3524a42d4ec20c3d9c04  oneliner_run2.txt
   REPRODUCE.md one-liner (x2): identical = True
5c6edeee46966f5bf24cf6be5fe5ebbd9d9559f7d84fa75727e3f76fc9f99087  neg_controls_run1.txt
5c6edeee46966f5bf24cf6be5fe5ebbd9d9559f7d84fa75727e3f76fc9f99087  neg_controls_run2.txt
   negative controls (x2): identical = True
RUNS_DETERMINISTIC True
== (2) claim/status_sources.md records vs claim/inputs/ ==
inputs/FermQ_Sorg.txt recorded 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 actual 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 match = True
inputs/FermQ_Sort.txt recorded bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b actual bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b match = True
inputs/ErstBasen.txt recorded e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 actual e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 match = True
inputs/ErstPBasen.txt recorded 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 actual 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 match = True
files recorded with a copy: ['ErstBasen.txt', 'ErstPBasen.txt', 'FermQ_Sorg.txt', 'FermQ_Sort.txt']
files present in claim/inputs/: ['ErstBasen.txt', 'ErstPBasen.txt', 'FermQ_Sorg.txt', 'FermQ_Sort.txt']
RECORDS_MATCH True
```

## 7. Scope and notes (none of them blocks)
- **What kind of claim this is.** claim/claim.md claims existence of one pair. It makes no exhaustive-search or coverage
  statement, so the rule "a sample is a spot check" does not apply. The object was checked completely, not sampled.
- **No tabulated pair under another base.** p occurs nowhere in either saved table, so no tabulated base carries this p.
  Since b is not a perfect power either, the pair cannot be an existing table entry under another base.
- **Coercion in claim/verify.py.** It reads b and p with int(), so it would also accept strings. The object holds genuine
  JSON integers (section 1), so this changes nothing here.
- **Table absence is not automated.** claim/verify.py does not test it; claim/REPRODUCE.md leaves it to a manual search. I
  did that search with code, on the saved copies (section 1, part 9).
- **Not confirmed by this role:**
  - OEIS absence. claim/status_sources.md records the search: URL, time, HTTP 200, the sha256 of the response, and the
    quoted sentence "Sorry, but the terms do not match anything in the table". The response itself is not saved under
    claim/, so I cannot re-derive it from saved files.
  - Whether the live Fischer tables changed after the recorded fetch.
  Both belong to NOVELTY, which re-fetches.

## Verdict
Reproduced, deterministic, no mismatch. Within this role's scope, the pair (28910, 1011548897263) meets every
mathematical clause of p1:
- 10125 < b < 65537;
- b is not a perfect power;
- p > 1e12;
- p is proven prime, by trial division and by a Lucas certificate;
- p does not divide b;
- b^(p-1) == 1 (mod p^2), exactly;
- the pair is absent from both saved Fischer tables.

claim/verify.py reproduces the same result and correctly fails all six negative controls.
pass: true
