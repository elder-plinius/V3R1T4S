# The record we beat

Never the page itself; the records below were copied from command output.

## Re-fetch by the NOVELTY panelist (panel/novelty.md)
- URL: https://en.wikipedia.org/w/index.php?title=Percolation_threshold&action=raw (raw wikitext of
  https://en.wikipedia.org/wiki/Percolation_threshold)
- 2026-10-18T05:11:54Z (UTC), one plain curl GET, HTTP 200, 267722 bytes,
  sha256 588b98d38a819a6712a7b3b497a8df7e5a955285ba0b7bc3bace199f2c742ba3 (identical to the run's fetch below).
- Row 23, site column: 0.5720(2) (ref NeherEtAl08).

## The run's fetch (copied from the claim's table/table_record.md)

- URL: https://en.wikipedia.org/wiki/Percolation_threshold (section "2-uniform lattices")
- fetched 2026-10-17T23:58:22Z (UTC), HTTP 200, 2514974 bytes, sha256 of the saved HTML
  63592327dc576ed1ddeafc55c4ab22a8078d25ae3369cb539113f468ca3914bc
- Raw wikitext https://en.wikipedia.org/w/index.php?title=Percolation_threshold&action=raw fetched
  2026-10-17T23:58:23Z, HTTP 200, 267722 bytes, sha256 588b98d38a819a6712a7b3b497a8df7e5a955285ba0b7bc3bace199f2c742ba3
  (identical to the copies fetched 2026-10-16T04:51Z, 2026-10-16T17:16Z and 2026-10-17T00:02Z).
- Request: one plain curl GET per URL, User-Agent "V3R1T4S-research-agent/1.0 (open-notebook percolation threshold check)".

Extracted rows of the "2-uniform lattices" table (raw wikitext lines 1146-1151 and 1153-1158), columns: number,
vertex types, z, zbar, site threshold, bond threshold:

    | 23 |({{frac|1|2}})(3<sup>3</sup>,4<sup>2</sup>) + ({{frac|1|2}})(4<sup>4</sup>) | 5,4 | 4.5 | 0.5720(2)<ref name="NeherEtAl08"/> | 0.45844622(40){{citation needed|date=June 2019}}
    | 22 |({{frac|2|3}})(3<sup>3</sup>,4<sup>2</sup>) + ({{frac|1|3}})(4<sup>4</sup>) | 5,4 | 4 {{frac|2|3}} | 0.5648(2)<ref name="NeherEtAl08"/> | 0.44528611(40){{citation needed|date=June 2019}}

Cell compared against: lattice #23, site threshold 0.5720(2) (Neher, Mecke and Wagner 2008, arXiv:0708.3250, table in
arXiv:0708.3251). Bond threshold of the same row (used for criterion (c)): 0.45844622(40).
Archimedean values used for criterion (c): kagome (3,6,3,6) site 1 - 2 sin(pi/18) = 0.65270364466614 (exact, Wikipedia
"Archimedean lattices" table); (3,12^2) site sqrt(1 - 2 sin(pi/18)) (exact). Calibration values: square site
0.59274605079210 (Jacobsen 2015, arXiv:1507.03027), (3^3,4^2) bond 0.41964035886369(2) (Scullard and Jacobsen 2019,
arXiv:1910.12376), (3^3,4^2) site 0.550213(3) (Suding and Ziff 1999, cond-mat/9811416).

## Literature search by the run (copied from the claim's table/literature_record.md)

Searched 2026-10-17, 23:58Z to about 00:02Z (UTC):
- arXiv API query: https://export.arxiv.org/api/query?search_query=abs:"percolation threshold" AND (abs:uniform OR
  abs:tiling OR abs:"critical polynomial" OR abs:"transfer matrix")&sortBy=submittedDate&sortOrder=descending&max_results=40
  fetched 2026-10-17T23:58:24Z, HTTP 200, 87836 bytes, sha256 a64bb707cfce00c55b93ff55dfa22ab650404ad36bd1d29c188794b9f83edde1.
  40 entries (2007-12 to 2026-08). None reports a site threshold for any two-uniform lattice. Newest: arXiv:2608.09479
  (path percolation), 2605.11310 (random fractional-dimensional lattices), 2603.16167 (hyperuniform Delaunay networks,
  bond), 2507.12229 (Archimedean lattices, site-bond phase diagrams), 2402.10909 (conductivities of tessellations),
  1910.12376 (Archimedean bond thresholds from critical polynomial roots).
- Web search "2-uniform lattice site percolation threshold high precision 2026" and "two-uniform tilings percolation
  thresholds Monte Carlo critical polynomial new values arXiv": no two-uniform site threshold newer than Neher, Mecke
  and Wagner 2008 (arXiv:0708.3250, table in arXiv:0708.3251). Other hits: Lebrecht, Centres and Ramirez-Pastor,
  Physica A 569 (2021) (an empirical site-bond formula checked against the 20 two-uniform lattices, no new
  measurement); Suding and Ziff, cond-mat/9811416 (Archimedean site thresholds); arXiv:2604.21165 (2026, the aperiodic
  hat tile).
- The live Wikipedia table (table_record.md) cites only Neher, Mecke and Wagner 2008 for the two-uniform site column.
