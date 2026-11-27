# REPRODUCE skeptic: A002224(42) = 6072205049848081

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Scope note: I opened only files under claim/ and my own work folder (mine/). I did not open the repository's
AGENTS.md, so that this context stayed independent. One `ps` call that I ran to check on my own job also printed
the command lines of unrelated processes (other jobs on the machine). I did not use anything from them, and after
that I queried only my own PIDs.

## Definition (quoted from claim/CLAIM.md, which quotes https://oeis.org/A002224)

"Smallest prime p of form p = 8k+1 such that first n primes (p_1=2, ..., p_n) are quadratic residues mod p."

claim/data/A002224.html contains the same string (grep), and the sha256 of both data files matches the table in CLAIM.md:
```
e8763c3a42f50f8011ac20c1eadad666f169a884c247cbbcef83653f9add4861  data/A002224.html
70fa340ea4ea5035017afad7742632f61ae03c75cafdcf7ab0e69f2b99579ce8  data/b002224.txt
```
The b-file ends at `41 178936222537081`, so n = 42 is a new index.

Claim: A002224(42) = 6072205049848081. The 42nd prime is 181.

## What I wrote before opening claim/code/ (all in mine/)

- mine/check.py: my property checker, standard library only. It runs deterministic Miller-Rabin with the first 13
  primes as bases (valid for n < 3.317e24), checks q mod 8, applies Euler's criterion pow(r,(q-1)/2,q) == 1 to each
  of the first n primes, and reports the leading-QR count and the least QNR.
- mine/enum.c: my exhaustive enumerator. It uses Bernstein-style doubly focused enumeration (two CRT lists, the
  second list sorted, then a range sweep), which is a different method from the author's single wheel:
  - list A: residues mod M1 = 8*3*5*7*11*13*17*19*23*29 = 25878772920 (|A| = 1995840)
  - list B: residues mod M2 = 31*37*41*43*47 = 95041567 (|B| = 2608200)
  - M = M1*M2 = 2459559130353965640 < 2^63. Each q = (a*e1 + b*e2) mod M, with CRT idempotents e1 and e2.
  - for each u = a*e1 mod M, the admissible v = b*e2 mod M are exactly the two contiguous ranges [0, N-u) and
    [M-u, M-u+N) of sorted B. Binary search finds each range start.
  - the remaining odd primes 53..PMAX are tested by table lookup with compile-time-constant moduli (PMAX is a
    compile flag).
  - self-checks: every residue in A and B is re-verified against every condition, the list sizes equal the product
    of (p-1)/2, A and B have no duplicates, and the CRT idempotents are verified.
- mine/post.py: re-verifies that every survivor meets every sieve condition (in Python), tests primality with
  check.py, recomputes the leading-QR count by Euler's criterion, and reports the least prime for each n against
  the b-file.
- mine/bf.c: a plain brute-force reference (every q = 1 mod 8 in a range), used only to test enum.c.
- mine/mrfilter.c: deterministic 64-bit Miller-Rabin (bases 2..37) that keeps only the primes from a list.
- mine/cert.py: a Pocklington certificate built from a full factorization of q-1.

Hashes of my sources: enum.c 08f5b6df82d7d0e0..., bf.c c28edf268155a0b3..., check.py 5199e1e9aa7cb9c3...,
post.py 832560c72b6a053c..., cert.py 845a6c5d9afc3767..., mrfilter.c d15c7383ab1b0b1c...

### Why the search is complete

Let q be prime, q = 1 (mod 8), and let p be an odd prime with p != q.
- (2/q) = +1 because q = +-1 (mod 8) (the second supplementary law).
- By quadratic reciprocity, (p/q) = (q/p)(-1)^{((p-1)/2)((q-1)/2)} = (q/p), because (q-1)/2 is even.

So "p_1..p_42 are QRs mod q" holds exactly when q mod p is a nonzero square mod p for every odd prime p <= 181.
That condition is a union of residue classes.
- If q <= 181, then q is itself one of the first 42 primes, and q mod q = 0 is excluded (Euler gives 0, not 1), as
  it should be.
- enum.c lists every integer q in [0, N) with q = 1 mod 8 that meets every class condition. The CRT map from
  A x B onto the admissible residues mod M is a bijection. Since N < M, each admissible q in [0, N) comes from
  exactly one pair (u, v), with q = u+v or q = u+v-M. The two v-ranges cover exactly those two cases.
- Primality is decided afterwards. Miller-Rabin never rejects a prime, so no prime survivor can be lost.
- Only q = 1 needs special mention: it is admissible but not prime, and it is rejected.

### Tests of enum.c against brute force (exact set equality)

The second and third windows exercise the no-wrap range (q = u+v) as well as the wrap range.
```
[1, 2e10), PMAX=53:   34011 survivors both, MATCH, sha256 51f87412ef432af6...
[1, 2e10), PMAX=61:   21218 survivors both, MATCH, sha256 2dac97c9df520e85...
window [6072185049848081,6072205049848082), PMAX=53:
  pairs_in_range=12851754464 survivors=20650 (from no-wrap range: 47) L0=6072185049848081
  MATCH, sha256 203f086d7a9dbeab86f612b31926d36192a387f4024b51fa61b0725e24dcd4f9 (both)
window [3000000000000001,3000020000000001), PMAX=61:
  pairs_in_range=6349595889 survivors=5003 (from no-wrap range: 7) L0=3000000000000001
  MATCH, sha256 d6afe82f348798c9bdc0ca922ad30332038caaf821e03a4c41efbccf2a23ebb9 (both)
```

## Calibration (from 1, same split, compiled with PMAX=113)

`nice -n 10 timeout 3600 ./enum113 178936222537082 4 cal/c113`, then `python3 post.py 113 178936222537082 ../claim/data/b002224.txt cal/c113.*.txt`:
```
pairs_in_range=378837781 survivors=1540762 (from no-wrap range: 44) L0=0
survivors=1540762 sha256(sorted)=5f0616c755f773acbbc48d4a0eb3421c40df98ed2ce0be3aec3b61a9f666de17
prime survivors=1201 non-prime survivors=1539561: [1, 16129, 17161, 18769, ...]
n=30 p_n=113 least prime < N: 196265095009  b-file: 196265095009 MATCH
n=31 p_n=127 least prime < N: 196265095009  b-file: 196265095009 MATCH
n=32 p_n=131 least prime < N: 2871842842801  b-file: 2871842842801 MATCH
n=33 p_n=137 least prime < N: 2871842842801  b-file: 2871842842801 MATCH
n=34 p_n=139 least prime < N: 2871842842801  b-file: 2871842842801 MATCH
n=35 p_n=149 least prime < N: 26437680473689  b-file: 26437680473689 MATCH
n=36 p_n=151 least prime < N: 89436364375801  b-file: 89436364375801 MATCH
n=37 p_n=157 least prime < N: 112434732901969  b-file: 112434732901969 MATCH
n=38 p_n=163 least prime < N: 112434732901969  b-file: 112434732901969 MATCH
n=39 p_n=167 least prime < N: 112434732901969  b-file: 112434732901969 MATCH
n=40 p_n=173 least prime < N: 178936222537081  b-file: 178936222537081 MATCH
n=41 p_n=179 least prime < N: 178936222537081  b-file: 178936222537081 MATCH
n=42 p_n=181 least prime < N: None  b-file: None
```
Calibration result: A002224(30..41) reproduced from 1, 12 of 12 MATCH.

Bonus run (PMAX=53, N = 196265095010): n=16..31 all MATCH, from `n=16 p_n=53 least prime < N: 22000801  b-file:
22000801 MATCH` through `n=31 ... 196265095009 ... MATCH`. In that run's output, n >= 32 prints MISMATCH (None).
That is expected and not a failure: those b-file terms lie above that run's bound N.

## Property of the claimed value (mine/check.py, mine/cert.py)

```
q=6072205049848081 n=42 (p_n=181) prime=True q%8=1 all_euler_eq_1=True leading_QR_primes=44 least_QNR=197
PROPERTY OK
q=178936222537081 n=42 (p_n=181) prime=True q%8=1 all_euler_eq_1=False leading_QR_primes=41 least_QNR=181
PROPERTY FAIL
q-1 = 2^4 * 3^2 * 5 * 11 * 13 * 58976350523
  f=2: witness a=197
  [f=3, 5, 11, 13 lines omitted]
  f=58976350523: witness a=2
Pocklington (full factorization of q-1): q is PRIME
```

## Minimality: complete search over [0, 6072205049848082) with PMAX=181

Job run as `nohup ... nice -n 10 timeout 3600 ./enum181 6072205049848082 4 main/r1` (PID 7913, recorded in
mine/main/r1.pid):
```
PMAX=181 N=6072205049848082 M1=25878772920 |A|=1995840 M2=95041567 |B|=2608200 M=2459559130353965640 threads=4
pairs_in_range=12851754464 survivors=8266786 (from no-wrap range: 6926) L0=0
real	2m55.300s
```
`python3 post.py 181 6072205049848082 ../claim/data/b002224.txt main/r1.[0-3].txt`:
```
survivors=8266786 sha256(sorted)=bf5bf6ce3e7fa657e21cde4f58c7d1eaa803f9748074ac2d44ff451f9b40edff
prime survivors=1 non-prime survivors=8266785: [1, 36481, 37249, 38809, 39601, 44521, ...]
n=42 p_n=181 least prime < N: 6072205049848081  b-file: None
n=43 p_n=191 least prime < N: 6072205049848081  b-file: None
n=44 p_n=193 least prime < N: 6072205049848081  b-file: None
n=45 p_n=197 least prime < N: None  b-file: None
  prime 6072205049848081 leading_QR=44 least_QNR=197
```
Every q = 1 mod 8 below the claimed value that meets all 41 odd-prime conditions is composite or 1. The claimed
value is the only prime survivor, so it is the least prime with the property.

Determinism: I reran the job with 3 threads (PID 11596). It printed the same `pairs_in_range=12851754464
survivors=8266786 (from no-wrap range: 6926)`, and the sorted survivor sha256 was identical:
`bf5bf6ce3e7fa657e21cde4f58c7d1eaa803f9748074ac2d44ff451f9b40edff`.

## Author's code and REPRODUCE.md (read only after all of the above)

I read claim/code/check_a002224.py, claim/code/wheel.c and claim/code/analyze.py. The method is a wheel mod
8*3*...*31 = 802241960520 with 29937600 residues, branchless byte tables for 37..47, q % p for 53..113, and a
base-2 Fermat filter (which never drops a prime). The analysis recomputes the leading-QR count with Euler's
criterion. I found no logic error. One minor point: wheel.c's residue sanity check samples only every 9973rd
residue. That does not matter, because the set comparison below independently confirms its output.

I reran the REPRODUCE.md steps, writing outputs into mine/author_run/ so that claim/ stayed unmodified:
```
q=6072205049848081 n=42 prime=True q%8=1 least_qnr=197 property=True
q=178936222537081 n=42 prime=True q%8=1 least_qnr=181 property=False
M=802241960520 residues=29937600
periods=7570 candidates~2.266e+11
DONE survivors=56025 X=6072205049848081          (real 4m19.734s, PID 12500)
primes among survivors: 56022
[lines n=30..n=41 omitted here: all twelve end in MATCH, with the same values as my calibration]
n=42 least_prime=6072205049848081 NOT IN BFILE
n=43 least_prime=6072205049848081 NOT IN BFILE
n=44 least_prime=6072205049848081 NOT IN BFILE
bfile terms <= X not found: []
CALIBRATION PASS
```

Cross-check between the two enumerators: I ran my enumerator with PMAX=113 to the same bound
(`./enum113 6072205049848082 4 x113/s`, PID 12684: `pairs_in_range=12851754464 survivors=9168642`) and kept the
primes with mine/mrfilter. I applied the same filter to the author's survivors.
```
  56022 x113/mine_primes.txt
  56022 x113/author_primes.txt
5909e7371a3e6a9ff24690b0c2db6be387a1526e13778cb8fe35a37eb303190e  (both files)
IDENTICAL prime sets (odd primes <= 113 QR, q <= claimed value)
```
My Euler-criterion pass over those 56022 primes printed `with >=42 leading QR primes: [(6072205049848081, 44, 197)]`
and `max leading QR among q < claimed: 41`.

Differences from the author: none in any result.
- I did not rerun the author's search to 1e16. claim/result/author_analysis_1e16.txt reports
  `primes among survivors: 95181` for that range; it is not needed for this claim and I did not verify it.
- claim/result/a002224_42.json gives `first_n_primes_QR: 44` and `least_qnr: 197`. Both agree with my checker.

## Verdict

I confirm the full claim:
- 6072205049848081 is prime (deterministic Miller-Rabin and a Pocklington certificate) and is 1 mod 8.
- Euler's criterion gives 1 for all 42 primes 2..181, and 197 is its least QNR.
- A complete, deterministic, brute-force-validated doubly focused CRT search over every q = 1 mod 8 below it
  found no smaller prime with the property.
- The enumerator reproduces A002224(30..41), and also 16..31, from 1.
- The author's independent wheel gives the identical prime set at level 113 up to the claimed value.

pass: true
