# Novelty review: IHTP i08, claimed cost 6225

context: subagent (Claude Code Agent tool, fresh context)
role: NOVELTY skeptic (panel of three)
target_id: ihtp-ihtc2024-upper-bounds, cell i08 (public set i01-i30)

## 1. Live status fetch (one plain fetch, no retries)
- Command: `curl -sS -A 'V3R1T4S-research-agent (+https://github.com/elder-plinius/V3R1T4S)' -w '%{http_code}' https://ihtc2024.github.io/ihtp/index.html`
- URL: https://ihtc2024.github.io/ihtp/index.html
- Fetch time (date -u): 2026-10-31T00:20:56Z (finished 00:20:57Z)
- HTTP status: 200 (not blocked)
- i08 listed value: **6243** (row `i08 | 6243 | sol_i08.json`)
- Page sha256 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363, identical to the scout's saved claim/ihtp_table.html.
- Organiser repo ihtc2024/ihtc2024.github.io: last table update commit "updated batch of UB" 2026-10-23T10:07Z; the live page still lists 6243 for i08.

## 2. Sources checked for an i08 cost <= 6225
| Source | i08 value found | Beats or ties 6225? |
|---|---|---|
| Organisers' UB table (live, above) | 6243 | no |
| Organisers' published sol_i08.json (https://ihtc2024.github.io/assets/files/solutions/public/IHTP/sol_i08.json, HTTP 200), rescored with official validator | 6243, 0 violations | no |
| elder-plinius/V3R1T4S pull requests, all states (`gh pr list --state all --limit 2000`: 828 PRs; `gh search prs` "IHTP", "i08") | 14 IHTP PRs (i19, i23, i26, i27, m09, m21, m24, m26-m30); none for i08; no i08 mention in their bodies or files | no |
| V3R1T4S TROPHY_CASE.md | no IHTP/IHTC/i08 entry | no |
| V3R1T4S known-knowns/ (26 entries) | no IHTP entry; known-unknowns/optimization-benchmarks/ihtp-ihtc2024-upper-bounds.md gives no i08 value below 6243 | no |
| Guericke, van der Hulst, Karimpour, Schrader, Walter, arXiv 2511.04685 v2 (1 May 2026; ORDAL vol. 46, 200502), HTML tables | i08 lower bound 4733; best-known at writing 6291; their runs 6414 / 6340 / 6310 | no |
| Kletzander 2026, ORDAL vol. 47, 200512 (TU Wien repositum record) | abstract only; no per-instance i08 value accessible | not found |
| Gioia, Mazza, Macis, Fadda, Brandimarte 2026, ORDAL vol. 47, 200514 (iris.polito.it PDF) | PDF returned HTTP 403; not read | not found |
| Othman and Chiarandini (ORDAL, IHTC 2nd place); Ceschia et al. competition overview; Garcia Tercero et al. COR 2026 | no i08 value surfaced in searches | not found |
| ihtc2024/ihtc2024.github.io PRs and issues | 1 closed PR (i27, m26); no i08 | no |
| GitHub competitor repos: Arthod/ihtc2024-imada-submission solutions/sol_i08.json (rescored) | 6363, 0 violations | no |
| emfrea/ihtc2024-evolved-solvers-main results/public/ihtc_per_instance_final.csv | best i08 6754 | no |
| AntonioPalma95/ihtc2024-heuristic-scheduler i08_sol.json (rescored) | 16700 | no |
| davidvanbulck/IHTC2024_Multi_Neighborhood_Hybrid, discopt/ihtc-twente, carlocoletta, Rvittimberga | no i08 solutions or results files | no |
| GitHub releases of the above repos | none listed | no |

Smallest i08 value found anywhere: 6243 (the organisers' table). 6225 < 6243 strictly (-18).

## 3. Seed comparison (claim/published_sol_i08.json vs claim/sol_i08.json)
- The seed is byte-identical to the organisers' live sol_i08.json (sha256 4fbbf647...8c971), and the claim names it.
- Both rescored here with the claim's IHTP_Validator.cc (checksums in SHA256SUMS verified): seed 6243, claim 6225, both 0 violations.
- Structural diff: 174 patients; scheduled 172 -> 173 (p166 newly admitted on day 14); 3 admission-day changes (p124 14->11, p139 11->14, p166); 96 room changes; 36 operating-theatre changes; 509 of 593 nurse (day, shift) room sets changed.
- Cost breakdown seed -> claim: ElectiveUnscheduled 400 -> 200; ContinuityOfCare 1152 -> 1144; RoomAgeMix 105 -> 115; ExcessiveNurseWorkload 616 -> 646; SurgeonTransfer 70 -> 90; PatientDelay 2300 -> 2430; OpenOT 1600 -> 1600.
- Assessment: the gain comes from inserting an elective patient (-200) and repairing the knock-on effects (+182 across other terms). Deletion or restriction can only remove patients, and relabelling or symmetry leaves the cost unchanged, so none of these edits can produce this. It is a coordinated combinatorial re-optimisation, not a local numerical polish (the problem is discrete). The change is more than a trivial edit, and it beats what those edits alone give (6243).

## Caveats
- The full texts of Kletzander (2026), Gioia et al. (2026; HTTP 403), Othman and Chiarandini, and Garcia Tercero et al. were not read, so per-instance tables in those papers are unchecked. The organisers' table, updated 2026-10-23, is the maintained aggregate and lists 6243.
- Novelty only. Feasibility and cost were rescored here only to compare objects; that is not the validity panel's job.

## Verdict
6225 is strictly below every i08 value found (minimum 6243). The object is seeded from the named published solution and changes it non-trivially. novelty: PASS.

pass: true
