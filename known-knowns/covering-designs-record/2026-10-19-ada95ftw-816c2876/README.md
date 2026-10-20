# C(29,5,3) <= 399 (explicit covering design), covering-designs-record

## What
The file claim/C29_5_3_399blocks.txt (sha256 816c287640bc50f50a87d27707aaae2c77ff99c1580a07336a594d3b94a56bbb) is a valid (29,5,3) covering design with 399 blocks, verified exhaustively over all 3654 triples, so C(29,5,3) <= 399, which is 14 fewer than the value 413 shown on 2026-10-19 by the dmgordo/LJCR GitHub data, the Zenodo LJCR v1.2 dataset and the operator's hand read of the live coveringrepository.com plain-coverings row.

(In this package the file is object/C29_5_3_399blocks.txt; it is byte-identical to the panel's claim/C29_5_3_399blocks.txt.)

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED C(29,5,3) <= 399`). Python 3 standard library only; well under a second on a laptop. The check is exhaustive over all C(29,3) = 3654 triples.

## Compared to
- Covering Repository (https://coveringrepository.com/), (v,k,t)-covering designs (plain, m=t), cell v=29, k=5, t=3 (m=3): **413** blocks, "Known design", creator Anastasios Tampakis, method Wheel Generator, source Dan Gordon Covering Repository, date 31/03/2011. Read by hand by the operator in a browser at 2026-10-19T23:43Z. The per-cell values load by JavaScript and the per-cell pages are challenged for machines, so they were never requested by the machine.
- La Jolla Covering Repository data, dmgordo/LJCR GitHub `coverings/coverdata.json`: C(29,5,3) size **413**, low_bd 366. Fetched 2026-10-19T23:02:23Z, 23:45:26Z and by the panel at 23:49:50Z and 23:50:05Z, all HTTP 200, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef. History: 435 (JCD 1996), 424 (Rade Belic 1997), 418 (Dietmar Pree 1998), 415 and 414 (Anastasios Tampakis 2006), 413 (Anastasios Tampakis 2011).
- Zenodo LJCR v1.2 (record 19735294, 2026-04-24, newest version, confirmed by the panel at 23:49-23:50Z): **413**. File fetched 2026-10-19T23:06:16Z.
- Lower bound: Schonheim L(29,5,3) = 366, so the cell stays open at 366..399.
- Details are in the-record-we-beat/.

## Not claimed
- Not optimality. The design is a union of orbits of PSL(2,7) (order 168) acting on 14 + 14 + 1 points, found by a time-capped CP-SAT solve (status FEASIBLE, not OPTIMAL), so 399 is not claimed optimal even within that family. C(29,5,3) is still open (366..399). A capped push to 398 (simulated annealing, a CP-SAT re-solve of the blocks through the fixed point, large-neighbourhood search) found nothing, and nothing is excluded.
- Not a new method. Orbit covers under a group action are classical; this is new only as a table entry.
- No claim about any other cell.
- The live coveringrepository.com value rests on a human hand read, so no saved page or hash exists for it. The old per-cell LJCR page (ljcr.dmgordon.org) was unreachable (TLS error, not retried), and https://dmgordon.org/covering-designs/ has no per-cell values. The LJCR comparison uses its GitHub/Zenodo data.
- The 6-month GitHub/arXiv search for competing claims was at search, title, abstract and README level, not a full-text or code-level grep.

## Credits
- La Jolla Covering Repository, Dan Gordon: https://dmgordon.org/covering-designs/ , https://github.com/dmgordo/LJCR (Zenodo: https://zenodo.org/records/19735294).
- Covering Repository: https://coveringrepository.com/
- Previous record (413 blocks): Anastasios Tampakis (2011, Wheel Generator). Earlier: Anastasios Tampakis (414, 415; 2006), Dietmar Pree (418, 1998), Rade Belic (424, 1997); D. M. Gordon, G. Kuperberg, O. Patashnik, "New constructions for covering designs", J. Combin. Des. 3 (1995) (435).
- J. Schonheim, On coverings, Pacific J. Math. 14 (1964): the lower bound.
- Google OR-Tools CP-SAT (https://developers.google.com/optimization) for the orbit set cover.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
