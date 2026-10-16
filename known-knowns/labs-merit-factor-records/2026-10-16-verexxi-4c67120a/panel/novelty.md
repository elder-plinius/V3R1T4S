# Novelty skeptic report: labs-merit-factor-records, L = 232, claimed E = 3032
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: NEW: E=3032 (F=8.8760) < 3340 (minimum over the published L=232 values I could read: arXiv:2206.12070 E=3340, Knauer 2004 via the Boskovic repository E=3752; no L=232 row in arXiv:2607.09688, arXiv:2504.00987 or any newer arXiv result; no claim at L=232 in V3R1T4S TROPHY_CASE.md or its pull requests), margin 308

All times are UTC from `date -u` on this machine. arXiv's own Date headers read about 53 s later than my clock (consistent offset), so
the spacing between my arXiv requests is the same on both clocks. Every status, hash and time below is copied from `work/fetchlog.tsv`
or from command output in this session. Files of the claim are named relative to claim/.

## 1. The claim, recomputed (no network)

- `python check_energy.py "$(cat sequence.txt)"` run inside claim/ (the REPRODUCE.md command) printed `232 3032`.
- Two extra exact integer methods of mine (XOR/popcount per shift; big-integer polynomial product with the four 0/1 cross-counts)
  also gave E = 3032. E of the reversed and of the negated sequence is 3032 as well. F = 53824/6064 = 8.8759894459.
- Parent: the 229-symbol `parent_sequence` in parent.txt recomputes to E = 2810 (three methods), F = 9.3311, and is skew-symmetric
  (s[n+i] = (-1)^i s[n-i], n = 114). `sequence.txt` equals that parent followed by `000` (string comparison: True).
- Independent provenance check: I fetched the TeX source of arXiv:2210.15962 myself (section 4) and decoded the printed hex of its L=229 row
  (first half plus the skew rule). It gives exactly the parent_sequence of parent.txt, E = 2810. All 17 rows of that table decode to their printed
  energies.

## 2. Status source, fetched once

- URL https://arxiv.org/abs/2607.09688, fetched 2026-10-16T20:53:57Z, HTTP 200, 43398 bytes,
  sha256 c14c75eae85c1e30dcedf2fc98aa5295188e681aef1f15020b5e4e7c45c4420c. No block, no challenge page.
- Page content: "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem" (Psenicnik, Boskovic, Popic, Brest),
  [v1] submitted 17 Jun 2026, only version listed. Abstract (as worded): improves the previously best-known results for 35 sequence lengths in
  450 <= L <= 527 and for L = 573. Value for L = 232 on this page: none (abstract page only; the table is in the source below).
- Caveat on freshness: the response headers show a CDN hit (Age 1398157 s, X-Cache MISS, HIT, HIT). So I also looked at two fresher reads:
  the TeX tarball (served as arXiv-2607.09688v1.tar.gz, Age 167994 s) and the live API listing of 2026-10-16T20:56:02Z (Age 0, X-Cache MISS),
  which names the entry 2607.09688v1. Version v1 was current at that time.
- The table itself: https://arxiv.org/src/2607.09688, fetched 2026-10-16T20:54:23Z, HTTP 200, 770457 bytes,
  sha256 738c297c53b58cbd7ed4cddd7a05f25e379604427d201e2354471bebe47b43a0. TAB_RECORDS.tex has 35 rows in total: 34 lengths inside 450..527 and
  L = 573 (the abstract's "35" counts the table rows). Value for L = 232: no row (the number 232 does not appear anywhere in the TeX files). Its introduction
  only says that earlier local search produced F > 8.0 for 172 <= L <= 268 (no per-length energy).

## 3. The other sources named by the criterion, each read for L = 232

| source | what I read | value for L = 232 |
|---|---|---|
| arXiv:2504.00987 | https://arxiv.org/src/2504.00987, 2026-10-16T20:55:15Z, HTTP 200, sha256 bc0b444f8dddf0a13c28c5e4ee8a75cc034befada7231d4047797af80c72f5cd; results table in main.tex (27 rows, N = 20..120) | no row; the paper states its scope as N <= 120 and cites the Boskovic repository as https://github.com/borkob/git_labs |
| Boskovic et al. records repository (github.com/borkob/git_labs) | depth-1 clone of the only branch, master = 1aa123407636e48630174e0bf122037e369c1d68 (2020-09-15, "results 2018"); no tags; 120 files: README, results-2016 (Knauer html/txt, 2016-labs-skew.txt), results-2018 (2018-labs-skew.txt), solver sources | Knauer 2004 row only: "232* 3752 7.1727" (E = 3752). The two skew-symmetric result files hold odd lengths only (no even L). The Merit_Factor_Records-2013 pages named in the claim package are not in this tree |
| any newer arXiv result | one export.arxiv.org API query (section 5), 2026-10-16T20:56:02Z, HTTP 200, sha256 d90beafb34d5360ee6f92649af4c4fe870ed52c92a65beb1026f8c2486cad894 | none gives an L = 232 sequence or energy |

Under the criterion's literal list the best published energy at L = 232 is therefore 3752 (Knauer, via the repository). The claim's baseline.tsv
is stricter and also counts arXiv:2206.12070 (3340); I compare against the stricter number.

## 4. Published rows at L = 232 outside the criterion's list, read by me

- arXiv:2206.12070 (Dimitrov, June 2022): https://arxiv.org/src/2206.12070, 2026-10-16T20:55:34Z, HTTP 200, 104737 bytes,
  sha256 79806b61419d8ace9351322122bebef2408ea191651b725d4986c3376e53f13a. Row n = 232, class B_233 composed with eta_4, hex of 58 digits
  (232 bits), "Old MF" 7.1727, new MF 8.05748502994. I decoded the hex and computed E exactly: 3340 (F = 8.0574850299, equal to the printed value).
  This is the lowest published L = 232 energy I found. (Its own L = 233 row has E = 3300, so its 232 entry is looser than its neighbour.)
- arXiv:2210.15962 (Boskovic, Herzog, Brest; journal version J. Comput. Sci. 2024): https://arxiv.org/src/2210.15962, 2026-10-16T21:04:44Z,
  HTTP 200, 186881 bytes, sha256 7217b1d4ed4b0ec421956a72c527f715c4a23f5bd3a4161f83c88b73ca7af179. Table of 17 skew-symmetric (odd) lengths
  171..247, no even lengths, no row at 232. The L = 229 row (E 2810), L = 231 row (E 2963) and L = 235 row (E 2965) are the ones that matter below.
- Knauer 2004 (git_labs copy): E = 3752, F = 7.1727 (see section 3).
- ERK 2025 paper "Integer partitions and the merit factor problem" (https://erk.fe.uni-lj.si/2025/papers/psenicnik(integer_partitions).pdf,
  2026-10-16T21:03:42Z, HTTP 200, sha256 72574b63061ac62707b26b77c02698ef20ac8d0bcde1956e9f7060a443149605): improves all previously published
  sequences for 400 <= L <= 450 only; names arXiv:2206.12070 as the list for 225 <= L <= 527 with F >= 7.0. No 232.
- Elektrotehniski vestnik 92(3) 2025 (https://ev.fe.uni-lj.si/3-2025/Brest.pdf, 2026-10-16T21:07:07Z, HTTP 200,
  sha256 75dedd7d8628f7e3ef461d5d14fe2e1ca15260b03fff427f2ce48eeb9bcb4665): merit factor versus PSL distance study; no 232.
- Maribor PSL repository https://github.com/J-Brest/LABS (depth-1 clone, 4232311cb4f3626ab008336f6069cd5af5e3915b, 2026-05-12): only sequences with
  L >= 2047. Nothing at 232.
- Not re-read by me (arXiv budget used up): arXiv:1406.5301, 1512.02475, 2011.00068, 2106.03377, 2409.07222. sources_checked.md reports no L = 232
  row in any of them (odd-only or other ranges). Everything of that package that I could re-check (2607.09688, 2504.00987, 2206.12070, 2210.15962,
  Knauer) matched. I also decoded the six 2011.00068 lines quoted in source_excerpts.txt (L = 229..239): each decodes to its printed merit factor.

## 5. Last 24 months of literature (2024-10-16 to 2026-10-16)

- arXiv API, one query on the abstract field (phrases "low autocorrelation binary", "autocorrelation binary sequences", "merit factor" with "binary",
  "skew-symmetric" with "binary sequences"; sorted by submission date, 100 requested): 41 matches in total, 10 dated 2024-10-01 or later.
  I read the abstracts of all 10; none states an L = 232 sequence or an even-length record in 200..300:
  2610.14361 (2026-10-09, small-subsystem heuristics, N up to 60), 2609.05771 (2026-09-04, crosscorrelation demerit moments),
  2607.09688 (the status source), 2511.05778 (2025-11-08, TOPSIS-like mutation operators; abstract only, no record claim), 2511.04553
  (QE-MTS, N 27..37), 2510.24237 (PUBO benchmark), 2506.17391 (PCE solver, N up to 45), 2504.11549 (QPE-QITE, LABS only as a test),
  2504.01694 (QAOA schedules, LABS only as a benchmark), 2504.00987 (criterion source).
- Maribor group page https://labraj.feri.um.si/bibliografija/bibliografski-izbirni-seznam/?tgid=2 (tag LABS_MF), 2026-10-16T21:07:08Z, HTTP 200,
  sha256 112dc48ec1d55e53693083c93b8b1e7c7964942135b2b55c5d0c6a97956a4efa: the group's own list of LABS_MF-tagged papers, 2017..2026. Entries dated 2025-2026:
  PSL preprint (Preprints.org, July 2026), 2607.09688, ERK 2025, DSP 2025 (arXiv:2409.07222), EV 2025. Entries dated 2024 (at or just before the window start):
  JoCS (arXiv:2210.15962, odd lengths) and a MELECON neural-network paper. None is an L = 232 record table.
  A second page of the group (https://labraj.feri.um.si/dejavnosti/raziskovalna-dejavnost/binarna-zaporedja-z-nizkimi-avtokorelacijami/, 2026-10-16T21:12:12Z, HTTP 200,
  sha256 e2b3ffe9644bfbddf5771b66098b9debc85522eac7f5035413bd1cfed6e8d200) names the group's two repositories: git_labs (merit factor, checked) and J-Brest/LABS (PSL, checked).
- OpenAlex, two queries (published since 2024-10-01), 2026-10-16T21:12:43Z and 21:12:44Z, HTTP 200
  (sha256 c8d010dae927c08937eb32f1102ac09f1fd39490b529e0486683a992bd889bea and 93dff8898907b7197702cef7ae2e675573274c365b86c1f66c43b1c643402a3e):
  177 distinct works returned, 19 with binary-sequence / merit-factor vocabulary. I read the abstracts of the unfamiliar ones: SamBa-GQW quantum walk
  (n <= 30), a 2026 "pm1 sequences with low aperiodic autocorrelation" construction paper (sidelobe energy / ISL / PSL against random baselines, no record table),
  an IEEE Access 2026 PUBO benchmark, a 2025 CPU/GPU LABS heuristics paper, a Maribor thesis abstract on dual-step optimization (long sequences).
  None reports a sequence of length 232.
- Nine queries to the web search tool (merit-factor records 2025/2026, Boskovic/Brest/Dimitrov/Psenicnik, length 232, energies 3340/3032,
  Mertens table, the odd "12.6678" figure): nothing new. One search summary mentioned "merit factors 12.12 and 12.6678 for lengths 231 and 237"; a targeted search
  found no page with those numbers, and they contradict every table I read (for example E = 3118 at L = 237 in arXiv:2210.15962). I treat that as a summary artifact.

## 6. This repository (github.com/elder-plinius/V3R1T4S)

- Depth-1 clone started 2026-10-16T20:57:02Z (three git HTTP exchanges, all 200). main = ab114dcb1aad5cc1b2a53c58bc3ad3fcacd1107c (2026-10-15T15:18:21-07:00).
- TROPHY_CASE.md on main (sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad) differs from claim/TROPHY_CASE.md
  (sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412) only by "overtaken"/"superseded" annotations on one constant-weight-code row and the
  matrix-multiplication rows (diff lines 15, 73, 92, 93, 95 after stripping CRs) and by line endings. Neither copy has any LABS row; the main copy contains none of
  "labs", "merit", "autocorrel", "binary sequence", "skew" or the number 232. known-knowns/ has no LABS folder. The bank page
  known-unknowns/record-tables/labs-merit-factor-records.md lists the target as open (as of 2026-10-03).
- Pull requests, open and closed: GitHub REST API, 3 of 3 calls, GET /repos/.../pulls?state=all&per_page=100 pages 1-3,
  2026-10-16T20:58:07Z, 20:58:30Z, 20:58:37Z, all HTTP 200 (sha256 42b479483b7fc05704e019d6af3fdb47d8bb234865dcd75b2b67f0e155a048b0,
  86440a1af6a4d25da331c2e0e444d9bab2cdd2a18539ef60b8d2dc0880da1e1b, 40e49f1323c31587867d47bb944e83d1120556534ec402bcc70da47f3d5a42ba).
  260 pull requests (#1..#267; numbers 61, 152, 232, 233, 240, 253, 254 are not pull requests): 77 open, 59 merged, 124 closed unmerged.
  I searched titles, bodies and branch names for labs, merit factor, autocorrel, binary seq, skew: exactly one pull request touches the target,
  #255 (open, created 2026-10-16T19:30:57Z), "[claim] labs-merit-factor-records: L=463 energy 14047 ...", a one-length end extension of a published sequence.
  Its body says it claims nothing about any other length. No pull request names L = 232, and the word 3032 appears in the repository text only in five unrelated
  files (graph edge lists and a robust-indices list), none of which mentions LABS or merit factors.
- Not examined: the seven non-pull-request numbers above (issues or gaps), because the REST budget of three calls went to the pull request pages.
  The task text asks for pull requests only.

## 7. Hosts that blocked or failed (stopped, not retried)

- www.preprints.org: HTTP 403, Akamai "Access Denied", 2026-10-16T21:03:41Z. I stopped using that host. The July 2026 Maribor PSL preprint
  (Preprints.org 202605.0907 v2) is therefore not read by me; its abstract (via the Maribor page and OpenAlex) is about peak sidelobe levels of Legendre
  and Rudin-Shapiro sequences, not merit-factor energies.
- www.ovgu.de (Mertens' open.dat): http 301, then https 404 at 2026-10-16T21:08:31Z. The page no longer exists (not a block).
- ScienceDirect and IEEE Xplore were not requested (journal-only versions of DSP 2025 x2, JoCS 2024, IEEE Access 2018, MELECON 2024). Their arXiv
  counterparts were read as described above (2210.15962 by me; 2409.07222 and 2106.03377 by the claim package only). Extra tables that exist only in
  journal versions would be unseen by me.
- No 401/429/503 appears in any logged response. (The single-pack lazy fetches mentioned in section 8 were not individually logged.)

## 8. Request footprint

- arxiv.org / export.arxiv.org: 6 of 6 requests, all HTTP 200, one each: abs 2607.09688 (20:53:57Z), src 2607.09688 (20:54:23Z), src 2504.00987 (20:55:15Z),
  src 2206.12070 (20:55:34Z), export API (20:56:02Z), src 2210.15962 (21:04:44Z). Smallest gap 19 s. No retries.
- GitHub REST API: 3 of 3 (section 6). Git protocol: clones of V3R1T4S (20:57:02Z), borkob/git_labs (20:59:14Z, blobless, then one batched checkout of the
  five files I needed at 21:02:37Z), J-Brest/LABS (21:12:25Z), plus `git ls-remote` of borkob/git_labs (21:14:14Z) and one `git ls-remote --heads` of V3R1T4S (not timestamped; it listed no LABS-named branch head).
  A slip of mine: after the blobless git_labs clone I ran `git ls-tree -l`, which makes git fetch every blob one by one (git count-objects later showed 64 packs);
  I killed the git processes once I saw it. Git reported no error for those fetches (their individual statuses were not logged); the later batched checkout returned
  200 on both exchanges, with a local error for one file I did not need (solversjs/README.md).
- Other single requests: erk.fe.uni-lj.si, ev.fe.uni-lj.si, labraj.feri.um.si (with its two redirects), ovgu.de (301 then 404), api.openalex.org (2 queries),
  preprints.org (403).

## 9. Reasoning

1. The claimed object is exactly what it says: 232 symbols, E = 3032 under three exact methods, a skew-symmetric published parent whose printed energy I
   reproduced from the arXiv source, plus a 3-symbol suffix.
2. For L = 232 the published rows I can find are 3340 (Dimitrov, arXiv:2206.12070) and 3752 (Knauer 2004, in the Boskovic repository). 3032 is strictly smaller than both
   (by 308 and 720), so this is not a tie. The status source and the other named tables contain no L = 232 value at all (450..527 and 573; N <= 120; odd-only skew files).
3. The size of the margin (F 8.057 to 8.876) is plausible for a specific reason, not a suspicious one. Dimitrov's even-length table (June 2022) predates the much better
   skew-symmetric odd-length sequences of arXiv:2210.15962 (October 2022), and I found no later publication of even lengths near 232: the 2025 and 2026 Maribor papers work at
   400..527 and 573, and the bank page itself says lengths 121..449 may be softer. As a calibration I tried 1495 end edits (adding up to 7 symbols with every split and sign pattern,
   or removing up to 15 symbols with every split) of the published sequences near L = 232: the 17 rows of arXiv:2210.15962 and the rows of arXiv:2206.12070 with 227 <= L <= 240.
   The minimum is exactly 3032 (L=229 plus suffix 000, its reversed/alternated equivalent, and also L=231 plus one symbol), none is below 3032, and the next value is 3100.
   The PSL-table sequences of arXiv:2011.00068 (as quoted in source_excerpts.txt) give at best 3160.
4. Tie caveat, stated openly: the published L=231 sequence plus one `0` also has E = 3032, but it is a different sequence (not equivalent to the claimed one under
   reversal, negation or alternation, which I tested). That derivation is not a published row. If anyone prints an L=232 sequence with E <= 3032 (it is a one-symbol
   extension of a published sequence, and pull request #255 shows others doing the same at L=463), this record would be tied or lost. I found none in print.
5. Residual uncertainty: journal-only content (ScienceDirect, IEEE), the blocked PSL preprint, the git_labs 2013 pages (absent from the tree) and five arXiv sources I
   did not re-open. Nothing I read points to a value at or below 3032 for L = 232, and the sources that matter for this length (the status source, the other named tables,
   the one paper that has a looser L = 232 row, the parent paper, this repository) were read directly.
6. Verdict: no published energy for L = 232 that I can find is <= 3032. The result strictly beats every published value I could read, and the repository holds no competing claim at this length.

pass: true
