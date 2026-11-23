role: REPRODUCE
context: claude code Task subagent (fresh context, saw only claim/)

# REPRODUCE report: pair (b, p) = (28860, 1017279755641), partial win p1

Report written after 2026-11-07T21:18:08Z (`date -u`). All paths below are relative to the run folder
(the claim is in claim/, my scratch work in panel/work2-reproduce/).

## Definition checked (quoted verbatim from claim/claim.md, partial win p1)

"New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2
checked exactly, and absent from both Fischer tables and OEIS."

The claim (claim/claim.md) and the object (claim/object/pair.json) name b = 28860 and p = 1017279755641, and
the congruence 28860^1017279755640 == 1 (mod 1017279755641^2).

## Order of work

1. Read claim/claim.md and claim/object/pair.json, and previewed the head and tail of the four files in
   claim/inputs/ to learn their format.
2. Wrote my own checker, panel/work2-reproduce/my_check.py (Python standard library only), from the definition
   above, plus a GMP cross-check, panel/work2-reproduce/my_check_gmpy2.py. I ran both **before** opening
   claim/verify.py or claim/REPRODUCE.md.
3. Only then read claim/REPRODUCE.md, claim/verify.py and claim/status_sources.md. I ran claim/verify.py exactly
   as REPRODUCE.md says (from inside claim/: `python3 verify.py object/pair.json`), twice, and twice more with
   full paths. I also ran the REPRODUCE.md one-liner, fed verify.py five mutated pairs, cross-checked every
   Fermat quotient it printed, and compared the recorded source hashes with the saved inputs.
4. Re-hashed claim/ at the end: it is unchanged (same 9 files, same sha256).

my_check.py was revised twice, for output format only: once to make the source ASCII-only, and once to drop
arrow tokens from its output lines. Every version ended `MY_CHECK RESULT: ALL PASS`. The output below is from
the final version, sha256 3dbcc16ccf8ee53adf1cb7dfb8054872c70ef109c2876a54a7e0ea7632d69ac3.

## Verdict per property

| # | Property | How it was verified (sections below) | Result |
|---|---|---|---|
| 1 | object present, well formed, agrees with claim.md | A1-A10: keys, integer types, target_id, partial_win, congruence base/exponent/modulus, criterion text | PASS |
| 2 | 10125 < b < 65537 | B1 (b = 28860); gmpy2; verify.py | PASS |
| 3 | b is not a perfect power | C1: exact integer k-th roots for k = 2..14 (2^14 <= b < 2^15), none exact; C2-C4: b = 2^2 * 3 * 5 * 13 * 37, gcd of exponents 1; gmpy2.is_power False; verify.py | PASS |
| 4 | p above 1e12 | D1: p - 10**12 = 17279755641; gmpy2; verify.py | PASS |
| 5 | p is prime (proved) | E1: complete trial division by every integer 2..isqrt(p) = 1008602 (1008601 divisions, no divisor); E2: deterministic Miller-Rabin (p below psi_6 = 3474749660383, Jaeschke); E3: Lucas test, p-1 = 2^3 * 3^2 * 5 * 47^2 * 1279211 fully factored (each factor proved prime), witness a = 11; gmpy2 is_prime and strong BPSW; verify.py | PASS |
| 6 | p does not divide b | F1: b mod p = 28860, gcd(b, p) = 1 | PASS |
| 7 | b^(p-1) == 1 (mod p^2), exact | G: five routes (built-in pow, own square-and-multiply, Fermat-quotient additivity over 2, 3, 5, 13, 37, exponent chain over the prime factors of p-1, b^p == b mod p^2); gmpy2.powmod = 1; verify.py; REPRODUCE.md one-liner prints 1 | PASS |
| 8 | absent from both Fischer tables (saved copies) | H: p occurs 0 times (as token, substring, and with thousands separators) in all four saved files; b occurs 0 times as a token in all four; no row for b in FermQ_Sorg.txt (bases 2..10125) or FermQ_Sort.txt (bases 2..1052 and 65537) | PASS |
| 9 | saved inputs are the recorded fetches | compare_sources.py: 4/4 sha256 in claim/status_sources.md MATCH the saved copies | PASS |
| 10 | absent from OEIS | not re-derivable from saved files (no OEIS response is saved in claim/); see "Scope" below | not in REPRODUCE scope |
| 11 | determinism | my_check.py 3 runs byte-identical; gmpy2 check 2 runs byte-identical; verify.py 4 runs byte-identical | PASS |

Proof steps re-derived:
- **Primality.** isqrt(p) = 1008602, with 1008602^2 = 1017277994404 <= p and 1008603^2 = 1017280011609 above
  p. No integer d in 2..1008602 divides p, so p is prime. Two independent proofs agree: the Lucas witness 11 has
  order exactly p-1 (11^(p-1) == 1, and 11^((p-1)/q) != 1 for q = 2, 3, 5, 47, 1279211), and all Miller-Rabin
  rounds pass below the Jaeschke bound.
- **Not a perfect power.** b = 2^2 * 3 * 5 * 13 * 37, and the exponents (2, 1, 1, 1, 1) have gcd 1.
- **The Wieferich congruence.** It is equivalent to q_p(b) == 0 (mod p). By additivity,
  q_p(b) = 2*q_p(2) + q_p(3) + q_p(5) + q_p(13) + q_p(37). With the values printed below the sum is
  3051839266923, which is 0 mod p. This route never exponentiates b itself, and it agrees with the direct
  computation pow(b, p-1, p^2) = 1.

## Evidence (real command output)

### 1. Own checker, final version, run 1 (full output)

Command: `python -B panel/work2-reproduce/my_check.py claim` (venv interpreter), with output captured by
`2>&1 | tee`.

```
=== my_check.py: REPRODUCE skeptic's independent checker ===
definition (claim/claim.md, p1, verbatim): New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS.

--- inventory of the claim folder (sha256, bytes, path relative to claim/) ---
84708ae3ce9db6735b8e7905fa79c8c87bfd7b23c325b3664cdf51f9b0bde689      958  claim/REPRODUCE.md
bda2e42b48de713106c39bff37d16505cd561feadeca12147751ed56a9c6b1fb     1774  claim/claim.md
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820   115771  claim/inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362    81696  claim/inputs/ErstPBasen.txt
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4   288459  claim/inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b    33141  claim/inputs/FermQ_Sort.txt
6f917770e4d29ea0863a3c1801b1d0f216e7d54316a6d4ba768b179fec8a4ed1      106  claim/object/pair.json
6bf508fbd94ac7be6201d776f6151e26850ffcf5a00c281e8baee2429eaacfd9     1690  claim/status_sources.md
991d0c0f01f695e615c871a283bde85def2a1f0de8758494df25933b184d02e7     2370  claim/verify.py

--- A. object/pair.json and claim.md ---
pair.json: {"b": 28860, "p": 1017279755641, "partial_win": "p1", "target_id": "wieferich-other-bases-fischer-table"}
CHECK A1 pair.json keys: ['b', 'p', 'partial_win', 'target_id'] -- PASS
CHECK A2 b and p are JSON integers: type(b)=int type(p)=int -- PASS
CHECK A3 target_id: wieferich-other-bases-fischer-table -- PASS
CHECK A4 partial_win: p1 -- PASS
claim.md congruence parsed: base=28860 exponent=1017279755640 modulus=1017279755641^2
CHECK A5 claim.md congruence base == b: 28860 vs 28860 -- PASS
CHECK A6 claim.md congruence modulus root == p: 1017279755641 vs 1017279755641 -- PASS
CHECK A7 claim.md exponent == p-1: 1017279755640 vs 1017279755640 -- PASS
CHECK A8 claim.md 'p = ...' equals pair.json p: 1017279755641 -- PASS
CHECK A9 claim.md 'b = ...' equals pair.json b: 28860 -- PASS
CHECK A10 claim.md carries the p1 criterion verbatim: substring search -- PASS

--- B. base range ---
CHECK B1 10125 < b < 65537: b=28860 -- PASS

--- C. b is not a perfect power ---
b.bit_length()=15 so exponents k=2..14 are tested
  k= 2: floor root=169, root^k=28561, (root+1)^k=28900
  k= 3: floor root=30, root^k=27000, (root+1)^k=29791
  k= 4: floor root=13, root^k=28561, (root+1)^k=38416
  k= 5: floor root=7, root^k=16807, (root+1)^k=32768
  k= 6: floor root=5, root^k=15625, (root+1)^k=46656
  k= 7: floor root=4, root^k=16384, (root+1)^k=78125
  k= 8: floor root=3, root^k=6561, (root+1)^k=65536
  k= 9: floor root=3, root^k=19683, (root+1)^k=262144
  k=10: floor root=2, root^k=1024, (root+1)^k=59049
  k=11: floor root=2, root^k=2048, (root+1)^k=177147
  k=12: floor root=2, root^k=4096, (root+1)^k=531441
  k=13: floor root=2, root^k=8192, (root+1)^k=1594323
  k=14: floor root=2, root^k=16384, (root+1)^k=4782969
CHECK C1 no exact k-th root for k>=2: exact roots at k=[] -- PASS
factorisation by trial division: 28860 = 2^2 * 3 * 5 * 13 * 37 (product check 28860)
CHECK C2 factorisation multiplies back to b: 28860 -- PASS
CHECK C3 each factor of b is prime (trial division): [2, 3, 5, 13, 37] -- PASS
CHECK C4 gcd of exponents == 1: gcd=1 -- PASS

--- D. p above 1e12 ---
CHECK D1 p > 10**12: p=1017279755641, p-10**12=17279755641 -- PASS

--- E. primality of p (three independent proofs) ---
isqrt(p)=1008602, r^2=1017277994404, (r+1)^2=1017280011609, r^2<=p<(r+1)^2: True
CHECK E1 complete trial division by every integer 2..isqrt(p): divisions=1008601, smallest divisor=None -- PASS
strong-probable-prime rounds, bases [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]: [True, True, True, True, True, True, True, True, True, True, True, True]
CHECK E2 deterministic Miller-Rabin (bases 2..13 suffice below psi_6): p<psi_6=3474749660383: True -- PASS
p-1 = 1017279755640 = 2^3 * 3^2 * 5 * 47^2 * 1279211 (product check 1017279755640)
prime factors of p-1 proved prime by trial division: {2: True, 3: True, 5: True, 47: True, 1279211: True}
Lucas witness a=11: a^(p-1) mod p = 1; a^((p-1)/2) mod p = 1017279755640, a^((p-1)/3) mod p = 331660448318, a^((p-1)/5) mod p = 495396832494, a^((p-1)/47) mod p = 325776137472, a^((p-1)/1279211) mod p = 676978286326
CHECK E3 Lucas test with fully factored p-1: witness=11, fermat_failure_base=None -- PASS

--- F. p does not divide b ---
CHECK F1 b mod p != 0 and gcd(b,p)=1: b mod p=28860, gcd=1 -- PASS

--- G. b^(p-1) == 1 (mod p^2), exact integer arithmetic ---
p^2 = 1034858101237012671320881
b^(p-1) mod p^2 (built-in pow)          = 1
b^(p-1) mod p^2 (own square-and-multiply) = 1
b^(p-1) mod p (Fermat level)            = 1
Fermat quotient q_p(b) = 0
  q_p(2) = 805472779928 (exponent 2 in b)
  q_p(3) = 647969670660 (exponent 1 in b)
  q_p(5) = 149508072110 (exponent 1 in b)
  q_p(13) = 515524916456 (exponent 1 in b)
  q_p(37) = 127891047841 (exponent 1 in b)
  sum of e*q_p(r) = 3051839266923, mod p = 0
CHECK G R1 built-in pow: pow(b, p-1, p^2) == 1 -- PASS
CHECK G R2 own square-and-multiply: b^(p-1) mod p^2 == 1 -- PASS
CHECK G R3 Fermat-quotient additivity: sum over r^e || b of e*q_p(r) == 0 (mod p) -- PASS
CHECK G R4 exponent chain over the prime factors of p-1: (((b^q1)^q2)...) mod p^2 == 1 -- PASS
CHECK G R5 equivalent form: b^p == b (mod p^2) -- PASS

--- H. saved Fischer files in claim/inputs/ (no row for b, no occurrence of p) ---
separator-tolerant pattern for p: "(?<!\\d)1[ .,'\xa0]?017[ .,'\xa0]?279[ .,'\xa0]?755[ .,'\xa0]?641(?!\\d)"
ErstBasen.txt: 10379 integer tokens; tokens == p: 0; substring p: 0; separator-tolerant p: 0; tokens == b: 0; 13+ digit tokens: 431
CHECK H ErstBasen.txt: p absent: 0/0/0 -- PASS
ErstPBasen.txt: 7315 integer tokens; tokens == p: 0; substring p: 0; separator-tolerant p: 0; tokens == b: 0; 13+ digit tokens: 188
CHECK H ErstPBasen.txt: p absent: 0/0/0 -- PASS
FermQ_Sorg.txt: 44745 integer tokens; tokens == p: 0; substring p: 0; separator-tolerant p: 0; tokens == b: 0; 13+ digit tokens: 572
CHECK H FermQ_Sorg.txt: p absent: 0/0/0 -- PASS
FermQ_Sort.txt: 4707 integer tokens; tokens == p: 0; substring p: 0; separator-tolerant p: 0; tokens == b: 0; 13+ digit tokens: 158
CHECK H FermQ_Sort.txt: p absent: 0/0/0 -- PASS
FermQ_Sorg.txt header: 'Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125'
FermQ_Sorg.txt header: 'Die Basen sind gegenwaertig durchsucht bis 4.8E+12'
FermQ_Sort.txt header: 'Die gefundenen Primzahlen der Fermatquotienten von der Basis 2 bis 1052'
FermQ_Sort.txt header: 'Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14'
FermQ_Sort.txt header: 'Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13'
FermQ_Sort.txt header: '65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)'
FermQ_Sorg.txt rows parsed: 10001, min base 2, max base 10125
FermQ_Sort.txt rows parsed: 981, min base 2, max base 65537
CHECK H FermQ_Sorg.txt has no row for b: 28860 in rows: False -- PASS
CHECK H FermQ_Sort.txt has no row for b: 28860 in rows: False -- PASS

--- Z. controls (the same code on known answers) ---
CHECK Z1 known pair (2, 1093): prime=True -- PASS
CHECK Z1 known pair (2, 3511): prime=True -- PASS
CHECK Z1 known pair (3, 11): prime=True -- PASS
CHECK Z1 known pair (3, 1006003): prime=True -- PASS
CHECK Z1 known pair (5, 2): prime=True -- PASS
CHECK Z1 known pair (5, 20771): prime=True -- PASS
CHECK Z1 known pair (5, 40487): prime=True -- PASS
CHECK Z1 known pair (5, 53471161): prime=True -- PASS
CHECK Z1 known pair (5, 1645333507): prime=True -- PASS
CHECK Z1 known pair (5, 6692367337): prime=True -- PASS
CHECK Z1 known pair (5, 188748146801): prime=True -- PASS
CHECK Z1 known pair (7, 5): prime=True -- PASS
CHECK Z1 known pair (7, 491531): prime=True -- PASS
CHECK Z1 known pair (10, 3): prime=True -- PASS
CHECK Z1 known pair (10, 487): prime=True -- PASS
CHECK Z1 known pair (10, 56598313): prime=True -- PASS
exhaustive control: 85714 primes below 1100000
CHECK Z2 exhaustive base 2 below 1100000: found=[1093, 3511] expected=[1093, 3511] -- PASS
CHECK Z2 exhaustive base 3 below 1100000: found=[11, 1006003] expected=[11, 1006003] -- PASS
CHECK Z2 exhaustive base 5 below 1100000: found=[2, 20771, 40487] expected=[2, 20771, 40487] -- PASS
CHECK Z2 exhaustive base 7 below 1100000: found=[5, 491531] expected=[5, 491531] -- PASS
CHECK Z2 exhaustive base 10 below 1100000: found=[3, 487] expected=[3, 487] -- PASS
CHECK Z3 perturbed pair (28859, 1017279755641) is NOT Wieferich: residue=6660953383860137955928 -- PASS
CHECK Z3 perturbed pair (28861, 1017279755641) is NOT Wieferich: residue=326043247432694220901043 -- PASS
CHECK Z3 perturbed pair (28860, 1017279755669) is NOT Wieferich: residue=638594272201669009962668 -- PASS
CHECK Z3 perturbed pair (28860, 1017279755633) is NOT Wieferich: residue=627618936420149295919486 -- PASS

MY_CHECK RESULT: ALL PASS
exit status: 0
```

The controls show the checker can discriminate. It accepts the 16 literature Wieferich pairs. Exhaustive scans
of every prime below 1100000 for bases 2, 3, 5, 7 and 10 find exactly the known sets, and four perturbed pairs
next to the claim are rejected.

Determinism: run 2 (venv interpreter) and run 3 (`python3` on PATH, which printed `Python 3.14.7`) are
byte-identical to run 1:

```
3dbcc16ccf8ee53adf1cb7dfb8054872c70ef109c2876a54a7e0ea7632d69ac3 *my_check.py
245024b8ad8849a860c0b08c5bc2cfdae650ea8de352f6f1e227d847fcff7ace *my_check_v3_run1.txt
245024b8ad8849a860c0b08c5bc2cfdae650ea8de352f6f1e227d847fcff7ace *my_check_v3_run2.txt
245024b8ad8849a860c0b08c5bc2cfdae650ea8de352f6f1e227d847fcff7ace *my_check_v3_python3.txt
ca2f5df30322e032aa6fb770f2068bf25ceab12e02e151bc1e4f14dc5f4a3479 *gmpy2_v2_run1.txt
ca2f5df30322e032aa6fb770f2068bf25ceab12e02e151bc1e4f14dc5f4a3479 *gmpy2_v2_run2.txt
my_check: 3 runs byte-identical
gmpy2: 2 runs byte-identical
```

### 2. GMP cross-check (independent big-integer library), run 1 of 2

Command: `python -B panel/work2-reproduce/my_check_gmpy2.py claim` (venv interpreter). Run 2 is byte-identical
(hashes above).

```
gmpy2 2.3.2 | GMP GMP 6.3.0
b = 28860 p = 1017279755641
gmpy2.powmod(b, p-1, p^2) = 1
gmpy2.powmod(b, p, p^2) == b: True
Fermat quotient (b^(p-1) mod p^2 - 1)/p mod p = 0
gmpy2.is_prime(p, 50): True
gmpy2.is_strong_bpsw_prp(p): True
gmpy2.is_strong_prp(p, 2): True
gmpy2.next_prime(p - 1) == p: True
gmpy2.isqrt(p) = 1008602 | is_square(p): False
gmpy2.is_power(b): False
exact k-th roots of b, k=2..14: []
10125 < b < 65537: True
p exceeds 10**12: True
b mod p = 28860 | gcd(b,p) = 1
GMPY2_CROSSCHECK: PASS
exit status: 0
```

### 3. The author's checker, claim/verify.py, run as claim/REPRODUCE.md says

Command: from inside claim/, `python3 -B verify.py object/pair.json`, run twice. It was also run twice with
full paths. All four outputs are byte-identical:

```
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 28860, p = 1017279755641, Fermat quotient q_p(b) mod p = 0
PASS
exit status: 0
```

```
bba0429deeaf31cb4672dcaf92d3d272325d79d40f0e54112b6276ed20cb1a37 *verify_abs_run1.txt
bba0429deeaf31cb4672dcaf92d3d272325d79d40f0e54112b6276ed20cb1a37 *verify_abs_run2.txt
bba0429deeaf31cb4672dcaf92d3d272325d79d40f0e54112b6276ed20cb1a37 *verify_asdocumented_run1.txt
bba0429deeaf31cb4672dcaf92d3d272325d79d40f0e54112b6276ed20cb1a37 *verify_asdocumented_run2.txt
all four verify.py outputs byte-identical
```

The REPRODUCE.md one-liner, `python3 -B -c "p=1017279755641; print(pow(28860, p-1, p*p))"`, printed:

```
1
exit status: 0
```

Reading of verify.py (sha256 991d0c0f...; read only after my own checks):
- Its Miller-Rabin is standard: 12 prime bases, with a guard that refuses to answer at or above the cited
  Jiang-Deng bound.
- Its perfect-power test uses floating-point k-th roots with a window of plus or minus 1. That is exact at this
  size of b, and my exact-integer route agrees.
- The range, size, divisibility and congruence tests are exact integer arithmetic.
- It does not check the target_id or partial_win fields, or absence from the tables. REPRODUCE.md leaves table
  absence as a search. My checker covers all three (A3, A4, H).
- I found no defect.

### 4. verify.py rejects wrong pairs (mutation test, inputs in panel/work2-reproduce/)

```
### mut1_b_plus_1.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28861, "p": 1017279755641}
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 28861, p = 1017279755641, Fermat quotient q_p(b) mod p = 320504999362
FAIL
exit status: 1
### mut2_p_plus_2.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28860, "p": 1017279755643}
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
FAIL p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 28860, p = 1017279755643, Fermat quotient q_p(b) mod p = 223355118527
FAIL
exit status: 1
### mut3_perfect_power.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28561, "p": 1017279755641}
ok   10125 < b < 65537
FAIL b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 28561, p = 1017279755641, Fermat quotient q_p(b) mod p = 27540154542
FAIL
exit status: 1
### mut4_b_out_of_range.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 10125, "p": 1017279755641}
FAIL 10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 10125, p = 1017279755641, Fermat quotient q_p(b) mod p = 1005843387688
FAIL
exit status: 1
### mut5_known_small_pair.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 5, "p": 188748146801}
FAIL 10125 < b < 65537
ok   b is not a perfect power
FAIL p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 5, p = 188748146801, Fermat quotient q_p(b) mod p = 0
FAIL
exit status: 1
```

Each mutation fails on the right line. mut5 is a genuine Wieferich pair outside the p1 cell: its congruence
line passes, and only the range and size lines fail.

### 5. Every Fermat quotient printed by verify.py, re-derived with my own arithmetic

Command: `python3 -B panel/work2-reproduce/crosscheck_quotients.py` on the saved verify.py outputs.

```
b=28860 p=1017279755641 (p prime: True): verify.py q=0 | own direct q=0 | own additive q=0 -- AGREE
b=28861 p=1017279755641 (p prime: True): verify.py q=320504999362 | own direct q=320504999362 | own additive q=320504999362 -- AGREE
b=28860 p=1017279755643 (p prime: False): verify.py q=223355118527 | own direct q=223355118527 | own additive q=None -- AGREE
b=28561 p=1017279755641 (p prime: True): verify.py q=27540154542 | own direct q=27540154542 | own additive q=27540154542 -- AGREE
b=10125 p=1017279755641 (p prime: True): verify.py q=1005843387688 | own direct q=1005843387688 | own additive q=1005843387688 -- AGREE
b=5 p=188748146801 (p prime: True): verify.py q=0 | own direct q=0 | own additive q=0 -- AGREE
QUOTIENT_CROSSCHECK: PASS
exit status: 0
```

### 6. Recorded fetch hashes against the saved inputs

Command: `python3 -B panel/work2-reproduce/compare_sources.py claim`.

```
records with a saved copy in status_sources.md: 4
inputs/FermQ_Sorg.txt: recorded 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 | computed 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 | MATCH
inputs/FermQ_Sort.txt: recorded bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b | computed bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b | MATCH
inputs/ErstBasen.txt: recorded e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 | computed e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 | MATCH
inputs/ErstPBasen.txt: recorded 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 | computed 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 | MATCH
files in inputs/: ['ErstBasen.txt', 'ErstPBasen.txt', 'FermQ_Sorg.txt', 'FermQ_Sort.txt']
every saved input has a record, and vice versa: True
recorded fetches without a saved copy in claim/ (sha256 followed by ';'): 1
SOURCES_COMPARE: PASS
```

### 7. claim/ unchanged after all runs

```
84708ae3ce9db6735b8e7905fa79c8c87bfd7b23c325b3664cdf51f9b0bde689 claim/REPRODUCE.md
bda2e42b48de713106c39bff37d16505cd561feadeca12147751ed56a9c6b1fb claim/claim.md
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 claim/inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 claim/inputs/ErstPBasen.txt
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 claim/inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b claim/inputs/FermQ_Sort.txt
6f917770e4d29ea0863a3c1801b1d0f216e7d54316a6d4ba768b179fec8a4ed1 claim/object/pair.json
6bf508fbd94ac7be6201d776f6151e26850ffcf5a00c281e8baee2429eaacfd9 claim/status_sources.md
991d0c0f01f695e615c871a283bde85def2a1f0de8758494df25933b184d02e7 claim/verify.py
claim folder unchanged: same 9 files, same sha256 as the first inventory
```

Scratch files (panel/work2-reproduce/):

```
3dbcc16ccf8ee53adf1cb7dfb8054872c70ef109c2876a54a7e0ea7632d69ac3 *my_check.py
0e2fe334e717a3e86995a5e8a8a22869654c9a73e20a93507ea343228b67cc56 *my_check_gmpy2.py
64bca5f2611a04daf29d02456f9cee978fa9430d3edaad785fc713b374f41ce5 *compare_sources.py
53853e8bebc8940122799f73f0a003b0db7a3daae17be21180bfb5c5bac063a0 *crosscheck_quotients.py
4406c10b5ae4dba3291e39423fbe1fb154b4575e44fa10aa828e6f409d755de1 *mut1_b_plus_1.json
d7e2a1a89dbf5e973fba573490855175885e8cf05a26bf5157c2d10a435c8501 *mut2_p_plus_2.json
ff529ba6919cb5dc413a7b1d40b9554f62fbc446651f29648250c660ee2af907 *mut3_perfect_power.json
11df903022cfe604ddea7b4d06211fea13b88bc197c1e429d8f06dcc0ebc406b *mut4_b_out_of_range.json
1175c4c74b420f832c19615ce4ffe9691254a3f5f98a34885ce60c918172fd37 *mut5_known_small_pair.json
```

## Scope and limits

- **OEIS.** The OEIS clause of the definition cannot be re-derived from saved files: no OEIS response is saved
  in claim/. claim/status_sources.md records the fetch only, with HTTP 200, a sha256 and the quoted text "Sorry,
  but the terms do not match anything in the table". This role makes no network requests, so the OEIS check is
  left to the NOVELTY skeptic's fresh fetch. The same holds for the live versions of Fischer's files. I verified
  only that the saved copies match their recorded hashes and do not contain the pair.
- **Not an exhaustive-search claim.** The claim asserts one pair, not the completeness of a search, so the
  "sample is a spot check" rule does not apply. Every property was checked in full and none was sampled. The
  trial-division proof covers every integer from 2 to isqrt(p).
- **Disclosure about context.** The Claude Code harness preloads the workspace's project instruction files
  (CLAUDE.md and the files it imports) into every session, and those files summarise this pair's earlier
  status. I did not open them. No result above relies on them: every value comes from claim/ and my own
  computation. Outside claim/, I listed the file names in the panel folder to find my scratch folder, and read
  this output file's one-line reservation stub, because the Write tool needs a read before it can overwrite. I
  opened no other panel file.

## Verdict

Every property of the p1 definition that can be checked from the saved files reproduces exactly, by
independent routes, with nothing missing and no non-determinism:
- the object is present and consistent with the claim text;
- 10125 < 28860 < 65537;
- 28860 = 2^2 * 3 * 5 * 13 * 37 is not a perfect power;
- p is above 1e12;
- p is prime, proved by trial division and confirmed by a Lucas certificate and deterministic Miller-Rabin;
- p does not divide b;
- 28860^(p-1) == 1 (mod p^2) in exact arithmetic;
- p is absent from all four saved Fischer files, neither table has a row for b, and the saved files match their
  recorded hashes.

The author's verify.py independently gives the same verdict, deterministically, and it correctly rejects five
wrong pairs. I found no mismatch.
pass: true