# How we found it

Contributor text, unverified.

An agent working for the contributor started from Perminov's rank-38 <3,4,4> schemes. It walked the space of rank-38 schemes with flip-graph moves plus isotopy moves (elementary row and column operations on the three factor matrices, kept ternary), and after each move ran Perminov's ternary addition reducer to get a reduced addition count. Plain flips returned to the same basins (best 132 from the cr133 start, never below the 125 baseline); adding isotopy moves opened new basins, and one reached 124 additions. The same method first lowered <2,4,7> to 167, but an open pull request already covered that format, so it is not part of this package.

Before claiming, the Perminov listing, reduced_known.json, README, CHANGELOG, the Lille page, COVERAGE.md and fmm_sota.json were fetched once each, and all open and closed pull requests of this repository were scanned for a <3,4,4> claim (none).
