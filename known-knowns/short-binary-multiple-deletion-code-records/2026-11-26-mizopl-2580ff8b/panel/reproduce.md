context: cold-reproduction-2026-11-26
Independent cold verification passed on all three primary record codes and all four companion codes:
- Exact s-deletion ball disjointness (D_s hash map) + full pairwise DP LCS(x,y) < n - s.
- Exact sorted-list SHA-256 verification and full SHA256SUMS manifest check.
- Negative control (--corrupt, 1-bit collision injection) rejected with exit code 1.
- Standalone Lean 4.36.0 kernel audit: `lake build DeletionCode` (216/216 jobs), `lake env lean AuditAxioms.lean` (13/13 theorems strictly subset of [propext, Classical.choice, Quot.sound], 0 sorryAx, 0 native_decide), and `lake env leanchecker DeletionCode` (exit 0).
pass: true
