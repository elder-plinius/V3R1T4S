# Novelty check: IHTC-2024 i18, claimed cost 37625

context: subagent (Claude Code Agent tool, fresh context)
role: NOVELTY skeptic (saw only claim/, plus public web/GitHub sources listed below)

## 1. Live status fetch (one plain fetch, no retries)
- Command: `curl -sS -A 'V3R1T4S-research-agent (+https://github.com/elder-plinius/V3R1T4S)' -w '%{http_code}' https://ihtc2024.github.io/ihtp/index.html`
- URL: https://ihtc2024.github.io/ihtp/index.html
- Fetch time (date -u): 2026-10-31T00:20:55Z (completed 00:20:56Z)
- HTTP status: 200 (not blocked)
- Listed i18 value: **37650** (row: `i18 | 37650 | sol_i18.json`)
- sha256 of fetched page: 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363, identical to the scout's claim/ihtp_table.html.
- Organisers' repo history (ihtc2024/ihtc2024.github.io): i18 changed 37660 -> 37650 in commit c078cf57 "updated batch of UB" (2026-10-23T10:07:15Z); latest commit 04f7bff9 (2026-10-23, .gitignore). No releases. Repo PRs: #2 (i27/m26, closed) and #1 (dependabot); none on i18.

## 2. Sources checked for an i18 cost <= 37625
| Source | i18 value found | <= 37625? |
|---|---|---|
| Organisers' UB table (live, above) | 37650 | no |
| Organisers' published sol_i18.json (same sha256 as claim/published_sol_i18.json), re-scored with the claim's IHTP_Validator.cc | 37650, 0 violations | no |
| arXiv 2511.04685v2, Guericke et al. (Team Twente; ORDAL vol. 46, 200502), Table 5/6 | LB 37246; best known cited 37660; own runs 37682 (10 min), 37632 (1 h), 37684 | no (best 37632 > 37625) |
| Kletzander 2026, ORDAL vol. 47, 200512 (repositum page + gitlab.tuwien.ac.at/lucas.kletzander/ihtc_rust tree) | no per-instance i18 value published; repo has no result/solution files | no value |
| Gioia et al. 2026, ORDAL vol. 47, 200514 (iris.polito.it PDF) | not read: HTTP 403 | unchecked |
| Garcia Tercero et al. 2026, Comput. Oper. Res. 107453 (repo davidvanbulck/IHTC2024_Multi_Neighborhood_Hybrid) | paper behind Elsevier redirect, not read; repo has no i18 solution/result file | unchecked (paper) |
| Organisers' competition overview / Udine papers (air.uniud.it handles 11390/1322324, 11390/1333207) | not read: HTTP 403 | unchecked |
| Othman/Chiarandini multi-neighbourhood lexicographic LS (ORDAL) | not located in open full text | unchecked |
| GitHub Arthod/ihtc2024-imada-submission (SDU-IMADA) solutions/sol_i18.json, validated | 39094 | no |
| GitHub pchtsp/ihtc2024 results/submissions (csv + sol, validated) | 40635 | no |
| GitHub emfrea/ihtc2024-evolved-solvers-main results/public/ihtc_per_instance_final.csv | best 37838 (gurobi-fix-opt) | no |
| GitHub ahmedelhefnawy21/ihtp-matheuristic... best_known csv + reference sol (validated) | 37660 | no |
| GitHub AntonioPalma95/ihtc2024-heuristic-scheduler (3 sols, validated) | 51384-52418 | no |
| Other IHTC repos (discopt/ihtc-twente, carlocoletta, Rvittimberga, angelaluiss, Mattmandav, etc.) | no i18 result found | no value |
| elder-plinius/V3R1T4S PRs, all states (828 listed via `gh pr list --state all --limit 2000`; `gh search prs` for "i18" and "IHTP") | 14 IHTP PRs (i19, i23, i26, i27, m09, m21, m24, m26-m30); bodies/files grepped: none mention i18 | no |
| V3R1T4S TROPHY_CASE.md | no IHTP/i18 entry | no |
| V3R1T4S known-knowns/ tree | no IHTP/IHTC directory | no |

All validations used the claim's IHTP_Validator.cc (sha256 0b56fa75...) built with g++ -O2 -std=c++17 against claim/i18.json; it reproduces the listed 37650 for the published solution and gives 37625 / 0 violations for claim/sol_i18.json.

## 3. Seeded-object comparison (claim/sol_i18.json vs claim/published_sol_i18.json)
- The seed is named in CLAIM.md (organisers' published sol_i18.json, 37650).
- Same 257 patients, same 146 admitted, admission days unchanged for every patient.
- Changed: 141 of 257 patient records differ (116 room changes, 114 operating-theatre changes); 989 of 1173 (day, shift, room) nurse slots have a different nurse.
- Not a relabelling/symmetry: the room mapping is not a permutation (all 19 rooms map to more than one room) and the nurse mapping is not a permutation (40 of 41 nurses map to more than one nurse). Not a deletion or restriction (same admitted set). It is a combinatorial re-optimisation of room, theatre and nurse assignments by simulated annealing, not a trivial edit or a numerical polish. Trivial edits of the published object leave the cost at 37650 or worse; the claim beats that by 25.

## Verdict
37625 is strictly below every i18 value found: the live table (37650), the published solution (37650), the best paper value seen (Guericke et al. 1 h run, 37632) and every competitor repository checked (best 37838). The object is not a trivial edit of its named seed.
Residual risk: Gioia et al. (403), the Udine overview papers (403), Garcia Tercero et al. (paywall) and the Othman/Chiarandini paper were not read in full. The organisers' table was refreshed with a batch of upper bounds on 2026-10-23 and still lists 37650.

pass: true
