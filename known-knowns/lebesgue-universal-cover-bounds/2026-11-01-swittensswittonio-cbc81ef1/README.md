# Independent interval-arithmetic replay of Zeng's 0.834 certificate for Lebesgue's universal covering problem

## What

A separate C# outward-rounded-interval/exact-integer checker accepted all 6,746,392 leaves of Zeng's published certificate (arXiv:2609.01284) at tau = 0.834 with exact box partitions, conditional on the unformalised lemma layer L1-L8/F1-F4 and trusted mpmath sample/pi tables, proving the certificate verifies and not that a_Leb >= 0.834 unconditionally.

Plainly: Zeng's certificate (bodies: a disk, a regular Reuleaux triangle and a regular Reuleaux pentagon of width 1; far-field reduction, two collar domains and a five-dimensional core domain) was replayed end to end by a checker written from the definitions. Every operation that feeds a certified lower bound is either an `Iv` interval operation (binary64 result of + - * / sqrt widened by one ulp each way; sin and cos by Taylor sums in `Iv` with an explicit remainder) or exact integer arithmetic (box partitions at scale 10^34). Undecided counts as failure. The replay found eight documentation or code defects in the published artifact (D1-D8 in `object/REPLAY_NOTE.md` section 4); none invalidates the bound. This is bank partial win p1 of `lebesgue-universal-cover-bounds` (a replay), not a new lower bound.

## Check it yourself

Needs Python 3.9+ with `mpmath`, the .NET SDK (8 or newer; 10 was used), a POSIX shell (Git Bash on Windows works), about 4 GB free disk and network access to zenodo.org the first time (the 765 MB public certificate is downloaded once, verified by md5 and sha256, cached in `V3R1T4S_CACHE` or the system temp folder, and is not copied into this package):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Just before it the log shows `TOTAL leaves=6746392 failing=0 worst_slack_over_0.834=1.551089E-009`, `VERDICT: ACCEPT`, and `controls: 14 tampers rejected, baseline accepted`. Rough laptop time: about 6 minutes on an idle 10-core desktop, up to about 30 minutes when the machine is loaded (the receipts show the loaded 27-minute run), dominated by the download on the first run and by the leaf replay (3,291 thread-seconds). Any changed byte in `object/` gives `FAIL`. Real output is in `verify-it-yourself/RECEIPTS.md`; `RUN_IT_YOURSELF.md` has the individual commands, including the optional 21-minute per-record hash census.

## Compared to

| target | cell | table value | status page | fetched (UTC) | this package |
|---|---|---|---|---|---|
| lebesgue-universal-cover-bounds | p1: independent rigorous replay of one 2026 lower-bound certificate with outward-rounded interval or exact arithmetic | no table cell (the status page lists lower bound 0.832 and upper bound 0.8440935944 and none of the 2026 preprints) | https://teorth.github.io/optimizationproblems/constants/13b.html (HTTP 200, sha256 5bbaacfed90fd6b53fb15d8566a33a17ad6fce11da5c67a74eef95d71908dcfb) | 2026-10-31T22:24:42Z (the novelty skeptic re-read it at about 2026-11-01T00:59Z, same content) | all 6,746,392 leaves accepted, 0 failing, exact partitions of the core, R3-collar and R5-collar domains |

The novelty skeptic found no public replay of this certificate (Tao's optimization-constants repository: open PR 223 adds only Mishra's 0.8344; no replay PR for this constant; nothing in this repository, Zenodo, GitHub or the arXiv listing it could reach). The bound itself is not a record: 0.834 is below Mishra's 0.8344 and the later public claims 0.83474, 0.8366 and 0.8368. Snapshot data is under `the-record-we-beat/`.

## Not claimed

- No new lower bound for the Lebesgue constant, and nothing about the true value. The replay confirms "this certificate verifies".
- Not unconditional: the analytic reductions (hull lower bound, normalisation to psi in [0, pi/5], far-field closed form, collar reduction, local polygon certificates, Reuleaux polygon as an intersection of unit discs) are written as proofs in `object/LEMMAS_ZENG.md` and checked numerically (`object/lemma_checks/`), not machine-checked in a proof assistant. The flags F1-F4 there (reference orientation must be mirror-symmetric; one derivative bound needs an absolute value; rotation-index premise; the angular-end bridge) are part of the scope.
- Trusted: the .NET runtime and compiler, IEEE-754 correct rounding of + - * / sqrt (the basis of the one-ulp widening), `double.Parse`, and the sample-point and pi tables generated with mpmath (Reuleaux table points are re-checked by the C# program with `Iv`; disk points, centres and the pi enclosures are checked only by an independent 90-digit Python script and by inspection).
- Zeng's hierarchy theorems (Part I) were not replayed and are not needed for 0.834.
- "Every operation entering a certified bound" is meant exactly: the choice of hull vertices, candidate templates and their ordering use plain doubles (completeness heuristics only; every polygon is re-certified). For 2,354 of 6,742,989 core leaves (0.035%) the replay needed a second polygon variant that drops one near-vertex sample point per Reuleaux set, the same point the author's own verifier drops under python-flint 0.9.0 (defect D4); dropping a sample point only shrinks the witness polygon, so this is sound, but it is a dependence on the author's artifact.
- The checker reads the leaf boxes, sample counts and hull-vertex hints from the certificate; it does not trust the recorded `lower_bound` or `method` fields.
- In `object/records/controls/controls.log` the line `c16_bad_table ACCEPT` is an ineffective tamper (a table point shifted but still inside the body, on a sample set the collar run does not use); the real test is the next line `c16b_bad_table(+1%) REJECT`. The loose-tau accepts (tau 0.8340004, 0.8340005, 0.8348 on the one-frontier mini certificate) are explained in `object/REPLAY_NOTE.md` section 3: the replay finds a stronger witness polygon than the recorded one, so they are not soundness holes.
- The worst slack 1.551e-09 is the first witness found at the recorded template, not the best bound of that leaf (a stronger polygon for the same box reaches 4.5e-04).
- "Published" here means this package and its draft pull request; no other publication was made.

## Credits

- Zeng, "An exact hierarchy ... certified 0.834 lower bound" (https://arxiv.org/abs/2609.01284) and the certificate artifact, Zenodo 10.5281/zenodo.20528351 (https://zenodo.org/records/20528351): the object replayed here.
- Brass and Sharifi (2005), the disk/triangle/pentagon lower bound 0.832 that this family extends; Lebesgue (1914) for the problem; Terence Tao's optimization constants page, problem 13b (https://teorth.github.io/optimizationproblems/constants/13b.html), as the status source.
- Mishra (https://arxiv.org/abs/2608.30538, 0.8344, same family), Xie (https://arxiv.org/abs/2606.04458, 0.833), Hatchett (Zenodo 10.5281/zenodo.22135010, 0.83474), Tomar (Zenodo 10.5281/zenodo.23717911, 0.8366) and Eren (Zenodo 10.5281/zenodo.23711421, 0.8368) as the neighbouring public claims compared against.
- mpmath (sample-point and constant tables, cross-checks); python-flint was used by the replay only to time and compare against the author's own verifier, never for the verdict.
- The three panel skeptics (`panel/`) wrote their own checks; the REPRODUCE skeptic's independent checker also accepted all 6,746,392 leaves.
