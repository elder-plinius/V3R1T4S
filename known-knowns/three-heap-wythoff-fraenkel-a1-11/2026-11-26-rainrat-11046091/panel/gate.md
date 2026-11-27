# Honesty gate (`three-heap-wythoff-fraenkel-a1-11`)

status: CONFIRMED_SOLUTION
confirmed_scope: Both of Fraenkel's three-heap Wythoff conjectures are proved and independently verified from the game rules for smallest heap A_1 = 12 (together with the full prerequisite inductive chain m = 0..11, including Sun and Zeilberger's Table 1 for m = 0..10 and N_3^i, B_{N_3^i}^i for all 0 <= i <= 11), with explicit thresholds (n_2, n_1) = (601, 1762) and derived constants satisfying Claims 3.3, 3.4, and 3.5 (under the intended midpoint alpha' = floor((max + min)/2)) as well as a self-contained Lemma 2.6 direct induction proof.

## Gate notes
- Object: `wythoff_a1_12_certificate.json`, sha256 `1104609158ffe4f753070d369f788ee0ae891427af6c8407cb961a5bd9843e1f`.
- Panel verdicts: `reproduce.md` `pass: true`, `novelty.md` `pass: true`, `criterion.md` `pass: true`.
- `confirmed_scope` matches `panel/criterion.md` word for word.
- All three skeptics ran in fresh subagent contexts seeing only `claim/`.
- Primary status source (`GONC6-04.pdf`) was fetched honestly on `2026-11-25T07:12:29Z` (run scout) and independently on `2026-11-25T07:19:48Z` (novelty skeptic), both returning `HTTP 200` and SHA-256 `cc1b985ef7fa16d79877677a49b59eb65924a6d082341ae53348544c22cde1f1` (< 15 minutes old).
