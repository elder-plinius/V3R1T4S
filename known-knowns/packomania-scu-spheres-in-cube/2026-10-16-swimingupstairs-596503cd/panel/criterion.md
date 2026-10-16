# CRITERION skeptic, round 3, N=806
context: subagent (fresh knowledgeWork context; read only the kit (RULES.md, POLICY.md, SUBMIT.md) and the claim_806/ folder; panel/ not read)
target: packomania-scu-spheres-in-cube (full criterion; not a partial win: author.txt row is "806 Lu Peng", so p1 does not apply)

## Object
claim_806/scu806_candidate.txt, 806 rows of 3 decimal coordinates, sha256 596503cd75b4f31d5d6dcb5d248e0cbb56f088acef07d045565e6e98b770e64d.

## Criterion clause by clause
1. **N listed in radius.txt**: yes, row 806 = 0.056998279608 (12 decimals in the live file, not 30 as the criterion text assumes; the 1e-11 margin is still meaningful because the gap is many orders larger). PROVED-HERE.
2. **Feasible radius, cube [-1/2,1/2]^3, 50 digits, no tolerance**: reran on a scratch copy (python3, `PYTHONDONTWRITEBYTECODE=1`, claim folder untouched):
   - `python3 exact.py scu806_candidate.txt 0.056998279608` -> `scu806_candidate.txt n=806 r*=0.05702080830646564701052 table=0.056998279608 diff=2.25287e-5 pass_1e-11=True` (exact Fraction squared distances, ALL pairs, no duplicates, 3 columns per row).
   - `python3 scu_check.py scu806_candidate.txt` -> BEATS_BY_1e-11=True, same r* to 30 digits (the binding constraint is the pair distance; the wall term is larger).
   - Definition check: exact.py implements r* = min(min_{i<j}|ci-cj|/2, 1/2 - max|coord|) exactly as in CRITERION_VERBATIM.md, for the centred unit cube (Packomania convention). PROVED-HERE.
3. **Margin >= 1e-11 over the live value re-fetched before claiming**: diff = 2.25287e-5 >> 1e-11; live radius.txt re-fetched by me (below) is byte-identical to the claim's copy. PROVED-HERE.
4. **Not isometric to posted scu806.txt**: the posted file has 805 centres, the candidate 806, so the sorted distance multisets differ in size (`different sizes 806 805` in check_output.txt; I counted the rows myself; isometry.py itself could not run here because scipy is absent, which does not matter for a size mismatch). PROVED-HERE.
5. **No newer History-of-updates line**: live scu.html is byte-identical to the scout's fetch (Last update 08-Oct-2026). N=806 does appear in the 08-Oct-2026 line ("... by Lu Peng"), but that line is the one the scout already saw, not a newer one, and the table value compared against already reflects it. PROVED-HERE.
6. **Queue rule**: live pending-requests.html (identical hash) lists no scu range; the only lines are Moki & Julio crt/ccq/crc (other categories) and "26-Sep-2026 Moki & Julio *many* 4666 candidates total", which is category-unspecified. CLAIM.md states this caveat honestly and says N=806 must be re-checked once that bundle leaves the list. Caveat required by the criterion: present.
7. **Moki & Julio dataset**: MJ_MANIFEST.csv scu row N=806 new_radius 0.05699827673690576549947939 < r*; no scu manifest row with N' >= 806 has published or new radius >= r* (checked myself). Only manifest radii were compared, as CLAIM.md says.
8. **Deletion / subsumption from larger N**: no N' > 806 in live radius.txt has r(N') >= r* (checked). r(N-1)=r(805) = 0.057020808305: r* equals r(805) to 1.5e-12; the entire radius is Lu Peng's.

## Live re-fetch at verification (one plain GET each, User-Agent "V3R1T4S-criterion-skeptic", no retries; no 401/403/429/503 met)
| URL | HTTP | UTC | sha256 / note |
|---|---|---|---|
| https://packomania.com/scu/txt/radius.txt | 200 | 2026-10-16T16:29:12Z | 832c9563391ccaffd571066d407dcd92c95661e6802e1da291e4d9f2e2fd1ed8 (identical to the scout's fetch and to claim radius.txt) |
| https://packomania.com/scu/scu.html | 200 | 2026-10-16T16:29:13Z | 344927b84a7214c58f20f508646a93c6885e3c3e635abce1357413ffe4a35900 (identical; "Last update: 08-Oct-2026") |
| https://packomania.com/pending-requests.html | 200 | 2026-10-16T16:29:14Z | 0d6ebbbe8e95abe7e701e1c70fbc1c0ec5bb06d611822b0b135ce3b776972384 (identical) |
| https://packomania.com/scu/txt/author.txt | 200 | 2026-10-16T16:29:15Z | fafdf2d15007d951b3f320dc5cf760b3efce98c9916ac630d437e97eb694ea75 (identical) |
| https://packomania.com/scu/txt/scu805.txt | 200 | 2026-10-16T16:29:17Z | 0d71de699efba494afbd759a7cb2837ef3a8ede38cf5b6582897ca0e1d45dbcc |
| https://packomania.com/scu/txt/scu806.txt | 200 | 2026-10-16T16:30:47Z | byte-identical to claim scu806.txt |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 200 | 2026-10-16T16:30:57Z | 51 open PRs listed |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 200 | 2026-10-16T16:30:57Z | no line matching scu / cube / sphere / packomania |

## Provenance and posted-file statements (verified against posted Packomania files fetched by me)
- Claim: "scu805.txt unchanged (all 805 centres within 1e-4) plus one sphere placed in a free hole". Measured: 805/805 scu805 centres within 1e-4 of a candidate centre; exactly 1 candidate centre is more than 1e-4 (indeed more than 1e-2) from every scu805 centre. **Accurate.**
- Claim: "r* equals Lu Peng's N=805 table radius 0.057020808305 to about 1.5e-12". Measured: r* - r_table(805) = 1.4656e-12 (float r* of posted scu805 itself is 0.0570208083043). **Accurate.**
- Claim: posted scu806.txt "lists 805 centres with a blank 806th row". Measured: 805 numeric rows plus an empty row "806". **Accurate.** (Float r* of those 805 centres is 0.0569982796075, the table value.)
- Claim: "only a handful coincide with scu805's to 1e-4". Measured: 8/805 (identity), at most 13 over the 48 cube symmetries. **Accurate.**

## Literature, trophies, open PRs
- LITERATURE_SEARCH.md names the recent work (Peng Lu, arXiv 2610.13978, N=203 only; Tatarevic 2015; Lai, Hao, Xiao, Glover 2023) and reports no published radius >= r*. I did not repeat the web literature search; I have no contrary evidence. NUMERICAL/KNOWN as reported, not re-verified.
- TROPHY_CASE.md (re-fetched): no cube entry. Confirmed.
- Open PRs #235-#238 (scu N=884, 883, 882, 886, created 2026-10-16T16:29Z, after LITERATURE_SEARCH.md was written) are not for N=806 or any N' >= 806 near it with r >= r*; #206/#207 are N=507/83. No competing PR. LITERATURE_SEARCH.md's 'only #206 and #207' sentence is now stale but was true when written.
- The search notes one injection_suspected leaderboard page, treated as data only. Appropriate.

## Prereg before measurement
PREREG.md frozen_utc 2026-10-16T08:50:58Z; candidate files and table fetches are later (table fetched 15:47:57Z). The statistic, 1e-11 threshold, live re-fetch, isometry, history, queue and Moki & Julio checks are all frozen there and the claim was judged by exactly those. The freeze time is self-reported (no commit hash in the folder), so it is taken on trust. No null model is needed for an explicit configuration checked by a deterministic radius rule (PREREG says so; I agree).

## Credit (rule 13)
Credits Eckard Specht / Packomania (scu.html link), Lu Peng for the extended scu805 packing (direct link to scu805.txt) and as live row author, Moki & Julio (Zenodo DOI 10.5281/zenodo.22986800, v2.7), and the literature authors with arXiv id / DOIs. The method credit is honest: the candidate is Lu Peng's posted scu805 packing unchanged plus one sphere in a free hole, with no relaxation gain. Minor: the table writes "Lu Peng", the arXiv paper "Peng Lu" (name order only). No missing credit found.

## Leak check
No term from the human's never-publish list occurs in any file of claim_806/ (case-insensitive fixed-string search). No email address, token pattern, username path or absolute path found (scu_check.py computes its own directory at runtime; no literal path). Page copies with the maintainer's email were correctly left out. Packaging note (not a panel failure): radius.txt, scu806.txt and MJ_MANIFEST.csv are full third-party data copies; SUBMIT.md section 1 forbids copying third-party pages/datasets into a package, so they must be replaced by URL + sha256 in the-record-we-beat/ when packaging, and MJ_MANIFEST.csv (575 KB, all shelves) should not ship.

## Subsumption judgement specific to N=806
The candidate adds nothing to Lu Peng's radius: it is his scu805 packing plus one sphere in an empty hole. PREREG.md's "table-consistency observation, not a claim" rule is written for deletion only ("sub-configuration of a posted Packomania file ... deletion only"); this is an insertion, i.e. a super-configuration, so the rule does not literally apply. No posted, published, queued or PR'd configuration for N=806 reaches r*; the existence of an 806th free hole in the 805 packing is not deducible from the table. I therefore judge it a genuine, non-subsumed improvement of the N=806 cell under the literal criterion, with credit correctly assigned (CLAIM.md says "The whole radius is Lu Peng's"). The gate may want to note that a stricter reading of the PREREG spirit (no optimisation gain) would make this a table-consistency observation instead.

## Verdict
The result meets the full success criterion literally, with the mandatory Moki & Julio queue caveat stated. All statements about the posted files that I checked are accurate.

confirmed_scope: The 806 centres in claim_806/scu806_candidate.txt (sha256 596503cd75b4f31d5d6dcb5d248e0cbb56f088acef07d045565e6e98b770e64d) lie in the cube [-1/2,1/2]^3 with feasible radius r* = 0.05702080830646564701 (exact rational squared distances over all pairs, sqrt at 50 dp), which exceeds the live Packomania scu radius.txt value for N=806 (0.056998279608, re-fetched 2026-10-16T16:29:12Z, unchanged) by 2.253e-5; the configuration is Lu Peng's posted scu805 packing unchanged plus one sphere in a free hole (r* equals Lu Peng's N=805 radius to 1.5e-12, so the radius is entirely his), and N=806 remains subject to the unresolved 26-Sep-2026 Moki & Julio pending bundle.

pass: true
