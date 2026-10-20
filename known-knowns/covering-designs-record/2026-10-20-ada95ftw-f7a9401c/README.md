# C(36,5,3) <= 812 (explicit covering design), covering-designs-record

## What
The 812 blocks in claim/object/C36_5_3_812.txt form a valid (36,5,3) covering design (all 7140 triples covered, 812 distinct 5-subsets of {1..36}), so C(36,5,3) <= 812, which is strictly below the value 821 listed on 2026-10-20 by coveringrepository.com (archive and live search) and by dmgordo/LJCR GitHub coverdata.json, and above the Schonheim bound 756.

(In this package the file is object/C36_5_3_812.txt; it is byte-identical to the panel's claim/object/C36_5_3_812.txt, sha256 f7a9401c9fc3e6db6721b7eee490dbad8a7cb95bf6a9e8d0de9bcf7851da6b23.)

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED C(36,5,3) <= 812`). Python 3 standard library only; about a second on a laptop. The check is exhaustive over all C(36,3) = 7140 triples.

## Compared to
- Covering Repository (https://coveringrepository.com/), (v,k,t)-covering designs (plain, m=t), cell v=36, k=5, t=3 (m=3): **821** blocks, lower bound 756, "Known design", creator Anastasios Tampakis, source Dan Gordon Covering Repository, date 01/01/2009. Read with clients that follow the V3R1T4S table-access rule (a User-Agent naming V3R1T4S or a plain non-browser client, no cookies, no retries, no challenged URLs): the site's own search form at 2026-10-20T23:04:56Z, and its public plain-text archive download_archive_vkt.aspx (line `36 05 03 03 821`) at 22:56:37Z, 23:14:58Z and 23:15:17Z, HTTP 200, the same sha256 each time.
- dmgordo/LJCR GitHub `coverings/coverdata.json`: C(36,5,3) size **821** (Anastasios Tampakis, 2009-01-01), low_bd 756. Fetched 2026-10-20T22:56:38Z and by the panel at 23:15:18Z, HTTP 200, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef.
- La Jolla Covering Repository data, Zenodo LJCR v1.2 (record 19735294, 2026-04-24): **821** (Anastasios Tampakis, 2009-01-01). File fetched 2026-10-20T13:13:05Z, HTTP 200, sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87 (a versioned record; not fetched again).
- Lower bound: Schonheim L(36,5,3) = 756, so the cell stays open at 756..812.
- Details are in the-record-we-beat/.

## Not claimed
- Not optimality. The design is a union of orbits of PSL(2,7) (order 168) acting on the disjoint union of three of its coset spaces (14 + 14 + 8 = 36 points; point stabilisers of order 12, 12 and 21). An exact MIP proved 812 optimal only within that G-set, not globally. C(36,5,3) is still open (756..812).
- Not a new method. Orbit covers under a prescribed group (Kramer-Mesner style) are classical; this is new only as a table entry.
- No claim about any other cell. It is not derived from the same contributor's pending C(35,5,3) <= 713 submission: adding one point to a (35,5,3) covering needs a C(35,4,2) = 105 blocks more, which gives 818, not 812; and for no point p do the blocks avoiding p form a C(35,5,3).
- The old per-cell LJCR page (ljcr.dmgordon.org) was unreachable (TLS error, not retried), and https://dmgordon.org/covering-designs/ has no per-cell values. The LJCR comparison uses its GitHub/Zenodo data.
- The fixed lookup tool's search-form read has a saved page and sha256, but the tool does not log the HTTP status line; the HTTP 200 status is carried by the plain archive reads. A panel reviewer's own search-form read (2026-10-20T23:15:54Z, also 821) did not record how it handled cookies, so it is not relied on.
- The 6-month GitHub/arXiv search for competing claims was unauthenticated, at repository, tree, README, issue, title and abstract level, not a full-text code grep.

## Credits
- La Jolla Covering Repository, Dan Gordon: https://dmgordon.org/covering-designs/ , https://github.com/dmgordo/LJCR (Zenodo: https://zenodo.org/records/19735294).
- Covering Repository, Giovanni Acerbi: https://coveringrepository.com/
- Previous record (821 blocks): Anastasios Tampakis (2009). Earlier: Michael Dambmann (871, simulated annealing, 2008), LJCR simple constructions (889 and 920, 2008).
- J. Schonheim, On coverings, Pacific J. Math. 14 (1964): the lower bound.
- E. S. Kramer and D. M. Mesner, t-designs on hypergraphs, Discrete Math. 15 (1976): designs with a prescribed automorphism group.
- Google OR-Tools (https://developers.google.com/optimization) with the SCIP solver for the orbit set cover.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
