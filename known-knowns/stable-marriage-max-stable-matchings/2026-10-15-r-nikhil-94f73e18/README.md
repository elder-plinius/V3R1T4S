# Stable-marriage instance at n=23

## What

The complete strict preference profile in `object.prefs` for 23 men and 23 women has exactly 19,305,568 stable matchings, exceeding the supplied preceding same-size profile's 19,290,640 by 14,928 and the historical OEIS A357271 n=23 lower bound of 15,481,956.

The claim-relative object.prefs is stored here at object/object.prefs. The claim-relative data/prior_n23.prefs is stored at the-record-we-beat/prior_n23.prefs.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Python3 and a C++17 compiler; normally a few seconds. The independent reviewer's exact constraint recurrence counts every stable completion. The original full leaf-by-leaf enumerator is also supplied; see RUN_IT_YOURSELF.md and verify-it-yourself/CHECKER_PROVENANCE.md.

## Compared to

The preceding same-size object has 19290640 stable matchings; this object has 19305568, a gain of 14928. The weaker public A357271 n23 term is15481956, fetched at 2026-10-15T18:51:58.356959+00:00 from https://oeis.org/A357271/b357271.txt. The independent panel checked current comparison sources.

## Not claimed

No maximum, result at another size, exhaustive preference search, or n7 optimality assertion.

## Credits

R. W. Irving and P. Leather, The complexity of counting stable marriages (1986); D. Gusfield and R. W. Irving, The Stable Marriage Problem (1989); E. G. Thurber, Concerning the maximum number of stable matchings (2002), https://doi.org/10.1016/S0012-365X(01)00194-7; Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks and Genti Buzi, Improved Hill Climbing for the Stable Marriage Problem (2024), linked through https://oeis.org/A357271. M. Jo's 2026 order-seven preprint motivated the 85 calibration; its optimality claim is not used.

V3R1T4S lane A supplied the earlier rotation-poset counter. Lane X2 supplied the nonrepeating-word construction, word-ideal evaluator, prior profiles and saved random calibration input. Lane X4 supplied the direct arc-consistency counter, the fresh calibration replay and the new nonlocal/routing-style repair search. This one-cell claim starts from the saved preceding n=23 profile and counts the final explicit preferences independently.
The fresh cycle-construction lens identified the unused-pair directed-cycle extension at n13; the parent independently implemented and transferred it to n23, scanning the stated suffix family.
