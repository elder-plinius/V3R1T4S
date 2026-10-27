# How We Found It — `ihtp-ihtc2024-hidden-m-instances-upper-bounds` (`m21`)

Contributor text, unverified.

## Brief & Observation
Competition instance m21 is a 14-day benchmark with 46 nurses, 21 rooms, 234 patients, 13 occupants, 9 surgeons, and 11 operating theaters. In the BKS solution (cost 25157), room skill mismatches (2070) and nurse continuity penalties (1458) were the dominant targets for optimization.

## What Failed
Individual shift nurse swaps disrupted continuity in the 21 rooms, creating offsetting penalties that nullified skill improvements. Direct patient transfers between rooms triggered gender-mix (H1) or capacity (H7) violations.

## What Worked
The C++17 solver (`how-we-built-it/IHTP_Polisher.cpp`) deployed synchronized 2-shift Kempe chains (`NRA-CONT`) to align nurse skill levels with room requirements. This reduced RoomSkillLevel from 2070 to 1930 (-140), ContinuityOfCare from 1458 to 1375 (-83), resulting in Total cost = 24934 with zero hard violations across all 9 categories (strict improvement of -223 points vs live BKS 25157).
