# Criterion skeptic report: qutrit-16-4-8-4
context: Claude Code subagent, fresh context

Target: eaqecc-qutrit-codetables-gaps. Cell compared: [[16,4,7-9;4]]_3 in the qutrit table. Object: object/eaqecc_16_4_8_4.json.
File hashes were checked with shasum -a 256 -c: all listed files OK; the object's sha256 is the one in INDEX.csv and SHA256SUMS.

## Method
I wrote my own checker (exact GF(3) linear algebra, no use of the author's code) and ran it on object/eaqecc_16_4_8_4.json. It computes: rank s of S; the commutation matrix S J S^T and its rank; c = rank/2; k = n - s + c; a basis B of the symplectic dual of span(S) (null space of S J); the radical of the dual (the isotropic part span(S) meets span(S)^perp, found as the vectors a.B with a (B J B^T) = 0); and then the minimum symplectic weight over all 3^m nonzero dual vectors outside that radical by full enumeration (3^m vectors, m = 2n - s = 16, so 43046721 vectors).
Output (verbatim): rows 16 (all independent, rank s = 16); rank(S J S^T) = 8; c = 4; k = 4; dual dimension 16; radical dimension = s - 2c as expected; d (dual minus isotropic part) = 8. Isotropic part has minimum weight 8 as well (information only).

## Clause by clause
- Explicit EAQECC [[n,k,d;c]]_3 with c >= 1: met. c = 4.
- Generator matrix in an allowed form: met. S is a 16 x 32 matrix over GF(3), entries 0, 1, 2 only, columns x_1..x_n then z_1..z_n (the symplectic form with 2n columns). Checked that every entry is in {0,1,2}.
- s independent generators, c = rank(S J S^T)/2, k = n - s + c: met (s = 16, c = 4, k = 4; all match the claimed n, k, c).
- d computed as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp, computed exactly: met. My enumeration gives d = 8; the claimed d is 8.
- Cell is in the live qutrit table, re-fetched live immediately before claiming: met on the saved record. the-record-we-beat/README.md records a fetch at 2026-10-18T13:53:54Z (sha256 37bbf731...936c, 628039 bytes). I fetched https://eaqecc.codetables.de/qutrit.php once myself at 2026-10-18T14:24Z (HTTP 200, 628039 bytes, sha256 identical to that record), so the page was unchanged. The cell in the page reads: [[16,4,7-9;4]]_3, title "increasing dimension of [[16,0,7;0]] from codetables.de". Page as fetched: d_lower = 7, d_upper = 9.
- d STRICTLY greater than d_lower: met. 8 > 7.
- d <= d_upper: met. 8 <= 9.
- c = 0 excluded: met (c = 4).
- Comparison set: the criterion names only the table's d_lower for this (n,k,c); that is the one compared. Not decided from the folder: whether other literature (outside the table) already has a better code; that belongs to the novelty skeptic.
Note on the table cell: its stated origin is 'increasing dimension of [[16,0,7;0]] from codetables.de'; nothing in the cell suggests d_lower is stale.


confirmed_scope: The 0/1/2 matrix in object/eaqecc_16_4_8_4.json is a 16 x 32 generator matrix over GF(3) defining an entanglement-assisted qutrit code with n = 16, k = 4, c = 4 and exact minimum distance d = 8 (computed here by full enumeration of the symplectic dual outside the isotropic part), which is strictly above the live qutrit table's d_lower = 7 and not above d_upper = 9 for the cell [[16,4,7-9;4]]_3, as that page read on 2026-10-18.

pass: true
