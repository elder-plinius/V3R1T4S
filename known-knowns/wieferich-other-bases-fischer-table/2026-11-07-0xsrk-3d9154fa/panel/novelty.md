role: NOVELTY
context: claude code headless session (claude -p --safe-mode in a copy of claim/ outside the workspace; fresh context, saw only claim/)

# Novelty check: Wieferich pair (b, p) = (56350, 1024048960667), target wieferich-other-bases-fischer-table, partial win p1

Object: claim/object/pair.json = `{"target_id": "wieferich-other-bases-fischer-table", "partial_win": "p1", "b": 56350, "p": 1024048960667}`.
Cell: base 56350 (inside the p1 band of bases above 10125 and below 65537), prime p = 1024048960667. The bank counts each new
pair once, so the bar is that this exact pair is absent from every known source and not obtainable by trivial edits of a
published pair.

## 1. Sanity re-run of the claim's checker (work/verify_out.txt)

`python3 -B -I claim/verify.py claim/object/pair.json`:

```
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 56350, p = 1024048960667, Fermat quotient q_p(b) mod p = 0
PASS
```

## 2. Fetch records (one request per source, curl with the kit User-Agent, no retries)

UTC time is the `date -u` output taken immediately before each curl; HTTP status is curl's `%{http_code}`; sha256 is
`sha256sum` of the saved file. GitHub URLs have the owner segment replaced by [repository owner].

| source | URL | UTC time (date -u) | HTTP | sha256 of saved file |
|---|---|---|---|---|
| Fischer, bases 2..10125 (bank status source) | http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt | Sat Nov  7 22:05:41 UTC 2026 | 200 | 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 (work/fetch/FermQ_Sorg.txt) |
| Fischer, bases 2..1052 and 65537 | http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt | Sat Nov  7 22:05:47 UTC 2026 | 200 | bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b (work/fetch/FermQ_Sort.txt) |
| Fischer, extreme first bases | http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt | Sat Nov  7 22:05:55 UTC 2026 | 200 | e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 (work/fetch/ErstBasen.txt) |
| Fischer, extreme first prime bases | http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt | Sat Nov  7 22:06:01 UTC 2026 | 200 | 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 (work/fetch/ErstPBasen.txt) |
| Fischer, index page | http://www.fermatquotient.com/ | Sat Nov  7 22:06:08 UTC 2026 | 200 | 42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1 (work/fetch/fischer_index.html) |
| OEIS search for p | https://oeis.org/search?q=1024048960667&fmt=data | Sat Nov  7 22:06:13 UTC 2026 | 200 | 107b5fb7daf9672e5a83a0d7a92413ac942992f681e06c7851a7a2dbdc692000 (work/fetch/oeis_p.txt) |
| V3R1T4S tree (GitHub API, recursive) | https://api.github.com/repos/[repository owner]/V3R1T4S/git/trees/HEAD?recursive=1 | Sat Nov  7 22:07:33 UTC 2026 | 200 | 93b7eef8c4a599e1c8925507d9f8ad7dbb3e982741af87c745c69000d6d73625 (work/fetch/repo_tree.json) |
| V3R1T4S TROPHY_CASE.md at the tree commit | https://raw.githubusercontent.com/[repository owner]/V3R1T4S/06b61ea410a5ee90f3c9377a01d468c7cf05c0bd/TROPHY_CASE.md | Sat Nov  7 22:07:55 UTC 2026 | 200 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 (work/fetch/TROPHY_CASE.md) |
| V3R1T4S releases (GitHub API) | https://api.github.com/repos/[repository owner]/V3R1T4S/releases?per_page=100 | Sat Nov  7 22:08:06 UTC 2026 | 200 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 (work/fetch/releases.json, 2 bytes) |
| hit record of the nearest open Wieferich claim (PR 1008, at its head commit) | https://raw.githubusercontent.com/[repository owner]/V3R1T4S/0c73d33ed52f463d93e021639ef3f5331b888ced/known-knowns/wieferich-other-bases-fischer-table/(PR 1008 claim folder)/how-we-built-it/hit_block_record.json | Sat Nov  7 22:09:23 UTC 2026 | 200 | 98d15b639558e1ca595e9ea076b6d13e52694a0c1f7e7bbaf00f2804b00e5fca (work/fetch/pr1008_hit_block_record.json) |
| Fischer, news and records | http://www.fermatquotient.com/FermatQuotienten/News.txt | Sat Nov  7 22:09:43 UTC 2026 | 200 | 1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7 (work/fetch/News.txt) |
| a third-party GitHub repository named "wieferich" (updated 2026-06-08), file tree | https://api.github.com/repos/[third-party owner]/wieferich/git/trees/HEAD?recursive=1 | Sat Nov  7 22:08:49 UTC 2026 | 200 | 1adb0bcdc45b1aaab78349cfa1568acfdedf02273e920b795942669deb863551 (the third-party tree JSON in work/fetch/) |

No request was blocked, challenged or rate-limited. The live Fischer files are byte-identical to the scout's copies
(the four sha256 values equal those in claim/status_sources.md). The OEIS page hash differs from the scout's, as expected for a dynamic page;
the result text is the same.

## 3. Absence from the published tables

Fischer's index page (work/fetch/fischer_index.html) lists FermQ_Sort.txt as "List from base 2 until 1052 and base 65537 /
Update 21.10.2026" and FermQ_Sorg.txt as "List from base 2 until 10125 / Update 21.10.2026"; no Fischer table covers
bases 10126..65536. FermQ_Sorg.txt header: "Die Basen sind gegenwaertig durchsucht bis 4.8E+12".

Row parse of the live files (work/code/fischer_rows.py, output work/out/fischer_rows.txt; the row parse is meaningful
only for the two tables, the other files were only text-searched):

```
FermQ_Sorg.txt rows: 10001 min base: 2 max base: 10125 bases > 10125: [] row for 56350: False p present: False
FermQ_Sort.txt rows: 983 min base: 2 max base: 65537 bases > 10125: [65537] row for 56350: False p present: False
ErstBasen.txt ... row for 56350: False p present: False
ErstPBasen.txt ... row for 56350: False p present: False
```

A text search of every fetched file for `1024048960667|56350[^0-9]|102404896` matched only the OEIS page's own echo of
the query (title, search box, "Search:" line). News.txt has no match.

OEIS (work/fetch/oeis_p.txt): line 101 `Search: 1024048960667`, line 116 `Sorry, but the terms do not match anything in the table.`
So no OEIS sequence (including any base-b Wieferich sequence) contains p.

## 4. Trivial edits and propagation from published pairs (work/code/scan_bases.py, output work/out/scan_bases.txt)

The Fermat quotient q_p is a homomorphism from (Z/p^2)^* to Z/p, so products and quotients of Wieferich bases for p,
p-th-power multiples and sign changes (which give numbers of size about p^2) are the trivial ways to get a new base for the same p.
A pair is trivially derivable only if some published base already has this p. Exact scan of every base up to 70000:

```
p = 1024048960667
factorisation of 56350: {2: 1, 5: 2, 7: 2, 23: 1}
q_p(2) mod p = 366008234196  (exponent 1)
q_p(5) mod p = 29806142339  (exponent 2)
q_p(7) mod p = 70436202038  (exponent 2)
q_p(23) mod p = 457556037717  (exponent 1)
sum e*q_p(r) mod p = 0
q_p(56350) mod p = 0
bases 2..70000 with b^(p-1) == 1 mod p^2: [56350]
any hit <= 10125: False
base 65537 Wieferich for p: False
smallest Wieferich base for p in 2..70000: 56350
```

56350 is the only (hence smallest) Wieferich base for this p up to 70000. No base in Fischer's tabulated range (2..10125
and 65537) has this p, so no published pair with this prime exists. Therefore the pair cannot come from deletion,
restriction, products or quotients of published bases, relabelling, or the b to -b symmetry. 56350 is not a perfect power, so it is not a
repeat of a smaller base's pair. The claim does not say it was seeded from a published object, and none exists for this p.

## 5. This repository: TROPHY_CASE.md, known-knowns/, pull requests, releases

- Tree at commit 06b61ea410a5ee90f3c9377a01d468c7cf05c0bd (work/out/tree_paths.txt): `sha: 06b61ea410a5ee90f3c9377a01d468c7cf05c0bd truncated: False entries: 7190`.
  Paths matching wieferich or fermat: none. known-knowns/ has a single top-level folder, `known-knowns/bigger-codes`.
- TROPHY_CASE.md: search for `wieferich|fermat|1024048960667|56350` (case-insensitive): `No matches found`.
- Releases: the API returned a 2-byte body (no releases), so there are no release assets that could lag the tree.
- Pull requests, all states (`gh pr list --state all --limit 3000`, work/out/prs_wieferich_all.txt):
  ```
  total PRs listed: 960
  number range: 1 - 1008
  states: {'MERGED': 181, 'CLOSED': 350, 'OPEN': 429}
  973 OPEN 2026-11-07T13:02:22Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (24766, 1000747824697), partial win p1
  983 OPEN 2026-11-07T16:47:06Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (28910, 1011548897263), partial win p1
  999 OPEN 2026-11-07T19:01:07Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (17766, 1016845912283), partial win p1
  1008 OPEN 2026-11-07T21:41:22Z [claim] wieferich-other-bases-fischer-table: Wieferich pair (28860, 1017279755641), partial win p1
  ```
  These four open claims each name a different pair with a different prime, and none has been merged. The Wieferich property is per prime, so
  none of them implies or duplicates this pair. The nearest one (PR 1008) records its swept block in hit_block_record.json:
  `{"lo": 1017260000000, "hi": 1017280000000, ... "hits": [[28860, 1017279755641]], ...}`. This prime is outside that block.
- `gh search prs 1024048960667` in this repository, open: `[]`; closed: `[]`. `gh search issues 1024048960667`: `[]`.
  `gh search prs wieferich`: only the four PRs above.

## 6. Literature and code, last 24 months

- Web search (extended) for "1024048960667": no page mentions the number (only unrelated digit strings).
- Web search "Wieferich pair base 56350": nothing on this base.
- Web search (extended) for recent large-base and generalized Wieferich searches: theory papers (arXiv 2508.08472,
  2512.08060, 2605.13460, 2609.03091) report no pairs for bases above 10000. One 2026 GPU project covers 27 small bases
  (OEIS A039951) for primes from 4.4e12 to 1e14, so it covers neither this base nor this prime.
- `gh search repos wieferich`: projects updated in the last 24 months are the GPU project above, a BOINC base-2/Wall-Sun-Sun
  program, single-problem research-page repositories, and a small repository named "wieferich" whose tree has only `README.md` and
  `index.html`. None has a table of pairs for bases 10126..65536.
- `gh search code 1024048960667` failed with `HTTP 408: Request timed out while fetching results.` and was not retried.
  This global code search is the one gap. The repository-specific checks above (tree, PR and issue text search, PR hit record) do not depend on it.

## 7. Verdict

The pair (56350, 1024048960667) does not appear in either Fischer table (live, byte-identical to the scout's copies, and neither has a row
for any base from 10126 to 65536), Fischer's extreme-first-bases files or news file, OEIS, this repository's
TROPHY_CASE.md, known-knowns/, releases or pull requests, or any literature or code found from the last 24 months. Trivial edits can't produce it,
because no base in Fischer's tabulated range (2..10125 and 65537) has this prime: the exact scan up to 70000 finds only 56350.
Under the bank's count-of-new-pairs metric it adds one pair that no known source has. That is a strict improvement,
not a tie.

novelty: The pair (56350, 1024048960667) is absent from the live Fischer tables (byte-identical to the scout's copies), Fischer's other files, OEIS, this repository's trophy case, known-knowns, releases and all 960 listed pull requests, and from the recent literature and code I could find; it is not derivable from any published pair because no base up to 70000 other than 56350 is Wieferich for this prime, so it is one strictly new pair (only gap: GitHub-wide code search timed out with HTTP 408 and was not retried).

pass: true
