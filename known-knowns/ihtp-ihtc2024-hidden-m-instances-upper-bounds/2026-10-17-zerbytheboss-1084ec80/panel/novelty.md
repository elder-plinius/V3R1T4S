# Internal Verification Notes — Novelty (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` / `m26` Cost `68496`)

- Context: contributor internal verification notes

Question under test: Does the feasible schedule in `object/sol_m26_68496.json` (`Total violations = 0`, `Total cost = 68496`) strictly beat every known upper bound for the IHTC-2024 competition (`m`) instance `m26` across the official live status page and the literature?

## 1. Fetch of Primary Tables and Status Pages

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 | Extracted Value for `m26` |
|---|---|---|---:|---|---|
| Official IHTC-2024 IHTP status page | `https://ihtc2024.github.io/ihtp/index.html` | `2026-11-07T05:10:33Z` | `200` | `351d0dcb75edfe3d9c250ed6af1abcd71d9e14a947ae076df783972d283b39de` | Hidden (`m`) table row `m26`: Best Known Solution (BKS) = **`69715`** (`sol_m26.json`). |

## 2. Literature Audit (2024–2026)

- **Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf, and Eugenia Zanazzo (University of Udine), and Pieter Smet and Greet Vanden Berghe (KU Leuven), Official IHTC-2024 Repository (`https://ihtc2024.github.io/ihtp/index.html`)**: Continuously maintained Best Known Solution (BKS) table for all 30 hidden competition instances `m01`–`m30`. The live BKS for `m26` is **`69715`** (`sol_m26.json`).
- **Alfonso Gippini Requeijo (2026), `arXiv:2610.00044`** (*"Improved upper bounds for five IHTC-2024 benchmark instances via exact reoptimization of the nurse-to-room layer"*): Reports improved bounds for `i02`, `i05`, `m01`, `m03`, and `m04` only, and does not touch `m26`.

## 3. Exact Novelty Comparison

- **Official live BKS (`https://ihtc2024.github.io/ihtp/index.html`, `sol_m26.json`)**: `69715`
- **Candidate (`object/sol_m26_68496.json`)**: **`68496`** (`Total violations = 0` across all 9 hard constraint categories; soft costs: `RoomAgeMix = 72`, `RoomSkillLevel = 2470`, `ContinuityOfCare = 2974`, `ExcessiveNurseWorkload = 130`, `OpenOperatingTheater = 2580`, `SurgeonTransfer = 200`, `PatientDelay = 12370`, `ElectiveUnscheduledPatients = 47700`).
- **Strict improvement over live BKS**: `68496 vs 69715` (**`-1219`** objective points, a `-1.75%` reduction).

pass: true
