# Honesty gate, cell L30 (proportion 0.30, mean BLEU), run 2026-10-18-1249 (kit RUN.md step 7)

Written 2026-10-18T13:18:44Z (date -u) by the main session (Opus 5.5, claude-opus-5-5[1m]) after reading all three panel files.

status: CONFIRMED_SOLUTION
confirmed_scope: At proportion 0.30, the frozen BLEU-MBR stage-2 object combiner/test/0.30 (the same predictions as object/predictions-0.30.tsv; six frozen entries trained on training-0.30 only, weights [2, 2, 1, 3, 1, 3] fit on the validation split shared/val/0.30 cut from training-0.30) has mean BLEU 0.6874377388475998 over the 10 surprise families under the pinned official ST2022 scorer (same value with left-to-right and compensated summation), strictly above Mockingbird-I1's official 0.6058548112827981, FeVeT's rescored 0.6356571184958077 and the cell's bar, our own earlier NED-targeted object bar_comb_new/test/0.30 at 0.6839233380559118 (by 0.003514400791688077 left-to-right and 0.003514400791687966 compensated), as a claim on mean BLEU only.

## Panel (three fresh contexts, Agent tool, model opus = Opus 5.5; each saw only its own copy of claim/)
- panel/reproduce.md: own scorer from the pinned compare_words (Mockingbird-I1 reproduced bit for bit, 44 of 44 values),
  every freeze hash checked, all six entries retrained twice (harness and its own read-sandbox, every partition alone):
  60 of 60 test files byte-identical; its own implementation of the PREREG.v2 BLEU-MBR rule rebuilds the object byte for
  byte, also from the retrained entries; its exhaustive weight fit equals the stored top 20; null test re-run; pass: true.
- panel/novelty.md: status source https://github.com/sigtyp/ST2022 HTTP 200 at 2026-10-18T12:55:22Z (HEAD 03094435,
  unchanged since 2022-05-27; results-surprise-0.30.json identical to the claim's copy); FeVeT unchanged (31898c53), its
  paper and repository print no BLEU; Cognate Transformer prints no BLEU; literature of the last 24 months searched
  (ACL Anthology bibliography, export.arxiv.org API, Europe PMC, Zenodo, OpenReview, Hugging Face papers, github.com
  pages); best published BLEU at 0.30 Mockingbird-I1 0.6058548112827981, best derivable FeVeT 0.6356571184958077, highest
  known our own bar 0.6839233380559118; pass: true. The fetch is under 1 h old at this gate.
- panel/criterion.md: literal criterion met; the disclosures (test BLEU of the entries and the bar seen before PREREG.v2;
  six objects pre-registered, one beat its bar; narrow null) judged; its own null with 100,000 extra controls gives
  p about 5.3e-4 (about 3e-3 with a factor 6 for the six objects); not subsumed by the earlier NED claim on the bar object;
  pass: true; its confirmed_scope is copied above exactly.

## Gate checks (downgrade on any; none applies)
- Hedging panelist: none (three plain pass: true; NOVELTY lists coverage gaps from stopped hosts).
- Reproduction mismatch: none (all entries and the object byte-identical; rule 12 iv of rules/PREREG.md in its strict case).
- Value strictly better than the live table and the bar: 0.6874377388475998 vs our own bar 0.6839233380559118 (margin
  0.003514400791688077 left-to-right, 0.003514400791687966 compensated, both far above 1e-9), FeVeT 0.6356571184958077,
  Mockingbird-I1 0.6058548112827981.
- Stretched criterion or hidden quantifier: none found; the earlier sight of test BLEU values is disclosed in PREREG.v2
  and CLAIM.md; the object is a fixed function of frozen entries, val-0.30 and PREREG.v2's text.
- Scope wider than reproduced: no (one object, one proportion, mean BLEU only).
- Sample presented as complete, capped search, probable prime: not applicable.
- Table value obtained by evasion: no (stop-aware helper; no block recorded by this cell's skeptics).
- Several objects bundled: no.
- PREREG.v2 rule 1: (i) met in both summation modes; (ii) null passed (best_control: 0.0035017194380646544; real:
  0.003514400791687966; 0 of 400 controls at or above real; narrow, as disclosed); sealed checks at 0.30 for all six
  entries (rules/sealed_check_0.30.log and sealed2_check_0.30.log in the claim, both PASS).

Final status: CONFIRMED_SOLUTION, standing only if python3 repo/kit/check_run.py prints CHECK_RUN: PASS for this folder.
