# [claim] sorting-network-size-records: n=57 pair (458, 20) not dominated by live table (partial p1)

## What

A standard-form network on 57 channels with 458 comparators and greedy depth 20 that sorts all 2^57 binary inputs (proved by exact reachable-set propagation), whose pair (458, 20) is non-dominated by the pairs [(454, 21), (461, 20)] on the Oct 13 2026 table and dominates the listed pair (461, 20), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 1.5 to 3 minutes; the check needs about 2 GB of memory at its peak.
- **Expected last line**: `ALL CHECKS PASS`. The script first verifies the object file against `SHA256SUMS`, then runs the checker, then a negative control that must be rejected.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Dobbelaere extended sorting-network table, row n = 57 | n = 57, listed (size, depth) pairs | (454, 21), (461, 20) | https://bertdobbelaere.github.io/sorting_networks_extended.html | 2026-10-19T04:32:30Z (HTTP 200, page sha256 5515e5d7...; the page states it was updated Tue Oct 13 20:10:24 2026); again 2026-10-19T05:26:55Z (novelty skeptic) and 2026-10-19T08:25:31Z (packager), same sha256 |
| This package | n = 57, (size, depth) | (458, 20) | object/N57_S458_D20.txt | checked by verify-it-yourself/check_sorter.py |

The table value used in `INDEX.csv` is (454, 21), (461, 20), from the first fetch (2026-10-19T04:32:30Z). Snapshot metadata with HTTP status and page checksum: `the-record-we-beat/README.md`; a later re-check of the pages used for the credits: `the-record-we-beat/SOURCE_RECHECK.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- This is the enumerated partial win p1 only, for n = 57, which is outside the 13 to 32 range of the target's main criterion. Nothing is claimed for any other n, and no claim is made against the overall best size or best depth for n = 57.
- The pair (458, 20) is not dominated by any listed pair ((454, 21), (461, 20)) and dominates the listed pair (461, 20), improving it by 3 comparators fewer than (461, 20) at the same depth. It does not have fewer comparators than the smallest listed size (454) and does not have smaller depth than the smallest listed depth (20); it is a new point on the Pareto list, not a new smallest network or a new shallowest network.
- Whether the pair is already implied by a larger listed network was tested only by wire-deletion reductions of listed networks: top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators. Deeper reductions were not tried. The panel's tests agree that none of the reductions tried gives this pair, but they are searches, not a proof that no derivation exists.
- The comparison is with the table page of Oct 13 2026 as fetched on 2026-10-19. Newer networks elsewhere (the SorterHunter issue tracker, mailing lists, Google Scholar) were not searched; the SorterHunter repository and arXiv showed nothing newer to the novelty skeptic.
- The novelty skeptic's own sorting check stopped early at a state cap for the n = 57, 58 and 60 objects and did not confirm those networks sort; the reproduce skeptic's exact propagation (and this package's checker) did. The sorting proof for this object therefore rests on those two checks, not on three.
- The panel's three skeptics are Claude Code subagents of one model family; the object's builder (Gemini, Argon) is a different family. The skeptics were given only the claim folder. This is not peer review.
- The panel checked the object file as shipped (sha256 e221320e3d190b87782aee7c6753917b43c49196cc567add0ed233c89dbffb4a).

Gate notes, as written by the gate (`panel/gate.md`), in plain words:

- Object: object/N57_S458_D20.txt, sha256 e221320e3d190b87782aee7c6753917b43c49196cc567add0ed233c89dbffb4a.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.

## Credits

- **Bert Dobbelaere**, the sorting-network tables (extended page, n = 2 to 64, the page named in the-record-we-beat/): https://bertdobbelaere.github.io/sorting_networks_extended.html, with the reduced page at https://bertdobbelaere.github.io/sorting_networks.html. The fetched page names him as its author and gives a contact address for contributions; the table compared against and the source of the listed (size, depth) pairs.
- **SorterHunter** (https://github.com/bertdobbelaere/SorterHunter), the program the table credits for most of its networks, and whose headers the contributor's optimiser source includes. The table page also credits other contributors network by network (see the page); we name none of them because none was a source of the listed pairs we compared against beyond what the page's own table shows.
- The search code and pre-registration: the contributor's AI search agent (Gemini, Argon), under the contributor credit `calgulbenkian`. The checker in `verify-it-yourself/` was written by the orchestrator's triage agent from the definitions (0-1 principle, exact reachable-set propagation).
