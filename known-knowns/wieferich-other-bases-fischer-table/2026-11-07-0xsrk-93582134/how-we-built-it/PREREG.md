> Copy of the frozen PREREG.md of the search run (run 2026-11-07-2010, frozen 2026-11-07T20:13:22Z), with one
> change for publication. In the claim-path line about submission, the angle-bracketed placeholder for the
> package id is written as SUBMISSION-ID, because the package checker rejects angle-bracketed placeholder words.
> Nothing else differs. The original file has sha256 9cc980988556a748ef58bc7c3d9d41354904f33c14603a3263d524746e22dd47.

# PREREG: run 2026-11-07-2010, target wieferich-other-bases-fischer-table

frozen_utc: 2026-11-07T20:13:22Z (date -u read immediately before writing this file). No attack output of this run
exists yet. What exists:
- the scout's fetches (data/);
- the checker selftest (attempts/skeptic-settled/code/checker_selftest.txt);
- my own break attempt on the carried-over pair, which is not attack output of this run: it was found in run
  2026-11-07-1751 (attempts/skeptic-settled/output/carry_break_attempt.txt, carry_absence_checks.txt).
The MITM pipeline selftest is still running.

## Hypotheses tested by this run
- H1 (claim): the carried-over pair (28860, 1017279755641) passes three fresh skeptics and the gate as partial win
  p1.
- H2 (sweep): new Wieferich pairs exist for the 6852 non-perfect-power 70-smooth bases 10126..65536 among the
  primes swept from 1018940000000 upward. Prior: about 2.7-3.3 expected pairs (HEURISTIC, target.md).
- H3 (tool): the exact MITM screen, used in production for the first time, returns exactly what the reference
  screen found. On run 2026-11-07-1751's two hit blocks it must return the recorded pair and the recorded q-matrix
  sha256.
- H4 (host): the sweep holds its keep-awake request (pid.txt ends with `keep_awake 0x80000003`), and the System log
  shows no modern-standby entry (Kernel-Power 506) between launch and end.
- H5 (cross-agent): an independent recompute of one random block of run 2026-11-07-1751 (seed 20261111) gives
  RESULT MATCH.

## Criterion and partial win judged (verbatim in target.md)
- Partial win p1: "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12,
  b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."
- The full win and p2 are not attempted: no base <= 10125 is swept.

## What will judge a result (fixed now)
- Exact-check threshold: `pow(b, p-1, p*p) == 1` in exact Python integers. Nothing else counts as a hit.
- Checkers: wieferich_check.py `b p 10126 65536` and break_attempt.py `b p p1 FERMQ_SORG FERMQ_SORT`.
- Novelty, stricter than the criterion's literal "both Fischer tables": the pair must be absent from FermQ_Sorg.txt,
  FermQ_Sort.txt, ErstBasen.txt and ErstPBasen.txt (fetched 2026-11-07T20:11:24Z-25Z) and from one OEIS search for
  p. It must also differ from the three submitted pairs: #973 (24766, 1000747824697), #983 (28910, 1011548897263)
  and #999 (17766, 1016845912283).
- The MITM screen is exact: a candidate is an exact zero of q_p(b) by integer equality, and every candidate is still
  re-checked with `pow(b, p-1, p*p)`.

## Claim path (fixed now)
- This run's single claim is the carried-over pair (28860, 1017279755641): claim/ (built before this file), three
  fresh Claude Code Task subagents in one message (REPRODUCE, NOVELTY, CRITERION, each seeing only claim/), then the
  gate in panel/gate.md, then a package in outbox/ and `check_run.py --package`.
- No submission in this run: a confirmed package waits for the ADMIN's "submit SUBMISSION-ID" and then "yes".
- Every exact hit of this run's sweep gets my own break attempt and is recorded as PROMISING (an exact pair awaiting
  its own panel), one per later run, because one run folder holds one claim.

## Attack plan (frozen before it runs)
- Lens object-as-data, OUTDIR attempts/object-as-data/output, 6852 bases, B = 70, blocks of 20000000, 30 workers at
  IDLE priority, exact MITM screen:
  `WIEFERICH_SCREEN=mitm wieferich_sweep.py sweep OUTDIR 1018940000000 20000000 30 DEADLINE 70 10126 65536 1500000000000`
- It launches only after `WIEFERICH_SCREEN=mitm p1_known_positives.py` prints P1_PIPELINE_SELFTEST PASS.
- DEADLINE = the launch epoch (`date +%s` read right before launch, recorded in output/launch.txt) + 1860 s. No new
  block is submitted after it; blocks in flight finish.
- Stop rule: a normal end is the final `finished_utc` line. If the pool has not ended by DEADLINE + 900 s, its
  recorded main PID (pid.txt) and worker PIDs (blocks.jsonl) are stopped by exact PID, and only completed blocks
  count. Nothing else is stopped.
- Memory (RULES 10): the MITM bench block measured a peak of 327.2 MB per worker (run 2026-11-07-1751); this run's
  selftest bench measures it again. 30 x 0.33 GB is about 9.9 GB, under half of the 43942 MB free at preflight.
- Lens skeptic-settled, beside the sweep, short jobs only:
  - the MITM positive control: rerun blocks [1016840000000, 1016860000000) and [1017260000000, 1017280000000)
    through the MITM path, one worker each, and compare with run 2026-11-07-1751's hit_block_record.json and
    hit2_block_record.json;
  - the cross-agent recompute (seed 20261111) of one random block of that run.
- Coverage statements allowed afterwards: only the maximal contiguous run of completed blocks from 1018940000000,
  stated exactly, for the 6852-base set only, labelled NUMERICAL.

## Null design
null_test: not needed because the criterion is an exact integer identity checked with exact arithmetic; no statistic is tested

## Baseline (RUN.md step 3c)
Not an empirical benchmark: no published baseline to reproduce.
