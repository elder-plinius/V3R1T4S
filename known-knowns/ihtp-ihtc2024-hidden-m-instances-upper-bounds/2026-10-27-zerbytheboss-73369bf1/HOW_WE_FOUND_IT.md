# How We Found It (contributor text, unverified)

## Brief & Observation
Competition instance m29 features 28 days, 96 nurses, 49 rooms, 631 patients, 44 initial occupants, 8 surgeons, and only 5 operating theaters. The critical bottleneck is the severe theater scarcity: 631 patients must be scheduled into just 5 operating theaters over 28 days, forcing dense theater packing while leaves nurse assignment across 49 rooms prone to high skill-level mismatches (1600 in BKS).

## What Failed
Attempting to shift operating theater assignments (`SCP-OT`) frequently violated daily theater availability (hard constraint H4) or surgeon daily capacity (H3). Furthermore, isolated nurse reassignments could not overcome skill deficits without creating excessive nurse workload (H8/S4) in the remaining 49 rooms.

## What Worked
Using `how-we-built-it/IHTP_Polisher.cpp`, we locked the tightly packed feasible theater schedule and executed intensive nurse-room neighborhood search with 3-cycle permutations (`NRA-3CYCLE`) and skill-guided Kempe swaps. This drastically collapsed RoomSkillLevel from 1600 to 1090 (-510), ContinuityOfCare from 2739 to 2453 (-286), and ExcessiveNurseWorkload from 115 to 80 (-35), easily absorbing a minor +5 adjustment in RoomAgeMix (50 to 55). The result is Total cost = 47253 with Total violations = 0 (-829 vs baseline 48082, -826 vs live table 48079).
