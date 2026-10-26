# Criterion skeptic: C(35,5,3) <= 713 (covering-designs-record)

context: subagent (fresh executor, saw only claim/; additionally, as permitted by the brief, ran the workspace tool live_cell.py once, and read that tool's request code and its README to judge the rule-5 fix the parent reported at 12:34 PM ET)

Target: full success criterion in claim/criterion.md (no partial win claimed). Every clause checked literally below.

## (d) Exhaustive check, my own checker written from the definition (claim/../work/mycheck.py, stdlib)
```
blocks 713 distinct 713 covered 6545 of 6545 uncovered 0
schonheim 658 C(v,t) 6545
```
claim/checker.py and its controls:
```
VALID C(35,5,3) blocks=713 distinct=713 t_subsets=6545 uncovered=0 schonheim=658
point degrees min=101 max=107 points_used=35; coverage multiplicity histogram=[(1, 6320), (2, 180), (10, 45)]
rc=0
VALID C(7,5,3) blocks=21 distinct=21 t_subsets=35 uncovered=0 schonheim=5
rc=0
INVALID C(35,5,3) blocks=712 distinct=712 t_subsets=6545 uncovered=10 schonheim=658
rc=1
INVALID C(35,5,3) blocks=713 distinct=713 t_subsets=6545 uncovered=6 schonheim=658
problem: line 1: repeated point
rc=1
a19e372c3611962126c615fd73a79e8c023e2f7369b38aa29f12ca00e2181149  C35_5_3_713blocks.txt
```
My checker also asserts every block has 5 distinct points in 1..35. sha256 matches the brief. Clause met.

## (c) Parameter limits
v=35 <= 99, k=5 <= 25, t=3 <= 8; Schonheim L(35,5,3)=658 <= 713 (not below, so no bug signal); C(35,3)=6545 <= 5e9 (same-day claim allowed). Clause met.

## (a) Live tables, each re-fetched at verification time (2026-10-20, ~16:40Z = 12:40 PM ET)

### coveringrepository.com, live plain (35,5,3), m=t
Honest-access judgment:
- The read recorded in claim/CLAIM.md and claim/data/live_coveringrepository_C35_5_3.txt (16:26:12Z) was made with User-Agent "Mozilla/5.0 (X11; Linux x86_64) V3R1T4S-live_cell/1.0 ..." and carried the ASP.NET session cookie from the GET to the POST. That is a browser-imitating UA prefix and cookie replay, both barred by RULES.md rule 5. **I do not rely on the 16:26:12Z read**, and the package file describing it must be replaced before publication (see "Required package fix").
- The fixed tool (request code inspected): `UA = "V3R1T4S-live_cell/1.0 (record-table check; low volume)"`, `# No cookie jar: RULES.md rule 5 forbids cookie replay.`, `_opener = urllib.request.build_opener()` (no HTTPCookieProcessor), one request per URL with no retry loop, 2 s spacing, and it never requests the challenged query-string/per-cell URLs. It GETs the public search page and POSTs the site's own public search form, which is what a human pressing "Search" does, with no challenge being bypassed. I judge this compliant with rule 5. (`http.cookiejar` is still imported but unused, a cosmetic leftover.)

My one run of the fixed tool:
```
(35,5,3,3)  blocks=732  lower=658
   author : Known design, view notes ->
   notes  : Creator: Moshe Milshtein | Method: Tabu Search started from a 733-block covering previously created by Kleszek | Source: Dan Gordon Covering Repository | Repository: https://dmgordo.github.io/
   date   : 13/07/2024
   source : https://coveringrepository.com/systems.aspx (form POST: Search)
   fetched: 2026-10-20 12:39:42 EDT  sha256=0e9406bc3b80b76a62240a7eb44fa8f5d0269a313af87d0eca921b210ae3f0f8
   archive: blocks=732  https://coveringrepository.com/download_archive_vkt.aspx  sha256=3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7
rc=0
```
Independent plain curl (UA "V3R1T4S-research (honest client)", no cookies, one request):
```
archive HTTP 200
2026-10-20T16:39:59Z
3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7  archive.txt
414:35	05	03	03		732
```
Live coveringrepository.com value = 732, from two compliant reads (search grid and public archive). 713 < 732. Met.

### LJCR (dmgordon.org/covering-designs/)
```
dmgordon HTTP 200
a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3  dmg.html
```
It is a landing page with no per-cell values (text: "Giovanni Acerbi's website coveringrepository.com has similar functionality to my old website ... contains more recent improvements"). The old per-cell host, one honest request:
```
curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading
ljcr per-cell HTTP 000
2026-10-20T16:42:42Z
```
(Not retried.) A web-search index snippet of that same per-cell page reads "658 ≤ C(35,5,3) ≤ 732 ... Created by: Moshe Milshtein". That is a cached index, not a fetch, and is given only as corroboration.
LJCR's data now lives on GitHub/Zenodo (re-fetched below), and the live coveringrepository.com row names "Source: Dan Gordon Covering Repository" for its 732. Judgment: read literally, the "live LJCR value" clause has no fetchable per-cell live page. Its maintainer points to coveringrepository.com, though, and the LJCR's own current data (Zenodo v1.2, the latest version) is fetchable and gives 732. I treat the clause as met through LJCR's canonical published data, with that caveat stated. Every LJCR-derived number (733, 732) is above 713, so no reading of the clause changes the outcome.

### dmgordo/LJCR GitHub and Zenodo
```
github HTTP 200
0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef  gh.json
zenodo HTTP 200
9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87  zen.json
gh.json 733 658 ['733', 'Wheel Generator', 'kleszek', '2017-03-25 12:48:15']
zen.json 732 658 ['732', 'Tabu Search started from a 733-block covering previously created by Kleszek', 'Moshe Milshtein', '2024-07-13 05:10:05']
latest version 19735294 1.2 2026-04-24
```
The hashes match the package's recorded fetches. 713 < 733 and 713 < 732. Met.

## (b) 6-month GitHub/arXiv grep (since 2026-04-20)
GitHub repository search, then each covering-design repo's full tree and README grepped for (35,5,3):
```
== hectorfarahani/covering-designs tree HTTP 200   path hits (35,5,3): []
== TheEslabonGroup/covering-designs tree HTTP 200  path hits (35,5,3): []
== vibemathing/problem-um-opg-762-combinatorial-covering-designs-0fa59888 tree HTTP 200  path hits (35,5,3): []
== WynandVStaden/covering-design-records tree HTTP 200  path hits (35,5,3): []
== Meliwat/covering-hunt tree HTTP 200  path hits (35,5,3): []
== nickroci/fuzzy-solvers tree HTTP 200  path hits (35,5,3): []
== Soulxlight/covering-design-c54-16-4 tree HTTP 200  path hits (35,5,3): []
== edwares/horizonmath-c13-7-4 tree HTTP 200  path hits (35,5,3): []
== thebrockchain/covering-designs tree HTTP 301 (renamed; same README as TheEslabonGroup/covering-designs)
```
The only v=35 files (WynandVStaden) are C_35_13_5_5, C_35_15_5_5, C_35_8_5_5 and C_35_9_5_5, which are other cells. README hits for "35" are other cells only.
V3R1T4S repo issues/PRs mentioning "35,5,3": `total 0`.
arXiv API (abs/title "covering design(s)", newest 50): 10 entries since 2026-04-20, all `mentions (35,5,3): False`.
Limitation: GitHub code search needs authentication and was not used, so the grep covers repository names, descriptions, trees and READMEs, not file contents in unrelated repos. Within that scope, no value at or below 713 was found. Met as far as an honest unauthenticated search can show.

## (e) One object, one cell, non-subsumed
There is one block file and one cell (35,5,3), with no partial win and no derived companion claims in this package. The previous holders are 733 (2017) and 732 (2024). 713 is not implied by any listed neighbouring value: the package's history gives 815 as the trivial (34,5,3)+(34,4,2) construction. Met.

## Null models
PREREG says no null model is needed. I agree: the object is explicit, coverage is decided by a deterministic exhaustive check over all 6545 triples (two independent checkers, with positive and negative controls behaving correctly), and the comparison is with fixed published integers. There is no statistical claim to test.

## Hidden quantifiers and stretched definitions
- "C(35,5,3) <= 713" is an upper bound by explicit construction. The package says the orbit MIP proved 713 optimal only within its S5 G-set, "not globally", which is correctly scoped.
- "strictly smaller than EVERY one": the values 732 (coveringrepository live), 732 (Zenodo), 733 (GitHub) and 732 (cached LJCR page) all exceed 713.

## Required package fix (before submission)
claim/data/live_coveringrepository_C35_5_3.txt and the "Live coveringrepository.com cell read" section of claim/CLAIM.md cite the 16:26:12Z read made with the Mozilla-prefixed UA and cookie carry. Replace them with the compliant read: fixed tool at 2026-10-20 12:39:42 EDT (16:39:42Z), sha256 0e9406bc3b80b76a62240a7eb44fa8f5d0269a313af87d0eca921b210ae3f0f8, value 732. Also cite the plain curl archive read (16:28:59Z and 16:39:59Z, sha256 3bc89519...4f331f7, line `35 05 03 03 732`). My pass relies only on those compliant reads.

confirmed_scope: The file claim/C35_5_3_713blocks.txt (sha256 a19e372c3611962126c615fd73a79e8c023e2f7369b38aa29f12ca00e2181149) is a (35,5,3) covering design with 713 blocks, verified exhaustively over all 6545 triples, which is strictly smaller than the live coveringrepository.com plain value 732 (read honestly at 2026-10-20T16:39:42Z), the LJCR Zenodo v1.2 value 732 and the dmgordo/LJCR GitHub value 733, with no smaller (35,5,3) value found in an unauthenticated GitHub repository and arXiv search covering the last six months.
pass: true
