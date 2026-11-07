# Internal Verification Gate Notes — `ihtp-ihtc2024-hidden-m-instances-upper-bounds`

status: CONFIRMED_PARTIAL
confirmed_scope: A feasible solution JSON file in object/sol_m28_45037.json for the IHTC-2024 competition instance m28 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 45037 (RoomAgeMix 52, RoomSkillLevel 1345, ContinuityOfCare 13495, ExcessiveNurseWorkload 165, OpenOperatingTheater 4880, SurgeonTransfer 410, PatientDelay 16290, ElectiveUnscheduledPatients 8400), verified both by our standalone Python port (verify-it-yourself/check_ihtp.py) and by the organisers' compiled C++ IHTP_Validator (IHTP_Validator.cc), strictly below the table upper bound of 45873 listed on https://ihtc2024.github.io/ihtp/index.html by 836 points.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: Independent verification against both the organisers' compiled C++ validator (`IHTP_Validator.cc`) and our standalone Python port (`verify-it-yourself/check_ihtp.py`); exact SHA-256 and constraint properties certified.
- **NOVELTY (`panel/novelty.md`)**: Verified against the live IHTC-2024 status table (`45873`, `sol_m28.json`) and 2024–2026 literature.
- **CRITERION (`panel/criterion.md`)**: Exact integer soft-cost reconciliation summing to claimed objective `45037`, zero hard violations, strict improvement by `836` points over `45873`.
