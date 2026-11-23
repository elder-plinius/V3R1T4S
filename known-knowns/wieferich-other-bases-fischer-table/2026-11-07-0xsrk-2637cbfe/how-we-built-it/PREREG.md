> Copy of the frozen PREREG.md of the search run (run 2026-11-07-2158, frozen 2026-11-07T22:00:35Z), with one
> change for publication. In the claim-path line about the panel folders, a local absolute path is replaced by
> a description, because the package must not publish local user paths. Nothing else differs. The original file
> has sha256 a78b41c49ad193eb56c06dd2845dc224aa65f14b8febf1d0ee22c3be0699e366.

# PREREG: run 2026-11-07-2158, target wieferich-other-bases-fischer-table

frozen_utc: 2026-11-07T22:00:35Z (date -u read immediately before writing this file).

No claim/ exists yet, and no attack output of this run exists. What exists is the scout's fetches (data/) and the
target notes. The pair to panel was found in run 2026-11-07-2010; my own break attempt on it from that run is in that
run's attempts/object-as-data/output/hit_1024048960667_*. claim/ is built only after this file.

## Hypotheses tested by this run
- H1 (claim): the carried-over pair (56350, 1024048960667), 56350 = 2 * 5^2 * 7^2 * 23, passes three fresh, isolated
  skeptics and the gate as partial win p1.
- H2 (sweep): new full-win pairs exist for the 2360 non-perfect-power 70-smooth bases 1053..10125 among the primes
  swept from 4826140000000 upward. Prior: about 3.35e-4 expected pairs per 2e7 block (2360 x 684561 / 4.826e12). At
  about 40-50 s per block with 30 workers for 31 minutes, that is about 0.35-0.45 pairs (HEURISTIC).
- H3 (tool): the MITM screen, now the default, runs the full-win set in production. An independent recompute
  (wieferich_recompute.py, seed 20261112) of one random block of this sweep gives RESULT MATCH.
- H4 (host): the sweep holds its keep-awake request (pid.txt shows `keep_awake 0x80000003`), and
  power_window_check.py finds no standby, sleep or plan-change event between launch and end.
- H5 (panel isolation): every isolated skeptic runs with no workspace context. Its init event shows 7 tools,
  0 MCP servers and the dontAsk mode, and `collect` finds no absolute path outside its own folder.

## Criterion and partial win judged (verbatim in target.md)
- Partial win p1 for the claim: "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above
  1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."
- The full win for any sweep hit: "an integer base 3 <= b <= 10125 that is not a perfect power ..., and a proven
  prime p not dividing b with pow(b, p-1, p^2) == 1", with p strictly above 4.8e12 (FermQ_Sorg.txt's stated limit
  for bases 1053..10125), and absent from that base's row in both files and from OEIS (target.md).

## What will judge a result (fixed now)
- Exact-check threshold: `pow(b, p-1, p*p) == 1` in exact Python integers. Nothing else counts as a hit.
- Checkers: wieferich_check.py (`b p 10126 65536` for p1, `b p` for a full win) and
  break_attempt.py (`b p p1|full FERMQ_SORG FERMQ_SORT`).
- p1 novelty: the pair must be absent from FermQ_Sorg.txt, FermQ_Sort.txt, ErstBasen.txt and ErstPBasen.txt (fetched
  2026-11-07T21:59:02Z-04Z) and from one OEIS search for p (21:59:04Z). It must also differ from the four submitted
  pairs: #973 (24766, 1000747824697), #983 (28910, 1011548897263), #999 (17766, 1016845912283) and #1008 (28860,
  1017279755641).

## Claim path (fixed now)
1. Build claim/ after this file: claim.md, object/pair.json, verify.py (templates/claim-verify.py), REPRODUCE.md,
   status_sources.md and inputs/ (the four Fischer files as fetched).
2. Run the panel isolated with scripts/headless_panel.py.
   - `prepare` puts copies in a fresh temporary folder per ROLE outside the workspace (local path withheld).
   - Three background `run` calls go out in one message. Each skeptic gets its role sentence verbatim from RUN.md
     step 6 and the run-6 panel rules, adapted to its own folder.
   - `collect` copies the files back into panel/ and prints the path audit.
   - Fallback only if the headless run fails: three Task subagents, with the preload disclosed.
3. Gate in panel/gate.md, then the full `check_run.py` on the workspace BEFORE any package.
4. If the status stands: package in outbox/, then `check_run.py --package`.
5. No submission in this run without the ADMIN's explicit yes for that package.
6. Any exact hit of this run's sweep gets my own break attempt and is recorded as PROMISING (one claim per run).

## Attack plan (frozen before it runs)
- Lens frontier-archivist, OUTDIR attempts/frontier-archivist/output, 2360 bases, B = 70, blocks of 20000000,
  30 workers at IDLE priority, default (MITM) screen:
  `wieferich_sweep.py sweep OUTDIR 4826140000000 20000000 30 DEADLINE 70 1053 10125 6000000000000`
- It launches only after the checker selftest and `wieferich_sweep.py selftest FermQ_Sorg.txt 70 6` through the
  default path print PASS. The pre-switch validation of the MITM screen on this base set is copied into
  output/mitm_default_validation/.
- DEADLINE = the launch epoch (`date +%s` read right before launch, recorded in output/launch.txt) + 1860 s. No new
  block is submitted after it; blocks in flight finish.
- Stop rule: a normal end is the final `finished_utc` line. If the pool has not ended by DEADLINE + 900 s, its
  recorded main PID (pid.txt) and worker PIDs (blocks.jsonl) are stopped by exact PID, and only completed blocks
  count. Nothing else is stopped.
- Memory (RULES 10): the MITM full-win block peaked at 288.7 MB on one worker. 30 x 0.29 GB is about 8.7 GB, under
  half of the 43755 MB free at 22:00Z.
- Coverage statements allowed afterwards: only the maximal contiguous run of completed blocks from 4826140000000,
  stated exactly, for the 2360-base set only, labelled NUMERICAL.

## Null design
null_test: not needed because the criterion is an exact integer identity checked with exact arithmetic; no statistic is tested

## Baseline (RUN.md step 3c)
Not an empirical benchmark: no published baseline to reproduce.
