# C(38,6,3) <= 469 (explicit covering design), covering-designs-record

## What
The file claim/C38_6_3_469blocks.txt (sha256 09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b) is a (38,6,3) covering design with 469 blocks, checked exhaustively over all 8436 triples, so C(38,6,3) <= 469, which is strictly below the value 510 shown on 2026-10-20 by the live coveringrepository.com plain table (read with a rule-5-compliant client), the LJCR GitHub data and the LJCR Zenodo v1.2 record.

(In this package the file is object/C38_6_3_469blocks.txt; it is byte-identical to the panel's claim/C38_6_3_469blocks.txt.)

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED C(38,6,3) <= 469`). Python 3 standard library only; well under a second on a laptop. The check is exhaustive over all C(38,3) = 8436 triples.

## Compared to
- Covering Repository (https://coveringrepository.com/), (v,k,t)-covering designs (plain, m=t), cell v=38, k=6, t=3 (m=3): **510** blocks, lower bound 425, "Known design", creator Jan de Heer and Steve Muir, method Private Tools, source Dan Gordon Covering Repository, date 05/06/2010. Read from the site's public archive https://coveringrepository.com/download_archive_vkt.aspx by two single plain curl GETs (User-Agent naming V3R1T4S, no cookies, no retries) at 2026-10-20T16:35:04Z and 16:35:40Z, HTTP 200, sha256 3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7 (`38 06 03 03 510`), and from the site's own search form at 2026-10-20T16:34:13Z (raw response sha256 be283df78172861efedd8a74c45c261049e38136627a5ec5361a263b25f708bc; author and date above come from this row).
- An earlier search-form read (2026-10-20T16:26:03Z) used a browser-style User-Agent and replayed a session cookie, which the V3R1T4S rules forbid. It was superseded and nothing here rests on it; it gave the same 510.
- La Jolla Covering Repository data, dmgordo/LJCR GitHub `coverings/coverdata.json`: C(38,6,3) size **510**, low_bd 425. Fetched 2026-10-20T12:55:53Z and by the panel at 16:35:04Z and 16:35:41Z, HTTP 200, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef. History: 526 (Flavio Perona 2008), 523 (Michael Dambmann 2008), 513 (Jan de Heer and Steve Muir 2009), 510 (Jan de Heer and Steve Muir 2010).
- Zenodo LJCR v1.2 (record 19735294, 2026-04-24, still the newest version on 2026-10-20): **510**. File fetched 2026-10-20T13:13:05Z and by the panel at 16:35:42Z, HTTP 200, sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87.
- Lower bound: Schonheim L(38,6,3) = 425, so the cell stays open at 425..469.
- Details are in the-record-we-beat/.

## Not claimed
- Not optimality. The design is a union of orbits of PSL(2,7) (order 168) acting on 24 + 14 points (coset spaces of Z7 and A4). An exact MIP proved 469 optimal only within that G-set, not globally. C(38,6,3) is still open (425..469).
- Not a new method. Orbit covers under a prescribed group (Kramer-Mesner style) are classical; this is new only as a table entry.
- No claim about any other cell. Deleting a point gives C(37,6,3) <= 468, but that corollary is not part of this submission.
- https://dmgordon.org/covering-designs/ has no per-cell values and points to the GitHub/Zenodo data; the old per-cell LJCR page (ljcr.dmgordon.org) failed to connect (not retried). The LJCR comparison uses its GitHub/Zenodo data.
- The 6-month GitHub/arXiv search for competing claims was at search, title, abstract and README level, and the arXiv part used arxiv.org's own search page because the arXiv API was unreachable (not retried).

## Credits
- La Jolla Covering Repository, Dan Gordon: https://dmgordon.org/covering-designs/ , https://github.com/dmgordo/LJCR (Zenodo: https://zenodo.org/records/19735294).
- Covering Repository: https://coveringrepository.com/
- Previous record (510 blocks): Jan de Heer and Steve Muir (2010, private tools); earlier 513 (Jan de Heer and Steve Muir, 2009), 523 (Michael Dambmann, simulated annealing, 2008), 526 (Flavio Perona, 2008).
- J. Schonheim, On coverings, Pacific J. Math. 14 (1964): the lower bound.
- E. S. Kramer and D. M. Mesner, t-designs on hypergraphs, Discrete Math. 15 (1976): the prescribed-automorphism-group method.
- Google OR-Tools (https://developers.google.com/optimization) with the SCIP solver for the orbit set cover.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
