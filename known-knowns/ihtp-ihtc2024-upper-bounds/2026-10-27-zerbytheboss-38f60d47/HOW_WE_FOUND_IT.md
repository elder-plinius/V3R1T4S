# How We Found It (contributor text, unverified)

## Brief & Observation
Public benchmark instance i26 features 28 days with 54 nurses, 26 rooms, 476 patients, 33 initial occupants, 7 surgeons, and 8 operating theaters. With 476 patients competing for only 26 rooms over 28 days, room density is high, making room age mixing and nurse continuity major soft-cost challenges (10100 for ContinuityOfCare and 201 for RoomAgeMix in BKS).

## What Failed
Uncoordinated patient room reallocations broke age-group homogeneity (S1) or room capacity (H7), while isolated nurse reassignments could not overcome fragmented continuity over lengthy patient stays.

## What Worked
The C++17 solver in `how-we-built-it/IHTP_Polisher.cpp` performed synchronized patient room swaps (`PAS-SWAP`) paired with multi-shift nurse Kempe-chain sweeps. This harmonized patient age clusters in rooms and unified nurse coverage schedules, lowering ContinuityOfCare from 10100 to 9815 (-285), RoomAgeMix from 201 to 167 (-34), RoomSkillLevel from 1163 to 1136 (-27), and ExcessiveNurseWorkload from 30 to 20 (-10). The final schedule reaches Total cost = 63978 with zero violations across all 9 hard constraint categories (-374 vs baseline 64352, -356 vs live table 64334).
