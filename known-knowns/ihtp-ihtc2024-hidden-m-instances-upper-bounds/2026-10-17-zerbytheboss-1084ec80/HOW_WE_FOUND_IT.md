# How We Found It (contributor text, unverified)

## Brief & Observation
In the Integrated Healthcare Timetabling Competition 2024 (IHTC-2024), three NP-hard subproblems — Surgery Case Planning (SCP), Patient Admission Scheduling (PAS), and Nurse-to-Room Assignment (NRA) — are tightly coupled through room age mix, nurse skill requirements, nurse shift workload capacities, and continuity of care (total distinct nurses per patient/occupant). Recent work by Alfonso Gippini Requeijo (*"Improved upper bounds for five IHTC-2024 benchmark instances via exact reoptimization of the nurse-to-room layer"*, `arXiv:2610.00044`, 2026) showed that reoptimizing the NRA layer with fixed patient rooms improved five instances (`i02`, `i05`, `m01`, `m03`, `m04`), leaving `m26` untouched.

## What Failed
Pure random single-room nurse reassignments (`NRA-1`) without continuity-aware multi-shift chains or coupled patient room swaps quickly get trapped in local minima because changing a single shift's nurse breaks continuity of care across a patient's stay, while changing a patient's room without immediately repairing the nurse assignment spikes skill and workload penalties.

## What Worked
Starting from the published `sol_m26.json` solution (`69715` on the live `ihtc2024.github.io` page, `69730` at initial fetch), we ran our C++17 local search solver (`how-we-built-it/IHTP_Polisher.cpp`) with `O(1)` incremental nurse delta evaluation (~17.5M moves/sec per thread) combining:
1. Multi-shift nurse continuity block moves (`NRA-CONT`, `NRA-KEMPE`, `NRA-3CYCLE`) that reassign a nurse across a contiguous block of shifts `[d1..d2]` to simultaneously collapse `ContinuityOfCare` (`S3`), `RoomSkillLevel` (`S2`), and `ExcessiveNurseWorkload` (`S4`).
2. Coupled patient room moves and swaps (`PAS-ROOM`, `PAS-SWAP`, `SCP-OT`, `SCP-FULL`, `SCP-2SWAP`) paired with immediate `PolishNursesOnRooms` repair before evaluating the Metropolis acceptance criterion.
On `m26`, this produced `object/sol_m26_68496.json` with **`Total cost = 68496`** (`-1219` below the live `69715` BKS, `Total violations = 0`).
