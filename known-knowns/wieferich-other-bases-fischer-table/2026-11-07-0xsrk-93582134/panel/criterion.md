role: CRITERION
context: claude code headless session (claude -p --safe-mode in a copy of claim/ outside the workspace; fresh context, saw only claim/)

# CRITERION skeptic: wieferich-other-bases-fischer-table, partial win p1

Object: claim/object/pair.json = `{"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 36260, "p": 1026120862861}`

Named win: p1. Verbatim criterion (from claim/claim.md): "New pair for a base 10125 < b < 65537 that is not a
perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."

## Verdict in one paragraph

Every clause of p1 holds when taken literally, and I checked each one with my own code or my own fetches. The full win
does NOT apply: its base range is 3 to 10125 inclusive, and b = 36260 lies outside it. So p1 is the only win that can
apply, and the full win can't subsume it. The pair is not a cheap derivation either. 36260 is not a perfect power. No
other base in 2..131072 is Wieferich for this p, so 36260 is not a product of known Wieferich bases for p. And p appears
nowhere in Fischer's four files, so those files hold no known base for p to build from. One limit belongs in the scope:
Fischer's two tables have no row and no searched limit for any base from 10126 to 65536. The "absent from both Fischer
tables" clause is therefore met vacuously for the base row (that is how p1 is designed). Its real content is that p is
missing from the files' text and from OEIS. So the scope must not call this "beyond a searched limit", "the first
Wieferich prime to base 36260", or a full win.

## Clause-by-clause check (my code: work/code/check_arith.py, work/code/check_tables.py)

Command: `python3 -I -B work/code/check_arith.py claim/object/pair.json` (full output saved in work/out/check_arith.txt):

```
object: {'target_id': 'wieferich-other-bases-fischer-table', 'partial_win': 'p1', 'b': 36260, 'p': 1026120862861}
b = 36260  p = 1026120862861
[range] 10125 < b < 65537: True
[perfect power] factorization of b: {2: 2, 5: 1, 7: 2, 37: 1}  gcd of exponents: 1  exact k-th roots found: []
[perfect power] b is NOT a perfect power: True
[size] p > 10**12: True  p / 1e12 = 1.026120862861
[prime] trial division by every integer 2..isqrt(p) = 1012976 -> divisor found: None  (0.09s)
[prime] Lucas certificate: p-1 = {2: 2, 3: 1, 5: 1, 17102014381: 1}  product check: True  witness a = 6
[prime] p is prime (trial division and Lucas): True
[coprime] b % p = 36260  p does not divide b: True
[wieferich] own square-and-multiply b^(p-1) mod p^2 = 1
[wieferich] built-in pow             b^(p-1) mod p^2 = 1
[wieferich] b^(p-1) mod p (sanity, Fermat) = 1
[wieferich] q_p of prime factors of b: {2: 124791506035, 5: 493211622138, 7: 164673106328, 37: 980100878858}
[wieferich] sum e*q_p(prime) mod p = 0  direct q_p(b) mod p = 0
[all bases] bases a in 2..131072 with a^(p-1) == 1 mod p^2: [36260]  (1.1s)
[all bases] of these, bases <= 10125: []
[smallest] smallest prime q not dividing b with b^(q-1) == 1 mod q^2: 3
[smallest] all such primes q < 200000 for base b: [3, 11, 491]
[null model] non-perfect-power bases in 10126..65536: 55237  heuristic expected pairs with 1e12 < p <= claimed p: 51.5
```

| p1 clause | result | evidence |
|---|---|---|
| base strictly between 10125 and 65537 | yes | `[range] ... True`; 65537 itself (Fischer's extra row) is excluded by the strict bound, and b is not 65537 |
| b not a perfect power | yes | 36260 = 2^2 * 5 * 7^2 * 37, exponent gcd 1, and no exact k-th root found for any k |
| p above 1e12 | yes, strictly | p / 1e12 = 1.026120862861 (a 2.6% margin, but the clause is a plain strict bound) |
| p prime (implicit in "pair") | proven | full trial division to isqrt(p) = 1012976 finds no divisor; an independent Lucas certificate (p-1 fully factored, witness 6). This doesn't depend on the Miller-Rabin bound cited in claim/verify.py |
| b^(p-1) == 1 mod p^2, checked exactly | yes | my own square-and-multiply gives 1, built-in pow gives 1, and the additive Fermat-quotient cross-check 2*q(2)+q(5)+2*q(7)+q(37) gives 0 mod p |
| absent from both Fischer tables | yes (vacuous for the base row) | see the table section below |
| absent from OEIS | yes | see the OEIS section below |

Claim's own checker, `python3 -I -B claim/verify.py claim/object/pair.json` (work/out/claim_verify.txt):

```
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 36260, p = 1026120862861, Fermat quotient q_p(b) mod p = 0
PASS
```

## Table-absence clause (Fischer tables)

"Both Fischer tables" are FermQ_Sorg.txt (bases 2..10125) and FermQ_Sort.txt (bases 2..1052 and 65537), as the full
criterion names them. To cover a wider reading, I also checked his two "extreme first bases" files. My checker matches
p and b only as whole numbers, so digit runs inside longer numbers don't count.

Command on the scout's copies in claim/inputs/ (work/out/check_tables_inputs.txt; excerpt, with the base-row lists of
the two Erst files left out because their layout is not one row per base):

```
== FermQ_Sorg.txt  bytes: 288459  sha256: 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
   header: Die Basen sind gegenwaertig durchsucht bis 4.8E+12
   base rows parsed: 10001  min: 2  max: 10125  bases > 10125: []
   row for b = 36260 present: False
   p occurs as a whole number: False   b occurs as a whole number: False
== FermQ_Sort.txt  bytes: 33141  sha256: bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
   header: Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
   header: Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
   base rows parsed: 983  min: 2  max: 65537  bases > 10125: [65537]
   row for b = 36260 present: False
   p occurs as a whole number: False   b occurs as a whole number: False
== ErstBasen.txt  bytes: 115771  sha256: e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820
   p occurs as a whole number: False   b occurs as a whole number: False
== ErstPBasen.txt  bytes: 81696  sha256: 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362
   p occurs as a whole number: False   b occurs as a whole number: False
```

All four sha256 values match those recorded in claim/status_sources.md.

My own live re-fetch: one request per URL with the required User-Agent. Status codes (work/out/fetch_sorg_status.txt,
work/out/fetch_sort_status.txt): `200` and `200`. File write times from `TZ=UTC ls -l` (work/out/fetch_times.txt,
owner and size columns dropped):

```
2026-11-07T23:29:42Z FermQ_Sorg.txt
2026-11-07T23:29:44Z FermQ_Sort.txt
2026-11-07T23:29:46Z oeis_search.txt
```

Check on the live copies (work/out/check_tables_live.txt, excerpt):

```
== FermQ_Sorg.txt  bytes: 288459  sha256: 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
   row for b = 36260 present: False
   p occurs as a whole number: False   b occurs as a whole number: False
== FermQ_Sort.txt  bytes: 33141  sha256: bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
   row for b = 36260 present: False
   p occurs as a whole number: False   b occurs as a whole number: False
```

The live tables are byte-identical to the scout's copies (same sha256), so the snapshot the package calls
the-record-we-beat/RECORD.md was still current at my fetch time.

Hidden quantifier: the base-row absence is vacuous. The largest base row in FermQ_Sorg.txt is 10125. The only row above
10125 in FermQ_Sort.txt is 65537. Neither table has a row or a searched limit for base 36260, so this pair is not "above
Fischer's searched limit" for its base; no such limit exists. The clause still has content in that p appears nowhere in
any of the four files (ErstBasen.txt lists some large primes with all their small bases, and p is not among them).
FermQ_Sorg.txt is stated to be searched to 4.8E+12, which is above p. Its silence on p agrees with my finding that no
base 2..10125 is Wieferich for p.

## OEIS clause

One request: `https://oeis.org/search?q=1026120862861&fmt=data`, status `200` (work/out/fetch_oeis_status.txt), page
saved as work/fetch/oeis_search.txt with sha256 `5de2872d3163db421f9d6301ec0b038ec5a2a33bbe32a08bd6452a193f27993f`
(an HTML page, so it is not expected to match the scout's hash). Page text at line 116 (HTML tags stripped):
"Sorry, but the terms do not match anything in the table." The only place p occurs as a whole number on the page is the
echoed query.

The search doesn't index b-files, so a check for a b-file hiding the pair is needed. The obvious candidate is the
"smallest Wieferich prime to base n" sequence. For n = 36260 its entry would be 3, not p: my output above gives smallest
q = 3, and the Wieferich primes for base 36260 below 200000 are [3, 11, 491]. So that sequence can't carry this pair. I
know of no OEIS base-36260 Wieferich sequence, and the number search found none.

## Subsumption and null models

- Full win: does not apply (b = 36260 is above 10125). So p1 is not a weaker restatement of a full-win pair.
- Equivalence under powers: 36260 is not a perfect power, so this is not the pair of some smaller base a with b = a^k.
- Product derivation: Fermat quotients add under multiplication. Two known Wieferich bases for the same p would give a
  free "new" product pair. For this p, the only Wieferich base in 2..131072 is 36260 itself. No proper divisor of 36260
  is Wieferich for p, so the pair is not a product of smaller Wieferich bases. Also, p appears in none of Fischer's
  files, so those files give no base for p to build from.
- Double Wieferich / SwitchFermQ.txt: `python3 -I -B -c ...` (work/out/double_wieferich.txt) printed
  `p^(b-1) mod b^2 = 1209425941` and `double Wieferich: False`. So the pair can't appear in a list of double Wieferich
  pairs, and the headline flag does not apply.
- Already banked: I made one request for the V3R1T4S trophy case
  (`https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`, status `200`,
  work/out/fetch_trophy_status.txt; 100 lines). A search for `1026120862861|36260|wieferich|Wieferich|fermat|Fermat`
  found no matches. I didn't check known-knowns/ or pull requests; that is the NOVELTY skeptic's job.
- Rarity null model: the heuristic (each pair holds with probability about 1/p) gives about 51.5 expected pairs over the
  55237 non-perfect-power bases in 10126..65536 with 1e12 below p and p at most the claimed value. So pairs like this
  exist in quantity. p1 does not require rarity, though. I know of no shortcut that produces such a pair without a real
  search (each (b, p) test needs a modular exponentiation mod p^2). The win is not trivial; it is modest, which is what
  a partial win is.

## Scope limits (what this panel does NOT confirm)

- Not a full win, and not a new pair "beyond the searched limit" for any base: no Fischer limit exists for base 36260.
- Not the smallest Wieferich prime to base 36260 (that is 3).
- "Absent" is checked only against the four Fischer files and the OEIS number search named above. It is not checked
  against the wider literature or against unpublished searches.

confirmed_scope: The pair in object/pair.json (b = 36260, not a perfect power, strictly between 10125 and 65537; p = 1026120862861, proven prime and above 1e12) satisfies 36260^(p-1) == 1 mod p^2 in exact integer arithmetic, and neither p nor a row for base 36260 appears in the Fischer files or the OEIS search recorded in the-record-we-beat/RECORD.md, which meets partial win p1 only (not the full win, and not a beyond-searched-limit result, since those tables give no row or limit for base 36260).

pass: true
