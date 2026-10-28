# Panelist Report: CRITERION

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: ihtp-ihtc2024-upper-bounds
confirmed_scope: An explicit feasible IHTC-2024 solution claim/sol_i27.json (209,120 bytes, sha256 900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7) for benchmark instance i27 (claim/i27.json, sha256 a4c3d597021eca59eb2ce37ef4de189eed25a8a91d51a466bbde5c42c54e4134) verified by the official C++ validator claim/IHTP_Validator.cc and standalone checker claim/author_checker_ihtp_check.py with Total violations = 0 and Total cost = 50,063, strictly improving on the best known upper bound of 50,976 listed on ihtc2024.github.io by 913 points (-1.791%).

## 1. Mandate & Literal Success Criterion Audit

The verbatim bank `success_criterion` stated in `claim/CLAIM.md` is:

"A JSON solution file for at least one of the 60 IHTC-2024 instances (`i01`..`i30` or `m01`..`m30`) for which running the official validator `IHTP_Validator` on `(instance.json, solution.json)` reports `Total violations = 0` and a `Total cost` strictly smaller than the best known cost for that instance listed on https://ihtc2024.github.io/ihtp/index.html at claim time. Same-day claim since `IHTP_Validator` compiles in seconds and verifies a single instance/solution pair in under 1 second."

I executed an independent verification script (`panel/criterion_work/verify_criterion.py`) against the artifacts in `claim/`. Every clause of the bank criterion was checked literally:

### Clause (1): Valid JSON Solution File for one of the 60 IHTC-2024 Instances (`i01`..`i30` or `m01`..`m30`)
- **Instance file:** `claim/i27.json` (`478,008` bytes, `sha256: a4c3d597021eca59eb2ce37ef4de189eed25a8a91d51a466bbde5c42c54e4134`) is benchmark instance `i27` from the 30 public instances (`i01`..`i30`) of the 60-instance IHTC-2024 benchmark suite (`i01`..`i30` and `m01`..`m30`).
- **Direct inspection of `claim/i27.json`:** `days = 28`, `shifts_per_day = 3` (`84` total shifts: `early`, `late`, `night`), `rooms = 26`, `operating_theaters = 8`, `surgeons = 8`, `nurses = 55`, `occupants = 41`, `patients = 493` (`123` mandatory, `370` optional). *(Minor prose erratum noted: line 6 of `claim/CLAIM.md` lists header entity counts from a different instance, whereas `claim/i27.json` and `claim/sol_i27.json` have exactly `493` patients, `55` nurses, `26` rooms, `8` operating theaters, `8` surgeons, and `41` occupants. This prose header discrepancy does not affect the validator, the solution file, or the objective calculation.)*
- **Solution file:** `claim/sol_i27.json` (`209,120` bytes, `sha256: 900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7`) is a valid JSON file containing all `493` distinct patient records (`448` admitted with valid admission day, room, and operating theater; `45` optional patients with `"admission_day": "none"`) and all `55` nurse assignment records covering all `26` rooms across all `84` shifts.
- **Status:** **MET**.

### Clause (2): Official `IHTP_Validator` Reports `Total violations = 0` and `Total cost = 50063`
- **Validator integrity:** `claim/IHTP_Validator.cc` (`38,733` bytes, `sha256: 0b56fa75ea7de1d4a7e3dbd2d5b88e7ac779d69e4287e1247305d873a06a8afa`) is the unmodified official C++ competition validator (`Version 0.0 (23/05/24)`).
- **Execution on `(claim/i27.json, claim/sol_i27.json)`:** Compiling `claim/IHTP_Validator.cc` with `clang++ -O3 -std=c++17` and running it on `(claim/i27.json, claim/sol_i27.json)` produces:
  - `RoomGenderMix = 0`
  - `PatientRoomCompatibility = 0`
  - `SurgeonOvertime = 0`
  - `OperatingTheaterOvertime = 0`
  - `MandatoryUnscheduledPatients = 0`
  - `AdmissionDay = 0`
  - `RoomCapacity = 0`
  - `NursePresence = 0`
  - `UncoveredRoom = 0`
  - `Total violations = 0`
  - `RoomAgeMix = 298 (1 X 298)`
  - `RoomSkillLevel = 3610 (10 X 361)`
  - `ContinuityOfCare = 3045 (1 X 3045)`
  - `ExcessiveNurseWorkload = 620 (10 X 62)`
  - `OpenOperatingTheater = 3210 (30 X 107)`
  - `SurgeonTransfer = 290 (10 X 29)`
  - `PatientDelay = 16490 (5 X 3298)`
  - `ElectiveUnscheduledPatients = 22500 (500 X 45)`
  - `Total cost = 50063`
- **Independent Python cross-check:** Running `claim/author_checker_ihtp_check.py` (`13,255` bytes, `sha256: f39b76a6e1bcb0d724ac3c2cb700418b534a5f31be00f08f4d2fc94dbb09cd0c`) on `(claim/i27.json, claim/sol_i27.json, 50063)` independently reproduces `Total violations = 0`, identical values for all 8 weighted soft-cost components, `Total cost = 50063`, and `IHTP_CHECK: PASS` in `0.0439` seconds.
- **Status:** **MET**.

### Clause (3): `Total cost` Strictly Smaller Than the Best Known Cost on `https://ihtc2024.github.io/ihtp/index.html`
- **Leaderboard snapshot verification:** Parsing `claim/ihtp_index.html` (`17,442` bytes, `sha256: 7c09c272ce00ce581c8537a3316898c97f7cfcf9a3fc6cdbeaac00e08279b495`) extracts all `60` instance upper bounds (`i01`..`i30` and `m01`..`m30`). Line 247-249 of `claim/ihtp_index.html` lists `i27` with best known cost `50976`.
- **Published baseline solution verification:** Running the compiled official `IHTP_Validator` on `(claim/i27.json, claim/published_sol_i27.json)` (`209,603` bytes, `sha256: 62669ec464f96211d362f2f4af07ac4913178975511d309110bd75e81493d1d5`) confirms `Total violations = 0` and `Total cost = 50976` (`RoomAgeMix = 298`, `RoomSkillLevel = 3930`, `ContinuityOfCare = 3518`, `ExcessiveNurseWorkload = 740`, `OpenOperatingTheater = 3210`, `SurgeonTransfer = 290`, `PatientDelay = 16490`, `ElectiveUnscheduledPatients = 22500`).
- **Strict improvement:** `50,063` is strictly smaller than `50,976` by `913` integer cost units (`-1.7910%` of total cost). Because the Surgical Case Planning and Patient Admission Scheduling (`"patients"`) assignments in `claim/sol_i27.json` are identical to `claim/published_sol_i27.json`, the entire `-913` reduction comes cleanly from the Nurse-to-Room Assignment subproblem (`RoomSkillLevel` reduced by `320` from `3,930` to `3,610`; `ContinuityOfCare` reduced by `473` from `3,518` to `3,045`; `ExcessiveNurseWorkload` reduced by `120` from `740` to `620`, a `-11.005%` reduction in NRA cost from `8,188` to `7,275`).
- **Status:** **MET**.

### Clause (4): Same-Day Claim Condition (Compilation in Seconds, Single-Pair Verification Under 1 Second)
- **Compilation time:** Compiling `claim/IHTP_Validator.cc` took `4.95` seconds.
- **Verification time:** Across 5 consecutive runs of `./IHTP_Validator_bin claim/i27.json claim/sol_i27.json`, wall-clock times were `0.5319s` (cold first run) and `0.0327s`, `0.0323s`, `0.0320s`, `0.0327s` (warm runs, mean `0.1323s`), well under the `1` second threshold. The standalone Python verifier `claim/author_checker_ihtp_check.py` also completes in `0.0439s`.
- **Status:** **MET**.

## 2. Hidden Quantifiers, Stretched Definitions, Perturbation Controls & Null Model Analysis

- **No hidden quantifiers or stretched definitions:** Every constraint (`H1`..`H9`) and objective weight (`S1`..`S8`) is defined directly by the competition's C++ source `claim/IHTP_Validator.cc` and instance file `claim/i27.json`. No problem parameters, weights, or feasibility rules were relaxed.
- **Why a 400-control statistical null test is not required for the claim decision:** Improving a deterministic combinatorial optimization upper bound requires exhibiting a single concrete witness certificate `claim/sol_i27.json` whose deterministic integer cost (`50,063`) is strictly less than the published integer upper bound (`50,976`) with zero hard violations (`Total violations = 0`). There is no sampling noise or estimator variance in evaluating a fixed schedule.
- **Perturbation & corruption controls (falsification checks):** To verify that neither `IHTP_Validator` nor `claim/author_checker_ihtp_check.py` can be bypassed or return a vacuous pass:
  1. *Control A (Unschedule mandatory patient `p000`):* Setting `"admission_day": "none"` for mandatory patient `p000` causes `IHTP_Validator` to report `MandatoryUnscheduledPatients = 1` (`Total violations = 1`) and `claim/author_checker_ihtp_check.py` to exit with return code `1` (`FAIL`).
  2. *Control B (Uncover occupied room `r04` on day 0 shift `early`):* Removing room `r04` from nurse `n011` on day 0 shift `early` causes `IHTP_Validator` to report `UncoveredRoom = 1` (`Total violations = 1`) and `claim/author_checker_ihtp_check.py` to exit with return code `1` (`FAIL`).
  3. *Control C (Incompatible room assignment for `p000`):* Reassigning patient `p000` from `r20` to incompatible room `r09` causes `IHTP_Validator` to report `PatientRoomCompatibility = 1` and `RoomCapacity = 2` (`Total violations = 3`) and `claim/author_checker_ihtp_check.py` to exit with return code `1` (`FAIL`).
  4. *Control D (Valid nurse swap perturbation on day 0 shift `early`):* Swapping assigned rooms between working nurses `n011` and `n013` on day 0 shift `early` preserves `Total violations = 0` but degrades `ContinuityOfCare` from `3045` to `3054` and `Total cost` from `50063` to `50072`; both C++ and Python checkers agree on `50072`, and `claim/author_checker_ihtp_check.py ... 50063` exits with return code `1` (`FAIL`).
  5. *Control E (Random feasible NRA null model, 100 seeds):* Fixing the exact patient admission schedule of `claim/sol_i27.json` and assigning each room on each shift uniformly at random to a working nurse on that shift across 100 random seeds yields `Total violations = 0` with `Total cost` ranging from `89,059` to `93,489` (mean `91,599.57`, standard deviation `1,017.85`). The claimed solution (`50,063`) is `40.8` standard deviations below the random feasible NRA null mean and `913` points below the published state-of-the-art upper bound (`50,976`).

pass: true
