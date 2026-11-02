# NOVELTY verdict: [[24,4,13;10]]_3 at the listed cell (24,4,10)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

**Bottom line: novel.** I found no known code with (n,k) = (24,4), d >= 13 and c <= 10. That covers the listed cells, the closure of the page's own rules (teleportation cells excluded), every code named in the 15 open V3R1T4S PRs for this target, the merged known-knowns entry and the literature I checked. The best known value at (24,4,c<=10) is 12 (the listed [[24,4,12-19;10]], and also [[23,4,12;9]] lengthened). The claimed d = 13 is strictly above 12 and at most d_upper 19. Two routes come within one step of a tie, but neither is a known code (section 5).

## 1. Fetch record (status source)

- URL: https://eaqecc.codetables.de/qutrit.php
- One plain GET with curl, User-Agent "V3R1T4S-research-agent (honest single fetch)", no retries.
- Time (UTC, `date -u` before and after): 2026-10-25T11:05:08Z to 2026-10-25T11:05:09Z. The server Date header is Sun, 25 Oct 2026 11:05:08 GMT.
- HTTP 200, 628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. These are the same bytes as claim/table/qutrit.php. The footer reads "Last change: 10.07.2025".
- Saved as fetched/qutrit.php, with fetched/qutrit.headers.txt, fetched/qutrit.result, fetched/qutrit.time_start and fetched/qutrit.time_end.
- Row (24,4) verbatim (fetched/row_24_4.txt, made by tools/extract_row.py, a copy of claim/table/extract_row.py; it is identical to claim/table/row_24_4.txt):

```html
<TD NOWRAP bgcolor="#66ff00" class="EAQECC" title="from codetables.de">[[24,4,8-10;0]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[23,4,9;3]] increasing dimension of [[23,1,9;0]] from codetables.de">[[24,4,9-12;3]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[24,4,11-17;4]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff6600" class="EAQECC" title="subcode of [[24,6,12;10]] from arXiv:2207.05647">[[24,4,12-19;10]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[23,4,13;11]] from arXiv:2207.05647">[[24,4,13-19;11]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[21,4,14;13]] increasing dimension of [[21,2,14;11]] from arXiv:2207.05647">[[24,4,14-20;13]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[25,3,16;14]] from arXiv:2207.05647">[[24,4,15-20;14]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[25,3,17;16]] increasing dimension of [[25,2,17;15]] from arXiv:2207.05647">[[24,4,16-20;16]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[22,4,17;18]] increasing dimension of [[22,1,17;15]] from arXiv:2207.05647">[[24,4,17-20;18]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[23,4,18;19]] quantum shortening of [[24,3,19;19]] increasing dimension of [[24,0,19;16]] from arXiv:2207.05647">[[24,4,18-20;19]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[24,0,19;16]] from arXiv:2207.05647">[[24,4,19-21;20]]<sub>3</sub></TD>
```

- Summary as c: d_lower-d_upper: 0: 8-10; 3: 9-12; 4: 11-17 (teleportation); 10: 12-19; 11: 13-19; 13: 14-20; ... The claimed cell (24,4,10) reads [[24,4,12-19;10]]. The best listed value at any c <= 10 is 12, or 11 if the teleportation cell is excluded at c = 4 to 9.
- Neighbour rows from the same fetch, as c: d_lower (non-teleportation cells, c <= 12):
  - (23,4): 10:12, 11:13
  - (25,4): 3:9, 11:13
  - (24,3): 2:9, 12:14
  - (24,5): 8:11, 10:12, 12:13
  - (25,3): 2:9
  - (26,4): 2:9, 12:14
  - (27,3): 2:10

## 2. The page's own rules (colour legend), closure

The legend on the page lists eight rules:
- subcode [[n,k-1,d;c]]
- lengthening [[n+1,k,d;c]]
- puncturing [[n-1,k,d-1;c]]
- trivial [[n,0,n+1;n]]
- quantum shortening [[n-1,k+1,d-1;c]]
- increasing dimension [[n,k+1,d;c+1]]
- length reduction [[n-1,k,d;c+1]]
- "using teleportation" [[n,k,d;k]]

The table's source paper (arXiv:2207.05647, read in full, fetched/arxiv/2207.05647.pdf) states the side conditions in Section 4:
- Increasing dimension is rule (6), "increasing the dimension of a pure q-ary quantum code with q > 2", with c <= n-k-2.
- Quantum shortening is rule (8), "shortening pure quantum code".
- Length reduction (rule 7) needs c <= n-k-2.
- Puncturing needs d > 1 and c < n-k.

I wrote three closure programs that iterate to a fixed point, with n <= 40, over every cell parsed from the fetch (3888 cells, 124 of them teleportation):
- tools/closure.py applies all rules to everything, ignoring purity.
- tools/closure_pure.py tracks purity generously: every listed or extra code is assumed pure.
- tools/closure_pure2.py is the same as closure_pure.py, but impure codes get only subcode, lengthening and puncturing.

Results at (24,4,c) for c <= 10. Each closure's only conflict with a listed d_upper is (11,0,0), a k = 0 artifact of lengthening a k = 0 code; it does not touch k = 4.

| seeds | best d at (24,4,c<=10) |
|---|---|
| listed non-teleportation cells only (any of the three programs) | **12** (c = 10, the listed cell) |
| + every code named in open PR bodies, the merged entry, literature codes, the author's unfiled codes and leads (scratch/all_known_final.txt, 146 codes) | **12** |
| + the k = 1 extension rule of PR #363 (outputs impure) + teleportation cells as impure seeds (closure_pure2) | **12** |
| the claimed code itself added (sanity check of the tool) | 13 |
| teleportation cells seeded into all rules, purity ignored | 24, but it puts 2569 listed cells above their own d_upper (unsound) |

## 3. Teleportation cells (24,3,3) = [[24,3,13-19;3]] and (24,4,4) = [[24,4,11-17;4]]

- **Checked:** the page never chains its rules through a teleportation cell. No cell title combines "using teleportation" with another rule. Increasing dimension of (24,3,3) would give 13 at (24,4,4), but the page lists 11 there. Across the page, one increasing-dimension step from a teleportation cell would beat the listed value at (n,k+1,<=c+1) in 102 of 124 cases, so the page systematically does not apply it.
- **Why that is right:** these codes are impure (their isotropic part is Z-only, with low-weight words), and rules (6) and (8) of the source paper require pure codes. Seeding them anyway gives contradictions:
  - quantum shortening of the listed teleportation [[8,1,6;1]] gives [[7,2,5;1]], above that cell's d_upper of 4;
  - increasing dimension applied three times to the teleportation [[24,1,18-23;1]] gives [[24,4,18;4]], above (24,4,4)'s d_upper of 17.
- So it is not only length reduction that fails for them, as the caller's note says. Increasing dimension and quantum shortening fail too, because of purity.
- With teleportation cells used only as impure seeds (subcode, lengthening, puncturing), (24,4,c<=10) stays at 12.
- CLAIM.md's statement that all teleportation cells in all rules give 24 at (24,4,10), and thousands of cells above d_upper, checks out: 24, and 2569 cells.
- Directly, the teleportation cells give nothing at k = 4 above 11: (24,4,4) is 11, from a classical [24,8,11]_3 code.

## 4. Sources checked and what each gives at (24,4,c<=10)

| source | what I read | gives at (24,4,c<=10) |
|---|---|---|
| Live table (section 1) | full page, rows (23..27, 3..5) | 12 |
| arXiv:2207.05647 (table source; fetched/arxiv, HTTP 200, sha256 5efbf317...80e3) | rules (Sec. 4), Table 2 (qutrit codes up to n = 36); its n = 24 codes are [[24,13,6;3]], [[24,11,8;7]], [[24,6,11;8]], [[24,6,12;10]], [[24,0,19;16]], [[24,0,24;22]] | 12 (subcode of [[24,6,12;10]]) |
| arXiv:2607.02170 (Li, Ezerman, Li, Ling, Sun, Jul 2026; HTTP 200, sha256 f1b77941...dbef) | Table V (all 14 qutrit codes, n <= 25) and Table VII (5 qutrit rows); at n >= 23 only [[23,2,20;21]], [[24,2,21;22]], [[25,2,22;23]], [[25,3,20;22]], all with c >= 21 | nothing (all c > 10); closure stays 12 |
| arXiv:2105.02166 (Christensen, Munuera, Pereira, Ruano; HTTP 200, sha256 2b22f0a0...3a23) | q = 3 example: [[27,1,19;16]], [[27,4,16;13]], [[27,6,13;9]], [[27,9,10;6]], [[27,13,7;4]], [[27,16,4;1]] | see below; closure stays 12 |
| One-point Hermitian family, actual hulls (tools/herm_hulls.py: C_m on the 27 affine points and the extended E_m on 28, unscaled, every m) | my computation reproduces all six 2105.02166 parameters exactly; it also gives [[27,4,14;9]] (m = 13, hull 7) and the n = 28 codes that the author's PRs claim | 12 (one step short, section 5) |
| codetables.de [24,9]_9 (HTTP 200, sha256 dff6f79a...9fcb) | 13-14, from shortening a [28,13,13] AG code of the Hermitian curve; no hull information | a classical code only, not an EAQECC; no published hull 5 |
| codetables.de [24,10]_9 (HTTP 200, sha256 d84606e0...18bd) | 12-13 | no known [24,10,13]_9, so no route to (24,4,8) at d = 13 by the Hermitian construction |
| arXiv API, last 24 months, 3 queries (EA + hull: 35 hits, 10 since 2024-10-25; EA + qutrit: 10 hits; EA + AG / Hermitian curve / one-point: 8 hits) | titles and abstracts; candidates 2609.20453 (Roth-Lempel), 2607.03802 (twisted GRS), 2512.17128 (rational AG), 2507.18361 (GRS), 2603.16187 (LCD, hull 0), 2605.05613 (constacyclic, 3-designs), 2608.09886 and 2608.06854 (EA-LRC), 2604.23097, 2606.02137 | none gives a length-24 qutrit EA code with k = 4, c <= 10, d >= 13 (GRS-type codes over GF(9) have length <= 10 or 11; LCD codes give c = n - k) |
| V3R1T4S TROPHY_CASE.md (raw, HTTP 200, sha256 b946f68e...171a1) | no EAQECC entry | nothing |
| V3R1T4S known-knowns/eaqecc-qutrit-codetables-gaps/ (API listing + README) | one merged entry, [[14,3,8;5]] plus k = 0 neighbours [[11..14,0,8;5..2]] | nothing; included in the closure |
| V3R1T4S open PRs (search API, 2 queries, both list the same 15 PRs: #363, #403, #404, #405, #643, #645, #646, #651, #710, #721, #726, #727, #728, #729, #739) | all 15 bodies; every [[n,k,d;c]] string extracted (scratch/pr_codes.txt); the PR #739 file list with patches (36 files) | 12. Within n = 23..26 the codes are [[25,5,12;8]] (#739), [[24,5,11;8]], [[24,6,11;8]], [[25,4,12;8]], [[26,5,12;8]]; at most 12 at (24,4,9) |
| PR #363's k = 1 extension rule [[n,1,d;c]] -> [[n+1,1,d+1;c+1]] (q >= 3) | proven by hand and checked exactly on 40 random small codes (tools/k1ext_test.py: 40/40 give [[n+1,1,d+1;c+1]]) | 12 once purity is respected (section 5) |
| Author's own unfiled codes and leads (CLAIM.md) | [[30,6,13;8]], [[28,10,10;6]], [[28,13,8;5]], [[28,2,19;16]], [[25,5,12;8]], [[23,4,12;9]], [[24,5,12;9]], [[23,5,12;10]] | 12 (from [[23,4,12;9]] by lengthening, at c = 9) |

When I fed the closure every string in the PR bodies, some of them were not codes:
- [[5,1,6;4]] is the "impossible" example in #739.
- [[25,4,12;4]] and [[10,1,7;1]] are teleportation cells.
- [[12,1,10;3]] is a teleportation-derived core in #363 and pushes 75 cells above d_upper.

I removed those four and the #363 codes [[33,1,30/31;24]] from the sources. None of them can reach (24,4,c<=10) at d >= 13 by subcode, lengthening or puncturing anyway: their d is too small or their c is too large.

## 5. What came close (not known codes)

- **Unscaled one-point Hermitian C_13, [[27,4,14;9]]** (2105.02166 family, hull 7 by my computation). It gives:
  - [[26,4,13;9]] (puncturing), then [[25,4,13;10]] (length reduction);
  - [[24,4,13;11]], which is the listed value at c = 11.

  It is one step short: going from n = 27 to 24 at d >= 13 and c <= 10 needs three steps, and only one puncturing and one length reduction fit.
- **A C_13 equivalent with Hermitian hull 8** would give [[27,3,14;8]], then [[26,4,13;8]] (quantum shortening), then [[24,4,13;10]] (two length reductions). That would be a tie. No such scaling is published. I did not search for one, and the page's best at (27,3,c<=8) is 10, so it would itself be a new code, not prior art.
- **k = 1 extension chains** reach (24,4,10) only through increasing dimension of an impure code:
  - listed [[17,1,7;0]], then seven extensions, then [[24,1,14;7]], then increasing dimension three times, would give 14;
  - #739's own panel's path through [[26,1,13;5]] and [[26,3,13;7]] works the same way.

  The extension leaves the source's isotropic part unchanged, so the output is impure, and rule (6) requires a pure code. Purity is not a formality here: increasing dimension on impure teleportation codes contradicts the page's upper bounds (section 3). No PR or paper exhibits a pure code on these chains, so they are not known codes.
- **Author's lead [[23,4,12;9]]** gives 12 at (24,4,9). PR #739 [[25,5,12;8]] gives at most 12 (length reduction and subcode give [[24,4,12;9]]).

## 6. Could not read / limits

- Journal papers without an arXiv version, for example:
  - Cao, Li and Zhu, IEEE TIT 71 (2025);
  - Li, Li, Guan and Song, IJTP 63 (2024);
  - Liu, Li and Shi, AMC 19;
  - Li and Zhu, "Galois hulls of arbitrary dimensions".

  I judged these only through 2607.02170's comparison columns, which list no qutrit code with n >= 23 at k = 4.
- Abstract only: 2605.05613 and the other recent arXiv hits above.
- The file lists of the 14 PRs other than #739 were not fetched. Their bodies were read in full, and every code they name is in the closure. Their lengths (16, 28 to 36) cannot reach (24,4,c<=10) at d >= 13 under the rules.
- The closure assumes every listed or extra code is pure. That is generous: it can only raise values, and it still gives 12.
- No HTTP 401, 403 or 429 was received. One arXiv API request over http got a 301 redirect, and I repeated that query once over https (HTTP 200). GitHub search allowance at the end: 4 left.
- injection_suspected: none.
- Machine use: light Python only (each run under a minute), no compiled programs, no background jobs left.

pass: true
