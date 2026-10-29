# How we found it (contributor text, unverified)

An earlier run (2026-10-25) cut odd LITA cubes (Khoruzhii, Serafin, Gelss, Pokutta) along one direction and then used
the "flat" (consensus) absorption on the result. One cut of LITA's 13x13x13 rank-1379 scheme, with the pair
e = (1,1,1,1,1,1,-4,1,1,1,1,1,1) on the A side and f = (-1,1,...,1) on the C side, left 1295 terms for <12,13,13>, and
absorption removed 25 more. A fresh-context self-break in that run could not break it, and it was kept as a lead.

Before that, an exploratory probe of one slice of LITA 13^3 plus absorption gave 1275 (reported in our pull request
#708, https://github.com/elder-plinius/V3R1T4S/pull/708), and this repository's matrix multiplication write-up reports
1276 from LITA 13^3 as a near miss; both are above the 1274 bar. The "flat" absorber is what took the cut to 1270.

What failed before (earlier runs by this contributor, not included in this package): starting from near-record
schemes and screening one-flip and same-axis two-flip moves gave only ties on the formats tried. What worked was the
stronger absorber applied directly to a published LITA parent.

This run did no search. It re-verified the stored object with the package checkers and an independently written
checker, rebuilt it byte for byte from LITA's upstream file, re-fetched the four tables and all pull requests, and then
ran the three-skeptic panel.
