# Honesty gate, cell N40 (proportion 0.40, mean NED), session 2026-10-18-1758 (kit RUN.md step 7)

Written 2026-10-18T22:04:59Z (date -u) by the main session (Opus 5.5, claude-opus-5-5[1m]) after reading all three panel files in full.

status: CONFIRMED_SOLUTION
confirmed_scope: At proportion 0.40, the frozen single system classifier/PRIMARY, whose predictions are attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv (the same predictions as object/predictions-0.40.tsv), has mean NED 0.2455448938803044 over the 10 surprise families under the pinned ST2022 scorer (left-to-right summation; 0.24554489388030437 with the builtin sum), strictly lower than Mockingbird-I1's official 0.316240240534308 from results-surprise-0.40.json, a win on mean NED at 0.40 only.

## Panel (three fresh contexts, Agent tool, model opus = Opus 5.5; each saw only its own copy of claim/)
- panel/reproduce.md: own scorer from the pinned compare_words (Mockingbird-I1 0.40 reproduced bit for bit, left to right);
  claimed value recomputed in both summation modes; MANIFEST and freeze hashes checked; the entry retrained twice from its
  frozen code (one run sandboxed or traced): all 10 test-0.40 files byte-identical, bit-deterministic (PREREG rule 12 iv,
  strict case); access trace and row-isolation tests of its own; pass: true.
- panel/novelty.md: status source https://github.com/sigtyp/ST2022 HTTP 200 between 2026-10-18T21:40:36Z and 21:41:30Z
  (HEAD 03094435 unchanged; results-surprise-0.40.json at the pinned commit byte-identical to the claim's copy); FeVeT and
  Cognate Transformer publish no 0.40 value; literature of the last 24 months searched (ACL Anthology bibliography,
  OpenAlex or OpenCitations, Europe PMC, Zenodo, Hugging Face papers, GitHub); best published value at 0.40 stays
  Mockingbird-I1 0.316240240534308; pass: true. The fetch is under 1 h old at this gate (less than 6 h), so no re-fetch.
- panel/criterion.md: literal criterion met; selection followed PREREG rule 10 as written; disclosed issues judged within
  the letter and spirit with counterfactuals (NED 0.2478195460955122 without the development rows (CRITERION counterfactual, margin 0.068); hillburmish byte-identical without them); null test rerun; pass: true. Its confirmed_scope is copied above
  exactly.

## Gate checks (downgrade on any; none applies)
- Hedging panelist: none (three plain pass: true). Residual coverage gaps the NOVELTY skeptics state (stopped hosts:
  arxiv.org, api.semanticscholar.org, dblp.org, scholar.archive.org, ieeexplore.ieee.org, api.github.com; github.com after
  2026-10-18T21:48:35Z) are listed in the report; the unreadable ICCIES 2025 paper's abstract is off-task.
- Reproduction mismatch: none.
- Value strictly better than the bar: mean NED 0.2455448938803044 (lower is better) vs Mockingbird-I1 0.316240240534308; margin 0.0706953466540036
  (left to right; also in builtin summation), far above 1e-9.
- Stretched criterion or hidden quantifier: none found; development-family rows disclosed (at 0.40 only the listsamplesize
  rows for kesslersignificance are read; the CLAIM.md wording about mannburmish rows overstates what happens at 0.40, on the
  conservative side, as all three REPRODUCE and two CRITERION skeptics found).
- Scope wider than reproduced: no (one cell, one metric, one object: attempts/classifier/frozen/PRIMARY/test/0.40).
- Sample presented as complete, capped search as exclusion, probable prime: not applicable.
- Table value obtained by evasion: no (one plain GET each through the stop-aware helper; one 429 on github.com at
  21:48:35Z was recorded by the helper and never retried).
- Several objects bundled: no (the same object is claimed on the other two metrics in sibling folders, each its own cell).
- Null test: 400 controls, best control 0.011794897907416113 vs real 0.0706953466540036, real_beats_all_controls yes (null_test.md).
- Sealed check: rules/sealed_cand_0.40.log ends SEALED_CHECK 0.40 PASS (10 of 10 families byte-identical).

## Corrections noted by the panel (kit rule 14; recorded, not silently fixed)
- PREREG.md and scout.md say Cognate Transformer reports 0.50 only; its EMNLP 2023 paper reports 0.10, 0.30 and 0.50
  (Table 5). No 0.40 value either way; the bar is unchanged. The frozen PREREG is not edited.
- The claim's REPRODUCE.md step 3 needs --python SYS (the harness default interpreter is a WORKDIR placeholder in the claim
  copy); every REPRODUCE skeptic added it.
