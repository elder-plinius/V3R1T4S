# How We Found It — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m24`)

Contributor text, unverified.

## Brief & Observation
Competition instance m24 is a hidden 21-day benchmark featuring 78 nurses across 39 rooms, 397 patients, 59 initial occupants, 8 surgeons, and 11 operating theaters. In the published Best Known Solution (BKS cost 30870), elective patient delays (5670) and nurse workload imbalances (1046) were the leading non-scheduling cost drivers.

## What Failed
Direct local search with single-shift nurse swaps failed to reduce ExcessiveNurseWorkload because shifts in heavily occupied rooms triggered cascading skill-level deficits across neighboring wards. Similarly, shifting surgery days for delayed patients repeatedly violated surgeon daily limits (H3) or room capacity (H7).

## What Worked
We deployed the coupled simulated annealing polisher (`how-we-built-it/IHTP_Polisher.cpp`) using multi-shift Kempe chain sweeps (`NRA-CONT`) paired with patient admission date shifts (`SCP-SWAP`). This allowed elective patient delays to be compressed from 5670 to 5355 (-315) and ExcessiveNurseWorkload to be rebalanced from 1046 to 926 (-120). Additional fine-grained nurse allocation reduced ContinuityOfCare from 2314 to 2242 (-72), achieving Total cost = 30363 with zero violations across all 9 hard constraint categories (strict improvement of -507 points vs the live table BKS 30870).
