# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m26`)

- `context`: subagent (fresh invocation)
- `target_id`: `ihtp-ihtc2024-hidden-m-instances-upper-bounds`
- `submission_id`: `2026-10-17-1084ec80`
- `audit_utc`: `2026-10-17T17:00:10Z`

## Literal Success Criterion Audit

1. **Instance Membership (`m01`–`m30`)**:
   - Instance `m26` is one of the 30 official hidden/final benchmark instances (`m01`–`m30`) in `ihtc2024_final_instances.zip`.
2. **Zero Hard-Constraint Violations**:
   - Verified against both the official C++ `IHTP_Validator.cc` specification and its standalone Python port across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonsOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table at `https://ihtc2024.github.io/ihtp/index.html` lists `69730` as the Best Known Solution (BKS) for `m26`.
   - Candidate solution `object/sol_m26_68496.json` achieves `Total cost = 68496` (`RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700`), strictly lower than `69730` by `1234` points (`-1.77%`).
   - Satisfies both the full `success_criterion` (`CONFIRMED_SOLUTION`) and partial win `p1`.
4. **Hidden Quantifiers, Stretched Definitions, and Null Models**:
   - All integer weights and soft penalty calculations match `IHTP_Validator.cc` exactly with no relaxed constraints or modified instance parameters. Null model is not applicable to deterministic combinatorial optimization with an exact validator.

confirmed_scope: A feasible solution JSON file in object/sol_m26_68496.json for the IHTC-2024 competition instance m26 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 68496 (RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700), verified by both the official C++ IHTP_Validator specification and its standalone Python port, strictly below the best-known upper bound of 69730 listed on https://ihtc2024.github.io/ihtp/index.html by 1234 points.

pass: true
