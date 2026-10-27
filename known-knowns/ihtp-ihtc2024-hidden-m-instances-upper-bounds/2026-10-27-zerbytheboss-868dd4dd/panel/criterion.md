# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m21`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
package: 2026-10-27-zerbytheboss-868dd4dd
audit_utc: 2026-10-27T19:50:00Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `m21` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `25157` as Best Known Solution.
   - Candidate solution `object/sol_m21_24934.json` achieves `Total cost = 24934` (RoomAgeMix 49, RoomSkillLevel 1930, ContinuityOfCare 1375, ExcessiveNurseWorkload 385, OpenOperatingTheater 2200, SurgeonTransfer 40, PatientDelay 11955, ElectiveUnscheduledPatients 7000), strictly lower by 223 points vs live BKS.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     49 + 1930 + 1375 + 385 + 2200 + 40 + 11955 + 7000 = 24934.

confirmed_scope: A feasible solution JSON file in object/sol_m21_24934.json for the IHTC-2024 competition instance m21 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 24934 (RoomAgeMix 49, RoomSkillLevel 1930, ContinuityOfCare 1375, ExcessiveNurseWorkload 385, OpenOperatingTheater 2200, SurgeonTransfer 40, PatientDelay 11955, ElectiveUnscheduledPatients 7000), verified by the official IHTP_Validator specification, strictly below the table upper bound of 25157 listed on https://ihtc2024.github.io/ihtp/index.html by 223 points.

pass: true
