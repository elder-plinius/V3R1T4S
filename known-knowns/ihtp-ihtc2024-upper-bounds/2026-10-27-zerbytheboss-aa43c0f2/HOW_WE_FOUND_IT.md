# How We Found It (contributor text, unverified)

## Brief & Observation
Public benchmark instance i19 spans 28 days with 52 nurses, 25 rooms, 359 patients, 26 initial occupants, 7 surgeons, and 8 operating theaters. In the published BKS (cost 43852, baseline 43857), 102 elective patients remained unscheduled, incurring an enormous ElectiveUnscheduledPatients penalty of 26250 (weight 250 each).

## What Failed
Simply trying to insert unscheduled elective patients into open operating theater slots failed because surgeon daily surgery limits (hard constraint H3) or room capacity (H7) were breached, or caused severe nurse workload overages.

## What Worked
We utilized the full coupled search engine (`how-we-built-it/IHTP_Polisher.cpp`) to execute a coordinated multi-level move: admitting an additional elective patient by shifting two existing surgery schedules (`SCP-2SWAP`), opening an operating theater slot, and re-optimizing room assignments. Admitting this extra elective patient saved 1000 penalty points on ElectiveUnscheduledPatients (26250 down to 25250). Although this increased PatientDelay by 720 (6675 to 7395) and OpenOperatingTheater by 60 (1860 to 1920), fine-grained nurse Kempe-chain optimization reduced ContinuityOfCare from 7375 to 7225 (-150), RoomAgeMix from 192 to 135 (-57), RoomSkillLevel from 760 to 730 (-30), ExcessiveNurseWorkload from 610 to 590 (-20), and SurgeonTransfer from 130 to 120 (-10), for a net reduction of -487 points (Total cost = 43365, Total violations = 0; -492 vs baseline 43857, -487 vs live table 43852).
