# C(20,6,3) <= 70 (explicit covering design), covering-designs-record

## What
The 70-block file C20_6_3_70blocks.txt (sha256 a6c6ddb8...4c6f) is an exhaustively verified (20,6,3) covering design, so C(20,6,3) <= 70, one block below the value 71 in the dmgordo/LJCR GitHub data (re-fetched 2026-10-17T15:01Z), the newest Zenodo LJCR release v1.2, and the live coveringrepository.com (v,k,t) row as hand-read by the operator at 2026-10-17T14:57Z, with no competing value of 70 or less found in a repo-level GitHub/arXiv search of the last 6 months.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED C(20,6,3) <= 70`). Python 3 standard library only; well under a second on a laptop. The check is exhaustive over all C(20,3) = 1140 triples.

## Compared to
- Covering Repository (https://coveringrepository.com/), (v,k,t)-covering designs, cell v=20, k=6, t=3 (m=3): **71** blocks, "Known design", creator Chaoying Dai, Ben Li and Michel Toulouse, source Dan Gordon Covering Repository, date 11/04/2006. Read by hand by the operator in a browser at 2026-10-17T14:57Z. Machine requests to the per-cell pages get a Cloudflare challenge and were never retried or bypassed.
- La Jolla Covering Repository data, dmgordo/LJCR GitHub `coverings/coverdata.json`: C(20,6,3) size **71**, low_bd 64. Fetched 2026-10-17T13:04:00Z, 14:51:09Z and by the panel at 15:00-15:01Z, all HTTP 200, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef. History: 75 (JCD 1996), 72 (Muehl 1997), 71 (Dai, Li, Toulouse 2006).
- Zenodo LJCR v1.2 (record 19735294, 2026-04-24, newest version): **71**. File fetched 2026-10-17T14:51:27Z. Also v1.1 (record 19472830): 71.
- Lower bound: Schonheim L(20,6,3) = 64, so the cell stays open at 64..70.
- Details are in the-record-we-beat/.

## Not claimed
- Not optimality: 70 is the optimum only among unions of orbits of this one A5 subgroup (order 60) of PSL(2,19) acting on PG(1,19). C(20,6,3) is still open (64..70). The search for 69 (local surgery, simulated annealing, capped CP-SAT over subgroups) did not finish, and nothing is excluded.
- Not a new method. Orbit covers under a group action are classical; this is new only as a table entry.
- No claim about any other cell. The same search only tied C(20,12,3)=10 and C(20,12,4)=20.
- The live coveringrepository.com value rests on a human hand read, so no saved page or hash exists for it. The old per-cell LJCR page (ljcr.dmgordon.org) was unreachable (TLS error, not retried), and https://dmgordon.org/covering-designs/ has no per-cell values. The LJCR comparison uses its GitHub/Zenodo data.
- The 6-month GitHub/arXiv search for competing claims was at repo and README level, not code level.

## Credits
- La Jolla Covering Repository, Dan Gordon: https://dmgordon.org/covering-designs/ , https://github.com/dmgordo/LJCR (Zenodo: https://zenodo.org/records/19735294).
- Covering Repository, Giovanni Acerbi: https://coveringrepository.com/
- Previous record (71 blocks): Chaoying Dai, Ben Li and Michel Toulouse (2006). Earlier: Adolf Muehl (72, 1997); D. M. Gordon, G. Kuperberg, O. Patashnik, "New constructions for covering designs", J. Combin. Des. 3 (1995) (75).
- J. Schonheim, On coverings, Pacific J. Math. 14 (1964): the lower bound.
- Google OR-Tools CP-SAT (https://developers.google.com/optimization) for the exact orbit set cover.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
