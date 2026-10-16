# Stable-marriage instance at n=13

## What

The complete strict n=13 preference profile in `object.prefs` (SHA256 `30437fed4d5de6bf272631b49ae7a94298a2fdefb65c3cd5529df582506c9c56`) has exactly 9,836 stable matchings, exceeding the independently recounted 9,796 stable matchings of `data/prior_n13.prefs` by 40.

The claim-relative object.prefs is stored here at object/object.prefs. The claim-relative data/prior_n13.prefs is stored at the-record-we-beat/prior_n13.prefs.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Python3 and a C++17 compiler; roughly a minute depending on hardware. Complete enumeration checks every accepted matching for blocking pairs.

## Compared to

The preceding same-size object has 9796 stable matchings; this object has 9836, a gain of 40. The weaker public A357271 n13 term is6720, fetched at 2026-10-15T16:49:49.350346+00:00 from https://oeis.org/A357271/b357271.txt. The independent panel checked current comparison sources.

## Not claimed

No maximum, result at another size, exhaustive preference search, or n7 optimality assertion.

## Credits

R. W. Irving and P. Leather, The complexity of counting stable marriages (1986); D. Gusfield and R. W. Irving, The Stable Marriage Problem (1989); E. G. Thurber, Concerning the maximum number of stable matchings (2002), https://doi.org/10.1016/S0012-365X(01)00194-7; Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks and Genti Buzi, Improved Hill Climbing for the Stable Marriage Problem (2024), linked through https://oeis.org/A357271. M. Jo's 2026 order-seven preprint motivated the 85 calibration; its optimality claim is not used.

V3R1T4S lane A supplied the rotation-poset reference counter; lane X2 supplied the earlier word construction and n13 comparison profile. A fresh X4 cycle-construction context built arbitrary cyclic moves, independently counted the new profile and found its deterministic suffix description. The parent X4 context supplied an additional independent complete counter, fresh n7 calibration and portable packet.
