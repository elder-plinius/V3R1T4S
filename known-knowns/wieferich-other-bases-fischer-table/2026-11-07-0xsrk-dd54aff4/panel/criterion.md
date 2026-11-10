role: CRITERION
context: hermes delegation (delegate_task subagent, fresh context, saw only claim/)

# CRITERION skeptic: wieferich-other-bases-fischer-table, partial win p1

**Object** (`claim/object/pair.json`): `{"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 24766, "p": 1000747824697}`. This is one pair, the one named in `claim.md`.

**Criterion, read literally.** This is p1 as quoted in `claim.md`. I could not compare the quote with the bank file, because that file is outside `claim/`.

> New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS.

**Method.** I read only `claim/` and made one OEIS request. My own code and raw outputs are in `panel/work-criterion/` (python 3.14.7, standard library only, nothing reused from `verify.py`): `arithmetic.py`, `inspect_tables.py`, `table_rows.py`, `absence_check.py`, `coverage_and_checker_controls.py`, `base65537_check.out.txt`, plus the OEIS record `oeis_request_record.txt` and the response body `oeis_search_1000747824697.txt`. Every block below is pasted from those runs.

## Clause by clause

### C0. "pair": p must be a prime that does not divide b
This is implicit in a Wieferich pair; the target's full criterion says "a proven prime p not dividing b". I proved primality twice without Miller-Rabin: by trial division up to isqrt(p), and by a Lucas n-1 certificate.
```
isqrt(p) = 1000373 | isqrt(p)^2 <= p < (isqrt(p)+1)^2: True
trial division: prime = True, trial divisors used = 500187, 0.05 s
p - 1 = 2^3 * 3^4 * 881 * 1321 * 1327 | product check: True | each factor prime (trial division): True
Lucas n-1 certificate: witness a = 5 | a^(p-1) mod p = 1 | a^((p-1)/q) mod p for q | p-1: {2: 1000747824696, 3: 692861880170, 881: 482512563863, 1321: 856733977312, 1327: 986727024230}
b mod p = 24766 | p divides b: False
```
**Met.**

### C1. "for a base 10125 < b < 65537" (strict on both sides)
```
10125 < b: True | b < 65537: True | b - 10125 = 14641 | 65537 - b = 40771
```
**Met.** b is on neither excluded boundary. The upper boundary, 65537, is the one extra base of FermQ_Sort.txt (see C5).

### C2. "that is not a perfect power"
Checked with exact integer roots and a factorisation, no floats:
```
factorisation of b: 2 * 7 * 29 * 61 | product check: True
gcd of exponents: 1 -> perfect power iff gcd >= 2: False
exact k-th roots, k = 2 .. 15 -> c with c^k == b: none
```
**Met.** b is squarefree. The full criterion's rule that b = a^k gives the same pair as a therefore cannot fold this pair into a smaller base.

### C3. "with p above 1e12"
```
p > 10**12: True | p > 1e12 (float literal): True | p - 10**12 = 747824697
```
**Met, strictly.**

### C4. "b^(p-1) == 1 mod p^2 checked exactly"
I computed this three independent ways, all in exact integer arithmetic:
```
p^2 = 1001496208635777443141809
built-in pow(b, p-1, p^2)          = 1
hand-rolled square-and-multiply    = 1
product over prime factors of b    = 1
pow(b, p, p^2) == b: True
Fermat quotient q_p(b) mod p = 0
q_p of the prime factors of b mod p: {2: 231556755366, 7: 206995164662, 29: 98138082196, 61: 464057822473} | sum mod p = 0 | any factor individually 0: False
trivial solution? b mod p^2 in {1, p^2-1}: False | b mod p == 1: False
```
**Met, and not by a trivial solution.** The claimant's `verify.py` also uses exact `pow` with modulus `p * p`.

### C5. "absent from both Fischer tables"
"Both Fischer tables" means FermQ_Sorg.txt and FermQ_Sort.txt, the two files named in the target's full criterion. The copies in `claim/inputs/` hash to the values recorded in `status_sources.md`:
```
file: FermQ_Sorg.txt
bytes: 288459
sha256: 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
  11|Die Basen sind gegenwaertig durchsucht bis 4.8E+12
10167|21.10.2026  Richard Fischer
file: FermQ_Sort.txt
bytes: 33141
sha256: bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
 1025|65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)
```
Which bases have rows in the two tables:
```
Sorg base-row block: lines 14 to 10013 | rows: 10000 | equals the non-perfect-powers 2..10125 ( 10000 ): True
Sort base rows (P: / keine gefunden): 1011 | equals non-perfect-powers 2..1052 ( 1010 ) plus 65537: True
any base row in 10125 < b < 65537 in either file: none
```
I searched each file for the base and the prime four ways:
1. base rows, including Sorg's "Basis: ... P: ..." proximity lines;
2. whole digit tokens;
3. raw substrings;
4. a digit stream with every non-digit deleted, so that no separator or line wrap can hide the prime.

```
FermQ_Sorg.txt
row for base 24766: none
token == '24766': 0 | token == prime: 0
13-digit tokens: 549 | 13-digit tokens within 1e10 of p: [1000436194319, 1002205496401, 1002545906249, 1003364577899, 1006363479007, 1007840228201, 1008360911707, 1010499405017]
raw substring prime occurrences: 0
raw substring '24766' occurrences: 0 []
substring '747824697' occurrences: 0
digit stream length: 178499 | prime in digit stream: False
FermQ_Sort.txt
row for base 24766: none
token == '24766': 0 | token == prime: 0
raw substring prime occurrences: 0
raw substring '24766' occurrences: 0 []
substring '747824697' occurrences: 0
digit stream length: 18741 | prime in digit stream: False
```
The search is not blind. It finds the 13-digit primes Sorg does list near p, and two of them trace back to rows whose pairs pass the congruence (b=6113, p=1000436194319 and b=7629, p=1002205496401; see Null models).

The conclusion also holds without trusting the copies. A table row lists primes p' with b'^(p'-1) == 1 mod p'^2 for its base b'. For this p, no base from 2 to 65537 other than 24766 has that property (scan below), so no row of the genuine files could hold p either.

**Met** for the copies in `claim/inputs/`. I did not re-fetch the files, because I was not cleared to, and p1, unlike the full win, does not require a re-fetch. The base-row absence is structural, since neither table has any base in (10125, 65537). The real content of the clause is that p appears nowhere in either file.

### C6. "and OEIS"
I made one request and did not retry:
```
url=https://oeis.org/search?q=1000747824697&fmt=data
user_agent=V3R1T4S-research-kit (criterion panel skeptic; single OEIS novelty lookup)
request_start_utc=2026-11-07T12:24:27Z
request_end_utc=2026-11-07T12:24:27Z
curl_exit=0
http_code=200 size_download=6737 url_effective=https://oeis.org/search?q=1000747824697&fmt=data num_redirects=0
server_date_header=Date: Sat, 07 Nov 2026 12:24:26 GMT
status_line=HTTP/1.1 200 OK
body_sha256=1aea8d92ebd66d4615138144792da5a24e4781129b0c2cb912c03344d2061c68
```
Result line and footer, extracted from the body:
```
RESULT LINE (raw): Sorry, but the terms do not match anything in the table.
A-number links (A + 6 digits) in body: []
| Last modified November 7 07:22 EST 2026. Contains 401111 sequences.
```
**Met:** no OEIS entry matches the prime. Searching for p would catch any sequence whose indexed terms contain p, including a base-24766 Wieferich sequence that listed it. The search does not show that p is absent from OEIS b-files, which, to my knowledge, the search does not index.

My response body hashes differently from the scout's recorded hash. That is expected, because the page carries a "Last modified" stamp and a sequence count. The result line matches the text the scout quotes.

### C7. "New" (hidden quantifier)
The p1 sentence names its own novelty test ("absent from both Fischer tables and OEIS"), and the full criterion does the same ("absent from that base's row in both files and from OEIS"). Read that way, "new" is met by C5 and C6.

Read more widely, as "no prior record anywhere", it is not established by the claim folder. `status_sources.md` lists Fischer's main page and the V3R1T4S repository (TROPHY_CASE.md, known-knowns/, pull requests), but records no check of either, and I was not cleared to fetch them. I do not count this against p1 as written. It stays outside the confirmed scope and is left to the novelty check and the submission step.

## Null models
- **The object cannot be manufactured.** For a fixed prime p, the units mod p^2 with x^(p-1) == 1 form the subgroup of order p-1, so a random unit qualifies with probability 1/p. Choosing p first and solving for a b in range is hopeless; a hit takes a search, and the congruence is the whole evidence:
```
non-perfect-power bases with 10125 < b < 65537: 55237 | chance that a fixed prime p ~ 1e12 has such a base: about 5.52e-08 (a unit mod p^2 qualifies with probability 1/p)
```
- **The test discriminates.** With the same hand-rolled routine, pairs read from the Fischer data pass and the neighbouring primes of p fail:
```
  positive control  b=2      p=1093           b^(p-1) mod p^2 == 1: True
  positive control  b=2      p=3511           b^(p-1) mod p^2 == 1: True
  positive control  b=3      p=1006003        b^(p-1) mod p^2 == 1: True
  positive control  b=5      p=188748146801   b^(p-1) mod p^2 == 1: True
  positive control  b=15     p=119327070011   b^(p-1) mod p^2 == 1: True
  positive control  b=17     p=478225523351   b^(p-1) mod p^2 == 1: True
  positive control  b=6113   p=1000436194319  b^(p-1) mod p^2 == 1: True
  positive control  b=7629   p=1002205496401  b^(p-1) mod p^2 == 1: True
  negative control  b=24766  p=1000747824677  (prime) b^(p-1) mod p^2 == 1: False | q_p(b) mod p = 528675048598
  negative control  b=24766  p=1000747824707  (prime) b^(p-1) mod p^2 == 1: False | q_p(b) mod p = 228378153921
```
- **The hit is not inherited from a smaller base.** The Fermat quotient is additive mod p. The four prime-factor quotients are each non-zero and sum to 0 (C4). A scan of every base against this p:
```
bases a in 2..65536 with a^(p-1) == 1 mod p^2: [24766]  (0.83 s)
of which a <= 10125 (Fischer FermQ_Sorg range, searched to 4.8E+12 per its header): []
proper divisors d > 1 of b: [2, 7, 14, 29, 58, 61, 122, 203, 406, 427, 854, 1769, 3538, 12383] | any with d^(p-1) == 1 mod p^2: []
65537^(p-1) mod p^2 == 1: False | q_p(65537) mod p = 465281982906
```
This agrees with Sorg's header: bases up to 10125 are searched to 4.8E+12, which is above p, so the table should not contain p, and it does not.

## Full win and subsumption
- **Not a full win.** The full criterion needs 3 <= b <= 10125, and b - 10125 = 14641. The claim asks for p1 only, which is consistent with that.
- **Not subsumed by anything in `claim/`.** The folder holds one object. Neither Fischer file has a row for 24766 or contains the number p. b is not a perfect power. For this p, no other base from 2 to 65537, and in particular no divisor of b, satisfies the congruence. So the pair is neither a restatement nor a product of a tabulated pair.

## Claimant's checker
I ran it as REPRODUCE.md says, from `claim/`, and nothing was written there:
```
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 24766, p = 1000747824697, Fermat quotient q_p(b) mod p = 0
PASS
exit_status=0
--- REPRODUCE one-liner ---
1
```
It is selective. These test objects are kept in `panel/work-criterion/`:
```
  neg_next_prime.json      b=24766  p=1000747824707  exit=1 last line='FAIL' failed checks=['b^(p-1) == 1 mod p^2']
  neg_b_10125.json         b=10125  p=1000747824697  exit=1 last line='FAIL' failed checks=['10125 < b < 65537', 'b^(p-1) == 1 mod p^2']
  neg_b_65537.json         b=65537  p=1000747824697  exit=1 last line='FAIL' failed checks=['10125 < b < 65537', 'b^(p-1) == 1 mod p^2']
  neg_b_square.json        b=24649  p=1000747824697  exit=1 last line='FAIL' failed checks=['b is not a perfect power', 'b^(p-1) == 1 mod p^2']
  neg_p_composite.json     b=24766  p=1000000000001  exit=1 last line='FAIL' failed checks=['p is prime (deterministic Miller-Rabin)', 'b^(p-1) == 1 mod p^2']
  pos_claimed_pair.json    b=24766  p=1000747824697  exit=0 last line='PASS' failed checks=[]
```
`verify.py` tests the perfect-power clause with float roots plus or minus 1, which is adequate at this size; C2 uses exact integer roots instead. It does not test absence from the tables or OEIS (REPRODUCE.md leaves that as a manual step); C5 and C6 cover it.

## Not covered by this verdict
- whether the `claim.md` quote matches the bank file;
- a live re-fetch of the Fischer files;
- any Fischer file other than these two;
- OEIS b-files;
- the literature and other Wieferich databases;
- the V3R1T4S repository's trophy case, known-knowns and pull requests.

confirmed_scope: Against the p1 text as quoted in claim.md, the pair (b, p) = (24766, 1000747824697) has 10125 < b < 65537, b = 2*7*29*61 not a perfect power, p > 10^12 proven prime (full trial division and a Lucas certificate) and not dividing b, and 24766^(p-1) == 1 (mod p^2) by exact integer arithmetic, while neither claim/inputs copy of FermQ_Sorg.txt or FermQ_Sort.txt (hashes as recorded, not re-fetched) has a row for 24766 or contains p, and one OEIS search at 2026-11-07T12:24:27Z returned HTTP 200 with no match, so the object meets partial win p1 and not the full win (b > 10125); novelty against any other source, a live re-fetch of the tables and whether the quoted criterion matches the bank file are not established.

pass: true
