# CRITERION — xs26_08ehmkk8z6a87066
context: subagent

## What was judged
Fresh re-run after CLAIM.md rewrite. Read only this claim package:
`CLAIM.md`, `TARGET_CRITERION.md`, `STATUS.md`, `METHOD.md`, `REPRODUCE.md`,
`result/xs26_08ehmkk8z6a87066.json`, `result/xs26_08ehmkk8z6a87066.rle`.
Did not re-simulate Life, did not re-fetch Catagolue, did not read other claim
folders / INDEX / CHECKPOINT / sibling panel notes for the verdict.

## Bank text (TARGET_CRITERION.md)
Main success requires an RLE in B3/S23 that (1) at gen 0 is only separate
gliders, (2) rewinds cleanly from infinity, (3) settles to exactly the target
apgcode with no debris / escaping ships (unless the page convention says
otherwise), and (4) uses **STRICTLY fewer** gliders than the cost shown for
that apgcode on its Catagolue **object page and tabulation**
(`…/census/b3s23/synthesis-costs/<class>`), re-fetched live before claiming.
Pseudo-listed costs: compare to the listed number; call it a true improvement
only if the new synthesis is all-glider. First synthesis of an object absent
from the class tables also counts.

Partial win **p1**: a strictly cheaper true glider synthesis for an object
whose **current listed cost is at least 60**, verified as above.
(p2 oscillators / p3 converter: not asserted.)

## Independent word senses (not derived from the claim prose)
- **strictly** (with a numeric comparison): fewer and not equal; requires
  `n_new < n_old`, not `n_new <= n_old`.
- **at least**: not less than; `n >=` the stated lower bound.
- **and**: both conjuncts required.
- **tabulation**: the arranged cost table for the class, i.e. the recorded
  cost row for that apgcode — not merely a truncated HTML preview of the
  most expensive rows.
- **shown**: recorded as the value for that apgcode.

## What CLAIM.md now asserts
One sentence: a verified all-glider synthesis builds
`xs26_08ehmkk8z6a87066` with **12** gliders, strictly below the live
Catagolue true cost of **58** (saving 46), meeting the target's **success
criterion**. Explicitly **Not claimed**: partial win p1 (because 58 is below
p1's threshold of 60); full harvest; post-fetch absorption; submission.

Live-cost paragraph (package text): re-fetched 2026-11-06 10:23 ET
(America/Coral_Harbour, UTC-5) — **58 true** on the object page `#CSYNTH`
line, and **58 true** in the xs26 textcensus CSV row
`"xs26_08ehmkk8z6a87066","100000000000000058"`. Notes that the HTML
tabulation page lists only the 200 most expensive of 105952 objects, so
cost 58 does not appear in that HTML slice.

## Package-stated numbers (criterion uses these; no re-sim / no re-fetch)
From `result/*.json`:
- `ok: true`, `structurally_valid: true`
- `n_gliders: 12`
- `rewind_ok: true`
- `final_apgcode: "xs26_08ehmkk8z6a87066"` (exact match)
- `live_csynth: 58`, `live_pseudo: false`
- `improvement: 46`
RLE is `rule = B3/S23`. Method/REPRODUCE describe all-glider verify with
live `#CSYNTH` compare. Construction note (11G seed xs28 + 1G transfer)
is background; the packaged artifact is the 12G synthesis of this xs26.

## Hidden-quantifier / stretch hunt
1. **Main vs p1.** p1 needs current listed cost **at least 60**. Independent
   sense: `58 >= 60` is false. The rewritten CLAIM drops p1 and names the
   main success rule. That is the correct label. No fail on mislabeled p1.

2. **"Strictly fewer" (clause 4).** Independent sense requires `12 < 58`,
   not equality. Package: 12 and 58; `12 < 58` holds. Saving 46 is
   arithmetic on those two package numbers, not a wider claim.

3. **"Object page and tabulation".** Both conjuncts are asserted in CLAIM
   with the same cost 58. Object-page `#CSYNTH … costs 58 gliders (true)`
   matches `live_csynth: 58` / `live_pseudo: false` in result JSON. For
   tabulation: citing the xs26 **textcensus** row that records cost 58 is
   not a stretch of "tabulation" — it is the full class cost table. Treating
   absence from the HTML top-200 slice as "absent from the tables" (first-
   synthesis win) **would** be a stretch; CLAIM does not do that. It reports
   the CSV cost and compares 12 < 58. The bank parenthetical URL names the
   census class path; the HTML view is incomplete for mid-cost rows, so the
   recorded table row is the right referent for "cost shown … on …
   tabulation."

4. **True vs pseudo.** Listed cost is true (`live_pseudo: false`); new
   synthesis is claimed all-glider with `n_gliders: 12`. No pseudo-as-true
   inflation.

5. **Null / subsumption.** Within package evidence this is a cheaper
   all-glider synthesis of **this** apgcode against a stated live true cost
   of 58. CLAIM does not widen to "every cheaper find in the run," does not
   claim Catagolue has kept 58 after a later fetch (explicitly not claimed;
   NOVELTY's job), and does not claim submission. No package evidence that
   a ≤12 synthesis of this same object is already the live baseline.

6. **Clauses (1)–(3).** Package states structurally valid separate-glider
   start, rewind_ok, exact final apgcode, period 1. Life truth is
   REPRODUCE's lane; criterion only checks that the claim's success-label
   matches the bank text given those package-stated facts.

## Verdict
The rewritten claim asserts the **main success criterion**, not p1, and the
package-stated comparison `12 < 58` (true cost on object page and class
tabulation data) satisfies clause 4's "strictly fewer" under independent
senses of those words. This is a genuine, non-subsumed main-criterion win
on the evidence in this package. Partial win p1 is correctly excluded.

confirmed_scope: A package-stated 12-glider all-glider synthesis of xs26_08ehmkk8z6a87066 uses strictly fewer gliders than the claimed live true cost of 58 on both the object page and the xs26 synthesis-costs tabulation data, meeting the main success criterion of catagolue-glider-synthesis-cost-records (not partial win p1).
pass: true
