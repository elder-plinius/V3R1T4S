# Panel: REPRODUCE skeptic

context: subagent (fresh, saw only claim/)

Scope: only files under claim/ were read (CLAIM.md, status.md, REPRODUCE.md, object/counts.txt). The author's
source/csenum2.c was compiled and run as a black box (never read); source/count.c, count2.c, fix.py,
conventions.py and checker/ were not read or used. My own checker and counter were written from CLAIM.md's
definitions before any author code was looked at.

## Definition used (quoted from CLAIM.md)

> Charges F_X, X in {Q_i, u_i, d_i, L_i, e_i, nu_i}, i = 1, 2, 3, all-left-handed basis (Q:(3,2)_{1/6},
> u^c:(3b,1)_{-2/3}, d^c:(3b,1)_{1/3}, L:(1,2)_{-1/2}, e^c:(1,1)_{1}, nu^c:(1,1)_{0}); sums over i:
>   SU(3)^2 U(1)_F:  sum (2 F_Q + F_u + F_d) = 0
>   SU(2)^2 U(1)_F:  sum (3 F_Q + F_L) = 0
>   U(1)_Y^2 U(1)_F: sum (F_Q/6 + 4 F_u/3 + F_d/3 + F_L/2 + F_e) = 0
>   grav^2 U(1)_F:   sum (6 F_Q + 3 F_u + 3 F_d + 2 F_L + F_e + F_nu) = 0
>   U(1)_Y U(1)_F^2: sum (F_Q^2 - 2 F_u^2 + F_d^2 - F_L^2 + F_e^2) = 0
>   U(1)_F^3:        sum (6 F_Q^3 + 3 F_u^3 + 3 F_d^3 + 2 F_L^3 + F_e^3 + F_nu^3) = 0

> Convention ("inequivalent"): count = 1 + the number of nonzero integer solutions with |F| <= Q_max and gcd 1,
> modulo independent permutations of the three families within each species and the overall sign F -> -F (the "1"
> is the all-zero assignment).

> Canonical line: species order Q u d L e nu; each species sorted ascending; of F and -F the lexicographically
> larger; gcd 1; nonzero; lines strictly increasing (lexicographic, as integer tuples); single spaces, "\n" line ends.

For the SM rows (no nu) the nu terms are dropped. I re-derived the anomaly coefficients from the quoted
representations (multiplicity x charge factors: Q 6, u^c 3, d^c 3, L 2, e^c 1, nu^c 1; Y^2 and Y weights) and they
agree with the six equations above. The basis remark holds: F_X -> -F_X for one species is a bijection of the box |F| <= Q_max, and
the ACCs written with that species conjugated are the same equations with F_X negated.

## My code (scratchpad only; not part of claim/)

- mycount.c (own counter, own algorithm): the four linear ACCs fix all species sums from (S_Q, S_u)
  (S_d = -2S_Q - S_u, S_L = -3S_Q, S_e = 2S_Q - S_u, S_nu = 4S_Q + S_u; SM: S_u = -4S_Q). For each (S_Q,S_u) it
  joins all sorted (Q,u,d) multiset triples against all sorted (L,e,nu) triples on the exact (quadratic, cubic)
  partial sums with a hash table: every multiset of every species is enumerated (exhaustive). Then
  Burnside for the sign (orbits = ((S-1)+(Sym-1))/2, Sym = species of form {-x,0,x} with
  xQ^2 - 2xu^2 + xd^2 - xL^2 + xe^2 = 0, nu free) and Moebius for gcd 1 (P(Q) = sum_d mu(d) O(floor(Q/d))),
  count = 1 + P.
- mycheck.c (own streaming checker): per line: exact token format (single spaces, '\n', no leading zeros/-0),
  number of entries, |F| <= Q, each species ascending, nonzero, gcd 1, sign canonical (line >= sorted form of
  -F, integer-tuple lexicographic), all six ACCs exactly (integer form of the Y^2 equation x6), strict
  lexicographic increase over the previous line; at end: stream ends in '\n', line count == expected, nonzero.
  Prints PASS only if all hold.
- brute1.py: naive brute force of the definition (explicit orbit set) for SMnuR Q_max 1.

## Checks and results (copied from command output)

1. Counter calibration vs status.md (published values):
   - SM: `QMAX 1 NU 0 count(incl zero) 8`, `QMAX 3 ... 82`, `QMAX 5 ... 626`, `QMAX 7 ... 3902`, `QMAX 10 ... 23800`
     -> all 5 match.
   - SMnuR: `QMAX 6 NU 1 count(incl zero) 435305`, `QMAX 7 ... 1358388`, `QMAX 8 ... 3612734`,
     `QMAX 9 ... 9587085`, `QMAX 10 ... 21546920` -> all 5 match.
   - Brute force SMnuR Q_max 1: `brute SMnuR q=1 count incl zero: 38` vs mycount `QMAX 1 NU 1 count(incl zero) 38`.
2. Counter on the claimed rows (exhaustive, single thread):
   - `q=17 NU=1 sorted_incl0=3294219380 sym_incl0=61488 orbits_nonzero=1647140433 (204.9s)`
     `QMAX 17 NU 1 count(incl zero) 1643386480 list_lines 1643386479` -> equals object/counts.txt (1643386480).
   - `QMAX 18 NU 1 count(incl zero) 2720672222 list_lines 2720672221` -> equals object/counts.txt (2720672222).
3. Lister (source/csenum2.c, compiled `gcc -O2 -fopenmp`) on the known rows of REPRODUCE.md:
   - `./csenum2 12 1 2 2`: `95067545` lines, `c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84` -> matches.
   - `./csenum2 20 0 3 2`: `1071440` lines, `f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770` -> matches.
   - Cross-check of these rows by my tools: mycount `QMAX 12 NU 1 count(incl zero) 95067546` and
     `QMAX 20 NU 0 count(incl zero) 1071441`; mycheck on SMnuR 12 stream (3 threads): `lines: 95067545 expected:
     95067545 errors: 0 PASS`; on SM 20: `lines: 1071440 expected: 1071440 errors: 0 PASS`; on SMnuR 6:
     `lines: 435304 expected: 435304 errors: 0 PASS`.
4. Checker negatives (on the SM 20 list and again on the SMnuR 6 list; each must FAIL):
   - dropped line: `lines: 1071439 expected: 1071440 errors: 0 FAIL` (SMnuR 6: `lines: 435303 ... FAIL`)
   - duplicated line: `bad flags 64` (order) `FAIL`
   - swapped adjacent lines: `bad flags 64` `FAIL`
   - wrong sign choice (line replaced by canonical form of -F): `bad flags 96` (sign + order) `FAIL`
   - gcd 2 (a line doubled): `bad flags 72` (gcd + order) `FAIL`; SMnuR 6: `bad flags 9` `FAIL`
   - altered entry (last entry +1): `bad flags 16` (ACC) `FAIL`; SMnuR 6 (nu entry): `bad flags 17` `FAIL`
   - empty stream: `lines: 0 expected: 1071440 errors: 0 FAIL`
   - missing final newline: `stream does not end with newline` `FAIL`
   - unmodified list: `PASS`.
5. Full lists, streamed (never stored), `set -o pipefail`, one stream tee'd into sha256sum, wc -l and mycheck:
   - SMnuR 17 (`./csenum2 17 1 16 3`):
     `lines: 1643386479 expected: 1643386479 errors: 0` `PASS` `pipeline rc=0`
     `sha256: 385eb5abe1adb8107c6d678374555095202c3c7fcae17316f8334730d5e61023` `wc -l: 1643386479`
     -> line count and sha256 equal object/counts.txt.
   - SMnuR 18 (`./csenum2 18 1 25 3`):
     `lines: 2720672221 expected: 2720672221 errors: 0` `PASS` `pipeline rc=0`
     `sha256: ba766218c78ca20f29c48f2bb677bca4a31235f398638ba317315b7bf8994d3c` `wc -l: 2720672221`
     -> line count and sha256 equal object/counts.txt.
6. Determinism: SMnuR 17 regenerated a second time with a different pass split (`./csenum2 17 1 20 3`, NPASS 20
   instead of 16), streamed into sha256sum and wc -l: `det pipeline rc=0`,
   `det sha256: 385eb5abe1adb8107c6d678374555095202c3c7fcae17316f8334730d5e61023`, `det wc -l: 1643386479`
   -> identical to the first run and to object/counts.txt. (Thread count was 3 in both runs; SMnuR 12 also gave the
   certified hash with 2 threads/2 passes, and passed my checker with 3 threads.)

## Conclusion

Both rows are fully reproduced: for SMnuR Q_max 17 and 18 my own exhaustive counter gives exactly the claimed
counts (1643386480, 2720672222), the regenerated lists have exactly count-1 lines and the sha256 values recorded
in object/counts.txt, and my own checker confirms on the same bytes that every line is a nonzero, gcd-1,
sign- and permutation-canonical solution of all six ACCs with |F| <= Q_max, strictly increasing (hence pairwise
inequivalent); with the independent count equal to the line count, each list is complete. The convention
reproduces all 10 published calibration values in status.md (which are themselves only search-tool text, as
status.md states; the published table was not fetched). No mismatch, missing object or non-determinism found.

Notes: all jobs ran under nice -n 10 (counter nice 19), at most 3 lister threads; peak lister RSS about 3.2 GB;
only my own PIDs were started and none had to be killed. Other processes (`csenum2 12 1 2 1`, `count`) seen
running on the machine were not mine and were not touched.

pass: true
