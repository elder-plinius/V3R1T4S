# Novelty skeptic: A002224(42) = 6072205049848081

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

target id: least-qnr-prescribed-quadratic-character-next-terms
cell: A002224(42), the least prime p = 1 (mod 8) such that the first 42 primes (2..181) are quadratic residues mod p
claimed value: 6072205049848081 (claim/CLAIM.md, claim/result/a002224_42.json)

Question checked here: is A002224(42) already published? That covers the OEIS entry and b-file, the data of any other
sequence that implies it, the literature and code from the last 24 months, and earlier pull requests or results of
github.com/elder-plinius/V3R1T4S. Whether the value is correct and minimal is for the other skeptics.

## 1. Status source (one plain GET each, User-Agent "V3R1T4S-agent (research notebook)", no retries)

| URL | fetched (UTC) | HTTP | sha256 | note |
|---|---|---|---|---|
| https://oeis.org/A002224 | 2026-11-27T16:44:41Z | 200 | a4b9d7a82025088915d1ed891ddc5839bbc69c80d4e34227fefcc217467dcbb3 | real entry page, not a challenge page (21025 bytes) |
| https://oeis.org/A002224/b002224.txt | 2026-11-27T16:44:42Z | 200 | 70fa340ea4ea5035017afad7742632f61ae03c75cafdcf7ab0e69f2b99579ce8 | 532 bytes, byte-identical to claim/data/b002224.txt |
| https://oeis.org/search?q=6072205049848081&fmt=short | 2026-11-27T16:44:59Z | 200 | 7f17969c522400df263e1090b79041208cd0679626044137a4b673ce42a43408 | "Sorry, but the terms do not match anything in the table." |
| https://oeis.org/history?seq=A002224 | 2026-11-27T16:45:20Z | 200 | 5be5fa867891b40e1f0e62eb7680f1f9eea29eabb733aea3d14ba34fe4f71475 | newest revision #63, approved, no pending draft |

Quoted from the fetched b-file, last line: `41 178936222537081`. There is no line for n = 42.

Quoted from the fetched entry page:
- name: "Smallest prime p of form p = 8k+1 such that first n primes (p_1=2, ..., p_n) are quadratic residues mod p."
- links: "Michael Hortmann, Table of n, a(n) for n = 1..41"
- extensions: "More terms from Don Reble, Sep 19 2001" and "More terms from Mike Oakes, Nov 28 2022"
- keywords: "nonn, nice, changed"
- footer: "Last modified November 27 11:41 EST 2026. Contains 402066 sequences."

The page differs from claim/data/A002224.html (fetched 16:27:36Z) only in Cloudflare beacon tokens and the footer
time (11:41 vs 11:26 EST). The keyword "changed" comes from cross-reference edits: history revisions #56 to #63 by
Jianing Song (approved by Michael De Vlieger, Mon Nov 16 15:48:56 EST 2026) change only CROSSREFS (A002189, A045535,
A399983). No revision adds a term, and no pending draft is shown.

## 2. Sequences whose data could imply A002224(42) (one fetch each)

For a prime p = 1 (mod 8), reciprocity gives (q/p) = (p/q) for every odd prime q, and (2/p) = 1. So A002224(n) is the
least prime among the integers that A002189 (the pseudosquares) minimises over. A002189 therefore implies the cell
only when its term is prime.

| URL | fetched (UTC) | HTTP | sha256 | what it gives for this cell |
|---|---|---|---|---|
| https://oeis.org/A002189/b002189.txt | 16:45:14Z | 200 | 77bb28a622f2eb545a13b7c4760795481e71e40034b8bdb3c635e3917a84e5bc | `41 696161110209049`, `42 696161110209049`, `43 2854909648103881`, `44 6450045516630769`, `45 6450045516630769` (indexed by odd primes: a(41) = L_181, a(43) = L_193, a(44) = L_197) |
| https://oeis.org/search?q=id:A002189&fmt=text | 16:45:16Z | 200 | bca439e07d6de5c556111b1055b8c3bed3e239dccb7072f83170c07a26745df0 | definition; the b-file to n = 73 is "from Bernstein link" |
| https://oeis.org/search?q=id:A401222&fmt=text | 16:45:18Z | 200 | 927962b1a17e910eefceeea59fb9adb958f7150f47cc1dab3f5685c3cf348699 | "Records in A002189." (Nov 16 2026), not prime-restricted |
| https://oeis.org/search?q=id:A399983&fmt=text | 16:46:01Z | 200 | 3a3220812089e9e56566622bf437152442d1207406129c0a27e0ad612015048b | class numbers of A002224 terms; data ends at term 41 ("...,1,65,65"); keyword "more"; its table lists the sibling sequences checked below |
| https://oeis.org/search?q=id:A102295&fmt=text | 16:46:34Z | 200 | 6c59cf373ba98ac4c73c0b1d07e0aa76883d2e39ca45946a3ff47a8055770d03 | records of A002224; data ends 178936222537081; "More terms copied from A002224 by Jianing Song, Nov 16 2026" |
| https://oeis.org/A102295/b102295.txt | 16:46:36Z | 200 | 9339dc12f7608e76062ee4d990376c82eba97272acbee309d6ae4b70def7f111 | "b-file synthesized from sequence entry", last line `30 178936222537081` |
| https://oeis.org/search?q=id:A402321&fmt=text | 16:46:43Z | 200 | 34208c510ec9e53f0259e305db4a91479503e539620d29563b15f66a987e816e | class numbers of A102295, 29 terms, ends at 65 (the class number of 178936222537081) |
| https://oeis.org/search?q=id:A147972&fmt=text | 16:46:39Z | 200 | 02f51a92189d4fda97db5f3deac606d0c001d00650291e91f02f37be0fc8a10a | min(A002224, A002223) |
| https://oeis.org/A147972/b147972.txt | 16:46:41Z | 200 | 7326b1a73cb2ff5316af897afbad818fdb5b3a266d786bef8dcc0120414292e8 | last line `37 70864718555231`, so it stops before n = 42 |
| https://oeis.org/search?q=id:A002223&fmt=text | 16:46:04Z | 200 | b022a15750ca710b81e552a1a4d54a1340bc440f9afb962179000dd372c3a034 | the 8k-1 version; its terms are 7 mod 8 and cannot equal a 1 mod 8 term |
| https://oeis.org/A002223/b002223.txt | 16:48:17Z | 200 | 2e6b7bdde46a35f33e84ed84e9e68b14b94628721c5450cd4d82df0db5650ba3 | last line `57 3546374752298322551` |
| https://oeis.org/search?q=id:A000229&fmt=text | 16:46:06Z | 200 | 8f36ad835b66468a2b79e0703635af61f597e41f6cd6fbe8450bf1eac4c38ee7 | b-file "for n = 1..38"; least QNR = prime(n), no class restriction; does not fix the least 1 mod 8 prime |
| https://oeis.org/search?q=id:A133435&fmt=text | 16:46:45Z | 200 | 1030f5deaf18b06911ab006be76c382edab8c2fd5bd0e49a2058efcec420ff0c | records of A000229; data ends 70864718555231 |
| https://oeis.org/search?q=id:A045535&fmt=text | 16:48:08Z | 200 | 86e2d813eea13b6f9c523ac71ccfcf2c681d5a68c21ad7ecafb93dc04f6ed8f1 | negative pseudosquares (7 mod 8), table n = 0..50; other residue class |
| https://oeis.org/search?q=id:A001992&fmt=text | 16:48:11Z | 200 | e6c4250bc8e963ab21eacdc47ef1acba40a3bbb776bc971637f62f65ccc63f7e | 5 mod 8 version, table n = 1..55; other residue class |
| https://oeis.org/search?q=id:A002225&fmt=text | 16:48:13Z | 200 | c5a7e720861343c0831cb1640480dd52baebeb2e9ced737edbb820b048bff6c7 | cube roots; different property |
| https://oeis.org/search?q=id:A002226&fmt=text | 16:48:15Z | 200 | 84e300039313d39dbd865f381acd3e4eaec706563f7c0f44a130dfbdc75edd82 | quintic residues; different property (links github.com/jhg023/first-knowns, checked in section 4) |

All times are 2026-11-27. The claimed value occurs in none of the fetched files: `grep -l 6072205049848081` matched
only the OEIS search page, which echoes the query.

Checking whether A002189 implies the cell (my own Miller-Rabin with the 13 prime bases up to 41, deterministic in
this range, plus trial division):
```
696161110209049 composite mod8= 1 smallfactor= 3793 least_qnr= None
2854909648103881 composite mod8= 1 smallfactor= 331 least_qnr= None
6450045516630769 composite mod8= 1 smallfactor= None least_qnr= None
6072205049848081 prime mod8= 1 smallfactor= None least_qnr= 197
```
L_181 = L_191 and L_193 are composite, so A002189 gives only the lower bound A002224(42) > 696161110209049. It does
not determine the cell. The claimed value falls between L_193 and L_197 (2854909648103881 < 6072205049848081 <
6450045516630769), which agrees with its least QNR of 197, so it contradicts no published pseudosquare. No published
sequence I found gives A002224(42).

## 3. Literature (last 24 months, plus the classical tables the entries cite)

- Web search for "6072205049848081": no relevant hit (all results unrelated: datasheets, government PDFs). Searching
  for the neighbour "178936222537081" found no page discussing it either.
- Web searches for "A002224", prime pseudosquares and "prescribed quadratic character" (2025, 2026), and for least
  quadratic non-residue computations on arXiv (2024 to 2026). The hits were theoretical bounds only (arXiv:2607.14515,
  2106.00544, 2404.08380, 2405.13159, 2512.24147, 2611.00485). None reports a new term of A002224.
- Sorenson, arXiv:1001.3316 (PDF fetched via WebFetch, sha256
  58959c861df5582634a11fe1197023da5ad1014eb6c245617ab57f20f5099798). Its table lists only the least pseudosquares
  (`42 181 696161110209049`, `44 193 2854909648103881`, `45 197 6450045516630769`). The claimed value is absent.
- Bernstein, https://cr.yp.to/focus.html (2026-11-27T17:03:45Z, HTTP 200, sha256
  a3cc4590b63dc680bd515b1242aac657c5070c92e7888197dd4be0a521f2d537), and its paper
  https://cr.yp.to/focus/focus-20030928.pdf (17:03:54Z, HTTP 200, sha256
  8f0b40557c7d0095bb2c277c8a35bf9fd06a2451d53c2bb23b71fa118724cdae). Both list only the least pseudosquares
  (`181 ... 696161110209049`, `193 ... 2854909648103881`). The claimed value is absent.
- Oliveira e Silva, https://sweet.ua.pt/tos/p_roots.html (16:47:16Z, HTTP 200, sha256
  8dc77b8aa2ca12da41a1358c6e7696c7f8fe9ea5b9043d367bb8a170e0c8f7f0), with its 10^16 table
  https://sweet.ua.pt/tos/p_roots/tX.txt.gz (16:47:34Z, HTTP 200, sha256
  4d9e7dd25a3d132052b1b0d30a268069101996d70aadbd02a164735b2fe857a5) and
  https://sweet.ua.pt/tos/p_roots/t2.txt.gz (16:47:36Z, HTTP 200, sha256
  b3a378d7f2acd4f1e62aec0f5ab9c29362e044798c7a342db64351d0b86f1dae). These record first occurrences of least
  (prime) primitive roots, not least 1 mod 8 primes with a prescribed character. The claimed value is in neither
  table.
- Lukes, Patterson and Williams (1996). The PDF
  https://www.ams.org/mcom/1996-65-213/S0025-5718-96-00678-3/S0025-5718-96-00678-3.pdf answered HTTP 403
  (17:06:17Z), and I did not retry. Bronson and Buell (PSAM 48, 1994) is not online. OEIS cites Bronson and Buell for
  A002223 ("gives terms through prime(n) = 227") and for A045535, but not for A002224, whose terms past n = 35 were
  added in 2022 (Mike Oakes) and curated again on Nov 16 2026 without new terms. I did not read these two papers
  directly. This is a residual gap, but a 1 mod 8 table to 227 in them would very likely have reached A002224 by now.

## 4. Code and repositories

- GitHub code search: "6072205049848081" returned 0 results. "least-qnr-prescribed-quadratic-character" returned only
  the two V3R1T4S target pages. "A002224" plus pseudosquare returned 0. The hits for the neighbours 178936222537081
  and 696161110209049 are pseudosquare tables and OEIS b-file mirrors (flintlib/flint, kimwalisch/Pseudosquares-Prime-Sieve,
  ashallue/tabulate_car, pietrotiaraju/oeis-python-golf and others). The claimed value is in none of them, since its
  code search returned 0.
- github.com/jhg023/first-knowns, cloned at HEAD a67309f (2026-11-24) because A002226 links it. Its residue-ladders
  project covers A002226, A002227, A002228, A060363 and A060364, not A002224. A grep for A002224, A002189 and the value
  found no hit. It has no tags (git ls-remote --tags is empty), so it has no release assets.

## 5. This repository: github.com/elder-plinius/V3R1T4S

- Read-only clone at HEAD 4798bb448561d3f174b911f556d8092ee5c8ac17 (2026-11-27T08:34:08-08:00), cloned
  2026-11-27T16:48:34Z. A grep over the whole tree for A002224, 6072205049848081, least-qnr and "prescribed quadratic"
  matched only known-unknowns/number-hunts/least-qnr-prescribed-quadratic-character-next-terms.md, the README table
  row, bank/targets.json and SHA256SUMS. TROPHY_CASE.md, known-knowns/ (50 families, none for this target) and
  sealed-envelopes/ have no hit. The target page still reads "open as of 2026-10-30" and lists "A002224 (n = 42)" as
  the next unknown index.
- Releases: `git ls-remote --tags origin` printed nothing, so there are no tags and no release assets. The HTML page
  https://github.com/elder-plinius/V3R1T4S/releases answered 403 through the proxy (17:02:26Z), not retried.
- Pull request search (gh api search/issues, 2026-11-27T16:49:07Z and 17:04:15Z), open and closed, title and body:
  - A002224, least-qnr, A000229, A002223, qnr and "A002224(42)" each matched exactly one PR, #862.
  - 6072205049848081, pseudosquare, pseudo-squares, nonresidue, A002189, A045535, A001992 and A102295 matched none.
  - quadratic, prescribed and non-residue matched only #862 plus PRs on unrelated targets.
  - Issue search for A002224 and least-qnr: 0.
- PR #862 (open, created 2026-10-31T05:34:24Z by HindsightWise), title "[claim]
  least-qnr-prescribed-quadratic-character-next-terms: exact A000229(39..43) and A002224(39, 41) via dual-CRT census
  (p1)". Its body says verbatim: "No value is claimed for `A000229(44)` (least QNR $p_{44} = 193$) or `A002224(42)`."
  I fetched its head (7c3518f19f6ee0c348ecce96f39570c7ebc61367, 2026-10-30T21:04:45-07:00) with `git fetch --depth 1
  origin pull/862/head`, and a grep of its package for 6072205049848081 found nothing. Its Stage 2 census lists the
  primes up to 1463971373078639 that have the first 40 primes as QRs. The only 1 mod 8 one is 178936222537081 (least
  QNR 181); the other four are 7 mod 8 (my own check). So #862 implies at most the lower bound A002224(42) >
  1463971373078639. That bound is unreviewed and agrees with the claim. It does not give the value.
- Every PR head: all 1200 refs/pull/*/head were fetched shallowly and searched with `git grep -F 6072205049848081`.
  The run started at 2026-11-27T16:51:11Z, ended at 17:08:35Z and printed `value hits: 0`. No PR head anywhere in the
  repository contains 6072205049848081. As a positive control, the same `git grep` on refs/pr/862 finds
  1463971373078639 in that PR's INDEX.csv, README.md and HOW_WE_FOUND_IT.md.

## 6. Comparison with published objects for this cell and its neighbours

The object is a single sequence term at an index (n = 42) strictly beyond the live b-file (last n = 41). It is not
built from a published object by deletion, restriction, relabelling or any propagation rule. The neighbouring cells
give only bounds:
- A002224(41) = 178936222537081 has least QNR 181, so it is not a candidate.
- A002189 gives A002224(42) > L_181 = 696161110209049, because L_181 = L_191 and L_193 are composite.
- PR #862 gives a lower bound of 1463971373078639.
None of these yields 6072205049848081. A new term at an empty index cannot be a tie. No published value exists to tie
or beat, and the claim fills a cell that is empty in every source checked.

## Verdict

novelty: NEW. A002224(42) = 6072205049848081 is not in the OEIS entry or b-file (live b-file ends `41
178936222537081`, sha256 70fa340e...ce8, unchanged since the scout fetch). It is in no OEIS sequence data (the OEIS
search finds no match), is not implied by any sibling sequence (the A002189 terms at L_181, L_191 and L_193 are
composite; A102295, A399983, A402321 and A147972 stop at or before n = 41), and appears in no literature or code found.
It is not in TROPHY_CASE.md, known-knowns/ or sealed-envelopes/. No earlier pull request claims it: the only related
PR, #862 (2026-10-31), explicitly does not claim A002224(42), and its tree does not contain the value. Residual
gaps: the Bronson and Buell (1994) and Lukes, Patterson and Williams (1996) tables could not be read (offline or 403).
This verdict concerns novelty only; correctness and minimality are left to the reproduce and criterion skeptics.

pass: true
