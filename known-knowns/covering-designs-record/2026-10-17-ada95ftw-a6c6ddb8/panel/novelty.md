# NOVELTY skeptic verdict: C(20,6,3) <= 70
context: subagent (fresh executor, saw only claim/; shares parent's product and conversation history)

Question: does a 70-block (20,6,3) covering strictly beat every known value? Verdict: yes (70 < 71), with one caveat (my own Zenodo fetch was blocked; see 3).

## 0. Object sanity (own checker, from the definition)
```
70 70 True          # blocks, distinct blocks, all 6-subsets of 1..20
0 uncovered         # over all 1140 3-subsets
a6c6ddb8d095dc3818d1eb09a2a2342cfa3254b443799c213068aff07d2a4c6f  C20_6_3_70blocks.txt   (matches CLAIM.md)
```
70 >= Schonheim bound 64, so it is plausible and not below the lower bound.

## 1. Primary status page (coveringrepository.com), one plain request each, no retries
```
2026-10-17T15:00:51Z 200 https://coveringrepository.com/   (home page only; per-cell values load by JavaScript)
2026-10-17T15:00:49Z 200 https://www.coveringrepository.com/systems.aspx?li=2   (latest improvements)
```
Latest-improvements page: 100 dated rows, date range 30/09/2026 to 17/10/2026; a regex search for a (20,06,03) row found none (`[]`).
The per-cell systems.aspx?k=..&t=.. pages were NOT requested, as instructed (Cloudflare-challenged).
The live per-cell value comes from the operator's hand read in CLAIM.md (2026-10-17T14:57Z): `20 06 03 03 71 ... Creator: Chaoying Dai, Ben Li and Michel Toulouse ... 11/04/2006`.
Kit rule 5 allows a hand read like this. It is consistent with everything I fetched myself. The home page (seen in a web-search copy) also says historical data up to the end of March 2026 was imported from the Dan Gordon repository.

## 2. dmgordo/LJCR GitHub, one request
```
2026-10-17T15:00:48Z 200 https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
/C(20,6,3) {"size": 71, "low_bd": 64, "imps": [["71", "", "Chaoying Dai, Ben Li and Michel Toulouse", "2006-04-11 00:00:00"], ["72", "", "Adolf Muehl", "1997-06-27 00:00:00"], ["75", "", "JCD article", "1996-11-14 17:08:00"]]}
```
The live LJCR per-cell page (ljcr.dmgordon.org/cover/show_cover.php?v=20&k=6&t=3) was not fetched directly. A web-search copy of it is titled "64 ≤ C(20,6,3) ≤ 71", created by Chaoying Dai, Ben Li and Michel Toulouse.

## 3. Zenodo LJCR (conceptrecid 10779736), newest version, one request: BLOCKED
```
2026-10-17T15:00:50Z 403 https://zenodo.org/api/records/10779736/versions/latest
  "403 Forbidden ... Access to this resource has been restricted due to unusual traffic from your network."
```
I did not retry this URL. A single fetch of the human-facing concept page https://zenodo.org/records/10779736 with a different tool timed out, and I did not retry that either.
So I could not confirm the Zenodo value myself. The package says LJCR v1.2 (record 19735294, 2026-04-24) gives 71 (scout fetch 2026-10-17T14:51:27Z; excerpt for v1.1 in data/zenodo_v1.1_coverdata_C20_6_3.json).
Zenodo is a snapshot of the same LJCR dataset, which I did fetch live from GitHub main (71), so this gap does not change the comparison.

## 4. Literature / hobbyist / lottery-wheel search (24 months)
- Web search for "C(20,6,3) covering design 70 blocks" and for "C(20,6,3)" with 2025/2026 arXiv upper bounds: the only C(20,6,3) hit is the LJCR page (≤ 71). The search engine's summary claimed a "70-block" design, but the page it cited is titled ≤ 71 and lists the Dai/Li/Toulouse design, so the summary is wrong. The only recent arXiv covering paper found (2608.19872) is about q-ary covering codes K_q(n,R), which is a different problem.
- Lottery wheels (the same object as a 20-number "guarantee 3 if 3" pick-6 wheel): statlotto.com/lottery/us/mega-millions/wheels/v20k6t3 says "Reduced Wheel 20 of 70 ... guarantee 3, 71 tickets". The other hits were "3 if 6" wheels (10 tickets), which are a different object.
- Hobbyist repo thebrockchain/covering-designs (GitHub API tree, 200): its records/ folder holds only C28_13_4_53blocks.txt and C32_13_4_95blocks.txt, with nothing for (20,6,3).
- GitHub issue/PR search for "C(20,6,3)" across all of GitHub: total_count 0.

## 5. V3R1T4S TROPHY_CASE.md and PRs
- TROPHY_CASE.md (raw main, 200): no covering-design family and no (20,6,3) row.
- GitHub search `repo:elder-plinius/V3R1T4S covering`: 8 results. The covering-designs claims are C(41,12,5), C(53,20,3), C(85,24,3), C(61,25,3) (open) and C(38,16,3), C(45,14,3), C(55,14,3) (closed). None is (20,6,3).
- `repo:elder-plinius/V3R1T4S "20,6,3"`: 0 results. `"C(20"`: 1 result (#212, C(53,20,3)), which is not this cell.

## Conclusion
Every value I could read for C(20,6,3) is 71: the live coveringrepository.com per-cell value (operator hand read, 14:57Z), the LJCR GitHub data fetched live, a web-search copy of the LJCR page, a lottery-wheel site, and the latest-improvements list, which has no newer row.
I found no claim of 70 or fewer anywhere. 70 < 71 is a strict improvement by one block, not a tie.
Caveat: I could not fetch Zenodo myself (403, not retried); I relied on the package's 14:51Z fetch for that source.
pass: true
