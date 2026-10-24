# Stable-marriage instance at n=21

> Public value for n = 21: OEIS A357271 a(21) = 3,506,880. This object: 5,400,616 (+54 %). The 5,382,608 profile named below is an unsubmitted intermediate from this workspace.

## What

The complete strict preference profile in `object.prefs` for 21 men and 21 women has exactly 5,400,616 stable matchings, exceeding the independently recounted 5,382,608 stable matchings of `data/prior_n21.prefs` by 18,008 and the freshly fetched OEIS A357271 n=21 composition bound of 3,506,880.

The claim-relative object.prefs is stored here at object/object.prefs. The claim-relative data/prior_n21.prefs is stored at the-record-we-beat/prior_n21.prefs.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Python3 and a C++17 compiler; roughly a minute depending on hardware. Complete enumeration checks every accepted matching for blocking pairs.

## Compared to

| source | n = 21 value |
|---|---|
| OEIS A357271 data line, a(21) (Thurber 2002 composition bound), https://oeis.org/A357271/b357271.txt | 3,506,880 |
| this object | **5,400,616** |

The 5,382,608 profile in `the-record-we-beat/` is an unsubmitted intermediate from this workspace, not a public value.

**Composition statement.** This object is not a composition of known instances; it was found by search. The best lexicographic product of a 3-instance with the published 81- and 85-blocks is 1,842,375 (checked in both orders); the best direct sum of published blocks is 3,419,680 (the order-20 composition bound plus one pair), then 3,127,552 (order 16 plus order 5). Thurber's (2002) own composition operations (his Appendix C) were not recomputed with the newer blocks: we could not access the paper.

## Not claimed

No maximum, result at another size, exhaustive preference search, or n7 optimality assertion.

## Credits

R. W. Irving and P. Leather, The complexity of counting stable marriages (1986); D. Gusfield and R. W. Irving, The Stable Marriage Problem (1989); E. G. Thurber, Concerning the maximum number of stable matchings (2002), https://doi.org/10.1016/S0012-365X(01)00194-7; Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks and Genti Buzi, Improved Hill Climbing for the Stable Marriage Problem (2024), linked through https://oeis.org/A357271. M. Jo's 2026 order-seven preprint motivated the 85 calibration; its optimality claim is not used.

V3R1T4S lane A supplied the earlier rotation-poset counter. Lane X2 supplied the nonrepeating-word construction, word-ideal evaluator, prior profiles and saved random calibration input. Lane X4 supplied the direct arc-consistency counter, the fresh calibration replay and the new nonlocal/routing-style repair search. This one-cell claim starts from the saved preceding n=21 profile and counts the final explicit preferences independently.
