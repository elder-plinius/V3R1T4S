# How We Found It — `ihtp-ihtc2024-upper-bounds` (`i23`)

Contributor text, unverified.

## Brief & Observation
Public benchmark instance i23 spans a 28-day horizon with 55 nurses, 26 rooms, 426 patients, 43 occupants, 5 surgeons, and 5 operating theaters. In the published BKS (cost 37542), the primary soft costs were continuity-of-care penalties (7910) and nurse workload imbalances (959).

## What Failed
With 426 patients competing for only 5 operating theaters and 26 rooms over 28 days, theater scheduling is exceptionally tight. Moving surgeries between days routinely violated surgeon limits (H3) or theater capacity (H4).

## What Worked
Using `how-we-built-it/IHTP_Polisher.cpp`, we preserved the feasible surgery schedule and targeted nurse-to-room allocations using multi-shift Kempe chains (`NRA-CONT`). Reallocating nurses over contiguous multi-day stay blocks reduced ContinuityOfCare from 7910 to 7675 (-235) and ExcessiveNurseWorkload from 959 to 883 (-76), yielding Total cost = 37231 with zero hard violations across all 9 categories (strict improvement of -311 points vs live BKS 37542).
