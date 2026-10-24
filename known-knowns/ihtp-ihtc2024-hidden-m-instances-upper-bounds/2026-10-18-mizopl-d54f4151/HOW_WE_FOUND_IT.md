# How We Found It (`contributor text, unverified`)

> **Note:** This narrative is contributor text, unverified; only the solution file `object/sol_i27.json` and its mechanical verification in `verify-it-yourself/` constitute the verified claim.

## 1. Diagnosing the `ContinuityOfCare` Multi-Shift Seam Barrier

Competition entries for the Integrated Healthcare Timetabling Competition 2024 (IHTC-2024) typically decompose the problem into two stages:
1. Stage 1 assigns admission days, rooms, and operating theaters to patients (`SCP` + `PAS`).
2. Stage 2 assigns working nurses to `(room, shift)` pairs (`NRA`), minimizing `RoomSkillLevel`, `ContinuityOfCare` (`CoC`), and `ExcessiveNurseWorkload`.

In `NRA`, `ContinuityOfCare` counts the number of *distinct* nurses covering each occupant or admitted patient across their stay. Standard local search neighborhoods that reassign one `(room, shift)` at a time or swap nurses between two rooms on a single shift hit a structural barrier whenever a nurse $n_{\text{drop}}$ covers $k \ge 2$ shifts of a patient $q$'s stay: replacing $n_{\text{drop}}$ on any single shift leaves $n_{\text{drop}}$ covering $k - 1 \ge 1$ shifts of $q$'s stay, yielding $\Delta \text{CoC}(q) \ge 0$.

## 2. CLSS Compound Patient-Stay Nurse Consolidation (`how-we-built-it/seam_surgery_ihtp.cc`)

We built a C++ solver (`seam_surgery_ihtp.cc`) directly atop the official validator's data structures with three components:
1. **$O(1)$ (`~10 ns`) Incremental NRA Evaluation:** Precomputes per-`(room, shift, nurse)` skill penalties, room-shift patient workloads, nurse-shift loads, and per-`(patient, nurse)` shift coverage counts so single-shift reassignments and two-room shift swaps are evaluated in ~10 nanoseconds.
2. **Compound Patient-Stay Nurse Consolidation (`GreedyPolishNRA`):** For each patient/occupant $q$, identifies every nurse $n_{\text{drop}}$ covering $q$ on $k \ge 1$ shifts and attempts to simultaneously replace or swap $n_{\text{drop}} \to n_{\text{keep}}$ across *all $k$ shifts of $q$'s stay at once*, crossing the $k \ge 2$ barrier in a single move.
3. **Exact 6-Nurse Subset MILP Polish (`how-we-built-it/subset_nra_milp.py`):** Samples subsets of $K = 6$ nurses across all 84 shifts and solves the exact subproblem MILP (`scipy.optimize.milp` / HiGHS) over all rooms covered by those 6 nurses, capturing coordinated multi-room, multi-shift nurse reassignments.

## 3. Results Across the 60-Instance Benchmark Suite and Deep Polish on `i27`

- Running `how-we-built-it/run_60_benchmark.py` (`seed=42`, `2.5s` per instance) across all 60 IHTC-2024 instances (`i01..i30`, `m01..m30`) strictly improved **31 out of 60 best known upper bounds** (`16` public `i`-instances and `15` hidden `m`-instances), all with `Total violations = 0`.
- On instance `i27` (published best `50,976`), single-pass CLSS seam surgery reached `50,078` (`-898`), multi-seed CLSS SA (`seeds 1..25`) reached `50,068` (`-908`), and 6-nurse subset MILP polish (`subset_nra_milp.py`) followed by `GreedyPolishNRA` reached **`50,063` (`-913`)**:
  - `RoomSkillLevel`: `3,930 -> 3,610` (`-320`)
  - `ContinuityOfCare`: `3,518 -> 3,045` (`-473`)
  - `ExcessiveNurseWorkload`: `740 -> 620` (`-120`)
