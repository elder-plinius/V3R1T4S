# NOVELTY skeptic: IHTC-2024 m08, claimed cost 14877

context: subagent (Claude Code Agent tool, fresh context)
Inputs read: only the claim folder (CLAIM.md, sol_m08.json, published_sol_m08.json, m08.json, IHTP_Validator.cc, json.hpp, ihtp_table.html).

## 1. Primary status page (one plain fetch, no retries)
- URL: https://ihtc2024.github.io/ihtp/index.html
- Command: `curl -sS -A 'V3R1T4S-research-agent (+https://github.com/elder-plinius/V3R1T4S)' -w '%{http_code}'`
- Fetch time (date -u): 2026-10-31T09:45:18Z (finished 09:45:19Z)
- HTTP status: 200
- sha256 of the body: 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363. It matches the scout's saved claim/ihtp_table.html byte for byte.
- m08 listed value: **14976**, linked to /assets/files/solutions/hidden/IHTP/sol_m08.json.

## 2. Sources checked for an m08 cost at or below 14877

Every solution file below was rescored with the claim's IHTP_Validator.cc (sha256 0b56fa75…a8afa, matching the organisers' file) against claim/m08.json.

| Source | m08 value | At or below 14877? |
|---|---|---|
| Organisers' live table (above) | 14976 | no |
| Organisers' repo ihtc2024/ihtc2024.github.io: solutions/hidden/IHTP/sol_m08.json and solutions/hidden/sol_m08.json, rescored | 14976 / 14976 (0 viol.) | no |
| Organisers' repo PRs (all states): #2 (i27, m26 only), #1 (dependency bump) | none for m08 | no |
| elder-plinius/V3R1T4S PRs, all 834 (open and closed; `gh pr list --state all --limit 2000`). 14 are IHTP-related: #358, #359, #416, #431, #786-#790, #794-#798. I read the full diffs (README, INDEX.csv, panel files, solution files) | no m08 value anywhere. The PR #358 README lists m01, m09, m11, m14, m21, m23, m24, m26-m30 and i-instances; m08 is not among them | no |
| `gh search prs` in the repo for m08, 14976, 14877, sol_m08, IHTC | only the 14 IHTP PRs above | no |
| V3R1T4S TROPHY_CASE.md (default branch) | no IHTP entries | no |
| V3R1T4S known-knowns/ (default branch) | no IHTP directory. IHTP appears only in known-unknowns/optimization-benchmarks | no |
| arXiv 2511.04685v2 (Guericke et al., hybrid approach), Table 5, fetched 2026-10-31 (HTTP 200) | m08: LB 13070, BKS 14976, own results 15838 (10 min) and 15064 (1 h). Other tables: 15838 and 15906 | no |
| arXiv 2610.00044 (Requeijo, 2026-09, nurse-layer exact reoptimisation of published solutions) | improves only i02, i05, m01, m03 and m04. No m08 value | no |
| ORDAL special issue on IHTP (2026): Gioia et al., "Healthcare Predictive Timetabling" (DOI 10.1016/j.ordal.2026.200514); code at DanieleGioia/HealthcarePredictiveTimetabling, results/sol_m08.json rescored | 15538 (0 viol.) | no |
| ORDAL: Kletzander (2026), parallel CP + SA, Article 200512 | no open full text found (TU Wien repository page has no PDF) | not found |
| Polito IRIS PDF of the Gioia et al. paper | HTTP 403. I did not retry; the repo results above stand in for it | n/a |
| KCL workshop paper (IHTP modelling case study) | no m08 value | no |
| Ceschia, Schaerf et al. (organisers): the BKS table and solution files above | 14976 | no |
| GitHub repos (28 scanned: trees and release assets). Searches: "ihtc2024", "IHTC 2024", "healthcare timetabling" | | |
| - emfrea/ihtc2024-evolved-solvers-main: 20 m08 solutions (gurobi-fix-opt, memetic) | best 15646 | no |
| - ahmedelhefnawy21/ihtp-matheuristic…: 5 seeds, plus a copy of the reference solution | best 15348 (reference copy 14976) | no |
| - cristianbelfiore/ihtc: m08 HTML plots | only 14976 appears | no |
| - the other 24 repos | no m08 solution files and no release assets | no |

Lowest m08 value found anywhere: **14976**. The claim's 14877 is 99 below it. Nothing found ties it or beats it.

## 3. Seed comparison (published_sol_m08.json, 14976, versus sol_m08.json, 14877)
The claim names its seed: the organisers' published m08 solution.

Validator breakdown, published → claim:

| Cost term | Published | Claim |
|---|---|---|
| RoomAgeMix | 11 | 117 |
| RoomSkillLevel | 435 | 445 |
| ContinuityOfCare | 4400 | 4195 |
| ExcessiveNurseWorkload | 20 | 0 |
| OpenOperatingTheater | 490 | 500 |
| SurgeonTransfer | 30 | 30 |
| PatientDelay | 1340 | 1340 |
| ElectiveUnscheduled | 8250 | 8250 |

Both have 0 violations.

The admission layer is untouched:
- 0 admission days changed.
- The same 33 patients are left unscheduled.
- PatientDelay and ElectiveUnscheduled are identical.

The lower layers changed a lot:
- 119 of the 167 admitted patients changed room. This is not a relabelling: none of the 13 rooms maps consistently onto a single new room, and RoomAgeMix moved by +106.
- 94 patients changed operating theatre. 40 of the 49 (day, OT) groups map consistently, so this part is mostly a cost-neutral relabelling.
- The nurse layer was largely rebuilt: 823 of 993 nurse/day/shift/room tuples were removed and 913 were added.

So the gain is not a deletion, restriction, relabelling or symmetry. It is not a few-move polish either: it trades +126 in room and OT terms for -225 in continuity and workload.

The closest trivial-edit baseline is the published-solution nurse-layer reoptimisation in arXiv 2610.00044, and it found no m08 improvement. This change also re-optimises rooms, which that baseline holds fixed.

Caveat: this is still a local-search improvement (SA, 150 s + 300 s) from the published seed, with the admission plan held as it was. The margin is small: -99, or -0.66%.

## Verdict
14877 is strictly below every m08 value I found: table 14976, organiser files 14976, V3R1T4S PRs none, Guericke et al. 15064, Gioia et al. 15538, competitor repos at least 15348. The change from the named seed is a substantial room and nurse re-optimisation, not a trivial edit or a symmetry.

pass: true
