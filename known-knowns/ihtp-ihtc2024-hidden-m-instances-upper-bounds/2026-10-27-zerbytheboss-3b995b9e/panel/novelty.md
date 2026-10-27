# Novelty Skeptic Report — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m28` Cost `45037`)

context: subagent (fresh invocation)

Role: NOVELTY skeptic.
Question under test: Does the feasible schedule in `object/sol_m28_45037.json` (`Total violations = 0`, `Total cost = 45037`) strictly beat every known upper bound for the IHTC-2024 instance `m28` across the official live status page, the 2024-2026 literature, `TROPHY_CASE.md`, and open pull requests? A tie is not a record.

## 1. Single Honest Fetch of Primary Tables and Status Pages

Each primary table and repository endpoint was fetched once (HTTP 200, no retries):

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 | Extracted Value for `m28` |
|---|---|---|---:|---|---|
| Official IHTC-2024 status page | `https://ihtc2024.github.io/ihtp/index.html` | `2026-10-27T19:43:31Z` | `200` | `2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363` | Row `m28`: BKS = **`45873`** (`sol_m28.json`). |
| V3R1T4S `TROPHY_CASE.md` | `TROPHY_CASE.md` | `2026-10-27T19:43:31Z` | local | `repo/TROPHY_CASE.md` | Inspection confirms zero existing entries in `TROPHY_CASE.md` for target `ihtp-ihtc2024-hidden-m-instances-upper-bounds`. |
| Open pull requests | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls` | `2026-10-27T19:43:31Z` | `200` | live API | Unmerged open PR #431 (`claim/2026-10-18-mizopl-d54f4151`) touches `m28` with cost `45,873`. Our candidate solution `45037` strictly beats PR #431 by `-836` points. |

## 2. Literature Audit (Last 24 Months, 2024–2026)
- **Ceschia et al. (2024–2026), Official IHTC-2024 Repository (`https://ihtc2024.github.io/ihtp/index.html`)**: The authoritative live Best Known Solution for `m28` is `45873` (baseline `45913`).
- **Sylejmani et al. (2026), arXiv:2610.00044**: Reoptimization baselines are already reflected on the live page; no published or preprint result reports a feasible objective for `m28` below `45037`.

## 3. Exact Novelty Comparison
- **Official live BKS (`https://ihtc2024.github.io/ihtp/index.html`)**: `45873`
- **Hunt baseline**: `45913`
- **Open unmerged PR #431**: `45873` (strictly beaten by -836 points)
- **Candidate (`object/sol_m28_45037.json`)**: **`45037`** (`Total violations = 0`; `RoomAgeMix 52, RoomSkillLevel 1345, ContinuityOfCare 13495, ExcessiveNurseWorkload 165, OpenOperatingTheater 4880, SurgeonTransfer 410, PatientDelay 16290, ElectiveUnscheduledPatients 8400`).
- **Strict improvement**: Margin `-836` vs live BKS `45873`, and `-876` vs hunt baseline `45913`.

pass: true
