# Honesty gate, amoxicillin-clavulanic acid (2026-10-17T00:52:54Z)

status: CONFIRMED_SOLUTION
confirmed_scope: On the cluster-held-out TEST partition in result/split.csv (sha256 68a7e358...577dca) of NCBI export PDG000000004.6366 as the claimant describes it, the LightGBM model's predictions in result/test_predictions_amoxicillin-clavulanic_acid.csv score F1 91.97% and accuracy 97.68% (TP 189, FP 7, TN 1200, FN 26), against 44.78% and 69.48% for the code-reimplemented Table 3 genotype rule on the same 1422 rows and 44.5% and 73.6% published, with the model's cluster-bootstrap F1 interval lying above both baselines, for amoxicillin-clavulanic acid only and for database concordance only.

Path note (added 2026-10-19, matching the maintainer's request on this pull request, #308): the confirmed_scope sentence above uses the claim-folder paths the panel reviewed. In this package, result/split.csv is how-we-built-it/split.csv and result/test_predictions_amoxicillin-clavulanic_acid.csv is object/test_predictions_amoxicillin-clavulanic_acid.csv.

Panel results:
- reproduce: pass: true; context: subagent (same VM)
- novelty: pass: true; context: subagent (Claude Code on the owner's PC, fresh context, Sonnet); novelty: PASS - live Table 3 (HTTP 200, 2026-10-17T00:24:41Z) gives amoxicillin-clavulanic acid F1 44.5% and accuracy 73.6%; the claim's F1 91.97% and accuracy 97.68% strictly beat both (+47.47 and +24.08 points); Front Microbiol
- criterion: pass: true; context: subagent (same VM)

Earlier round: the first NOVELTY panelist (round1/novelty.md, cloud run) could not open this repository's pull-request list
(HTTP 403 from the session proxy) or Front Microbiol 2026;17:1842717, and wrote pass: false. This round's NOVELTY panelist ran
in a fresh context on the owner's PC with both reachable. REPRODUCE and CRITERION are unchanged from the first round.

Changes after the first round, none to the claim's object or numbers: NCBI moved export PDG000000004.6366 from latest_snps/ to
the versioned folder PDG000000004.6366/ (both files downloaded again on the owner's PC on 2026-10-17 and their sha256 match the
pinned values), so the package uses the versioned URLs; and the package checker now opens its files as UTF-8 so it also runs on
Windows. Run on the owner's PC, the package checker reproduces F1 91.97 and accuracy 97.68 on the same 1422 TEST rows and prints PASS.

Gate review (main session): read all three panel files. Downgrade triggers checked (hedging panelist, reproduction mismatch,
value not strictly better than the published one, stretched criterion, scope wider than reproduced, sample presented as
complete, capped search used as an exclusion, several objects in one claim): none found. The CRITERION panelist's notes (the
paper's post hoc TEM-1 rule was not compared; test labels were read again for contrarian checks with no model change) are
recorded in criterion.md; the post hoc rule recomputed by the run scores F1 60.2 on TEST, far below 91.97.
