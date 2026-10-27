# How We Found It — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m27`)

Contributor text, unverified.

## Brief & Observation
Competition instance m27 features a 14-day horizon with 70 nurses, 36 rooms, 295 patients, 47 occupants, 11 surgeons, and 16 operating theaters with 5 skill levels and 5 age groups. The incumbent BKS (cost 28013) carried heavy continuity-of-care penalties (6385) and room skill mismatches (2035).

## What Failed
Because m27 has 5 distinct age groups and 5 skill levels, unguided patient room swaps frequently caused age-mixing penalty explosions (S1), while isolated nurse reassignments could not reconcile high-skill demand without generating excessive workload elsewhere.

## What Worked
The C++17 polisher (`how-we-built-it/IHTP_Polisher.cpp`) combined age-preserving patient room exchanges (`PAS-ROOM`) with 3-cycle nurse-skill permutations (`NRA-3CYCLE`). This restructured the nurse rosters to match patient skill profiles, slashing ContinuityOfCare from 6385 to 6020 (-365) and RoomSkillLevel from 2035 to 1915 (-120), with minor improvements in delay, reaching Total cost = 27527 with zero violations across all 9 hard constraint categories (strict improvement of -486 points vs live BKS 28013).
