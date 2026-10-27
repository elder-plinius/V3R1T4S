# CRITERION Skeptic Audit — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m28`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
package: 2026-10-27-zerbytheboss-3b995b9e
audit_utc: 2026-10-27T19:43:31Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `m28` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `45873` as Best Known Solution (hunt baseline `45913`).
   - Candidate solution `object/sol_m28_45037.json` achieves `Total cost = 45037` (RoomAgeMix 52, RoomSkillLevel 1345, ContinuityOfCare 13495, ExcessiveNurseWorkload 165, OpenOperatingTheater 4880, SurgeonTransfer 410, PatientDelay 16290, ElectiveUnscheduledPatients 8400), strictly lower by 836 points vs live BKS and 876 points vs table baseline.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     52 + 1345 + 13495 + 165 + 4880 + 410 + 16290 + 8400 = 45037.

confirmed_scope: A feasible solution JSON file in object/sol_m28_45037.json for the IHTC-2024 competition instance m28 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 45037 (RoomAgeMix 52, RoomSkillLevel 1345, ContinuityOfCare 13495, ExcessiveNurseWorkload 165, OpenOperatingTheater 4880, SurgeonTransfer 410, PatientDelay 16290, ElectiveUnscheduledPatients 8400), verified by the official IHTP_Validator specification, strictly below the table upper bound of 45873 listed on https://ihtc2024.github.io/ihtp/index.html by 836 points (and strictly below hunt baseline 45913 by 876 points).

pass: true
