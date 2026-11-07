role: CRITERION
context: claude code Task subagent (fresh context, saw only claim/)

# CRITERION seat: pair (28910, 1011548897263), target wieferich-other-bases-fischer-table

Verdict: the pair meets partial win **p1** literally, clause by clause. The **full win does not apply**: its base range is
3 <= b <= 10125 and b = 28910.

## What I read, what I ran
- Read only claim/: claim.md, object/pair.json, verify.py, REPRODUCE.md, status_sources.md, inputs/ (4 files). No skill
  loaded, no other workspace file opened.
- Own code, standard library only, written from scratch (no code shared with claim/verify.py), in
  panel/work-criterion/: criterion_check.py (arithmetic clauses), tables_and_controls.py (table absence, positive and
  negative controls, null count), compare_criterion.py (live bank text), scan_pulls.py, small_wieferich.py. Every output
  below was saved with `2>&1 | tee` next to these scripts. Python: `3.14.7 (tags/v3.14.7:823f032, Aug  5 2026, 10:51:32) [MSC v.1944 64 bit (AMD64)]`.
- Network: one request per source, honest User-Agent `V3R1T4S-agent/1.0 (open-research notebook; one honest request)`,
  no retry, no outward action: the V3R1T4S repository's bank/targets.json on branch main (raw.githubusercontent.com),
  https://oeis.org/search?q=1011548897263&fmt=data, Fischer's FermQ_Sorg.txt and FermQ_Sort.txt, and the GitHub API
  pulls listing of the V3R1T4S repository (state=all, sort=created, direction=desc, per_page=100).
- In pasted output, the run-folder prefix of local file paths was stripped with sed; paths are relative to the run
  folder.

```
targets_json fetch_utc 2026-11-07T15:59:57Z
200 <- http_code targets.json
oeis_search fetch_utc 2026-11-07T16:00:32Z
200 <- http_code oeis search q=1011548897263
FermQ_Sorg fetch_utc 2026-11-07T16:00:54Z
200 <- http_code FermQ_Sorg.txt
FermQ_Sort fetch_utc 2026-11-07T16:00:54Z
200 <- http_code FermQ_Sort.txt
v3r1t4s_pulls fetch_utc 2026-11-07T16:01:10Z
200 <- http_code V3R1T4S pulls (state=all, newest 100)
```

## 1. The criterion quoted in claim.md is the live bank text
```
targets.json: 6189749 bytes, sha256 c2ee5ddad1634104acc41512e052dd4ab2c3af70d26cae8bc82f3af0bf6be65e
top-level type dict; entries 1116; entries with id 'wieferich-other-bases-fischer-table': 1
--- partial_wins: [{"id": "p1", "statement": "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."}, {"id": "p2", "statement": "Range certificate: one base b <= 1052 extended contiguously from its stated limit by at least 20%, with Fermat quotients q_p(b) mod p published in hashed blocks and surviving a random 1% recomputation by the verifier."}]
--- status_source: "http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt"
--- verification_method: "Prove p prime (BPSW plus PARI isprime). Check pow(b, p-1, p*p) == 1 with Python big integers. Read the base's row and the stated limit lines in the live Fischer file (latin-1 text) and check that p is greater and absent. For double pairs, also check pow(p, b-1, b*b) == 1."
claim.md p1 text found verbatim as a string inside the live entry: True; as a substring of some string: True
claim.md full-criterion text found verbatim as a string inside the live entry: True; as a substring of some string: True
```
The bank's own statement and pitfalls fix what "both Fischer tables" means and why 65537 is excluded:
```
--- kind: "harvest"
Base 65537 appears in FermQ_Sort.txt with its own limit (1.2e14 on 2026-10-30)."
p dividing b is trivially excluded.
maintains two tables. The first, FermQ_Sort.txt, covers bases 2 to 1052.
The second, FermQ_Sorg.txt, covers bases 2 to 10125, all searched to 4.
```

## 2. Clause by clause (p1)
| clause of p1 (live text) | evidence (own code unless stated) | result |
|---|---|---|
| New pair ... | operational test in the text is the absence clause below; also not in the newest 100 V3R1T4S PRs (section 6) | met |
| for a base 10125 < b < 65537 (strict) | b = 28910; b - 10125 = 18785; 65537 - b = 36627 | met |
| that is not a perfect power | 28910 = 2 * 5 * 7^2 * 59, gcd of exponents 1; no exact integer k-th root for k = 2..15 | met |
| with p above 1e12 (strict) | p - 10^12 = 11548897263 > 0 | met |
| p a proven prime (the target's notion of a pair) | trial division by 2 and every odd d up to isqrt(p) = 1005757 (502879 divisions, no divisor); independent Lucas certificate: p - 1 = 2 * 3^2 * 15937 * 3526207, witness a = 3 | met |
| p not dividing b (target definition and pitfalls) | p > b | met |
| b^(p-1) == 1 mod p^2 checked exactly | four exact routes agree: built-in pow, own square-and-multiply, additivity over the prime factors of b (sum = 0 mod p), b^((p-1)/2) == +1 mod p^2 equal to the Legendre symbol (b/p) = 1 from reciprocity | met |
| absent from both Fischer tables | no row for 28910 in either file; p and 28910 occur nowhere in either file (nor in Fischer's two extra files in inputs/); live files re-fetched at 16:00:54Z are byte-identical to the snapshot | met |
| absent from OEIS | OEIS search for p at 16:00:32Z: "Sorry, but the terms do not match anything in the table.", 0 A-numbers on the page | met |

Full success criterion: **not met**, and not claimed. It needs 3 <= b <= 10125; b = 28910. The pair is also not a
Mirimanoff prime (b != 3) and not a double Wieferich pair (p^(b-1) mod b^2 = 535037323, not 1).

## 3. Arithmetic, own code (criterion_check.py)
```
pair.json fields: {'target_id': 'wieferich-other-bases-fischer-table', 'partial_win': 'p1', 'b': 28910, 'p': 1011548897263}
b = 28910; b - 10125 = 18785; 65537 - b = 36627
factorisation of b: 2 * 5 * 7^2 * 59 | product check: True
gcd of exponents = 1; exact integer k-th roots of b for k = 2..15: []
p = 1011548897263; p - 10^12 = 11548897263
trial division proof: isqrt(p) = 1005757 (r^2 <= p < (r+1)^2: True), tested 2 and every odd d in 3..1005757 (502879 divisions, expected 502879): smallest divisor found = None (0.015 s)
p - 1 = 2 * 3^2 * 15937 * 3526207 | product check: True | every factor prime: True
Lucas certificate: smallest a with a^(p-1) = 1 mod p and a^((p-1)/q) != 1 mod p for all q | p-1: a = 3
route A, built-in pow(b, p-1, p^2) = 1
route B, own square-and-multiply b^(p-1) mod p^2 = 1
route C, additivity: q_p(r) mod p for prime factors r of b: {2: 749604166799, 5: 252643161267, 7: 9495223617, 59: 1001860019226} | sum of e_r * q_p(r) mod p = 0
route D, b^((p-1)/2) mod p^2 is +1; Jacobi/Legendre symbol (b/p) by reciprocity = 1
22 proper divisors d of b (1 < d < b): [2, 5, 7, 10, 14, 35, 49, 59, 70, 98, 118, 245, 295, 413, 490, 590, 826, 2065, 2891, 4130, 5782, 14455]
proper divisors d with d^(p-1) == 1 mod p^2: []
full win base range 3 <= b <= 10125 holds: False
p > 4.8E+12 (Fischer's searched limit for bases 1053..10125): False
double Wieferich check p^(b-1) mod b^2 = 535037323 (1 would be a double pair)
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (trial division proof)
ok   p is prime (Lucas certificate, independent)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2 (route A)
ok   b^(p-1) == 1 mod p^2 (route B)
ok   sum of e_r*q_p(r) == 0 mod p (route C)
ok   b^((p-1)/2) == (b/p) mod p^2 (route D)
ok   no proper divisor of b is a Wieferich base for p
ok   b mod p^2 not in {1, p^2-1}
ALL_P1_ARITHMETIC_CLAUSES PASS
```
The bank's verification_method names BPSW plus PARI isprime. PARI is not installed here. The proof above is
unconditional instead: complete trial division to isqrt(p), confirmed by a separate Lucas certificate.

## 4. Absence from both Fischer tables (tables_and_controls.py, and the live re-fetch)
Hashes of the claim's copies match the scout's records in claim/status_sources.md:
```
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 claim/inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 claim/inputs/ErstPBasen.txt
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 claim/inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b claim/inputs/FermQ_Sort.txt
9f39532bfc7ab17685cc172f0e2ff2ca917a21bc1f5a51ba702cddb75e644383 claim/object/pair.json
```
Parsed tables and the search for b and p:
```
FermQ_Sorg.txt main table: lines 14..10013, 10000 base rows, bases 2..10125, 31606 (b, p) entries; row set == non-perfect-powers 2..10125: True
FermQ_Sorg.txt 'Basis: b  P: p' lines after the table: 132, bases 220..10017
FermQ_Sort.txt: 1011 base rows, bases 2..1052 plus 65537, 3367 (b, p) entries, 30 rows 'keine gefunden'; row set == non-perfect-powers 2..1052 plus 65537: True
base 28910 has a row in FermQ_Sorg.txt: False; in FermQ_Sort.txt: False
bases whose row lists p = 1011548897263: FermQ_Sorg.txt [], FermQ_Sort.txt [], FermQ_Sorg.txt 'Basis:' lines []
FermQ_Sorg.txt: 44745 digit runs; substring '1011548897263': 0; with thousands separators: 0; digit runs equal to p: 0; prefix '1011548897': 0; '28910' as a number (with or without separator): 0; digit runs equal to b: 0
FermQ_Sort.txt: 4707 digit runs; substring '1011548897263': 0; with thousands separators: 0; digit runs equal to p: 0; prefix '1011548897': 0; '28910' as a number (with or without separator): 0; digit runs equal to b: 0
ErstBasen.txt: 10379 digit runs; substring '1011548897263': 0; with thousands separators: 0; digit runs equal to p: 0; prefix '1011548897': 0; '28910' as a number (with or without separator): 0; digit runs equal to b: 0
ErstPBasen.txt: 7315 digit runs; substring '1011548897263': 0; with thousands separators: 0; digit runs equal to p: 0; prefix '1011548897': 0; '28910' as a number (with or without separator): 0; digit runs equal to b: 0
```
The live tables, fetched once each at 16:00:54Z, are byte-identical to that snapshot:
```
288459 panel/work-criterion/fetched/FermQ_Sorg.txt
 33141 panel/work-criterion/fetched/FermQ_Sort.txt
321600 total
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 panel/work-criterion/fetched/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b panel/work-criterion/fetched/FermQ_Sort.txt
--- byte-identical to the claim's inputs/ copies? ---
FermQ_Sorg.txt identical
FermQ_Sort.txt identical
--- limit lines in the live files ---
panel/work-criterion/fetched/FermQ_Sorg.txt:11:Die Basen sind gegenwaertig durchsucht bis 4.8E+12
panel/work-criterion/fetched/FermQ_Sort.txt:9:Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
panel/work-criterion/fetched/FermQ_Sort.txt:10:Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
```
No stated limit applies to base 28910, because neither file has a row for it. p1 asks only for p > 1e12, not for p above
a table limit.

## 5. Absence from OEIS (one search for p)
```
bytes: 6737
68b345c0bec1a122446f9c0e848a4f91a66de450c5f195cf5ebe69f5e40d16ad panel/work-criterion/fetched/oeis_search_p.html
--- lines containing 'Sorry' / 'match' / 'result' / 'Search:' (tags stripped) ---
 Search: 1011548897263 
 Sorry, but the terms do not match anything in the table. 
--- count of A-numbers (A followed by 6 digits) in the page ---
0
--- occurrences of the digits of p in the page ---
6
line numbers holding p: 15 22 38 53 78 101 
element markers on those lines:
15:<title>
22:myURL
26:myURL
38:login?redirect
53:alt="1011548897263
78:name=q value="1011548897263"
101:LTR">Search:
```
All six occurrences echo the query: the page title, the page's own URL variable, the login link, the banner's alt text,
the search box and the "Search:" label. Line 26 reuses the URL variable and holds no p. The raw lines are in
panel/work-criterion/oeis_check_output.txt. My page hash differs from the scout's 15:49Z hash, as expected for a dynamic
page.
Both searches report no match. OEIS search does not index b-files. The only kind of b-file that could hold this pair is
a "smallest Wieferich prime to base n" sequence, and base 28910 has smaller Wieferich primes, so no such entry can be p
(small_wieferich.py):
```
base 28910: 5761455 primes q <= 100000000 tested; Wieferich primes q (q not dividing b): [11, 30307, 73194013]; heuristic expected count sum(1/q) = 2.315; 23.1 s
```

## 6. Not subsumed
- **Not the full win** (b > 10125), so p1 is the correct, narrowest claim level. The claim names p1.
- **Not derived from a smaller pair by additivity.** None of the 22 proper divisors d of b has d^(p-1) == 1 mod p^2,
  so b is not a product of two Wieferich bases for p. Every base-d pair with d <= 10125 and this p would also sit below
  Fischer's 4.8E+12 limit, and p occurs nowhere in his files, which is consistent.
- **Not trivial.** b mod p^2 is neither 1 nor p^2 - 1, and p does not divide b.
- **Not already claimed in V3R1T4S** (newest 100 pull requests, #871..#982):
```
pull requests in listing: 100; numbers 871..982; created 2026-10-31T13:36:55Z .. 2026-11-07T15:36:50Z
pull requests whose title, body or branch name contains p = 1011548897263: []
pull requests whose title, body or branch name contains b = 28910 as a number: []
pull requests mentioning Wieferich, Fermat quotient or Fischer: 1
   (973, 'open', True, '[claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partia')
```
  p1 is stated per pair ("New pair for a base ..."), in a target of kind "harvest". This pair differs from the only other
  Wieferich claim (#973, pair (24766, 1000747824697)), so that claim does not subsume it.

## 7. Hidden quantifiers and stretched definitions, checked
- **"both Fischer tables".** The bank's statement defines them as FermQ_Sort.txt (bases 2..1052) and FermQ_Sorg.txt
  (bases 2..10125). The claim uses exactly these two. ErstBasen.txt and ErstPBasen.txt were checked as well; p and b
  occur in neither.
- **"absent" holds structurally.** Neither table has a row for any base in 10126..65536 (row sets verified above). p1 is
  defined by the bank for exactly that base range, so this is the clause's intended reading, not a stretch. I also
  checked the stronger reading, "p appears nowhere in either file", and it holds.
- **Strict inequalities.** 10125 < b < 65537 and p > 1e12 hold strictly, with margins 18785, 36627 and 11548897263.
  65537 is excluded on purpose (pitfall: it has its own row in FermQ_Sort.txt).
- **"pair" implies a prime p.** p is proven prime unconditionally, with no probabilistic step.
- **"checked exactly".** Exact integer arithmetic, four routes. No floating point is involved in any decision; the
  perfect-power test uses integer roots.
- **"New".** The p1 text has no novelty test beyond the tables and OEIS. I checked those, plus Fischer's two extra
  files and the V3R1T4S pull requests. Literature beyond these sources is the NOVELTY seat's question, so the
  confirmed_scope below names only the sources checked.
- **claim.md overstates nothing.** Its one-sentence claim says exactly: the congruence, the base range, not a perfect
  power, p > 1e12, partial win p1.

## 8. Null models and controls
- The criterion is an exact integer identity, so no statistic is tested and no null test is needed. A chance pass does
  not exist: the check is deterministic. Under the usual heuristic, a random (b, p) passes with probability about
  1/p = 9.89e-13.
- The pair is ordinary under the heuristic. About 23 pairs are expected in the p1 box up to this p (55237
  non-perfect-power bases times about 0.000415). Base 28910 itself shows 3 Wieferich primes below 1e8 against 2.315
  expected. The value of the claim is the explicit pair, not an anomaly.
- Positive and negative controls run on the same code paths:
```
positive control: 35105 table entries checked with pow(b, p-1, p^2): 0 failures []; 362 of them re-checked with own square-and-multiply: 0 failures; entries with p > 1e12: 730, all pass: True
negative control (b, previous prime) = (28910, 1011548897231): b^(p-1) mod p^2 = 832228176060083689042280 -> FAIL as expected; b^(p-1) mod p = 1
negative control (b, next prime) = (28910, 1011548897279): b^(p-1) mod p^2 = 303583476057893971222830 -> FAIL as expected; b^(p-1) mod p = 1
negative control (b-1, p) = (28909, 1011548897263): b^(p-1) mod p^2 = 489810206317437783738402 -> FAIL as expected; b^(p-1) mod p = 1
negative control (b+1, p) = (28911, 1011548897263): b^(p-1) mod p^2 = 951099898965754203437709 -> FAIL as expected; b^(p-1) mod p = 1
negative control (b+p, p) [same residue mod p, not mod p^2] = (1011548926173, 1011548897263): b^(p-1) mod p^2 = 839785749133917372848561 -> FAIL as expected; b^(p-1) mod p = 1
trial-division control, composite 10^12 + 1 = 73 * 137 * 99990001 = 1000000000001: is_prime=False, smallest divisor=73 (expected 73)
trial-division control, composite 1000003 * 1000033 = 1000036000099: is_prime=False, smallest divisor=1000003 (expected 1000003)
trial-division control, composite 1005751^2 (largest prime <= isqrt(p), squared; its divisor sits at the very end of the range) = 1011535074001: is_prime=False, smallest divisor=1005751 (expected 1005751)
trial-division control, 661 distinct table primes p > 1e12 (independent source): all proven prime: True
heuristic null: non-perfect-power bases with 10125 < b < 65537: 55237; sum of 1/q over primes 1e12 < q <= p ~ ln(ln p / ln 1e12) = 0.000415487; expected pairs in that box ~ 23.0; chance that one given (b, p) passes ~ 1/p = 9.89e-13
ok   pair absent from FermQ_Sorg.txt
ok   pair absent from FermQ_Sort.txt
ok   p and b absent from FermQ_Sorg.txt
ok   p and b absent from FermQ_Sort.txt
ok   p and b absent from ErstBasen.txt
ok   p and b absent from ErstPBasen.txt
ok   positive control (all table pairs pass)
ok   negative controls all fail
ok   trial-division controls
TABLES_AND_CONTROLS PASS
```
  The (b+p, p) control shows that the test separates mod p^2 from mod p: every control passes mod p, and none passes
  mod p^2.

## 9. The claim's own checker agrees (claim/verify.py on claim/object/pair.json)
```
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 28910, p = 1011548897263, Fermat quotient q_p(b) mod p = 0
PASS
```
verify.py does not machine-check the absence clause; REPRODUCE.md leaves it as a manual search. Sections 4 and 5 above
do that check with my own code and fresh fetches.

confirmed_scope: The pair in object/pair.json, base b = 28910 (2*5*7^2*59, not a perfect power, 10125 < b < 65537) and p = 1011548897263 (proven prime, p > 1e12), satisfies 28910^(p-1) == 1 (mod p^2) in exact integer arithmetic and is absent from both Fischer tables, FermQ_Sorg.txt and FermQ_Sort.txt, in the snapshots identified in the-record-we-beat/RECORD.md, and from OEIS (no match for p on 2026-11-07), so it meets partial win p1 of wieferich-other-bases-fischer-table and not the full win, whose base range ends at 10125.

pass: true
