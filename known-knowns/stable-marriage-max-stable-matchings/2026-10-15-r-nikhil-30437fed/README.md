# Stable-marriage instance at n=13

> Public values for n = 13: OEIS A357271 a(13) = 6,720; Ong et al.'s instance file 7,123; V3R1T4S #150 7,698 (superseded by this object). This object: 9,836. The 9,796 profile named below is an unsubmitted intermediate from this workspace.

## What

The complete strict n=13 preference profile in `object.prefs` (SHA256 `30437fed4d5de6bf272631b49ae7a94298a2fdefb65c3cd5529df582506c9c56`) has exactly 9,836 stable matchings, exceeding the independently recounted 9,796 stable matchings of `data/prior_n13.prefs` by 40.

The claim-relative object.prefs is stored here at object/object.prefs. The claim-relative data/prior_n13.prefs is stored at the-record-we-beat/prior_n13.prefs.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. Python3 and a C++17 compiler; roughly a minute depending on hardware. Complete enumeration checks every accepted matching for blocking pairs.

## Compared to

| source | n = 13 value |
|---|---|
| OEIS A357271 data line, a(13) (Thurber 2002 composition bound), https://oeis.org/A357271/b357271.txt | 6,720 |
| Ong et al. instance file a357271_1.txt linked from A357271 | 7,123 |
| V3R1T4S known-knowns, merged #150 (superseded by this object) | 7,698 |
| this object | **9,836** |

The 9,796 profile in `the-record-we-beat/` is an unsubmitted intermediate from this workspace, not a public value.

**Composition statement.** This object is not a composition of known instances; it was found by search. n = 13 is prime, so the only products are trivial, and the best direct sum of published or merged blocks is 6,472 (the order-12 composition bound plus one pair); the best composition we know is therefore the merged 7,698 instance itself. Thurber's (2002) own composition operations (his Appendix C) were not recomputed with the newer blocks: we could not access the paper.

## Not claimed

No maximum, result at another size, exhaustive preference search, or n7 optimality assertion.

## Credits

R. W. Irving and P. Leather, The complexity of counting stable marriages (1986); D. Gusfield and R. W. Irving, The Stable Marriage Problem (1989); E. G. Thurber, Concerning the maximum number of stable matchings (2002), https://doi.org/10.1016/S0012-365X(01)00194-7; Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks and Genti Buzi, Improved Hill Climbing for the Stable Marriage Problem (2024), linked through https://oeis.org/A357271. M. Jo's 2026 order-seven preprint motivated the 85 calibration; its optimality claim is not used.

V3R1T4S lane A supplied the rotation-poset reference counter; lane X2 supplied the earlier word construction and n13 comparison profile. A fresh X4 cycle-construction context built arbitrary cyclic moves, independently counted the new profile and found its deterministic suffix description. The parent X4 context supplied an additional independent complete counter, fresh n7 calibration and portable packet.
