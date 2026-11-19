# Novelty skeptic: covering-designs-record, C(29,5,3) <= 399

context: subagent (fresh executor, saw only claim/)

Claim: claim/C29_5_3_399blocks.txt (sha256 816c287640bc50f50a87d27707aaae2c77ff99c1580a07336a594d3b94a56bbb), 399 blocks, (v,k,t) = (29,5,3). Schonheim L(29,5,3) = 366, so 399 is not below the lower bound.

## Fetches (one plain request each, curl -A "V3R1T4S-research (honest client)", no retries)

```
== https://coveringrepository.com/
2026-10-19T23:49:49Z
HTTP 200 size 12140
== https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
2026-10-19T23:49:50Z
HTTP 200 size 6517686
== https://zenodo.org/api/records?q=conceptrecid:10779736&all_versions=true
2026-10-19T23:49:51Z
HTTP 200 size 18140
== https://www.coveringrepository.com/systems.aspx?li=2
2026-10-19T23:49:51Z
HTTP 200 size 176378
== https://dmgordon.org/covering-designs/
2026-10-19T23:49:52Z
HTTP 200 size 9200
```

sha256 of saved pages:
```
0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef  coverdata.json
29b4008179c613fea9f7dcae88ee26106a835d7c2e0f38a44838fee325213b54  cr_home.html
605ccd047b7675d2c15b96fd099fce8cbec4a97fbab61e194f007548b7605e89  cr_li2.html
a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3  dmg.html
eaa1ea052c0263a3a099d0e4f51bcd0acbfb5a9c918efd9d774bd11a3d65beb9  zenodo.json
```

### dmgordo/LJCR GitHub coverdata.json, key "C(29,5,3)"
```
{"size": 413, "low_bd": 366, "imps": [["413", "Wheel Generator", "Anastasios Tampakis", "2011-03-31 09:09:59"], ["414", "", "Anastasios Tampakis", "2006-07-07 00:00:00"], ["415", "", "Anastasios Tampakis", "2006-06-26 00:00:00"], ["418", "", "Dietmar Pree", "1998-06-03 00:00:00"], ["424", "", "Rade Belic", "1997-09-30 00:00:00"], ["435", "", "JCD article", "1996-11-14 17:08:00"]]}
```
Value: 413.

### Zenodo LJCR concept record 10779736 (all versions)
```
19735294 1.2 2026-04-24 [... 'coverdata.json', ...]
10779737 v1.0 2024-03-04 [...]
19472830 1.1 2026-04-08 [...]
```
Newest is v1.2 / record 19735294, which is not newer than v1.2, so per the brief its coverdata.json was not re-fetched. The GitHub coverdata.json above has the same sha256 as the scout's fetch (0984bb8b...), and the claim's excerpt claim/data/zenodo_v1.2_coverdata_C29_5_3.json records 413 for v1.2.

### coveringrepository.com home page
HTTP 200. The page only has the shell; per-cell values load by JavaScript. Per-cell systems.aspx?k=..&t=..&m=.. pages were NOT requested, as the brief says.

### coveringrepository.com systems.aspx?li=2 (latest (v,k,t) improvements)
```
data rows 100 dates ['19/10/2026', '20/10/2026'] v values [25, 26, 27, 33, 37, 39, 40, 43, 44, 45, 46, 48, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 99]
v=29 rows: []
k05 t03 rows: []
```
There is no (29,05,03) row. Caveat: this list only covers about the last two days, so on its own it cannot rule out an improvement made between April and October 2026. That gap is closed by our own browser read as submitters below.

### dmgordon.org/covering-designs/
HTTP 200. Landing text only, with no per-cell values. It says "This database contains a collection of good (v,k,t)-coverings..." and points to the data (GitHub/Zenodo).

### Live coveringrepository.com cell (human read, kit rule 5)
claim/CLAIM.md records our own browser read (as submitters) of the live plain-coverings cell at 2026-10-19T23:43Z: `29 05 03 03 413 ... Creator: Anastasios Tampakis / Method: Wheel Generator / Source: Dan Gordon Covering Repository ... 31/03/2011`. In that row M = T = 3, so this is the plain (v,k,t) section. The value matches LJCR GitHub and Zenodo exactly (413, Tampakis, Wheel Generator, 2011-03-31). Coveringrepository.com says its history up to March 2026 is imported from LJCR, so a value still dated 2011 means no improvement has been tracked there since. I accept this read as the live value: 413.

## Literature / hobbyist / repo searches
- Web search "C(29,5,3) covering design 413 blocks": top hit is the old LJCR page titled "366 <= C(29,5,3) <= 413" (Anastasios Tampakis). Nothing lower.
- Web search "\"C(29,5,3)\" covering design new bound 2025 OR 2026": same LJCR 413 page, nothing else relevant.
- Web search for a 29-number, pick-5, "3 if 3" lottery wheel: no such wheel listed (Lottery Post pick-5 wheels stop well below 29 numbers for 3 if 3). No wheel with 413 tickets or fewer was found.
- arXiv API, all:"covering design", newest 100 by submission date: 22 entries since 2024-10. None mentions (29,5,3). The relevant-looking ones are "A tight single-change covering design with block size 6" (2026-07-13, k=6), "Tackling the 6/49 Lottery ..." (2026-03-25, v=49, k=6), and "On Zero Skip-Cost Generalized Fractional-Repetition Codes from Covering Designs" (2025-02-18). None gives a C(29,5,3) value.
- thebrockchain/covering-designs (fetched at 2026-10-19T23:50:34Z, HTTP 200, via the repo-id redirect): the full tree is `records/C28_13_4_53blocks.txt, records/C32_13_4_95blocks.txt, reference/C28_13_4_54blocks_Fadlaoui2008.txt, reference/C32_13_4_96blocks_Fadlaoui2009.txt, src/verify.py, ...`. It has no (29,5,3) entry.
- GitHub repository search for "covering design" pushed since 2024-10-19 (2026-10-19T23:50:52Z, HTTP 200): results are generic and unrelated, with no (29,5,3) repo. This search was low-yield, so it is weak evidence.
- elder-plinius/V3R1T4S TROPHY_CASE.md (2026-10-19T23:50:15Z, HTTP 200): `grep -i -E 'covering|C\(29'` found no match at all.
- elder-plinius/V3R1T4S pull requests, state=all, 6 pages (2026-10-19T23:50:15Z to 23:50:26Z, all HTTP 200): `total PRs 560 numbers 1 571`. A regex for `(29,5,3)`, `C29_5_3` or `29-5-3` in titles and bodies found no hits. The covering-design PRs that exist are for C(40,16,7), C(57,14,3), C(20,6,3), C(68,14,5), C(94,13,5), C(41,12,5), C(53,20,3), C(85,24,3), C(61,25,3), C(55,14,3), C(45,14,3) and C(38,16,3). None is (29,5,3).

## Sanity re-check of the object (own code, from the definition)
```
own check: blocks 399 distinct 399 valid_points True covered 3654 of 3654
```

## Verdict
Every known value is 413: the live coveringrepository.com cell (our own browser read as submitters), LJCR GitHub coverdata.json, and Zenodo LJCR v1.2. The old LJCR page shows "366 <= C(29,5,3) <= 413". No claim below 413 turned up in arXiv, GitHub, the hobbyist repo, lottery-wheel sources, the trophy case or the 560 PRs scanned. 399 < 413 strictly, by 14 blocks, and 399 >= Schonheim 366. This is not a tie.
Residual caveats: the live per-cell value rests on a human read, which is sanctioned by rule 5. About 11 PR numbers up to #571 were not returned by the pulls API (most likely issues).

pass: true
