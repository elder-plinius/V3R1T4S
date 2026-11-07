# Internal Verification Notes — Criterion (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` / `m26`)

- Context: contributor internal verification notes
- Target: `ihtp-ihtc2024-hidden-m-instances-upper-bounds`

## Literal Success Criterion Audit

1. **Instance Membership (`m01`–`m30`)**:
   - Instance `m26` is one of the 30 official hidden/final benchmark instances (`m01`–`m30`) in `ihtc2024_final_instances.zip`.
2. **Zero Hard-Constraint Violations**:
   - Verified against both the organisers' compiled C++ `IHTP_Validator` (`IHTP_Validator.cc`) and its standalone Python port (`verify-it-yourself/check_ihtp.py`) across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table at `https://ihtc2024.github.io/ihtp/index.html` lists `69715` (`sol_m26.json`) as the Best Known Solution (BKS) for `m26`.
   - Candidate solution `object/sol_m26_68496.json` achieves `Total cost = 68496` (`RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700`), strictly lower than `69715` by `1219` points (`-1.75%`).
4. **Hidden Quantifiers, Stretched Definitions, and Null Models**:
   - All integer weights and soft penalty calculations match `IHTP_Validator.cc` exactly with no relaxed constraints or modified instance parameters.

pass: true
