# Disclosures (contributor text; the same as the claim's disclosures the final panel read)

Paths below are those of the claim package the panel read: its record/*.txt files are how-we-built-it/records/ here,
record/status_source.md and record/published_table.md are the-record-we-beat/RECORD.md and
the-record-we-beat/published_scores_found.md, and PREREG files are in how-we-built-it/.

1. Hub scores. The hub's repository has no score file at e947ca8 or at 1985aee (record/status_source.md); hub issues
   #294 and #515 and pull request #295 describe scoring for an internal CDC page (the claim text the panel read
   called #295 an issue; it is a pull request). The p3 clauses "discrepancy with the hub's own
   published scores (if any)" and "the exclusion rules needed to reconcile them" are therefore met only vacuously for
   the hub. The reconciliations are with third-party scores.
2. Overlap with prior work, and no completeness claim. This claim does not say that the object's values are unpublished
   elsewhere or that the sources named are all that exist; other sources may publish values that overlap the object's
   cells. record/published_table.md names what this work read and reconciled. Known overlap: the epi-hub-analysis rows
   cover 26,248 of the object's 38,728 hosp tasks (7 of the 8 hosp directories, 22 of the 30 reference dates; the
   paper's Supplementary Table 7 summarises them as log WIS by horizon); EpiBenchmark covers RSVHub-ensemble and
   RSVHub-baseline on 28 dates on 5 quantile levels (its published ensemble mean on its tasks is 26.688 with its
   2026-09-16 truth; with the pinned oracle the same tasks give 26.743 on 5 levels and 29.194 on the object's 23
   levels); tapestry publishes RSVHub-ensemble season scores for both targets, UGA_flucast-INFLAenza season WIS for both
   targets on the units it shares with the ensemble (hosp: 5,936 shared at horizons 0-3, 5,824 outside Puerto Rico;
   ED: 5,350), Google_SAI-RSVEns natural-scale WIS on 4,692 hosp tasks from 2025-12-27, and plots of RSVHub-ensemble's
   WIS by reference date; Zenodo 10.5281/zenodo.22988800 gives RSVHub-ensemble WIS relative to RSVHub-baseline.
3. Truth vintage. The table uses oracle-output.parquet at e947ca8, whose 5,140 non-missing quantile rows equal the
   2026-11-12 vintage of time-series.parquet (record/truth_revisions.txt). The season's truth was still being revised:
   between the 2026-11-04 and 2026-11-12 vintages, 50 of 4,305 in-season truth rows (target_end_date
   2025-09-13..2026-06-20) changed: 43 hosp, 7 ED, target_end_date 2025-11-29..2026-06-20. The largest change relative
   to the 2026-11-04 value is 12.2% (hosp, location 48, 2026-06-13, 41 -> 46; 10.9% of its 2026-11-12 value); the
   largest relative to the 2026-11-12 value is 13.7%, on another row (ED, location 19, 2026-06-06). The table holds for
   the pinned oracle only. Against epi-hub-analysis's truth snapshot, the per-model differences on its summary task set
   (52 jurisdictions without US, horizons 0-3) are at most 0.1009 (0.100807, CFA_Pyrenew-Pyrenew_H_RSV, which has no
   Table 6 row) and at most 0.0463 (0.046253, CEPH-Rtrend_rsv) for the four Table 6 rows; these bounds are for that summary task set only, not for all 26,248 of
   its rows.
4. p3 was declared after failures. p3 was declared (run 2026-11-13-0233, PREREG.v3.md, 2026-11-13T02:53:41Z) after that
   run's main attempt (a frozen forecaster against RSVHub-ensemble, scored 02:48Z) and p1 had failed, and after a first
   reproduction of Supplementary Table 6 (kit step 3c). It is a post-failure, bank-enumerated recomputation, not a
   forecasting result. PREREG.v3.md is kept unedited; its sentence calling the arXiv table "the only published per-model
   scores for this season" was wrong and is withdrawn by disclosure 2.
5. "Released" becomes true only if the package is made public; until then that clause is not met.
6. Mis-dated rows. The 2025-09-27 ED files of RSVHub-ensemble and UGA_flucast-INFLAenza carry 250 tasks each whose
   target_end_date is one week earlier than reference_date + 7 x horizon. The object scores them at their stated
   target_end_date (as a hubverse join on target_end_date would) and gives a sensitivity (the ensemble's ED mean WIS
   0.000887532 as tabled, 0.000918589 on its date-consistent tasks only). tapestry's ED values reproduce only when these
   rows are left out.
7. Scorer and conventions. code/wis.py is a Python re-implementation of the scoringutils/hubverse quantile WIS; the R
   hubEvals code was not run (no installs). The pairwise relative WIS uses the scoringutils convention of a geometric
   mean that includes each model's self-ratio of 1 (without it, values change by up to about 4%). The kit step-3c
   baseline (baseline/) has a separately written loader and aggregation, but its wis.py is byte-identical to
   code/wis.py, so it is not an independent WIS implementation.
8. Line endings (this version). Earlier versions of the text outputs had CRLF line endings, so byte-identity of
   REPRODUCE.md held only on Windows. Every script now writes LF (newline="\n"); object/p3_exclusions.txt,
   object/p3_era_subset.txt, object/p3_reconcile_epi_hub_analysis.txt and the record/ outputs changed bytes but not
   content (each equals its predecessor after CRLF -> LF; new sha256 in REPRODUCE.md). object/p3_table.csv was always
   LF and is unchanged.
9. History (text-only corrections of an unchanged table). Run 2026-11-13-0233: round 1 REPRODUCE fail (cross-model
   pairing without target_end_date; the table was repaired), NOVELTY pass, CRITERION pass; round 2 (this table):
   REPRODUCE pass, CRITERION pass with wording corrections, NOVELTY fail ("the only published" scores; EpiBenchmark had
   published scores). Run 2026-11-13-0349: round 1 REPRODUCE pass, CRITERION pass, NOVELTY fail (the text said no cited
   source had UGA_flucast-INFLAenza scores; tapestry publishes them; three sources unnamed); round 2 (repair) CRITERION
   pass, REPRODUCE fail (the Puerto Rico rule was missing from the text; 5,824 vs 5,936 shared units), NOVELTY fail
   (the text said tapestry's scores were "exactly" those listed; its Google comparison has natural-scale WIS and plots
   were unlisted). Every NOVELTY skeptic judged the table itself new. This version (run 2026-11-13-0523) drops every
   completeness or exclusivity statement, adds the Puerto Rico rule and the 5,936/5,824 counts, describes the Google
   comparison folder in full and reconciles it, lists the plots, and switches the text outputs to LF. object/p3_table.csv
   (sha256 e01db6ee9d55baf24c06fa801c2fdfee27d9c1f70d1d513b9e98b75bd6d2f804) has not changed since run 2026-11-13-0233's
   round 2.
10. Corrections asked for by the final panel's CRITERION skeptic, applied in this package and not in the claim text
    the panel read (the object does not change):
    - R1: the reconciled third-party values are reproduced to within 2e-12 absolute, not 1e-12 absolute: the largest
      difference, 1.82e-12, is RSVHub-ensemble's summed WIS of about 9,077 for location 36 in tapestry's
      native-location-scores.csv (relative 2.0e-16); every other reconciled value is within 1e-12.
    - R2: in item 3 the two bounds are 0.1009 (0.100807) and 0.0463 (0.046253); the claim text had rounded them down
      to 0.1008 and 0.046. The claim sentence's "at most 0.101" was correct.
    - R3: the claim sentence made code/p3_recompute.py the subject of "finds no score file in the hub's own
      repository, and was reconciled with these third-party score sets". The hub-tree check is recorded in
      the-record-we-beat/RECORD.md, and the reconciliations are run by how-we-built-it/code/p3_reconcile_k2.py and
      how-we-built-it/code_reconcile/ (with their own loader and WIS function), not by p3_recompute.py; this work, not
      that script, did them.
    - Optional note from the same skeptic: tapestry main (06508218) also has
      docs/experiments/nowcast-overnight-20261005/rsv-component-target-scores*-2025-2026.csv with RSVHub-ensemble summed
      WIS on the leaderboard's unit sets (not opened by the contributor; reported by the skeptic).
