# Independent interval-arithmetic replay of Mishra's 0.8344 certificate for Lebesgue's universal covering problem

## What

The C# program code/LebVerifyI, using outward-rounded interval arithmetic (one-ulp widening, trust base = IEEE correct rounding of + - * / sqrt, JIT executes as written), accepted every one of the 245,496,952 leaves (486,799,600 nodes) of the published cert_B_08344 (disc + Reuleaux 3 + Reuleaux 5, tau 0.8344) with 0 failures and interval-checked child-covers-parent at every split, conditional on the written-proof lemma layer LEMMAS.md (not machine-checked, by one author) and on the paper's reduction being as restated there; it establishes no new bound, replays only family B, and its re-runnable note has one broken (controls) step that must be fixed.

(The broken step named in the last clause, the negative-controls step of the replay note, hard-coded a path outside the folder; it is fixed in this package: `object/tools/make_tampers.py` now takes the control certificate path as an argument and `verify-it-yourself/run_checks.sh` runs the controls from a clean copy. The stale file names in `object/INTERVAL_AUDIT.md` were corrected too.)

Plainly: Mishra's certificate (arXiv:2608.30538; test sets disc, Reuleaux triangle and Reuleaux pentagon of width 1) is a tree of 486,799,600 boxes over the placement space, stored as one bit per node. The program regenerates every box from the tree, and for every leaf computes a lower bound of the hull area of the three eroded bodies with an `Iv` interval type: every + - * / sqrt result of binary64 is widened by one ulp each way, constants are outward-rounded enclosures from mpmath.iv, sin/cos are interval Horner sums with explicit remainders, witness points are exact doubles whose membership is decided by interval bounds, polygon order and area come from interval cross products, and coverage of every parent by its two children is checked with interval comparisons at every split. Undecided counts as failure. This is bank partial win p1 of `lebesgue-universal-cover-bounds` (a replay), not a new lower bound.

## Check it yourself

Needs Python 3.9+ with `mpmath`, the .NET SDK (8 or newer; 10 was used), a POSIX shell (Git Bash on Windows works) and network access to raw.githubusercontent.com (the public inputs, 26 MB, are fetched from the author's repository at its pinned commit and checked by sha256; they are not copied into this package):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. What this runs, in about 3 minutes on an idle 10-core desktop and up to about 15 minutes on a loaded one (see `verify-it-yourself/RECEIPTS.md`): the sha256 of every file in `object/`, the build, the interval-type containment test (20,000 random operations per type against exact Fractions and mpmath, `violations: 0`), the negative controls (the author's small valid certificate verifies; 10 tampered copies of it are refused or fail, and a copy of the real certificate with the header tau raised to 0.83442 fails on job 3431, which holds the worst leaves, while the unpatched job passes; the other tampers and the raised-tau runs of the original controls, which take up to an hour each, are recorded in `object/records/controls_summary.txt`), and a deterministic 1% slice of the real certificate (43 of 3,596 jobs, 2,897,141 leaves, `failing leaves 0`, `RESULT: SLICE OK`). The slice is a spot check; the FULL replay is the command in `RUN_IT_YOURSELF.md` step 7 (about 2.5 hours on 5-6 threads, 1.1 GB, checkpointed) and ends with `RESULT VERIFIED  (interval mode)  a >= 0.8344 nodes 486,799,600 leaves 245,496,952 failing 0`; its log is `object/records/full_run.log` and its checkpoint (one line per job) `object/records/full_ckpt.tsv.gz`. A fresh REPRODUCE skeptic ran the full replay again and got byte-identical checkpoint rows (`panel/reproduce.md`). Any changed byte in `object/` gives `FAIL`.

## Compared to

| target | cell | table value | status page | fetched (UTC) | this package |
|---|---|---|---|---|---|
| lebesgue-universal-cover-bounds | p1: independent rigorous replay of one 2026 lower-bound certificate with outward-rounded interval or exact arithmetic | no table cell (the status page lists lower bound 0.832 and upper bound 0.8440935944 and none of the 2026 preprints) | https://teorth.github.io/optimizationproblems/constants/13b.html (HTTP 200, sha256 5bbaacfed90fd6b53fb15d8566a33a17ad6fce11da5c67a74eef95d71908dcfb) | 2026-10-31T22:24:42Z (the novelty skeptic re-read it at about 2026-11-01T01:58Z, same hash) | all 245,496,952 leaves accepted, 0 failing, worst interval slack 3.4267e-06 (accepting tier), 1.577e-05 (finest-tier re-evaluation) |

The novelty skeptic found no public independent replay of this certificate: the author's own verifiers are not independent; Hatchett (0.83474), Tomar (0.8366, with Lean proofs) and Eren (0.8368) check their own certificates. A Lean proof of a bound for the same family is not a replay of this file. Value caveat: 0.8344 is already superseded by those later public claims, so this adds provenance, not a bound. Snapshot data is under `the-record-we-beat/`.

## Not claimed

- No new lower bound, nothing about the true Lebesgue constant, no replay of the family-A certificates (cert_A_0832, cert_A_0833).
- Not unconditional: the analytic reductions of Mishra's paper (hull lower bound, gauge and mirror reduction, a-priori bound f(d), erosion and corner-movement lemmas, Prop 4.9, Reuleaux polygon = intersection of unit discs, compact-domain reduction) are written as proofs in `object/LEMMAS.md` (one author, textbook facts T1-T8, constants by mpmath intervals and exact integers) and are not machine-checked in a proof assistant. `object/LEMMAS.md` also flags that the paper's sentence "retained point within eps0 of C_n" is false as stated (harmless: the replay certifies every point's membership directly).
- Trusted: IEEE-754 correct rounding of + - * / sqrt on the executing CPU, the .NET JIT executing the source as written, exact integer bit decoding, mpmath for constants. The bit-stream format and the split rule come from the author's README and verifier (a-priori leaf type included); soundness does not depend on matching them, because children are interval-checked to cover parents and the forest identity 2L - seeds = nodes holds exactly.
- Independence limits: the independent leaf-level evidence beyond the program itself is partial: a Python/mpmath second checker (3,111 leaves, exact integer membership; `object/crosscheck/`) and the REPRODUCE skeptic's own float64 checker (44,271 leaves incl. the worst leaf of every job) found no leaf below 0.8344. No second full-coverage implementation exists. The second checker's values differ from the program's logged bound by 5.3e-6 to 9.3e-6 (the program logs the bound at the first witness-resolution tier that reaches tau); a pre-registered agreement criterion of 1e-6 therefore failed as written and was replaced, before the panel, by `how-we-built-it/PREREG.v2.md` (independent bound >= 0.8344 on every sampled leaf: 3,111/3,111; interval bound <= independent exact polygon area on every compared leaf: 1,500/1,500). Nothing rests on the original wording.
- The negative controls act on the author's small certificate (1,071,192 leaves, tau 0.83) and on one job of the real certificate; none of them reaches the per-split coverage check (the inflate tampers are refused at the header), so that check's soundness rests on code reading (done by the CRITERION skeptic) and on zero failures over the full run.
- The header's (m, K) resolution fields are ignored by the program, so the two accept-controls with rewritten m/K say nothing about resolution.
- The worst slack 3.4267e-06 is at the accepting witness tier; no leaf needed the finer tiers to pass.
- "Published" here means this package and its draft pull request.

## Credits

- Mishra (repository owner Ujjwal238), "Lebesgue's universal covering problem: a lower bound of 0.8344" (https://arxiv.org/abs/2608.30538) and the certificate at https://github.com/Ujjwal238/universal-cover-problem (commit da956b117a5f876fc3c530db3e00673e6cb18865): the object replayed here.
- Brass and Sharifi (2005), the disc/triangle/pentagon lower bound 0.832; Lebesgue (1914); Terence Tao's optimization constants page, problem 13b, as the status source.
- Zeng (https://arxiv.org/abs/2609.01284), Xie (https://arxiv.org/abs/2606.04458), Hatchett (Zenodo 10.5281/zenodo.22135010), Tomar (Zenodo 10.5281/zenodo.23717911) and Eren (Zenodo 10.5281/zenodo.23711421) as neighbouring public claims compared against.
- mpmath, for constants and cross-checks.
- The panel skeptics (`panel/`) wrote their own checks.
