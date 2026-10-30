# Honesty gate

status: CONFIRMED_SOLUTION
confirmed_scope: On the single ProteinGym assay PTEN_HUMAN_Matreyek_2021, the frozen pre-registered equal-weight z-score ensemble of the 12 model columns that M1 selects using only 187 non-cancer-gene, non-PTEN fitting assays assigns a prediction to all 5,083 reference mutants with no target-assay label entering the method and reaches a skeptic-recomputed Spearman of 0.56576, which exceeds by 0.0498 the 0.516 maximum over all 97 model columns of the independently re-fetched live DMS-level table, satisfying the full success criterion on that one assay alone and implying nothing about the other 12 pre-registered cancer-gene assays or about the method's general performance.

Read by the run's main session on 2026-10-18T19:47:36Z:
- reproduce.md: pass: true (fresh subagent). Exhaustive re-implementation from PREREG text; values agree to 3.9e-10 because packaged inputs are rounded to 10 significant digits.
- novelty.md: pass: true (fresh subagent). Live table fetched 2026-10-18T19:29:11Z, HTTP 200, PTEN_HUMAN_Matreyek_2021 max 0.516; no competing PR, trophy or paper.
- criterion.md: pass: true (fresh subagent, round 2). Round 1 (panel_work/criterion.round1.md) also passed but found the criterion's 'list of external score files with provenance' deliverable only partial. The gate treated that as a literal gap: EXTERNAL_SCORES.md was added (no other change to claim/) and CRITERION re-ran in a new fresh context.
- Downgrade checks: no hedging verdict; reproduction matches; strictly better than the live table (+0.0498); the scope is the single assay; one object (one score file); table fetch < 6 h old; no evasive access (plain GETs, V3R1T4S User-Agent).
- Context the scope already carries: 13 assays were pre-registered and all scored with M1; 4 clear the bar (see attempts/optimizer/report.md).
