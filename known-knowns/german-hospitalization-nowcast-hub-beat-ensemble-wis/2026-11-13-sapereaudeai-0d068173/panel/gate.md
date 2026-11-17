# Honesty gate (kit/RUN.md step 7), run 2026-11-13-0420, written 2026-11-13T05:31:52Z

claim: p3 of german-hospitalization-nowcast-hub-beat-ensemble-wis (claim/CLAIM.md)

Panel (three fresh subagent contexts, each given only claim/):
- REPRODUCE: pass: true. An independent checker reproduces all 93 stage cells to 3e-12, and 28 of the 31 published
  cells to 1.2e-13. Truth and FrozenBaseline are re-derived. 9 hub files were re-fetched, all with matching sha256.
  Caveat: under the 700 MB panel cap it could not rerun the author's step 2. The main session reran that step from
  claim/ and got byte-identical output.
- NOVELTY: pass: true. The status source was fetched 2026-11-13T04:53:55Z, HTTP 200. No earlier independent
  recomputation was found. Its caveats were the sample-only provenance (resolved before CRITERION started: the full
  check covers 1,593 files with 0 mismatches) and paper-vs-release differences (documented in claim/ADDENDUM.md).
- CRITERION: pass: true, with a narrowed confirmed_scope (main tables only, not the _100k/_40d/_7d/_updated tables).
  It asks for four wording fixes before posting; none changes a number. They are applied in the package's text
  files, never in panel/ or claim/.

Gate checks:
- No panelist hedges on its verdict.
- No reproduction mismatch beyond the documented Epiforecasts residuals (< 1.04e-4, inside the 1% tolerance).
- The scope is no wider than reproduced (CRITERION's sentence).
- No sample is presented as complete: provenance is full (1,593 files).
- No table value was obtained by evasion: one honest request each, all HTTP 200, no retries.
- One object: the 31-cell table.
- The baseline (step 3c) is resolved: it reproduces.
- The panel's fetch is less than 6 hours old.
- V3R1T4S PRs were re-checked at 05:31Z: none exist for this target.

Process note: claim/ADDENDUM.md (documentation only; no number changed) was added after the NOVELTY report and
before CRITERION started; the full provenance file arrived at 05:22Z; REPRODUCE was told and checked it.

status: CONFIRMED_PARTIAL
confirmed_scope: A released, independently written Python script (claim/code/p3_reproduce.py, with the provenance, exclusion-re-derivation and FrozenBaseline checks in claim/code/) recomputes the 31 per-model mean WIS cells of the published evaluation's three main tables (data/scores/wis_national.csv, wis_states.csv, wis_age.csv; the overall means of Wolffram et al. 2023 Fig 7) for forecast dates 2021-11-22..2022-04-29 from the hub's data-processed, data-processed_retrospective and data-processed_updated_models nowcasts (read via the evaluation's assembly, verified row for row against those hub files) and the hub's truth at the 2022-08-08 commit 11c74532, matching 28 cells to |relative difference| below 1e-9 and the 3 Epiforecasts cells to within 1.04e-4, and documents the exclusion and repair rules of the released evaluation code needed for that agreement, without reproducing the evaluation's other WIS tables (_100k, _40d, _7d, _updated) or verifying the paper's S1 Appendix description of those rules.
