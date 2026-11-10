# hsp4 N = 81: 81 equal balls in the unit 4-ball, radius 0.254080381791775

## What

From the files alone, the 81 four-dimensional centres in hsp4-81-candidate.txt have feasible radius r* = 0.254080381791775 (mpmath, 50 digits, no tolerance, every centre within 1 - r* of the origin) in the unit 4-ball, exceeding the snapshot Packomania hsp4 table value 0.254058669351 for d=4, N=81 by 2.1712440774903e-05 (above the 1e-10 margin), and are not isometric to the posted hsp4-81 packing (all 3240 sorted pairwise distances differ by more than 1e-8); the live-table, history-page and queue-page clauses depend on the NOVELTY skeptic's re-fetch and carry the unresolved Moki & Julio bundle caveat.

## Check it yourself

From this folder, Python 3 standard library only (about 1 second on a laptop):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (it prints r* to 50 digits, the gain over the table value, the posted packing's radius as a
parser-sanity check, and the maximum sorted-pairwise-distance difference to the posted packing, which must exceed 1e-8).
The checker judges the coordinates by the definition, so a copy of the object with one late digit altered is still a valid
packing above the table value and also prints PASS; SHA256SUMS pins the exact file, and altering a leading digit prints FAIL.

## Compared to

- Table: Packomania, section 4, "hyperspheres in a hypersphere", d = 4 (E. Specht), https://packomania.com/hsp4/hsp4.html
- Cell: N = 81, file https://packomania.com/hsp4/txt/radius.txt, row `81 0.254058669351` (12 decimals)
- Fetched: 2026-10-14 02:40:17 UTC (HTTP 200, sha256 f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f);
  re-fetched unchanged at 2026-10-16T16:29:32Z and by this claim's NOVELTY skeptic at 2026-10-16T16:32:17Z (HTTP 200, panel/novelty.md).
- Page: "Last update: 06-Jul-2025"; History of updates has only 04/05/06-Jul-2025 entries.
- Queue: https://packomania.com/pending-requests.html (2026-10-14 02:40:22 UTC, HTTP 200) lists no hsp4 entry. Caveat required
  by the bank: the category-unspecified "Moki & Julio *many* 4666 candidates" bundle (26-Sep-2026) cannot be resolved; this
  cell must be re-checked against the live table once that bundle leaves the pending list.
- Our value: r* = 0.25408038179177490302490222756670917019602502200718 (50 digits, exact from object/hsp4-81-candidate.txt),
  gain 2.17124407749e-05 over the posted 12-decimal value.

## Not claimed

Not optimality, not a "record" in any sense beyond strictly exceeding the posted value in this table on this date, nothing
about any other N or about hsp5/hsp6. Packomania has not been contacted; whether this packing is listed is the table
owner's decision. This is one of 15 hsp4 rows improved in the same search; each is its own package (one cell per claim). N = 66 is in a separate pull request.

## Credits

- Eckard Specht, Packomania (https://packomania.com/), who built and maintains the hsp4 table and posted the packing we
  improved on ("program hsp4", 2010-2025); our search started from his posted coordinates for N = 81.
- The success criterion and checker definition are the V3R1T4S bank entry `packomania-hyperspheres-hsp4-hsp6`.
- Method: sequential linear programming with a trust region (LPs solved by HiGHS through SciPy), then basin hopping by
  displacing the loosest balls; the D4 lattice of Conway and Sloane ("Sphere Packings, Lattices and Groups", 1988) was
  used by a sibling lens for seeds and ties, not for this cell.
