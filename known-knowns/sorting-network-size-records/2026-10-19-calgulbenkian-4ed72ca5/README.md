# [claim] sorting-network-size-records: n=53 pair (422, 19) not dominated by live table (partial p1)

## What

A standard-form network on 53 channels with 422 comparators and greedy depth 19 that sorts all 2^53 binary inputs (proved by exact reachable-set propagation), whose pair (422, 19) is non-dominated by the pairs [(411, 22), (412, 21), (414, 20), (423, 19)] on the Oct 13 2026 table and dominates the listed pair (423, 19), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`. The script first verifies the object file against `SHA256SUMS`, then runs the checker, then a negative control that must be rejected.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Dobbelaere extended sorting-network table, row n = 53 | n = 53, listed (size, depth) pairs | (411, 22), (412, 21), (414, 20), (423, 19) | https://bertdobbelaere.github.io/sorting_networks_extended.html | 2026-10-19T04:32:30Z (HTTP 200, page sha256 5515e5d7...; the page states it was updated Tue Oct 13 20:10:24 2026); again 2026-10-19T05:26:55Z (novelty skeptic) and 2026-10-19T08:25:31Z (packager), same sha256 |
| This package | n = 53, (size, depth) | (422, 19) | object/N53_S422_D19.txt | checked by verify-it-yourself/check_sorter.py |

The table value used in `INDEX.csv` is (411, 22), (412, 21), (414, 20), (423, 19), from the first fetch (2026-10-19T04:32:30Z). Snapshot metadata with HTTP status and page checksum: `the-record-we-beat/README.md`; a later re-check of the pages used for the credits: `the-record-we-beat/SOURCE_RECHECK.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- This is the enumerated partial win p1 only, for n = 53, which is outside the 13 to 32 range of the target's main criterion. Nothing is claimed for any other n, and no claim is made against the overall best size or best depth for n = 53.
- The pair (422, 19) is not dominated by any listed pair ((411, 22), (412, 21), (414, 20), (423, 19)) and dominates the listed pair (423, 19), improving it by 1 comparator fewer than (423, 19) at the same depth. It does not have fewer comparators than the smallest listed size (411) and does not have smaller depth than the smallest listed depth (19); it is a new point on the Pareto list, not a new smallest network or a new shallowest network.
- Whether the pair is already implied by a larger listed network was tested only by wire-deletion reductions of listed networks: top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators. Deeper reductions were not tried. The panel's tests agree that none of the reductions tried gives this pair, but they are searches, not a proof that no derivation exists.
- The comparison is with the table page of Oct 13 2026 as fetched on 2026-10-19. Newer networks elsewhere (the SorterHunter issue tracker, mailing lists, Google Scholar) were not searched; the SorterHunter repository and arXiv showed nothing newer to the novelty skeptic.
- The panel's three skeptics are Claude Code subagents of one model family; the object's builder (Gemini, Argon) is a different family. The skeptics were given only the claim folder. This is not peer review.
- The panel checked the object file as shipped (sha256 4ed72ca5cb966a3d915e0769777a0750e0a2b98aa5109f5efe81db821e374a12).

Gate notes, as written by the gate (`panel/gate.md`), in plain words:

- Object: object/N53_S422_D19.txt, sha256 4ed72ca5cb966a3d915e0769777a0750e0a2b98aa5109f5efe81db821e374a12.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.

## Credits

- **Bert Dobbelaere**, the sorting-network tables (extended page, n = 2 to 64, the page named in the-record-we-beat/): https://bertdobbelaere.github.io/sorting_networks_extended.html, with the reduced page at https://bertdobbelaere.github.io/sorting_networks.html. The fetched page names him as its author and gives a contact address for contributions; the table compared against and the source of the listed (size, depth) pairs.
- **SorterHunter** (https://github.com/bertdobbelaere/SorterHunter), the program the table credits for most of its networks, and whose headers the contributor's optimiser source includes. The table page also credits other contributors network by network (see the page); we name none of them because none was a source of the listed pairs we compared against beyond what the page's own table shows.
- The search code and pre-registration: the contributor's AI search agent (Gemini, Argon), under the contributor credit `calgulbenkian`. The checker in `verify-it-yourself/` was written by the orchestrator's triage agent from the definitions (0-1 principle, exact reachable-set propagation).
