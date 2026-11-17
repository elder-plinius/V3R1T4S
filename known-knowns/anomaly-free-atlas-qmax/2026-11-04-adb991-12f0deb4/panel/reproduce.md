# REPRODUCE skeptic: anomaly-free-atlas-qmax (run 2026-11-03-0919)

Scope: only the claim folder was read (CLAIM.md, REPRODUCE.md, status.md, object/, source/, checker/). Claim files
are named relative to claim/. My own working files (checker, counters, logs) are in the run's
panel_work/reproduce/ folder; every file I used there was written in this session (some names coincide with
files tracked in git from an earlier attempt; I did not read those versions).

## Order of work

1. Read CLAIM.md, REPRODUCE.md, status.md, object/counts.txt, object/receipts/ (outputs only).
2. Wrote my own streaming checker `mycheck.c` from the definition below, BEFORE opening checker/ or source/
   (sha256 of my checker source: ffed7cdecf477a5f33e595ec5bd7d10d7582f220349c37b0228b50e2f6d5b59b).
3. Compiled the author's tools as in REPRODUCE.md, without reading them: source/csenum2.c, source/acclist.c,
   checker/checklist.c, source/mitm.c (count.c was not run: ~10 GB, forbidden by the machine limits).
4. Regenerated all four lists in full, streamed (never stored), with `tee` feeding `sha256sum` and my checker the
   same bytes, under `set -o pipefail`:
   - `./csenum2 20 1 80 3 | tee >(sha256sum) | ./mycheck 20 1` (3 threads, 7053 s)
   - `./acclist Q 0 | tee >(sha256sum) | ./mycheck Q 0` for Q = 36, 37, 38 (fourth core)
5. Ran the author's independent counter source/mitm.c on all four rows.
6. Additionally wrote two counters of my own from the definition (not from the author's code) and ran them on all
   four rows and on the published range (details below).

## Definition implemented (quoted from CLAIM.md)

> Charges F_X, X in {Q_i, u_i, d_i, L_i, e_i} (SM) or also nu_i (SMnuR), i = 1, 2, 3 [...] sums over i:
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

My checker (`mycheck`, C) verifies on every line: exact byte format (integers `0` or `-?[1-9][0-9]*`, exactly one
space between fields, `\n` terminator, exactly 15 / 18 fields; it is stricter than checker/checklist.c, which skips
blank lines and accepts tabs); |F| <= Q_max; all six equations in exact integers (hypercharge one multiplied by 6:
sum(F_Q + 8F_u + 2F_d + 3F_L + 6F_e) = 0); nonzero; gcd 1; each species block sorted ascending; the line is >= the
canonical form of -F (negate, re-sort each species) lexicographically; strictly increasing versus the previous line.
Any defect fails the run (exit 1). Strictly increasing canonical representatives of distinct orbits means the
line count is the number of distinct inequivalent nonzero solutions listed; completeness then rests on the count
agreeing with independent counters. Negative tests (mutated charge, deleted line, duplicated line, tab separator)
all FAILed as expected.

## Proof steps re-derived

- Linear ACCs from sQ, su: sd = -2sQ - su; sL = -3sQ; se = 2sQ - su (6xY^2: sQ + 8su + 2sd + 3sL + 6se = -12sQ +
  6su + 6se = 0); snu = 4sQ + su (grav: -4sQ - su + snu = 0); SM: snu = 0 forces su = -4sQ. Matches the formulas
  stated in source/mitm.c, source/acclist.c and source/csenum2.c headers.
- Permutation orbits = tuples of sorted triples (each ACC is symmetric within a species).
- Sign quotient (Burnside, Z2): orbits = (P + Fx)/2, fixed tuples are those with every species {-a,0,a}; these
  satisfy the linear and cubic ACCs identically, leaving aQ^2 - 2au^2 + ad^2 - aL^2 + ae^2 = 0 with a_nu free.
- Primitivity by Moebius inversion over floor(Q/d): P(Q) = sum_d mu(d)(N(Q/d) - 1), likewise Fx.
- Nesting check: count(Q) - count(Q-1) must equal the number of listed lines with some |F| = Q (checked below).

## Own counters (written from the definition)

- `brute.c` (direct enumeration of sorted-triple tuples, all six ACCs checked per candidate, canonical-sign test as
  in the definition): SM Q=1..10 = 8, 22, 82, 251, 626, 1983, 3902, 7068, 14354, 23800; SMnuR Q=1..8 = 38, 358,
  4116, 24552, 111152, 435305, 1358388, 3612734. All equal the published values (source/atlas/arXiv-1812.04602v5.txt
  lines 868, 888-889 checked directly for SM 10, SMnuR 9, 10; the rest via source/atlas/table_comparison.txt) and
  the author's listers' line counts + 1 at the same Q (each list validated by mycheck).
- `mycount.c` (own meet-in-the-middle with Burnside + Moebius, hashed species subset chosen per sum-block by cost,
  so its splits differ from mitm.c's (Q,L,nu)|(u,d,e)): reproduces all 40 published values (counts and, as
  Fx+1, the symmetric-solution column, e.g. SM 10 Fx=581, SMnuR 10 Fx=7539), agrees with/without the sign
  half-plane shortcut (`nosym`), and gives SM 20 = 1071441, SMnuR 12 = 95067546.

## Certified-row lister checks (REPRODUCE.md)

- `./acclist 20 0 | sha256sum` -> f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770 (expected, match);
  mycheck: lines=1071440, PASS.
- `./csenum2 12 1 2 1 | sha256sum` -> c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84 (expected,
  match; 1 thread instead of 2, same bytes); mycheck: lines=95067545, PASS.

## Rows (all values copied from command output)

### SMnuR Q_max 20 (claimed 6465226975; lines 6465226974; sha256 4919f760...a327cf)
- pipeline: `pipeline exit 0 (7053 s)`; csenum2 stderr: `lines 6465226974, count(+1) 6465226975`
- my checker: `MYCHECK QMAX=20 NU=1 lines=6465226974 count(lines+1)=6465226975 lines_touching_bound=2218176770` / `MYCHECK PASS`
- sha256: `4919f760902d647f6406a801bf463a9fdafdbf8189f549093f00826ed3a327cf` (equals object/counts.txt)
- mitm.c: `RESULT SMnuR Qmax 20: inequivalent = 6465226975` (185 s, exit 0)
- my mycount.c: `MYCOUNT SMnuR Qmax 20: count = 6465226975 (P=12930354435 Fx=99513)`
- nesting: my mycount SMnuR 19 = 4247050205; 6465226974 - 4247050204 = 2218176770 = lines touching the bound. OK.
- verdict: PASS

### SM Q_max 36 (claimed 32457211)
- pipeline: `pipeline exit 0 (526 s)`; acclist stderr `count=32457210`
- my checker: `MYCHECK QMAX=36 NU=0 lines=32457210 count(lines+1)=32457211 lines_touching_bound=5987261` / `MYCHECK PASS`
- sha256: `7fd525fd695292d2991dbc051bf7ddf10a35b91d3e85a7a22a165e9183e52b4f` (equals object/counts.txt)
- mitm.c: `RESULT SM Qmax 36: inequivalent = 32457211`
- my mycount.c: `MYCOUNT SM Qmax 36: count = 32457211 (P=64891593 Fx=22827)`
- verdict: PASS

### SM Q_max 37 (claimed 37347334)
- pipeline: `pipeline exit 0 (637 s)`; acclist stderr `count=37347333`
- my checker: `MYCHECK QMAX=37 NU=0 lines=37347333 count(lines+1)=37347334 lines_touching_bound=4890123` / `MYCHECK PASS`
- sha256: `06de08d7c30a9ffd285529c826037f9cd90a1afb1932c243e2a82a3ba26ae5bc` (equals object/counts.txt)
- mitm.c: `RESULT SM Qmax 37: inequivalent = 37347334`
- my mycount.c: `MYCOUNT SM Qmax 37: count = 37347334 (P=74669201 Fx=25465)`
- nesting: 37347333 - 32457210 = 4890123 = lines touching the bound. OK.
- verdict: PASS

### SM Q_max 38 (claimed 42898799)
- pipeline: `pipeline exit 0 (804 s)`; acclist stderr `count=42898798`
- my checker: `MYCHECK QMAX=38 NU=0 lines=42898798 count(lines+1)=42898799 lines_touching_bound=5551465` / `MYCHECK PASS`
- sha256: `bf99b850233b5ef48594174f48779bbe1b3bded3efaf7e854153a62ab7632393` (equals object/counts.txt)
- mitm.c: `RESULT SM Qmax 38: inequivalent = 42898799`
- my mycount.c: `MYCOUNT SM Qmax 38: count = 42898799 (P=85770535 Fx=27061)`
- nesting: 42898798 - 37347333 = 5551465 = lines touching the bound. OK.
- verdict: PASS

## Determinism and limits

- Every regenerated stream hashes to the value recorded in object/counts.txt from the author's earlier run (and
  for the SM rows also an earlier day per CLAIM.md), so the listers are byte-deterministic across runs, thread count
  (SMnuR 12 at 1 vs 2 threads) and pass split.
- Not done: count.c (third counter) was not run (memory limit); the author's checker/checklist.c was compiled but not
  run on the big streams (my own checker is the validator here; it is stricter on format).
- A first run of my mycount.c with a 5e6 hash cap was too slow and was killed (my own PID); it was rerun with a
  1.2e7 cap; that rerun produced all numbers above. No numbers came from the killed run.

context: subagent (fresh context, Claude Code Agent tool)
pass: true
