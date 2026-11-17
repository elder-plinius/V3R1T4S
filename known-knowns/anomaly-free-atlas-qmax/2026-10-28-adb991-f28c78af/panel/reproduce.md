# REPRODUCE skeptic: anomaly-free-atlas-qmax (SMnuR 19, SM 32..35)

context: subagent (fresh context, Claude Code Agent tool)

Inputs read: only claim/ (CLAIM.md, REPRODUCE.md, status.md, object/, checker/, source/). Work directory: panel_work/reproduce/
(copies of claim/source and claim/checker; claim/ was never modified). Lists were streamed, never written to disk.

## 1. Definition (quoted from claim/CLAIM.md)

> Charges F_X, X in {Q_i, u_i, d_i, L_i, e_i} (SM) or also nu_i (SMnuR), i = 1, 2, 3, all-left-handed basis
> (Q:(3,2)_{1/6}, u^c:(3b,1)_{-2/3}, d^c:(3b,1)_{1/3}, L:(1,2)_{-1/2}, e^c:(1,1)_{1}, nu^c:(1,1)_{0}); sums over i:
>   SU(3)^2 U(1)_F:  sum (2 F_Q + F_u + F_d) = 0
>   SU(2)^2 U(1)_F:  sum (3 F_Q + F_L) = 0
>   U(1)_Y^2 U(1)_F: sum (F_Q/6 + 4 F_u/3 + F_d/3 + F_L/2 + F_e) = 0
>   grav^2 U(1)_F:   sum (6 F_Q + 3 F_u + 3 F_d + 2 F_L + F_e + F_nu) = 0
>   U(1)_Y U(1)_F^2: sum (F_Q^2 - 2 F_u^2 + F_d^2 - F_L^2 + F_e^2) = 0
>   U(1)_F^3:        sum (6 F_Q^3 + 3 F_u^3 + 3 F_d^3 + 2 F_L^3 + F_e^3 + F_nu^3) = 0
> (SM: drop nu.)

> Convention ("inequivalent"): count = 1 + the number of nonzero integer solutions with |F| <= Q_max and gcd 1,
> modulo independent permutations of the three families within each species and the overall sign F -> -F (the "1"
> is the all-zero assignment).

> Canonical line: species order Q u d L e [nu]; each species sorted ascending; of F and -F the lexicographically
> larger; gcd 1; nonzero; lines strictly increasing (lexicographic, as integer tuples); single spaces, "\n" line ends.

## 2. My own checker (panel_work/reproduce/mycheck.c), written before reading checker/ or source/

`mycheck QMAX NU` reads the byte stream and, for every line, requires: exactly 15/18 tokens of the form
-?(0|[1-9][0-9]*) (no "-0", no leading zeros), single spaces, "\n" terminated (a final partial line fails); |F| <= QMAX;
each species non-decreasing; gcd of all entries = 1 (so nonzero; zero reported separately); sign-canonical
F >= canon(-F) lexicographically, where canon(-F) maps each sorted species (a,b,c) to (-c,-b,-a); all six ACCs in
integer form (hypercharge one multiplied by 6: sQ + 8su + 2sd + 3sL + 6se = 0; nu enters only grav and cubic);
line strictly greater than the previous one as integer tuples. Prints `lines=N` and PASS, else FAIL with reason.

Why this certifies distinct classes: under S3^k x Z2 every class has exactly two species-sorted representatives
(F_sorted and canon(-F_sorted), possibly equal); requiring sorted + F >= canon(-F) picks exactly one, so each passing
line is the unique canonical representative of its class, and strict increase makes the lines pairwise distinct, i.e.
distinct lines = distinct classes. Completeness is NOT checkable by a line checker (verified: deleting a line still
passes both checkers); it follows from line count = count - 1 with count from an independent counter (section 5).

### Validation of mycheck

a) Brute force from the definition (panel_work/reproduce/brute.py: all species-sorted tuples in [-Q,Q], every ACC
   re-checked with exact fractions, gcd, classes = set of max(F, canon(-F)), sorted output). Output bytes compared
   with the author's listers (`cmp`) and checked by mycheck:

   | row | sorted sols incl 0 | classes | count | published (table_comparison.txt) | lister bytes == brute force | mycheck |
   |---|---|---|---|---|---|---|
   | SM 1 | 8 | 7 | 8 | 8 | yes | lines=7 PASS |
   | SM 2 | 37 | 21 | 22 | 22 | yes | lines=21 PASS |
   | SM 3 | 146 | 81 | 82 | 82 | yes | lines=81 PASS |
   | SM 4 | 489 | 250 | 251 | 251 | yes | lines=250 PASS |
   | SMnuR 1 | 60 | 37 | 38 | 38 | yes | lines=37 PASS |
   | SMnuR 2 | 727 | 357 | 358 | 358 | yes | lines=357 PASS |

b) Raw brute force with no symmetry assumption (panel_work/reproduce/rawbf.c: every ordered tuple, all ACCs checked,
   primitive nonzero solutions printed) + panel_work/reproduce/burnside.py (orbits by canonical set and by Burnside,
   sum_x |Stab(x)| / |G|, |G| = 6^k * 2):
   - SM q=1: raw primitive nonzero ordered solutions=8532, orbits by canonical set=7, by Burnside=7, count=8
   - SM q=2: raw=60642, orbits 21 / Burnside 21, count=22
   - SM q=3: raw=372978, orbits 81 / Burnside 81, count=82
   - SMnuR q=1: raw=97658, orbits 37 / Burnside 37, count=38

c) Mutation tests (panel_work/reproduce/mutate.py on SM 4 and SMnuR 2 lists, mycheck vs author's checklist):
   swap two lines, duplicate a line, replace a line by its sign partner, unsort a species, perturb one entry (ACC),
   append doubled line (bound), prepend zero line, insert a gcd-2 line in order, CRLF: both FAIL.
   Trailing space, double space, "-04" token, missing final newline: mycheck FAIL, checklist PASS (the author's
   checker is whitespace-lenient and skips blank lines; immaterial here because sha256 binds the exact bytes).
   Dropped line: both PASS (expected; completeness comes from the count). Empty stream: both PASS with 0 lines
   (seen in an aborted first launch, exit 127 of the first pipeline stage caught by pipefail) - hence pipefail and the
   line-count comparison are essential.

d) Certified rows from REPRODUCE.md through mycheck: `./csenum2 12 1 2 2` -> lines=95067545 PASS, sha256
   c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84 (expected value); `./acclist 20 0` ->
   lines=1071440 PASS, sha256 f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770 (expected value).

## 3. Full regeneration of every row (streamed; sha256, author's checklist and mycheck on the same bytes via tee)

Commands (scripts panel_work/reproduce/run_nu19.sh, run_sm.sh; `set -o pipefail`, `nice -n 10`, `timeout`):
`timeout 9000 nice -n 10 ./csenum2 19 1 40 3 | tee >(sha256sum) >(./mycheck 19 1) | ./checklist 19 1` and
`timeout 2400 nice -n 10 ./acclist $q 0 | tee >(sha256sum) >(./mycheck $q 0) | ./checklist $q 0`, q = 32..35.

| row | wall | pipestatus | sha256 (regenerated) | = counts.txt | checklist | mycheck | lines = count-1 |
|---|---|---|---|---|---|---|---|
| SMnuR 19 | 10:52:47Z-12:27:56Z (lister 5708.4 s) | 0 0 0 | 0fc9e8b841f69b7825c4de8c8ff1b987f29a2314edce997157069e0b48216f81 | yes | valid solutions: 4247050204, PASS | lines=4247050204, PASS | 4247050205-1, yes |
| SM 32 | 253 s | 0 0 0 | 3a5d7d1695cd98e6aa70ecc3c0ff9121f9312a11f0123ec6e6cec7a8ad408a07 | yes | valid solutions: 15866881, PASS | lines=15866881, PASS | 15866882-1, yes |
| SM 33 | 313 s | 0 0 0 | fab3aded0a00e3dfeedf3c45386728a3d9bd3f6bf22f748c58c0dcea7f1ee86c | yes | valid solutions: 19550224, PASS | lines=19550224, PASS | 19550225-1, yes |
| SM 34 | 376 s | 0 0 0 | e22875f7b3ded06eeb05e00464da98b943e60db7afac2d673357e1da1e72c74b | yes | valid solutions: 22847888, PASS | lines=22847888, PASS | 22847889-1, yes |
| SM 35 | 440 s | 0 0 0 | f3a6b7ff8fd4abe877c3d3f867877a811a27eb0fe3317495978f6c631a02fa9f | yes | valid solutions: 26469949, PASS | lines=26469949, PASS | 26469950-1, yes |

Lister self-reports: csenum2 "QMAX 19 NU 1: ... lines 4247050204, count(+1) 4247050205, 5708.4s";
acclist "DONE Q=32 ... count=15866881", "Q=33 ... count=19550224", "Q=34 ... count=22847888", "Q=35 ... count=26469949".
The full stream of each row was checked; no sampling.

## 4. Determinism

Every regenerated hash equals the hash recorded by the author's independent earlier run (object/counts.txt and
object/receipts/*.sha256), including the 3-thread SMnuR 19 lister: the byte streams are reproducible across runs.
No non-determinism observed. (I did not run any row twice myself; the cross-run equality is the evidence.)

## 5. Independent recount (my own counters, not mitm.c/count.c)

panel_work/reproduce/mycount.c (SM) and mycount_nu.c (SMnuR). Method:
- N(q) = number of solutions with every species sorted (= number of S3^k orbits of all bounded solutions, zero
  included): loop over species-sum tuples satisfying the linear ACCs (checked as written, hypercharge x6), then
  meet-in-the-middle on (quadratic, cubic) partial sums: SM (Q,u) table vs (d,L,e) probes; SMnuR (Q,u,d) vs (L,e,nu)
  (smaller side hashed).
- Moebius: sorted solutions all divisible by k at bound q correspond to sorted solutions at bound floor(q/k), so
  P(q) = sum_{k=1..q} mu(k) (N(floor(q/k)) - 1) = primitive nonzero sorted solutions.
- Sign: F -> canon(-F) is an involution on these P; its fixed points are tuples whose species are all (-x,0,x);
  S(q) = their number with gcd 1, enumerated directly with all ACCs checked. Burnside for Z2: orbits = (P+S)/2.
- count = 1 + (P+S)/2.

Validation: SM q=1..10 -> 8, 22, 82, 251, 626, 1983, 3902, 7068, 14354, 23800; SMnuR q=1..10 -> 38, 358, 4116, 24552,
111152, 435305, 1358388, 3612734, 9587085, 21546920: all 20 equal the published "solutions" column; moreover S+1
equals the published "symmetric solutions" column in all 20 cases (SM 8, 14, 32, 56, 114, 144, 252, 336, 492, 582;
SMnuR 16, 48, 154, 338, 796, 1218, 2332, 3514, 5648, 7540). Certified rows: SM 20 -> 1071441 (= 1071440 lines + 1),
SMnuR 12 -> 95067546 (= 95067545 lines + 1).

Results (output copied):
- SM Qmax=32 N_sorted_incl0=32403781 P=31717361 S=16401 (P+S)%2=0 count=15866882 (59.8 s)
- SM Qmax=33 N_sorted_incl0=39795028 P=39082319 S=18129 (P+S)%2=0 count=19550225 (71.3 s)
- SM Qmax=34 N_sorted_incl0=46604307 P=45676285 S=19491 (P+S)%2=0 count=22847889 (85.0 s)
- SM Qmax=35 N_sorted_incl0=53850800 P=52918349 S=21549 (P+S)%2=0 count=26469950 (114.8 s)
- SMnuR Qmax=19 N_sorted_incl0=8514120350 P=8494014927 S=85481 (P+S)%2=0 count=4247050205 (554 s)

All five equal object/counts.txt; N, P and the sign-fixed primitive numbers also coincide with the author's mitm
receipts (e.g. SMnuR 19: N 8514120350, P 8494014927, sign-fixed primitive 85481).

Why list lines = count - 1: the classes of nonzero primitive solutions are the Z2-orbits on the P sorted primitive
nonzero solutions, (P+S)/2 of them; each has exactly one canonical representative; the list holds exactly the canonical
representatives (checker) without repetition (strict order). The convention's count adds 1 for the zero assignment,
which is excluded from the list (gcd 1/nonzero). Hence lines = (P+S)/2 = count - 1, and with the independently counted
(P+S)/2 equal to the line count, the injective map lines -> classes is a bijection: the list is complete.

## 6. Mismatches / gaps

- None in the numbers: 5/5 sha256, 5/5 line counts, 10/10 checker runs PASS, 5/5 independent counts.
- The author's checklist.c accepts whitespace variants, blank lines and a missing final newline, and both checkers
  PASS an empty stream; not a defect of the certified rows (hashes bind the bytes, my strict checker passed, pipefail
  and line counts were used).
- SMnuR 19 ran 5708 s vs the author's 5191 s because of CPU contention (my other jobs and another process); the lister
  used 3 threads as in REPRODUCE.md, with the stream consumers adding some CPU beyond that. Finished at 12:27:56Z,
  before the 13:30 hard stop.
- I did not run the author's mitm.c/count.c (replaced by my own counters); the lister sources were not audited line by
  line (not needed: their output was verified in full).

pass: true
