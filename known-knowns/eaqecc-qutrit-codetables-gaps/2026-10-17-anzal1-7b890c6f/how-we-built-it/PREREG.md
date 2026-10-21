# Pre-registration (`PREREG.md`)

- Frozen (UTC): `2026-10-17T05:01:00Z`
- Target ID: `eaqecc-qutrit-codetables-gaps`
null_test: not needed because a claim is an explicit algebraic generator matrix S over GF(3) whose parameters [[n, k, d; c]]_3 (rank s, commutation rank 2c = rank(S J S^T), logical dimension k = n - s + c, and exact minimum symplectic weight d over span(S)^perp \ (span(S) ∩ span(S)^perp)) are verified deterministically in exact finite-field arithmetic against the live table https://eaqecc.codetables.de/qutrit.php.

## Verbatim success criterion
Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Exact checker and acceptance thresholds
- **Checker:** `python3 check_eaqecc.py <candidate.json>` (exact `GF(3)` Gaussian elimination for `rank(S) == s`, `rank(S J S^T) == 2c`, `k = n - s + c`, and exhaustive enumeration of all `3^(2n-s) - 3^(s-2c)` vectors in `span(S)^perp \ (span(S) ∩ span(S)^perp)` to compute exact minimum symplectic weight `d`).
- **Threshold:** `c >= 1`, `k >= 1`, `rank(S) == s`, `d > d_lower(n, k, c)` (strict inequality), and `d <= d_upper(n, k, c)` on `https://eaqecc.codetables.de/qutrit.php` re-fetched live before claiming.
