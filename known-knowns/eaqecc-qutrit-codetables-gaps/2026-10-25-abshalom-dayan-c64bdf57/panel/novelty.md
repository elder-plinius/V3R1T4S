# NOVELTY verdict: [[23,4,12;9]]_3 at cell (n,k,c) = (23,4,9)

**Bottom line: novelty PASS.** The live table lists the cell as [[23,4,11-18;9]]_3 (d_lower 11, d_upper 18). The claimed
d = 12 is strictly above 11 and at most 18. I found no known code with (n,k) = (23,4), d >= 12 and c <= 9 in any
source I checked:

- the listed cells;
- the page's six propagation rules, applied to every listed non-teleportation cell plus 328 extra codes. The extras are
  every exact code in the bodies of the 15 open PRs and the closed PR #331 for this target, the files of PR #739, the
  known-knowns entry, the author's unfiled codes, arXiv:2607.02170's qutrit codes and arXiv:2207.05647's Table 2;
- TROPHY_CASE.md and known-knowns/ of the V3R1T4S repo;
- arXiv literature from the last 24 months.

All of these give 11 at (23,4,9), the listed value. The closest known codes reach 12 only at c = 10 (the listed
(23,4,10) value). The only routes to 12 or more at c <= 9 use invalid steps. One seeds the page's teleportation cells.
The other applies increasing dimension to impure codes, which arXiv:2207.05647 allows only for pure codes. Neither is a
known code.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## 1. Fetch record (status source)

- URL: https://eaqecc.codetables.de/qutrit.php. I sent one plain GET with curl, User-Agent "V3R1T4S-research-agent
  (honest single fetch)", and made no retries.
- `date -u` before: 2026-10-25T11:27:14Z. After: 2026-10-25T11:27:14Z. Server Date header: Sun, 25 Oct 2026 11:27:14 GMT.
- HTTP 200, size 628039 bytes.
- sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is the same hash as the claim's copy
  (claim/table/RECORD.md). Footer: "Last change: 10.07.2025".
- Saved as fetched/qutrit.php, with fetched/qutrit.headers.txt, fetched/qutrit.result, fetched/qutrit.time_start and
  fetched/qutrit.time_end. The row was extracted by scripts/row.py into fetched/row_23_4.txt. Its 12 cells are
  identical to claim/table/row_23_4.txt.

Row (23,4), verbatim:

```html
<TD NOWRAP bgcolor="#66ff00" class="EAQECC" title="from codetables.de">[[23,4,7-9;0]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[24,4,8;0]] from codetables.de">[[23,4,8-11;1]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[23,1,9;0]] from codetables.de">[[23,4,9-12;3]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[23,4,10-16;4]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[19,4,11;9]] quantum shortening of [[20,3,12;9]] from arXiv:2207.05647">[[23,4,11-18;9]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[20,4,12;10]] increasing dimension of [[20,3,12;9]] from arXiv:2207.05647">[[23,4,12-18;10]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ffff" class="EAQECC" title="from arXiv:2207.05647">[[23,4,13-18;11]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[21,4,14;13]] increasing dimension of [[21,2,14;11]] from arXiv:2207.05647">[[23,4,14-19;13]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[25,2,17;15]] from arXiv:2207.05647">[[23,4,15-19;15]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[21,4,16;17]] increasing dimension of [[21,1,16;14]] from arXiv:2207.05647">[[23,4,16-19;17]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[22,4,17;18]] increasing dimension of [[22,1,17;15]] from arXiv:2207.05647">[[23,4,17-19;18]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[24,3,19;19]] increasing dimension of [[24,0,19;16]] from arXiv:2207.05647">[[23,4,18-20;19]]<sub>3</sub></TD>
```

The listed cells at c <= 9 are c = 0, 1, 3, 4 (teleportation) and 9, with d_lower 7, 8, 9, 10 and 11. None reaches 12.

Neighbouring rows, read from the same page (c: d_lower-d_upper):

- (23,3): 0:7-9, 1:8-11, 2:9-12, 3:12-18 (teleportation), 11:13-20, ...
- (23,5): 0:7-9, 2:8-11, 4:9-12, 6:10-15, 9:11-17, 11:12-17, ...
- (22,4): 0:7-9, 2:8-11, 4:9-15 (teleportation), 6:10-16, 9:11-17, 10:12-17, ...
- (22,5): 0:6-8, 1:7-10, 3:8-11, 5:9-13 (teleportation), 6:10-14, 9:11-16, 11:12-16, ...
- (24,4): 0:8-10, 3:9-12, 4:11-17 (teleportation), 10:12-19, ...
- (24,5): 0:7-9, 1:8-11, 4:9-12, 5:10-15, 8:11-17, 10:12-18, ...

## 2. Propagation closure (the page's colour legend)

The legend lists these rules:

- subcode: [[n,k-1,d;c]]
- lengthening: [[n+1,k,d;c]]
- puncturing: [[n-1,k,d-1;c]]
- trivial: [[n,0,n+1;n]]
- quantum shortening: [[n-1,k+1,d-1;c]]
- increasing dimension: [[n,k+1,d;c+1]]
- length reduction: [[n-1,k,d;c+1]]
- using teleportation: [[n,k,d;k]]

arXiv:2207.05647 (fetched, section "Propagation Rules" and its list of eight rules) attaches side conditions:

- increasing dimension needs a pure code from the Hermitian construction (its Theorem 12), and c <= n-k-2;
- shortening needs a pure code;
- length reduction needs c <= n-k-2;
- puncturing needs d > 1 and c < n-k.

That paper's rule "(4) requiring more entanglement" only raises c, so it cannot add anything at c <= 9.

No rule lowers c or raises d, so any source must already have c <= 9 and d >= 12. My closures drop the side
conditions, which can only make them more generous. They run up to n = 40 and c = 60 (scripts/closure.py, a worklist
fixpoint).

| variant | best d at (23,4,c<=9) |
|---|---|
| listed non-teleportation cells only (3764 seeds; 124 teleportation cells skipped) | **11** (c = 9) |
| plus all 328 extra codes (scripts/seeds_all.txt) | **11** |
| plus PR #363's k = 1 extension rule [[n,1,d;c]] -> [[n+1,1,d+1;c+1]], purity tracked: the extension's output is impure, and increasing dimension and shortening need pure sources (scripts/closure_purity.py) | **11** |
| same rule, purity ignored (scripts/closure_k1ext.py) | 13, invalid (see below) |
| teleportation cells also seeded, all six rules (diagnostic only, scripts/closure_diag_with_teleport.py) | 22, unsound: 2700 listed cells end up above their own d_upper, and 22 is above this cell's d_upper of 18 |

The purity-ignored path is: listed [[17,1,7;0]], then six k = 1 extensions to [[23,1,13;6]], then increasing
dimension three times to [[23,4,13;9]]. A k = 1 extension keeps the stabilizer's own words, and the 16-dimensional
isotropic part of [[17,1,7;0]] has weight at most 10 by the Singleton-type count. So [[23,1,13;6]] is impure, and
Theorem 12 of arXiv:2207.05647 does not apply. This is not a valid derivation.

The backward cone is in scripts/cone.py. For every (n,k,c) it gives the minimum d a code needs there to reach
(23,4,c<=9) at d >= 12 under the generous rules. Every listed non-teleportation cell in the cone falls short by at
least 1. Examples: (22,4,9) has 11 and needs 12; (23,5,9) has 11 and needs 12; (20,3,9) has 12 and needs 13;
(23,0,5) has 11 and needs 12. The extra codes come no closer:

- [[24,5,11;8]] and [[24,6,11;8]] (from arXiv:2207.05647) need 12;
- PR #739's [[25,5,12;8]], its subcode [[25,4,12;8]], and the author's lead [[24,5,12;9]] need 13.

## 3. Teleportation cells (CLAIM.md's statements checked)

- All 124 yellow cells carry the bare title "using teleportation". No listed cell's title cites a code with a
  teleportation cell's (n,k,d;c). So the page never propagates them.
- (23,4,4) = [[23,4,10-16;4]] is itself at c <= 9, but its d is 10, below 12.
- (23,3,3) = [[23,3,12-18;3]] would give 12 at (23,4,4), and so at (23,4,9), only through increasing dimension. That
  rule needs a pure code from the Hermitian construction (Theorem 12 of arXiv:2207.05647). A teleportation scheme is
  not such a code, and the page itself lists (23,4,4) at 10, not 12.
- CLAIM.md says seeding the teleportation cells gives 22 at (23,4,9) and pushes thousands of cells above their own
  d_upper. I confirm both: 22 at (23,4,9), and 2700 cells.
- Conclusion: the teleportation cells are not valid sources for these rules, and they give nothing at (23,4,c<=9)
  with d >= 12.

## 4. Other sources checked

| source (fetched once each, HTTP 200 unless noted) | what it gives at (23,4), c <= 9 |
|---|---|
| GitHub search API, 4 queries for PRs in repo elder-plinius/V3R1T4S: "eaqecc-qutrit", "qutrit", "eaqecc", "entanglement-assisted" (fetched/gh_search_*.json, 11:28:26Z to 11:28:37Z) | 16 or 17 PRs, the same set. Open for this target: #363, #403, #404, #405, #643, #645, #646, #651, #710, #721, #726, #727, #728, #729 and #739; #331 is closed. Every exact code named in their bodies was seeded. Nothing reaches the cell. |
| PR #739 (filed 2026-10-25T11:02:34Z, [[25,5,12;8]]): body and all 36 file patches (fetched/pr739_files.json, 11:30:16Z) | Its codes were seeded, except [[5,1,6;4]] (impossible) and teleportation-derived or hypothetical codes that the PR itself says do not exist: [[25,4,12;4]], [[28,5,12;5]], [[25,4,12;7]], [[25,5,12;5]], [[25,5,12;6]], and the intermediates [[26,1,13;5]] and [[26,3,13;7]] of its "purity ignored" path. Best route: [[25,5,12;8]] -> subcode -> length reduction twice -> [[23,4,12;10]]. That is c = 10, equal to the listed (23,4,10), and not <= 9. |
| TROPHY_CASE.md (raw main, 11:29:53Z, sha256 b946f68e...472171a1) | No mention of EAQECC or qutrit. |
| known-knowns/eaqecc-qutrit-codetables-gaps/ (contents API, 11:29:59Z and 11:30:04Z; INDEX.csv and README.md at 11:30:10Z) | One entry: [[14,3,8;5]]_3 (anzal1), plus k = 0 neighbours named in its README. Seeded. Nothing reaches the cell. |
| arXiv:2207.05647, the table's source (PDF, 11:33:32Z, sha256 5efbf317...a80e3) | The propagation rules and purity conditions quoted above. All 216 Table 2 qutrit codes were seeded. Nothing reaches the cell. |
| arXiv:2607.02170 (HTML, 11:32:40Z, sha256 f2e6c891...a18e1) | 29 qutrit codes. At n >= 20: [[21,0,16;16]], [[21,2,18;19]], [[22,2,19;20]], [[23,0,13;13]], [[23,2,20;21]], [[24,2,21;22]], [[25,2,22;23]], [[25,3,20;22]], [[26,0,14;18]], [[26,2,22;24]]. All have c >= 13, and no rule lowers c. Nothing at (23,4,c<=9). |
| arXiv API, 4 queries sorted by date: "entanglement-assisted" (200 newest), "entanglement-assisted" AND hull, "entanglement-assisted" AND (qutrit OR ternary), and Hermitian curve / AG codes AND (hull OR entanglement) (fetched/arxiv_q_*.xml). The first two queries went to http:// and got 301 redirects, so I sent them once to the https:// address. | 140 papers from the last 24 months. The relevant ones, judged from their abstracts: 2609.20453 (Galois hulls of GRL codes; GF(9) lengths far below 23), 2512.17128 (rational AG codes; length at most q^2 + 1), 2607.03802 (twisted GRS hulls; short lengths over GF(9)), 2501.15465 (qubit), 2501.04921 and 2412.16082 (concatenated EA codes), 2603.03182 (non-stabilizer EA codes, qubit examples), 2608.09886 and 2608.06854 (EA locally recoverable codes; abstracts mention one-point Hermitian codes but no qutrit parameters), 2608.02850 (hulls of superelliptic AG codes; GF(7) and GF(11) examples). None names a [[23,4,>=12;<=9]]_3 code or a [23,9,>=12]_9 code with Hermitian hull 5. |
| codetables.de BKLC GF(9) [23,9] (11:31:35Z, sha256 6f676bbb...b8e3cfea) | Bounds 12-13. Construction: shortening of a [28,14,12] AG code from the Hermitian curve. No hull is stated, so this is not a known hull-5 code (the claim does not say the classical code is new). |
| codetables.de BKLC GF(9) [23,10] (11:31:36Z, sha256 38b1ba2c...1fe1e479) | Bounds 11-12. No [23,10,12]_9 is known, so there is no kappa = 10, hull 6 route to [[23,4,12;7]]. For kappa >= 11 a code would need d >= 12 above the listed lower bounds, which is not known either. |

## 5. Could not read, and residual risk

- I read only the abstracts of the recent arXiv papers listed above, not their full text. Journal papers without an
  arXiv version were not searched.
- I fetched the file list of PR #739 only. For the other PRs I used their bodies. CLAIM.md says the author's own
  earlier PRs name further codes in their bodies, and all exact codes in those bodies were seeded.
- The codetables [23,9,12]_9 code (a shortened Hermitian AG code) has an unknown Hermitian hull. If someone showed its
  hull is at least 5, Theorem 7 of arXiv:2207.05647 would give [[23,4,12;9]] and make this a tie. No source I found
  states this, and the page's own value of 11 suggests the table maintainer has no such code.
- I hit no blocks. The GitHub API answered 200 every time (rate-limit remaining 24 at the last call).
  injection_suspected: none.

## 6. Files (relative to the work folder)

fetched/ (every web response, with its times and hashes), scripts/closure.py, scripts/closure_purity.py,
scripts/closure_k1ext.py, scripts/closure_k1ext_path.py, scripts/closure_diag_with_teleport.py, scripts/cone.py,
scripts/row.py, and the seed files scripts/seeds.txt, scripts/seeds_2607.txt, scripts/seeds_739.txt,
scripts/seeds_2207.txt and scripts/seeds_all.txt.

pass: true
