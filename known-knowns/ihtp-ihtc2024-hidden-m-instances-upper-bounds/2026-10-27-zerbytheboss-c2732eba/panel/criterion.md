# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m30`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
package: 2026-10-27-zerbytheboss-c2732eba
audit_utc: 2026-10-27T19:43:31Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `m30` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `31641` as Best Known Solution (hunt baseline `31649`).
   - Candidate solution `object/sol_m30_31102.json` achieves `Total cost = 31102` (RoomAgeMix 130, RoomSkillLevel 320, ContinuityOfCare 2830, ExcessiveNurseWorkload 1252, OpenOperatingTheater 6000, SurgeonTransfer 350, PatientDelay 11420, ElectiveUnscheduledPatients 8800), strictly lower by 539 points vs live BKS and 547 points vs table baseline.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     130 + 320 + 2830 + 1252 + 6000 + 350 + 11420 + 8800 = 31102.

confirmed_scope: A feasible solution JSON file in object/sol_m30_31102.json for the IHTC-2024 competition instance m30 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 31102 (RoomAgeMix 130, RoomSkillLevel 320, ContinuityOfCare 2830, ExcessiveNurseWorkload 1252, OpenOperatingTheater 6000, SurgeonTransfer 350, PatientDelay 11420, ElectiveUnscheduledPatients 8800), verified by the official IHTP_Validator specification, strictly below the table upper bound of 31641 listed on https://ihtc2024.github.io/ihtp/index.html by 539 points (and strictly below hunt baseline 31649 by 547 points).

pass: true
