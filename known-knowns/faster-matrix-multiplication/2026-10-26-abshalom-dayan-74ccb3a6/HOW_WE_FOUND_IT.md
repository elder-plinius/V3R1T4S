# How we found it (contributor text, unverified)

This scheme was a by-product of the work that produced the <14,14,15> rank-1709 claim (pull request #752). That run
cut odd LITA cubes (Khoruzhii, Serafin, Gelss, Pokutta) along their own kill direction and used the "flat"
(consensus) absorption on the result. The first cut of LITA's 15x15x15 rank-1977 scheme gave this <14,15,15> scheme of
rank 1836, which was then cut again to reach <14,14,15>. Pull request #752 named the 1836 intermediate but did not
claim it, so this package claims it on its own, as one cell.

What failed before (earlier runs by this contributor, not included in this package): starting from the merged near-record schemes of this repository (for example
the merged <14,15,15> 1842) gave only ties with exhaustive one-flip and two-flip screens. What worked was the
stronger absorber applied directly to the published LITA parent.

This run did no search. It re-verified the stored object with the package checkers and an independently written
checker, rebuilt it byte for byte from LITA's upstream file, re-fetched the four tables and all pull requests, and then
ran the three-skeptic panel.
