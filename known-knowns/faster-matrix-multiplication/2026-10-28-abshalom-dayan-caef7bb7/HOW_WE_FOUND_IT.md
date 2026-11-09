# How we found it (contributor text, unverified)

An earlier run (2026-10-25) cut odd LITA cubes (Khoruzhii, Serafin, Gelss, Pokutta) along one direction and then used
the "flat" (consensus) absorption on the result, and then scanned further cuts of the best children. LITA's 15x15x15
rank-1977 scheme, cut once, gave a 14x15x15 scheme of rank 1836, byte-identical to the object of our open pull request #791 (https://github.com/elder-plinius/V3R1T4S/pull/791). One cut of that along the column index gave a 14x15x14 scheme of rank 1709 (not claimed; the same rank as our open pull request #752 for <14,14,15>, https://github.com/elder-plinius/V3R1T4S/pull/752, but a different scheme: #752 cuts the inner index), and a scan of cuts of the 1709 along the same index found two cuts (numbers
8 and 30 of the scan) that leave 1644 terms for <14,15,13> after absorption. The scan is not shipped; the
object here is cut 8.

What failed before (earlier runs by this contributor, not included in this package): cuts of this repository's merged
13x15x15 rank-1762 scheme down to this format gave only ties at 1645, and a plateau walk with one- and two-flip screens
on the merged 1645 found no reduction. What worked was cascading cuts from a
published LITA parent instead of from the merged record.

This run did no search. It re-verified the stored object with the package checkers and an independently written
checker, rebuilt it byte for byte from LITA's upstream file, re-fetched the four tables and all pull requests, and then
ran the three-skeptic panel.
