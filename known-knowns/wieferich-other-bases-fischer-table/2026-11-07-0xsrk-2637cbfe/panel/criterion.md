role: CRITERION
context: claude code headless session (claude -p --safe-mode in a copy of claim/ outside the workspace; fresh context, saw only claim/)

# CRITERION skeptic: wieferich-other-bases-fischer-table, pair (b, p) = (5481, 4848813530161)

Claimed: the full win (the success criterion), not a partial win. Object: claim/object/pair.json =
`{"target_id": "wieferich-other-bases-fischer-table", "win": "full", "b": 5481, "p": 4848813530161}`.

My checker is work/crit_check.py. I wrote it from scratch and it does not reuse claim/verify.py. It ran on my own
re-fetched live files in work/fetch/. Its full output is in work/crit_check_out.txt, and every number below is pasted
from command output. I shortened paths in pasted output to relative ones; nothing else is changed.

## 1. Re-fetch of the live sources (one request each, kit User-Agent)

Time before the fetches: `2026-11-07T22:46:58Z`. Time after: `2026-11-07T22:47:13Z` (work/time_before_fetch.txt,
work/time_after_fetch.txt). All five requests returned HTTP `200` (work/fetch_*_status.txt).

sha256 of my re-fetched files (work/sha256_fetched.txt) next to the scout's values (claim/status_sources.md). I also
hashed the claim copies myself (work/sha256_inputs.txt):

| file | my live re-fetch | claim/inputs copy (my hash) | scout's record |
|---|---|---|---|
| FermQ_Sorg.txt | 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 | 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 | same |
| FermQ_Sort.txt | bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b | bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b | same |
| SwitchFermQ.txt | 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa | 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa | same |
| OEIS search for p (fmt=data) | 4bd7d4d125da3b5c2559eead8ae0d6b51ce626836ef129de349c957d45b3335d | (not in inputs) | 124007da4c378ce70533976e1d5cbabb7d38f1acb0e887f63ecc662aca92507d |

The three Fischer files are byte-identical to the claim's inputs and to the scout's fetch records from
2026-11-07T22:40:10Z to 22:40:12Z. The OEIS page hash differs, which is normal for a dynamic page. Its text is the
same no-match result: line 116 of work/fetch/oeis_p.html contains "Sorry, but the terms do not match anything in the
table." for the search `4848813530161` (line 101).

I made one more OEIS request, `q=751787&fmt=text` (751787 is the only odd prime in base 5481's row), to look for "the
base-b Wieferich sequence, if one exists". It gave "Showing 1-4 of 4", and none of the four is a Wieferich sequence:
- `%N A042380 Numerators of continued fraction convergents to sqrt(717).`
- `%N A181245 T(n,k) = Number of n X k binary matrices with no 2 X 2 circuit having pattern 0101 in any orientation.`
- `%N A181241 Number of nX6 binary matrices with no 2X2 circuit having pattern 0101 in any orientation.`
- `%N A208267 Number of nX6 0..1 arrays with new values 0..1 introduced in row major order and no element equal to more than two of its immediate leftward or upward or left-upward diagonal neighbors.`

So OEIS has no base-5481 Wieferich sequence, and no OEIS sequence contains p in its data.

On "re-fetched immediately before the claim": claim/status_sources.md records fetches of every criterion source at
22:40:10Z–22:40:12Z. The claim folder gives no separate claim timestamp, so I cannot measure the exact gap. My own
fetch about seven minutes later returned the same bytes. So whatever that gap was, the live record at judgment time
is exactly the record the claim was checked against.

## 2. Clause-by-clause check of the full success criterion

From work/crit_check_out.txt:

```
b = 5481, p = 4848813530161
factorisation of b: {3: 3, 7: 1, 29: 1} | perfect_power(b): None
isqrt(p) = 2202002 | trial division up to isqrt(p) says prime: True
p-1 factorisation: {2: 4, 3: 1, 5: 1, 307: 1, 797: 1, 82571: 1} | Pocklington witnesses: {2: 7, 3: 2, 5: 2, 307: 2, 797: 2, 82571: 2} | certificate ok: True
deterministic MR bases 2..37 (valid < 3.18e23): True
pow(b, p-1, p^2) = 1
pow(b, p-1, p^3) = 75280445891607534169433307482715286989 (1 would mean a p^3 entry)
FermQ_Sorg.txt 'durchsucht bis' statements: ['4.8E+12']
FermQ_Sort.txt 'durchsucht bis' statements: ['2.00E+14', '7.4E+13']
governing file for this b: FermQ_Sorg.txt
FermQ_Sorg rows parsed: 10000 bases from 2 to 10125
FermQ_Sort rows parsed: 981 bases from 2 to 65537
row for b in FermQ_Sorg.txt: ['2^3, 751787']
row for b in FermQ_Sort.txt: None
per-row note in Sorg row of b: none
stated searched limit for b: 4.8E+12 = 4800000000000
p - limit = 48813530161 | p / limit = 1.0101694854502083
primes listed for b: Sorg [2, 751787] | Sort []
p as a substring anywhere in Sorg/Sort/Switch: False False False
  check listed q=2: b^(q-1) mod q^2 = 1 | b^(q-1) mod q^3 = 1
  check listed q=751787: b^(q-1) mod q^2 = 1 | b^(q-1) mod q^3 = 247622801208373233
largest 5 P in Sorg rows for bases >= 1053: [(4795482544417, 1999), (4764929208187, 2625), (4741258166573, 5758), (4727293347713, 4942), (4710091241467, 6483)]
entries above the stated limit for bases >= 1053: []
pow(p, b-1, b^2) = 25942981 (1 needed for a double Wieferich pair)
SwitchFermQ.txt mentions b as a token: False | mentions p: False
all c in 2..10125 with c^(p-1) == 1 mod p^2: [5481]
...
ok   3 <= b <= 10125
ok   b not a perfect power
ok   p proven prime (trial division + Pocklington)
ok   p does not divide b
ok   pow(b,p-1,p^2) == 1
ok   p STRICTLY GREATER than stated limit
ok   p absent from b's row in FermQ_Sorg.txt
ok   p absent from b's row in FermQ_Sort.txt
no   headline flag: Mirimanoff (b == 3 and p > 1.2e15)
no   headline flag: double Wieferich pair
FULL-WIN COMPUTABLE CLAUSES: ALL PASS
```

Clause by clause:

- **"an integer base 3 ≤ b ≤ 10125 that is not a perfect power"**: holds. 5481 = 3^3·7·29. The exponent gcd is 1,
  and an exact integer k-th-root search finds no perfect power. The proviso about b = a^k does not apply.
- **"a proven prime p"**: holds, with an actual proof and not just a probable-prime test. Trial division by every
  odd number up to isqrt(p) = 2202002 finds no factor. Independently, a Pocklington certificate built from the full
  factorisation p−1 = 2^4·3·5·307·797·82571 gives a witness for every prime factor. Deterministic Miller–Rabin
  (bases 2..37) agrees.
- **"not dividing b"**: holds, since p is far larger than b.
- **"pow(b, p-1, p^2) == 1"**: holds in exact integer arithmetic. My checker printed `pow(b, p-1, p^2) = 1`, the
  one-liner printed `1` (work/oneliner_out.txt), and claim/verify.py printed `PASS` with
  `Fermat quotient q_p(b) mod p = 0` (work/verify_py_out.txt). It is a p^2 pair, not p^3.
- **"STRICTLY GREATER than that base's searched limit stated in the live … FermQ_Sorg.txt (for 1053 ≤ b ≤ 10125)"**:
  holds. b = 5481 falls in the FermQ_Sorg.txt band. That file makes exactly one limit statement, "Die Basen sind
  gegenwaertig durchsucht bis 4.8E+12", and base 5481's row has no per-row "(>…)" note overriding it. p − 4.8E+12 =
  48813530161, so p is greater by 1.0%. The stated limit is consistent with the table's contents: no entry for any
  base ≥ 1053 exceeds it (largest 4795482544417, base 1999), and the file's own expectation-vs-actual footer reads
  `10^12 4.8E+12 552.2 549 -0.1`.
- **"absent from that base's row in both files"**: holds. The FermQ_Sorg.txt row is `5481,  2^3, 751787`. I
  re-verified both listed primes, so the row is a genuine record. FermQ_Sort.txt has no row for 5481 (it covers
  2..1052 and 65537), so the clause holds trivially there. The string 4848813530161 appears nowhere in FermQ_Sorg.txt,
  FermQ_Sort.txt or SwitchFermQ.txt. A grep of all five claim/inputs files, including ErstBasen.txt and ErstPBasen.txt,
  also finds no occurrence.
- **"and from OEIS (the base-b Wieferich sequence, if one exists)"**: holds. The p search returns no match, and no
  base-5481 Wieferich sequence exists (section 1).
- **"All of these are re-fetched immediately before the claim"**: holds as far as it can be checked (section 1).
- **"Each new pair counts once" / "maximize the number of new pairs"**: this claim adds exactly 1 new pair. An
  exhaustive scan of c = 2..10125 finds no other base for which this p is a Wieferich prime (`[5481]`), so this p
  yields no second pair.

Parse artifact, disclosed: my row parser also matched the header line " 4354, 669, 5185, …" (the "Letzte 20" list) as
a duplicate base 4354 row. It does not touch base 5481.

## 3. Headline flags

- Mirimanoff prime (b = 3, p > 1.2e15): **no**, because b = 5481.
- Double Wieferich pair: **no**. `pow(p, b-1, b^2) = 25942981`, which is not 1, and SwitchFermQ.txt mentions neither
  5481 nor p.

## 4. Hidden quantifiers, stretched definitions, null models

- **Precision of the stated limit.** "4.8E+12" has two significant figures, and p is only 1.0% above it, inside the
  band that would still print as 4.8E+12. So Fischer's true frontier could be above 4.8e12, and he might reach p
  independently. That does not break the criterion, which literally says "searched limit stated", and the stated
  figure is 4800000000000 < p. His table, unchanged at my re-fetch, does not contain p. Nothing in it is listed above
  4.8e12 for bases ≥ 1053, and the expected count above the limit (next bullet) would almost certainly have produced
  entries if he had searched past p. The claim does not stretch the definition here, but `confirmed_scope` says
  "stated" and not "searched".
- **Trivial-solution null model.** Since 3 ≤ b < p, b cannot be ≡ ±1 (mod p^2). p ∤ b. b is not a perfect power, so
  the pair cannot be inherited from a smaller base a with b = a^k. Fermat quotients are multiplicative, so I also
  checked whether the pair follows from table pairs: no base in 2..10125 other than 5481 has p as a Wieferich prime,
  and the quotients of the factor-bases are all non-zero (q_p(3) = 1100775266518, q_p(7) = 3839059523915,
  q_p(29) = 2556241736853 mod p). The pair is primitive, not subsumed by any known pair.
- **Frequency null model.** With the heuristic Σ1/q over the 8990 non-perfect-power bases 1053..10125, the expected
  number of pairs with 4.8E+12 < P ≤ p is `3.115`. One find is typical of an honest search just past the frontier,
  not a suspicious outlier. The chance of a random prime near p being Wieferich for a fixed base is
  `1/p = 2.062e-13`, so the pair cannot be a lucky guess, and the exact congruence settles it anyway. The
  significance is modest: a new record entry beyond the frontier, not a new kind of mathematical object. That is
  exactly what the full criterion counts ("Each new pair counts once").

## 5. Which win applies

- **Full win (the success criterion): applies.** Every clause holds literally, as shown above. Count: 1 new pair.
  Neither headline flag is raised.
- **Partial win p1** (10125 < b < 65537, p above 1e12): **does not apply**, because b = 5481 ≤ 10125. The full win
  makes it moot anyway. claim/claim.md quotes no other enumerated partial win, and none is needed.
- The claim says it is a full win and not a partial win. That label is accurate.

confirmed_scope: The pair in object/pair.json (b = 5481 = 3^3·7·29, not a perfect power; p = 4848813530161, proven prime by trial division to its square root and by a Pocklington certificate) satisfies 5481^(p−1) ≡ 1 (mod p^2) in exact arithmetic, p is strictly greater than the 4.8E+12 searched limit stated in FermQ_Sorg.txt and is absent from base 5481's row there, from FermQ_Sort.txt (which has no 5481 row) and from OEIS as recorded in the-record-we-beat/RECORD.md (the three Fischer tables re-fetched byte-identical at 2026-11-07T22:46:58Z–22:47:13Z), so it counts as one new pair under the full success criterion of wieferich-other-bases-fischer-table, with neither headline flag (not a Mirimanoff prime, not a double Wieferich pair).

pass: true
