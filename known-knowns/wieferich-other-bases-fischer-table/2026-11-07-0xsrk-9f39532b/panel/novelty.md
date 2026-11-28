role: NOVELTY
context: claude code Task subagent (fresh context, saw only claim/)

# NOVELTY review of claim/object/pair.json

object (claim/object/pair.json): `{"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28910, "p": 1011548897263}`,
claimed as partial win p1 (claim/claim.md).

novelty: The pair (28910, 1011548897263) is new: neither number occurs in any fetched Fischer file, in OEIS, in the V3R1T4S repository (TROPHY_CASE.md, known-knowns/, the target page, tree, releases) or its 934 pull requests, nor in any literature or code hit of the last 24 months, and since 28910 is the only base in 2..65536 for which p is a Wieferich prime, no published pair shares p, so no trivial edit or propagation of a published object yields it; it adds one pair to the p1 cell and strictly beats the known set.

How I worked: I read only claim/ and what I fetched myself. Fetched files are in panel/work-novelty/fetched/, my scripts
in panel/work-novelty/code/ (standard-library Python, run with `python3 -I -B`), and every command output quoted below
is saved under panel/work-novelty/. Every fetch was `curl -sS -A 'V3R1T4S-agent/1.0 (open-research notebook; one honest
request)' -o FILE -w '%{http_code}' URL`, one request per URL, no retries. Review window (`date -u`):
2026-11-07T15:52:48Z to 2026-11-07T16:05:12Z. GitHub owner handles are written `<repo>` (the repository named in
claim/status_sources.md) or `<owner>`, so this file carries no user names.

## 1. Primary table (the bank's status source), fetched once

- URL: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
- time: 2026-11-07T15:53:12Z (`date -u` just before the request); HTTP 200; 288459 bytes;
  sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4, the same hash as the scout's record in
  claim/status_sources.md, so the table has not changed since the claim's scout fetch.
- value: the scope and limit lines (`grep -n` on my fetched copies; FermQ_Sort.txt was fetched once at
  2026-11-07T15:53:17Z, HTTP 200):

```
FermQ_Sorg.txt:7:Letzte 20 mit Basen: 1319 (prim), 9223, 3626, 1255, 7978, 8220, 4180, 8572, 3328 (neue Basis),
FermQ_Sorg.txt:10:Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125
FermQ_Sorg.txt:11:Die Basen sind gegenwaertig durchsucht bis 4.8E+12
FermQ_Sort.txt:4:Die gefundenen Primzahlen der Fermatquotienten von der Basis 2 bis 1052
FermQ_Sort.txt:9:Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
FermQ_Sort.txt:10:Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
FermQ_Sort.txt:1025:65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)
```

Reading: FermQ_Sorg.txt covers bases 2..10125 searched to 4.8E+12; FermQ_Sort.txt covers 2..1052 plus the single base
65537. Neither table has a row for base 28910 or for any base in 10126..65536, and p occurs in neither file
(section 3).

## 2. Fetch records (one request each)

| URL | UTC time (date -u before request) | HTTP | bytes | sha256 | same as scout's record |
|---|---|---|---|---|---|
| http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt | 2026-11-07T15:53:12Z | 200 | 288459 | 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 | yes |
| http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt | 2026-11-07T15:53:17Z | 200 | 33141 | bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b | yes |
| http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt | 2026-11-07T15:53:22Z | 200 | 115771 | e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 | yes |
| http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt | 2026-11-07T15:53:28Z | 200 | 81696 | 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 | yes |
| http://www.fermatquotient.com/ | 2026-11-07T15:53:33Z | 200 | 16104 | 42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1 | yes |
| http://www.fermatquotient.com/FermatQuotienten/News.txt | 2026-11-07T15:53:54Z | 200 | 8500 | 1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7 | n/a (no scout hash) |
| http://www.fermatquotient.com/FermatQuotienten/FermatQ3.txt | 2026-11-07T15:53:59Z | 200 | 11274 | 022855e8d16257ca4931bd9f7f9133012f17bbf1bc528f9a6cd12995b02a0a41 | n/a (no scout hash) |
| http://www.fermatquotient.com/FermatQuotienten/SwitchFermQ.txt | 2026-11-07T15:54:04Z | 200 | 10726 | 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa | n/a (no scout hash) |
| http://www.fermatquotient.com/FermatQuotienten/PQuotient_Sort.txt | 2026-11-07T15:54:09Z | 200 | 28364 | 375de4557fcf0569bf80040532606e7e2c1f9e7f2101d9878bc947ce95dce864 | n/a (no scout hash) |
| http://www.fermatquotient.com/FermatQuotienten/Statistik.txt | 2026-11-07T16:01:39Z | 200 | 24222 | dde1fa8d6c6105a74895dfb64646b7b74cb327a15aa7c49695f1c58ebabd2b2b | n/a (no scout hash) |
| http://www.fermatquotient.com/FermatQuotienten/Generelles.txt | 2026-11-07T16:01:41Z | 200 | 8011 | 418d7557fa5bd72192af394901187e5f8d0b18826e1dd63b13988bb0cfae3e69 | n/a (no scout hash) |
| https://oeis.org/search?q=1011548897263&fmt=data | 2026-11-07T15:54:14Z | 200 | 6737 | e5211faf57da6322a01a7feaae4b072de777903c88cfc07a341dd6f517df80ce | no (scout d8b7fd36ede5..) |
| https://api.github.com/repos/<repo>/git/trees/main?recursive=1 | 2026-11-07T15:58:40Z | 200 | 2167895 | 93b7eef8c4a599e1c8925507d9f8ad7dbb3e982741af87c745c69000d6d73625 | n/a (no scout hash) |
| https://raw.githubusercontent.com/<repo>/main/TROPHY_CASE.md | 2026-11-07T15:59:13Z | 200 | 31306 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 | n/a (no scout hash) |
| https://raw.githubusercontent.com/<repo>/main/known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md | 2026-11-07T15:59:19Z | 200 | 5492 | 8395b2fe8a39df3816c850ea9279ab8931e3e3655b4b7ad69c7e437b8f520d52 | n/a (no scout hash) |
| https://api.github.com/repos/<repo>/releases?per_page=100 | 2026-11-07T15:59:24Z | 200 | 2 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 | n/a (no scout hash) |
| https://api.github.com/repos/<owner>/wieferich-base-search/readme | 2026-11-07T16:00:59Z | 200 | 5982 | 71e8f50ca82566bb55880b3c8ffca98add17493cbd4a6a635bce3582166fb387 | n/a (no scout hash) |
| https://api.github.com/repos/<owner>/wieferich/readme | 2026-11-07T16:01:04Z | 200 | 1172 | f11ec13c62f727e6952d119f01638d2e73635db18ecb4c329ff7be4b17758faf | n/a (no scout hash) |

The OEIS hash differs from the scout's because the page embeds a per-request token and the live database line; its
search result is the same "no match" (section 4). No request was blocked, challenged or retried.

Read-only `gh` calls (outputs saved under panel/work-novelty/): `gh pr list` over all states (run twice, because a
pipe cut the first saved copy short), four `gh pr list --search` queries, `gh pr view 973` and
`gh search repos wieferich` (sections 5 and 6). Two calls did not give an answer and were not repeated:
`gh api` (repository metadata) was refused by this workspace's permission settings, and `gh search code
'1011548897263'` answered `HTTP 408: Request timed out while fetching results. Please try again.
(https://api.github.com/search/code?page=1&per_page=50&q=1011548897263)`. The repository files above were read with
the prescribed honest curl GET, one request each, as the run's scout does for api.github.com.

## 3. Fischer's files: search for b = 28910 and p = 1011548897263

`python3 -I -B panel/work-novelty/code/novelty_scan.py <files>` (whole-token and substring search over the latin-1
text, plus a row parse of the two tables):

```
== FermQ_Sorg.txt: 288459 bytes, sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4, 44745 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: True
   line 775: 799,  5, 2891032049
   lines containing b or p as substring: 1
   nearest integer tokens around p: below 1010499405017, above 1013674942057
   integer tokens in (1e12, 2e12): 247
   table rows parsed: 10000; min base 2, max base 10125; non-increasing row starts (wrapped lines): 0
   row for base 28910: False
   bases above 10125 with a row: []
   bases in 10126..65536 with a row: []
   rows listing p: []
== FermQ_Sort.txt: 33141 bytes, sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b, 4707 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: True
   line 775: 799  P: 5, 2891032049
   lines containing b or p as substring: 1
   nearest integer tokens around p: below 902060958301, above 1082305363079
   integer tokens in (1e12, 2e12): 18
   table rows parsed: 981; min base 2, max base 65537; non-increasing row starts (wrapped lines): 1
   row for base 28910: False
   bases above 10125 with a row: [65537]
   bases in 10126..65536 with a row: []
   rows listing p: []
== ErstBasen.txt: 115771 bytes, sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820, 10379 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 1000158170385, above 1036253048315
   integer tokens in (1e12, 2e12): 69
== ErstPBasen.txt: 81696 bytes, sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362, 7315 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: True
   line 720: 182058941, 182792723, 182891069, 182961703, 183106003, 183707863, 183877913, 184348817, 184359761, 185387539,
   lines containing b or p as substring: 1
   nearest integer tokens around p: below 998892348491, above 1069929736297
   integer tokens in (1e12, 2e12): 12
== FermatQ3.txt: 11274 bytes, sha256 022855e8d16257ca4931bd9f7f9133012f17bbf1bc528f9a6cd12995b02a0a41, 1389 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 834277575727, above 1209257922307
   integer tokens in (1e12, 2e12): 5
== SwitchFermQ.txt: 10726 bytes, sha256 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa, 935 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 988813725773, above 1125950115061
   integer tokens in (1e12, 2e12): 4
== PQuotient_Sort.txt: 28364 bytes, sha256 375de4557fcf0569bf80040532606e7e2c1f9e7f2101d9878bc947ce95dce864, 4244 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 976497503143, above 1042783068319
   integer tokens in (1e12, 2e12): 30
== News.txt: 8500 bytes, sha256 1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7, 570 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 902060958301, above 1082305363079
   integer tokens in (1e12, 2e12): 10
== fermatquotient_index.html: 16104 bytes, sha256 42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1, 463 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 65537, above None
   integer tokens in (1e12, 2e12): 0
== Statistik.txt: 24222 bytes, sha256 dde1fa8d6c6105a74895dfb64646b7b74cb327a15aa7c49695f1c58ebabd2b2b, 2211 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: True
   line 679: Basis: 799 P: 2891032049
   lines containing b or p as substring: 1
   nearest integer tokens around p: below 1000436194319, above 1013674942057
   integer tokens in (1e12, 2e12): 63
== Generelles.txt: 8011 bytes, sha256 418d7557fa5bd72192af394901187e5f8d0b18826e1dd63b13988bb0cfae3e69, 1026 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 321644, above None
   integer tokens in (1e12, 2e12): 0
```

The one "non-increasing row start" in FermQ_Sort.txt is the footer prose, not a row:

```
non-increasing row start at line 1031 : 9, 25, 27, 36, ..., die die gleichen Primzahlen haben, wie deren Grundbasen. (previous base 65537 )
```

Reading: p is neither a token nor a substring of any Fischer file, including the two "extreme first bases" files
(ErstBasen.txt, ErstPBasen.txt, which list some pairs above 1e12), the mod p^3 list (FermatQ3.txt), the double
Wieferich pairs (SwitchFermQ.txt), PQuotient_Sort.txt, News.txt (records), Statistik.txt and Generelles.txt. The base
28910 is never a token; its only substring hits sit inside 2891032049 (base 799's prime) and 182891069, which are other
numbers. Both tables are parsed completely and neither has a row for any base in 10126..65536.

## 4. OEIS (one search for p)

```
101:Search:</span> <b>1011548897263</b>
116:Sorry, but the terms do not match anything in the table.
184:Last modified November  7 10:49 EST 2026.  Contains 401116 sequences.
```

Reading: a normal result page (search box, result bar, database line), not a challenge page. p is in no OEIS sequence's
terms. The page's other occurrences of p are only the echoed query (section 3, `oeis_search_p.html`).

## 5. This repository: TROPHY_CASE.md, known-knowns/, releases, pull requests

Tree (`python3 -I -B panel/work-novelty/code/tree_scan.py fetched/gh_tree_main.json`):

```
tree sha 06b61ea410a5ee90f3c9377a01d468c7cf05c0bd, truncated False, entries 7190
files: 5940
top-level entries: ['.github', '.gitignore', 'AGENTS.md', 'CITATION.cff', 'CLAUDE.md', 'DONT_SPOIL_THE_HUNT.md', 'GEMINI.md', 'LICENSE', 'LICENSE-DATA', 'LICENSING.md', 'README.md', 'READ_BEFORE_CITING.md', 'SHA256SUMS', 'TROPHY_CASE.md', 'bank', 'kit', 'known-knowns', 'known-unknowns', 'llms.txt', 'news', 'sealed-envelopes', 'site', 'wrangler.jsonc']
files under known-knowns/: 4724; categories (30): ['bigger-codes', 'biggest-graphs', 'cap-set-dim7-dim8', 'codetables-binary-linear', 'codetables-qubit-upper-bounds-n101-256', 'constant-weight-codes', 'eaqecc-qutrit-codetables-gaps', 'erdos-699-binomial-gcd', 'faster-matrix-multiplication', 'group-testing-separable-designs', 'hadamard-maxdet-records', 'iea37-cs1-circular-wind-farm-layout', 'lehmer-past-10-to-the-50', 'lennard-jones-ccd-doye-table', 'minimizer-density-record-tables', 'ncbi-pathogen-ast-ecoli-genotype-phenotype-f1', 'nucleotide-transformer-benchmark-mcc', 'packomania-cci-equal-circles-in-circle', 'packomania-hyperspheres-hsp4-hsp6', 'packomania-scu-spheres-in-cube', 'qoblib-market-split-and-portfolio', 'risk-or-safety-exact-optimal-play', 'robust-forecast-aggregation-bounds', 'robustbench-cifar100-stronger-attack', 'spherical-codes-cohn-table', 'square-grid-lattice-gas-exact-counts-oeis', 'stable-marriage-max-stable-matchings', 'sunflower-free-capacity-lower-bound', 'thomson-problem-live-tables', 'vnncomp-2026-unsolved-instances']
files directly in known-knowns/: []
paths (anywhere) mentioning ('wieferich', 'fermat', 'fischer', 'quotient'): 6
  known-unknowns/graphs-games-automata/misere-quotient-period-5-element.md
  known-unknowns/number-hunts/fermat-catalan-new-solution-with-square.md
  known-unknowns/number-hunts/fermat-numbers-new-factor.md
  known-unknowns/number-hunts/wieferich-base-2-beyond-2-64.md
  known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md
  known-unknowns/wildcard/kourovka-16-46-conder-finite-quotient.md
TROPHY_CASE.md: present, blob 18b731d7d4bf99efd323d48740284daccb8501b0, 31306 bytes
bank/targets.json: present, blob 89f9e6ed07700c84edc91d7227e10845097484ff, 6189749 bytes
```

The same token scan as section 3, on the fetched repository files:

```
== TROPHY_CASE.md: 31306 bytes, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113, 2037 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 99990918, above None
   integer tokens in (1e12, 2e12): 0
== ku_wieferich-other-bases-fischer-table.md: 5492 bytes, sha256 8395b2fe8a39df3816c850ea9279ab8931e3e3655b4b7ad69c7e437b8f520d52, 158 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 1006003, above 194092950328757
   integer tokens in (1e12, 2e12): 0
== gh_releases.json: 2 bytes, sha256 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945, 0 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below None, above None
   integer tokens in (1e12, 2e12): 0
== gh_tree_main.json: 2167895 bytes, sha256 93b7eef8c4a599e1c8925507d9f8ad7dbb3e982741af87c745c69000d6d73625, 215228 integer tokens
   p=1011548897263 as integer token: False; as substring: False
   b=28910 as integer token: False; as substring: False
   lines containing b or p as substring: 0
   nearest integer tokens around p: below 995461777560, above 1296034948496
   integer tokens in (1e12, 2e12): 6
```

```
--- releases file (fetched/gh_releases.json):
[]
--- TROPHY_CASE.md lines matching wieferich|fermat|fischer (count):
0
--- p1 line in the known-unknowns page (generated from bank/targets.json):
15:- **p1:** New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS.
```

Pull requests (`gh pr list --state all --limit 3000 --json ...`, run between the `date -u` stamps
2026-11-07T15:57:45Z and 2026-11-07T15:58:21Z, then `python3 -I -B panel/work-novelty/code/pr_scan.py`):

```
pull requests listed: 934; numbers 1..982; by state {'OPEN': 403, 'MERGED': 181, 'CLOSED': 350}
created range: 2026-10-14T01:52:59Z .. 2026-11-07T15:36:50Z
titles/branches mentioning any of ('wieferich', 'fermat', 'quotient', 'fischer', '28910', '1011548897263', 'mod p^2'): 1
  #973 OPEN draft=True 2026-11-07T13:02:22Z :: [claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1
entries containing p=1011548897263 anywhere: []
entries containing b=28910 as a number anywhere: []
```

GitHub search over pull-request titles, bodies and comments (`gh pr list --state all --search ...`):

```
2026-11-07T15:58:21Z
search: 1011548897263
[]
search: 28910
[]
search: wieferich
[{"number":973,"state":"OPEN","title":"[claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1"}]
search: fermat quotient
[{"number":973,"state":"OPEN","title":"[claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1"}]
```

The one Wieferich pull request (`gh pr view 973 --json number,title,state,isDraft,createdAt,body,comments,files`):

```
title: [claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1
state: OPEN draft: True created: 2026-11-07T13:02:22Z
files: 23
comments: 0
contains p=1011548897263: False
contains b=28910 as a number: False
```

Reading: TROPHY_CASE.md has no Wieferich, Fermat or Fischer entry and neither number. known-knowns/ has no category
for this target, and no path anywhere in the tree contains either number (sealed-envelopes/ holds two unrelated topics,
cipher machines and Vesuvius letters). The repository has no releases, so no release asset can hold the pair. Among all
open, merged and closed pull requests the only Wieferich claim is draft #973, a different pair (24766, 1000747824697),
whose body, comments and file list mention neither number.

## 6. Literature and code of the last 24 months

Web searches (WebSearch, during the review window): `"1011548897263"`; `"28910" "1011548897263"`;
`Wieferich prime base 28910`; `Wieferich primes to bases above 10125 up to 65536 new search 2025 2026`;
`arXiv 2025 Fermat quotient zeros Wieferich pairs many bases computation b^(p-1) ≡ 1 mod p^2`;
`github Wieferich pairs search bases 2 to 65536 Fermat quotient table`;
`V3R1T4S wieferich-other-bases-fischer-table pair claim`;
`new Wieferich primes to other bases found 2026 fermatquotient Fischer table larger bases`.
No result contains p or any Wieferich prime to base 28910, and none reports a search of bases 10126..65536. The recent
items found are OEIS per-base sequences for small bases, base-2 work, papers without new pairs for large bases, and the
repositories below.

`gh search repos wieferich` (owners omitted):

```
query time (date -u): 2026-11-07T16:00:37Z
repositories returned: 11
updated since 2024-11-07: 6
  wieferich | updated 2026-06-08T13:10:20Z | 
  wieferich-base-search | updated 2026-06-14T21:58:25Z | GPU search for Wieferich primes to 10^14 across 27 bases; extends R. Fischer's bound for six of them (OEIS A03
  WWCL | updated 2026-08-18T00:01:59Z | A BOINC OpenCL program to search for Wieferich and Wall-Sun-Sun primes
  problem-wikipedia-2f641b3840b65622 | updated 2026-09-16T12:12:03Z | Vibe Mathing single-problem candidate research: Are there infinitely many Wieferich primes ?
  problem-wikipedia-9dc175e41e9cb81d | updated 2026-09-16T12:17:45Z | Vibe Mathing single-problem candidate research: Wieferich primes
  problem-wikipedia-a19065cf878620a0 | updated 2026-09-16T12:30:36Z | Vibe Mathing single-problem candidate research: For any given integer a > 0, are there infinitely many Lucas?W
```

The two that could hold search data, read once each (`readme_scan.py`, lines trimmed where marked `[...]`):

```
== README of repository wieferich-base-search (owner omitted): path README.md, 3705 chars, sha256 486f4731754ef6621a865fac95c1d544dc402f46370dff2fb08c73374dc6b00b
   contains p=1011548897263: False; contains b=28910 as a number: False
   | # Wieferich base search
   | A search for Wieferich primes in 27 bases whose smallest example was unknown, run
   | on a single workstation GPU. No Wieferich prime exists below 10^14 for any of
   | these 27 bases.
   [...]
   | we tested every prime p in (4.4 x 10^12, 10^14] for the Wieferich condition
   [...]
== README of repository wieferich (owner omitted): path README.md, 303 chars, sha256 f7b2d368671a67e373d4994d0649128cf7c18450e2e6dd7591b0ba4ab887301e
   contains p=1011548897263: False; contains b=28910 as a number: False
   | An interactive, browser-based explorer of Fermat quotients and the search for
   | Wieferich primes to any base ? for example, the base-2 Wieferich primes below
```

Reading: the 27-base GPU search is a null result for small bases over primes in (4.4 x 10^12, 10^14], so it touches
neither base 28910 nor primes near p; the other repository is an interactive explorer; WWCL and the three
single-problem repositories are base-2 or general. GitHub code search for p timed out (section 2) and was not
repeated; the web searches did not find p either.

## 7. Trivial edits and propagation: my own computation

`python3 -I -B panel/work-novelty/code/pair_context.py`:

```
b = 28910, p = 1011548897263, p < 3.18e23: True
p prime (deterministic Miller-Rabin, bases 2..37): True
pow(b, p-1, p^2) = 1
factorisation of b: 2 * 5 * 7^2 * 59
gcd of exponents = 1 (b is a perfect power iff this is > 1)
  q_p(2) mod p = 749604166799  (Wieferich for base 2: False)
  q_p(5) mod p = 252643161267  (Wieferich for base 5: False)
  q_p(7) mod p = 9495223617  (Wieferich for base 7: False)
  q_p(59) mod p = 1001860019226  (Wieferich for base 59: False)
sum of e*q_p(r) mod p = 0  (0 means b is a Wieferich base, by additivity)
proper divisors d of b (1 < d < b): 22; those with d^(p-1) == 1 mod p^2: []
all bases x in 2..65536 with x^(p-1) == 1 mod p^2: [28910]
of these, bases <= 10125 (Fischer's FermQ_Sorg range): []
pow(65537, p-1, p^2) == 1: False
elapsed 0.3 s
```

Reading, edit by edit (the novelty rule's list):
- relabelling (perfect powers): 28910 = 2 * 5 * 7^2 * 59 has exponent gcd 1, so it is not a power of a smaller base,
  and its own powers lie above 65536; no published pair (a, p) with a^k = 28910 exists.
- a valid propagation rule (Fermat-quotient additivity: products, quotients and powers of bases; residues mod p^2):
  each such rule keeps the prime p fixed, so it needs a published pair with this same p. There is none: p occurs in
  no fetched source, and the exhaustive check shows 28910 is the only base in 2..65536 with x^(p-1) == 1 (mod p^2).
  No proper divisor of 28910 works, and the four prime factors have nonzero Fermat quotients whose weighted sum
  vanishes, so the pair is not inherited from any smaller base. 28910 is also the smallest Wieferich base of p, which
  is why p cannot sit in Fischer's tables.
- symmetry: the other bases that share this pair's Wieferich property at p (p^2 - 28910, the inverse of 28910 mod p^2,
  28910 times a p-th power mod p^2) all lie above 65536, since the exhaustive check finds no other Wieferich base of p
  up to 65536, and none appears in any source (p occurs nowhere); the double-Wieferich swap (b, p) to (p, b) needs a
  prime base, and 28910 is composite.
- deletion, restriction, local numerical polish: not applicable to a single exact integer pair.
- seeding: claim/ names no seed object, and none of the published objects can produce this pair (above).

The first three lines of the output only confirm that the object is the pair claim.md describes; exactness is the
REPRODUCE skeptic's check, not mine.

## 8. Its cell and the neighbouring cells

- p1 cell (10125 < b < 65537, p > 1e12): the only other known object is draft PR #973's (24766, 1000747824697), a
  different base and a different prime, so neither pair is an edit of the other. Fischer publishes no pair in this
  cell (no rows for bases 10126..65536, and his extreme-first-base files do not list p).
- Fischer's searched region and the full-win cell (b <= 10125): no base <= 10125 has p as a Wieferich prime (section 7),
  consistent with p's absence from FermQ_Sorg.txt, whose stated limit 4.8E+12 lies above p. Nothing published at
  b <= 10125 relates to this p.
- base 65537 (FermQ_Sort.txt's extra row): its row lists 2^16, 3, 131, 151, 163, and pow(65537, p-1, p^2) is not 1.
- bases above 65536: no source lists p.

## 9. Verdict

The bank counts each new pair once ("Each new pair counts once", claim/claim.md; the p1 line in section 5 matches the
bank text quoted in claim/claim.md). The pair lies in the p1 range, is absent from both Fischer tables (and from every
other Fischer file I fetched), absent from OEIS, absent from TROPHY_CASE.md, known-knowns/, releases and every pull
request of the V3R1T4S repository, absent from the literature and code I could search, and no trivial edit or
propagation of a published object yields it. It adds one pair beyond everything known in its cell: a strict
improvement, not a tie. Caveat recorded above: GitHub code search timed out once and was not repeated, and `gh api`
was refused by the permission settings; neither gap touches the bank's named sources (Fischer's tables and OEIS), which
were fetched and read in full.

pass: true
