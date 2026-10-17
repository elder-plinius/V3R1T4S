Package copy of the run's PREREG.md (original sha256 3e75298163970a43d18b67693608c288de2b4e51a7fdfa6e8d6408efa92f6d7f, unchanged in the run folder). Only change: the bank's URL template placeholders are written as n=N&k=K so the package checker does not read them as unfilled placeholders.

# PREREG (frozen 2026-10-16T17:25:38Z, before any LP for n > 100 was run)

frozen_at: 2026-10-16T17:25:38Z

## Criterion (verbatim, from target.md)

Success means, for some qubit cell (n,k) with 101 <= n <= 256, a proof that no [[n,k,d]] stabilizer code exists for d equal to the live table upper bound (https://codetables.de/QECC.php?q=4&n=N&k=K, re-fetched live immediately before claiming), thereby lowering it by at least 1 (direction: min upper bound), where the proof is an exact rational infeasibility certificate (Farkas dual) of the quantum weight-enumerator LP (stabilizer and normalizer enumerators linked by the quaternary MacWilliams identity, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, plus shadow-enumerator nonnegativity where used), checked in exact integer arithmetic by an independent script; and the new bound is NOT already implied by applying the standard propagation rules (d(n,k) <= d(n,k-1) for k >= 2, d(n,k) <= d(n+1,k), d(n,k) <= d(n-1,k+1)+1 or as stated by the table) to other live cells.

## Statistic / checker that judges a claim
- Object: a Farkas certificate (integers u_E0, u_E1, u_Q[j], v_G[j] >= 0, v_H[j] >= 0) in JSON for one cell (n,k,d).
- Checker: attempts/exact-solver/code/check_cert.py (standard library, integer arithmetic only; Krawtchouk by the
  explicit binomial sum). PASS = it prints VERIFIED and exits 0. The LP it encodes: A_0 = 1, sum A_i = 2^(n-k),
  B = 2^-(n-k) MacWilliams(A), A_j = B_j (1 <= j < d), A_j <= B_j (j >= d), A >= 0, and (variant "shadow")
  Rains shadow S_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0.
- Threshold: a cell (n,k), 101 <= n <= 256, k >= 1, counts only if (a) the certificate for d = D verifies, (b) D <= the live
  upper bound U(n,k) in the table snapshot data/qubit_table_full_n1-256.html AND in a fresh one-request re-fetch of
  https://codetables.de/QECC.php?q=4&n=N&k=K made immediately before claiming, (c) D <= C(n,k), the propagation
  closure of all OTHER live cells under R1 U(n,k)<=U(n,k-1) (k>=2), R2 U(n,k)<=U(n+1,k), R3 U(n,k)<=U(n-1,k+1)+1
  (attempts/settled-check/code/propagate.py), so the new bound D-1 is not implied, and (d) for the literal reading,
  a second verified certificate at d = U(n,k) is shipped as well.
- Sanity gate (must hold or every claim is void): the LP must be feasible (no certificate) at d = live LOWER bound
  of every cell scanned (a known code exists there); any certificate at d <= lower bound means a bug.
- Validation (step 1, run before this prereg on 30 random cells with 20 <= n <= 100): reproduce table upper bounds
  (LP infeasible at upper+1, feasible at upper and at lower).

## Cells and program variants (in this order)
1. Variant shadow, k = 1, every n = 101..256: test d = C(n,1); if infeasible, descend d -> d-1 until feasible or
   d = lower+1 (the LP bound = largest feasible d).
2. Variant shadow, spot cells (n,k) in {(200,20),(256,60)} and the grid n in {110,128,150,180,200,230,256} x
   k in {2,3,5,10,20,40,60} (k < n), same descend rule.
3. If 1-2 show improvements: systematic scan of n = 101..256, all k >= 1 with C(n,k) > lower bound, d = C(n,k),
   in order of increasing k, as time allows (capped search; covered cells listed exactly).
4. Variant no-shadow on every claimed cell, to state which constraints the certificate needs.
Claims: at most a few cells go to the panel (one claim per cell); all other verified cells are listed in the
dossier as PROMISING (single-context, unpanelled).

null_test: not needed because each claim is an explicit certificate checked by a deterministic exact checker against a table value; the independent exact verification and the propagation check play that role (human's instruction).
