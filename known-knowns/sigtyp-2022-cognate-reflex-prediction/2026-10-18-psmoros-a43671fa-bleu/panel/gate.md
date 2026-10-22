# Honesty gate, cell LA (A_BLEU, the aggregate over the five proportions 0.10-0.50), session 2026-10-18-1758 (kit RUN.md step 7)

Written 2026-10-18T22:54:34Z (date -u) by the main session (Opus 5.5, claude-opus-5-5[1m]) after reading all three panel files in full,
and after the three 0.40 gates (runs/2026-10-18-1758, -1809, -1811 panel/gate.md), as PREREG rule 3 requires.

status: CONFIRMED_SOLUTION
confirmed_scope: The frozen single system classifier/PRIMARY (attempts/classifier/frozen/PRIMARY/code, trained at each proportion P on training-P alone) has test predictions attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv for P = 0.10, 0.20, 0.30, 0.40, 0.50 (rebuilt exactly from object/predictions-P.tsv) that reach an aggregate A_BLEU = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5 of the 10-surprise-family mean BLEU of 0.6729772402356671 under the pinned official ST2022 scorer, strictly higher than Mockingbird-I1's A_BLEU of 0.6015772270938825 computed the same way from its official results-surprise-P.json totals (margin 0.0714); this is a win on BLEU only.

## Panel (three fresh contexts, Agent tool, model opus = Opus 5.5; each saw only its own copy of claim/)
- panel/reproduce.md: own scorer from the pinned compare_words (Mockingbird-I1 reproduced bit for bit at all five P, left
  to right; its aggregate recomputed); claimed per-P values and the aggregate recomputed in both summation modes; MANIFEST,
  freeze, object and record hashes checked; the entry retrained from its frozen code at EACH of the five proportions in fresh
  folders: all 50 test-P files byte-identical (bit-deterministic; PREREG rule 12 iv, strict case); read traces or sandboxed
  stages and row-isolation tests of its own; pass: true.
- panel/novelty.md: github.com is host-stopped for this session (429 at 2026-10-18T21:48:35Z), so the skeptic fetched the
  primary table itself: the five official results files on the main branch from raw.githubusercontent.com (one GET each,
  HTTP 200 at 2026-10-18T22:10:57Z-22:11:31Z), each byte-identical to the pinned copy at 03094435; no published five-proportion
  aggregate exists; FeVeT and Cognate Transformer report 0.10, 0.30 and 0.50 only; Mockingbird-I1's aggregate is the best
  official one (Mockingbird-N2's lower number is a missing-file placeholder); pass: true. The fetch is under 1 h old at this
  gate (less than 6 h), so no re-fetch.
- panel/criterion.md: the aggregate is stated in PREREG rule 2 (body hash equal to the frozen body); the score aggregate is a
  fair, literal reading (the win also holds per proportion, in every family-by-proportion cell, and under the README's rank
  reading); one frozen system retrained per proportion; development-family rows and the selection note judged within the
  letter and spirit with counterfactuals; null test reproduced independently; pass: true. Its confirmed_scope is copied above
  exactly.

## Gate checks (downgrade on any; none applies)
- Hedging panelist: none (three plain pass: true). Coverage gaps the NOVELTY skeptics state: stopped hosts (github.com,
  api.github.com, arxiv.org, api.semanticscholar.org, dblp.org, scholar.archive.org, ieeexplore.ieee.org), so the V3R1T4S
  pull-request list could not be re-read live (scout copy of 18:07:43Z: no pull request on this target).
- Reproduction mismatch: none (50 of 50 files byte-identical in each REPRODUCE run).
- Value strictly better than the bar: A_BLEU 0.6729772402356671 (higher is better) vs Mockingbird-I1's aggregate 0.6015772270938825; margin 0.07140001314178457
  (left to right; also with builtin summation), far above 1e-9.
- Stretched criterion or hidden quantifier: none found. The aggregate form is the criterion's own ("aggregated over all 5
  proportions, stated in PREREG.md"); "best official system on this aggregate" in CLAIM.md means among official systems with
  all five proportions (Mockingbird-N2 submitted 0.10 only; its JSON rows at 0.20-0.50 are placeholder zeros), as the NA
  CRITERION skeptic notes.
- Scope wider than reproduced: no (one cell, one statistic, one object: attempts/classifier/frozen/PRIMARY/test/P for the
  five P).
- Table value obtained by evasion: no. The status page's host was stopped mid-session by a skeptic's search; no stopped URL or
  host was requested again; the official results files were read from raw.githubusercontent.com, a separate unstopped host
  (flagged for the human in the report).
- Several objects bundled: no (the same object carries two sibling aggregate cells on the other metrics; each is its own cell).
- Null test: 400 controls, best control 0.006990622234683363 vs real 0.07140001314178449, real_beats_all_controls yes (null_test.md).
- Sealed check at every P: rules/sealed_cand_0.10/0.20/0.30/0.40/0.50.log, each ending SEALED_CHECK P PASS.
- Charter order ("claimed only after both lanes report"): every proportion was reported by the lane that held it (this lane
  held all five after the HANDOFF); the report names this reading for the human.
