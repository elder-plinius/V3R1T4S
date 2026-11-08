role: REPRODUCE
context: claude code headless session (claude -p --safe-mode in a copy of claim/ outside the workspace; fresh context, saw only claim/)

# REPRODUCE skeptic: wieferich-other-bases-fischer-table, pair (b, p) = (5481, 4848813530161)

## Definition checked (quoted verbatim from claim/claim.md)

> success criterion (verbatim, bank/targets.json): CONFIRMED (full win) for each pair (b, p): an integer base 3 <= b
> <= 10125 that is not a perfect power (a pair for b = a^k with p not dividing k is the same pair as for a), and a
> proven prime p not dividing b with pow(b, p-1, p^2) == 1. The p must also be STRICTLY GREATER than that base's
> searched limit stated in the live FermQ_Sort.txt (for b <= 1052) or FermQ_Sorg.txt (for 1053 <= b <= 10125), and
> absent from that base's row in both files and from OEIS (the base-b Wieferich sequence, if one exists). All of these
> are re-fetched immediately before the claim. Each new pair counts once. Direction: maximize the number of new pairs.
> A new Mirimanoff prime (b = 3, p > 1.2e15) or a new double Wieferich pair (with p^(b-1) == 1 mod b^2 as well, absent
> from SwitchFermQ.txt) is flagged as a headline result.

Object (claim/object/pair.json, read verbatim):
`{"target_id": "wieferich-other-bases-fischer-table", "win": "full", "b": 5481, "p": 4848813530161}`

## Order of work

1. Read claim/claim.md, claim/object/pair.json, claim/status_sources.md and the saved tables in claim/inputs/.
2. Wrote my own checker, work/my_check.py (standard library only), from the definition above. I did this BEFORE
   opening claim/verify.py.
3. Ran my checker twice and an extra gmpy2 cross-check (work/gmp_check.py) twice.
4. Only then opened claim/REPRODUCE.md and claim/verify.py. I ran verify.py twice and the REPRODUCE.md one-liner twice.

Commands (each run with absolute paths and captured with `2>&1 | tee` into work/; shortened here to relative paths):

    python3 -B work/my_check.py claim                     -> work/my_check_run1.txt, work/my_check_run2.txt
    (venv python with gmpy2) -B work/gmp_check.py         -> work/gmp_check_run1.txt, work/gmp_check_run2.txt
    python3 -B claim/verify.py claim/object/pair.json     -> work/verify_run1.txt, work/verify_run2.txt
    python3 -B -c "p=4848813530161; print(pow(5481, p-1, p*p))"  -> work/oneliner_run1.txt, work/oneliner_run2.txt

Interpreter (work/python_version.txt): `Python 3.14.7`. gmpy2 run: `gmpy2 version 2.3.2 gmp GMP 6.3.0`.

## What my checker proves, and how

- **Range:** 3 <= b <= 10125. Also 1053 <= b, so FermQ_Sorg.txt is the table that sets the limit.
- **b not a perfect power, two routes:**
  (a) b factors as 3^3 * 7^1 * 29^1, the factors multiply back to b, and the gcd of the exponents is 1.
  (b) No exact integer k-th root exists for any 2 <= k <= bit_length(b), checked with an exact integer bisection root.
  Since b is not a power, the "b = a^k" equivalence clause does not apply.
- **p prime, three independent routes:**
  1. Full trial division. A composite n has a prime factor at most isqrt(n). isqrt(p) = 2202002 (checked:
     r^2 <= p < (r+1)^2). Every candidate divisor was tried: 2 and every odd d from 3 to 2202002. None divides p, so
     p is prime. This route is complete, not a sample.
  2. Deterministic Miller-Rabin with bases 2, 3, 5, 7, 11, 13, 17. This is valid for n < 341550071728321
     (Jaeschke 1993), and p is below that bound.
  3. Lucas test with a Pratt-style certificate. p-1 = 2^4 * 3 * 5 * 307 * 797 * 82571; the product is checked to equal
     p-1, and each factor is checked prime by trial division. For the witness a = 11, a^(p-1) == 1 (mod p) and
     a^((p-1)/q) != 1 (mod p) for every prime q dividing p-1. So a has order p-1, (Z/pZ)^* has p-1 elements, and p
     is prime.
  As a cross-check, gmpy2 gives `is_prime(p, 50) = True` and `is_strong_bpsw_prp(p) = True`.
- **p does not divide b:** b mod p = 5481, which is not 0.
- **Wieferich congruence, computed exactly in integer arithmetic by three routes:**
  - Python's built-in `pow(b, p-1, p^2)` gives 1.
  - My own square-and-multiply code, independent of `pow`, gives 1.
  - GMP's `powmod` gives 1.
  The Fermat quotient (b^(p-1) - 1)/p mod p is 0. For information only: the residue mod p^3 is not 1, so this is an
  ordinary p^2 pair.
- **Searched limit, read from the saved file rather than hard-coded:** claim/inputs/FermQ_Sorg.txt contains exactly
  one "durchsucht bis" line: `Die Basen sind gegenwaertig durchsucht bis 4.8E+12`. Its header covers
  `von der Basis 2 bis 10125`. Parsed exactly with Decimal, the limit is 4800000000000. p - limit = 48813530161 > 0,
  so p is STRICTLY greater than the limit. Two consistency checks pass:
  - The table has no per-row limit annotations. A grep for "(" or ">" in FermQ_Sorg.txt finds only header and
    footer lines.
  - The largest prime anywhere in the main table is 4795482544417, which is below the limit. The table's footer also
    ends at "10^12 4.8E+12".
- **Base 5481's row:** the only line matching `^\s*5481,` is line 5401: `5481,  2^3, 751787`.
  - My checker parses it as entries (2, power 3) and (751787, power 2). The p in the claim is not among them.
  - Sanity check of the parse: 5481^1 == 1 (mod 2^3) and 5481^751786 == 1 (mod 751787^2) both hold, so I read the
    table format correctly.
  - The table has 10000 rows, covering every non-perfect-power base from 2 to 10125.
- **FermQ_Sort.txt:** its header says it covers `von der Basis 2 bis 1052`. Its rows are bases up to 1052 plus 65537
  (981 rows), with no row for 5481, so p is trivially absent from base 5481's row there.
- **p absent from every saved input:** I searched all five files in claim/inputs/ (FermQ_Sorg.txt, FermQ_Sort.txt,
  ErstBasen.txt, ErstPBasen.txt, SwitchFermQ.txt) for the digit string of p, bounded so that no other digits touch
  it. A second search allowed space, dot, comma or apostrophe separators between digit groups. Neither search found
  any hit.
- **Saved inputs match the scout's record:** the sha256 of each of the five saved input files appears verbatim in
  claim/status_sources.md.
- **Headline flag, for information only:** p^(b-1) mod b^2 = 25942981, which is not 1. This is not a double
  Wieferich pair and not a Mirimanoff prime (b != 3). Neither is required for the full win.

The only non-check line in the output is `duplicate row for base 4354 at line 4284`. It is harmless. Header line 8 of
FermQ_Sorg.txt (` 4354, 669, 5185, ...`, the continuation of the "Letzte 20 mit Basen" list) happens to match my row
pattern, and the real row at line 4284 then replaces it. The row for 5481 occurs exactly once (grep: line 5401 only).

## Real output: my checker, run 1 (work/my_check_run1.txt)

```
object: {"b": 5481, "p": 4848813530161, "target_id": "wieferich-other-bases-fischer-table", "win": "full"}
CHECK object types are int: PASS b=5481 p=4848813530161
CHECK object target_id: PASS wieferich-other-bases-fischer-table
CHECK object win == full: PASS full
CHECK object matches claim.md text (b=5481, p=4848813530161): PASS
CHECK 3 <= b <= 10125: PASS b=5481
CHECK 1053 <= b (so FermQ_Sorg.txt is the governing table): PASS b=5481
factorisation of b: 3^3 * 7^1 * 29^1
CHECK factorisation of b multiplies back: PASS
CHECK b not a perfect power (gcd of exponents == 1): PASS gcd=1
CHECK b not a perfect power (no exact k-th root, 2<=k<=log2 b): PASS exact roots=[]
CHECK isqrt(p) correct: PASS isqrt(p)=2202002
CHECK p prime by full trial division up to isqrt(p): PASS divisors tried: 2 and all odd 3..2202002; smallest divisor found=None
CHECK p < 341550071728321 (Jaeschke bound for MR bases 2..17): PASS
CHECK p prime by deterministic Miller-Rabin (bases 2..17): PASS
factorisation of p-1: 2^4 * 3^1 * 5^1 * 307^1 * 797^1 * 82571^1
CHECK factorisation of p-1 multiplies back: PASS
CHECK every prime factor q of p-1 is prime (trial division): PASS
CHECK Lucas test: some a has order p-1 mod p: PASS witness a=11
CHECK p does not divide b: PASS b mod p = 5481
pow(b, p-1, p^2) builtin = 1
pow(b, p-1, p^2) own square-and-multiply = 1
CHECK b^(p-1) == 1 (mod p^2), builtin pow: PASS
CHECK b^(p-1) == 1 (mod p^2), own square-and-multiply: PASS
CHECK b^(p-1) == 1 (mod p) (Fermat, sanity): PASS
CHECK Fermat quotient q_p(b) == 0 (mod p): PASS q_p(b) mod p = 0
pow(b, p-1, p^3) = 75280445891607534169433307482715286989 (info: ==1 would mean p^3 level, Fischer notation p^3)
sha256 inputs/FermQ_Sorg.txt = 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
CHECK sha256 of inputs/FermQ_Sorg.txt matches status_sources.md record: PASS
sha256 inputs/FermQ_Sort.txt = bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
CHECK sha256 of inputs/FermQ_Sort.txt matches status_sources.md record: PASS
sha256 inputs/ErstBasen.txt = e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820
CHECK sha256 of inputs/ErstBasen.txt matches status_sources.md record: PASS
sha256 inputs/ErstPBasen.txt = 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362
CHECK sha256 of inputs/ErstPBasen.txt matches status_sources.md record: PASS
sha256 inputs/SwitchFermQ.txt = 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa
CHECK sha256 of inputs/SwitchFermQ.txt matches status_sources.md record: PASS
CHECK FermQ_Sorg.txt header covers bases 2..10125: PASS ['Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125']
FermQ_Sorg.txt 'durchsucht bis' lines: ['Die Basen sind gegenwaertig durchsucht bis 4.8E+12']
CHECK FermQ_Sorg.txt has exactly one searched-limit line: PASS
CHECK searched limit is an integer value: PASS 4.8E+12 -> 4800000000000
CHECK searched limit parsed: PASS limit=4800000000000
CHECK p STRICTLY greater than searched limit: PASS p=4848813530161 limit=4800000000000 p-limit=48813530161
duplicate row for base 4354 at line 4284
CHECK FermQ_Sorg.txt has a row for b: PASS line 5401: 5481,  2^3, 751787
row entries for b (prime, Fischer power): [(2, 3), (751787, 2)]
CHECK all row entries parsed: PASS
CHECK p absent from b's row in FermQ_Sorg.txt: PASS
CHECK row sanity: 5481^(2-1) == 1 mod 2^3: PASS
CHECK row sanity: 5481^(751787-1) == 1 mod 751787^2: PASS
CHECK largest prime in FermQ_Sorg.txt main table < stated limit (consistency): PASS max=4795482544417
CHECK FermQ_Sorg.txt rows are exactly bases 2..10125 minus perfect powers or a superset of non-powers: PASS rows=10000 first=2 last=10125
FermQ_Sort.txt row bases: count 981 max 65537 has 65537: True
CHECK FermQ_Sort.txt header covers bases 2..1052: PASS
CHECK FermQ_Sort.txt has no row for b (so p absent from b's row there): PASS row=None
CHECK p does not occur in inputs/FermQ_Sorg.txt: PASS hit lines=[]
CHECK p does not occur in inputs/FermQ_Sort.txt: PASS hit lines=[]
CHECK p does not occur in inputs/ErstBasen.txt: PASS hit lines=[]
CHECK p does not occur in inputs/ErstPBasen.txt: PASS hit lines=[]
CHECK p does not occur in inputs/SwitchFermQ.txt: PASS hit lines=[]
CHECK p (with separators) does not occur in inputs/FermQ_Sorg.txt: PASS
CHECK p (with separators) does not occur in inputs/FermQ_Sort.txt: PASS
CHECK p (with separators) does not occur in inputs/ErstBasen.txt: PASS
CHECK p (with separators) does not occur in inputs/ErstPBasen.txt: PASS
CHECK p (with separators) does not occur in inputs/SwitchFermQ.txt: PASS
info: p^(b-1) mod b^2 = 25942981 (double Wieferich pair would need 1)
CHECK status_sources.md records an OEIS search for p with 'no match': PASS
checks: 51 passed: 51 failed: 0
ALL: PASS
```

Run 2 (work/my_check_run2.txt) is byte-identical (sha256 of both outputs, work/my_check_runs_sha256.txt):

```
018ec7d202a9256f18038e192257a2a709f93282fc18ff2d10e0d8e658cfb251 *work/my_check_run1.txt
018ec7d202a9256f18038e192257a2a709f93282fc18ff2d10e0d8e658cfb251 *work/my_check_run2.txt
```

## Real output: GMP cross-check (work/gmp_check_run1.txt; run 2 identical)

```
gmpy2 version 2.3.2 gmp GMP 6.3.0
is_prime(p, 50) = True
is_strong_bpsw_prp(p) = True
powmod(b, p-1, p^2) = 1
is_power(b) = False
b mod p = 5481
p > 4800000000000 = True
(r - 1) mod p = 0 ; t = (r-1)/p mod p = 0
```

## Real output: the author's checker, claim/verify.py (work/verify_run1.txt; run 2 identical)

```
ok   3 <= b <= 10125
ok   b is not a perfect power
ok   p > 4.8e12 (the table's searched limit for bases 1053..10125)
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 5481, p = 4848813530161, Fermat quotient q_p(b) mod p = 0
PASS
```

REPRODUCE.md one-liner (work/oneliner_run1.txt and work/oneliner_run2.txt) printed `1` both times.

Determinism hashes (work/runs_sha256.txt; path prefixes shortened to work/ and claim/):

```
2db0c8000b9f51eb7953c9bbc7ef7b20e12200d48c3101184f384826fc7dff11 *work/verify_run1.txt
2db0c8000b9f51eb7953c9bbc7ef7b20e12200d48c3101184f384826fc7dff11 *work/verify_run2.txt
cd9e8c30a9e2b70b8af503f4d474519e90f123c85c41763b59538e21286df0cc *work/gmp_check_run1.txt
cd9e8c30a9e2b70b8af503f4d474519e90f123c85c41763b59538e21286df0cc *work/gmp_check_run2.txt
f1b2f662800122bed0ff255693df89c4487fbdcf453d3524a42d4ec20c3d9c04 *work/oneliner_run1.txt
f1b2f662800122bed0ff255693df89c4487fbdcf453d3524a42d4ec20c3d9c04 *work/oneliner_run2.txt
daf79cf21f8249160f431c7f4c9e8fcdbcd805edb7fd6f6df888edef463cdbae *work/my_check.py
6c3255d9ce2bf1169f86279cea04f76185ced03e57a276e572cf410eb633870e *claim/verify.py
2637cbfeedbd8ac9e0cec5f8d51e676bb7c728cde9cb518bdf0fa35d1f117732 *claim/object/pair.json
```

## Comparison with claim/verify.py

- **Agreement:** both checkers agree on all six arithmetic properties, and both find a Fermat quotient of 0.
- **Differences, none of which change the result:**
  - verify.py hard-codes `TABLE_LIMIT = 4_800_000_000_000`. My checker reads the limit from claim/inputs/FermQ_Sorg.txt
    and gets the same value.
  - verify.py proves primality only with Miller-Rabin on bases 2..37. My checker adds full trial division and a
    Lucas certificate.
  - verify.py tests perfect powers with a float root and a +-1 window. My checker uses factorisation and an exact
    integer root.
  - verify.py does not check the table-absence clauses, as its docstring says. My checker checks them against the
    saved files in claim/inputs/.

## Scope and limits of this role

- **No network:** I fetched nothing. Two clauses of the definition depend on outside sources, so I could not confirm
  them myself:
  - "absent ... from OEIS". The only evidence I had is the scout's record in claim/status_sources.md: an OEIS search
    for p, HTTP 200, with the text "Sorry, but the terms do not match anything in the table". No saved copy of that
    page is in the claim folder.
  - "re-fetched immediately before the claim". I confirmed only that the saved copies' sha256 values match the
    fetch record.
  Those live checks belong to the panel's status/novelty work, not to REPRODUCE.
- **Checked in full:** within my remit, every property and the claimed value were re-derived from the saved files.
  There was no exhaustive search to reproduce, since the claim is one explicit pair checked by direct computation.
  Every run was deterministic, nothing was missing and nothing mismatched.

## Verdict

The pair (b, p) = (5481, 4848813530161) satisfies every part of the full-win definition that I can check from
claim/:
- 3 <= b <= 10125, and b is not a perfect power.
- p is a proven prime, by trial division and by a Lucas certificate.
- p does not divide b, and b^(p-1) == 1 (mod p^2) exactly.
- p is strictly greater than the 4.8E+12 searched limit stated in the saved FermQ_Sorg.txt.
- p is absent from base 5481's row (`5481,  2^3, 751787`). p does not occur in FermQ_Sort.txt or in any other saved
  input file.

Both my checker and the author's checker pass, and each gave identical results on two runs.

pass: true
