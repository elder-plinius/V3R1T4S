# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m09`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
package: 2026-10-27-zerbytheboss-c200f4f9
audit_utc: 2026-10-27T19:50:00Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `m09` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `32967` as Best Known Solution.
   - Candidate solution `object/sol_m09_32675.json` achieves `Total cost = 32675` (RoomAgeMix 34, RoomSkillLevel 170, ContinuityOfCare 1198, ExcessiveNurseWorkload 968, OpenOperatingTheater 1170, SurgeonTransfer 10, PatientDelay 13125, ElectiveUnscheduledPatients 16000), strictly lower by 292 points vs live BKS.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     34 + 170 + 1198 + 968 + 1170 + 10 + 13125 + 16000 = 32675.

confirmed_scope: A feasible solution JSON file in object/sol_m09_32675.json for the IHTC-2024 competition instance m09 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 32675 (RoomAgeMix 34, RoomSkillLevel 170, ContinuityOfCare 1198, ExcessiveNurseWorkload 968, OpenOperatingTheater 1170, SurgeonTransfer 10, PatientDelay 13125, ElectiveUnscheduledPatients 16000), verified by the official IHTP_Validator specification, strictly below the table upper bound of 32967 listed on https://ihtc2024.github.io/ihtp/index.html by 292 points.

pass: true
