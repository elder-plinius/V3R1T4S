# PREREG: eaqecc-qutrit-codetables-gaps, run 2026-10-17-1119

frozen at (date -u): 2026-10-17T17:30:23Z, before any attack output exists (no lens had started).

## Criterion (verbatim, bank/targets.json)

Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Statistic and checker

- The object is an explicit stabilizer generator matrix S over GF(3), s0 rows x 2n columns (X part, then Z part). If a lens builds the code over GF(9), it converts to S over GF(3). The GF(3) matrix S is the claimed object.
- From S, compute exactly:
  - s = rank(S);
  - c = rank(S J S^T)/2, with <u,v> = u_X.v_Z - u_Z.v_X mod 3;
  - k = n - s + c;
  - d = the minimum symplectic weight over span(S)^perp minus (span(S) & span(S)^perp).
- Checker of record: code/eacheck.py (exhaustive). It was tested at 2026-10-17T17:30:23Z on a known positive ([[5,1,3;0]]_3, PASS), on [[2,1,2;1]]_3 (PASS), and on a known negative (one entry of [[5,1,3]] changed: FAIL). Output: data/checker_tests_output.txt.
- When dim span(S)^perp = n+k-c exceeds 20, exhaustive enumeration in numpy is too slow. d must then come from two independent minimum-weight computations that agree exactly: one exhaustive enumeration, of the GF(9)-linear code when there is one, and one Brouwer-Zimmermann or information-set exhaustive method, each written separately. The REPRODUCE skeptic recomputes d with its own checker.

## Thresholds (all must hold)

1. c >= 1 and k >= 1. The criterion's definition of d is the empty set when k = 0, so k = 0 cells are not claimed.
2. d > d_lower(n,k,c), using data/qutrit_table.tsv (parsed from the 2026-10-17T17:24:09Z fetch, sha256 37bbf731...) AND a live re-fetch of https://eaqecc.codetables.de/qutrit.php right before the claim. Also d <= d_upper. A d above d_upper means a checker or table error: stop and audit, no claim.
3. The cell is not (14,3,5), (14,0,2), (13,0,3), (12,0,4) or (11,0,5). Those belong to open PR #331 or are implied by it.
4. The cell's value is not implied by any open or closed V3R1T4S pull request or public paper object, rechecked before the gate. Checked with code/propagate.py over the table's own rules.
5. One cell per claim. If several cells qualify, the panel carrier is the one with the largest d - d_lower. Ties go to the smallest n, then the smallest c, then the smallest k. All other qualifying cells go to a verified ledger in the dossier and are not claimed in this run.

## Partial wins

- p2 (fewer entangled pairs than any listed code with the same (n,k,d)) counts only if checked against the live table row literally.
- p1 (LP certificate lowering d_upper) is not targeted in this run.

## Null design

null_test: not needed because the claim is an explicit object (a generator matrix) checked by a deterministic exact checker against a table value; no search statistic or chance claim is made.
