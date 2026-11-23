# Criterion skeptic: matsp instance 155 (155_28_10_2), claimed penalty 0 vs best known 24

context: fresh subagent started for this claim only

Inputs read: CLAIM.md, target.md, PREREG.md, PREREG.sha256, SHA256SUMS, REPRODUCE.md, code/verify_claim.py, data/ProblemDefinition.txt, data/matsp.html, data/changes.html, data/fetched-utc.txt, data/8_7_20_2.txt, data/8_7_20_2.Solution.889.xml, data/155_28_10_2.txt, data/155_28_10_2.ros (header and tags), object/155_28_10_2.Solution.0.xml. Nothing in claim/ was modified.

## Integrity
- `sha256sum -c SHA256SUMS`: all OK. `sha256sum -c PREREG.sha256`: OK. object/155_28_10_2.Solution.0.xml is byte-identical to data/selected_solution.xml (the preregistered object, sha256 ebc23f1e...dac9b).

## Clause-by-clause reading of the success criterion (target.md, "What counts as a win")
1. "one instance listed on .../matsp/ with a positive 'Best known' value": data/matsp.html (226 data rows parsed) lists `155 | 28 | 10 | 2 | 24 | TRA26`. 24 > 0. Instance 5 (value 0) is not the target. MET.
2. "an independent checker written from the published ProblemDefinition.pdf": code/verify_claim.py is standalone (stdlib only, imports nothing from code/matsp.py or code/cpsat_matsp.py). Compared line by line with data/ProblemDefinition.txt:
   - C1 one shift per calendar day, one start, one length: duplicate-day check; length 360-600 min in 15-min steps (L = {24..40}). Matches.
   - Allowed starts (00:00, 06:00-10:00, 14:00-18:00, 20:00-23:45; no 00:00 on day 0; only 00:00 on day h): `allowed()`. Matches (it numbers days 1..h+1 internally, i.e. definition day + 1).
   - C2 shifts end within the horizon: `u > N` check. Matches (applied to all days, a superset).
   - C3 14 h rest between shifts on consecutive calendar days: `byday[d][1] > byday[d+1][0] - 56`. Matches.
   - C4 total minutes in [b_e, c_e]. Matches.
   - C5 at most 5 working days in each 6-day window d = 0..h-5. Matches (range(1, h-3) in 1-based days).
   - C6 minimum activity duration, literal pattern 0,1^s,0 for s = 1..3, with zero padding past the horizon. Matches the literal formula (which does not reach a run starting at interval 0; irrelevant here, see spot check).
   - C7 activities only inside shifts, one per interval: occupancy is built from the task blocks, overlaps flagged. Matches.
   - C8 cover >= v (hard) and objective sum over (i,a) of max(0, cover - w)^2. Matches the MIQP objective.
   MET.
3. "which first reproduces penalty 889 on the site's example file 8_7_20_2.Solution.889.xml": I ran `python3 code/verify_claim.py data/8_7_20_2.txt data/8_7_20_2.Solution.889.xml 890` -> `violations 0, penalty 889`. MET. Null model on the day convention: re-reading the example with 1-based days (my own checker) gives 24 hard violations and penalty 920, so the 889 match pins the 0-based Day convention and the cover-line indexing; it is not a trivially reproduced number.
4. "reports all hard constraints satisfied and a total penalty strictly below that instance's 'Best known' value": `python3 code/verify_claim.py data/155_28_10_2.txt object/155_28_10_2.Solution.0.xml 24` -> `violations 0, penalty 0, record 24, PASS`. 0 < 24. MET.
5. "A solution in the site's XML solution format": the claimed file uses the same element tree as the site's example (Solution / ProblemFile / Penalty / Employee@ID / Shift / Day / Start hh:mm:ss / Task / ID / Length), 0-based Day like the example, all 10 employees of the instance. Differences from the example: no xsi:noNamespaceSchemaLocation="Solution.xsd" attribute, no optional-looking metadata (TimeStamp, Author, Reference, Machine, SolveTime), and no `WorkLength` attribute on Task (in the example it equals Length on all 140 Task elements). Solution.xsd is not in claim/, so schema validity cannot be checked here. I count it as the site's format (same structure and semantics, redundant fields omitted), with the caveat that the human's optional RosterViewer/verifier cross-check, or adding WorkLength="<Length>" to every Task, would settle the remaining doubt. MET with caveat.
6. "with the table and changes.html re-fetched live immediately before claiming": data/fetched-utc.txt = 2026-11-22T08:03:12Z; run directory is 2026-11-22-0805, i.e. about 2 minutes before claim/ was built. data/changes.html newest entry is 29-Oct-2026 (nurse instances); no multi-activity entry after 07-Oct-2026 (verifier release). The table still shows 24 for 155. MET for the claim as built; "immediately before claiming" also binds the filing itself: per PREREG.md check 3, the lead must re-fetch both pages at filing and withdraw if 155's best known has dropped to <= 0 (the claimed penalty), and should re-check the row if any new multi-activity entry appears. Not checkable by me now; it is a filing condition, not a defect.
7. "Cross-checking with the closed-source verifier ... optional and done by the human; nothing emailed or submitted by the agent": no binary in claim/, no submission artefact; REPRODUCE.md uses only verify_claim.py and an optional OR-Tools re-solve. MET. If the human's official-tool check disagrees, the claim must be withdrawn (target.md, "How a win is checked").

## Code-independent spot check (my own checker, written from data/ProblemDefinition.txt, run in a scratch directory)
- Reproduces 889 on the example with 0 hard errors (814 over-cover cells); 1-based variant fails as above.
- On object/155_28_10_2.Solution.0.xml: 5376/5376 cover lines parsed (28 days x 96 x 2 tasks, no gaps or duplicates), employee set equals the instance's, 0 hard errors (starts, lengths 24-40 intervals, horizon, rest, minutes, 5-in-6, overlaps, every maximal task run >= 4 intervals including at interval 0), 0 under-cover cells, 0 over-cover cells, penalty 0.
- Extra conservatism beyond the definition: minimum rest between ANY two consecutive shifts in absolute time is 840 min (exactly 14 h); maximum run of consecutive working days is 5 (consistent with the .ros `MinRestTime 840`, `MaxSeq 5`, task min length 60).

## Hidden quantifiers, stretched definitions, null models
- "Optimal" in CLAIM.md: penalty is a sum of squares of non-negative integers, so 0 is a trivial lower bound; the optimality remark is correct and adds nothing contested.
- No statistic involved; PREREG.md's "null_test: not needed" is right. The relevant null (a checker that would score anything low) is ruled out by the 889 reproduction and by the 1-based-day perturbation scoring 920/658 with violations.
- Shared-misreading risk (solver and verifier from the same team) is mitigated by the 889 match and by my separately written checker agreeing on every count.
- Not subsumed: the full criterion is met; this also falls inside the partial win matsp-small-instance-improve (instance 155, 10 staff), which the full win subsumes, not the other way round.
- How it was found (overnight CP-SAT run under a frozen plan, seed 1) does not enter this criterion, which judges only the roster, the checker and the live status. workhorse/plan.json is outside claim/ and was not examined; nothing in the verdict depends on it.

confirmed_scope: The roster object/155_28_10_2.Solution.0.xml for instance 155 (155_28_10_2) satisfies every hard constraint of ProblemDefinition.pdf and has total penalty 0 under two independent checkers that both reproduce 889 on 8_7_20_2.Solution.889.xml, strictly below the best known value 24 (TRA26) in the table fetched 2026-11-22T08:03:12Z, subject to a live re-fetch of the table and changes.html at filing and to the human's optional official-verifier cross-check not disagreeing.

pass: true
