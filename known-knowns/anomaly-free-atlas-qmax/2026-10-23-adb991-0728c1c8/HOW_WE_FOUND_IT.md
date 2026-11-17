# How we found it (contributor text, unverified)

**Brief.** This run (2026-10-20) resumed a live lead on the census. Earlier runs had pinned the atlas convention,
certified lists up to SMnuR Q_max 16, and counted SMnuR 17 and 18 without lists. The obstacle was memory: the
second lister (`csenum.c`) split its work into passes on the first canonical charge, and one value of that charge
holds too many solutions at Q_max 17. The run before (2026-10-19) wrote `csenum2.c`, which splits passes on the
first two canonical charges (q1, q2) and gives byte-identical output on the certified rows, but its SMnuR 17 stream
was stopped by its own 2-hour timeout at 81%, so no row was claimed then. The pre-registration
(`how-we-built-it/PREREG.md`, frozen 2026-10-20 08:18:25 UTC before any attack output of the run) required: the full
list streamed through the C checker with PASS and "valid solutions" = count - 1, its sha256 recorded, and agreement
with at least two independent counters; rows that do not finish are not claimed.

**What worked.**
- *extender*: `csenum2 17 1 16 3` (16 passes, 3 threads) streamed through `checklist`: PASS, 1643386479 lines in
  1301 s; `csenum2 18 1 25 3`: PASS, 2720672221 lines in 2357 s; the sha256 of each stream is in
  `object/counts.txt`. Both counts + 1 agree with the counters of earlier runs (count.c/count2.c, rcount.c, mitm.c).
- *contrarian*: tried to break `csenum2.c`. A written argument that every solution is emitted in exactly the pass
  that owns its (q1, q2) cell; 1714 runs over SMnuR Q_max 1..9 and SM 1..15 with many pass counts, all identical to
  the single-pass output, which is byte-identical to a definition-level brute force at small Q_max; planted bugs
  (mutants) were caught, so the tests have power; alternate builds (-O0, -O3, sanitizers) gave identical output.

**What failed.** The contrarian found one robustness flaw, not a wrong list: with an absurd number of passes
(NPASS >= 2e8) the lister crashes with empty output, and both checkers print PASS on empty input. Hence
`set -o pipefail` and a comparison of the line count with the expected count are required; the run, the panel and
`verify-it-yourself/run_checks.sh` (which checks the lister's exit status and compares counts) do both. SMnuR 19
(about 1 hour more) was not started in this run so the panel could finish within the budget, and per-pass hashes for
partial re-checks were not implemented.

**Panel.** REPRODUCE (own counter and own checker written from the definition before reading any code) regenerated
both lists in full with `pipefail`, got the claimed line counts and sha256 values, and regenerated SMnuR 17 a second
time with 20 passes (same hash); CRITERION passed on 2026-10-20; NOVELTY could not read the table and returned
PENDING STATUS CHECK (`panel/novelty_round1_pending.md`), so the gate wrote PROMISING. On 2026-10-23 the workspace
owner supplied the paper (v5) and the erratum as PDFs; a fresh NOVELTY skeptic read them (largest published Q_max is
10 for both contents) and passed, all 40 published numbers were matched by the counters, and the gate's second round
wrote CONFIRMED_SOLUTION (`panel/gate.md`).
