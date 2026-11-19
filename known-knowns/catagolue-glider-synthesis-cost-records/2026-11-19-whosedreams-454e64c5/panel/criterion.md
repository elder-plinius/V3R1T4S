# CRITERION — xs31_g8e1ugmmzd553w643

context: subagent

## Job (quoted)
Decide literally whether the result meets the full success criterion or one named enumerated partial win. Hunt hidden quantifiers and stretched definitions; check null models. Write `confirmed_scope`: one exact sentence, no wider than the evidence. Pass only for a genuine, non-subsumed win.

## What was read and checked
- how-we-built-it/TARGET_CRITERION.md, compared against the pinned bank entry catagolue-glider-synthesis-cost-records
- README.md, HOW_WE_FOUND_IT.md, how-we-built-it/PREREG.md, the-record-we-beat/RECORD.md, INDEX.csv (claim wording only)
- object/xs31_g8e1ugmmzd553w643.rle (independent parse, glider count, rewind, and forward simulation)
- Live Catagolue object page and class tabulation, fetched once each with no retries, at 19:40:43–19:40:45 ET (America/New_York, UTC-5) on 18 November 2026

Language was judged with Wiktionary (independent of the claim text): "strictly" = in a strict manner; "at least" = at a minimum or lower limit. "True" versus "(pseudo)" is used as the bank entry and the Catagolue #CSYNTH line define it, not as everyday English.

Did not use lifelib or Shinjuku. Did not treat the packaging-run notes already in this folder as a panel vote. Did not write or edit panel/gate.md.

## Criterion text
how-we-built-it/TARGET_CRITERION.md copies the bank success_criterion verbatim, and copies partial win p1 verbatim: "A strictly cheaper true glider synthesis for any object whose current listed cost is at least 60 gliders, verified as above." p2 and p3 are not copied; they are not claimed.

## Claim as written
README.md claims partial win p1 only: a 14-glider all-glider synthesis of xs31_g8e1ugmmzd553w643, strictly cheaper than a live true Catagolue cost of 60, with 60 at least 60. It says the main success criterion is also met on these numbers, but that p1 is the intended claim, and that p2 and p3 are not claimed. It does not claim a CONFIRMED_* status, does not claim the listed cost will stay 60, does not claim other harvest objects, and does not claim that the converter steps are new. It discloses that the pattern is the cheaper 12-glider seed xs26_08ehmkk8z6a87066 stitched with published components that add 2 gliders, and that the saving of 46 versus the live 60 is entirely downstream of that cheaper seed.

One wording slip, not an overclaim of the result: HOW_WE_FOUND_IT.md, in the forum-search paragraph for this xs31 object, still names the general query "synthesis" "xs28" 2026.

## Literal checks

### TARGET_CRITERION.md versus the bank
The success_criterion paragraph and the p1 statement match the pinned bank entry word for word.

### Does p1 apply, and is the listed cost true and at least 60?
Yes. Independent live refetch, one try, no retries:

- Object page https://catagolue.hatsya.com/object/xs31_g8e1ugmmzd553w643/b3s23 at 19:40:43 ET (America/New_York, UTC-5) on 18 November 2026, HTTP 200, 8447 bytes, sha256 4f18b74b7b06f34c161507798f2a2ba8f568f97fd1041242b7d333193cdfe9a2. Extracted line: `#CSYNTH xs31_g8e1ugmmzd553w643 costs 60 gliders (true).`
- Class tabulation data https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs31 at 19:40:44 ET, HTTP 200, 2203035 bytes, sha256 83b06ac0d229fa243d8ebdf621900fb3325bd9a6949e65677f81d1ed62e7c422. Row: `"xs31_g8e1ugmmzd553w643","100000000000000060"` (value >= 10^17, so a true synthesis with cost 60).
- HTML tabulation https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs31 at 19:40:45 ET, HTTP 200, does not list this apgcode. That page shows only a short list of expensive objects of the class, not the full table. The complete class table is the textcensus, which does list this object at 60 true. README.md already notes this limit.

60 is at least 60 (Wiktionary: at a minimum; 60 counts). The listing is true, not pseudo. 14 is strictly fewer than 60.

### Independent synthesis check (own Life simulator, not lifelib or Shinjuku)
object/xs31_g8e1ugmmzd553w643.rle, sha256 454e64c5bf7e7b17ab5db6edb0ca6e4b35dd77f88f5233ec179b36c99169748a, rule B3/S23, run 19:43:29–19:43:34 ET (America/New_York, UTC-5) on 18 November 2026:

- Generation 0 is 14 separate 8-connected 5-cell components, each a glider, population 70, and nothing else.
- Rewind of every glider by 3612 generations (4 times the longer bounding-box side) and by 4624 generations (4 times the ceiling of the bounding-box diagonal) shows no glider-glider interaction, and both recover generation 0 exactly.
- Forward run becomes periodic at generation 1819, period 1, population 31. The final cells match xs31_g8e1ugmmzd553w643 under one of the 8 symmetries plus a translation, with no other live cells and no escaping glider or spaceship.
- 14 is strictly below the live listed cost 60.

Those are clauses (1)–(4) of the success criterion, and they are the verification p1 requires.

### Hidden quantifiers, stretched definitions, bundling, null models
- One object only. README.md does not claim the rest of the harvest, a new converter, or p3.
- "True" is backed by the live #CSYNTH "(true)." line and the textcensus offset, plus an all-glider RLE.
- Derivative construction does not stretch p1: the packaged RLE is a complete all-glider synthesis of this object. The cheaper seed is a different table cell. Against this object's still-live listed cost of 60, 14 is a non-subsumed p1 win.
- Outdated-cost null model: the cost was re-fetched during this review and is still 60 true.
- Pseudo-as-true null model: not this listing.
- The "at least 60" threshold is met exactly; it is not stretched below 60.

### Wording
README.md does not overclaim the result. The intended claim is p1, the listed cost is stated as true and at least 60, the derivative seed is disclosed, and confirmed status is not asserted. The remark that the main success criterion is also met on these numbers is accurate, and is not substituted for p1. The only wording slip is the leftover xs28 general-search string in HOW_WE_FOUND_IT.md, which does not widen the claim. No wording change is required for this vote.

## Verdict
The result meets partial win p1 of catagolue-glider-synthesis-cost-records (and would also meet the full success criterion). Pass.

confirmed_scope: A 14-glider all-glider synthesis of xs31_g8e1ugmmzd553w643 that is strictly cheaper than a live true Catagolue cost of 60 meets partial win p1 (listed cost at least 60) of catagolue-glider-synthesis-cost-records.

pass: true
