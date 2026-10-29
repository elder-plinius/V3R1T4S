# CRITERION skeptic verdict: claim [[23,4,12;9]]_3 at cell (23,4,9)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

The claim meets the full success criterion, read literally, at the listed cell (n,k,c) = (23,4,9). The stabilizer matrix S
has 28 independent rows over GF(3) with 46 columns. rank(S J S^T) = 18, so c = 9 and k = 23 - 28 + 9 = 4. My own exhaustive
enumeration of all 3^18 - 1 = 387420488 nonzero vectors of span(S)^perp gives an exact EA minimum distance of 12. The live
page, re-fetched by me and byte-identical to the author's copy, lists the cell as [[23,4,11-18;9]]_3, so 12 > 11 = d_lower
and 12 <= 18 = d_upper. The page's own propagation rules, applied to its non-teleportation cells, give 11 at (23,4,9), so
the claim does not follow from them. The one route to 12 starts from the teleportation cell (23,3,3) and applies
"increasing dimension". The page never applies its rules to teleportation cells. Applying that one rule to the page's
teleportation cells also breaks 626 of the page's own d_upper values, so the route is not valid propagation. No hidden
quantifier, stretched definition, capped search, catalytic reading or c = 0 issue found.

## Phrase by phrase

1. **"an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1"**: object/eaqecc_23_4_12_9.json states n=23, k=4, c=9,
   d=12 (sha256 c64bdf57...f06f4, re-checked). c = 9 >= 1. Every value below is recomputed, not read from the file.
2. **"given by an exact generator matrix over GF(3) (symplectic form, 2n columns)"**: S has 28 rows x 46 columns, every
   entry in {0,1,2} (checked), rows (x|z), form x.z' - z.x'. Exact integers, no floats. The author's rebuild
   (rebuild/build_punct_obj.py with the REPRODUCE.md arguments) reproduces the same sha256 c64bdf57...f06f4.
3. **"s independent generators"**: my exact GF(3) row reduction (mine/prep.py) gives rank(S) = 28 = number of rows, so
   s = 28.
4. **"c = rank(S J S^T)/2"**: rank(S J S^T) = 18, so c = 9. This matches the claimed cell's c. c follows from the
   commutation structure, not from a free choice.
5. **"k = n - s + c"**: 23 - 28 + 9 = 4. This matches the claimed cell's k.
6. **"d computed exactly as the minimum weight of vectors in span(S)^perp outside span(S) ∩ span(S)^perp"**:
   - My prep (mine/prep.py) gives dim N = 18 for N = span(S)^perp, the symplectic dual. It gives dim I = 10 for
     I = span(S) ∩ N, computed as {aS : a(SJS^T) = 0} and cross-checked by s + dim N - rank(S + N) = 10. The basis of N is
     ordered with I first, so a vector lies outside I exactly when one of its last 8 coordinates is nonzero.
   - My own C program (mine/enum.c, run as mine/enum_infoset) enumerates all of N. It uses a GF(3) addition that
     self-tests on all 9 cases. Run time was 1.09 s and peak RSS 1409024 bytes. Results:
     - nonzero vectors: 387420488 = 3^18 - 1, so the search is complete, not sampled and not capped
     - vectors in I: 59048 = 3^10 - 1, all of weight >= 12; at weight 12 there are 8 in I and 2608 outside it
     - no vector of weight <= 11 exists anywhere in N
     - min weight outside I = 12, so d = 12
   - Isotropic vectors are not counted: weight is the symplectic weight, a position counts when x_i or z_i is nonzero, and
     only vectors outside I count.
   - Witness (mine/witness_check.py, independent Python): the enumerator's first weight-12 vector outside I has
     symplectic weight 12. It is orthogonal to all rows of S and is not in span(S).
   - Cross-check: the author's sb_enum gives the identical histogram (12: 2616 = 8 + 2608; 13: 33288 = 24 + 33264) and
     d_EA = 12.
7. **"for a cell of the live qutrit table ... re-fetched live immediately before claiming"**:
   - Author's fetch: 2026-10-25T09:53:51Z, sha256 37bbf731...936c.
   - My single honest GET (fetched/): started 2026-10-25T13:58:02Z, ended 2026-10-25T13:58:03Z, HTTP 200, 628039 bytes,
     sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. The two copies are identical, and the
     footer reads "Last change: 10.07.2025".
   - Row (23,4) lists c = 0,1,3,4,9,10,11,13,15,17,18,19. Cell (23,4,9) is listed as [[23,4,11-18;9]]_3 ("lengthening of
     [[19,4,11;9]] quantum shortening of [[20,3,12;9]] from arXiv:2207.05647"). It is the same (n,k,c) as claimed.
8. **"STRICTLY GREATER than the table's d_lower"**: 12 > 11. **"d <= d_upper"**: 12 <= 18. Both hold.
9. **"c = 0 excluded"; non-catalytic**: c = 9. The page header states the non-catalytic setting. The claim uses the
   standard stabilizer EA parameters with c taken from rank(SJS^T), with no catalytic reduction.
10. **Pitfall "Propagation-only improvements from existing table rows are not new"** (mine/closure2.py,
    mine/tele_rules.py, mine/tele_check.py, mine/examples.txt):
    - **The page's rules.** I parsed all 3888 cells of the fetched page, 124 of them titled "using teleportation". The
      legend gives 7 rules, each starting from a code [[n,k,d;c]]:
      - subcode: [[n,k-1,d;c]]
      - lengthening: [[n+1,k,d;c]]
      - puncturing: [[n-1,k,d-1;c]]
      - trivial: [[n,0,n+1;n]]
      - quantum shortening: [[n-1,k+1,d-1;c]]
      - increasing dimension: [[n,k+1,d;c+1]]
      - length reduction: [[n-1,k,d;c+1]]
    - **Closure without teleportation cells.** I applied the six derivation rules to every non-teleportation cell, with
      k >= 1 and k + c <= n, until nothing changed. The result is 11 at (23,4,9), and no listed cell with k >= 1 exceeds
      its own d_upper. So the claim is not subsumed by the page's propagation of its ordinary cells.
    - **The teleportation route.** The listed cell (23,3,3) is [[23,3,12-18;3]] "using teleportation". Increasing
      dimension six times, then subcode five times, would give 12 at (23,4,9). With only this seed added, the closure
      gives 12 there with no d_upper conflict.
    - **The page itself never propagates its teleportation cells.** It lists (23,4,4) as [[23,4,10-16;4]], where
      increasing dimension of [[23,3,12;3]] would give 12. It lists (23,2,2) as 14, where [[23,1,17;1]] would give 17.
    - **Increasing dimension applied to the teleportation cells contradicts the page's bounds.** That rule alone, applied
      to the 124 teleportation cells, pushes 626 listed cells (k >= 1) above their own d_upper. Example: [[8,1,6;1]]
      (teleportation) gives [[8,3,6;3]], but the page lists (8,3,3) with d_upper 5. Quantum shortening (764 cells) and
      length reduction (143 cells) break the bounds the same way. All rules together break 2700.
    - **Conclusion.** The page's bounds rule out applying these rules to teleportation cells, so the (23,3,3) route is
      not a propagation the page gives. The route would also need [[23,9,12;9]], which sits exactly at that cell's
      d_upper 12, where the page lists d_lower 10.
    - I read the teleportation cells as outside the page's propagation system, and the claim as not subsumed.
    - Residual: I did not establish from first principles whether increasing dimension can hold for this one specific
      teleportation code. Whether the result is new against the literature is the novelty skeptic's question, not
      checked here.
11. **Partial wins p1/p2**: not claimed and not needed. The claim is the full criterion.
12. **Null models / watch list**:
    - different (n,k,c): no, recomputed as (23,4,9)
    - isotropic vectors counted: no, the 8 isotropic weight-12 vectors are excluded and 2608 non-isotropic ones remain
    - part of span(S)^perp ignored: no, all 3^18 vectors enumerated
    - sampled or capped search: no
    - catalytic reading: no
    - c = 0: no
    - stretched criterion: no, every phrase is met in its plain sense

injection_suspected: none (no file or page content tried to direct my actions).

confirmed_scope: The GF(3) stabilizer matrix S in claim/object/eaqecc_23_4_12_9.json defines a non-catalytic EAQECC [[23,4,12;9]]_3 (s = 28, rank(SJS^T) = 18, exact minimum distance 12 by full enumeration of span(S)^perp), which exceeds the d_lower 11 and is within the d_upper 18 of the listed cell [[23,4,11-18;9]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched 2026-10-25T13:58:02Z (sha256 37bbf731...936c), and is not obtained by the page's propagation rules applied to its non-teleportation cells.

pass: true
