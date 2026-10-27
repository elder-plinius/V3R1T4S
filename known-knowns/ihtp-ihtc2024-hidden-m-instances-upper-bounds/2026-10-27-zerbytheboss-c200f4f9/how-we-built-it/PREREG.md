# Preregistered Evaluation Bar (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` / `m09`)

frozen_utc: 2026-10-27T15:08:00Z
target_id: ihtp-ihtc2024-hidden-m-instances-upper-bounds
cell: m09
category: optimization-benchmarks

## 1. Verbatim Target Bank Criteria
> Feasible schedule with zero hard-constraint violations (Total violations = 0 across all 9 categories) whose integer soft objective strictly improves upon the published table upper bound on https://ihtc2024.github.io/ihtp/index.html.

## 2. Evaluation Metric & Thresholds
- Hard constraints: H1 (RoomGenderMix), H2 (PatientRoomCompatibility), H3 (SurgeonOvertime), H4 (OperatingTheaterOvertime), H5 (MandatoryUnscheduledPatients), H6 (AdmissionDay), H7 (RoomCapacity), H8 (NursePresence), H9 (UncoveredRoom). All must equal 0.
- Soft objective: weighted sum of S1 (RoomAgeMix), S2 (RoomSkillLevel), S3 (ContinuityOfCare), S4 (ExcessiveNurseWorkload), S5 (OpenOperatingTheater), S6 (SurgeonTransfer), S7 (PatientDelay), S8 (ElectiveUnscheduledPatients).
- Threshold: Objective strictly lower than official live BKS 32967.
