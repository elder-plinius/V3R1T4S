# IHTC-2024 Hidden Instance `m28` Upper-Bound Improvement: `45,913 -> 45,873` (`-40`)

## What

An explicit feasible IHTC-2024 solution claim/sol_m28.json (307,109 bytes, sha256 d54f4151a022f91800fdc8a12226a5bc4da6d47ce2dcf51c575b36ead51b79c7) for hidden benchmark instance m28 (claim/m28.json, sha256 37061eb156c592feac39f5f148a5cfe4b594a57853638b0f2b041dd84c8f90e0) verified by the official C++ validator claim/IHTP_Validator.cc and standalone checker claim/author_checker_ihtp_check.py with Total violations = 0 and Total cost = 45,873, strictly improving on the best known upper bound of 45,913 listed on ihtc2024.github.io by 40 points.

- **Target ID:** `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`optimization-benchmarks`)
- **Instance:** `m28` (`28` days, `84` shifts, `42` rooms, `11` operating theaters, `10` surgeons, `84` nurses, `36` occupants, `611` patients)
- **Solution file:** `object/sol_m28.json` (`307,109` bytes, `sha256: d54f4151a022f91800fdc8a12226a5bc4da6d47ce2dcf51c575b36ead51b79c7`)
- **Hard constraint violations (`H1..H9`):** `Total violations = 0`
- **Weighted soft cost (`S1..S8`):** `Total cost = 45,873` (`RoomAgeMix = 58`, `RoomSkillLevel = 1,560`, `ContinuityOfCare = 13,875`, `ExcessiveNurseWorkload = 180`, `OpenOperatingTheater = 4,880`, `SurgeonTransfer = 480`, `PatientDelay = 16,440`, `ElectiveUnscheduledPatients = 8,400`)

## Check It Yourself

From the root of this package directory, run:

```bash
sh verify-it-yourself/run_checks.sh
```

This runs the zero-dependency standalone Python verifier `verify-it-yourself/author_checker_ihtp_check.py` (which implements all 9 hard constraints and 8 weighted soft constraints identically to `verify-it-yourself/IHTP_Validator.cc`) on `(verify-it-yourself/m28.json, object/sol_m28.json)` and checks `Total violations = 0` and `Total cost = 45873`, printing `PASS` on the final line in ~0.05 seconds.

## Compared To

- **Official IHTC-2024 Leaderboard (`https://ihtc2024.github.io/ihtp/index.html`):** Fetched at `2026-10-18T17:20:52Z` (`sha256: 7c09c272ce00ce581c8537a3316898c97f7cfcf9a3fc6cdbeaac00e08279b495`), which lists best known upper bound `45,913` for `m28` (Kletzander, Mischek & Musliu; solution file `the-record-we-beat/published_sol_m28.json`, `sha256: 4dff74744082ab6b04608cc13186aef635350ccf2cd92018ba443e1d85113cda`).
- **Component-wise improvement (`45,913 -> 45,873`, `-40` points):**
  - `RoomSkillLevel`: `1,565 -> 1,560` (**-5**)
  - `ContinuityOfCare`: `13,920 -> 13,875` (**-45**)
  - `ExcessiveNurseWorkload`: `170 -> 180` (+10)

## Not Claimed

- We do not claim optimality (a matching lower bound) for `m28`; `45,873` is a verified feasible upper bound.
- Although our solver `how-we-built-it/seam_surgery_ihtp.cc` with fixed settings (`seed=42, nra_sec=1.5, coupled_sec=1.0`) strictly improved 15 out of the 30 hidden `m`-instances (`m05, m10, m15, m17, m18, m19, m20, m21, m23, m24, m26, m27, m28, m29, m30`), this submission package claims and certifies the explicit solution `object/sol_m28.json` for hidden instance `m28`.

## Credits

- **Credit:** `mizopl` (`@mizopl`)
- **Benchmark & Official Validator:** Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf, Eugenia Zanazzo, Pieter Smet, and Greet Vanden Berghe (IHTC-2024 organizers); baseline `m28` solution (`45,913`) by Lucas Kletzander, Florian Mischek, and Nysret Musliu.
