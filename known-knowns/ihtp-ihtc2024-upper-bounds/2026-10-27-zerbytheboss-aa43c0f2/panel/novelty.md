# Novelty Skeptic Report — `ihtp-ihtc2024-upper-bounds` (`i19` Cost `43365`)

context: subagent (fresh invocation)

Role: NOVELTY skeptic.
Question under test: Does the feasible schedule in `object/sol_i19_43365.json` (`Total violations = 0`, `Total cost = 43365`) strictly beat every known upper bound for the IHTC-2024 instance `i19` across the official live status page, the 2024-2026 literature, `TROPHY_CASE.md`, and open pull requests? A tie is not a record.

## 1. Single Honest Fetch of Primary Tables and Status Pages

Each primary table and repository endpoint was fetched once (HTTP 200, no retries):

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 | Extracted Value for `i19` |
|---|---|---|---:|---|---|
| Official IHTC-2024 status page | `https://ihtc2024.github.io/ihtp/index.html` | `2026-10-27T19:43:31Z` | `200` | `2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363` | Row `i19`: BKS = **`43852`** (`sol_i19.json`). |
| V3R1T4S `TROPHY_CASE.md` | `TROPHY_CASE.md` | `2026-10-27T19:43:31Z` | local | `repo/TROPHY_CASE.md` | Inspection confirms zero existing entries in `TROPHY_CASE.md` for target `ihtp-ihtc2024-upper-bounds`. |
| Open pull requests | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls` | `2026-10-27T19:43:31Z` | `200` | live API | Zero open pull requests touch target `ihtp-ihtc2024-upper-bounds` or instance `i19`. |

## 2. Literature Audit (Last 24 Months, 2024–2026)
- **Ceschia et al. (2024–2026), Official IHTC-2024 Repository (`https://ihtc2024.github.io/ihtp/index.html`)**: The authoritative live Best Known Solution for `i19` is `43852` (baseline `43857`).
- **Sylejmani et al. (2026), arXiv:2610.00044**: Reoptimization baselines are already reflected on the live page; no published or preprint result reports a feasible objective for `i19` below `43365`.

## 3. Exact Novelty Comparison
- **Official live BKS (`https://ihtc2024.github.io/ihtp/index.html`)**: `43852`
- **Hunt baseline**: `43857`
- **Candidate (`object/sol_i19_43365.json`)**: **`43365`** (`Total violations = 0`; `RoomAgeMix 135, RoomSkillLevel 730, ContinuityOfCare 7225, ExcessiveNurseWorkload 590, OpenOperatingTheater 1920, SurgeonTransfer 120, PatientDelay 7395, ElectiveUnscheduledPatients 25250`).
- **Strict improvement**: Margin `-487` vs live BKS `43852`, and `-492` vs hunt baseline `43857`.

pass: true
