# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m29`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
package: 2026-10-27-zerbytheboss-73369bf1
audit_utc: 2026-10-27T19:43:31Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `m29` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `48079` as Best Known Solution (hunt baseline `48082`).
   - Candidate solution `object/sol_m29_47253.json` achieves `Total cost = 47253` (RoomAgeMix 55, RoomSkillLevel 1090, ContinuityOfCare 2453, ExcessiveNurseWorkload 80, OpenOperatingTheater 3600, SurgeonTransfer 120, PatientDelay 7305, ElectiveUnscheduledPatients 32550), strictly lower by 826 points vs live BKS and 829 points vs table baseline.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     55 + 1090 + 2453 + 80 + 3600 + 120 + 7305 + 32550 = 47253.

confirmed_scope: A feasible solution JSON file in object/sol_m29_47253.json for the IHTC-2024 competition instance m29 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 47253 (RoomAgeMix 55, RoomSkillLevel 1090, ContinuityOfCare 2453, ExcessiveNurseWorkload 80, OpenOperatingTheater 3600, SurgeonTransfer 120, PatientDelay 7305, ElectiveUnscheduledPatients 32550), verified by the official IHTP_Validator specification, strictly below the table upper bound of 48079 listed on https://ihtc2024.github.io/ihtp/index.html by 826 points (and strictly below hunt baseline 48082 by 829 points).

pass: true
