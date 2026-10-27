# How We Found It (contributor text, unverified)

## Brief & Observation
Competition instance m30 has a compact 21-day planning horizon with 90 nurses, 48 rooms, 489 patients, 31 occupants, 11 surgeons, and 8 operating theaters. In the BKS solution (cost 31641, baseline 31649), nurse workloads were unevenly distributed, generating an unusually high ExcessiveNurseWorkload penalty of 1422 alongside 3064 in ContinuityOfCare.

## What Failed
Local single-shift moves (`NRA-1`) could reduce individual nurse workload but consistently pushed load onto other shifts or degraded nurse-to-room continuity, oscillating without escaping the workload local minimum.

## What Worked
The C++17 solver in `how-we-built-it/IHTP_Polisher.cpp` targeted nurse workload balance using multi-shift workload-smoothing chains (`NRA-CONT`) combined with patient room swaps (`PAS-ROOM`). This successfully rebalanced the nurse shift rosters, reducing ExcessiveNurseWorkload from 1422 to 1252 (-170), ContinuityOfCare from 3064 to 2830 (-234), RoomSkillLevel from 450 to 320 (-130), and RoomAgeMix from 135 to 130 (-5), yielding Total cost = 31102 with Total violations = 0 (-547 vs baseline 31649, -539 vs live table 31641).
