# CRITERION review: claim/ (three XHSTT-2014 solutions)
context: fresh subagent started for this claim only

Reviewer working files: panel/work-criterion/ (fetch/ holds my live re-fetch, fetch_log.txt the HTTP statuses, fetch_sha.txt the hashes, verify_run.txt the captured output of my runs). Nothing under claim/ was modified. I did not read other panel files, attempts/ or scans/.

## The criterion, verbatim (claim/target.md, "What counts as a win")

"An XHSTT solution file for one instance that is open (best > LB) on https://www.utwente.nl/en/eemcs/dmmp/hstt/archives/XHSTT-2014/overview.html, whose cost, computed by an independent evaluator written from the XHSTT specification that first reproduces the cost of the best solution stored in that instance's own XML file, is hierarchically strictly lower (smaller infeasibility value, or equal infeasibility and smaller objective) than the best value on both the overview and the instance's dataset page, re-fetched live immediately before claiming. A cross-check with Kingston's HSEval is done by the human, not the agent; nothing is submitted to the archive by the agent."

Bank entry check: I fetched the live bank entry (raw.githubusercontent.com, HTTP 200, 2026-11-28T09:07:31Z, sha256 5404776af40c157a416fb8ba4bf560745e81f9e2444f6d4d3d040fed834a34f1). It is byte-identical to claim/data/target_live.md; claim/target.md is that file preceded only by the line `id: xhstt-2014-high-school-timetabling-bks` and a blank line (diff shows nothing else). The criterion and partial wins in claim/target.md are therefore verbatim.

## Live re-fetch (mine)

One plain request each, curl with User-Agent `V3R1T4S-panel-check`, no retries, at 2026-11-28T09:07:31Z: overview, the three dataset pages, the three instance XML files, the bank entry. All eight returned HTTP 200 and are byte-identical (same sha256, cmp clean) to claim/data/overview.html, claim/data/pages/*.html, claim/data/inst/*.xml and claim/data/target_live.md. Nothing changed between the claim's fetch (08:57:12Z) and mine. An audit of claim/code/, claim/data/fetch.json and REPRODUCE.md found no browser User-Agent, cookie, challenge-bypass or retry logic.

Timeline from the files: fetch.json 2026-11-28T08:57:12Z; PREREG frozen 09:04:27Z (PREREG.md header; file mtime 11:04:27 +0200 agrees); claim/ built 09:05:04Z (mtimes 11:05:04 +0200); my re-fetch 09:07:31Z, unchanged. The claim has not been filed; PREREG commits to a re-fetch before filing and withdrawal of any row whose best dropped to or below ours. "Immediately before claiming" is met for the panel stage (7 minutes before freeze, confirmed unchanged 10 minutes later) and must be met again at filing.

## Overview: open status (parsed from claim/data/overview.html, identical to live)

Open rows on the overview now (best > LB): AU-BG-98 126/0.0, DK-FG-12 1020/412, DK-HG-12 12.2330/7.0, DK-VG-09 2.2323/2.0, NL-KP-03 102/0, NL-KP-05 399/89, NL-KP-09 665/180, UK-SP-06 2.802/0.0. That is 8 open instances (the bank's narrative list of 9 is stale: ES-SS-08 is now 335/335 and DK-FG-12's best is now 1020, dated October 28, 2026). CLAIM.md's "8 open XHSTT-2014 dataset pages" matches the live overview.

Notation: the overview writes a feasible cost as the objective alone and an infeasible one as infeasibility.objective. The dataset pages have separate "Feasibility value" and "Objective value" columns, which confirm the reading: AU-BG-98 page best 0 / 128; DK-HG-12 page best 12 / 2330; DK-VG-09 page best 2 / 2323 with Lowerbound (2,0). So 126 = (0, 126), 12.2330 = (12, 2330), 2.2323 = (2, 2323), LB 0.0 = (0, 0), 7.0 = (7, 0), 2.0 = (2, 0). The claim's (0, 91) is infeasibility 0, objective 91, compared against (0, 126): read correctly.

## Clause-by-clause check per row

Commands run from inside claim/ (output in panel/work-criterion/verify_run.txt): `python3 code/verify.py data/inst/{instance}.xml object/{file} {overview best} {page best}` and `python3 code/xhstt_eval.py data/inst/{instance}.xml`.

### AU-BG-98, object/AU-BG-98_0_91.xml
- XHSTT solution file for one instance: one Solution, Reference="AU-BG-98"; verify.py structure checks pass. Yes (see the solution-only note under defects).
- Open on the overview: best 126 = (0, 126) > LB 0.0 = (0, 0). Yes.
- Evaluator reproduces the best stored solution of the instance's own file: 8 stored solutions, best stored evaluates to (0, 128) = dataset-page best. All 8 stored values match the page's 8 values exactly (7.433, 3.400, 3.311, 2.340, 1.386, 1.363, 0.334, 0.128). Yes.
- Cost: (0, 91) (soft: AvoidSplitAssignments 70, LimitBusyTimes 10, SpreadEvents 11). PASS.
- Hierarchically strictly lower than both: (0, 91) vs overview (0, 126): equal infeasibility, 91 < 126; vs page (0, 128): 91 < 128. Yes, strict against both.
- Overview/page disagreement (126 vs 128) handled the strict way: verify.py requires strictly lower than both, so it beats the better of the two (126), as the bank's trap demands. The overview's 126 has no stored solution behind it (the file's best is 128, both dated by the GOAL Dec 2016 submission / April 17, 2017), so 126 cannot be reproduced; beating it anyway is the correct, conservative reading. Margin 35 objective points below the stricter bound.
- Verdict for row: meets the criterion.

### DK-HG-12, object/DK-HG-12_12_2326.xml
- One Solution, Reference="DK-HG-12"; structure checks pass. Yes.
- Open: (12, 2330) > LB (7, 0). Yes.
- Reproduces best stored: 6 stored, best (12, 2330) = page best; all 6 values match the page (25.33844, 12.3124, 12.3056, 12.2628, 12.2611, 12.2330). Yes.
- Cost: (12, 2326) (hard: AssignResource 5, AssignTime 6, AvoidClashes 1; soft 742 + 424 + 672 + 488). PASS.
- Strictly lower than both: overview and page both (12, 2330): equal infeasibility 12, 2326 < 2330. Yes. Margin 4 objective points.
- Verdict for row: meets the criterion.

### DK-VG-09, object/DK-VG-09_2_2322.xml
- One Solution, Reference="DK-VG-09"; structure checks pass. Yes.
- Open: (2, 2323) > LB (2, 0). Yes.
- Reproduces best stored: 6 stored, best (2, 2323) = page best; all 6 values match the page (2.18862, 2.4097, 2.2881, 2.2731, 2.2718, 2.2323). Yes.
- Cost: (2, 2322) (hard: AssignTime 2; soft 398 + 144 + 236 + 1544). PASS.
- Strictly lower than both: overview and page both (2, 2323): 2322 < 2323. Yes. Margin 1 objective point.
- Verdict for row: meets the criterion.

`sha256sum -c SHA256SUMS`: all 26 entries OK (exit 0); PREREG.sha256 matches PREREG.md; claim/PREREG.md and claim/target.md are identical to the run folder's copies; object hashes in rows.csv match the files and the run folder's data/object_list.csv (sha256 c5a119ed31a41ee1ce36b601090336830a5e5844fe6e16cb02f0f01a0f56abc1, as PREREG states). The evaluator raises on any unsupported constraint type, so no constraint present in these files is silently skipped (types present: AU-BG-98 13 types incl. LimitWorkload and AvoidSplitAssignments; the Danish files 8 types each).

## "Independent evaluator written from the XHSTT specification"

Reading: "independent" in this criterion means independent of HSEval and of the solver's own reporting (the agent cannot run HSEval; the human cross-checks with HSEval later), i.e. a fresh implementation from the published specification whose correctness is anchored by reproducing the archive's stored best. It does not literally require independence from the claimant's team or from the search.

The claim's code/xhstt_eval.py qualifies on the literal text: its docstring says it was written from the HSEval specification 2.15 (saved in data/spec/), it uses no HSEval code, and it reproduces each file's best stored solution (in fact all 20 stored values of these three files, and per code/validate_57.out.txt all 57 page values on the 8 open pages). It even matches the page (0, 334) where a stored solution's own Report says (0, 340), which shows it follows the archive's evaluation, not self-reports.

The coupling is real but is a disclosure, not a failure under the criterion: the search was run on this same evaluator (provenance/README.md), so a search could in principle exploit an interpretation error in a constraint feature not exercised by the stored solutions. The criterion's guard (reproducing the stored best) is met; the further guard is the REPRODUCE skeptic's own evaluator, written before reading code/, and the human's HSEval cross-check. My pass assumes REPRODUCE independently obtains (0, 91), (12, 2326) and (2, 2322); if it does not, my pass does not cover the mismatched row.

## Partial wins p1/p2 and margins

CLAIM.md claims the full criterion per row and explicitly does not claim p1/p2 "beyond what the full criterion implies". That is accurate and not overstated: AU-BG-98 (0, 91) also satisfies p1 (strictly better feasible solution for AU-BG-98); DK-HG-12 (12, 2326) satisfies p2 (equal infeasibility, lower objective); DK-VG-09 (2, 2322) satisfies p2 (infeasibility 2, objective below 2323). The partial wins are subsumed by the full wins, so the claim level is correctly the full criterion (solution claim per row), not a partial claim.

Margins: the criterion says "strictly lower" and requires no margin; 4 and 1 objective points qualify. But the thin margins matter for robustness: on the same archive, AU-BG-98's overview (126) and dataset page (128) disagree by 2 points for what appears to be the same Dec 2016 GOAL submission, i.e. evaluator or version differences of a few points are known to occur in this archive. DK-VG-09's 1-point and DK-HG-12's 4-point margins are of that size, so the human's HSEval cross-check is decisive for those two rows; AU-BG-98's 35-point margin is not sensitive to that.

## Batching

Kit rule, kit/RULES.md rule 4: "One object or table cell per claim." kit/RUN.md step 7 lists "several objects bundled as one claim" as a downgrade reason, and kit/SUBMIT.md says "one object or table cell per package". The claim bundles three objects (three table cells).

RULES.md also says "Only your human's own messages outrank them." claim/PREREG.md records the human's decision: the lead agent proposed "one batched claim of the three, same route as before: freeze, a three-reviewer panel, package, then filing on your yes" and Boss answered "do it. Use Opus 5.5 on High for the novelty revirwer, medium for the rest". I cannot see the chat; I take PREREG's record at face value. Given that explicit human decision, and because the claim is structured as three independent rows, each with its own object, hash, instance file, bests, verify.py run and per-row withdrawal rule (PREREG counting rule), I judge the batching acceptable for the panel stage: nothing is pooled, no row leans on another, and each row meets the criterion on its own. It does not need to be split for this review.

It is acceptable only on these conditions, which the gate must honour: (a) the gate records that batching departs from RULES 4 / RUN.md step 7 and is authorised by the human's quoted message (not by an agent); (b) status and confirmed scope are stated per row, so a later failure of one row (REPRODUCE mismatch, NOVELTY finding, HSEval disagreement, re-fetch at filing) drops that row only; (c) packaging follows SUBMIT.md "one object or table cell per package", so either three packages or an explicit human yes for a single three-row package, recorded in the gate.

## Wording and documentation defects

1. CLAIM.md title "3 XHSTT-2014 instances solved below their best known cost": uses "solved", which RULES 4 forbids unless the criterion literally says so (it does not), and "solved" can be read as closing the instances (none is closed: gaps to LB remain). Also "best known" is wider than the evidence, which is "best archived on the overview and dataset page" (the bank warns papers may report unarchived values; that is for NOVELTY). Fix wording, e.g. "3 XHSTT-2014 instances: solutions below the best archived cost". Does not change a number.
2. code/validate_57.py reads raw/pages/ and raw/inst/, and xhstt_eval.py's docstring says the spec is "saved in raw/spec/"; the claim folder has data/ instead, and only 3 of the 8 instances' files. So the 57-value validation cannot be rerun from claim/; only the 20 values of the three included files can (I reran them: all 20 match). CLAIM.md and PREREG present the 57 as evidence; it should say the 57-value run is recorded output, rerunnable only from the run folder. Does not change a number (the criterion needs only each file's own best, which is rerunnable).
3. code/validate_57.out.txt reports stored solutions not listed on their pages ("ours not on page"): NL-KP-03 (0, 527) and UK-SP-06 (386000, 136). Unexplained, outside these three rows; worth a note (the UK-SP-06 value suggests a stored solution the evaluator scores very differently from anything listed). Does not change a number for the claimed rows.
4. PREREG.md cites data/object_list.csv, which is not in claim/ (it is in the run folder; its hash matches PREREG and its object hashes match rows.csv). Documentation only. Does not change a number.
5. The object files are solution-only archives whose Solution references an instance not in the file. The specification describes a solution group as solutions "to the instances of its archive", so for an HSEval check the solution must be merged into the instance file; REPRODUCE.md should give that merge step for the human. Does not change a number.
6. The object files' MetaData has `Contributor` "V3R1T4S (OrenSleepwalker)", and xhstt_eval.py names a team agent ("Andy"); provenance names team agents. Check against RULES 12 and the human's never-publish list before packaging. Does not change a number.
7. kit/SUBMIT.md: no third-party datasets copied into a package, files at most 1 MB. claim/data/inst/*.xml (about 2.0 to 3.1 MB each, the archive's own files with others' solutions), data/pages/, data/overview.html and data/spec/ are third-party and must stay out of the package (reference by URL and sha256). Does not change a number.
8. Bank narrative in target.md is stale (lists ES-SS-08 335/334 and DK-FG-12 1263/412 as open bests); the claim correctly uses the live overview. Not a claim defect. Does not change a number.

No statement of optimality, lower bounds or method superiority is made: CLAIM.md's "Not claimed" excludes optimality and method claims; the remark that DK-VG-09's infeasibility 2 cannot be lowered is the archive's own LB (2,0), correctly attributed. rows.csv's method column is provenance and is labelled so in provenance/README.md ("not evidence"). The NUMERICAL label is appropriate.

## What the gate must disclose

- Batching departs from RULES 4 / RUN.md step 7; authorised by the human's message quoted in PREREG.md; status and scope per row; packaging one row per package unless the human explicitly says yes to one package.
- The evaluator is the claimant team's own, written from the HSEval specification 2.15 and validated on the archive's stored values; the search used it. The independent re-evaluation is the REPRODUCE skeptic's evaluator; no HSEval cross-check was done (the human does that).
- Margins: AU-BG-98 35 points below the stricter (overview) best; DK-HG-12 4 points; DK-VG-09 1 point. The overview/page disagreement on AU-BG-98 (126 vs 128) shows few-point evaluator differences occur in this archive, so the HSEval cross-check is decisive for the two Danish rows.
- AU-BG-98 is compared against the overview's 126, which no stored solution reproduces; the claim beats both 126 and 128.
- Re-fetch before filing (the live tables were unchanged at 2026-11-28T09:07:31Z); a row whose best drops to or below ours is withdrawn.
- Fix the title wording ("solved", "best known") before anything is packaged; note that the 57-value validation is recorded output rerunnable only from the run folder; give the human a merge step for HSEval; keep third-party files and personal handles out of the package.

## confirmed_scope

confirmed_scope: Each of object/AU-BG-98_0_91.xml, object/DK-HG-12_12_2326.xml and object/DK-VG-09_2_2322.xml, evaluated on its instance's XHSTT-2014 file from the dataset page by the claim's evaluator written from the HSEval specification (which reproduces every stored solution value of these three files), has cost (0, 91), (12, 2326) and (2, 2322) respectively, hierarchically strictly lower than the best on both the XHSTT-2014 overview and that instance's dataset page ((0, 126) and (0, 128); (12, 2330); (2, 2323)) as fetched 2026-11-28T08:57:12Z and re-fetched unchanged 2026-11-28T09:07:31Z, with no HSEval cross-check.

## Verdict

Each of the three rows separately meets the full success criterion as literally written: open on the live overview, evaluator from the specification reproducing the file's best stored solution, cost hierarchically strictly lower than both the overview and dataset-page bests, live tables re-fetched and unchanged. AU-BG-98's 126/128 disagreement is handled the strict way. Batching is acceptable only under the recorded human decision, with per-row scope and the disclosures above. The wording defects (notably "solved" in the title) must be fixed but do not change any number or the criterion result. This pass is conditional on REPRODUCE independently obtaining the three costs; a row it cannot reproduce drops out of my confirmed scope.

pass: true
