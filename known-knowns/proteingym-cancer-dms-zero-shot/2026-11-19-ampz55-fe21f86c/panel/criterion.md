# CRITERION skeptic verdict — BORDA-12, 2026-11-19-0953

context: subagent (fresh panel context, claim package only)

## Verdict

pass: true — the result meets the full success criterion as literally written.
The pass is narrow and rests on the criterion's own point comparisons; the
two closest calls (post-hoc origin of the primary, and the noise-level
margin over M1) are recorded below, not hidden.

## Literal check against the criterion (claim/claim.md, claim/target.md)

(a) Score file over every mutant. claim/score_borda12.csv: 5,083 rows,
columns mutant, score, zero NaN scores, 5,083 unique mutants, mutant set
exactly equal to claim/data/reference_Matreyek_2021.csv (verified by
independent recompute, not by trusting the build log). sha256 matches the
claim: fe21f86cd41c75ce321ba511dfcdbe23888e12e1445eec27ba9e2d98ee942350.
Reference sha256 matches claim/PREREG.md: 1c52aba9....

(b) Zero-shot w.r.t. the assay. Audited claim/code/build_borda12.py in
full. The combiner is mean percentile rank over M1's 12 members, equal
weight 1/12 each, no fitted weight, no clipping, no logit, no threshold,
no hyperparameter. It reads only the mutant column and the 12 member
score columns (usecols) from the fetched assay file; DMS_score is never
read for construction. Labels appear only in gates/fixtures/diagnostics:
G1 checker fixtures (1.0 / -1.0), G2 E2 reproduction (0.3666), the G3
identity check (recomputed-vs-CSV member Spearman, reported only, never
drives a drop), the direct rho recompute for logging, and leave-one-out /
bootstrap diagnostics. The G3 drop rule is label-free (missing /
constant / >5% NaN); no member was dropped; all 12 members kept with 0
NaN. No measurement from any ProteinGym DMS assay of PTEN (P60484)
enters the method. Mighell labels are never used for fitting (Mighell is
a diagnostic only). Membership is M1's 12 as published in PR #467,
asserted in the package (claim/PREREG.md, claim/target.md) to have been
selected by its authors only on non-cancer assays; that selection
procedure itself is not evidenced inside the claim package (the PR text
is not included), so the zero-shot verdict relies on the package's
consistent assertion here. Fitting set: none — equal weights are "on no
data at all", which the criterion expressly permits.

Closest call 1 — post-hoc origin. claim/PREREG.md states openly that
the 2026-11-17 self-break already recomputed this exact combiner at
0.5682 post-hoc, and that this run pre-registers it as primary and
re-scores it fresh. The re-score is a deterministic recomputation of the
same formula on the same public inputs, so it returns the identical
0.5682 and adds no new evidence beyond the 11-17 recompute. I do not
fail on this, for two literal reasons. First, the criterion's
prohibitions attach to quantities chosen as part of the method
(hyperparameter, weight, threshold, model-selection decision,
combination weight): BORDA-12 contains zero such quantities chosen using
target labels — the weights are equal by construction, the membership
came from M1's non-cancer selection, and the post-hoc knowledge changed
no element of the formula. Second, the pre-registration timing clause
("written before the target assay is scored") attaches to logging the
fitting set, and there is no fitting set to log. The pre-registration
is therefore procedural compliance, not evidentiary novelty — but the
criterion as written demands a label-free method and a pre-registered
formula, both of which hold, not a method never before evaluated. Had
any weight, member, or threshold been tuned on Matreyek labels, this
would be a fail. None was.

(c) Strictly higher than the live row maximum by >= 0.015. Live CSV
claim/data/live_Spearman_DMS_level.csv (sha256 f432423b... matches
claim/PREREG.md, fetched 2026-11-19 10:34 UTC per claim/scout.md):
Matreyek row max over model columns is 0.516 (VenusREM); 'Number of
Mutants' is metadata and correctly excluded. Independently recomputed
Spearman from the score file and reference: 0.5682423873, matching the
claimed 0.5682. Margin over live max: +0.0522 (>= 0.015 required).
Margin over the 0.531 bar: +0.0372. Bootstrap 95% CI [0.5486, 0.5886]
lies entirely above the bar; P(BORDA-12 > bar) = 1.000
(claim/diagnostics.log). The checker (v2.0-dupe-reject) enforces exact
mutant-set match, rejects duplicate mutant IDs, drops NaN pairs, and
uses scipy Spearman — the official convention as implemented. PASS.

(d) PREREG frozen before scoring. Run-internal ordering holds: the
pre-registration file was last written 10:36:31 UTC, the build code
10:36:45 UTC, the score file 10:37:51 UTC. Minor discrepancy: the file
header states "frozen 2026-11-19 10:35 UTC", ~90 seconds before its
actual last-write time; the ordering relative to scoring is unaffected,
so this does not change the verdict. No sha256 stamp of the
pre-registration file itself was found in the package; the file carries
sha256 stamps of all its inputs instead. That is a documentation gap,
not a criterion failure as written.

(e) Null model. claim/null_test.md: controls 400, best control 0.0398,
real 0.5682, real beats all controls: yes. Design matches
claim/PREREG.md (400 permutations, seed 20261119). I independently
re-ran 400 permutations with seed 20261119: best control 0.03977,
matching 0.0398. Consistent. The null is decisive: the score is not
chance structure.

## Hidden quantifiers and stretched definitions

- "Beats M1 by 0.0024": the criterion's bar is the LIVE TABLE (0.531),
  not M1. 0.5682 clears it by 0.0372. The M1 comparison is a separate
  novelty bar operationalized in claim/target.md and claim/PREREG.md as
  a point comparison (rho > 0.5658). 0.5682 > 0.5658 literally.
  M1 is disclosed in unmerged PRs #467 (open) / #463 (closed), not in
  the live table and not in TROPHY_CASE.md (claim/scout.md confirms no
  entry). The criterion's "maximum over all model columns in the live
  CSV" leaves no room for a disclosed-but-unmerged ensemble to raise
  the criterion's bar — and the package's own added bar (beat M1) is
  also cleared on the point value. BORDA-12 is a different combiner
  from M1 (mean percentile rank vs M1's z-score ensemble) over the same
  12 members, so it is not a re-publication of M1; it is not subsumed
  under the stated rule.
- Noise caveat (closest call 2): the margin over M1 is inside noise —
  bootstrap CI on BORDA-12-minus-M1 is [-0.0172, +0.0228],
  P(BORDA-12 > M1) = 0.592 (claim/diagnostics.log, claim/claim.md). The
  criterion is written as a point comparison and contains no
  significance requirement for the M1 margin; imposing one would rewrite
  the criterion. The claim discloses the caveat honestly rather than
  hiding it. The margin over the LIVE TABLE, which is what the
  criterion actually requires to be >= 0.015, is robust (difference vs
  VenusREM 0.516: 95% CI [0.0326, 0.0726]). The "record over M1" is
  therefore a point-value record, not a statistically reliable one, and
  the confirmed scope below says exactly that. If the panel wants a
  significance bar over M1, that is a criterion change, not a finding
  about this claim.

## Baseline note (claim/PREREG.md step 3c)

Adequate. The published baseline is the live table value itself
(VenusREM 0.516); VenusREM releases no per-mutant predictions, so no
baseline code exists to reproduce — there is nothing to re-run. The
comparison is a number comparison against a re-fetched published table,
and I independently recomputed the row max (0.516). The scoring
pipeline is validated instead by the checker fixtures (score=DMS_score
-> 1.0 PASS, negated -> -1.0 FAIL) and the E2 reproduction (0.3666),
both re-verified in the build log. The residual is that the table value
is taken on trust from the ProteinGym repository, which is the
criterion's own designated source.

## Partial wins

- p1: NOT met. Requires >= 0.015 over the live best on at least three
  cancer-gene assays with ONE method and ONE frozen configuration. Only
  Matreyek is claimed; the diagnostic second assay does not replicate —
  BORDA-12 on Mighell is 0.5723 vs the Mighell bar 0.576
  (claim/diagnostics.log). No multi-assay claim.
- p2: NOT met. MSH2_HUMAN_Jia_2020 was not scored this run; no claim.
- p3: NOT met. No leakage-free combination audit or per-assay
  reachable-ceiling estimate was produced this run; no claim.

## What is NOT established

- The margin over M1 (+0.0024) is not statistically established; a
  re-fetch or a different sample could flip the point record over M1.
  The margin over the live table (+0.0522) is robust.
- M1's member selection on non-cancer assays only is asserted, not
  evidenced, inside the claim package.
- Mighell does not replicate (0.5723 < 0.576), so nothing is shown
  about BORDA-12 beyond Matreyek.

confirmed_scope: BORDA-12, a parameter-free equal-weight Borda over M1's 12 published members, scores Spearman 0.5682 on PTEN_HUMAN_Matreyek_2021, 0.0522 above the live best 0.516 and 0.0024 above M1's disclosed 0.5658, with the margin over M1 inside bootstrap noise (95% CI [-0.0172, +0.0228]).

pass: true
