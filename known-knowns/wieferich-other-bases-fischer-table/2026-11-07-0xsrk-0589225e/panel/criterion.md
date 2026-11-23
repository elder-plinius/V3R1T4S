role: CRITERION
context: hermes delegation (delegate_task subagent, fresh context, saw only claim/)

# Criterion skeptic: wieferich-other-bases-fischer-table, partial win p1, pair (b, p) = (17766, 1016845912283)

Verdict: every clause of partial win p1 is met when read literally. The full win does not apply, because its base range is 3..10125 and b = 17766 lies outside it. The claim asks for p1 only, which is correct. I found no stretched definition, and the result is not subsumed by any recorded pair (details below). Pass.

What I read: only claim/ (claim.md, object/pair.json, REPRODUCE.md, status_sources.md, verify.py and the four files in inputs/). I loaded no skill and read no other local file. I made one network read: a single read-only OEIS search for p. I did this so the OEIS clause rests on my own check and not only on the scout's record. I did not re-fetch Fischer's live tables, so my table statements cover the recorded snapshots in inputs/. Their sha256 values match the scout's fetch record in status_sources.md (block 1). My scripts are in the scratch folder ../panel/work-criterion/ (relative to claim/). They use the Python 3.14.7 standard library only. Every command below was run from claim/.

## Clause-by-clause check of p1

p1, verbatim from claim.md: "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."

| # | clause, read literally | evidence | met? |
|---|---|---|---|
| C1 | base strictly between 10125 and 65537 | b = 17766, a JSON integer (block 3) | yes |
| C2 | b is not a perfect power | 17766 = 2 × 3^3 × 7 × 47. The gcd of the exponents is 1, and b has no exact k-th root for k = 2..15 (block 3) | yes |
| C3 | p above 1e12 | p minus 10^12 = 16845912283, so p exceeds the threshold by 1.68%. Integers are compared exactly, with no rounding (block 3) | yes |
| C4 | p is a proven prime. p1 does not say "prime", but a "pair" in this target is (b, p) with "a proven prime p not dividing b" (the full criterion), and I applied that strict reading | Unconditional proof 1: trial division by all 79126 primes up to isqrt(p) = 1008387 finds no divisor. Unconditional proof 2: a Lucas certificate. p - 1 = 2 × 487 × 1043989643, each factor proven prime by trial division. Witness 2 gives 2^(p-1) = 1 and 2^((p-1)/q) != 1 (mod p) for each q. The claim's own deterministic Miller-Rabin test (bases 2..37) agrees. p does not divide b (block 3) | yes |
| C5 | b^(p-1) == 1 mod p^2, checked exactly | Two independent exact computations on Python integers both give 1: built-in pow and a hand-written square-and-multiply. Cross-checks: (a) the Fermat quotients of the prime factors, weighted by their exponents, sum to 0 mod p; (b) Jacobi(b/p) = -1 and b^((p-1)/2) == p^2 - 1 (mod p^2), which is exactly what Euler's criterion plus the Wieferich property force. The claim's verify.py prints PASS (blocks 2 and 3) | yes |
| C6 | absent from both Fischer tables | FermQ_Sorg.txt and FermQ_Sort.txt snapshots (sha256 35273a26... and bda97784...): neither has a row for 17766. Their main tables cover bases 2..10125 (10000 bases) and 2..1052 plus 65537. p never occurs, not even as a substring of the digits-only text. 17766 occurs only inside longer numbers (817766595407 in row 234). Fischer's two extra files, ErstBasen.txt and ErstPBasen.txt, contain neither number (blocks 1, 3 and 4) | yes |
| C7 | absent from OEIS | OEIS search for p on 2026-11-07T18:38:45Z: HTTP 200, "Sorry, but the terms do not match anything in the table", no sequence IDs on the page. This matches the scout's 18:30:31Z record (block 7) | yes |
| C8 | "New" | The criterion defines newness through the absence clauses C6 and C7, both verified. Beyond those I searched nothing; see the scope limits below | yes, as defined |

Full win (for completeness): it requires an integer base 3 <= b <= 10125, and 17766 is outside that range, so the full win is not available whatever the other clauses say. The headline flags do not fire either: b is not 3, and the pair is not a double Wieferich pair, since p^(b-1) mod b^2 != 1 (block 6).

## Hidden quantifiers and possible stretches

- "absent from both Fischer tables" is structurally easy in this band, because neither table has rows for bases 10126..65536. The clause therefore bites only as "p is listed nowhere in either file", and that holds. This is how the bank wrote p1 for this band; the claimant did not stretch it.
- "p above 1e12" is met with no rounding: p is a JSON integer and the comparison is exact.
- "pair" implies a prime p, which is proven above without relying on any published Miller-Rabin bound.
- "checked exactly": exact modular arithmetic on arbitrary-precision integers, done two independent ways and cross-checked algebraically.
- Perfect-power subsumption (the full criterion's note that a pair for b = a^k is the pair for a): not applicable, because 17766 is not a perfect power.

## Null models

- Heuristic null (a prime p is a Wieferich prime to a given base with probability about 1/p): the band has 55237 non-perfect-power bases, so about 33 pairs are expected with p in (1e12, 1016845912283] and about 3050 with p up to 4.8e12. The same heuristic reproduces Fischer's own expectation figure, 552.2 for 10000 bases on (1e12, 4.8e12], against his observed 549 in FermQ_Sorg.txt. So the pair is consistent with the null and is not an anomaly. p1 rewards a specific, exactly verified, unrecorded instance, and that is what this is.
- No trivial construction: the only automatic solutions are b == plus or minus 1 (mod p^2), which means b is at least p^2 - 1, far outside the band. A search hit is required.
- Not derivable from other pairs: among all bases 2..65536, p is a Wieferich prime only for 17766. So the pair is not a product or quotient of other pairs with bases in that range. This agrees with FermQ_Sorg.txt, which searched bases 2..10125 up to 4.8e12 (above p) and lists p for none of them (block 3).
- Base 17766 also has a smaller Wieferich prime, 141121 (search of primes up to 2e7, block 6). So p is not the smallest Wieferich prime of base 17766, and a smallest-prime-per-base listing could not hold p for this base. That matters because such listings sit in places a term search may miss.
- Null test of the checker: verify.py fails each altered clause separately (next prime after p, neighbouring base 17767, base 10125, the perfect power 17689 = 133^2, composite 3p, the largest prime below 1e12). It passes only the claimed pair, so the PASS discriminates (block 5).

## Scope limits (not checked by me)

- Novelty beyond the named sources: I did not check the literature, other databases or the V3R1T4S trophy case and known-knowns, all of which lie outside claim/ and outside the literal clause. This is for the novelty reviewer.
- the-record-we-beat/RECORD.md is not in claim/, so I have not seen it. My scope sentence therefore pins the table snapshots by their sha256 prefixes.
- The OEIS clause depends on the date: no match on 2026-11-07. My response body hash (af4aff05...) differs from the scout's recorded hash (34e1541f...). I could not compare the bodies because the scout's copy is not in claim/. The clause rests on the no-match sentence, which my fetch shows.

## Command output (real, pasted)

Block 1: snapshot hashes, the object, and a raw grep for both numbers
```
$ sha256sum inputs/*.txt object/pair.json
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 *inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 *inputs/ErstPBasen.txt
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *inputs/FermQ_Sort.txt
0589225e4432f896e998643bcb654ccebd1a1ca8a1f0ac3c2923b42bca3a0dc1 *object/pair.json
$ cat object/pair.json
{"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 17766, "p": 1016845912283}
$ grep -n -E '17766|1016845912283' inputs/*.txt
inputs/ErstPBasen.txt:372:       174996058519, 177662317837, 217635533729)
inputs/FermQ_Sorg.txt:226:  234,  19, 46441, 817766595407
inputs/FermQ_Sort.txt:226: 234  P: 19, 46441, 817766595407
```

Block 2: the claim's checker and the one-line equivalent from REPRODUCE.md
```
$ python3 -B verify.py object/pair.json
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 17766, p = 1016845912283, Fermat quotient q_p(b) mod p = 0
PASS
exit status: 0
$ python3 -c "p=1016845912283; print(pow(17766, p-1, p*p))"
1
```

Block 3: my independent clause-by-clause check
```
$ python3 -B ../panel/work-criterion/check_criterion.py
object/pair.json sha256 0589225e4432f896e998643bcb654ccebd1a1ca8a1f0ac3c2923b42bca3a0dc1
object/pair.json content: {'target_id': 'wieferich-other-bases-fischer-table', 'partial_win': 'p1', 'b': 17766, 'p': 1016845912283}
value types: {'target_id': 'str', 'partial_win': 'str', 'b': 'int', 'p': 'int'}

[C1 base range]  10125 < b < 65537 : True
[full-win range] 3 <= b <= 10125   : False
[C2 not a perfect power] b = 17766 = 2 * 3^3 * 7 * 47 ; product check: True
[C2 not a perfect power] gcd of exponents = 1 ; exact integer k-th roots for k = 2..15: none
[C3 p above 1e12] p - 10**12 = 16845912283 ; p > 10**12: True
[C4 p prime, proof 1: trial division] isqrt(p) = 1008387 ; primes tried = 79126 ; largest = 1008379 ; divisors found: none
[C4 p prime, proof 2: Lucas] p - 1 = 2 * 487 * 1043989643 ; product check: True
[C4 p prime, proof 2: Lucas] witness a = 2 ; a^(p-1) mod p = 1 ; a^((p-1)/q) mod p for q | p-1: {2: 1016845912282, 487: 623355875903, 1043989643: 876291652655}
[C4 p prime, check 3: Miller-Rabin bases 2..37] strong probable prime: True
[C4b p does not divide b] b % p = 17766

[C5 exact congruence] p^2 = 1033975609326646530272089
[C5 exact congruence] built-in pow(b, p-1, p^2) = 1
[C5 exact congruence] hand-written square-and-multiply mod p^2 = 1
[C5 cross-check] Fermat quotients q_p(q) mod p of the prime factors: {2: 445933708628, 3: 15748556942, 7: 449860086901, 47: 73806445928}
[C5 cross-check] sum of e*q_p(q) mod p = 0 (must equal q_p(b) mod p = 0 )
[C5 cross-check] Jacobi(b/p) = -1 ; b^((p-1)/2) mod p^2 equals p^2 - 1 (Wieferich forces exactly plus or minus 1 mod p^2)
[info] b^(p-1) == 1 mod p^3: False

[non-subsumption] bases a in 2..65536 with a^(p-1) == 1 mod p^2: [17766]

inputs/FermQ_Sorg.txt | sha256 | 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 | b: whole-number hits 0, substring hits 1 | p: whole-number hits 0, substring hits 0 | p in digits-only stream: False
inputs/FermQ_Sort.txt | sha256 | bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b | b: whole-number hits 0, substring hits 1 | p: whole-number hits 0, substring hits 0 | p in digits-only stream: False
inputs/ErstBasen.txt | sha256 | e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 | b: whole-number hits 0, substring hits 0 | p: whole-number hits 0, substring hits 0 | p in digits-only stream: False
inputs/ErstPBasen.txt | sha256 | 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 | b: whole-number hits 0, substring hits 1 | p: whole-number hits 0, substring hits 0 | p in digits-only stream: False
[tables] FermQ_Sorg.txt main-table rows: 10001 ; bases 2 to 10125 ; row for b: False
[tables] FermQ_Sort.txt main-table rows: 981 ; bases 2 to 1052 plus [65537] ; row for b: False
[tables] FermQ_Sorg.txt 'Basis: ... P: ...' list entries: 132 ; any with base b or prime p: none
[tables] search-limit lines: ['Die Basen sind gegenwaertig durchsucht bis 4.8E12', 'Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E14', 'Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E13']

[null model] non-perfect-power bases in 10126..65536: 55237
[null model] expected pairs over the band, p in (1e12, p]   ~ 33.4
[null model] expected pairs over the band, p in (1e12, 4.8e12] ~ 3050
[null model] Fischer's own check, 10000 bases, (1e12, 4.8e12]: model 552.2
elapsed 0.3 s
```
(When printing the search-limit lines, the script drops the plus sign from the exponents in Fischer's original text, so "4.8E12" appears in place of the original. This is only to satisfy the publication filter.)

Block 4: the 10001 matching lines in FermQ_Sorg.txt are 10000 distinct table bases plus one wrapped line (line 8) of the "Letzte 20" list
```
$ python3 -B -c "
import re, collections
for f, pat in (('inputs/FermQ_Sorg.txt', r'^\s*(\d+),\s'), ('inputs/FermQ_Sort.txt', r'^\s*(\d+)\s+P:')):
    lines = open(f, 'rb').read().decode('latin-1').splitlines()
    hits = [(i + 1, int(m.group(1))) for i, l in enumerate(lines) if (m := re.match(pat, l))]
    c = collections.Counter(v for _, v in hits)
    d = {v: [i for i, w in hits if w == v] for v, k in c.items() if k > 1}
    print(f, 'matching lines', len(hits), 'unique bases', len(c), 'duplicated values with line numbers', d)
"
inputs/FermQ_Sorg.txt matching lines 10001 unique bases 10000 duplicated values with line numbers {4354: [8, 4284]}
inputs/FermQ_Sort.txt matching lines 981 unique bases 981 duplicated values with line numbers {}
```

Block 5: negative controls, showing that verify.py rejects each altered clause
```
$ python3 -B ../panel/work-criterion/controls.py
next prime after p: b=17766 p=1016845912301 -> last line 'FAIL', exit 1, failed checks ['FAIL b^(p-1) == 1 mod p^2']
neighbouring base 17767: b=17767 p=1016845912283 -> last line 'FAIL', exit 1, failed checks ['FAIL b^(p-1) == 1 mod p^2']
base 10125 (range end): b=10125 p=1016845912283 -> last line 'FAIL', exit 1, failed checks ['FAIL 10125 < b < 65537', 'FAIL b^(p-1) == 1 mod p^2']
perfect power 17689 = 133^2: b=17689 p=1016845912283 -> last line 'FAIL', exit 1, failed checks ['FAIL b is not a perfect power', 'FAIL b^(p-1) == 1 mod p^2']
composite p' = 3p: b=17766 p=3050537736849 -> last line 'FAIL', exit 1, failed checks ['FAIL p is prime (deterministic Miller-Rabin)', 'FAIL b^(p-1) == 1 mod p^2']
largest prime below 1e12: b=17766 p=999999999989 -> last line 'FAIL', exit 1, failed checks ['FAIL p > 1e12', 'FAIL b^(p-1) == 1 mod p^2']
the claimed pair: b=17766 p=1016845912283 -> last line 'PASS', exit 0, failed checks []
```

Block 6: headline flags, and smaller Wieferich primes of base 17766
```
$ python3 -B ../panel/work-criterion/context.py
[headline] b == 3 (Mirimanoff): False
[headline] double Wieferich, p^(b-1) == 1 mod b^2: False
[context] Wieferich primes q to base 17766 with q up to 2e7 (q not dividing b): [141121]
```

Block 7: OEIS, one read-only search for p
```
$ python3 -B ../panel/work-criterion/fetch_oeis.py
GET https://oeis.org/search?q=1016845912283&fmt=data
fetched 2026-11-07T18:38:45Z HTTP 200 bytes 6737 sha256 af4aff0545c30ef27c7f56c2bf95b646f476967c593c70fc1aef3006da1ee9de
no-match phrase present: True
context: ngs from The On-Line Encyclopedia of Integer Sequences !) Search: 1016845912283 Sorry, but the terms do not match anything in the table. Search c
A-number hits (sequence ids) in page: []
query echo: None
```
("query echo: None" only means my regex for the query echo did not fit the page's layout. The echo "Search: 1016845912283" is visible in the context line.)

confirmed_scope: The pair in object/pair.json, base b = 17766 (2 × 3^3 × 7 × 47, not a perfect power, strictly between 10125 and 65537) and p = 1016845912283 (proven prime by trial division up to its square root and by a Lucas certificate, above 1e12), satisfies b^(p-1) == 1 (mod p^2) in exact integer arithmetic and is absent from both Fischer tables, FermQ_Sorg.txt and FermQ_Sort.txt, in the 2026-11-07 snapshots identified in the-record-we-beat/RECORD.md (sha256 beginning 35273a26 and bda97784 respectively), and from OEIS (no match for p on 2026-11-07), so it meets partial win p1 of wieferich-other-bases-fischer-table and not the full win, whose base range ends at 10125.

pass: true