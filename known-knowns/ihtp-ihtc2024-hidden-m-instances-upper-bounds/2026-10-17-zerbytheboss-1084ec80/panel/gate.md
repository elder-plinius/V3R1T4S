# Internal Verification Gate Notes — `ihtp-ihtc2024-hidden-m-instances-upper-bounds`

status: CONFIRMED_PARTIAL
confirmed_scope: A feasible solution JSON file in object/sol_m26_68496.json for the IHTC-2024 competition instance m26 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 68496 (RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700), verified by both the official compiled C++ IHTP_Validator and its standalone Python port, strictly below the best-known upper bound of 69715 listed on https://ihtc2024.github.io/ihtp/index.html by 1219 points.

## Internal Verification Summary
- **REPRODUCE (`panel/reproduce.md`)**: Internal reproduction notes verifying `object/sol_m26_68496.json` against both the organisers' compiled C++ `IHTP_Validator` and our standalone Python port (`verify-it-yourself/check_ihtp.py`).
- **NOVELTY (`panel/novelty.md`)**: Internal novelty check against `https://ihtc2024.github.io/ihtp/index.html` (`69715`, `sol_m26.json`, fetched `2026-11-07T05:10:33Z`) and `arXiv:2610.00044`.
- **CRITERION (`panel/criterion.md`)**: Internal criterion check against `bank/targets.json`.
