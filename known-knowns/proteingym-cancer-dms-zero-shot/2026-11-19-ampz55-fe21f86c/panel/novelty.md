# NOVELTY verdict — BORDA-12 on PTEN_HUMAN_Matreyek_2021

context: subagent (fresh panel context, claim package only)

Scope: novelty only. I judged only from claim/claim.md and claim/scout.md plus my
own fresh fetches below. I did NOT recompute the claimed 0.5682 Spearman — that is
the REPRODUCE/CRITERION skeptics' job. This verdict is conditional on 0.5682 being
verified by them.

## 1. Live ProteinGym table — re-fetched once, honestly

- URL: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
- Fetch: one plain curl GET, User-Agent "V3R1T4S (novelty panel)", 2026-11-19 10:41:02 UTC. HTTP 200, no retry, no block.
- sha256: f432423b87f79ac9778dfac86e3d95be041d246bc618dc0a406b35b0b7466437 — byte-identical to the claim package's record (claim/scout.md: fetched 2026-11-19 10:34 UTC, same sha256).
- Row PTEN_HUMAN_Matreyek_2021, max over numeric model columns only (metadata 'Number of Mutants' excluded): best 0.516 (VenusREM), n = 5,083. Bar 0.531.
- Comparison: 0.5682 beats the live best by +0.0522 and the bar by +0.0372. Both margins are far above the bank criterion's 0.015 threshold, and the claim's own bootstrap 95% CI [0.5486, 0.5886] sits entirely above the 0.531 bar. The margin over the live table is real, not noise.

## 2. V3R1T4S pull requests — checked via the GitHub API (one honest read each)

- Search `repo:elder-plinius/V3R1T4S type:pr proteingym`: total_count 2. #467 open, #463 closed. No other proteingym PR exists.
- PR #467 (open, created 2026-10-18, updated 2026-10-28, unmerged): body read directly. Its table states M1 on PTEN_HUMAN_Matreyek_2021 = 0.5658 vs table max 0.516 (+0.0498). Confirmed: M1 still stands at 0.5658 on Matreyek.
- PR #463 (closed, unmerged): same M1, 0.5658 on Matreyek (body read directly; states 0.56576).
- A full open-PR listing (first 100) contains no other proteingym claim; the targeted search above is the authoritative check.
- 0.5682 is strictly greater than 0.5658 as a point value (+0.0024).

## 3. TROPHY_CASE.md

Read in full (53 rows). No entry mentions proteingym, PTEN, Matreyek or VenusREM. No merged record for this target exists in the repo.

## 4. Literature, last 24 months (arXiv, Zenodo, GitHub) — web search, all sources actually opened

Searched for zero-shot PTEN Matreyek scores above 0.5682. What I found:

- VenusREM (Tan et al., Bioinformatics 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12261477/): the live-table leader at 0.516 on Matreyek. Already the table value; not above the claim.
- VenusRAR / Rank-and-Reason (arXiv:2602.00197, opened and searched in full text): claims a new ProteinGym *global average* Spearman of 0.551 (vs 0.518). No per-assay Matreyek value is reported anywhere in the paper (find for "Matreyek": zero hits). A global average of 0.551 cannot beat a per-assay bar of 0.5682, and no Matreyek number is published.
- LoMuS (Bioinformatics 2026, btag509; supplementary Table S5 opened via search): reports 0.6506 on "PTEN HUMAN Matreyek 2021" — BUT it is explicitly a supervised result: "LoMuS is evaluated as a supervised sequence-only model using per-assay train/validation/test splits", on a 509-variant held-out test split, i.e. trained on the assay's own labels. The bank criterion requires zero-shot with respect to the assay and forbids any measurement from any ProteinGym DMS assay of the same UniProt protein entering the method. LoMuS is therefore excluded by the criterion and is not a competing zero-shot result. (It is also not on the full 5,083-mutant set.)
- RankFlow (ICLR 2026 note): supervised/fine-tuned, category aggregates only, no per-assay Matreyek value.
- DynamicsPLM (2026-11-13): zero-shot, but claims SOTA only among sub-100M models on the global benchmark; no per-assay Matreyek value found.
- BioModelBench proteingym_suite run 20261103: a zero-shot ensemble at 0.519 *global* Spearman — below the claim and not per-assay.
- SSEmb (Nat Commun 2024): PTEN Mighell 0.422, a different assay, far below the bar.
- No Zenodo or GitHub source with a zero-shot per-assay Matreyek score above 0.5682 was found.

Conclusion: no known zero-shot result on PTEN_HUMAN_Matreyek_2021 exceeds 0.5682. The highest known values are: live table 0.516 (VenusREM), disclosed M1 0.5658 (PR #467/#463), claim 0.5682.

## 5. The noise caveat — decided explicitly

The claim package states, and I accept as stated: margin over M1 is +0.0024, bootstrap CI on the difference [-0.0172, +0.0228], P(BORDA12 > M1) = 0.592. The margin over M1 is inside noise.

Do I treat a point-value win inside noise as a record? YES, for this bank criterion — with the qualification below — for three reasons:

1. The bank criterion is defined on point values ("STRICTLY HIGHER ... by at least 0.015 absolute" vs the live table), not on statistical significance. The claim exceeds the live table by +0.0522, a margin far outside noise. The criterion the claim is actually judged against is met decisively.
2. The M1 comparison is a novelty bar, not the criterion. M1 is an unmerged, unpublished PR from the same project, and BORDA-12's computed point value is strictly higher than it (0.5682 > 0.5658; not a tie at the reported precision — the values differ in the third decimal). No other known zero-shot result is above 0.5682.
3. The claim discloses the noise honestly in claim/claim.md rather than hiding it; the record as stated is a best-known point value, not a claim of demonstrated superiority over M1.

Qualification that must travel with the claim: the +0.0024 over M1 is NOT evidence that Borda combining beats z-score combining — P = 0.592 is a coin flip, and BORDA-12 recombines M1's exact same 12 members. The honest statement is "new best-known point value on this assay (0.5682), beating the live table by a real margin; the improvement over the previous best-known point value M1 (0.5658) is within noise and not demonstrated." A future re-scoring could flip the M1/BORDA-12 ordering. The panel should not let the claim be presented as "Borda beats M1".

## Verdict

0.5682 strictly beats everything known for zero-shot PTEN_HUMAN_Matreyek_2021: live table 0.516, disclosed M1 0.5658, and no literature result above it. The record is thin over M1 (inside noise) but decisive over the live table (the actual criterion). Pass, with the noise qualification in section 5 attached.

pass: true
