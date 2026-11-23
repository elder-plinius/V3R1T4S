# CRITERION — xs26_8kk69ba952zw3453

context: subagent

## Job (quoted)
Decide literally whether the result meets the full success criterion or one named enumerated partial win. Hunt hidden quantifiers and stretched definitions; check null models. Write `confirmed_scope`: one exact sentence, no wider than the evidence. Pass only for a genuine, non-subsumed win.

## What was read and checked
- how-we-built-it/TARGET_CRITERION.md, compared against the pinned bank entry catagolue-glider-synthesis-cost-records and the same text in the target's known-unknowns page
- README.md, HOW_WE_FOUND_IT.md, how-we-built-it/PREREG.md, the-record-we-beat/RECORD.md, INDEX.csv (claim wording only)
- object/xs26_8kk69ba952zw3453.rle (independent parse, glider count, rewind, and forward simulation)
- Live Catagolue object page and class tabulation data, fetched once each with no retries, at 10:35:26–10:35:28 ET (America/New_York, UTC-5) on 19 November 2026

Language was judged with Wiktionary (independent of the claim text): "strictly" = in a strict manner; "at least" = at a minimum or lower limit. "True" versus "(pseudo)" is used as the bank entry and the Catagolue #CSYNTH line define it, not as everyday English.

Did not use lifelib or Shinjuku. Did not treat the packaging-run notes already in this folder as a panel vote. Did not write or edit panel/gate.md.

## Criterion text
how-we-built-it/TARGET_CRITERION.md copies the bank success_criterion verbatim, and also copies partial win p1 verbatim: "A strictly cheaper true glider synthesis for any object whose current listed cost is at least 60 gliders, verified as above." p2 and p3 are not copied; they are not claimed. The known-unknowns page carries the same success_criterion and p1 sentences.

## Claim as written
README.md claims the main success criterion only: a 13-glider all-glider synthesis of xs26_8kk69ba952zw3453, strictly cheaper than a live true Catagolue cost of 32 on the object page and in the xs26 synthesis-costs tabulation data. It states that partial win p1 is not claimed, because p1 needs a listed cost of at least 60 and this object's listed cost is 32. p2 and p3 are not claimed. It does not claim a CONFIRMED_* status, does not claim the listed cost will stay 32, does not claim other harvest objects, and does not claim that the 1-glider step is already in Shinjuku. It discloses that the pattern is the published 12-glider route to xs27_g88ehmkia4z0178a6 plus one new glider.

## Literal checks

### TARGET_CRITERION.md versus the bank
The success_criterion paragraph and the p1 statement match the pinned bank entry word for word.

### Does p1 apply?
No. Independent live refetch, one try, no retries:

- Object page https://catagolue.hatsya.com/object/xs26_8kk69ba952zw3453/b3s23 at 10:35:26 ET (America/New_York, UTC-5) on 19 November 2026, HTTP 200, 27635 bytes, sha256 a95b1034d24decdf023875c9af2c2cba1cfc0a4a1ae26e43ad1f9c3957630021. Extracted line: `#CSYNTH xs26_8kk69ba952zw3453 costs 32 gliders (true).`
- Class tabulation data https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs26 at 10:35:27–10:35:28 ET, HTTP 200, 4716955 bytes, sha256 7c74e09466399ebc4dbec487019e1ec3ca21b2c0907e0ee5b9048f568f20aacc. Row: `"xs26_8kk69ba952zw3453","100000000000000032"` (value >= 10^17, so a true synthesis with cost 32).

32 is below 60, so it is not "at least 60" (Wiktionary: at a minimum). Partial win p1 does not apply. The listing is true, not pseudo. The correct framing is the main success criterion, which is the claim the package actually makes.

### Independent synthesis check (own Life simulator, not lifelib or Shinjuku)
object/xs26_8kk69ba952zw3453.rle, sha256 6912e4ea017043ec4300cd01271206b94bcdef91023fbbb4516fbe50de6b9745, rule B3/S23, run 10:35:28–10:35:30 ET (America/New_York, UTC-5) on 19 November 2026:

- Generation 0 is 13 separate 8-connected 5-cell components, each a glider, population 65, and nothing else.
- Rewind of every glider by 2880 generations (4 times the longer bounding-box side) and by 4012 generations (4 times the ceiling of the bounding-box diagonal) shows no glider-glider interaction, and both recover generation 0 exactly. A third rewind of 4004 generations (4 times the ceiling of the cell-corner diagonal) also passed.
- Forward run becomes periodic at generation 1786, period 1, population 26. The final cells match xs26_8kk69ba952zw3453 under one of the 8 symmetries plus a translation, with no other live cells and no escaping glider or spaceship.
- 13 is strictly below the live listed cost 32 on both the object page and the class tabulation data.

Those are clauses (1)–(4) of the main success criterion.

### Hidden quantifiers, stretched definitions, bundling, null models
- One object only. README.md does not claim the rest of the harvest, a new converter, p1, p2, or p3.
- "True" is backed by the live #CSYNTH "(true)." line and the textcensus offset, plus an all-glider RLE.
- Derivative construction does not stretch the main criterion: the packaged RLE is a complete all-glider synthesis of this object. The precursor xs27_g88ehmkia4z0178a6 is a different table cell. Against this object's still-live listed cost of 32, 13 is a non-subsumed main-criterion win.
- Outdated-cost null model: the cost was re-fetched during this review and is still 32 true.
- Pseudo-as-true null model: not this listing.
- p1 is not a fallback here: the listed cost is below 60, and the package does not claim p1.

### Wording
README.md does not overclaim the result. The intended claim is the main success criterion, p1 is explicitly disclaimed because 32 is below 60, the precursor is disclosed, and confirmed status is not asserted. No wording change is required for this vote.

## Verdict
The result meets the main success criterion of catagolue-glider-synthesis-cost-records (not partial win p1). Pass.

confirmed_scope: A 13-glider all-glider synthesis of xs26_8kk69ba952zw3453 that uses strictly fewer gliders than a live true Catagolue cost of 32 on both the object page and the xs26 synthesis-costs tabulation data meets the main success criterion of catagolue-glider-synthesis-cost-records (not partial win p1).

pass: true
