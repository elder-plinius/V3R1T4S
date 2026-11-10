role: CRITERION
context: claude code Task subagent (fresh context, saw only claim/)

# CRITERION skeptic: wieferich-other-bases-fischer-table, partial win p1, pair (28860, 1017279755641)

Object: claim/object/pair.json, sha256 6f917770e4d29ea0863a3c1801b1d0f216e7d54316a6d4ba768b179fec8a4ed1, content
`{"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28860, "p": 1017279755641}`.
The claim names partial win p1 only ("partial win claimed: p1" in claim/claim.md); it does not claim the full win.

Context note: when this subagent started, the Claude Code harness placed the workspace's project instruction files
(CLAUDE.md and the HANDOFF.md and MISSION.md it imports) in its context; they summarise earlier runs and mention this
pair. I opened no workspace file outside claim/ and my own scratch folder panel/work2-criterion/, I did not rely on
those summaries, and every number in this file comes from the commands shown below.

## The criterion I judged against

I fetched the live bank entry once (bank/targets.json on the repository's main branch, 2026-11-07T21:16:34Z,
HTTP 200). It names two partial wins, p1 and p2, and both its p1 statement and its full success_criterion appear
verbatim in claim/claim.md (output F4 below). The p1 statement, verbatim:

"New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."

p2 (a range certificate for one base of at most 1052) is not claimed and does not apply.

## Clause by clause (every computable clause re-derived with my own code)

| p1 clause | my evidence (output labels below) | verdict |
|---|---|---|
| base strictly between 10125 and 65537 | C1: 10125 lt b True, b lt 65537 True | met |
| b not a perfect power | C2: 28860 = 2^2 * 3 * 5 * 13 * 37, exponent gcd 1, exact integer k-th root search for k = 2..15 finds none | met |
| p above 1e12 | C3: p gt 10^12 True, p - 10^12 = 17279755641 | met |
| p prime (implicit in "pair"; the full criterion says "a proven prime p") | C4a: none of the 504301 trial divisors up to isqrt(p) = 1008602 divides p, so p is proven prime; C4b: Lucas certificate, p - 1 = 2^3 * 3^2 * 5 * 47^2 * 1279211, witness 11; C4c and B1: Miller-Rabin with bases 2..37 and BPSW (the test the bank's verification_method names) also pass | met, proven |
| p does not divide b (implicit) | C5: b mod p = 28860 | met |
| b^(p-1) == 1 mod p^2 checked exactly | C6a: built-in pow gives 1; C6b: my own square-and-multiply gives 1; C6c: additivity, 2 q_p(2) + q_p(3) + q_p(5) + q_p(13) + q_p(37) == 0 mod p; C7: the congruence written in claim/claim.md has base b, exponent p - 1 and modulus p^2 | met, three independent routes |
| absent from both Fischer tables | Fischer's index lists exactly two pair tables, "List from base 2 until 10125" (FermQ_Sorg.txt) and "List from base 2 until 1052 and base 65537" (FermQ_Sort.txt). R1 and R2: no row for 28860 (largest bases 10125, and 1051, 1052, 65537). A, R1, R2, F1: p occurs in neither table, not even in the digit-only stream with every separator removed. F1: my live re-fetches (21:15:55Z and 21:16:01Z, HTTP 200) are byte-identical to the sha256 recorded in claim/status_sources.md | met |
| absent from OEIS | F3: my OEIS search for p (21:15:43Z, HTTP 200) returns "Sorry, but the terms do not match anything in the table" (OEIS then held 401124 sequences) | met |
| a new pair, counted once | the object holds one pair; it is absent from Fischer's four files in claim/inputs and from his News.txt (F2); a GitHub issue and pull-request search for p in elder-plinius/V3R1T4S returns total_count 0 (F5) | met |

## Hidden quantifiers and stretched definitions

1. "Pair" carries two quantifiers the p1 sentence does not repeat: p prime and p not dividing b. Both are proven
   above; primality rests on exhaustive trial division, which needs no published bound.
2. "Absent from both Fischer tables" has a structural half: neither table has rows between 10126 and 65536 (R1, R2),
   and Fischer's index lists no other pair table, so no row for 28860 can exist. That is the gap p1 was written for,
   not a stretched reading. The stronger reading also holds: the number p appears nowhere in FermQ_Sorg.txt,
   FermQ_Sort.txt, ErstBasen.txt, ErstPBasen.txt or News.txt, under any digit separator.
3. "Checked exactly": exact integer arithmetic only, no floating point, no screen; three routes agree.
4. "New": the pair is not inherited from a smaller base. b is not a perfect power; none of the 46 proper divisors d
   of b has q_p(d) == 0 mod p (C8), so the pair is not a product of smaller pairs; and the complete scan of every base
   2..65536 finds 28860 as the only base for this p (C9). This also agrees with Fischer's own completeness statement:
   p is below his 4.8E+12 limit for bases 2..10125 (L), his table lists p nowhere, and my scan finds no base up to
   10125 for p.
5. Freshness: the p1 text asks for no re-fetch (the full criterion does), but the live tables were re-fetched anyway
   and are byte-identical to the claim's snapshot.
6. The criterion texts are not paraphrased: both quoted texts match the live bank entry verbatim (F4).

## Null models and controls

- The criterion is an exact integer identity, so no statistic is tested. Under the uniform Fermat-quotient heuristic
  one fixed pair satisfies it with probability 1/p = 9.830e-13 (X2), so a pass cannot be a chance artefact of the check.
- Negative controls fail as they should: the same base with the neighbouring primes 1017279755633 and 1017279755669
  (N1), and the bases 28859 and 28861 with the same p (N2, C9).
- The claim's own checker claim/verify.py returns PASS (exit 0) on the object and FAIL (exit 1) on five mutated
  objects (b + 1, the next prime, the perfect power 28900, base 10125, the composite p + 2). Each FAIL line names the
  violated clause, so its PASS is not a permissive artefact.
- Positive controls: my exact check reproduces all 1569 of Fischer's own pairs with p above 1e11 (P), and my BPSW
  agrees with a sieve below 300000 and separates known strong Lucas and strong base-2 pseudoprimes (B0).

## Does the full win apply?

No. The full success criterion requires "an integer base 3 <= b <= 10125", and b = 28860 lies outside that range
(C1: "full-win base range 3 le b le 10125 holds: False"). The claim does not claim it. No headline flag applies:
b is not 3 (Mirimanoff), p^(b-1) mod b^2 = 53114761, not 1 (S1, so not a double-Wieferich-type pair), and the pair
does not hold mod p^3 (X1).

## Commands and real output

Commands ran with absolute paths and `2>&1 | tee` into panel/work2-criterion/; they are shown here relative to the
run folder. Python is the standard-library `python3 -I -B`; my scripts are in panel/work2-criterion/code/.

Hashes of the claim files (`sha256sum` on each file, relative names logged), saved as sha256_inputs.txt:
```
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820  claim/inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362  claim/inputs/ErstPBasen.txt
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4  claim/inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b  claim/inputs/FermQ_Sort.txt
6f917770e4d29ea0863a3c1801b1d0f216e7d54316a6d4ba768b179fec8a4ed1  claim/object/pair.json
```

`python3 -I -B panel/work2-criterion/code/criterion_check.py claim 2>&1 | tee panel/work2-criterion/criterion_check_output.txt`
```
[C0] claim/object/pair.json bytes: 106 content: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28860, "p": 1017279755641}
     keys: ['b', 'p', 'partial_win', 'target_id'] ; partial_win field: p1 ; target_id field: wieferich-other-bases-fischer-table
     JSON types: b int , p int
     b = 28860, p = 1017279755641
[C1] clause 'base 10125 lt b lt 65537': 10125 lt b: True ; b lt 65537: True
     full-win base range 3 le b le 10125 holds: False
[C2] clause 'not a perfect power': b = 2^2 * 3 * 5 * 13 * 37 ; product equals b: True ; every listed factor prime (trial division): True
     gcd of the exponents: 1 ; exact integer k-th roots r with r^k == b for k = 2 .. 15 : []
     b is not a perfect power: True
[C3] clause 'p above 1e12': p gt 10^12: True ; p - 10^12 = 17279755641
[C4a] implicit clause 'p prime': trial division of p by 2 and by every odd d up to isqrt(p) = 1008602 ; trial divisors tested: 504301 ; smallest factor found: None ; 0.02 s
      p proven prime by exhaustive trial division: True
[C4b] p - 1 = 1017279755640 = 2^3 * 3^2 * 5 * 47^2 * 1279211 ; all these factors prime by trial division: True
      Lucas witness a = 11 ; a^(p-1) mod p = 1 ; a^((p-1)/q) mod p for each prime q dividing p-1: {2: 1017279755640, 3: 331660448318, 5: 495396832494, 47: 325776137472, 1279211: 676978286326}
      p proven prime by the Lucas test: True
[C4c] Miller-Rabin with the 12 prime bases 2..37 (deterministic far above p): True
[C5] implicit clause 'p does not divide b': b mod p = 28860 ; p does not divide b: True
[C6a] clause 'b^(p-1) == 1 mod p^2 checked exactly': built-in pow(b, p-1, p^2) = 1
[C6b] own square-and-multiply ladder, b^(p-1) mod p^2 = 1 ; 0.000 s for both
[C6c] additivity route: Fermat quotients q_p(r) mod p for the prime factors r of b: {2: 805472779928, 3: 647969670660, 5: 149508072110, 13: 515524916456, 37: 127891047841}
      sum over r of e_r * q_p(r) mod p = 0 (0 means b^(p-1) == 1 mod p^2)
      direct Fermat quotient q_p(b) mod p = 0
      exact identity holds by all three routes: True
[C7] congruence as written in claim/claim.md: 28860^1017279755640 ≡ 1 (mod 1017279755641^2)
     its base == b: True ; its exponent == p - 1: True ; its modulus == p^2: True
[C8] subsumption by smaller bases: proper divisors d of b (1 lt d lt b): 46 ; divisors with q_p(d) == 0 mod p: []
[C9] complete scan, every base a in 2..65536 with a^(p-1) == 1 mod p^2: [28860] ; 0.3 s
     bases le 10125 among them: [] ; perfect powers among them: []
[N1] negative controls, same base b with the neighbouring primes:
     previous prime 1017279755633 : b^(q-1) mod q^2 == 1: False ; q_q(b) mod q = 616958052045
     next prime 1017279755669 : b^(q-1) mod q^2 == 1: False ; q_q(b) mod q = 627746958143
[N2] negative controls, same p with b-1 and b+1: q_p(b-1) mod p = 6547808847 ; q_p(b+1) mod p = 320504999362
[S1] side check, p^(b-1) mod b^2 = 53114761 (1 would make it a double-Wieferich-type pair)
```

`python3 -I -B panel/work2-criterion/code/table_check.py claim 2>&1 | tee panel/work2-criterion/table_check_output.txt`
```
pair under test: b = 28860, p = 1017279755641
[H] claim/inputs/FermQ_Sorg.txt: 288459 bytes, sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
    status_sources.md record (fetched, HTTP, sha256): ('2026-11-07T20:11:24Z', '200', '35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4'); sha256 match: True
[H] claim/inputs/FermQ_Sort.txt: 33141 bytes, sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
    status_sources.md record (fetched, HTTP, sha256): ('2026-11-07T20:11:25Z', '200', 'bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b'); sha256 match: True
[H] claim/inputs/ErstBasen.txt: 115771 bytes, sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820
    status_sources.md record (fetched, HTTP, sha256): ('2026-11-07T20:11:25Z', '200', 'e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820'); sha256 match: True
[H] claim/inputs/ErstPBasen.txt: 81696 bytes, sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362
    status_sources.md record (fetched, HTTP, sha256): ('2026-11-07T20:11:25Z', '200', '3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362'); sha256 match: True
[A] absence of p and of base b in each fetched Fischer file
    FermQ_Sorg.txt: literal '1017279755641' occurrences 0; occurrences in the digit-only stream (every separator removed) 0; p among 20941 distinct integer tokens: False; first 7 digits '1017279' occurrences 0
    FermQ_Sorg.txt: lines holding the integer token 28860: 0
    FermQ_Sort.txt: literal '1017279755641' occurrences 0; occurrences in the digit-only stream (every separator removed) 0; p among 2564 distinct integer tokens: False; first 7 digits '1017279' occurrences 0
    FermQ_Sort.txt: lines holding the integer token 28860: 0
    ErstBasen.txt: literal '1017279755641' occurrences 0; occurrences in the digit-only stream (every separator removed) 0; p among 9589 distinct integer tokens: False; first 7 digits '1017279' occurrences 0
    ErstBasen.txt: lines holding the integer token 28860: 0
    ErstPBasen.txt: literal '1017279755641' occurrences 0; occurrences in the digit-only stream (every separator removed) 0; p among 6498 distinct integer tokens: False; first 7 digits '1017279' occurrences 0
    ErstPBasen.txt: lines holding the integer token 28860: 0
[T] coverage statements quoted from the tables (verbatim lines)
    FermQ_Sorg.txt: Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125
    FermQ_Sorg.txt: Die Basen sind gegenwaertig durchsucht bis 4.8E+12
    FermQ_Sorg.txt: 10000 Basen von 2 bis 10125
    FermQ_Sort.txt: Die gefundenen Primzahlen der Fermatquotienten von der Basis 2 bis 1052
    FermQ_Sort.txt: Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
    FermQ_Sort.txt: Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
[R1] FermQ_Sorg.txt rows: 10000; smallest base 2; largest base 10125; bases strictly increasing in file order: True; row for base 28860: False; rows with a base above 10125: []
     entries: 31606; unparsed entries: []; p among the entries of any row: False; largest entry: 4795482544417
[R2] FermQ_Sort.txt rows: 1011; smallest base 2; largest bases [1051, 1052, 65537]; row for base 28860: False; bases between 1053 and 65536: []
     entries: 3367; unparsed entries: []; p among the entries of any row: False
     non-row lines after the header: 7, e.g. ['siehe https://en.wikipedia.org/wiki/Wieferich_prime#History_', '(Fermatprimbasis)', 'Die Basen 4, 8, 16, 32, ... haben die gleichen Primzahlen, w']
[L] p vs the stated search limits: p lt 4.8E+12 (FermQ_Sorg.txt, bases 2..10125): True; p lt 7.4E+13 (FermQ_Sort.txt, rest of bases 2..1052): True
[P] positive controls: Fischer's own pairs with p gt 1e11, re-checked with exact pow(b, p-1, p^2) == 1
    pairs: 1569; exact identity holds: 1569; fails: []
    largest three by p: [(852, 179290250382637), (963, 185422197633461), (770, 194092950328757)]
```

The claim's own checker on the object and on five mutated objects written to panel/work2-criterion/controls/
(`python3 -I -B claim/verify.py ...`, exit status from PIPESTATUS), saved as verify_runs_output.txt:
```
== claim/verify.py claim/object/pair.json
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 28860, p = 1017279755641, Fermat quotient q_p(b) mod p = 0
PASS
exit status 0
== claim/verify.py panel/work2-criterion/controls/neg_base_plus1.json
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 28861, p = 1017279755641, Fermat quotient q_p(b) mod p = 320504999362
FAIL
exit status 1
== claim/verify.py panel/work2-criterion/controls/neg_next_prime.json
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 28860, p = 1017279755669, Fermat quotient q_p(b) mod p = 627746958143
FAIL
exit status 1
== claim/verify.py panel/work2-criterion/controls/neg_perfect_power.json
ok   10125 < b < 65537
FAIL b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 28900, p = 1017279755641, Fermat quotient q_p(b) mod p = 345987645289
FAIL
exit status 1
== claim/verify.py panel/work2-criterion/controls/neg_base_10125.json
FAIL 10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 10125, p = 1017279755641, Fermat quotient q_p(b) mod p = 1005843387688
FAIL
exit status 1
== claim/verify.py panel/work2-criterion/controls/neg_composite_p.json
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
FAIL p is prime (deterministic Miller-Rabin)
ok   p does not divide b
FAIL b^(p-1) == 1 mod p^2
b = 28860, p = 1017279755643, Fermat quotient q_p(b) mod p = 223355118527
FAIL
exit status 1
```

`python3 -I -B panel/work2-criterion/code/extra_check.py claim 2>&1 | tee panel/work2-criterion/extra_check_output.txt`
```
[B0] BPSW self-test: agreement with a sieve for every n below 300000: True; mismatches: []
     known strong Lucas pseudoprimes [5459, 5777, 10877, 16109, 18971]: strong Lucas says probable prime: [True, True, True, True, True]; strong base-2 test: [False, False, False, False, False]
     known strong base-2 pseudoprimes [2047, 3277, 4033, 4681, 8321]: strong base-2 test: [True, True, True, True, True]; strong Lucas: [False, False, False, False, False]
[B1] BPSW on p = 1017279755641: strong base-2 test True; strong Lucas True; BPSW True
[X1] b^(p-1) mod p^3 == 1: False; (b^(p-1) mod p^3 - 1) / p^2 mod p = 934667587361
[X2] null model: if q_p(b) is uniform mod p, one fixed pair satisfies the identity with probability 1/p = 9.830e-13
```

Live fetches, one request each, with
`curl -sS -A 'V3R1T4S-agent/1.0 (open-research notebook; one honest request)' -o panel/work2-criterion/fetch_.../FILE -w '%{http_code}' URL`,
each download in its own new folder; the time is `date -u` read just before the request (fetch_log_*.txt):
```
request_utc 2026-11-07T21:15:43Z
url https://oeis.org/search?q=1017279755641&fmt=data
http_status 200
request_utc 2026-11-07T21:15:55Z
url http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
http_status 200
request_utc 2026-11-07T21:16:01Z
url http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
http_status 200
request_utc 2026-11-07T21:16:06Z
url http://www.fermatquotient.com/
http_status 200
request_utc 2026-11-07T21:16:31Z
url http://www.fermatquotient.com/FermatQuotienten/News.txt
http_status 200
request_utc 2026-11-07T21:16:34Z
url https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json
http_status 200
request_utc 2026-11-07T21:16:36Z
url https://api.github.com/search/issues?q=1017279755641+repo:elder-plinius/V3R1T4S
http_status 200
```

Hashes of the fetched files (sha256_fetched.txt):
```
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4  288459 bytes  panel/work2-criterion/fetch_sorg/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b  33141 bytes  panel/work2-criterion/fetch_sort/FermQ_Sort.txt
42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1  16104 bytes  panel/work2-criterion/fetch_index/index.html
a507f9e958842e3ad0ab63d52d0204dca316b918c53adbec7a97b0f67d561c4c  6737 bytes  panel/work2-criterion/fetch_oeis/oeis_search_p.txt
```

Fischer's index page, the Fermat-quotient file list (links and titles, tags stripped with sed):
```
[http://www.fermatquotient.com/FermatQuotienten/Generelles.txt] Generelles / Generals / Update 23.02.2009
[http://www.fermatquotient.com/FermatQuotienten/News.txt] Neues und Rekorde / News and records / Update 01.09.2025
[http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt] Tabelle bis Basis 1052 / List from base 2 until 1052 and base 65537 / Update 21.10.2026
[http://www.fermatquotient.com/FermatQuotienten/Statistik.txt] Statistisches / Statistics / Update 21.10.2026
[http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt] Tabelle bis Basis 10125 / List from base 2 until 10125 / Update 21.10.2026
[http://www.fermatquotient.com/FermatQuotienten/FermatQ3.txt] B^(P-1) == 1 (mod P^3) / Update 14.10.2023
[http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt] Extreme Erstbasen / Extreme first bases / Update 27.09.2025
[http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt] Extreme Erstprimbasen / Extreme first prime bases / Update 27.09.2025
[http://www.fermatquotient.com/FermatQuotienten/SwitchFermQ.txt] Doppel-Wieferich-Paare / Double Wieferich pairs / Update 10.06.2025
[http://www.fermatquotient.com/FermatQuotienten/PQuotient_Sort.txt] Potenz-Differenz-Quotienten / (B+1)^(P-1) - B^(P-1) == 0 (mod P^2) / New 21.04.2015 / Update 07.10.2022
```

`python3 -I -B panel/work2-criterion/code/live_check.py claim panel/work2-criterion 2>&1 | tee panel/work2-criterion/live_check_output.txt`
```
[F1] live re-fetch of the two Fischer tables vs the claim's records
    FermQ_Sorg.txt: live sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4; equals status_sources.md record: True; byte-identical to claim/inputs copy: True
    FermQ_Sorg.txt (live): literal p occurrences 0; p in digit-only stream 0; lines holding the integer token 28860: []
    FermQ_Sort.txt: live sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b; equals status_sources.md record: True; byte-identical to claim/inputs copy: True
    FermQ_Sort.txt (live): literal p occurrences 0; p in digit-only stream 0; lines holding the integer token 28860: []
[F2] Fischer's News.txt (news and records), live
    News.txt: 8500 bytes, sha256 1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7
    News.txt (live): literal p occurrences 0; p in digit-only stream 0; lines holding the integer token 28860: []
[F3] OEIS search page for p, live
    bytes 6737; contains 'Sorry, but the terms do not match anything in the table': True
    Search: 1017279755641
    Contains 401124 sequences
    Last modified November 7 16:06 EST 2026
    result entries (lines starting with an A-number such as A000001): 0
[F4] live bank entry vs the texts quoted in claim/claim.md
    entries with id wieferich-other-bases-fischer-table: 1; bank generated: 2026-11-06; targets: 1116
    partial wins named in the bank entry: ['p1', 'p2']
    p1 statement appears verbatim in claim/claim.md: True
    full success_criterion appears verbatim in claim/claim.md: True
    claim/claim.md names partial win: p1; object partial_win field: p1
[F5] GitHub issue and pull-request search for p in elder-plinius/V3R1T4S, live
    total_count 0; incomplete_results False; items []
```

## Verdict

Every clause of partial win p1 holds for the single pair in claim/object/pair.json, each checked with my own code or
my own fetch: the base is in range and not a perfect power, p is above 1e12 and proven prime, the identity holds in
exact arithmetic, and the pair is absent from both Fischer tables and from OEIS. The full win does not apply,
because b is above 10125. The win is not subsumed: b is not a perfect power, no proper divisor of b is a Wieferich
base for p, no other base in 2..65536 is, and p appears in no Fischer file, in no OEIS search result and in no
V3R1T4S issue or pull request.

confirmed_scope: The single pair in object/pair.json, b = 28860 = 2^2*3*5*13*37 (not a perfect power, an integer from 10126 to 65536) with p = 1017279755641 (above 1e12, proven prime by exhaustive trial division up to isqrt(p)), satisfies b^(p-1) == 1 mod p^2 in exact integer arithmetic and is absent from both Fischer tables identified by URL and sha256 in the-record-we-beat/RECORD.md (neither FermQ_Sorg.txt nor FermQ_Sort.txt has a row for base 28860 or contains p) and from OEIS (a search for p on 2026-11-07 matched no sequence), so it is one new pair meeting partial win p1 of wieferich-other-bases-fischer-table, and not the full win, which requires b at most 10125.

pass: true
