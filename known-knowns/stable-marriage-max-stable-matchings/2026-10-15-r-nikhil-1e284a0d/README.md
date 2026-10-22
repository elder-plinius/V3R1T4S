# Stable-marriage instance at n=19

## What

The complete strict preference profile in object.prefs for 19 men and 19 women has exactly 935,662 stable matchings, exceeding the independently recounted 896,068 in data/prior_n19.prefs by 39,594 and the checked OEIS A357271 order-19 composition bound of 637,336.

The claim-relative object.prefs is stored here at object/object.prefs. The claim-relative data/prior_n19.prefs is stored at the-record-we-beat/prior_n19.prefs.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Python3 and a C++17 compiler; roughly a minute depending on hardware. Complete enumeration checks every accepted matching for blocking pairs.

## Compared to

The preceding same-size object has 896068 stable matchings; this object has 935662, a gain of 39594. The weaker public A357271 n19 term is637336, fetched at 2026-10-15T16:49:49.350346+00:00 from https://oeis.org/A357271/b357271.txt. The independent panel checked current comparison sources.

## Not claimed

No maximum, result at another size, exhaustive preference search, or n7 optimality assertion.

## Credits

R. W. Irving and P. Leather, The complexity of counting stable marriages (1986); D. Gusfield and R. W. Irving, The Stable Marriage Problem (1989); E. G. Thurber, Concerning the maximum number of stable matchings (2002), https://doi.org/10.1016/S0012-365X(01)00194-7; Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks and Genti Buzi, Improved Hill Climbing for the Stable Marriage Problem (2024), linked through https://oeis.org/A357271. M. Jo's 2026 order-seven preprint motivated the 85 calibration; its optimality claim is not used.

V3R1T4S lane A supplied the earlier rotation counter. Lane X2 supplied the nonrepeating-word construction, exact word evaluator, prior n19 profile and calibration run. Lane X4 supplied the new multi-move search, resulting n19 object, and independent direct arc-consistency counter. The frozen preference lists use canonical ascending unused tails, rebuilt from the exact discovered word; all counts are independently recomputed on these final bytes.

The present X4 run adds nonlocal crossing slides and routing-style insertion/cascade-repair/reinsertion moves. Its base is the preceding X4 n19 profile, itself extending the X2 construction.
