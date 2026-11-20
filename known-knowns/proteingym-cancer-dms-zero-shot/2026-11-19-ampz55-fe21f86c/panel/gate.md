# gate.md — honesty gate, 2026-11-19-0953

I read all three panel files myself. REPRODUCE pass (own checker rho
0.5682423873, bar 0.531 recomputed, byte-identical deterministic rebuild,
independent recompute to 3.3e-16, null re-run with a fresh seed).
NOVELTY pass (live table re-fetched 2026-11-19 10:41 UTC, HTTP 200,
byte-identical; only PRs #467/#463 exist; M1 still 0.5658; no literature
result above 0.5682). CRITERION pass (literal criterion met; zero-shot
audit clean; null reproduced; no partial win). No hedging panelist, no
reproduction mismatch, the value is strictly better than the live table
(+0.0522, bar cleared by +0.0372), the scope is exactly the evidence,
and the panel's table fetch is under 6 hours old. The two closest calls
were decided explicitly by the panel and I agree with both decisions:
(1) the post-hoc origin of the primary does not violate the criterion,
because BORDA-12 contains zero label-chosen quantities (equal weights,
published membership, no hyperparameters/thresholds) and PREREG was
frozen before scoring; (2) the +0.0024 margin over M1 is inside noise
(CI [-0.0172, +0.0228], P = 0.592), but the criterion is a point
comparison and the margin over the live table is robust — so the record
over M1 is a point-value record, stated as such in the confirmed scope.
One packaging defect (REPRODUCE): the claim copy of build_borda12.py
does not run verbatim from its packaged location (path resolution lands
one level too high); the run-folder route reproduces fine. Fix before
submission; it affects no number.

status: CONFIRMED_SOLUTION
confirmed_scope: BORDA-12, a parameter-free equal-weight Borda over M1's 12 published members, scores Spearman 0.5682 on PTEN_HUMAN_Matreyek_2021, 0.0522 above the live best 0.516 and 0.0024 above M1's disclosed 0.5658, with the margin over M1 inside bootstrap noise (95% CI [-0.0172, +0.0228]).
