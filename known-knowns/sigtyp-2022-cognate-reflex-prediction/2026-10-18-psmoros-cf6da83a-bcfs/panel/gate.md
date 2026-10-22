# Honesty gate, cell B50 (proportion 0.50, mean BCFS), run 2026-10-18-0847 (kit RUN.md step 7)

Written 2026-10-18T12:39:05Z (date -u) by the main session (Opus 5.5, claude-opus-5-5[1m]) after reading all three panel files.

status: CONFIRMED_SOLUTION
confirmed_scope: At proportion 0.50, the frozen stage-2 combination combiner/test/0.50 (the same predictions as object/predictions-0.50.tsv) of 8 entries, which read only the 10 surprise families' training-0.50.tsv, the masked test-0.50.tsv one masked-language partition at a time, and the task release's development-family training-0.10.tsv and masked test-0.10.tsv files (no solutions file of any family), scores mean B-Cubed F-score 0.7114179305724276 over the 10 SIGTYP 2022 surprise families under the pinned ST2022 scorer (commit 03094435, the same value under left-to-right and builtin summation), strictly above Mockingbird-I1's official 0.6050308536957327 in results-surprise-0.50.json and above the cell's stricter bar, FeVeT's published predictions rescored at 0.6423935720824072; this is a win on mean BCFS at 0.50 only.

## Panel (three fresh contexts, Agent tool, model opus = Opus 5.5; each saw only its own copy of claim/)
- panel/reproduce.md: wrote its own scorer from the pinned compare_words (Mockingbird-I1 reproduced bit for bit), recomputed
  the bar from FeVeT's files, checked every freeze hash, retrained all 8 stage-2 entries (weight 0 included) from their
  frozen code with only training-0.50 and the development view readable: 80 of 80 test files byte-identical; rebuilt the
  object byte for byte with its own MBR implementation; isolation audits of its own; pass: true.
- panel/novelty.md: status source https://github.com/sigtyp/ST2022 HTTP 200 at 2026-10-18T11:44:55Z-11:45:09Z (HEAD
  03094435 unchanged since 2022-05-27; official results-surprise-0.50.json byte-identical to the claim's copy); FeVeT
  repository unchanged (31898c53); literature of the last 24 months searched (ACL Anthology bibliography, export.arxiv.org
  API, Europe PMC, Zenodo, OpenReview or OpenCitations, GitHub, Open Research Europe); the NOVELTY skeptic found a higher published BCFS on the official scale than the PREREG bar: CogTran-small 0.6477 (Akavarapu and Bhattacharya, EMNLP 2023, Table 5; its Mockingbird row equals the official 0.6050). By PREREG rule 2 it becomes this cell's bar; the candidate beats it by 0.0637179306 (computed by the skeptic). FeVeT's printed 0.673 is a language-pooled mean (candidate on that scale 0.742250); pass: true. The fetch is
  under 1 h old at this gate (< 6 h), so no re-fetch.
- panel/criterion.md: literal criterion met (training-0.50, development families, row-isolated masked test-0.50
  partitions, weights fit on a split cut from training-0.50); judged the disclosed development-family rows (classifier
  entries; mannburmish for hillburmish, listsamplesize for kesslersignificance) within the letter and spirit, with
  counterfactuals showing the win does not rest on them; null test re-run; pass: true; its confirmed_scope is copied above
  exactly.

## Gate checks (downgrade on any; none applies)
- Hedging panelist: none (three plain pass: true; the NOVELTY skeptics state residual coverage gaps from stopped hosts:
  Semantic Scholar, OpenAlex, Crossref, dblp, arxiv.org web, and api.github.com after 11:55:06Z; listed in the report).
- Reproduction mismatch: none (every entry and the object reproduced byte for byte; PREREG rule 12 iv, strict case).
- Value strictly better than the live table and the bar: candidate COMB-8 mean BCFS 0.7114179305724276 (higher is better) vs
  FeVeT 0.6423935720824072; margin 0.06902435849002042 (left-to-right; the same order in compensated summation), far above 1e-9.
- Stretched criterion or hidden quantifier: none found by CRITERION; the development-family rows are disclosed in the claim.
- Scope wider than reproduced: no; the scope is the CRITERION sentence, one object at one proportion on mean BCFS only.
- Sample presented as complete, capped search, probable prime: not applicable.
- Table value obtained by evasion: no (one honest GET per resource through the stop-aware helper; blocks recorded in
  logs/stops-2026-10-18-0839.tsv and never retried).
- Several objects bundled: no (one cell, one object; the same object is claimed separately in the sibling cells on the
  other two metrics, as the criterion's "a win on one metric is a win on that metric only" requires).
- PREREG rule 12: (i) met in both summation modes; (ii) null test passed (best_control: 0.010059480747746763; real: 0.06902435849002053; 0 of 400
  controls at or above real); (iii) every stage-2 entry passed the harness test-mode audit at 0.50 and the sealed check at
  0.50 (runs/2026-10-18-0839/out/sealed_carry_0.50.log and sealed_new_0.50.log, both SEALED_CHECK 0.50 PASS); (iv)
  REPRODUCE retrained every entry byte-identically.

Final status: CONFIRMED_SOLUTION, standing only if python3 repo/kit/check_run.py prints CHECK_RUN: PASS for this folder.
