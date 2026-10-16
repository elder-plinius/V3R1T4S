# The record we compared against (snapshot record, not the page itself)

- Page: Wikipedia, "Percolation threshold", https://en.wikipedia.org/wiki/Percolation_threshold, section
  "2-uniform lattices".
- Fetch used by the panel (NOVELTY skeptic, one plain GET through the run's shared fetch helper): 2026-10-16T07:52:05Z,
  HTTP 200, 2514902 bytes, sha256 2f44ce4065839fa2baf1c1655cdcf5aa40e21fcdb7cdabf69287093e0fd27e95. Byte-identical
  (`cmp`) to the claimant's own fetch at 2026-10-16T06:07:21Z (same sha256). The page then said "This page was last
  edited on 16 October 2026, at 04:25" (wgRevisionId 1380509084).
- Response headers: not recorded (the fetch helper does not record response headers).
- Extracted row #22 (tags stripped): `22 ( 2 ⁄ 3 )(3 3 ,4 2 ) + ( 1 ⁄ 3 )(4 4 ) 5,4 4 2 ⁄ 3 0.5648(2) [ 74 ] 0.44528611(40) [ citation needed ]`
  i.e. lattice (2/3)(3^3,4^2) + (1/3)(4^4), z = 5,4, z-bar = 4 2/3, site 0.5648(2) [ref. 74 = Neher, Mecke and Wagner],
  bond 0.44528611(40) [citation needed].
- The cell compared against: row #22, bond column: `0.44528611(40) [citation needed]` (value 0.44528611, stated
  one-sigma 4.0e-7). The string 0.4452 appears nowhere else on the page.
- Provenance of the cell (NOVELTY skeptic, from the page history through the MediaWiki API): the row's bond value
  first appears as 0.44529(5) in revision 190337879 (2008-02-10) and as 0.44528611(40) from revision 302924272
  (2009-07-19), both citing an unpublished reference: Hang Gu and R. M. Ziff, "Percolation thresholds of 2-uniform
  lattice", "To be published", 2007. That reference is no longer on the page; the cell carries a "citation needed"
  tag dated June 2019. The panel found no publication of that work.
- cell.json holds the same record in machine-readable form (the checker reads its table_value).
