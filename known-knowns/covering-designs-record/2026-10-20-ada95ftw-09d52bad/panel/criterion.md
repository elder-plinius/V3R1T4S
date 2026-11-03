# Criterion skeptic: covering-designs-record, C(38,6,3) <= 469

context: subagent (fresh executor, saw only claim/; additionally read the request-building lines of the workspace live-table tool to judge rule-5 compliance, at the orchestrator's instruction that the tool had been fixed at 12:34 ET)

Criterion checked: claim/criterion.md (full success criterion; no partial win claimed). All times below are UTC unless marked ET.

## (d) Checked exhaustively; (c) parameter limits, Schonheim, C(v,t)
My own checker written from the definition (every 3-subset of {1..38} in some block), plus claim/checker.py and its controls:

```
$ python3 work/mycheck.py claim/C38_6_3_469blocks.txt
lines 469 distinct 469 badblocks 0 triples 8436 uncovered 0
schonheim 425 C(v,t) 8436
$ python3 checker.py 38 6 3 C38_6_3_469blocks.txt
VALID C(38,6,3) blocks=469 distinct=469 t_subsets=8436 uncovered=0 schonheim=425
point degrees min=70 max=81 points_used=38; coverage multiplicity histogram=[(1, 8148), (3, 168), (5, 84), (7, 8), (9, 28)]
$ python3 checker.py 7 5 3 data/pos_C7_5_3_all.txt
VALID C(7,5,3) blocks=21 distinct=21 t_subsets=35 uncovered=0 schonheim=5
$ python3 checker.py 38 6 3 data/neg_minus_last_block.txt
INVALID C(38,6,3) blocks=468 distinct=468 t_subsets=8436 uncovered=8 schonheim=425
$ python3 checker.py 38 6 3 data/neg_repeated_point.txt
INVALID C(38,6,3) blocks=469 distinct=469 t_subsets=8436 uncovered=10 schonheim=425
problem: line 1: repeated point
$ sha256sum C38_6_3_469blocks.txt
09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b  C38_6_3_469blocks.txt
```
v=38 <= 99, k=6 <= 25, t=3 <= 8; b=469 >= L(38,6,3)=425 (not below Schonheim, so no bug signal); C(38,3)=8436 <= 5e9, so a same-day claim is allowed. Every block has 6 distinct points in 1..38, no duplicate blocks. Hash matches the brief.

## (a) Live table values, re-fetched at verification time

### Honest-access judgement on the live-table tool
The read recorded in claim/data/live_coveringrepository_C38_6_3.txt (16:26:03Z) was made with User-Agent "Mozilla/5.0 (X11; Linux x86_64) V3R1T4S-live_cell/1.0 ..." and carried the ASP.NET session cookie from the GET to the POST. A Mozilla-prefixed (browser-imitating) User-Agent and cookie replay are both named in rule 5 as not allowed, so I do not rely on that read. The package file must be replaced with a compliant read before publication.

The fixed tool, which I inspected:
```
UA = "V3R1T4S-live_cell/1.0 (record-table check; low volume)"
# No cookie jar: RULES.md rule 5 forbids cookie replay.
_opener = urllib.request.build_opener()
req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
```
It sends a User-Agent that names V3R1T4S, uses no cookie jar, waits 2 s between requests and never retries. It stops on any non-200 status or a Cloudflare challenge marker, and it never requests the challenged query-string URLs. Its POST is the site's own read-only search form. I judge this compliant with rule 5.

My single run of the fixed tool:
```
$ python3 live_cell.py 38 6 3        (started 2026-10-20T16:35:27Z)
(38,6,3,3)  blocks=510  lower=425
   author : Known design, view notes ->
   notes  : Creator: Jan de Heer and Steve Muir | Method: Private Tools | Source: Dan Gordon Covering Repository | Repository: https://dmgordo.github.io/
   date   : 05/06/2010
   source : https://coveringrepository.com/systems.aspx (form POST: Search)
   fetched: 2026-10-20 12:35:30 EDT  sha256=16035f1396eb60c8883d6b7a5cb489ea83dd5c8b838c69b647db10d655945995
   archive: blocks=510  https://coveringrepository.com/download_archive_vkt.aspx  sha256=3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7
```
I also made my own independent plain curl of the public archive (User-Agent "V3R1T4S-research (honest client)", no cookies, one request):
```
2026-10-20T16:35:40Z
HTTP 200 https://coveringrepository.com/download_archive_vkt.aspx
3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7  archive.txt
674:38^I06^I03^I03^I^I510^M$
```
Result: the live coveringrepository.com plain (m=t) value is 510, from two compliant reads. 469 < 510.

### LJCR GitHub / Zenodo (each fetched once, plain curl)
```
2026-10-20T16:35:41Z HTTP 200 https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef
2026-10-20T16:35:42Z HTTP 200 https://zenodo.org/api/records/19735294/files/coverdata.json/content
9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87
coverdata_gh.json 510 425 ['510', 'Private Tools', 'Jan de Heer and Steve Muir', '2010-06-05 09:25:35']
zenodo.json 510 425 ['510', 'Private Tools', 'Jan de Heer and Steve Muir', '2010-06-05 09:25:35']
2026-10-20T16:38:08Z HTTP 200 https://zenodo.org/api/records/19735294   (resolved from /api/records/10779736/versions/latest)
19735294 1.2 2026-04-24 La Jolla Coverings Repository
```
Zenodo v1.2 is the newest version of the LJCR concept record. 469 < 510 on both.

### "Live LJCR value (https://dmgordon.org/covering-designs/)"
```
2026-10-20T16:35:42Z HTTP 200 https://dmgordon.org/covering-designs/  sha256 a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3
  <title>Covering Designs - LJCR ; links only (coveringrepository.com, github.com/dmgordo, doi 10.5281/zenodo.10779736); no per-cell values
2026-10-20T16:38:02Z HTTP 200 https://dmgordon.org/ljcr/  sha256 385370cb590026bf64bbeed3492ff4cf3f88538691fd5b84eb56bc4a03693951
  <title>The La Jolla Combinatorics Repository - LJCR ; links to Zenodo/GitHub only; no per-cell values
2026-10-20T16:38:02Z https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=38
  curl: (35) TLS connect error ... HTTP 000   (not retried)
```
On a literal reading, the named URL has no per-cell value to beat. The LJCR's own pages now point to the GitHub and Zenodo data as the repository, and the live coveringrepository.com row names the Dan Gordon repository as its source, with a site note that LJCR history up to March 2026 was imported there. I therefore treat the live LJCR value as 510, read from the LJCR's current published data (GitHub main and Zenodo v1.2). A web search index snippet of the old per-cell page also shows "425 <= C(38,6,3) <= 510". This is the softest clause, but no LJCR source anywhere shows a value at or below 469.

## (b) 6-month GitHub/arXiv grep
- GitHub repository search for "covering design" pushed after 2026-04-20 (HTTP 200). The covering-design repos found were hectorfarahani/covering-designs, WynandVStaden/covering-design-records, TheEslabonGroup/covering-designs, and thebrockchain/covering-designs (which returned 301, moved). I fetched their trees and data files:
  - hectorfarahani records: C28_9_3, C29_17_4, C30_12_3, C32_18_4 only.
  - TheEslabonGroup records: C28_13_4_53, C32_13_4_95 only (the hobbyist claims named in the criterion).
  - WynandVStaden: search_plain.tsv (433 lines), derived.tsv (293), components.tsv (547) and RECORDS.md. `awk` for v=38,k=6,t=3 returned nothing. Its (*,6,3,3) components are v = 11,12,16,19,22,28,33,40,41 only.
- arXiv: the API request timed out (HTTP 000, not retried). The arxiv.org listing search for "covering design", newest first (HTTP 200, 54 results), had no abstract mentioning (38,6,3). The 2026 items in that topic were "A tight single-change covering design with block size 6" (a different problem), the C(12,6,4)=41 paper, and a 60-point lottery-style construction, none for this cell. A web search for "C(38,6,3)" found only the LJCR/coveringrepository value of 510.
- I found no value at or below 469 for (38,6,3).

## (e) One object, one cell
There is a single explicit block file for the single cell (v,k,t)=(38,6,3), plain covering (m=t). The construction notes (PSL(2,7) orbits, MIP optimal within the G-set) are orientation only and are not part of what is claimed. The claim makes no "optimal" or global statement.

## Hidden quantifiers / stretched definitions / null model
- The claim says "C(38,6,3) <= 469", an upper bound only, and it is exactly what the file proves. The "41 fewer than 510" margin is correct against all reached sources.
- The live coveringrepository.com read in the package's data file used a non-compliant method. It must be updated to the compliant fixed-tool read (or my plain archive read) before publication. Otherwise CLAIM.md would cite a read obtained in a way rule 5 forbids. This is a packaging fix, not a failure of the criterion, because compliant reads give the same 510.
- Null model: I agree none is needed. The claim is a deterministic, explicit object checked exhaustively over all 8436 triples by two independent checkers (with positive and negative controls), against fixed published values. There is no statistical or sampling component to null-test.
- Subsumption: no listed or grepped value for (38,6,3) is at or below 469, and the bound is not implied by any table entry I saw, so this is a genuine, non-subsumed win.

confirmed_scope: The file claim/C38_6_3_469blocks.txt (sha256 09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b) is a (38,6,3) covering design with 469 blocks, checked exhaustively over all 8436 triples, so C(38,6,3) <= 469, which is strictly below the value 510 shown on 2026-10-20 by the live coveringrepository.com plain table (read with a rule-5-compliant client), the LJCR GitHub data and the LJCR Zenodo v1.2 record.

pass: true
