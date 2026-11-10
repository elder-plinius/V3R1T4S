role: NOVELTY
context: claude code Task subagent (fresh context, saw only claim/)

context_note: before this task the harness auto-loaded the workspace's project instruction files (CLAUDE.md, HANDOFF.md, MISSION.md) into this subagent's context. This skeptic opened no workspace file other than those in claim/, its own scratch folder panel/work2-novelty/ and the placeholder line of this output file. Every finding below rests on its own fetches and computations.

# NOVELTY: Wieferich pair (28860, 1017279755641), partial win p1 of wieferich-other-bases-fischer-table

object: claim/object/pair.json = `{"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28860, "p": 1017279755641}`, sha256 `6f917770e4d29ea0863a3c1801b1d0f216e7d54316a6d4ba768b179fec8a4ed1`.

What "strictly beats everything known" means for this harvest target: the bank counts each new pair once, so the pair must not already be published or claimed, in its own cell or as a trivial consequence (propagation, relabelling, symmetry) of a published pair in a neighbouring cell.

How it was checked: every curl fetch used the User-Agent `V3R1T4S-agent/1.0 (open-research notebook; one honest request)`. Each URL was requested once, and no request was blocked, challenged or retried. Saved copies and outputs are in panel/work2-novelty/ (fetched copies in its fetched/ subfolder). GitHub URLs below show the account segment as (owner): the repository owner's handle is left out on purpose. Other read-only tools:
- gh, authenticated: `pr list` once; `search prs` with 6 queries; `pr view` 3 times for each of #973, #983 and #999 (different JSON fields; the first call's output was discarded by mistake); `search code` with 3 queries, `search issues` with 2, `search commits` with 1, `search repos` 3 times (the "wieferich" query twice, the second time for more fields);
- web search, 6 queries.

## 1. Status source, fetched once (primary table)

Command: `curl -sS -A '(UA above)' -o fetched/FermQ_Sorg.txt -w 'http_code %{http_code} size %{size_download} url %{url_effective}\n' 'http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt'`, between two `date -u` stamps, then `sha256sum`:

```
2026-11-07T21:08:48Z
http_code 200 size 288459 url http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
2026-11-07T21:08:48Z
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *FermQ_Sorg.txt
```

Value: own parser `table_rows.py` (latin-1 text; rows are lines that start with a base followed by a comma or by `P:`):

```
== FermQ_Sorg.txt ==
   line: Actual list from base 2 until 1052 and base 65537 see:
   line: Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125
   line: Die Basen sind gegenwaertig durchsucht bis 4.8E+12
   rows parsed: 10000; smallest base 2, largest base 10125
   bases with a row above 10125: []
   row for base 28860: False
   p 1017279755641 as a whole token anywhere: 0
```

The parser also printed the table's signature line, dated 21.10.2026. It is left out here because it carries a personal name. Reading:
- the table covers bases 2..10125 only, all of them searched to 4.8E+12;
- it has no row for 28860, and p appears nowhere in it;
- it is byte-identical to the scout's copy (claim/inputs/FermQ_Sorg.txt, same sha256; see section 2), so it has not changed since the scout's fetch at 2026-11-07T20:11:24Z (claim/status_sources.md).

## 2. The other Fischer files and OEIS, fetched once each

Fischer's index (http://www.fermatquotient.com/, fetched 2026-11-07T21:09:17Z, HTTP 200, 16104 bytes, sha256 `42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1`) links ten files in its FermatQuotienten/ folder. I fetched all ten. Fetch records:

```
2026-11-07T21:08:54Z http_code 200 size 33141 url http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
2026-11-07T21:09:00Z http_code 200 size 115771 url http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt
2026-11-07T21:09:09Z http_code 200 size 81696 url http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt
2026-11-07T21:09:39Z http_code 200 size 8500 url http://www.fermatquotient.com/FermatQuotienten/News.txt
2026-11-07T21:09:39Z http_code 200 size 8011 url http://www.fermatquotient.com/FermatQuotienten/Generelles.txt
2026-11-07T21:09:39Z http_code 200 size 24222 url http://www.fermatquotient.com/FermatQuotienten/Statistik.txt
2026-11-07T21:09:39Z http_code 200 size 11274 url http://www.fermatquotient.com/FermatQuotienten/FermatQ3.txt
2026-11-07T21:09:40Z http_code 200 size 10726 url http://www.fermatquotient.com/FermatQuotienten/SwitchFermQ.txt
2026-11-07T21:09:40Z http_code 200 size 28364 url http://www.fermatquotient.com/FermatQuotienten/PQuotient_Sort.txt
```

`sha256sum` (my copies, then the claim's inputs):

```
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *FermQ_Sort.txt
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 *ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 *ErstPBasen.txt
1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7 *News.txt
418d7557fa5bd72192af394901187e5f8d0b18826e1dd63b13988bb0cfae3e69 *Generelles.txt
dde1fa8d6c6105a74895dfb64646b7b74cb327a15aa7c49695f1c58ebabd2b2b *Statistik.txt
022855e8d16257ca4931bd9f7f9133012f17bbf1bc528f9a6cd12995b02a0a41 *FermatQ3.txt
8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa *SwitchFermQ.txt
375de4557fcf0569bf80040532606e7e2c1f9e7f2101d9878bc947ce95dce864 *PQuotient_Sort.txt
---
35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 *inputs/FermQ_Sorg.txt
bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b *inputs/FermQ_Sort.txt
e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 *inputs/ErstBasen.txt
3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 *inputs/ErstPBasen.txt
```

All four claim inputs are byte-identical to my fetches.

Second table, from the same parser (signature line dated 21.10.2026 left out):

```
== FermQ_Sort.txt ==
   line: Die gefundenen Primzahlen der Fermatquotienten von der Basis 2 bis 1052
   line: Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
   line: Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
   rows parsed: 982; smallest base 2, largest base 65537
   bases with a row above 10125: [65537]
   row for base 28860: False
   p 1017279755641 as a whole token anywhere: 0
```

No Fischer file has a row for any base in 10126..65536. The only base above 10125 in either table is 65537, which lies outside the p1 range.

Search of every fetched Fischer file and the index page. In the first column, digit-group separators (apostrophe, dot, comma, space, underscore) between digits were removed. The last column concatenates all digits of the file, which can only add false matches, never hide one:

```
ErstBasen.txt          sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
ErstPBasen.txt         sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
FermQ_Sorg.txt         sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
FermQ_Sort.txt         sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
FermatQ3.txt           sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
Generelles.txt         sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
News.txt               sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
PQuotient_Sort.txt     sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
Statistik.txt          sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
SwitchFermQ.txt        sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
fischer_index.html     sep-normalised p:0 b-as-token:0  all-digits-concatenated p:0
```

OEIS, query for p:

```
2026-11-07T21:10:36Z
http_code 200 size 6737 url https://oeis.org/search?q=1017279755641&fmt=data content_type text/html; charset=utf-8
2026-11-07T21:10:36Z
b518720451780beab298bf9e640fa531dc2136b315fd90a15651d88467861a8a *oeis_search_p.txt
contains Sorry phrase: True
A-numbers found: []
p occurrences in raw page: 6
```

The six occurrences are the query echoed by the page. The page text reads "Search: 1017279755641 / Sorry, but the terms do not match anything in the table."

OEIS, query for a Wieferich sequence that mentions 28860:

```
2026-11-07T21:16:59Z
http_code 200 size 6756 url https://oeis.org/search?q=wieferich+28860&fmt=data
2026-11-07T21:17:00Z
6a968f2336c2b2aa4ef8f20dbdec8a3f56c2ec3f4b14fa92b2dc2330f6c42047 *oeis_search_wieferich_28860.txt
Sorry phrase present: True
Search: wieferich 28860
A-numbers on page: []
page contains 1017279755641: False
```

The OEIS search reads sequence data and text, not b-files. Three kinds of table could hold this pair:
- (i) a base-28860 Wieferich sequence: the second query rules it out;
- (ii) a table of the smallest Wieferich prime of each base: it would list 7 for base 28860 (section 3), not p;
- (iii) a table of the least Wieferich base of each prime: its row for p would sit at an index of at least `36793768666` (own computation, the lower bound x/ln x). A b-file listing consecutive indices up to that row would have tens of billions of lines.

## 3. Neighbouring cells and trivial edits (own computation, Python standard library)

`python3 -B neighbours.py 28860 1017279755641 20000000`, started at 2026-11-07T21:11:16Z:

```
b = 28860, p = 1017279755641
pow(b, p-1, p^2) = 1
factorisation of b: {2: 2, 3: 1, 5: 1, 13: 1, 37: 1}
  q_p(2) mod p = 805472779928   (Wieferich for base 2? False)
  q_p(3) mod p = 647969670660   (Wieferich for base 3? False)
  q_p(5) mod p = 149508072110   (Wieferich for base 5? False)
  q_p(13) mod p = 515524916456   (Wieferich for base 13? False)
  q_p(37) mod p = 127891047841   (Wieferich for base 37? False)
sum of e*q_p(r) mod p = 0
bases 2..65536 with a^(p-1) == 1 mod p^2: [28860]   (0.3 s)
Wieferich primes to base 28860 below 20000000 (primes not dividing b): [7, 17, 1801]   (3.0 s)
primes dividing b (excluded): [2, 3, 5, 13, 37]
```

Reading, edit by edit:
- **Valid propagation rule.** For a fixed p, the Wieferich bases form a subgroup of (Z/p^2)*. So the only ways to derive a pair from published pairs are:
  - products, quotients and powers of other bases that are Wieferich for the same p;
  - the shifts b + k·p^2 and p^2 − b.

  For p = 1017279755641, 28860 is the only base in 2..65536. No pair (a, p) with another base a up to 65536 exists, published or not, from which (28860, p) could follow. 28860 is the least positive member of its class mod p^2, and none of its prime factors 2, 3, 5, 13, 37 is Wieferich for p.
- **Consistency with the published neighbouring cell.** FermQ_Sorg.txt covers every base 2..10125 to 4.8E+12, which is above p, and it lists no pair with this p. That agrees with the computation.
- **Relabelling.** 28860 = 2^2·3·5·13·37 is not a perfect power, so the pair is not a power-base copy of a smaller base's pair.
- **Symmetry.** The double-Wieferich swap (b, p) to (p, b) does not apply, because 28860 is not prime. SwitchFermQ.txt does not contain p, and neither do FermatQ3.txt (mod p^3) or PQuotient_Sort.txt (neighbour-base quotients).
- **Deletion, restriction, local numerical polish.** None of these has a meaning for one exact integer pair.
- **Same base, other primes.** Below 2·10^7, the Wieferich primes of base 28860 are 7, 17 and 1801. So p is not the first Wieferich prime of this base.

Published or claimed objects in the p1 cell itself (bases 10126..65536, p above 1e12):
- no Fischer file has a row in that range;
- the only other objects are three draft claims in this repository (section 4): (24766, 1000747824697), (28910, 1011548897263) and (17766, 1016845912283);
- none of them shares the base or the prime of this pair.

## 4. This repository: TROPHY_CASE.md, known-knowns/, sealed envelopes, releases, pull requests

Fetch records (owner segment redacted) and sha256:

```
2026-11-07T21:11:35Z http_code 200 size 2167895 url https://api.github.com/repos/(owner)/V3R1T4S/git/trees/main?recursive=1
2026-11-07T21:11:36Z http_code 200 size 31306 url https://raw.githubusercontent.com/(owner)/V3R1T4S/main/TROPHY_CASE.md
2026-11-07T21:11:36Z http_code 200 size 2 url https://api.github.com/repos/(owner)/V3R1T4S/releases?per_page=100
2026-11-07T21:12:04Z http_code 200 size 5492 url https://raw.githubusercontent.com/(owner)/V3R1T4S/main/known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md
2026-11-07T21:12:04Z http_code 200 size 6189749 url https://raw.githubusercontent.com/(owner)/V3R1T4S/main/bank/targets.json
2026-11-07T21:12:05Z http_code 200 size 2947 url https://raw.githubusercontent.com/(owner)/V3R1T4S/main/news/2026-10-19.md
2026-11-07T21:12:05Z http_code 200 size 1734 url https://raw.githubusercontent.com/(owner)/V3R1T4S/main/news/2026-10-26.md
2026-11-07T21:12:05Z http_code 200 size 1905 url https://raw.githubusercontent.com/(owner)/V3R1T4S/main/news/2026-11-02.md
93b7eef8c4a599e1c8925507d9f8ad7dbb3e982741af87c745c69000d6d73625 *repo_tree.json
83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 *TROPHY_CASE.md
4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 *releases.json
8395b2fe8a39df3816c850ea9279ab8931e3e3655b4b7ad69c7e437b8f520d52 *target_page.md
c2ee5ddad1634104acc41512e052dd4ab2c3af70d26cae8bc82f3af0bf6be65e *targets.json
96b58393fb43d32a6bed8995dfff7e73fcbe2fd58233bf5a22469d7419629e7f *news_2026-10-19.md
9364353e5d304a1adface321334eaf71e4332e2d73a528ccd29383521dbf0d62 *news_2026-10-26.md
8f152665b36b3f1e6d49f948130c41b1257b291e2cfd449404401ee41130063d *news_2026-11-02.md
```

Tree of main (parse of repo_tree.json):

```
tree sha: 06b61ea410a5ee90f3c9377a01d468c7cf05c0bd  truncated: False  entries: 7190
known-knowns entries: 5928
known-knowns target folders: 30
paths matching wieferich|fermat|fischer: 4
   known-unknowns/number-hunts/fermat-catalan-new-solution-with-square.md
   known-unknowns/number-hunts/fermat-numbers-new-factor.md
   known-unknowns/number-hunts/wieferich-base-2-beyond-2-64.md
   known-unknowns/number-hunts/wieferich-other-bases-fischer-table.md
paths containing 28860 or p: []
```

What the repository's main branch holds:
- **known-knowns/:** no folder for this target among its 30 target folders.
- **sealed-envelopes/:** two unrelated envelopes only (bouchaudy-cipher-machines, vesuvius-first-letters-unread).
- **Releases:** the releases endpoint returned `[]`.
- **TROPHY_CASE.md** (100 lines): `grep -n -i -E 'wieferich|fermat|fischer|28860|1017279755641'` printed nothing.
- **Target page, bank/targets.json and the three news files:** `grep -n -i -E '28860|1017279755641'` printed nothing.
- **Criterion:** targets.json's entry for this target gives the p1 statement exactly as quoted in claim/claim.md.

Pull requests, all states, `gh pr list --state all --limit 3000`:

```
2026-11-07T21:12:22Z
total PRs listed: 959
number range: 1 .. 1007
states: Counter({'OPEN': 428, 'CLOSED': 350, 'MERGED': 181})
PRs whose title or branch matches wieferich|fermat|fischer|mirimanoff|quotient|28860|p: 3
#973 OPEN draft=True 2026-11-07T13:02:22Z | [claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1
#983 OPEN draft=True 2026-11-07T16:47:06Z | [claim] wieferich-other-bases-fischer-table: Wieferich pair (28910, 1011548897263), partial win p1
#999 OPEN draft=True 2026-11-07T19:01:07Z | [claim] wieferich-other-bases-fischer-table: Wieferich pair (17766, 1016845912283), partial win p1
```

`gh search prs` in the repository (titles, bodies and comments; any state), run at 2026-11-07T21:12:42Z:
- "1017279755641": 0 results;
- "28860": 0 results;
- "wieferich", "fermatquotient" and "Fermat quotient": the same 3 results each, #973, #983 and #999;
- "Fischer": those 3 plus #700, an unrelated bank PR (symmetric-rendezvous-records).

The search index can lag, so I also read the titles of all 36 PRs created on 2026-11-07 (#972 to #1007). None besides #973, #983 and #999 concerns Wieferich pairs.

`gh pr view` of #973, #983 and #999, run at 2026-11-07T21:13:03Z (body, comments, reviews and file paths). The excerpt below leaves out the title and folder lines, because the folder names carry the claimant's handle:

```
#973 OPEN draft=True head=17514eb files=23 comments=0 reviews=0
   occurrences in body+comments+reviews+paths: p= 0  b=28860: 0
   (b, p) pairs written in the body: [('24766', '1000747824697')]
#983 OPEN draft=True head=c9d7d27 files=23 comments=0 reviews=0
   occurrences in body+comments+reviews+paths: p= 0  b=28860: 0
   (b, p) pairs written in the body: [('24766', '1000747824697'), ('28910', '1011548897263')]
#999 OPEN draft=True head=48cd4ea files=23 comments=0 reviews=0
   occurrences in body+comments+reviews+paths: p= 0  b=28860: 0
   (b, p) pairs written in the body: [('17766', '1016845912283'), ('24766', '1000747824697'), ('28910', '1011548897263')]
```

Package files of the three PRs: raw files at each PR's head commit. That was 28 GETs, "total 28, HTTP 200: 28", from 2026-11-07T21:13:55Z to 21:14:09Z. They covered object/pair.json, README.md, HOW_WE_FOUND_IT.md, the-record-we-beat/RECORD.md, panel/gate.md, hit_block_record.json, PREREG.md and INDEX.csv for each PR, plus panel/novelty.md, REBUILD_OUTPUT.txt, p1_known_positives.py and verify.py for #999. Results:

```
#973 object/pair.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 24766, "p": 1000747824697}
#983 object/pair.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 28910, "p": 1011548897263}
#999 object/pair.json: {"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 17766, "p": 1016845912283}
== all (b, p)-looking pairs named in the fetched PR files ==
      5 (17766, 1016845912283)
     12 (24766, 1000747824697)
      1 (28860, 1017279755641)
      7 (28910, 1011548897263)
```

The single mention of this pair is line 37 of #999's panel/gate.md. It lists (28860, 1017279755641) under "Not claimed", as an exact pair of the same run that "stays PROMISING until its own panel". It is a disclosure in the claimant's own open draft PR, whose object is a different pair. It is neither a competing claim nor a published record, so no double count arises: no PR claims this pair.

## 5. Literature and code, last 24 months

GitHub-wide searches (`gh search`, 2026-11-07T21:14:57Z):
- code "1017279755641": 0; code "28860 1017279755641": 0; code "wieferich 28860": 0;
- issues and PRs "1017279755641": 0; commits "1017279755641": 0;
- issues and PRs "wieferich 28860": 100 results. All 100 are items numbered 28860 in unrelated repositories, and 0 mention Wieferich or Fermat (counted).

Wieferich repositories pushed in the last 24 months (`gh search repos "wieferich" --sort updated`):
- **A GPU search repository named wieferich-base-search** (created 2026-06-07). It covers 27 bases from 186 to 986, with primes in (4.4·10^12, 10^14], and reports a null result. Its releases endpoint returned `[]`, and its README.md and report/findings_summary.md contain neither 28860 nor p (`grep` counts 0). Fetch records:
  - tree: 21:15:32Z, HTTP 200, sha256 `6811b04b971bde344ebd7a766bb9309b3140da5581fd634cbca29a1adbeb96e4`;
  - releases: 21:15:33Z, HTTP 200, `[]`;
  - README.md: 21:15:43Z, HTTP 200, sha256 `486f4731754ef6621a865fac95c1d544dc402f46370dff2fb08c73374dc6b00b`;
  - findings_summary.md: 21:15:43Z, HTTP 200, sha256 `e0d47b39dd38f1302e470d53466995506856727d60523850d4ec645be9c36592`.
- **A browser-demo repository named wieferich** (created 2026-06-07). Its releases endpoint returned `[]`, and its README.md and index.html contain neither 28860 nor p. Fetch records:
  - tree: 21:15:33Z, HTTP 200, sha256 `1adb0bcdc45b1aaab78349cfa1568acfdedf02273e920b795942669deb863551`;
  - releases: 21:15:34Z, HTTP 200, `[]`;
  - README.md: 21:15:43Z, HTTP 200, sha256 `f7b2d368671a67e373d4994d0649128cf7c18450e2e6dd7591b0ba4ab887301e`;
  - index.html: 21:15:44Z, HTTP 200, sha256 `66e54ae541dd5d14e52e6f5979a5f11368f7fd113a84b81a714eea3f55474437`.
- **Others:** a BOINC OpenCL program for Wieferich and Wall-Sun-Sun primes (created 2026-08-17) and three single-problem candidate-research repositories on Wieferich-type questions (created 2026-09-16). The GitHub-wide code search above finds p in none of them.
- The only "fermat quotient" repository found is an optimisation project (pushed 2026-11-05) unrelated to Wieferich pairs.

Web search: six queries, run between the fetches stamped 21:15:44Z and 21:16:59Z:
- `"1017279755641"`
- `Wieferich prime base 28860`
- `Wieferich primes to bases above 10125 Fermat quotient search 2025 2026`
- `arXiv 2025 2026 Wieferich primes many bases computational search new pairs`
- `"28860" "1017279755641" OR "28860^" Wieferich OR "Fermat quotient"`
- `Wieferich primes bases up to 65536 table b^(p-1) == 1 mod p^2`

No result mentions p, or any Wieferich pair for base 28860, or any table of Wieferich pairs for bases between 10126 and 65536. The newest search papers returned are Dorais and Klyve (2011) and older work. The other results are OEIS tables and expository notes for small bases or small primes.

## 6. Verdict

- **Status source:** fetched once (2026-11-07T21:08:48Z, HTTP 200, sha256 35273a26...e45ff4, "durchsucht bis 4.8E+12", bases 2..10125). It is unchanged since the scout's fetch, has no row for base 28860 and does not contain p. FermQ_Sort.txt is also unchanged and has no row in 10126..65536.
- **OEIS:** no match for p, and no Wieferich sequence that mentions 28860.
- **Neighbouring cells:**
  - no published pair shares this p;
  - no other base up to 65536 is Wieferich for this p, so no propagation, relabelling or symmetry of any pair can produce (28860, p);
  - 28860 is not a perfect power.
- **Repository:** no trophy, known-knowns entry, sealed envelope, release or pull request claims the pair. Its one public trace is an explicitly unclaimed mention in the claimant's own draft #999.
- **Last 24 months:** no literature, code or release found contains it.
- **Scope:** this check covers the sources listed above. It does not cover sources outside them (unindexed, private or paywalled material).

novelty: The pair (28860, 1017279755641) appears in none of the ten Fischer Fermat-quotient files (each fetched once; the four claim inputs are byte-identical), in OEIS, in this repository's TROPHY_CASE.md, known-knowns/, sealed envelopes, releases or any of its 959 pull requests (apart from an explicitly unclaimed mention in the claimant's own draft #999), nor in any literature or code found from the last 24 months, and no trivial edit of a published pair can produce it because no other base up to 65536 is Wieferich for this p, so it adds one strictly new pair to the p1 cell.

pass: true
