# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m24`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
package: 2026-10-27-zerbytheboss-2db80383
audit_utc: 2026-10-27T19:50:00Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `m24` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `30870` as Best Known Solution.
   - Candidate solution `object/sol_m24_30363.json` achieves `Total cost = 30363` (RoomAgeMix 70, RoomSkillLevel 0, ContinuityOfCare 2242, ExcessiveNurseWorkload 926, OpenOperatingTheater 1640, SurgeonTransfer 180, PatientDelay 5355, ElectiveUnscheduledPatients 19950), strictly lower by 507 points vs live BKS.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     70 + 0 + 2242 + 926 + 1640 + 180 + 5355 + 19950 = 30363.

confirmed_scope: A feasible solution JSON file in object/sol_m24_30363.json for the IHTC-2024 competition instance m24 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 30363 (RoomAgeMix 70, RoomSkillLevel 0, ContinuityOfCare 2242, ExcessiveNurseWorkload 926, OpenOperatingTheater 1640, SurgeonTransfer 180, PatientDelay 5355, ElectiveUnscheduledPatients 19950), verified by the official IHTP_Validator specification, strictly below the table upper bound of 30870 listed on https://ihtc2024.github.io/ihtp/index.html by 507 points.

pass: true
