# How We Found It (contributor text, unverified)

## Brief & Observation
In the Integrated Healthcare Timetabling Competition 2024 (IHTC-2024), three NP-hard subproblems — Surgery Case Planning (SCP), Patient Admission Scheduling (PAS), and Nurse-to-Room Assignment (NRA) — are tightly coupled through room age mix, nurse skill requirements, nurse shift workload capacities, and continuity of care (total distinct nurses per patient/occupant). Recent work (`arXiv:2610.00044`) showed that reoptimizing the NRA layer with fixed patient rooms improved five instances (`i02`, `i05`, `m01`, `m03`, `m04`), but left the coupled patient-room and nurse-room frontier unexplored on 55 of the 60 benchmark instances.

## What Failed
Pure random single-room nurse reassignments (`NRA-1`) without continuity-aware multi-shift chains or coupled patient room swaps quickly get trapped in local minima because changing a single shift's nurse breaks continuity of care across a patient's stay, while changing a patient's room without immediately repairing the nurse assignment spikes skill and workload penalties.

## What Worked
We built a C++17 solver (`how-we-built-it/IHTP_Polisher.cc`) with `O(1)` incremental nurse delta evaluation (~17.5M moves/sec per thread) combining:
1. Multi-shift nurse continuity block moves (`NRA-CONT`, `NRA-KEMPE`, `NRA-3CYCLE`) that reassign a nurse across a contiguous block of shifts `[d1..d2]` to simultaneously collapse `ContinuityOfCare` (`S3`), `RoomSkillLevel` (`S2`), and `ExcessiveNurseWorkload` (`S4`).
2. Coupled patient room moves and swaps (`PAS-ROOM`, `PAS-SWAP`, `SCP-OT`, `SCP-FULL`, `SCP-2SWAP`) paired with immediate `PolishNursesOnRooms` repair before evaluating the Metropolis acceptance criterion.
On `m26`, this reduced the objective from `69730` to **`68496`** (`-1234`, `Total violations = 0`).
