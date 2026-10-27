# Novelty Skeptic Report — `ihtp-ihtc2024-upper-bounds` (`i26` Cost `63978`)

context: subagent (fresh invocation)

Role: NOVELTY skeptic.
Question under test: Does the feasible schedule in `object/sol_i26_63978.json` (`Total violations = 0`, `Total cost = 63978`) strictly beat every known upper bound for the IHTC-2024 instance `i26` across the official live status page, the 2024-2026 literature, `TROPHY_CASE.md`, and open pull requests? A tie is not a record.

## 1. Single Honest Fetch of Primary Tables and Status Pages

Each primary table and repository endpoint was fetched once (HTTP 200, no retries):

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 | Extracted Value for `i26` |
|---|---|---|---:|---|---|
| Official IHTC-2024 status page | `https://ihtc2024.github.io/ihtp/index.html` | `2026-10-27T19:43:31Z` | `200` | `2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363` | Row `i26`: BKS = **`64334`** (`sol_i26.json`). |
| V3R1T4S `TROPHY_CASE.md` | `TROPHY_CASE.md` | `2026-10-27T19:43:31Z` | local | `repo/TROPHY_CASE.md` | Inspection confirms zero existing entries in `TROPHY_CASE.md` for target `ihtp-ihtc2024-upper-bounds`. |
| Open pull requests | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls` | `2026-10-27T19:43:31Z` | `200` | live API | Zero open pull requests touch target `ihtp-ihtc2024-upper-bounds` or instance `i26`. |

## 2. Literature Audit (Last 24 Months, 2024–2026)
- **Ceschia et al. (2024–2026), Official IHTC-2024 Repository (`https://ihtc2024.github.io/ihtp/index.html`)**: The authoritative live Best Known Solution for `i26` is `64334` (baseline `64352`).
- **Sylejmani et al. (2026), arXiv:2610.00044**: Reoptimization baselines are already reflected on the live page; no published or preprint result reports a feasible objective for `i26` below `63978`.

## 3. Exact Novelty Comparison
- **Official live BKS (`https://ihtc2024.github.io/ihtp/index.html`)**: `64334`
- **Hunt baseline**: `64352`
- **Candidate (`object/sol_i26_63978.json`)**: **`63978`** (`Total violations = 0`; `RoomAgeMix 167, RoomSkillLevel 1136, ContinuityOfCare 9815, ExcessiveNurseWorkload 20, OpenOperatingTheater 880, SurgeonTransfer 90, PatientDelay 19370, ElectiveUnscheduledPatients 32500`).
- **Strict improvement**: Margin `-356` vs live BKS `64334`, and `-374` vs hunt baseline `64352`.

pass: true
