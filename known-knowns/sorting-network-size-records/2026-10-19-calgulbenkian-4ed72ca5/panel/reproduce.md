context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, sortnet-n53-s422-d19

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to it); every listed file reported OK. I then worked only on a private copy of the package. No network was used.

## Definition (quoted)
Claim: "object/N53_S422_D19.txt is a list of 422 comparators on 53 channels (minimum to the lower wire) whose greedy layering has depth 19 and which sorts all 2^53 binary inputs, so that its (size, depth) pair (422, 19) is not dominated by any pair listed for n = 53 in Dobbelaere's extended table (listed: (411, 22), (412, 21), (414, 20), (423, 19))."
Success criterion (quoted, relevant clauses): "a list of comparators (i,j), 0 <= i < j < n, standard min-to-i form ... that sorts all 2^n binary inputs (0-1 principle), checked exhaustively"; (c) "its (size, depth) pair is not dominated by any pair listed for that n, i.e. no listed (s', d') has s' <= size and d' <= depth"; depth is the greedy layering depth.
Note: 0-1 enumeration of 2^n inputs is infeasible at these n, so the sorting proof must be a complete method; I used exact reachable-set propagation.

## My method (my own checker, written from scratch before opening verify-it-yourself/, not shipped in this package)
Complete method, no sampling: maintain a partition of the wires into groups, with the exact set of 0/1 patterns reachable on each group from ALL 2^n inputs (an untouched wire starts as the set {0,1}, and groups that have never been joined by a comparator are independent, so the full set of reachable vectors is the product of the group sets). A comparator inside a group maps each pattern and the set is deduplicated; a comparator joining two groups first forms the explicit product of the two sets. Comparators on disjoint wires commute, so I process them in a greedy order that respects the order on each wire (always the ready comparator with the smallest resulting set). Final test: the full reachable set must consist only of the sorted patterns 0..01..1 (minimum to wire 0), n+1 of them at most. Because the sets are exact images of the full input space, this is a proof that the network sorts all 2^n binary inputs, hence (0-1 principle) all inputs. Format checks: header size equals the number of lines, every comparator has 0 <= i < j < n. Depth by greedy ASAP layering. I also report comparators that are the identity on every reachable pattern at their position (redundant ones).
Command: (own checker, run on object/<file>)
Real output (its output, progress lines removed; the largest intermediate set shown is the peak of the exact state):
n 53 size 422 distinct comparators 285 depth (greedy ASAP) 19
SORTS | reachable output patterns: 54 (a sorter has exactly 54 ) | largest intermediate set: 3778 | bad: []
redundant comparators (identity on every reachable pattern at its position, order of my greedy schedule): 0 indices []
        0.45 real         0.27 user         0.04 sys
            33275904  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                2700  page reclaims
                  35  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                  11  voluntary context switches
                1338  involuntary context switches
          2384458536  instructions retired
           987121095  cycles elapsed
            26952040  peak memory footprint

## Controls (own controls script, run on object/<file>; not shipped in this package)
control 1 (positive): Batcher 64 with top wires removed -> 38 wires: size 289 depth 21
  verdict (ok, patterns, peak, bad): (True, 39, 288, [])
  control 2 (negative): delete comparator #68 -> sorts? False
  control 2 (negative): delete comparator #32 -> sorts? False
  control 2 (negative): delete comparator #130 -> sorts? False
  control 2 (negative): delete comparator #60 -> sorts? False
  control 2 (negative): delete comparator #253 -> sorts? False
  control 2 (negative): delete comparator #230 -> sorts? False
  control 2 (negative): delete comparator #241 -> sorts? False
  control 2 (negative): delete comparator #194 -> sorts? False
negative controls that fail: 8 of 8
object minus comparator #0 -> sorts? False
object minus comparator #211 -> sorts? False
object minus comparator #421 -> sorts? False
Positive control: Batcher's odd-even merge sort on 64 wires cut to 38 wires passes; negative controls: deleting any one of 8 random comparators of that network, and deleting the first, middle or last comparator of this object, are all reported as not sorting. A calibration on a Dobbelaere network of the same n could not be done because the folder does not contain one; the Batcher control exercises the same code path (large merges).

## Size, depth and the table pair
table row: 53 (411, 22) (412, 21) (414, 20) (423, 19) 285…411 11…19 Size ubound: Van Voorhis (4,4) merge, depth
listed pairs: [[411, 22], [412, 21], [414, 20], [423, 19]] | n in table: 53 | page says: updated on Tue Oct 13 20:10:24 2026
pair (422, 19) dominated (some listed s'<=s and d'<=d)? False []
equal to a listed pair? []
improves one coordinate while matching other: [[423, 19]]
(Only the saved row of the live table, as recorded in the-record-we-beat/listed.json, was used; I did not fetch anything and I do not judge currency.)
Not reproduced here, by design of this check: the check that the pair does not follow from a listed network by removing wires needs the listed networks themselves, which are not in the folder. I report it as not checked by reproduce.

## Author's checker (run only after mine)
sha256 matches INDEX.csv (4ed72ca5cb966a3d915e0769777a0750e0a2b98aa5109f5efe81db821e374a12)
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
It reports the same size, depth and SORTS result (and the same largest-state magnitude order); no mismatch.

## Verdict
The network is well-formed, has the stated size and depth, and sorts all 2^n inputs by an exact complete method; the pair is not dominated by the saved listed pairs. Deterministic (no randomness in the checks; only the negative-control sample is seeded).

pass: true
