# CRITERION Skeptic Audit — `ihtp-ihtc2024-upper-bounds` (`i27`)

- `context`: subagent (fresh invocation)
- `target_id`: `ihtp-ihtc2024-upper-bounds`
- `audit_utc`: `2026-10-17T17:00:10Z`

## Literal Success Criterion Audit

1. **Instance Membership (`i01`–`i30` or `m01`–`m30`)**:
   - Instance `i27` is one of the 30 official public competition instances (`i01`–`i30`) in `ihtc2024_competition_instances.zip`.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonsOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table at `https://ihtc2024.github.io/ihtp/index.html` lists `50976` as the Best Known Solution (BKS) for `i27`.
   - Candidate solution `object/sol_i27_50125.json` achieves `Total cost = 50125` (`RoomAgeMix 292, RoomSkillLevel 3650, ContinuityOfCare 3103, ExcessiveNurseWorkload 590, OpenOperatingTheater 3210, SurgeonTransfer 290, PatientDelay 16490, ElectiveUnscheduledPatients 22500`), strictly lower than `50976` by `851` points (`-1.54%`).
   - Satisfies both the full `success_criterion` (`CONFIRMED_SOLUTION`) and partial win `p1`.
4. **Hidden Quantifiers, Stretched Definitions, and Null Models**:
   - All integer weights and soft penalty calculations match `IHTP_Validator.cc` exactly with no relaxed constraints or modified instance parameters. Null model is not applicable to deterministic combinatorial optimization with an exact validator.

confirmed_scope: A feasible solution JSON file in object/sol_i27_50125.json for the IHTC-2024 public test instance i27 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 50125 (RoomAgeMix 292, RoomSkillLevel 3650, ContinuityOfCare 3103, ExcessiveNurseWorkload 590, OpenOperatingTheater 3210, SurgeonTransfer 290, PatientDelay 16490, ElectiveUnscheduledPatients 22500), verified by the official IHTP_Validator specification, strictly below the best-known upper bound of 50976 listed on https://ihtc2024.github.io/ihtp/index.html by 851 points.

pass: true
