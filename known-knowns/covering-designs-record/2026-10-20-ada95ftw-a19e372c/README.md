# C(35,5,3) <= 713 (explicit covering design), covering-designs-record

## What
The file claim/C35_5_3_713blocks.txt (sha256 a19e372c3611962126c615fd73a79e8c023e2f7369b38aa29f12ca00e2181149) is a (35,5,3) covering design with 713 blocks, verified exhaustively over all 6545 triples, which is strictly smaller than the live coveringrepository.com plain value 732 (read honestly at 2026-10-20T16:39:42Z), the LJCR Zenodo v1.2 value 732 and the dmgordo/LJCR GitHub value 733, with no smaller (35,5,3) value found in an unauthenticated GitHub repository and arXiv search covering the last six months.

(In this package the file is object/C35_5_3_713blocks.txt; it is byte-identical to the panel's claim/C35_5_3_713blocks.txt.)

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED C(35,5,3) <= 713`). Python 3 standard library only; about a second on a laptop. The check is exhaustive over all C(35,3) = 6545 triples.

## Compared to
- Covering Repository (https://coveringrepository.com/), (v,k,t)-covering designs (plain, m=t), cell v=35, k=5, t=3 (m=3): **732** blocks, lower bound 658, "Known design", creator Moshe Milshtein, method Tabu Search started from a 733-block covering previously created by Kleszek, source Dan Gordon Covering Repository, date 13/07/2024. Read with clients that follow the V3R1T4S table-access rule (a User-Agent naming V3R1T4S, no cookies, no retries, no challenged URLs): the site's own search form at 2026-10-20T16:34:25Z and 16:39:42Z, and its public plain-text archive download_archive_vkt.aspx (line `35 05 03 03 732`) at 16:28:59Z, 16:34:28Z, 16:37:43Z and 16:39:59Z, HTTP 200. An earlier read at 16:26:12Z used a browser-like User-Agent and carried a session cookie, so it was withdrawn and is not relied on.
- La Jolla Covering Repository data, Zenodo LJCR v1.2 (record 19735294, 2026-04-24, newest version, confirmed at 16:37:45Z): **732** (Moshe Milshtein, 2024-07-13). File fetched 2026-10-20T13:13:05Z and by the panel at about 16:40Z, HTTP 200, sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87.
- dmgordo/LJCR GitHub `coverings/coverdata.json`: C(35,5,3) size **733** (kleszek, 2017), low_bd 658. Fetched 2026-10-20T12:55:53Z and by the panel at 16:37:44Z and about 16:40Z, HTTP 200, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef.
- Lower bound: Schonheim L(35,5,3) = 658, so the cell stays open at 658..713.
- Details are in the-record-we-beat/.

## Not claimed
- Not optimality. The design is a union of orbits of S5 (order 120) acting on the disjoint union of three of its coset spaces (20 + 10 + 5 = 35 points). An exact MIP proved 713 optimal only within that G-set, not globally. C(35,5,3) is still open (658..713).
- Not a new method. Orbit covers under a prescribed group (Kramer-Mesner style) are classical; this is new only as a table entry.
- No claim about any other cell.
- The old per-cell LJCR page (ljcr.dmgordon.org) was unreachable (TLS error, not retried), and https://dmgordon.org/covering-designs/ has no per-cell values. The LJCR comparison uses its GitHub/Zenodo data.
- The fixed lookup tool's search-form reads have saved pages and sha256s, but the tool does not log the HTTP status line; the HTTP 200 status is carried by the plain archive reads.
- The 6-month GitHub/arXiv search for competing claims was unauthenticated, at repository, tree, README, title and abstract level, not a full-text code grep.

## Credits
- La Jolla Covering Repository, Dan Gordon: https://dmgordon.org/covering-designs/ , https://github.com/dmgordo/LJCR (Zenodo: https://zenodo.org/records/19735294).
- Covering Repository, Giovanni Acerbi: https://coveringrepository.com/
- Previous record (732 blocks): Moshe Milshtein (2024, tabu search) from kleszek's 733 (2017, Wheel Generator). Earlier: Anastasios Tampakis (734, 2011; 752, 2009), Jan de Heer and Steve Muir (735, 2011), Michael Dambmann (784, 2008), LJCR simple construction (815, 2008).
- J. Schonheim, On coverings, Pacific J. Math. 14 (1964): the lower bound.
- E. S. Kramer and D. M. Mesner, t-designs on hypergraphs, Discrete Math. 15 (1976): designs with a prescribed automorphism group.
- Google OR-Tools (https://developers.google.com/optimization) with the SCIP solver for the orbit set cover.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
