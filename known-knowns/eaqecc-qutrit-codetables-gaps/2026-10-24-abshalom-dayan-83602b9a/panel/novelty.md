context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/ and public sources

# Novelty skeptic: `[[28,5,15;11]]_3` (target `eaqecc-qutrit-codetables-gaps`)

Read: claim/CLAIM.md, claim/REPRODUCE.md, claim/table/RECORD.md (with qutrit.headers.txt), the metadata and
`construction` field of claim/object/eaqecc_28_5_15_11.json, and claim/rebuild/ (build_claim.py, hermitian.py). Nothing
else under runs/ was opened. The claimed object is the extended one-point code E(13) of the Hermitian curve
y^3 + y = x^4 over GF(9): a [28,11]_9 code. Its 28th coordinate marks the pole-order-13 monomial. Its Hermitian hull
has dimension 6, giving k = 11 - 6 = 5 and c = 28 - 11 - 6 = 11. The claimed d = 15 is the reproduce panel's job. This
report assumes it and asks only whether anything known already reaches d >= 15 at (n,k,c) = (28,5,11).

**Bottom line:** nothing published, in this repository, or in its pull requests reaches d >= 15 at (28,5,11). The table
says 13. But published data from Christensen, Munuera, Pereira and Ruano (arXiv:2105.02166), combined with the table's
own propagation rules, already imply **14** there. So the honest margin is +1 over everything known (15 vs 14), not +2
over the table. Pass, with that caveat.

## 1. Status page: one honest fetch

| item | value |
|---|---|
| URL | https://eaqecc.codetables.de/qutrit.php |
| method | one plain `curl` GET, User-Agent `V3R1T4S-research-agent (honest single fetch)`, no retries, no cookies |
| UTC time (date -u) | start 2026-10-24T11:13:23Z, end 2026-10-24T11:13:24Z; server header `date: Sat, 24 Oct 2026 11:13:23 GMT` |
| HTTP status | 200 (`http_code=200 size=628039`) |
| sha256 of body | `37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c` (identical to all three fetches in claim/table/RECORD.md) |
| footer | `Last change: 10.07.2025` |
| saved as | panel/work-novelty/qutrit.php, panel/work-novelty/qutrit.headers.txt |

The cell (n,k,c) = (28,5,11), verbatim:

```
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[27,5,13;11]] subcode of [[27,8,13;11]] from arXiv:2207.05647">[[28,5,13-22;11]]<sub>3</sub></TD>
```

So d_lower = 13 and d_upper = 22. The claimed d = 15 satisfies 13 < 15 <= 22.

Other entries in the same row (n = 28, k = 5), parsed from the page into panel/work-novelty/cells.tsv (3888 cells):
c=0: 9-11; c=3: 10-14; c=5: 12-19 (teleportation); c=11: 13-22; c=12: 14-22; c=13: 16-22; c=15: 17-22;
c=17: 18-23; c=19: 19-23; c=21: 20-23; c=23: 21-24.

## 2. Sources checked

| source | what it covers | relevance to (28,5,11) |
|---|---|---|
| Grassl qutrit EAQECC table (fetch above) | all qutrit cells n <= 36; at n = 28 no stabilizer entry has d >= 15 with c < 13 | d_lower 13 |
| Luo, Ezerman, Grassl, Ling, arXiv:2207.05647v2 (QIP 23:4, 2024), Table 2 (217 qutrit entries parsed) | the table's source. n=27: [[27,8,13;11]], [[27,7,14;12]], [[27,4,16;13]], ... n=28: [[28,8,14;12]], [[28,5,16;13]], [[28,4,17;14]], ... | nothing with d >= 15 and c <= 12 at n = 27..29. Theorem 12 ("More Entanglement", pure Hermitian-construction codes, `[[n, κ+i, δ; c+i]]` for i <= hull dim) is the table's "increasing dimension". Theorem 18 ("Less Entanglement") only gives `δ' ≤ δ`, so it implies no distance |
| Christensen, Munuera, Pereira, Ruano, arXiv:2105.02166v2 (AMC 17(1), 2023): EAQECCs from one-point Hermitian codes, q = 3 worked out | lists [[27,1,19;16]]_3, [[27,4,16;13]]_3, [[27,6,13;9]]_3, [[27,9,10;6]]_3, [[27,13,7;4]]_3, [[27,16,4;1]]_3. Its Table 2 "allows us to compute Δ(m) for all values of m" | affine C(12) and C(13) give [[27,4,15;11]] and [[27,4,14;9]] (section 4), which imply 14 at the cell |
| Li, Ezerman, Li, Ling, Sun, arXiv:2607.02170 (Jul 2026, generalized extended codes) and its data repo yanglimath/SI-EAQECCs-from-GECs (Tables V and VII ternary TSVs downloaded) | 14 new qutrit codes n <= 25, plus 5 recent-literature qutrit codes (Cao-Li-Zhu IEEE TIT 2025; Liu-Li-Shi AMC 2025; Li-Li-Guan-Song IJTP 2024; Li-Zhu DM 2024) | all have c >= 13 or d <= 9; no rule lowers c, so none can reach (28,5,11) at d >= 15 |
| Sok, Ezerman, Ling, arXiv:2512.17128 (Dec 2025), Hermitian hulls of rational AG codes | MDS EAQECCs from rational (genus-0) AG codes | rational curves over GF(9) give short MDS codes. The search summary: "by the classical MDS conjecture, the length of an MDS code over F_{q^2} is bounded by q^2+1". Not length 28 |
| Luo, Sok, Ezerman, Ling, arXiv:2404.04993 (2024); Anderson et al., arXiv:2212.14521 (relative hulls, 2022/2023) | MDS EAQECCs via hulls (abstracts) | MDS lengths only; no GF(9) length-28 code |
| Kshirsagar, Matthews, Shapiro, arXiv:2608.09886 (Aug 2026), EA quantum LRCs incl. Hermitian and Suzuki specializations | symbolic families (Prop. 5.13, 5.14); explicit examples are over F_13, F_29, F_(43^2) | no q = 3 instance |
| Kumar, Bandi, arXiv:2608.06854 (Aug 2026) | EA quantum LRC bounds; Tamo-Barg and cyclic constructions (abstract) | no qutrit length-28 code |
| Galindo, Hernando, Matsumoto, arXiv:2303.03079 (Steane enlargement of EAQECCs) | explicit tables: binary, 4-ary, 9-ary at n = 728 | no ternary codes |
| DeFranco, Nemec, arXiv:2603.03182 (Mar 2026); Zengin, Köroğlu, arXiv:2606.02137 (Jun 2026) | non-stabilizer EA codes (qubits); codes over F2 x (F2+vF2) | not qutrit |
| codetables.de classical entry [28,11] over GF(9), one GET at 2026-10-24T11:24:13Z, HTTP 200, sha256 `5e5168911fca26878525fd252b42d46d563a4fb02794ceb32916e350f57e333f` | "lower bound: 15 upper bound: 16"; "AlgebraicGeometricCode from the curve [1] which is based on 2 divisors of degree [ 3, 4 ]"; "last modified: 2003-10-23" | the classical [28,11,15]_9 ingredient has been public since 2003. Its Hermitian hull, and so the EAQECC, is not published anywhere found. This is a credit caveat, not a novelty failure |
| web search for the parameter string "[[28,5,15;11]]" / "[[28, 5, 15; 11]]" | exact-match search | no hit (search engines index such strings poorly) |
| repo TROPHY_CASE.md | 53 rows, six families | no EAQECC row |
| repo known-knowns/eaqecc-qutrit-codetables-gaps/ | one package, 2026-10-17-anzal1-7b890c6f: [[14,3,8;5]]_3 | unrelated cell; lengthening keeps d = 8 |
| repo known-unknowns/physics/eaqecc-qutrit-codetables-gaps.md | target description | no result |

## 3. Pull requests of elder-plinius/V3R1T4S (read-only, unauthenticated GitHub API GETs, 2026-10-24T11:20:05Z)

- Open PRs: all 310 listed (4 pages: numbers 9 to 638). Those touching EAQECC/qutrit: #363 [[33,1,31;24]]_3,
  #403 [[16,4,8;4]]_3, #404 [[34,2,24;24]]_3, #405 [[33,3,23;24]]_3.
- Search over all states, `is:pr eaqecc` and `is:pr qutrit`: 5 PRs each (#331 closed [[14,3,8;5]]_3, plus the four
  above). `is:pr hermitian`: 6 (the same five minus #363, plus #509 qubit [[23,9,5]] and #614 AME states).
  Search `"[[28"`: 75 hits, mostly other families. The only EAQECC mentions are #331 and #606, an audit that touches
  only the [[14,3,8;5]] README credits.
- None claims (28,5,11) or any n = 27..29 qutrit code. The PR codes have c >= 24 or d = 8, so none can imply d >= 15
  at c = 11 (they are included in the closure below anyway).

## 4. Implied codes

No propagation rule in the page legend lowers c: subcode, lengthening, puncturing and quantum shortening keep it;
increasing dimension and length reduction add 1. So any implying code needs c <= 11 and d >= 15 (or d >= 16 if one
puncturing or shortening step is used).

1. **Table entries.** No non-teleportation entry at any n has d >= 15 with c <= 11 that reaches the cell, which is why
   the page shows 13. Teleportation entries [[28,3,15;3]], [[28,4,15;4]], [[29,3,16;3]] and [[29,4,15;4]] have small c.
   But the table applies no dimension-raising rule to them: (28,5,5) is 12-19 "using teleportation". LEGL Theorem 12
   needs a pure code from the Hermitian construction, which these are not, and they are not stabilizer codes as the
   criterion requires.
2. **Christensen et al. data.** I recomputed the Hermitian hulls independently (panel/work-novelty/scripts/herm_hulls.py,
   output herm_hulls.out). They match the paper's listed [[27,4,16;13]] (C(11)) and [[27,6,13;9]] (C(14)), so the method
   agrees with the paper. The same data give:
   - C(12): [27,10]_9, hull 6, so [[27,4,15;11]]. d(C(12)) is exactly 15: (x-a1)...(x-a4) has 12 distinct zeros
     (c12_word.out). The EA distance is also exactly 15: 2322 of 2340 weight-15 words from three non-vertical lines lie
     outside the hull (c12_lines.out). The 126 words from vertical lines all lie inside it (minwords_vs_hull.out).
   - C(13): [27,11]_9, hull 7, so [[27,4,14;9]]. All 60 explicit weight-14 words lie outside the hull, so the EA
     distance is exactly 14 (minwords_vs_hull.out).
   - Implied at (28,5,11): **14**, by two routes. (a) [[27,4,14;9]], then Theorem 12 twice to [[27,6,14;11]], then
     lengthening to [[28,6,14;11]], then subcode to [[28,5,14;11]]. (b) [[27,4,15;11]], then quantum shortening to
     [[26,5,14;11]], then lengthening twice. Neither reaches 15. So the table's 13 is already stale against published
     data, and the claim's margin over everything known is +1.
3. **Permissive closure** (panel/work-novelty/scripts/closure.py, output closure.out). Starting from every source above
   (all non-teleportation page cells, the 217 LEGL Table 2 entries, Hermitian C(m) for m = 8..17, the GEC tables, and
   the PR codes), I applied all six legend rules plus c-monotonicity with no preconditions. That over-estimates what is
   implied. Result: "table-only start value at (28,5,11): 13", "closure value at (28,5,11): 14" (route 2b).
4. **Context.** The table's [[28,4,17;14]] and [[28,5,16;13]] match my extended codes E(11) and E(12) exactly
   (hulls 5 and 5). The claim is the next member, E(13) with hull 6, of the same extended Hermitian family. That fits
   "known ingredients, new parameter", not a rediscovery. A side observation, not part of this claim: E(14) has hull 6
   and gives [[28,6,>=14;10]], where the table has 12.

## 5. Text addressed to reviewers

None seen in the status page, papers, data files, repository files or PR texts I read.

## 6. Verdict

The claimed [[28,5,15;11]]_3 is strictly above the live table (13) and above the best value I can derive from any
published code (14, via arXiv:2105.02166 data and arXiv:2207.05647 rules). No paper, repository row or pull request
reaches 15. Caveats for whoever writes the record:
- State the comparison as 15 vs 14 (implied by published data) as well as 15 vs 13 (table).
- Credit the classical [28,11,15]_9 Hermitian-curve code (codetables.de, 2003) and the hull method of
  Christensen et al. and LEGL.
- This verdict assumes the reproduce panel confirms d = 15.

pass: true
