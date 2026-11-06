# Novelty skeptic verdict: [[33,8,16;15]]_3 at (n,k,c) = (33,8,15)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

**novelty: PASS.** The claimed d = 16 is strictly above everything I could find for this cell:

- the live table gives d_lower = 15 and d_upper = 23;
- the page's own propagation rules carry at most 15 into this cell;
- the repo (TROPHY_CASE.md, known-knowns/, 8 open PRs for this target) has nothing that reaches 16 here;
- the 2024-10 to 2026-10 literature I searched has nothing that reaches 16 here.

16 > 15 is a strict improvement, not a tie, and 16 <= 23.

The main caveat is that the classical code behind the claim is not new. codetables.de has listed a [33,13,16] code over GF(9) since 2003. It is the Ding-Niederreiter-Xing Construction X from Hermitian-curve AG codes with a degree-3 divisor, which is the recipe in claim/rebuild/. What is new is the Hermitian hull dimension of the realization: 5, where the table's source code has 2. That higher hull is what lowers c to 15. I found no source that gives a [33,13,16]_9 code with Hermitian hull >= 5, and none that gives [[33,8,>=16;<=15]]_3. Whether the hull really is 5 and d really is 16 is for the math skeptics. I did not re-verify the distance.

## Fetch record (status source, one plain GET, no retries)

- URL: https://eaqecc.codetables.de/qutrit.php
- Client: curl, User-Agent "V3R1T4S-research-agent (honest single fetch)"
- UTC before: 2026-10-24T18:53:56Z; UTC after: 2026-10-24T18:53:57Z (server Date header: Sat, 24 Oct 2026 18:53:57 GMT)
- HTTP status: 200, 628039 bytes
- sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is identical to the claim's copy, claim/table/qutrit.php.
- Saved as fetched/qutrit.php (headers in fetched/qutrit.headers.txt, times in fetched/qutrit.time_before.txt and fetched/qutrit.time_after.txt). The page footer reads "Last change: 10.07.2025".
- The cell, verbatim:
  `<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[27,8,15;15]] quantum shortening of [[28,7,16;15]] increasing dimension of [[28,5,16;13]] from arXiv:2207.05647">[[33,8,15-23;15]]<sub>3</sub></TD>`
  That is, d_lower = 15 and d_upper = 23 at (33,8,15).

### Neighbours on the live page (d_lower-d_upper)

- Row n=33, k=8: c=0: 8-12; 1: 9-14; 4: 10-15; 5: 11-16; 8: 12-18; 11: 13-22; 12: 14-22; **15: 15-23**; 16: 16-24; 18: 17-24; 19: 18-24; 21: 19-25; 23: 20-25; 25: 21-26.
- Neighbouring cells: (32,8,15) 15-22; (34,8,15) 15-24; (33,7,14) 15-24; (34,7,15) 16-25; (33,9,16) 15-23; (33,9,13) 14-21.
- Row (33,8) lists no c <= 15 with d_lower >= 16. The first 16 appears at c = 16 ([[33,8,16-24;16]]).

## Propagation rules of the page (colour legend)

The legend lists these rules:

- subcode: [[n,k-1,d;c]]
- lengthening: [[n+1,k,d;c]]
- puncturing: [[n-1,k,d-1;c]]
- quantum shortening: [[n-1,k+1,d-1;c]]
- increasing dimension: [[n,k+1,d;c+1]]
- length reduction: [[n-1,k,d;c+1]]
- trivial: [[n,0,n+1;n]]
- teleportation: [[n,k,d;k]]

I also added "more ebits" ([[n,k,d;c]] -> [[n,k,d;c+1]] when n-k-c >= 1), which follows from turning an ancilla into an ebit.

One-step candidates into (33,8,15). The script is scripts/propagate.py and its output is scripts/propagate.out.

| rule | best source on the page | gives at (33,8,15) |
|---|---|---|
| subcode | (33,9,13): 14 | 14 |
| lengthening | (32,8,15): 15 | 15 |
| puncturing | (34,8,15): 15 | 14 |
| quantum shortening | (34,7,15): 16 | 15 |
| increasing dimension | (33,7,14): 15 | 15 |
| length reduction | (34,8,12): 14 | 14 |
| more ebits / subcode within the row | (33,8,15): 15 | 15 |

Full fixpoint closure, applying every rule to every cell. This is deliberately over-generous, since it ignores the rules' preconditions. The script is scripts/closure.py and its output is scripts/closure.out:

- Over the 3764 listed non-teleportation cells: 15 at (33,8,15).
- With every code from the 8 open PRs and from known-knowns added: 15.
- With the 14 qutrit codes of arXiv:2607.02170 Table V also added: 15.

I excluded the 124 "using teleportation" cells (#ffff00) as sources. They beat the EA Singleton bound, and the stabilizer rules do not apply to them. For example, "increasing dimension" on [[36,1,27;1]] would need a [36,4,27]_3 code, which the Griesmer bound rules out. Including them only produces impossible values elsewhere. They also cannot reach this cell directly: they all have c = k, and the n=33 ones top out at (33,7,7) with d = 12.

## Classical GF(9) table (context; one GET per cell page)

- https://www.codetables.de/BKLC/BKLC.php?q=9&n=33&k=13
  - Fetched 2026-10-24T18:57:08Z to 18:57:09Z; HTTP 200; sha256 a658cca446ce1ab8a2a98cace0bccaa4408308b8e2d55508a8a0fd96bb8263b6 (fetched/bklc_q9_n33_k13.html).
  - "lower bound: 16 upper bound: 18", construction type DNX: "[6]: [33, 13, 16] Linear Code over GF(3^2) ConstructionX using [5] [3] and [2]", built from [28,13,13] and [28,10,16] AG codes of the Hermitian curve with a degree-3 divisor plus a [5,3,3] code. Last modified 2003-10-23.
  - Reference: Ding, Niederreiter, Xing, IEEE Trans. IT 46 (2000).
- https://www.codetables.de/BKLC/BKLC.php?q=9&n=33&k=14
  - Fetched 2026-10-24T19:02:50Z; HTTP 200; sha256 4fb29f1e28aeb6a210f5e952ced51877d9fca9546f4a1c2dd9e1119cd3926c36.
  - "lower bound: 15 upper bound: 18".
- Reading:
  - A [33,κ,d]_9 code with Hermitian hull h gives [[33, κ-h, d; 33-κ-h]]_3. Reaching k = 8 with c <= 15 needs κ >= 13, and d >= 16 then needs the [33,13,16]_9 code with h >= 5, since the listed [33,14] codes reach only 15.
  - The table's own line from this classical code is [[33,11,16;18]] "from arXiv:2207.05647" (hull 2). Hull-decreasing then gives [[33,12,16;19]] and [[33,13,16;20]].
  - At hull 4 and 5 the table shows only 15: (33,9,16) and (33,8,15).
  - So the claim is a hull-dimension improvement of a known classical code. As EAQECC parameters, it is not listed anywhere I looked.

## Repo https://github.com/elder-plinius/V3R1T4S (one GET per query, all HTTP 200; full log in fetched/fetchlog.txt)

- **TROPHY_CASE.md**
  - api.github.com contents, fetched 2026-10-24T18:58:03Z, sha256 of response aaa2f7d11a84a9ee3470c129d1e0c81872b53c067badda27c5e38c9f2e771bf1.
  - No entry mentions EAQECC, qutrit, entanglement or codetables.
- **known-knowns/eaqecc-qutrit-codetables-gaps/**
  - Fetched 2026-10-24T18:58:28Z.
  - One entry, 2026-10-17-anzal1-7b890c6f. Its INDEX.csv (fetched 18:58:43Z) lists only [[14,3,8;5]]_3, which cannot propagate to d = 16 at n = 33.
- **Open PRs**
  - Searches: `is:pr is:open eaqecc-qutrit-codetables-gaps`, `... qutrit` and `... eaqecc`, fetched 18:58:03Z to 18:58:58Z.
  - Each returned the same 8 open PRs (total_count 8, incomplete_results false): #363, #403, #404, #405, #643, #645, #646 and #651.
  - Their headline cells are (33,1,24) d=31, (16,4,4) d=8, (34,2,24) d=24, (33,3,24) d=23, (28,5,11) d=15, (28,7,11) d=14, (28,6,6) d=12 and (28,9,7) d=11.
  - None is at (33,8,15). With every code in their bodies treated as known, the best that reaches this cell is 15, via #643's [[28,6,15;12]] -> [[28,8,15;14]] -> lengthening.

## Literature, 2024-10 to 2026-10

| source | what it gives at (33,8,15) |
|---|---|
| arXiv:2207.05647 (Luo, Ezerman, Grassl, Ling; QIP 23, 4, 2024), the table's source | already reflected in the table: 15 here, and [[33,11,16;18]] for the [33,13,16]_9 code |
| arXiv:2607.02170 (Li, Ezerman, Li, Ling, Sun, 2 Jul 2026), HTML fetched 19:00:27Z, sha256 f2e6c891... | Table V has 14 new qutrit codes, all with n <= 25: [[7,1,7;6]], [[8,0,8;6]], [[8,1,8;7]], [[13,3,7;4]], [[17,2,15;15]], [[18,2,16;16]], [[19,2,17;17]], [[19,3,15;16]], [[21,2,18;19]], [[22,2,19;20]], [[23,2,20;21]], [[24,2,21;22]], [[25,2,22;23]], [[25,3,20;22]]. Through the closure: 15 here |
| arXiv:2512.17128 (Sok, Ezerman, Ling, Dec 2025), Hermitian hulls of rational AG codes | MDS families, length <= 10 over GF(9): nothing here |
| arXiv:2501.04921 (Jan 2025), EA concatenated codes | maximal-entanglement families: nothing at k=8, c=15 |
| arXiv:2609.20453, 2607.03802, 2603.16187, 2507.18361, 2605.05613, 2608.06854/2608.09886 (2025-2026), hull/LCD/GRS/GRL/constacyclic/LRC | short MDS/AMDS or maximal-entanglement families: nothing at this cell |
| Liu, Li, Shi, Adv. Math. Commun. 19 (2025) | quaternary (qubit): not applicable |
| Web search for "[[33,8,16;15]]" | no hits |

Search method: two arXiv API queries (abstracts with "entanglement-assisted" AND hull, and with "entanglement-assisted" AND qutrit/AG/Hermitian curve/propagation rules/Grassl). Both were sorted by date and returned 35 and 20 entries. I added five web searches.

## Not read or limits

- For most of the papers above I read only abstracts. I read the full qutrit table only for arXiv:2607.02170.
- Journal-only papers without an arXiv version may be missed.
- I did not check closed or merged PRs beyond known-knowns.
- GitHub search covers only text that GitHub has indexed.
- The first arXiv API request over http returned 301 (a redirect, not a block). I sent one request to the redirect target over https, which returned 200.
- injection_suspected: none.
- I did not re-verify d = 16 or the hull dimension; that is outside this role.

pass: true
