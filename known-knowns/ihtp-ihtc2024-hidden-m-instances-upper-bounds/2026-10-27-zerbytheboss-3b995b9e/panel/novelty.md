# Novelty Skeptic Report — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m28` Cost `45037`)

- Context: Live table and literature audit for IHTC-2024 instance `m28`

Question under test: Does the feasible schedule in `object/sol_m28_45037.json` (`Total violations = 0`, `Total cost = 45037`) strictly beat every known upper bound for the IHTC-2024 instance `m28` across the official live status page and the 2024–2026 literature? A tie is not a record.

## 1. Primary Table Status

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 | Extracted Value for `m28` |
|---|---|---|---:|---|---|
| Official IHTC-2024 status page (initial) | `https://ihtc2024.github.io/ihtp/index.html` | `2026-10-27T19:43:31Z` | `200` | `2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363` | Row `m28`: BKS = **`45873`** (`sol_m28.json`). |
| Official IHTC-2024 status page (re-verified) | `https://ihtc2024.github.io/ihtp/index.html` | `2026-11-07T05:10:33Z` | `200` | `351d0dcb75edfe3d9c250ed6af1abcd71d9e14a947ae076df783972d283b39de` | Row `m28`: BKS = **`45873`** (`sol_m28.json`). |

## 2. Literature Audit (2024–2026)
- **Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf, and Eugenia Zanazzo (Udine) with Pieter Smet and Greet Vanden Berghe (KU Leuven), Official IHTC-2024 Repository (`https://ihtc2024.github.io/ihtp/index.html`)**: The live Best Known Solution for `m28` is `45873` (`sol_m28.json`).
- **Alfonso Gippini Requeijo (2026), `arXiv:2610.00044`** (*"Improved upper bounds for five IHTC-2024 benchmark instances via exact reoptimization of the nurse-to-room layer"*): Improves upper bounds for five instances (`i02`, `i05`, `m01`, `m03`, and `m04`) and does not report any bound for `m28`.

## 3. Exact Novelty Comparison
- **Official live BKS (`https://ihtc2024.github.io/ihtp/index.html`, `sol_m28.json`)**: `45873`
- **Candidate (`object/sol_m28_45037.json`)**: **`45037`** (`Total violations = 0`; `RoomAgeMix 52, RoomSkillLevel 1345, ContinuityOfCare 13495, ExcessiveNurseWorkload 165, OpenOperatingTheater 4880, SurgeonTransfer 410, PatientDelay 16290, ElectiveUnscheduledPatients 8400`).
- **Strict improvement**: Margin `-836` (`-1.8224%`) vs live BKS `45873`.

pass: true
