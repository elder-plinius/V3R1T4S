# Criterion skeptic report: qutrit-33-3-23-24
context: Claude Code subagent, fresh context

Target: eaqecc-qutrit-codetables-gaps. Cell compared: [[33,3,22-30;24]]_3 in the qutrit table. Object: object/eaqecc_33_3_23_24.json.
Package folder hashes were checked against the contributor's hash list (run from inside the package folder): all listed files OK.

## Method
I wrote my own checker (exact GF(3) linear algebra, no use of the author's code) and ran it on object/eaqecc_33_3_23_24.json. Its output is quoted below. It computes: rank s of S; the commutation matrix S J S^T and its rank; c = rank/2; k = n - s + c; a basis B of the symplectic dual of span(S) (null space of S J); the radical of the dual (the isotropic part span(S) meets span(S)^perp, found as the vectors a.B with a (B J B^T) = 0); and then the minimum symplectic weight over all 3^m nonzero dual vectors outside that radical by full enumeration (3^m vectors, m = 2n - s = 12, so 531441 vectors).
Output (verbatim): rows 54 (all independent, rank s = 54); rank(S J S^T) = 48; c = 24; k = 3; dual dimension 12; radical dimension = s - 2c as expected; d (dual minus isotropic part) = 23. 

## Clause by clause
- Explicit EAQECC [[n,k,d;c]]_3 with c >= 1: met. c = 24.
- Generator matrix in an allowed form: met. S is a 54 x 66 matrix over GF(3), entries 0, 1, 2 only, columns x_1..x_n then z_1..z_n (the symplectic form with 2n columns). Checked that every entry is in {0,1,2}.
- s independent generators, c = rank(S J S^T)/2, k = n - s + c: met (s = 54, c = 24, k = 3; all match the claimed n, k, c).
- d computed as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp, computed exactly: met. My enumeration gives d = 23; the claimed d is 23.
- Cell is in the live qutrit table, re-fetched live immediately before claiming: met on the saved record. the-record-we-beat/ shows a fetch at 2026-10-18T13:53:54Z (sha256 37bbf731...936c, 628039 bytes). I fetched https://eaqecc.codetables.de/qutrit.php once myself at 2026-10-18T14:24Z (HTTP 200, 628039 bytes, sha256 identical to the claim record), so the page was unchanged. The cell in the page reads: [[33,3,22-30;24]]_3, title "subcode of [[33,5,22;24]] quantum shortening of [[34,4,23;24]] from arXiv:2207.05647". Page as fetched: d_lower = 22, d_upper = 30.
- d STRICTLY greater than d_lower: met. 23 > 22.
- d <= d_upper: met. 23 <= 30.
- c = 0 excluded: met (c = 24).
- Comparison set: the criterion names only the table's d_lower for this (n,k,c); that is the one compared. Not decided from the folder: whether other literature (outside the table) already has a better code; that belongs to the novelty skeptic.
Note on the table cell: its stated origin is a subcode of [[33,5,22;24]], a quantum shortening of [[34,4,23;24]], from arXiv:2207.05647. Gain over the table is exactly one. The isotropic part has minimum weight 25 (information only), so d = 23 comes from the non-isotropic dual vectors.


confirmed_scope: The 0/1/2 matrix in object/eaqecc_33_3_23_24.json is a 54 x 66 generator matrix over GF(3) defining an entanglement-assisted qutrit code with n = 33, k = 3, c = 24 and exact minimum distance d = 23 (computed here by full enumeration of the symplectic dual outside the isotropic part), which is strictly above the live qutrit table's d_lower = 22 and not above d_upper = 30 for the cell [[33,3,22-30;24]]_3, as that page read on 2026-10-18.

pass: true
