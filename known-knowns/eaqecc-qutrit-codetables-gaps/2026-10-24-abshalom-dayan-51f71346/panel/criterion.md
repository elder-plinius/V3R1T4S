# Criterion skeptic verdict: eaqecc-qutrit-codetables-gaps, claim [[28,6,12;6]]_3
context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

The object meets the FULL success criterion as literally written. It is not just a partial win (p1 or p2).
From S alone, my own code gets s = 28, c = 6, k = 6 and d = 12 exactly. The live cell (n,k,c) = (28,6,6) reads
[[28,6,11-17;6]]_3, so 11 < 12 <= 17. My single live re-fetch returned a page byte-identical to the author's copy.

One worry is worth passing on. It does not change the literal answer, but it matters for novelty. The same live page lists
[[28,5,12-19;5]]_3 "using teleportation". The page's own "increasing dimension" rule, [[n,k,d;c]] -> [[n,k+1,d;c+1]],
would turn that into [[28,6,12;6]] if the rule applied to teleportation entries. The table does not apply it: the
(28,6,6) cell reads 11. Teleportation schemes are not stabilizer EAQECCs of the kind the criterion defines, so the
printed d_lower = 11 is the table's real value. CLAIM.md and table/RECORD.md do not mention this neighbouring cell.

## Condition-by-condition check (criterion text read literally)

| # | Condition in the criterion | What the object must satisfy | Checked result |
|---|---|---|---|
| 1 | "explicit EAQECC ... given by an exact generator matrix over GF(3) (symplectic form, 2n columns)" | S is an exact integer matrix over GF(3) with 2n columns | S is 28 x 56, all entries in {0,1,2}, rows (x\|z), form x.z' - z.x' (J = [[0,I],[-I,0]]). Met. |
| 2 | "s independent generators on Alice's n qutrits" | s = rank(S); the rows are generators on n = 28 qutrits | rank(S) = 28 = number of rows, so the rows are independent. s = 28. Met. |
| 3 | "c = rank(S J S^T)/2" | c from the commutation matrix | The Gram matrix is antisymmetric and has rank 12, so c = 6. Met. |
| 4 | "c >= 1" / "c = 0 excluded" | c >= 1 | c = 6. Met. |
| 5 | "k = n - s + c" | k matches the cell's k | k = 28 - 28 + 6 = 6. Met. |
| 6 | d is "the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp" | d computed exactly under this definition | dim span(S)^perp = 28 and dim of the isotropic part = 16 (= s - 2c). d >= 12: no vector of span(S)^perp outside the isotropic part has support in any of the C(28,11) = 21474180 sets of 11 positions. d <= 12: explicit witnesses below. d = 12. Met. |
| 7 | "for a cell of the live qutrit table" | (28,6,6) is a listed cell | Listed verbatim on the live page (see below). Met. |
| 8 | "re-fetched live immediately before claiming" | a live read of the page close to the claim | The author fetched at 15:03:31 UTC (RECORD.md; the saved server Date header agrees). The claim files in the folder carry mtime 15:16:56 UTC, 13 min 25 s later. My re-fetch 1 h 4 min after the author's was byte-identical. Met in substance. The folder has no explicit claim timestamp, so "immediately" can only be bounded by file times. |
| 9 | "STRICTLY GREATER ... than the table's d_lower for that (n,k,c)" | d > d_lower | 12 > 11. Met. |
| 10 | "and d <= d_upper" | d <= d_upper | 12 <= 17. Met. |
| 11 | "over GF(9) (trace-Hermitian form)" alternative | not needed, since the GF(3) form is given | For consistency: S equals phi(D9) row by row, and span(S)^perp equals phi(GF(9)-span of G9), with GF(9) = GF(3)[w]/(w^2 - w - 1) (irreducible) and phi(a + b w) = (a\|b). |

## My own computations (no code shared with the author's)

- mine/params.py (pure Python, my own GF(3) row reduction) works from S only. It prints `s=rank(S)=28`,
  `Gram_antisymmetric=True`, `rank(SJS^T)=12`, `c=6`, `k=n-s+c=6`, `dim span(S)^perp=28`, `dim isotropic part=16`
  (also 16 by the dimension formula), and `span(S)^perp closed under w: True`. It writes bases of span(S)^perp (N) and
  of the isotropic part (I).
- mine/subsets.c is my own bit-sliced GF(3) code. It self-tests addition on all 9 pairs. Then it enumerates every
  support T, using the complement U and pruning when rank is full. A support T holds a vector of N outside I exactly when
  dim N_T > dim I_T. It agreed with pure-Python ranks on 60 random supports with 0 mismatches.
  - W = 11: total leaves 21474180 = C(28,11); supports with any nonzero vector of N = 0; supports with a vector
    outside I = 0. So d >= 12, and even the isotropic part has no nonzero vector of weight <= 11.
  - W = 12: total leaves 30421755 = C(28,12); supports with a nonzero vector of N = 7119; supports with a vector
    outside I = 7056. Both match the author's independently reported counts.
- mine/witness_mine.py (pure Python) solves for explicit vectors from S alone. On (0-based) positions 15..26:
  x|z = 0000000000000002222221111110 | 0000000000000001111111110000, with `symplectic_weight=12`,
  `orthogonal_to_all_rows_of_S=True`, `in_span_S=False`. Two more supports found by the enumeration
  (1,11,13,15,16,18,21,22,23,24,25,27 and 1,2,3,14,15,16,17,18,19,22,26,27) also give weight-12 witnesses outside
  span(S). So d <= 12.
- I also re-ran the author's tools in mine/author_rerun. The rebuild reproduces sha256
  51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573. infoset m=17 gives deficient=0 in all four parts,
  with subsets summing to C(28,17). subset_ea W=11 gives with_vector_outside_isotropic=0 in all four parts. Both of the
  author's witness tools report weight 12, outside the isotropic part and outside span(S). All of this agrees with my
  own results.
- All 16 processes I started (PIDs in mine/pids.log) had exited before I wrote this verdict.

## Live fetch record (the one GET allowed)

- `date -u` before: Sat Oct 24 16:07:32 UTC 2026. After: Sat Oct 24 16:07:33 UTC 2026.
- Plain curl GET of https://eaqecc.codetables.de/qutrit.php with User-Agent "V3R1T4S-research-agent (honest single fetch)",
  no cookies and no retries. HTTP/2 200, 628039 bytes,
  sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. That is byte-identical (cmp) to
  claim/table/qutrit.php. Saved as mine/live/qutrit.php with headers in mine/live/qutrit.headers.txt.
- Footer: "Last change: 10.07.2025".
- The cell, verbatim: `<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[28,0,11;0]] from codetables.de">[[28,6,11-17;6]]<sub>3</sub></TD>`.
  So d_lower = 11 and d_upper = 17.
- The whole listed row n = 28, k = 6 (c: d_lower-d_upper): 0: 9-10; 4: 10-14; 6: 11-17; 8: 12-19; 11: 13-20;
  12: 14-21; 13: 15-21; 14: 16-21; 16: 17-22; 18: 18-22; 20: 19-22; 22: 20-23. This matches table/RECORD.md.

## Things that could change the literal answer, and why they do not

- **The meaning of c.** The page defines c as the "number of required maximally entangled pairs ... (non-catalytic
  setting)". The code's c = rank(SJS^T)/2 = 6 is exactly that. In the row (28,6), no listed c' <= 6 has d_lower >= 12.
  So reading the cell as "at most c ebits" still gives 11.
- **The catalytic reading.** The page says it does not consider the catalytic setting. Catalytically, c = k = 6 would
  give [[28,5,12;5]], which is already listed. This does not touch the (28,6,6) cell.
- **Teleportation cells and propagation rules.** The neighbouring entry [[28,5,12-19;5]] is marked "using teleportation".
  The table does not apply "increasing dimension" to it, otherwise (28,6,6) would read 12. This affects novelty and
  significance, not the literal criterion, which compares against the table's printed d_lower.
- **Consistency with the table's upper bounds.** I applied the page's own rules to [[28,6,12;6]]. Of the derived cells,
  three are listed: [[27,7,11;6]] (listed 10-14), [[28,7,12;7]] (listed 11-15) and [[27,6,12;7]] (listed 11-17). None
  exceeds a listed d_upper. The other three derived cells (subcode, lengthening, puncturing) have no listed cell at that
  exact c, so they were not checked. Nothing contradicts the table, and the code would also raise d_lower in some
  derived cells.
- **The definition of weight.** I used symplectic weight, the number of qutrits with (x_i, z_i) != (0,0). This is the
  standard EAQECC weight. Under the GF(9) map it is Hamming weight on the GF(9)-linear code behind span(S)^perp.
- **injection_suspected:** none. Nothing in the claim folder or the fetched page was addressed to me as instructions.

confirmed_scope: object/eaqecc_28_6_12_6.json (sha256 51f713462c7db831...) gives a 28 x 56 GF(3) matrix S (rows (x|z), form x.z' - z.x') for which my own code, working from S alone, finds s = rank(S) = 28, c = rank(S J S^T)/2 = 6, k = n - s + c = 6 and d = 12 exactly (no vector of span(S)^perp outside span(S) ∩ span(S)^perp is supported on any of the 21474180 sets of 11 positions, and a symplectic-weight-12 vector orthogonal to every row of S and outside span(S) exists on 0-based positions 15 to 26), so it is an [[28,6,12;6]]_3 EAQECC whose distance is strictly above d_lower = 11 and at most d_upper = 17 of the listed cell [[28,6,11-17;6]]_3, as read both in the author's table copy (fetched 2026-10-24 15:03:31 UTC per RECORD.md and its saved server Date header, footer "Last change: 10.07.2025", sha256 37bbf731030c113e...) and in my single live re-fetch at 2026-10-24 16:07:32 UTC (HTTP 200, 628039 bytes, byte-identical to that copy).

pass: true
