# NOVELTY verdict: [[25,5,12;8]]_3 at cell (n,k,c) = (25,5,8)

**Bottom line: novelty PASS.** The live table lists the cell as [[25,5,11-18;8]]_3, so d_lower is 11, and the claimed d = 12
is strictly above it. I found no known code with (n,k) = (25,5), d >= 12 and c <= 8 in any source I checked:

- the listed cells;
- the page's six propagation rules, applied generously to every listed non-teleportation cell plus every code filed or
  published that I could find;
- the open and merged V3R1T4S material for this target (TROPHY_CASE.md, known-knowns/, open PR bodies);
- the newest qutrit EA paper (arXiv:2607.02170, July 2026) and the other recent papers I could read.

The best known value at (25,5,c<=8) stays 11, at c = 8. The only routes to d >= 12 (an exact tie at c = 8, or
better at lower c) all apply the page's stabilizer-code rules to its "using teleportation" cells. The page never does
that. I show below that doing so is unsound: it produces a [[5,1,6;4]] code, which is impossible. So those routes are
not known codes. Residual risk: I could not read the files of the target's PRs (GitHub API rate limit) or the full
text of three journal papers (listed below).

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## 1. Fetch record (status source)

- URL: https://eaqecc.codetables.de/qutrit.php. I sent one plain GET with curl, User-Agent "V3R1T4S-research-agent (honest single fetch)", and made no retries.
- `date -u` before: 2026-10-25T09:35:47Z; after: 2026-10-25T09:35:48Z (server Date header: Sun, 25 Oct 2026 09:35:48 GMT).
- HTTP status 200, size 628039 bytes.
- sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is byte-identical to the claim's copy
  (claim/table/qutrit.php, `cmp` reports identical). Page footer: "Last change: 10.07.2025".
- Saved as fetched/qutrit.php, with fetched/qutrit.headers.txt, fetched/qutrit.result, fetched/qutrit.time_start and fetched/qutrit.time_end.

Row (25,5), verbatim (every `[[25,5,...]]` cell on the page):

```html
<TD NOWRAP bgcolor="#66ff00" class="EAQECC" title="from codetables.de">[[25,5,7-10;0]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[26,5,8;0]] from codetables.de">[[25,5,8-11;1]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[28,5,9;0]] from codetables.de">[[25,5,9-12;3]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[25,5,10-16;5]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[24,5,11;8]] subcode of [[24,6,11;8]] from arXiv:2207.05647">[[25,5,11-18;8]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[24,5,12;10]] subcode of [[24,6,12;10]] from arXiv:2207.05647">[[25,5,12-19;10]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ffff" class="EAQECC" title="from arXiv:2207.05647">[[25,5,14-19;12]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[24,5,15;15]] quantum shortening of [[25,4,16;15]] increasing dimension of [[25,3,16;14]] from arXiv:2207.05647">[[25,5,15-20;15]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[25,3,16;14]] from arXiv:2207.05647">[[25,5,16-20;16]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[25,2,17;15]] from arXiv:2207.05647">[[25,5,17-20;18]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[27,3,20;20]] increasing dimension of [[27,1,20;18]] from arXiv:2207.05647">[[25,5,18-21;20]]<sub>3</sub></TD>
```

Listed cells at c <= 8: c = 0, 1, 3, 5, 8 with d_lower 7, 8, 9, 10, 11. None reaches 12. The cell (25,5,8) is
[[25,5,11-18;8]], and 12 lies within 11 < 12 <= 18.

Neighbouring rows, read from the same page (c: d_lower-d_upper, for the cells with c <= 8):

| row | cells with c <= 8 | what the page's rules carry into (25,5,c<=8) |
|---|---|---|
| (24,5) | 0:7-9, 1:8-11, 4:9-12, 5:10-15, 8:11-17 | lengthening: at most 11 |
| (24,6) | 0:7-9, 2:8-11, 4:9-12, 6:10-13, 8:11-16 | subcode, then lengthening: at most 11 |
| (25,6) | 0:7-9, 1:8-11, 3:9-12, 6:10-14, 8:11-16 | subcode: at most 11 |
| (26,5) | 0:8-10, 2:9-12, 5:10-17 (teleportation), 7:11-18 | length reduction (c+1): at most 11; puncturing: at most 10 |
| (26,6) | 0:8-10, 2:9-12, 6:10-15, 8:11-17 | at most 10 (lenred and subcode); puncturing at most 10 |
| (25,4) | 0:8-10, 3:9-13, 4:12-18 (teleportation) | increasing dimension: 9 from non-teleportation cells; 12 only from the teleportation cell |
| (26,4) | 0:8-10, 2:9-13, 4:13-19 (teleportation) | quantum shortening: 8 from non-teleportation cells; 12 only from the teleportation cell |

## 2. Propagation closure (the page's colour legend)

The legend's rules (fetched/qutrit.php) are:

- subcode: [[n,k-1,d;c]]
- lengthening: [[n+1,k,d;c]]
- puncturing: [[n-1,k,d-1;c]]
- quantum shortening: [[n-1,k+1,d-1;c]]
- increasing dimension: [[n,k+1,d;c+1]]
- length reduction: [[n-1,k,d;c+1]]
- trivial: [[n,0,n+1;n]]
- using teleportation: [[n,k,d;k]]

No rule lowers c, and none raises d. So a source must already have c <= 8 and d >= 12.

The scripts are scripts/closure2.py and scripts/closure_pure.py, with outputs in scripts/closure2_final.out and
scripts/closure_pure_final.out. Every rule is applied unconditionally, in any order, up to n = 40, which is more
generous than the page. Seeds: the 3764 listed non-teleportation cells, plus 73 extra codes (scripts/extra_codes_final.json):

- every exact code named in the bodies of the 14 open PRs and the merged PR #331 for this target;
- the known-knowns entry [[14,3,8;5]] and its four k = 0 neighbours;
- the author's four unfiled codes;
- the four n >= 23 qutrit codes of arXiv:2607.02170;
- the six q = 3 length-27 codes of arXiv:2105.02166 (Example 2);
- a generous hypothetical [[27,7,12;8]].

| variant | best d at (25,5,c<=8) |
|---|---|
| A0: listed non-teleportation cells only | **11** (c = 8), equal to the page |
| A: A0 plus all 73 extra codes | **11** (c = 8) |
| A with the k = 1 extension rule [[n,1,d;c]] -> [[n+1,1,d+1;c+1]] (named in PR #363), purity tracked | **11** |
| same, purity ignored | 12, but invalid (see below) |
| teleportation cells under subcode, lengthening and puncturing only (rules valid for any scheme) | 10 (c = 5) |
| teleportation cells plus length reduction | 12 at c = 8, but unsound (see section 3) |
| teleportation cells under all six rules | 23 at c = 8, but unsound; pushes 2717 listed cells above their own d_upper |

The "12, purity ignored" path is: listed [[23,0,10;1]] -> increasing dimension -> [[23,1,10;2]] -> three k = 1 extensions
-> [[26,1,13;5]] -> increasing dimension twice -> [[26,3,13;7]] -> quantum shortening -> [[25,4,12;7]] -> increasing
dimension -> [[25,5,12;8]]. The k = 1 extension leaves the hull words' weights unchanged, so its output is impure. Its
hull words keep weight about 10 while the outside words reach 13. Increasing dimension and quantum shortening need pure
codes: the CRSS-type shortening rule needs purity, and PR #646 says the source paper states increasing dimension only
for pure codes. Once purity is tracked, the best value is 11. This path is not a valid derivation.

Two side observations (no effect on the verdict):

- Under the unconditional closure, only PR #363's codes [[12,1,10;3]], [[33,1,30;24]] and [[33,1,31;24]] push cells above
  the page's upper bounds.
- From PR #646's [[28,6,12;6]], length reduction twice plus subcode gives [[26,5,12;8]] and [[26,6,12;8]], but not
  (25,5,c<=8) at 12.

## 3. Teleportation cells (CLAIM.md's statements checked)

- No listed cell's title derives from a teleportation cell. All 124 yellow cells have the bare title "using teleportation".
  Every derived title ends in "from codetables.de", "from arXiv:2207.05647" or "trivial". So the page never propagates them.
- Teleportation cells match a classical [n,2k,d]_3 code. Alice teleports k qutrits and sends the 2k outcome trits over the channel.
  For example, (25,4,4) = 12 matches codetables [25,8]_3 at 12-12 (fetched/bklc_q3_n25_k8.html). These schemes measure and feed
  classical results forward, so they are not stabilizer codes.
- Checked: increasing dimension of [[25,4,12;4]] would give [[25,5,12;5]], but the page lists (25,5,5) as 10. CLAIM.md's other
  statement also checks out: seeding all teleportation cells gives 23 at (25,5,8), above its d_upper of 18 ("thousands" of
  cells: 2717 in my run).
- The tie paths from teleportation cells are:
  - [[28,5,12-19;5]], length reduction three times -> [[25,5,12;8]] (an exact tie);
  - (25,4,4) by increasing dimension -> (25,5,12;5);
  - (26,4,13;4) by quantum shortening -> (25,5,12;4);
  - (25,3,14;3) by increasing dimension twice -> (25,5,14;5).
- These paths are unsound. The same length reduction applied to the listed teleportation cell [[8,1,6-7;1]] gives [[5,1,6;4]].
  That code cannot exist: for k >= 1, d <= n. Bob's halves are independent of the message, so some unitary on Alice's n qutrits
  maps one codeword to another. The page itself lists the cell as exactly [[5,1,5;4]].
  - Physically, a teleportation channel qutrit carries outcome trits that exist only after encoding, so it cannot be handed to Bob in advance.
  - Using the extra pair for superdense coding merges two classical coordinates, which can lose 1 in distance.
  - Increasing dimension on teleportation cells fails the same way: (8,3,3) gives 6 against d_upper 5.
- The teleportation rule itself only gives c = k at (25,5): [[25,5,10;5]]. A teleportation-plus-superdense scheme at c = 8
  is not on the legend, and I found it nowhere in the literature.

Conclusion: the teleportation cells are known schemes, but no known scheme or valid derivation from them reaches
(25,5,c<=8) at d >= 12.

## 4. Other sources checked

| source | what it gives at (25,5), c <= 8 |
|---|---|
| codetables BKLC [25,11]_9 (fetched/bklc_q9_n25_k11.html, 09:47:21-22Z, HTTP 200, sha256 108d7161...f9c) | [25,11] at 12-13, built by shortening a [28,14,12] Hermitian-curve AG code at 3 coordinates. No hull is given. The page (2207.05647 used codetables codes systematically) shows nothing from it at (25,5,c<=8) above 11. The claim does not say the classical code is new. |
| codetables BKLC [25,12]_9 (fetched/bklc_q9_n25_k12.html, HTTP 200, sha256 e442fcd9...6cf6) | 11-12. No [25,12,12]_9 is known, so there is no hull-7 route to [[25,5,12;6]]. |
| codetables BKLC [25,8]_3 (fetched/bklc_q3_n25_k8.html, HTTP 200, sha256 8a595222...d8a8) | 12-12. Confirms the teleportation reading of (25,4,4). |
| arXiv:2607.02170 (Li, Ezerman, Li, Ling, Sun, 2 Jul 2026), HTML v1 (fetched/arxiv_2607.02170v1.html, 09:48:50Z, HTTP 200, sha256 f2e6c891...18e1) | Table V (qutrit, 7 <= n <= 25), n >= 23: [[23,2,20;21]], [[24,2,21;22]], [[25,2,22;23]], [[25,3,20;22]]_3. All have c >= 21. Table VII qutrit: n <= 16. Matches CLAIM.md. Nothing at (25,5,c<=8). |
| arXiv:2105.02166 (Christensen, Munuera, Pereira, Ruano), PDF (fetched/arxiv_2105.02166.pdf, 09:51:53Z, HTTP 200, sha256 2b22f0a0...3a73) | q = 3, length 27: [[27,1,19;16]], [[27,4,16;13]], [[27,6,13;9]], [[27,9,10;6]], [[27,13,7;4]], [[27,16,4;1]]. Reaching n = 25 costs 2 in d or c. Even a hypothetical [[27,7,12;8]] gives at most 11. |
| arXiv:2501.04921 (Fan et al., EA concatenated codes), HTML (fetched/arxiv_2501.04921.html, 09:54:28Z, HTTP 200, sha256 2c3fc4a8...61f1) | Qubit codes only; no qutrit codes. |
| arXiv:2206.09782 (Luo, Ezerman, Ling), PDF (09:54:44Z, HTTP 200, sha256 a3a4c821...bf6) | GRS/MDS families (length <= 10 over GF(9)); nothing at n = 25. Older than 24 months. |
| arXiv:2410.04130 (Ghosh, Stylianou, Boche) | Withdrawn by the authors (protocol error). It would give c = 2k = 10 anyway. |
| arXiv:2603.03182 (DeFranco, Nemec, Mar 2026), abstract | Non-stabilizer EA constructions; no explicit qutrit parameters. |
| arXiv:2512.17128 (Sok, Ezerman, Ling), search summary | MDS EA families from rational AG codes (length <= 10 over GF(9)). |
| Liu, Li, Shi, AMC 19(2) 2025, abstract | Quaternary (qubit) codes up to length 13. |
| Web searches for "[[25,5,12" and for 2025-2026 qutrit Hermitian, Hermitian-hull and AG EA codes | No [[25,5,>=12;<=8]]_3, and no [25,11,12]_9 with Hermitian hull 6. I found no paper on punctured or extended one-point Hermitian codes with optimized hulls at length 25. |
| V3R1T4S TROPHY_CASE.md (raw.githubusercontent.com, 09:38:04Z, HTTP 200, sha256 b946f68e...a1a1) | No EAQECC or qutrit entry. |
| V3R1T4S known-knowns/ (github.com tree pages, 09:38:20Z and 09:38:27Z, HTTP 200) | One folder for this target, 2026-10-17-anzal1-7b890c6f (README and INDEX fetched 09:38:35Z, HTTP 200): [[14,3,8;5]]_3 plus k = 0 neighbours. Lengthening gives d = 8 at most. |
| GitHub search API, open PRs for the target (09:37:15Z, HTTP 200, 14 hits); queries "qutrit" and "eaqecc" (09:37:23Z, HTTP 200, 15 hits each, adding closed PR #331) | Bodies read: #363, #403, #404, #405 (others); #643, #645, #646, #651, #710, #721, #726, #727, #728, #729 (the claim's author); #331 (closed, merged). No body names any length-25 code (checked by regex). Every exact code named was added to the closure: best value 11. |

## 5. Not read, and process notes

- **PR files (not read):** GET /repos/elder-plinius/V3R1T4S/pulls/N/files for the 15 PRs, at 09:37:45-46Z, all HTTP 403
  ("API rate limit exceeded"; the IP is shared). One loop sent all 15 requests within one second, before I saw the
  first 403. I retried none and did not try another route. Codes that appear only in PR files, not in the bodies, are
  therefore unchecked. CLAIM.md says no PR names a length-25 code; the bodies agree.
- **Papers not read in full:**
  - Cao, Li, Zhu, IEEE TIT 71(10) 2025: no arXiv version found.
  - Li, Li, Guan, Song, IJTP 63, 2024: not found online.
  - The full text of arXiv:2512.17128.
  arXiv:2607.02170 compared its codes against these papers; the qutrit codes it cites from them have n <= 16 or large c.
- **ar5iv:** one GET to ar5iv.labs.arxiv.org for 2105.02166 hung with no response. I killed my own curl after 2 min and used the arXiv PDF instead.
- **No-op fetches:** a first, malformed batch of three codetables URLs was rejected locally by curl (http_code 000, nothing sent). I resent each once with correct URLs.
- **WebFetch of the 2607.02170 PDF:** it returned no readable text (the tool cached the binary in its own store outside the work folder; I did not read it). I used the arXiv HTML instead.
- **Text addressed to reviewers:** none found in the fetched pages or PR bodies.
- **Background jobs:** none are left running. My first closure run was too slow; I killed it (my own PID) and rewrote it as a worklist. Every later run took a few seconds under a 60 s alarm.

pass: true
