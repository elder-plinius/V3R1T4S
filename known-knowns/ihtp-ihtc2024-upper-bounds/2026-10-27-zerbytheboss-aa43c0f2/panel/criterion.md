# CRITERION Skeptic Audit — `ihtp-ihtc2024-upper-bounds` (`i19`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-upper-bounds
package: 2026-10-27-zerbytheboss-aa43c0f2
audit_utc: 2026-10-27T19:43:31Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `i19` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `43852` as Best Known Solution (hunt baseline `43857`).
   - Candidate solution `object/sol_i19_43365.json` achieves `Total cost = 43365` (RoomAgeMix 135, RoomSkillLevel 730, ContinuityOfCare 7225, ExcessiveNurseWorkload 590, OpenOperatingTheater 1920, SurgeonTransfer 120, PatientDelay 7395, ElectiveUnscheduledPatients 25250), strictly lower by 487 points vs live BKS and 492 points vs table baseline.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     135 + 730 + 7225 + 590 + 1920 + 120 + 7395 + 25250 = 43365.

confirmed_scope: A feasible solution JSON file in object/sol_i19_43365.json for the IHTC-2024 public instance i19 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 43365 (RoomAgeMix 135, RoomSkillLevel 730, ContinuityOfCare 7225, ExcessiveNurseWorkload 590, OpenOperatingTheater 1920, SurgeonTransfer 120, PatientDelay 7395, ElectiveUnscheduledPatients 25250), verified by the official IHTP_Validator specification, strictly below the table upper bound of 43852 listed on https://ihtc2024.github.io/ihtp/index.html by 487 points (and strictly below hunt baseline 43857 by 492 points).

pass: true
