role: REPRODUCE
context: hermes delegation (delegate_task subagent, fresh context, saw only claim/)

# REPRODUCE review: wieferich-other-bases-fischer-table, partial win p1, (b, p) = (17766, 1016845912283)

## Verdict in brief

Every property of the p1 criterion that the saved files can show reproduces exactly. I checked each one twice: with a checker I wrote from the
criterion text before opening verify.py, and with a second implementation in a different runtime (Node BigInt).

- **Range and form of b:** 10125 < b < 65537, and b = 2 · 3^3 · 7 · 47 is not a perfect power.
- **Size of p:** p = 1016845912283 exceeds 10^12.
- **Primality of p:** proven twice without the author's Miller-Rabin. First, full trial division by every integer from 2 to isqrt(p) = 1008387.
  Second, a Lucas n−1 certificate with p−1 = 2 · 487 · 1043989643 and witness 2.
- **p does not divide b.**
- **Congruence:** pow(b, p-1, p^2) == 1 exactly, derived four independent ways.
- **Fischer tables:** base 17766 has no row in either table, and p occurs nowhere in the four saved Fischer files.

verify.py, run as REPRODUCE.md says, prints PASS and agrees with me on every property it tests. Every run is byte-identical, and claim/ was not
modified.

## The definition I checked against (quoted from claim.md before opening verify.py)

> criterion for p1 (verbatim, bank/targets.json): New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS.

The definition of a pair, from the full success criterion quoted in claim.md:

> ... that is not a perfect power (a pair for b = a^k with p not dividing k is the same pair as for a), and a proven prime p not dividing b with pow(b, p-1, p^2) == 1.

From these two quotes my checker derives nine properties to test:

1. b and p are the object's integers and match claim.md.
2. 10125 < b < 65537.
3. b is not a perfect power.
4. p is above 1e12, i.e. strictly greater than 10^12.
5. p is a proven prime.
6. p does not divide b.
7. pow(b, p-1, p^2) == 1, computed exactly.
8. The pair is absent from both Fischer tables (the copies saved in inputs/).
9. The pair is absent from OEIS.

## Order of work and independence

1. I read claim.md and object/pair.json. In inputs/ I looked only at the file layout (headers and row formats), so I could write a parser.
2. I wrote and ran my own checker, ../panel/work-reproduce/my_check.py. Every path in this file is relative to claim/. Then I wrote two more
   scripts in the same folder:
   - node_check.js, a second implementation using Node BigInt and exact doubles;
   - controls.py, with negative and positive controls.
3. Only then did I open REPRODUCE.md, status_sources.md and verify.py. I ran verify.py exactly as REPRODUCE.md says and compared the results.

I opened files in claim/ and my own scratch files, nothing else. At the start I listed the run folder once to find claim/ (names only). I opened
no sibling file and loaded no skill or memory. Transcript 2 adds live re-fetches: read-only GETs that go beyond the saved-file verdict.

## How each proof step was re-derived

### Primality of p

- **Proof 1, trial division (a complete proof by itself).**
  - A composite n always has a divisor d with 2 ≤ d ≤ isqrt(n).
  - isqrt(p) = 1008387, checked against its definition: r^2 ≤ p, and (r+1)^2 exceeds p.
  - I tried all 1008386 integers d from 2 to 1008387: every integer, not only primes, and not a sample. Each one leaves a nonzero remainder.
  - The Node run repeats the loop in IEEE doubles and gets the same result. Doubles are exact here because p is below 2^53.
- **Proof 2, Lucas certificate (independent of proof 1).**
  - Trial division gives p−1 = 2 · 487 · 1043989643, and all three factors are prime.
  - For a = 2: 2^(p−1) ≡ 1 (mod p), and 2^((p−1)/q) ≢ 1 (mod p) for q = 2, 487 and 1043989643.
  - So 2 has order p−1 modulo p. That gives φ(p) = p−1, so p is prime (Lucas).
- **Cross-check only:** p passes Miller-Rabin to bases 2..37. My verdict does not rely on it.
- **Control for proof 1:** the same loop finds the factor 1008379 in the composite 1008379 · 1008401 = 1016850391979. That composite is close to p,
  and its smallest factor sits just below isqrt(p), so the loop really runs to the top of its range.

### b is not a perfect power

- Trial division gives b = 17766 = 2 · 3^3 · 7 · 47. I checked that the factors multiply back to b and that each one is prime.
- The gcd of the exponents is 1, so b is not a perfect power.
- Brute force over k = 2..15 finds no integer r with r^k = b.
- **Controls:** 17689 = 133^2, 17576 = 26^3 and 16807 = 7^5 are all flagged as perfect powers.

### p does not divide b

b is below p, so b mod p = 17766, which is not 0. Also gcd(b, p) = 1.

### The congruence, in exact big-integer arithmetic

Four independent derivations, all giving the same answer:

1. The builtin pow(b, p−1, p^2) returns 1.
2. My own left-to-right square-and-multiply returns 1.
3. The equivalent form b^p ≡ b (mod p^2) holds.
4. Via the factorisation:
   - For each prime factor a of b, write a^(p−1) = 1 + p·q_p(a) (mod p^2), where q_p(a) is the Fermat quotient.
   - Multiplying out gives b^(p−1) ≡ 1 + p·(q_p(2) + 3q_p(3) + q_p(7) + q_p(47)) (mod p^2).
   - That sum is 0 mod p, so the residue is 1.

The Node run (right-to-left exponentiation on BigInt) also returns 1.

- **Positive controls:** the same routine returns 1 for every pair in the saved table rows for bases 2 and 5, up to p = 188748146801.
- **Negative controls:** it does not return 1 for bases 17765, 17767, or b + p. The last one agrees with b modulo p but not modulo p^2.
- **Consistency with the tables:** q_p(2), q_p(3), q_p(7) and q_p(47) are each nonzero mod p. So p is not a Wieferich prime to any prime factor
  of b, which fits with p appearing in none of Fischer's rows for those bases.

### Absence from the Fischer tables (saved copies)

- **inputs/FermQ_Sort.txt:** I parsed 1011 base rows: the bases 2..1052 that are not perfect powers, plus 65537.
- **inputs/FermQ_Sorg.txt:** I parsed 10000 rows. As a sanity check on my parser, these are exactly the non-perfect-power bases 2..10125.
- Base 17766 has no row in either table.
- p appears in none of the four files in inputs/. I checked for it as an integer token, and also as a digit run after stripping every separator
  from each line.

### Saved files vs the scout's record

Each of the four files in inputs/ has the sha256 that status_sources.md records for it.

### Scope

This is a claim that one pair exists, not a claim that a search was exhaustive, so no sampling question arises. The one exhaustive step, the
trial division, covered its whole range.

## Transcript 1: checkers, controls and the author's checker

Run from claim/ with `bash ../panel/work-reproduce/run_all.sh`. The two `[time]` lines go to stderr and are the only lines that vary between
runs.

```
$ python3 --version
Python 3.14.7
[exit status 0]
$ node --version
v22.23.3
[exit status 0]

## 1. my checker (written before reading verify.py), three runs
run 1 exit status 0
run 2 exit status 0
run 3 exit status 0
$ python3 ../panel/work-reproduce/my_check.py .
[time] trial division of p: 0.056 s
[time] Lucas certificate: 0.002 s
object/pair.json sha256 = 0589225e4432f896e998643bcb654ccebd1a1ca8a1f0ac3c2923b42bca3a0dc1
object/pair.json bytes  = {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 17766, "p": 1016845912283}
PASS  object keys are exactly {target_id, partial_win, b, p} :: ['b', 'p', 'partial_win', 'target_id']
PASS  b and p are JSON integers (not str/float/bool) :: type(b)=int type(p)=int
PASS  target_id == wieferich-other-bases-fischer-table :: wieferich-other-bases-fischer-table
PASS  partial_win == p1 :: p1
PASS  claim.md p equals object p :: 1016845912283
PASS  claim.md b equals object b :: 17766
PASS  claim.md congruence is b^(p-1) == 1 mod p^2 for the same b, p :: 17766^1016845912282 ≡ 1 (mod 1016845912283^2)
PASS  claim.md target_id / partial win match object :: wieferich-other-bases-fischer-table / p1
PASS  10125 < b < 65537 :: b = 17766
PASS  p > 1e12 (exact integer compare with 10**12) :: p - 10**12 = 16845912283
factorisation of b: 2 * 3^3 * 7 * 47
PASS  product of factors == b
PASS  every factor of b is prime (trial division)
PASS  gcd of exponents == 1 (so b is not a perfect power) :: gcd = 1
PASS  brute force: no integer r, k >= 2 with r^k == b :: k tested 2..15, hits=[]
PASS  isqrt sanity: r^2 <= p < (r+1)^2 :: r = isqrt(p) = 1008387
PASS  PROOF 1: full trial division of p by every integer 2..isqrt(p) finds no divisor :: divisors tested = 1008386, divisors found = []
factorisation of p-1: 2 * 487 * 1043989643
PASS  product of factors == p-1
PASS  every factor of p-1 is prime (trial division)
PASS  PROOF 2: Lucas test - some a has a^(p-1)==1 and a^((p-1)/q)!=1 mod p for every prime q | p-1 :: witness a = 2
PASS  cross-check 3: strong probable prime to bases 2..37
PASS  p does not divide b :: b mod p = 17766, gcd = 1
p^2 = 1033975609326646530272089
pow(b, p-1, p^2) = 1
PASS  pow(b, p-1, p^2) == 1 exactly (builtin pow)
PASS  own square-and-multiply gives the same residue 1 :: residue = 1
PASS  equivalent form b^p == b mod p^2 :: b^p mod p^2 = 17766
Fermat quotient q_p(2) mod p = 445933708628   (exponent in b: 1)
Fermat quotient q_p(3) mod p = 15748556942   (exponent in b: 3)
Fermat quotient q_p(7) mod p = 449860086901   (exponent in b: 1)
Fermat quotient q_p(47) mod p = 73806445928   (exponent in b: 1)
PASS  sum over a|b of e_a*q_p(a) == 0 mod p  (re-derivation via factorisation) :: sum mod p = 0
PASS  none of q_p(a) is 0 for the prime factors a of b (so p is not a Wieferich prime to 2, 3, 7 or 47)
inputs/FermQ_Sort.txt sha256 = bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
FermQ_Sort.txt: 1011 base rows, min 2, max 65537, largest five [1049, 1050, 1051, 1052, 65537]
inputs/FermQ_Sorg.txt sha256 = 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
FermQ_Sorg.txt: 10000 base rows (lines 14..10013), min 2, max 10125
PASS  FermQ_Sorg.txt rows are exactly the non-perfect-power bases 2..10125 (sanity of my parser) :: 10000 rows vs 10000 expected
PASS  base b has no row in FermQ_Sort.txt
PASS  base b has no row in FermQ_Sorg.txt
PASS  p absent from inputs/FermQ_Sort.txt (as integer token; and as digit run with separators stripped) :: token hit=False, stripped-line hits=[]
      info: b=17766 appears as an integer token in FermQ_Sort.txt: False
PASS  p absent from inputs/FermQ_Sorg.txt (as integer token; and as digit run with separators stripped) :: token hit=False, stripped-line hits=[]
      info: b=17766 appears as an integer token in FermQ_Sorg.txt: False
PASS  p absent from inputs/ErstBasen.txt (as integer token; and as digit run with separators stripped) :: token hit=False, stripped-line hits=[]
      info: b=17766 appears as an integer token in ErstBasen.txt: False
PASS  p absent from inputs/ErstPBasen.txt (as integer token; and as digit run with separators stripped) :: token hit=False, stripped-line hits=[]
      info: b=17766 appears as an integer token in ErstPBasen.txt: False
SUMMARY: 33 checks, 0 failed
VERDICT (properties checkable from saved files): ALL PASS
[exit status 0]
92902ed8835fb2a1e358387a58723a7907e6d68849728055c8fe8454b4a9b714 *rerun_my_check.1.txt
92902ed8835fb2a1e358387a58723a7907e6d68849728055c8fe8454b4a9b714 *rerun_my_check.2.txt
92902ed8835fb2a1e358387a58723a7907e6d68849728055c8fe8454b4a9b714 *rerun_my_check.3.txt

## 2. controls
$ python3 ../panel/work-reproduce/controls.py .
control composite n = 1008379 * 1008401 = 1016850391979 ; smallest divisor found by the loop: 1008379
control: loop on p-1 finds 2 ; loop on p finds None
positive control from table row 2: p = 1093 -> b^(p-1) mod p^2 = 1
positive control from table row 2: p = 3511 -> b^(p-1) mod p^2 = 1
positive control from table row 5: p = 2 -> b^(p-1) mod p^2 = 1
positive control from table row 5: p = 20771 -> b^(p-1) mod p^2 = 1
positive control from table row 5: p = 40487 -> b^(p-1) mod p^2 = 1
positive control from table row 5: p = 53471161 -> b^(p-1) mod p^2 = 1
positive control from table row 5: p = 1645333507 -> b^(p-1) mod p^2 = 1
positive control from table row 5: p = 6692367337 -> b^(p-1) mod p^2 = 1
positive control from table row 5: p = 188748146801 -> b^(p-1) mod p^2 = 1
negative control: base 17765 with claimed p -> residue == 1 ? False
negative control: base 17767 with claimed p -> residue == 1 ? False
negative control: base 1016845930049 with claimed p -> residue == 1 ? False
note: base b + p shares b's residue mod p but not mod p^2, so it must NOT pass
perfect-power test: 17689 -> True
perfect-power test: 17576 -> True
perfect-power test: 16807 -> True
perfect-power test: 17766 -> False
[exit status 0]

## 3. second implementation (Node BigInt)
$ node ../panel/work-reproduce/node_check.js .
node: b = 17766  p = 1016845912283  p^2 = 1033975609326646530272089
node: b^(p-1) mod p^2 = 1 (== 1: Wieferich condition holds)
node: isqrt(p) = 1008387  divisors tested = 1008386  divisor found = none
node: factor(b) = 2 * 3 * 3 * 3 * 7 * 47  product = 17766
[exit status 0]

## 4. author's checker, exactly as REPRODUCE.md says, twice
$ python3 verify.py object/pair.json
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 17766, p = 1016845912283, Fermat quotient q_p(b) mod p = 0
PASS
[exit status 0]
7623d50c9a6d21341a9e483fd7e2c62270ce6ba13760150448128977ed7a4a7b *rerun_verify.1.txt
7623d50c9a6d21341a9e483fd7e2c62270ce6ba13760150448128977ed7a4a7b *rerun_verify.2.txt
$ python3 -c "p=1016845912283; print(pow(17766, p-1, p*p))"
1

## 5. saved inputs vs the hashes recorded in status_sources.md
$ sha256sum inputs/FermQ_Sorg.txt inputs/FermQ_Sort.txt inputs/ErstBasen.txt inputs/ErstPBasen.txt object/pair.json
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *inputs/FermQ_Sort.txt
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 *inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 *inputs/ErstPBasen.txt
0589225e4432f896e998643bcb654ccebd1a1ca8a1f0ac3c2923b42bca3a0dc1 *object/pair.json
[exit status 0]
sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4	(copy: inputs/FermQ_Sorg.txt)
sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b	(copy: inputs/FermQ_Sort.txt)
sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820	(copy: inputs/ErstBasen.txt)
sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362	(copy: inputs/ErstPBasen.txt)
```

## Comparison: my checkers vs verify.py

| property | my_check.py | node_check.js | verify.py |
|---|---|---|---|
| 10125 < b < 65537 | PASS (b = 17766) | not computed | ok |
| b not a perfect power | PASS: 2 · 3^3 · 7 · 47, exponent gcd 1, no r^k = b | factor(b) = 2 · 3 · 3 · 3 · 7 · 47 | ok |
| p above 1e12 | PASS: p − 10^12 = 16845912283 | not computed | ok |
| p prime | PASS, proven (trial division to 1008387; Lucas witness 2) | no divisor in 2..1008387 | ok (Miller-Rabin, bases 2..37) |
| p does not divide b | PASS: gcd 1 | not computed | ok |
| pow(b, p-1, p^2) | 1 (also b^p ≡ b; Fermat-quotient sum 0 mod p) | 1 | ok; q_p(b) mod p = 0 |
| absent from Fischer tables | PASS on inputs/ | not computed | not tested (REPRODUCE.md asks for a manual search) |
| repeat runs | 3 identical (stdout sha256 92902ed8…) | n/a | 2 identical (sha256 7623d50c…) |

No mismatch anywhere. REPRODUCE.md's stated outputs also reproduce: the last line of verify.py is PASS, and the one-liner prints 1.

## Review of verify.py (read after my checker had run)

- **Primality test.** verify.py uses Miller-Rabin with the 12 prime bases 2..37 and an explicit bound, 318665857834031151167461 (Jiang &
  Deng 2014). That is the correct published bound for those bases, and p is far below it. The code is the standard strong-probable-prime loop,
  with trial division by the base primes first. On its own this is a proof only by citing that theorem. My verdict does not depend on it,
  because the trial division and the Lucas certificate above prove primality by themselves.
- **Perfect-power test.** It takes floating-point k-th roots and checks the neighbours r−1, r and r+1. At this size (b = 17766, k up to 15)
  that is sound, and it agrees with my exact factorisation.
- **Input types.** It reads b and p through int(), so it would also accept strings in the JSON. That is not an issue here: my checker
  confirmed the object holds JSON integers.
- **Absence checks.** verify.py does not test absence from the tables or OEIS. REPRODUCE.md leaves that to a manual search. My checker did
  that search on inputs/, and the live re-check is below.

## Transcript 2: supplementary live re-check

Read-only GETs, run from claim/ with `bash ../panel/work-reproduce/live_check.sh`.

```
fetch time (UTC): 2026-11-07T18:40:34Z
GET fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt -> HTTP 200, 288459 bytes
   live sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 ; inputs/FermQ_Sorg.txt sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 ; IDENTICAL
GET fermatquotient.com/FermatQuotienten/FermQ_Sort.txt -> HTTP 200, 33141 bytes
   live sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b ; inputs/FermQ_Sort.txt sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b ; IDENTICAL
GET fermatquotient.com/FermatQuotienten/ErstBasen.txt -> HTTP 200, 115771 bytes
   live sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 ; inputs/ErstBasen.txt sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 ; IDENTICAL
GET fermatquotient.com/FermatQuotienten/ErstPBasen.txt -> HTTP 200, 81696 bytes
   live sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 ; inputs/ErstPBasen.txt sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 ; IDENTICAL
grep -w for 17766 or 1016845912283 in the four live files:
   grep exit status 1 (1 = no match)
GET oeis.org/search?q=1016845912283&fmt=data -> HTTP 200, 6737 bytes
   page text: Search: 1016845912283
   page text: Sorry, but the terms do not match anything in the table.
   page text: Last modified November 7 13:12 EST 2026. Contains 401120 sequences.
   A-number links in page: []
```

**Fischer files.** All four are byte-identical to the copies in inputs/ as of this fetch. The saved copies are the live tables.

**OEIS.** The search for p returns "Sorry, but the terms do not match anything in the table." and links no A-number, matching the scout's
record. Two caveats:

- claim/ holds no saved copy of the OEIS page. This clause rests on the scout's record plus my live re-query, not on saved files alone.
- Nobody can reproduce the OEIS response sha256 recorded in status_sources.md, because the page embeds a per-request token. Two of my own
  fetches 20 s apart differ only in that one line:

```
$ sha256sum ../panel/work-reproduce/live/oeis_data.txt ../panel/work-reproduce/live/oeis_data_2.txt   # two of my fetches of the same OEIS URL, 20 s apart
2d9829da8f35763243f080c6a34c0ddb578b99d96fcd535053be486f0ba875fc *../panel/work-reproduce/live/oeis_data.txt
9531e18df8b37fc72f781bb2025555482a1b263542cc0cd63a03d5aa173acdc4 *../panel/work-reproduce/live/oeis_data_2.txt
$ diff ../panel/work-reproduce/live/oeis_data.txt ../panel/work-reproduce/live/oeis_data_2.txt | grep -E "^[0-9]"   # which lines differ
192c192
$ grep -o "r:'[0-9a-f]*'" (the per-request Cloudflare ray id in that line)
../panel/work-reproduce/live/oeis_data.txt:r:'a56e73a6ab1be17d'
../panel/work-reproduce/live/oeis_data_2.txt:r:'a56e74f84d73e1ed'
```

Only the hash changes, not the content: the quoted sentence reproduces. Absence from OEIS is in any case mainly the novelty skeptic's call.

## Integrity of claim/ after all runs

```
$ find . -type f | sort | xargs sha256sum   # claim/ after every run above, compared with the listing taken before any run
eacba7deb1fb56b7f6670ae2ec5d180602f51e9beaa88b1189395450436c0d09 *./claim.md
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 *./inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 *./inputs/ErstPBasen.txt
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *./inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *./inputs/FermQ_Sort.txt
0589225e4432f896e998643bcb654ccebd1a1ca8a1f0ac3c2923b42bca3a0dc1 *./object/pair.json
b0c0da7a101ea5c907c76d687afc252659be7dd62c1ee27f17265e404d55945d *./REPRODUCE.md
6c97d82378998ae88a8cec27b6ec51853e2d95f9fb8e016a36497e403ae13dae *./status_sources.md
304ca8e82b9c0437ae4a087d287857c5197453995ebcc313de093a1ec9e2a2fc *./verify.py
cmp: identical to the pre-run listing (claim/ unchanged)
__pycache__ directories under claim/: 0
$ sha256sum (my scratch scripts, relative to claim/)
e815ceb990660e210c4465d20694c6f872a18043114652e6afc111de8afd7048 *../panel/work-reproduce/my_check.py
e8db133cdbec137d7414ecc532dc9bafbd6fafdefc22f86df55c497642d25085 *../panel/work-reproduce/controls.py
b2ab0e45a12962776938af20f7f2ffa30b0cca60e02cab108f21a81ae98b183a *../panel/work-reproduce/node_check.js
665d1453035e4bffd252af5845d77ad24e837c3834c923adc84fa208541c0ad6 *../panel/work-reproduce/run_all.sh
a45a20dd6b43f71614ac3092c39bd613a552e94751e2cdc49cd92d08e3054994 *../panel/work-reproduce/live_check.sh
```

## Verdict

From the saved object and inputs, every property of the p1 criterion reproduces exactly:

- 10125 < b < 65537;
- b is not a perfect power;
- p is above 1e12;
- p is a proven prime;
- p does not divide b;
- b^(p-1) == 1 mod p^2, checked exactly;
- the pair is absent from both saved Fischer tables.

I found no mismatch between claim.md, object/pair.json, REPRODUCE.md, the hashes in status_sources.md, verify.py and my own checkers. No
object is missing, and every run is deterministic. The OEIS clause reproduces live, though no saved copy of that page exists.

pass: true
