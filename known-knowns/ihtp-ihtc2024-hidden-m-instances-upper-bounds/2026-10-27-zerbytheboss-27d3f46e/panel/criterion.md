# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m27`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
package: 2026-10-27-zerbytheboss-27d3f46e
audit_utc: 2026-10-27T19:50:00Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `m27` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `28013` as Best Known Solution.
   - Candidate solution `object/sol_m27_27527.json` achieves `Total cost = 27527` (RoomAgeMix 335, RoomSkillLevel 1915, ContinuityOfCare 6020, ExcessiveNurseWorkload 90, OpenOperatingTheater 1680, SurgeonTransfer 12, PatientDelay 3825, ElectiveUnscheduledPatients 13650), strictly lower by 486 points vs live BKS.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     335 + 1915 + 6020 + 90 + 1680 + 12 + 3825 + 13650 = 27527.

confirmed_scope: A feasible solution JSON file in object/sol_m27_27527.json for the IHTC-2024 competition instance m27 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 27527 (RoomAgeMix 335, RoomSkillLevel 1915, ContinuityOfCare 6020, ExcessiveNurseWorkload 90, OpenOperatingTheater 1680, SurgeonTransfer 12, PatientDelay 3825, ElectiveUnscheduledPatients 13650), verified by the official IHTP_Validator specification, strictly below the table upper bound of 28013 listed on https://ihtc2024.github.io/ihtp/index.html by 486 points.

pass: true
