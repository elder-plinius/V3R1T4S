# Criterion verdict
context: fresh subagent started for this claim only

Claim judged: claim/ (version 2), "lower-bound certificates on 5 ITC2021 instances". I read only claim/, the live bank entry, repo/kit/POLICY.md and repo/kit/RULES.md. I did not read claim-v1/, panel-v1/ or any other panel file. Working files are in panel/work-criterion-v2/. `sha256sum -c claim/SHA256SUMS`: 46 of 46 OK, so the claim is unchanged since its freeze.

## Method

- Fetched once each, User-Agent "V3R1T4S-research-client (criterion skeptic)", 2026-11-27T15:30:43Z to 15:30:44Z. All seven requests returned HTTP 200: the bank entry (raw GitHub), the board, and the five history pages (panel/work-criterion-v2/fetch/).
- The live bank entry is byte-identical to claim/data/target_live.md. claim/target.md differs from it only by the leading line `id: itc2021-sports-timetabling-ub` and a blank line.
- My board fetch is byte-identical to claim/data/board.html (sha256 e008069e…2f75). All five history pages are byte-identical to claim/data/hist/*.html, with the same sha256 values as claim/data/fetch.json. Nothing has changed since the claim's fetch at 14:48:34Z.
- Model replay: I copied each bound.pbtxt into panel/work-criterion-v2/models/; the sha256 values match the claim. My own script (myreplay.py) parses each copy into a fresh CpModel and solves it with OR-Tools 9.15.6755, num_workers 1, random_seed from rows.csv, linearization_level 2 and a 600 s cap. The models have no solution hints and no assumptions. I also replayed Early 14 and Early 9 at the default linearization level, because their saved logs used it.
- I ran copies of the standard-library scripts (both certificate.py files and code/break_floor_stdlib.py) on copies of the original instance files.
- I ran RobinX built from source (binary sha256 080fcf6b…1142) and a copy of code/verify_timetable.py on copies of the Early 14 record and instance.

## Verbatim criterion (live bank entry, 2026-11-27T15:30Z)

> - **itc2021-lower-bound-certificate:** A strictly higher lower bound for any open instance, given as a saved MIP/CP model file plus solver log and seed whose dual bound a skeptic re-runs to the same value (or better) in a fresh session; or, more strongly, a feasible timetable whose penalty equals the listed Best LB, which closes the instance and is checked by the validator alone.

claim/target.md has the same text. CLAIM.md quotes the first clause correctly, without "(or better)", which does not matter here.

## Per-row results

Board values are (infeasibility, penalty). "History max LB" is the largest lower bound on the history page.

| instance | board LB / UB | open? | history LB entries (max) | claimed | strictly higher? | seed (rows.csv = log) | log: status / best_bound | my replay (lin 2) | stdlib script |
|---|---|---|---|---:|---|---|---|---|---|
| Early 14 | (0,1) / (0,4) | yes | 0, 1 (max 1) | 4 | yes | 20261124 = 20261124 | OPTIMAL / 4 | OPTIMAL, bound 4.0, 0.0 s (default lin: 4.0) | certificate.py: "Lower bound on Early 14: 4" |
| Early 9 | (0,0) / (0,56) | yes | 0 (max 0) | 40 | yes | 20261125 = 20261125 | OPTIMAL / 40 | OPTIMAL, bound 40.0, 0.0 s (default lin: 40.0) | certificate.py: "Lower bound on Early 9: 40" |
| Middle 6 | (0,24) / (0,1090) | yes | 0, 2, 24 (max 24) | 60 | yes | 20261126 = 20261126 | OPTIMAL / 60 | OPTIMAL, bound 60.0, 165.2 s | break floor: total breaks >= 22, LB 60 |
| Middle 9 | (0,0) / (0,415) | yes | 0 (max 0) | 20 | yes | 20261126 = 20261126 | OPTIMAL / 20 | OPTIMAL, bound 20.0, 34.3 s | break floor: >= 17, so 18 (even), LB 20 |
| Late 9 | (0,3) / (0,498) | yes | 0, 3 (max 3) | 20 | yes | 20261126 = 20261126 | OPTIMAL / 20 | OPTIMAL, bound 20.0, 56.4 s | break floor: >= 18, LB 20 |

- Each row has a saved model file (object/<instance>/bound.pbtxt), a solver log (bound.log, CP-SAT v9.15.6755) and a seed. The seed in each log's Parameters line equals the seed in rows.csv.
- My fresh-session dual bound equals the claimed value and the logged best_bound in all five rows.
- The three larger logs also set max_deterministic_time 30. My replays had no deterministic-time cap and still reached the same OPTIMAL bound.
- CLAIM.md, rows.csv and my numbers agree in every row: posted LB, claimed bound, Best UB, replay status and seed.
- The "other published bound" column agrees with the text. Early 14's "1 (CPLEX, Rosati et al. 2022)" equals the posted LB. Early 9 and Middle 9 show 0, meaning nothing above the posted bound. Middle 6's 39 and Late 9's 5 are attributed to Team MODAL bound files that are not on the board.
- I could not check the Rosati et al. and Team MODAL values, because fetching them was outside my allowed sources; that belongs to the NOVELTY skeptic. Either way, every claimed bound is far above them (60 > 39, 20 > 5, 4 > 1).
- The text hedges this column as "every other published bound the authors know of", which is not an overstatement.

Literal fit, first clause: all five instances are open on the live board. Each claimed bound is strictly above the posted Best LB and above every bound on its history page. Each comes with a model file, a log and a seed, and each re-runs in a fresh session to exactly the claimed value. **The first clause holds literally for all five rows.**

Caveat on how the bound is "given". For two rows, the model's dual bound is a bound on the instance only together with a hand proof:
- **Early 14:** the model adds "at most one break per team" (cp_bound.py: `sum(breaks) <= 1`). That is not valid for every feasible timetable. It is valid only in the case "penalty < 10", and PROOF.md covers the other case.
- **Early 9:** the model has 4 variables and 5 constraints that encode the conclusions of the lemmas in PROOF.md. These are: total repeats >= 15 + Team 2's repeats; >= 19 if Team 2 has an odd-index repeat; the total is even; cost = 10·(total − 16). The solver checks only that arithmetic.

The bank text does not require the model to be a stand-alone relaxation, and CLAIM.md says both things openly. So I count this as meeting the literal criterion, not as a failure. Whether the hand steps are valid is for the REPRODUCE skeptic. I checked them anyway and found them sound:
- Early 9: at most two break-free teams; a balanced one-repeat sequence repeats at an even index; equal home-home and away-away repeats at each transition, because every slot has 9 home teams. Together these give >= 20 repeats. The instance has BR2 intp 16, penalty 10, all teams and all slots, so the penalty is >= 40.
- Early 14: BR2 intp 18, penalty 10, all 20 teams and all 38 slots.

## Early 14 judgment

- **Score of the record.** RobinX (source build) on data/records/ITC2021_Early_14.record.xml with data/inst/ITC2021_Early_14.xml gives Objective 0 / 4: four CA1 soft violations by teams 0 and 15, cost 1 each. My copy of verify_timetable.py gives "valid compact double round robin; hard violations 0; penalty 4 (venue 4 + opponent 0) {'CA1': 4, 'BR1': 0, 'BR2': 0, 'FA2': 0}". **Score (0, 4) confirmed by both.** The file's metadata names Team Gionar, 24 June 2021, objective 4, which matches the history page entry "24 - 6 - 2021, Team Gionar, (0, 4)" and the board's Best UB (0, 4).
- **"Bound equals that timetable's penalty, so it is optimal."** Accurate, provided the bound 4 is valid.
- **"First clause, not the second."** Accurate. The second clause needs a timetable whose penalty equals the *listed* Best LB, which is 1. The record scores 4, so the second clause does not apply, and the claim correctly does not say that it does.
- **"Covers one case of a two-case proof."** Accurate and disclosed. PROOF.md argues that penalty <= 3 means at most 18 breaks (a 19th break costs 10 under BR2). At most two teams are break-free, so every team has at most one break. Under that case, the minima of the CA1 sums for teams 0 and 15 are 3 and 1, so the penalty is >= 4. That is a contradiction, so the optimum is 4. CLAIM.md's version ("holds whenever the penalty is below 10") is correct and slightly stronger than PROOF.md needs.
- **One wording slip.** CLAIM.md says "(more breaks cost at least 10 under BR2 and the BR1 rules)". The argument needs only BR2. The soft BR1 rules in Early 14 cost 5 each, and PROOF.md never uses BR1. This misattributes part of the argument but does not widen the claim. It should be cut to "under BR2".
- **Overall.** The Early 14 paragraph is accurate and not overstated, apart from the BR1 phrase.

## Overstatement and policy findings

1. **Scope words.** None of "solved", "first", "record" or "breakthrough" appears. "Not claimed" excludes new timetables, best-possible bounds, and optimality of any instance other than Early 14. The result label PROVED-HERE is qualified ("in the sense that every bound was replayed and re-derived in this claim run"), and the text says the certificates were made earlier by teammate agents. That disclosure appears in both CLAIM.md and PREREG.md. No overstatement of the result.
2. **"A standard-library script that re-derives the bound from the original instance file"** is only partly true for Early 9 (minor imprecision). certificate.py parses the instance and asserts the BR2 parameters (intp 16, penalty 10, all teams and slots). It also enumerates Team 2's venue patterns and asserts the finite lemma (16 survivors, all with 3 repeats, each with an odd repeat index). But it then prints "Minimum possible total repeats: at least 20" and "Lower bound on Early 9: 40" as fixed strings. The general pigeonhole and parity steps live only in PROOF.md, though they do not depend on the instance. The Early 14 script likewise works only inside the at-most-one-break case. Together with the CLAIM.md sentence that the Early 9 model is an arithmetic summary of PROOF.md, a reader is told where the proof lives. Still, the Early 9 bound is the most hand-dependent row, and the sentence suggests more machine checking than exists. Suggested wording: "re-checks the instance-specific premises of the proof".
3. **BR1 phrase** in the Early 14 paragraph (see above). Minor inaccuracy.
4. **Rule 4 ("One object or table cell per claim") against a 5-row batch.** CLAIM.md admits the rule and says the batching follows "Boss's explicit decision of 2026-11-27 to file the full wins and the partial wins as two separate filings". PREREG.md quotes the human as "I want the full wins and the partials to be filed separately" and "Do it". The quoted words require separation of full and partial wins; they do not literally say "all five partials in one claim". The phrase "two separate filings" is the claim author's reading, unless "Do it" answered a proposal that said so, which the package does not show. RULES.md lets only the human's own messages outrank rule 4, so **the gate should confirm the human's actual words authorise one claim of five cells**. Separately, the claim keeps each cell independently checkable: one model, log, seed and script per row, and a counting rule that drops failing rows. Every row passes on its own, so the batching changes no row's verdict.
5. **Credits (rule 13).** Present:
   - Team Gionar (Early 14 record), Bobby (Codex), Charlie (Antigravity), Andy (Claude Code).
   - The disclosure that the certificates were made by other agents in earlier runs, with Bobby's earlier package reviews.

   Missing (credit gaps the gate should ask to fix):
   - No link or DOI for "Rosati et al. 2022".
   - No path or link for the "Team MODAL bound file in the RobinX repository".
   - The posted bounds being exceeded have no named contributors. From the history pages these are David Van Bulck; George H. G. Fonseca and Túlio A. M. Toffolo; and Team Udine.
   - RobinX and the board are not credited to David Van Bulck, Dries Goossens, Jeroen Belien and Morteza Davari. Only the board URL is given.
6. **Package consistency.** The frozen PREREG.md names data/object_list.csv (sha256 cee2b995…), but that file is not in claim/ and not in SHA256SUMS. A reader cannot check the frozen object list from the package. This is minor, since every object hash is in SHA256SUMS and the model hashes match rows.csv's package tags (5488583a, f6c04f12).
7. **Rule 12.** No personal paths, emails or hostnames in the claim text. The only "@" strings are the public organiser address on the board page and the "DITUoI@Arta" team name. "Boss" is a role label.
8. **Replay settings.** Disclosed accurately. REPRODUCE.md says the Early 14 and Early 9 logs used the default linearization level, and I confirmed that both settings give the same bound.

## Points for the gate

- **Literal criterion, first clause:** met for all five rows. Every instance is open, every bound is strictly above the board and history bounds, every model, log and seed is present, and my fresh single-worker replays give 4, 40, 60, 20 and 20 exactly.
- Early 14 and Early 9 rely on PROOF.md as well as their models: a case split for Early 14, lemma arithmetic for Early 9. This is disclosed. The REPRODUCE skeptic must accept those hand proofs. I checked them and found them sound.
- Rule 4 batching rests on an interpretation of the human's message. Confirm the authorisation from the human's own words before filing.
- Non-blocking wording fixes for the filing text: drop "and the BR1 rules"; soften the Early 9 "re-derives the bound" description; add the missing credits and links (item 5); include data/object_list.csv or drop the reference to it.
- None of these findings overstates the result, its scope, or its fit to the criterion. I therefore pass the criterion, conditional on the gate confirming item 4.

pass: true
