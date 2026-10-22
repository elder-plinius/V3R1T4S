context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Novelty report: bklc-q4-n163-k11-d104

Role: novelty. Cell: [163,11,104] over GF(4), claimed against the live codetables.de lower bound.

## Primary table (fetched once, honestly)
- http://www.codetables.de/BKLC/BKLC.php?q=4&n=163&k=11 | fetched 2026-10-19T05:15:59Z | HTTP 200 | sha256 447e2d5ee68ef47d162dc8d39301b3739a324a85331159217b79dc95a0db2187
Value read: [163,11] over GF(4): lower bound 103, upper bound 113. The page hash equals the one the triage recorded for the same URL on 2026-10-19T04:35, so the cell was unchanged between the two fetches. The claim d = 104 is strictly greater than the lower bound 103 and at most 113.

## Shared sources (fetched once for the whole group, kept as notes)
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-binary-linear | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 904f233ba9fe62d5cfda8003313ed80b431e4f461c65bb3448a86fd3f04f308f
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-qubit-upper-bounds-n101-256 | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 d6c01566c6a9f0e61760f975304955861d84aeeb2efb1fe32adce5b664882ce9
- Pull requests: a snapshot of all V3R1T4S pull requests (titles and bodies), fetched 2026-10-19T04:30:31Z, was used instead of the api.github.com pulls pages, to spare the shared quota. 473 pull requests were scanned: every title for the target, and every title and body for the cell's own parameters (a regular-expression search for the cell, results below).
- TROPHY_CASE.md (text dated 2026-10-10 to 2026-10-12) lists six result families (graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench) and two cipher commitments. It has no row for a codetables.de table, so it holds no competing value for this cell.
- Merged folders for the target (listing above): binary-linear has three merged folders (the 2026-10-14 and 2026-10-15 binary [173,17,72], [175,25,61], [213,26,77] filings, all q = 2 lower bounds at other cells); the qubit-upper-bounds target has 52 merged folders by one other contributor.
- arXiv (4 queries plus the one named work). Query 1 (quaternary linear codes, new): 12 entries, newest 2609.21601 (Z4 quasi-cyclic codes) and 2605.14603 (Z4 codes with small Plotkin defect); none gives a GF(4) linear code with these parameters. Query 2 (linear programming bound, linear codes, nonexistence) returned zero entries (the server found nothing for that exact wording; not retried, the four-query allowance was then spent). Query 3 (quantum, upper bound, linear programming, stabilizer): 9 entries, the relevant ones 2610.09900 (Quantizing Delsarte Theory, general theory, no table cells) and 2601.15446 (check-weight-constrained codes, bounds for weight-limited checks, not the generic table). Query 4 (quantum codes, new, codetables): 3 entries, none newer than 2021. The named work 2609.37056 (LinCodeEvolve) is about BINARY linear codes and lists seven binary codes of length 172 to 200, so it cannot concern GF(4), GF(5), GF(7), GF(8), GF(9) or qubit cells.

## Own exact check that the claimed value is real
I wrote my own enumerator from the definition (not shipped in this package: GF(4) symbols as two bit planes, all 4^k nonzero messages by a binary reflected Gray code, weight = popcount of the union of the planes). Output:
k=11 n=163 nonzero messages=4194303 min weight=104 count_at_min=7956
zero-weight nonzero messages (rank deficiency indicator)=0
A rank-deficient generator would give zero-weight nonzero messages; there are none, so the rank is 11 and the minimum distance is exactly 104, with 7956 minimum-weight words (this matches the author's and the triage's count).

## Derivation and propagation
This is the refile of closed pull request 101 (title fragment 28103164 matches the object's sha256 prefix), closed unmerged in the 2026-10-14 bulk close; under the contributor's review ruling R1 that is an earlier filing of the author, reported here and not counted against the cell. The pull-request search finds no other value for this cell; the only hit is pull request 101 itself. 

## Pull requests, TROPHY_CASE, literature
- Pull-request search (title and body, cell parameters; in the snapshot of all V3R1T4S pull requests): only closed pull requests 90 to 101 of the same contributor (2026-10-14 bulk close, the contributor's review ruling R1); merged 142, 158, 163 are binary (q = 2) lower bounds at other cells and do not touch GF(4). No open pull request from another contributor concerns a GF(4) cell.
- arXiv: no GF(4) linear-code record with these parameters in the four queries (see shared sources). unresolved: the arXiv search was four generic queries, not a parameter-specific search of every 2024 to 2026 quaternary-code paper; a paper that lists a [n,k,d]_4 code of this size would most plausibly appear in the Magma-based QC/QT literature, which I could not exhaust.

Answers to the open questions that concern novelty:
1. Under ruling R1 a refile of a bulk-closed filing is judged like any other claim; I judged it on the live table, the pull requests and arXiv, as for any claim.
2. Cells filed in earlier closed pull requests are punctures or shortenings of this code; they follow from it, not the other way round, so they do not affect this cell.
3. My own enumeration agrees (104, 7956 words); same enumeration idea.
4. No newer arXiv claim found (see unresolved line).
5. Nothing further known.

unresolved: the Magma-generated Brouwer and Grassl tables carry no later data than the page fetched; whether an unpublished or non-arXiv code exists for this cell cannot be settled from public sources.

novelty: PASS (with the unresolved literature caveat above)
verdict: Exact d = 104 (my enumeration) beats live lower bound 103 and is not derivable from any live, merged, open or batch value; the earlier closed pull request 101 is the author's own bulk-closed filing (ruling R1).
pass: true
