context: Claude Code subagent, fresh context [Sonnet 5.5]

# novelty report: sortnet-n57-s458-d20

Claim: a sorting network on 57 channels with 458 comparators and greedy depth 20. Target sorting-network-size-records, partial win p1 (a Pareto size/depth improvement for some n in 33..64 on the extended table) and success criterion (c).

Read from the package: README.md, INDEX.csv, the-record-we-beat/listed.json. I recomputed size and depth of the object file (header "57 458", 458 comparators, all i less than j less than 57, greedy ASAP depth 20), which match the claim.

## Common sources (fetched once for the whole review group; each source is given with its fetch time, HTTP status and sha256)

- Fetch method: plain curl with the honest client string, one request per URL, no retries. Times are UTC. Where a fetch needed a deviation it is stated under unresolved.
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-19T05:27:03Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments. No row for sorting networks.
- known-knowns listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-19T05:27:03Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty directories. There is no directory for sorting-network-size-records.
- Pull requests: I used a snapshot of all V3R1T4S pull requests (titles and bodies), 473 entries, fetched 2026-10-19T04:30:31Z, instead of the api.github.com pulls pages, which I did not fetch. I read every title and searched every body for the target ids and keywords (sorting network, Dobbelaere).
- The contributor's review ruling R1: closed pull requests from the 2026-10-14 bulk close by the same contributor (#65-#120) are the author's own earlier filings, not competing values. They are reported, not counted against a cell.

## Primary table (sorting networks)

- Dobbelaere extended table: https://bertdobbelaere.github.io/sorting_networks_extended.html, fetched 2026-10-19T05:26:55Z, HTTP 200, sha256 5515e5d7862caaf31058225ff215850c1987704f6bcd9b5920590e2478d41a53 (same sha256 as the page the triage agent fetched at 2026-10-19T04:32:30Z). The page states: "Page updated on Tue Oct 13 20:10:24 2026". I parsed every network on the page (122 listed networks for n = 2..64; each parsed size matched its label) and the Pareto lists.
- Rows read from the page (listed (size, depth) pairs): n=57: (454,21) (461,20).
- SorterHunter repository (the source of most listed networks): pulls page https://github.com/bertdobbelaere/SorterHunter/pulls, 2026-10-19T05:27:04Z, HTTP 200, sha256 623400ea1fd28f4f0bc13f4dadf4bf4f7b6385546a90c0f8fbdcedcc58a7e855: one open pull request, titled "Added Ktop search" (a search option, no network). Commits (https://api.github.com/repos/bertdobbelaere/SorterHunter/commits?per_page=30, 2026-10-19T05:27:05Z, HTTP 200, sha256 cf73b5edd59e4317ef09a9d55ac134ee3065349763d670eccf25d482f8faa651): newest 2026-10-18T15:20:29Z "Updating average swap count page" (improvements to the average-swap-count page for sizes 18 to 63, not the size/depth table); 2026-10-13T19:24:56Z "Contributions ... 5 improvements for sorters of sizes 38, 43, 45, 46 and 53", which is before the table page's 20:10:24 update stamp, so it is already in the table I compared with. No commit after the table update touches the size/depth table.
- Literature (arXiv export API, https, query 2 of 4, 2026-10-19T05:32:38Z, HTTP 200, sha256 329126b78bb7950c25f08bfe0d0a6bdd0b31da83979742ff4d913e961dafe736): sorting networks with size or depth, newest first. The only recent sorting-network record paper is 2511.04107 "Depth-13 Sorting Networks for 28 Channels" (2025-11-06); nothing in 2026 gives size or depth networks for 38 to 60 channels. EinsteinArena home page (https://einsteinarena.com/, 2026-10-19T05:40:57Z, HTTP 200, sha256 f5c8fff10812b9c529aec39e0f9922c564c7bb3a1cbfb872ec5ef72a87258094) lists only a 16-input sorting problem.
- Pull requests in this repository on sorting networks: none (title and body search of the pull-request snapshot). The target has no merged known-knowns directory.

## My own propagation test (PR #350 rule: not implied by a listed network by removing wires)

Scripts: my own (parser, wire removal with untangling, depth, search, pruning and an exact check; not shipped in this package). Method: for every listed network with m channels (m = n+1 .. n+8 without pruning, m = n+1 .. n+4 with pruning), repeatedly fix any one input wire to 0 or to 1 (not only the top or bottom wire), delete the comparators on its path and untangle to standard min-to-low form, m minus n times, keeping a beam of the smallest results (beam 6 and beam 30). Wire removal was validated by exhaustive 0-1 checks of the results of removing every wire (both constants) from the listed 10, 12 and 14 channel networks, and by random tests for 16 channels. For results within 4 comparators of the claim I then tried to delete comparators: candidates were comparators whose removal survived 262,144 random 0-1 inputs, and every subset of up to 8 candidates was tested with my own exact sorting check (exact 0-1 reachable-set propagation over connected wire groups). This is a heuristic search, not a proof that no reduction exists; it complements the triage agent's different test (top and bottom wires only, 708 reductions).

## This cell

Live row n=57: listed pairs (454,21), (461,20).

Non-domination check of the claimed pair (458,20) against every listed pair: (454,21): does not dominate (depth larger); (461,20): does not dominate (size larger).
Result: not dominated by any listed pair. It weakly dominates (461,20): same depth 20, size 458 is less than 461, so it replaces that frontier point.

Propagation (wire removal and pruning): best (size, depth) I could reach for n=57 from listed networks of other widths: 461 at depth 20 (from the 60-channel size-489 depth-20 network), which equals the listed (461,20); no comparator could be pruned. Gap to the claimed size: 3 comparator(s). No reduction I found dominates or equals the claimed pair.

Open pull requests and merged work: no other pull request names sorting networks or this n. The author has no earlier filing for this cell (the closed pull requests #65-#105 cover other targets).

## Open questions for the panel, as far as they concern novelty

1. Does a pair that is not dominated, and that matches one listed coordinate while improving the other, count as a Pareto improvement under p1? Yes for novelty. Here the claimed pair weakly dominates a listed pair of the live table and is strictly better in one coordinate (see the cell table), so it removes that pair from the Pareto list; it is not only an incomparable point. It also satisfies success criterion (c) (no listed pair has size at most and depth at most the claimed pair).
2. Is the triage propagation test sufficient? It is a reasonable test; I ran an independent and broader one (any wire, both constants, beam search, plus exact comparator pruning). The best implied pair I reached is shown in the cell table; in no case does it reach the claimed size at the claimed depth. Residual risk: both tests are searches, not exhaustive over all reductions.
3. Is the page state of 2026-10-13 the one to compare with, and has anything newer appeared? My fetch of 2026-10-19T05:26:55Z has the same sha256 as the triage fetch; the SorterHunter repository has no later size/depth contribution; arXiv shows no newer network.

unresolved: Google Scholar and the SorterHunter issue tracker were not searched. My exact sorting check ended early (state cap) for the n=57, 58 and 60 objects, so I did not independently confirm that those three networks sort; whether each claimed network sorts is for the reproduce role. Contributions posted to places other than the SorterHunter repository, this repository's pull requests and arXiv (for example private mailing lists) cannot be seen from here. A better pair could exist that I could not see.

novelty verdict: the pair (458,20) is new against the live table fetched 2026-10-19T05:26:55Z (page stamp 2026-10-13), against the SorterHunter repository and open pull requests, and against my wire-removal test; limits as stated above.

pass: true
