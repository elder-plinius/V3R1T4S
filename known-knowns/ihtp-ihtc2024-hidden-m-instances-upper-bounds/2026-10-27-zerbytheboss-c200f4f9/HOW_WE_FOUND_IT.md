# How We Found It — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m09`)

Contributor text, unverified.

## Brief & Observation
Competition instance m09 spans 28 days with 30 nurses, 13 rooms, 221 patients, 18 occupants, 3 surgeons, and 3 operating theaters, featuring 5 skill levels. The incumbent BKS (cost 32967) suffered from substantial patient delay (13320) and nurse workload spikes (1065).

## What Failed
With only 13 rooms and 3 operating theaters, resource contention is acute. Shifting patients to earlier days to reduce delay caused nurse workload overages on peak days, while greedy room reallocation broke nurse coverage (H9).

## What Worked
The coupled solver (`how-we-built-it/IHTP_Polisher.cpp`) conducted coordinated patient admission advancement paired with nurse workload leveling. Advancing feasible surgeries reduced PatientDelay from 13320 to 13125 (-195), while Kempe-chain nurse balancing reduced ExcessiveNurseWorkload from 1065 to 968 (-97), achieving Total cost = 32675 with zero violations across all 9 hard constraint categories (strict improvement of -292 points vs live BKS 32967).
