# IHTC-2024 Benchmark Instance `i27` Upper-Bound Improvement: `50,976 -> 50,063` (`-913`)

## What

An explicit feasible IHTC-2024 solution claim/sol_i27.json (209,120 bytes, sha256 900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7) for benchmark instance i27 (claim/i27.json, sha256 a4c3d597021eca59eb2ce37ef4de189eed25a8a91d51a466bbde5c42c54e4134) verified by the official C++ validator claim/IHTP_Validator.cc and standalone checker claim/author_checker_ihtp_check.py with Total violations = 0 and Total cost = 50,063, strictly improving on the best known upper bound of 50,976 listed on ihtc2024.github.io by 913 points (-1.791%).

- **Target ID:** `ihtp-ihtc2024-upper-bounds` (`optimization-benchmarks`)
- **Instance:** `i27` (`28` days, `84` shifts, `26` rooms, `8` operating theaters, `8` surgeons, `55` nurses, `41` occupants, `493` patients)
- **Solution file:** `object/sol_i27.json` (`209,120` bytes, `sha256: 900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7`)
- **Hard constraint violations (`H1..H9`):** `Total violations = 0`
- **Weighted soft cost (`S1..S8`):** `Total cost = 50,063` (`RoomAgeMix = 298`, `RoomSkillLevel = 3,610`, `ContinuityOfCare = 3,045`, `ExcessiveNurseWorkload = 620`, `OpenOperatingTheater = 3,210`, `SurgeonTransfer = 290`, `PatientDelay = 16,490`, `ElectiveUnscheduledPatients = 22,500`)

## Check It Yourself

From the root of this package directory, run:

```bash
sh verify-it-yourself/run_checks.sh
```

This runs the zero-dependency standalone Python verifier `verify-it-yourself/author_checker_ihtp_check.py` (which implements all 9 hard constraints and 8 weighted soft constraints identically to `verify-it-yourself/IHTP_Validator.cc`) on `(verify-it-yourself/i27.json, object/sol_i27.json)` and checks `Total violations = 0` and `Total cost = 50063`, printing `PASS` on the final line in ~0.05 seconds.

## Compared To

- **Official IHTC-2024 Leaderboard (`https://ihtc2024.github.io/ihtp/index.html`):** Fetched at `2026-10-18T14:07:58Z` (`sha256: 7c09c272ce00ce581c8537a3316898c97f7cfcf9a3fc6cdbeaac00e08279b495`), which lists best known upper bound `50,976` for `i27` (Kletzander, Mischek & Musliu; solution file `the-record-we-beat/published_sol_i27.json`, `sha256: 62669ec464f96211d362f2f4af07ac4913178975511d309110bd75e81493d1d5`).
- **Component-wise improvement (`50,976 -> 50,063`, `-913` points):**
  - `RoomSkillLevel`: `3,930 -> 3,610` (**-320**)
  - `ContinuityOfCare`: `3,518 -> 3,045` (**-473**)
  - `ExcessiveNurseWorkload`: `740 -> 620` (**-120**)
  - Total Nurse-to-Room Assignment (`NRA`) soft cost: `8,188 -> 7,275` (**-913**, **-11.005%**)
- **Open V3R1T4S PRs:** Strictly improves on pending PR `#359` (`50,125` on `i27`) by another `-62` points.

## Not Claimed

- We do not claim optimality (a matching lower bound) for `i27`; `50,063` is a verified feasible upper bound.
- Although our solver `how-we-built-it/seam_surgery_ihtp.cc` strictly improved 31 out of 60 IHTC-2024 instances (`16` public `i`-instances and `15` hidden `m`-instances) in a single benchmark sweep, this submission package claims and certifies the explicit solution `object/sol_i27.json` for instance `i27`.

## Credits

- **Credit:** `mizopl` (`@mizopl`)
- **Benchmark & Official Validator:** Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf, and Eugenia Zanazzo (IHTC-2024 organizers); baseline `i27` solution (`50,976`) by Lucas Kletzander, Florian Mischek, and Nysret Musliu.
