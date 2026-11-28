# PREREG: run 2026-11-07-1508, target wieferich-other-bases-fischer-table

frozen_utc: 2026-11-07T15:11:03Z (date -u read immediately before writing this file). No attack output exists yet.
The only results so far are self-tests below the tables' limits or below 1e12
(attempts/object-as-data/code/p1_known_positives_output.txt, attempts/skeptic-settled/code/checker_selftest.txt) and
the scout's fetches (scout.md).

## Hypotheses tested by this run
- H1, p1 cell (lens object-as-data): at least one new Wieferich pair exists for one of the 6852 non-perfect-power
  70-smooth bases 10126..65536 among the primes swept from 1006300000000 upward with 30 workers. Prior expectation
  about 1.0 to 1.8 pairs (target.md). HEURISTIC.
- H2, skeptic (lens skeptic-settled): the p1 cell is not dead. No Fischer file lists pairs that make the cell or our
  coverage stale, the fresh table audit is clean, and the pipeline misses no listed pair in its regime.

## Criterion and partial win judged (verbatim in target.md)
- Partial win p1: "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12,
  b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."
- The full win and p2 are not attempted: no base <= 10125 is swept.

## What will judge a result (fixed now)
- Exact-check threshold: `pow(b, p-1, p*p) == 1` in exact Python integers. Nothing else counts as a hit.
- Checkers:
  - wieferich_check.py `b p 10126 65536` (selftest PASS);
  - the own break attempt, break_attempt.py `b p p1 FERMQ_SORG FERMQ_SORT` (selftested in run 2026-11-07-1419). It
    checks the base range, that b is not a perfect power and that p > 1e12. It proves p prime by full trial division
    and checks it with gmpy2 is_prime plus strong BPSW. It checks that p does not divide b, the exact identity and the
    additive re-derivation, that b has no row and p appears nowhere in either Fischer table, and that the pair
    differs from (24766, 1000747824697).
- Novelty, stricter than the criterion's literal "both Fischer tables":
  - p must also be absent from Fischer's ErstBasen.txt and ErstPBasen.txt (fetched 2026-11-07T15:09:43Z and
    15:09:44Z). These files list smallest bases for some primes above 1e12, and a pair listed anywhere by Fischer is
    already published.
  - One OEIS search for p (https://oeis.org/search?q=<p>&fmt=data, one request, the honest User-Agent). The reply
    "Sorry, but the terms do not match anything in the table" means p is absent.
- The tables are fetched once more before any claim if the panel's check comes more than 6 h after 15:08:57Z.
- The float64 screen is a filter with a proven no-false-negative margin (tolerance 2^-40 against a worst-case error of
  2^-47 for p < 2^43). Every flag is re-checked exactly.

## Attack plan (frozen before it runs)
- Lens object-as-data, OUTDIR attempts/object-as-data/output, 6852 bases, B = 70, blocks of 20000000, 30 workers at
  IDLE priority:
  `wieferich_sweep.py sweep OUTDIR 1006300000000 20000000 30 1794066123 70 10126 65536 1500000000000`
- Deadline: 1794066123 = 2026-11-07T15:42:03Z (the epoch read at freeze time, 1794064263, plus 1860 s). No new block
  is submitted after it; blocks already in flight (at most 2 x 30) finish.
- Stop rule: a normal end is the final `finished_utc` line. If the pool has not ended by 2026-11-07T15:57:03Z
  (deadline + 900 s), its recorded main PID (pid.txt) and worker PIDs (blocks.jsonl) are stopped by exact PID, and
  only completed blocks count. Nothing else is stopped.
- Memory (RULES 10): 458.4 MB peak per worker on a real-size p1 block (run 2026-11-07-1419; the bench line of this
  run's p1_known_positives_output.txt measures it again). 30 x 458.4 MB = 13.8 GB, under half of the 43248 MB free at
  preflight.
- Lens skeptic-settled, beside the sweep, short jobs only:
  - fischer_audit.py on the fresh FermQ_Sorg.txt;
  - parse ErstBasen.txt and ErstPBasen.txt for every listed pair with p > 1e12, and check each one against the
    dossier's coverage. A listed pair with a 70-smooth base in a covered range must appear in that run's hits, or the
    pipeline missed it.
  - replay the pipeline on a window around each listed pair above 1e12 whose base lies in one of the two smooth base
    sets;
  - recompute one random block of this run's sweep by the independent path (seed 20261109).
- Coverage statements allowed afterwards: only the maximal contiguous run of completed blocks from 1006300000000,
  stated exactly, for the 6852-base set only, labelled NUMERICAL.
- Claim path for an exact hit: own break attempt, then claim/, then three fresh Task subagents in one message, then
  the gate, then the package and `check_run.py --package`. One pair per claim. A second exact hit is recorded as
  PROMISING (an exact pair awaiting its own panel) and becomes the next run's first job. No submission in this run.

## Null design
null_test: not needed because the criterion is an exact integer identity checked with exact arithmetic; no statistic is tested

## Baseline (RUN.md step 3c)
Not an empirical benchmark: no published baseline to reproduce.
