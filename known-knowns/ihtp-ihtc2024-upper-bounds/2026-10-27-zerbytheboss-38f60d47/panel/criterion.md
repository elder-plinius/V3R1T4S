# CRITERION Skeptic Audit — `ihtp-ihtc2024-upper-bounds` (`i26`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-upper-bounds
package: 2026-10-27-zerbytheboss-38f60d47
audit_utc: 2026-10-27T19:43:31Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `i26` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `64334` as Best Known Solution (hunt baseline `64352`).
   - Candidate solution `object/sol_i26_63978.json` achieves `Total cost = 63978` (RoomAgeMix 167, RoomSkillLevel 1136, ContinuityOfCare 9815, ExcessiveNurseWorkload 20, OpenOperatingTheater 880, SurgeonTransfer 90, PatientDelay 19370, ElectiveUnscheduledPatients 32500), strictly lower by 356 points vs live BKS and 374 points vs table baseline.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     167 + 1136 + 9815 + 20 + 880 + 90 + 19370 + 32500 = 63978.

confirmed_scope: A feasible solution JSON file in object/sol_i26_63978.json for the IHTC-2024 public instance i26 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 63978 (RoomAgeMix 167, RoomSkillLevel 1136, ContinuityOfCare 9815, ExcessiveNurseWorkload 20, OpenOperatingTheater 880, SurgeonTransfer 90, PatientDelay 19370, ElectiveUnscheduledPatients 32500), verified by the official IHTP_Validator specification, strictly below the table upper bound of 64334 listed on https://ihtc2024.github.io/ihtp/index.html by 356 points (and strictly below hunt baseline 64352 by 374 points).

pass: true
