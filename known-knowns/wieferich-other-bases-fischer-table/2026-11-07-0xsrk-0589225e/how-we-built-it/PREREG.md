# PREREG: run 2026-11-07-1751, target wieferich-other-bases-fischer-table

frozen_utc: 2026-11-07T17:56:17Z (date -u read immediately before writing this file). No attack output exists yet. The only
results so far are self-tests below the tables' limits or below 1e12 (attempts/frontier-archivist/code/
checker_selftest_output.txt, PASS; attempts/frontier-archivist/code/p1_known_positives_output.txt, running at freeze
time, and it must print P1_PIPELINE_SELFTEST PASS before the sweep starts) and the scout's fetches
(data/fetch_log.txt).

## Hypotheses tested by this run
- H1, p1 cell (lens frontier-archivist): at least one new Wieferich pair exists for one of the 6852 non-perfect-power
  70-smooth bases 10126..65536 among the primes swept contiguously from 1011700000000 with 30 workers. Prior
  expectation about 1.5 pairs (target.md). HEURISTIC.
- H2, screen (lens evaluator-first): a meet-in-the-middle screen over split smooth parts gives exactly the current
  float64 matrix screen's candidate set and costs less per prime on the 6852-base set. Judged on real blocks:
  identical candidate sets (any mismatch kills it) and a time ratio measured inside one script run under one load.
  It yields a tool, never a claim.

## Criterion and partial win judged (verbatim in target.md)
- Partial win p1: "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12,
  b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."
- The full win and p2 are not attempted: no base <= 10125 is swept.

## What will judge a result (fixed now)
- Exact-check threshold: `pow(b, p-1, p*p) == 1` in exact Python integers. Nothing else counts as a hit.
- Checkers:
  - wieferich_check.py `b p 10126 65536` (selftest PASS, code/checker_selftest_output.txt);
  - the own break attempt, break_attempt.py `b p p1 FERMQ_SORG FERMQ_SORT`. It checks the base range, that b is not
    a perfect power and that p > 1e12. It proves p prime by full trial division and checks it with gmpy2 is_prime
    plus strong BPSW. It checks that p does not divide b, the exact identity and the additive re-derivation, that b
    has no row and p appears nowhere in either Fischer table, and that the pair differs from the PR #973 pair. The
    sweep starts above 1011548897263, so the PR #983 pair cannot recur.
- Novelty, stricter than the criterion's literal "both Fischer tables":
  - p must also be absent from Fischer's ErstBasen.txt and ErstPBasen.txt (fetched by the scout, data/fetch_log.txt);
  - one OEIS search for p (https://oeis.org/search?q=P&fmt=data with P the prime, one request, the honest
    User-Agent). The reply "Sorry, but the terms do not match anything in the table" means p is absent;
  - the 100 newest pull requests (data/pulls_newest100.json) and TROPHY_CASE.md at FETCH_HEAD 06b61ea hold no claim
    for the pair.
- The tables are fetched once more before any claim if the panel's check comes more than 6 h after the scout's fetch.
- The float64 screen is a filter with a proven no-false-negative margin (tolerance 2^-40 against a worst-case error of
  2^-47 for p < 2^43). Every flag is re-checked exactly.

## Attack plan (frozen before it runs)
- Lens frontier-archivist, OUTDIR attempts/frontier-archivist/output, 6852 bases, B = 70, blocks of 20000000,
  30 workers at IDLE priority:
  `wieferich_sweep.py sweep OUTDIR 1011700000000 20000000 30 1794076320 70 10126 65536 1500000000000`
- Deadline: 1794076320 = 2026-11-07T18:32:00Z (T+41). No new block is submitted after it; blocks already in flight
  (at most 2 x 30) finish.
- Stop rule: a normal end is the final `finished_utc` line. If the pool has not ended by 2026-11-07T18:47:00Z
  (deadline + 900 s), its recorded main PID (pid.txt) and worker PIDs (blocks.jsonl) are stopped by exact PID, and
  only completed blocks count. Nothing else is stopped.
- Memory (RULES 10): 458.4 MB peak per worker on a real-size p1 block (run 2026-11-07-1419; the bench line of this
  run's p1_known_positives_output.txt measures it again). 30 x 458.4 MB = 13.8 GB, under half of the 46976 MB free at
  preflight.
- Lens evaluator-first, beside the sweep, single-process jobs only: build the meet-in-the-middle screen, validate it
  against the current screen on real blocks (identical candidate sets) and on the known positives, and time both
  inside one script run. None of its output is scored against the criterion.
- Coverage statements allowed afterwards: only the maximal contiguous run of completed blocks from 1011700000000,
  stated exactly, for the 6852-base set only, labelled NUMERICAL.
- Claim path for an exact hit: own break attempt, then claim/, then three fresh hermes delegations (one delegate_task
  call with three tasks), then the gate, then the package and `check_run.py --package`. One pair per claim. A second
  exact hit is recorded as PROMISING (an exact pair awaiting its own panel) and becomes the next run's first job. No
  submission in this run.

## Null design
null_test: not needed because the criterion is an exact integer identity checked with exact arithmetic; no statistic is tested

## Baseline (RUN.md step 3c)
Not an empirical benchmark: no published baseline to reproduce.
