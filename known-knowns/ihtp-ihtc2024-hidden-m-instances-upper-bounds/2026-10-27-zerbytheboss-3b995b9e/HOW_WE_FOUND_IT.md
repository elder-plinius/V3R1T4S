# How We Found It (contributor text, unverified)

## Brief & Observation
Competition instance `m28` is a large-scale hidden problem spanning a 28-day planning horizon with 84 nurses across 42 rooms, 611 patients, 36 initial occupants, 10 surgeons, and 11 operating theaters. Starting from the published Best Known Solution `sol_m28.json` (`https://ihtc2024.github.io/assets/files/ihtp/solutions/sol_m28.json`, BKS cost `45873`), the primary objective drivers were heavy continuity-of-care penalties (`13875`) and nurse skill mismatches (`1560`), alongside substantial elective patient delay (`16440`).

## What Failed
Direct point swaps of individual nurses on single shifts (`NRA-1`) failed because swapping a nurse on one shift immediately ruptured continuity across multi-day patient stays in 42 rooms, causing massive spikes in the continuity-of-care penalty (weight 5 per excess nurse). Conversely, moving patients between rooms without coordinated nurse adjustments violated skill bounds and caused nurse workload violations.

## What Worked
Warm-starting from the published `sol_m28.json` (`45873`), we applied the coupled simulated annealing polisher (`how-we-built-it/IHTP_Polisher.cpp`) with multi-shift Kempe chains and contiguous nurse block moves (`NRA-CONT`). By reassigning nurses over multi-shift windows matching patient stay clusters, the polisher simultaneously reduced `ContinuityOfCare` from `13875` to `13495` (`-380`), `RoomSkillLevel` from `1560` to `1345` (`-215`), `PatientDelay` from `16440` to `16290` (`-150`), `SurgeonTransfer` from `480` to `410` (`-70`), `ExcessiveNurseWorkload` from `180` to `165` (`-15`), and `RoomAgeMix` from `58` to `52` (`-6`), achieving `Total cost = 45037` with zero violations across all 9 hard constraint categories (`-836` vs the live table BKS `45873`), verified by both our Python port (`verify-it-yourself/check_ihtp.py`) and the organisers' compiled C++ `IHTP_Validator`.
