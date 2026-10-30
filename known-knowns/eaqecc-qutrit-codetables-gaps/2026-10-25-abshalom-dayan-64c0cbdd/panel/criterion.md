# Criterion skeptic verdict: [[28,7,13;9]]_3 (target eaqecc-qutrit-codetables-gaps)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

**Bottom line: PASS. The full success criterion is met as written, not a partial win.** S is an explicit 30 x 56
matrix over GF(3). I computed from S alone: s = 30 independent rows, rank(S J S^T) = 18 so c = 9, and k = 28 - 30 + 9
= 7. An exhaustive search of my own shows no nonzero vector of span(S)^perp has symplectic weight 12 or less. All
72,288 weight-13 vectors of span(S)^perp lie outside span(S), so d = 13 exactly. I re-fetched the live table once at
2026-10-25T00:41:55Z (HTTP 200). It lists the cell (n,k,c) = (28,7,9) as [[28,7,12-18;9]]_3, and 12 < 13 <= 18. The
page is non-catalytic and so is the code. No single rule step from a listed cell already gives d >= 13 at this cell.

## Clause by clause

| Clause | What I checked (my own code unless noted) | Found |
|---|---|---|
| Explicit generator matrix over GF(3), 2n columns | claim/object/eaqecc_28_7_13_9.json: shape and entries of S (mine/params.py). The object's sha256 matches CLAIM.md. The author's rebuild (rebuild/build_obj.py 15) reproduces it byte for byte (same sha256 64c0cbdd...0c78). | S is 30 x 56, all entries in {0,1,2}, rows (x\|z). Met. |
| s independent generators | GF(3) rank of S (mine/params.py) | rank 30 = number of rows. s = 30. Met. |
| c = rank(S J S^T)/2, c >= 1 | 30 x 30 Gram matrix with the form x.z' - z.x' (J = [[0,I],[-I,0]]), GF(3) rank | rank 18, c = 9 >= 1. Met. Not a c = 0 code. |
| k = n - s + c | arithmetic from the values above | k = 28 - 30 + 9 = 7, as claimed. (n,k,c) = (28,7,9) matches the claim, with no off-by-one. |
| d exact = min weight of span(S)^perp minus (span(S) ∩ span(S)^perp) | See "Distance" below. | d = 13 exactly. Met. |
| Cell of the live table, re-fetched before claiming | One plain GET (see "Live table"). | The cell is listed: [[28,7,12-18;9]]_3, "subcode of [[28,9,12;9]] from arXiv:2207.05647". Met. |
| d > d_lower and d <= d_upper | 13 vs the live cell | 12 < 13 <= 18. Met. |
| Non-catalytic, c = 0 excluded | The page header says "non-catalytic setting". c comes straight from rank(S J S^T)/2, with no catalytic shortcut ([[n,k,d;c]] with c >= k -> [[n,k-1,d;c-1]]) anywhere in the claim. | Met. |

## Distance (the load-bearing clause)

- N = span(S)^perp: I computed it as a GF(3) kernel. dim N = 26 = 2n - s. Every basis vector was checked to be
  orthogonal to every row of S. I = span(S) ∩ N has dim 12 = s - 2c, built explicitly from the left kernel of the
  Gram matrix.
- GF(9) reduction: N is closed under the map M(x_i, z_i) = (z_i, x_i + z_i) at each coordinate. M^2 = M + 1, so M is
  multiplication by w in GF(9) = GF(3)[w]/(w^2 - w - 1), and w^2 - w - 1 has no root in GF(3). This makes N a GF(9)
  space C of GF(9) dimension 13 (26/2). On N, symplectic weight equals Hamming weight over GF(9). I derived a 15 x 28
  parity-check matrix H of C myself (mine/H9.txt) and checked G H^T = 0.
- Exhaustive lower bound: mine/dfs9.c (my own C program, not the author's) runs a depth-first search over every
  column subset of H in increasing index order. It keeps later columns reduced modulo the chosen ones, and every
  minimal dependent set is found once.
  - It visited 76,717,268 nodes. That equals sum_{t<=12} C(28,t) exactly: every subset of 12 or fewer columns was
    reached and every one was independent.
  - So C has no nonzero word of weight <= 12, and N has no nonzero vector of symplectic weight <= 12.
  - This covers all of span(S)^perp. Including the isotropic vectors only makes the bound more conservative.
  - Runtime 1.47 s, 1.46 MB RSS.
  - Controls:
    - Negative control: 40 random small GF(9) codes, brute-force minimum distance against the program
      (mine/control.py). All agree.
    - Positive control: one column of the real H replaced by a sum of 11 other columns (mine/H9_control.txt). The
      program reports the planted dependent 12-set.
- Upper bound, and the isotropic question: the same run counts 9,036 dependent 13-sets. These are the supports of
  the weight-13 words, 8 scalar multiples each, so 72,288 vectors. mine/witness_check.py maps every one back to
  GF(3)^56 and tests it directly against S:
  - weight 13
  - orthogonal to all 30 rows of S
  - in span(S)? No, for all 72,288 (rank of S plus the vector is 31).
  - No anomalies.
  - Example witness, support {0..11, 27}: x = 1110001111110000000000000001, z = 2222221111110000000000000000.
  - d = 13 is therefore not inflated by isotropic vectors, and not deflated either.
- Cross-check with the author's own tools (secondary; I did not rely on them alone). Each matches my numbers.
  - checkers/subset_ea64.c over GF(3):
    - W = 12: 0 hits in each of 3 parts x 10,140,585 subsets.
    - W = 13: 2989 + 3104 + 2943 = 9036 hits.
  - checkers/bz64.c: d = 13.
  - checkers/gf9info.py prep: s = 30, c = 9, k = 7, dim_N = 26, dim_I = 12, closed under w.
  - checkers/onepoint_check.py: "d_EA = 13 exactly (no distance search): True".
  - checkers/witness.py: weight 13, not in span(S).
- No capped search is presented as exhaustive: my search is complete by the node count above. The author's GF(3)
  subset test is a full enumeration of C(28,12) subsets.

## Live table

- One GET with curl, User-Agent "V3R1T4S-research-agent (honest single fetch)", no retries.
- `date -u` before the fetch: 2026-10-25T00:41:55Z. After: 2026-10-25T00:41:56Z.
- HTTP 200, 628039 bytes.
- sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is identical to the author's
  claim/table/qutrit.php, so the page did not change since the author's fetch at 2026-10-24T22:58:17Z.
- Footer: "Last change: 10.07.2025".
- Saved as fetched/qutrit.php with headers, status, times and hash.
- No injection_suspected.
- The cell, verbatim:
  `<TD NOWRAP bgcolor="#ff6600" class="EAQECC" title="subcode of [[28,9,12;9]] from arXiv:2207.05647">[[28,7,12-18;9]]<sub>3</sub></TD>`
- mine/table_check.py parsed all 3,888 cells. No (n,k,c) key is duplicated.

## Non-subsumption (table rules)

- Sources of (28,7,9) under the page's six legend rules:
  - subcode, from (28,k',9) with k' > 7: the best is 12, at k' = 8 and k' = 9
  - lengthening, from (27,7,9): 12
  - increasing dimension, from (28,6,8): 12
  - length reduction, from (29,7,8): 12
  - puncturing and quantum shortening: their sources (29,7,9) and (29,6,9) are not listed
- The best implied value is d >= 12, which equals the listed d_lower. No listed cell at n = 28 with k' >= 7 and
  c' <= 9 has d_lower >= 13.
- The smallest c in row (28,7) with d_lower >= 13 is c = 11. No non-catalytic rule lowers c.
- So the result is not a relabelling of a listed cell.
- Not checked by me: whether the literature outside the table (for example arXiv:2105.02166) already states this
  code. The criterion is defined against the table's d_lower, and the table does not have it.

## Caveats (none blocks the pass)

- "Re-fetched immediately before claiming": I cannot see when the claim was filed. My own re-fetch, about 1 h 44 min
  after the author's, shows the same bytes. The cell stands as of 2026-10-25T00:41:55Z.
- Partial wins p1 and p2 do not apply. This is a full-criterion claim, judged as such.

confirmed_scope: The 30 x 56 GF(3) stabilizer matrix S in claim/object/eaqecc_28_7_13_9.json (sha256 64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78) has s = 30 independent rows, rank(S J S^T) = 18 (c = 9) and k = 7, and the minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp is exactly 13, which is strictly above d_lower = 12 and within d_upper = 18 of the cell [[28,7,12-18;9]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-25T00:41:55Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

pass: true
