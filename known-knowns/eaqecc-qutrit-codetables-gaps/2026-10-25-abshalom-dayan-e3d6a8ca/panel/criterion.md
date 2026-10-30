# Criterion skeptic verdict: [[35,7,16;14]]_3 (target eaqecc-qutrit-codetables-gaps)

Bottom line: PASS. The claim meets the full success criterion literally. I recomputed every parameter from S with my own exact code. I proved d = 16 exactly with my own exhaustive Brouwer-Zimmermann search, which I validated against brute force. My own live re-fetch of the table, byte-identical to the author's copy, still lists the cell (35,7,14) as 15-26. So 15 < 16 <= 26. The page's own propagation rules, applied to its listed codes, give only 15 for this cell, so the result is not subsumed. It is not a partial win (p1/p2); it is the main criterion.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Clause by clause

| Clause | What I checked (my own code unless noted) | Found |
|---|---|---|
| Explicit generator matrix over GF(3), 2n columns | claim/object/eaqecc_35_7_16_14.json, field S; mine/params.py asserts the shape and the entries | S is 42 x 70, all entries in {0,1,2}, n = 35. Object sha256 e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4 matches CLAIM.md |
| s independent generators | GF(3) rank of S (mine/params.py) | rank 42 = number of rows, so s = 42 |
| c = rank(S J S^T)/2, c >= 1 | Commutation matrix with J = [[0,I],[-I,0]], i.e. x.z' - z.x' | rank 28, c = 14 (c >= 1; c = 0 trap absent) |
| k = n - s + c | arithmetic | 35 - 42 + 14 = 7 (matches claimed (n,k,c) = (35,7,14)) |
| d = min weight on span(S)^perp minus the isotropic part | My code computes N = span(S)^perp from S (dim 28) and I = span(S) ∩ N (dim 14 = s - 2c). It checks exactly that N is closed under the GF(3)-linear map (a,b) -> (b, a+b), which is multiplication by w in GF(9) = GF(3)[w]/(w^2-w-1). From that it builds its own GF(9) basis (K = 14) whose image is all of N (rank 28). Symplectic weight on N is then Hamming weight over GF(9). mine/bz9.c is my own Brouwer-Zimmermann search: 2 disjoint full-rank information sets (columns 0-13 and 14-27), every codeword with weight <= 7 on either set enumerated exhaustively. It ran 2,013,634,508 projective codewords, exactly 2 x sum_{i=1..7} C(14,i) 8^(i-1) = 2 x 1,006,817,254, with no cap, sampling or early exit. Any codeword it did not enumerate has weight >= 2 x 8 = 16 | Minimum found 16, unseen bound 16, so the minimum over all of N minus {0} is exactly 16. Every vector of N minus I therefore has weight >= 16, and no isotropic vector was counted. Upper side: 20 weight-16 witnesses from my run, plus the author's witness support {1,10,11,13-21,23-26}, which I re-derived independently with mine/witness_mine.py. Each is orthogonal to all rows of S and NOT in span(S). So d = 16 exactly |
| Validation of my distance program | mine/test_bz9.py: 160 random GF(9) codes (K = 3-4, n = 7-14) against brute force over all messages, plus a check of every witness's membership. 30 further runs exercised both the "exact" branch (11) and the "bound only" branch (19) | 160/160 agree |
| Cell of the live table, re-fetched | One plain GET with curl, User-Agent "V3R1T4S-research-agent (honest single fetch)", no retries. Saved as fetched/qutrit.php; time before and after (date -u) 2026-10-25T03:52:24Z, HTTP 200, 628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c, footer "Last change: 10.07.2025". The file is byte-identical to the author's claim/table/qutrit.php (fetched 02:35:12Z) | The cell is listed: `[[35,7,15-26;14]]_3` (title "lengthening of [[27,7,15;14]] quantum shortening of [[28,6,16;14]] increasing dimension of [[28,5,16;13]] from arXiv:2207.05647"). (n,k,c) = (35,7,14) is the same as the code's computed parameters |
| d > d_lower and d <= d_upper | arithmetic | 16 > 15 and 16 <= 26 |
| Non-catalytic | The page says c counts required pairs in the non-catalytic setting. The code's c is rank(S J S^T)/2 with k = n - s + c. No catalytic reduction ([[n,k,d;c]] -> [[n,k-1,d;c-1]]) is used | Non-catalytic |

## Null model and subsumption checks

- **Page's own rules.** mine/closure.py propagates every listed non-teleportation lower bound through the page's six rules plus monotonicity in c. The rules are subcode, lengthening, puncturing, quantum shortening, increasing dimension and length reduction. Its value at (35,7,14) is 15, equal to the listed value, so no listed code gives d >= 16 here. My rule set is if anything too generous: it lifts 32 other listed cells, mostly k = 0, above their listed d_lower. None of those touches this cell.
- **Teleportation cells as sources.** Seeding the "using teleportation" cells (c = k) would give 27 at (35,7,14). The same seeding pushes 2700 listed cells above their own d_upper, for example (5,1,4) to 6 > 5. So those cells are not valid propagation sources. This reproduces the author's stated numbers.
- **Neighbouring cells.** The listed (35,7,15) is 16-26. The claim reaches d = 16 with one entangled pair fewer, which strictly improves the c = 14 cell. Only (35,7,14) is claimed.
- **Not checked.** Whether some paper outside the table already builds a [35,14,16]_9 code with Hermitian hull of dimension 7 (for example by varying the hull of the known Xing-Ling code). The criterion compares only against the live table, and I had no remit to search the literature.

## Author's commands run as cross-checks (not relied on)

- Step 3 witness tools: `weight=16 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False` and `symplectic_weight=16 ... in_span_S=False`, which agrees with my results.
- Not run: step 1 (rebuild/provenance, outside the criterion), step 2 (my own exhaustive method replaces it), and step 4 (excluded by the ground rules).
- My single heavy job (mine/bz9, niced and capped) ran 04:13:29Z to 04:13:37Z, 8.40 s real, peak memory footprint 1065272 bytes. It started only when the real-job count was 2 (mine/wait.log). No job of mine is still running.

confirmed_scope: The 42 x 70 GF(3) stabilizer matrix S in claim/object/eaqecc_35_7_16_14.json (sha256 e3d6a8ca...b73b4) has 42 independent rows and rank(S J S^T) = 28, so it defines a non-catalytic entanglement-assisted qutrit code with n = 35, c = 14, k = 7 whose minimum distance (minimum symplectic weight over span(S)^perp outside span(S) ∩ span(S)^perp) is exactly 16, which is strictly above d_lower = 15 and at most d_upper = 26 of the listed cell [[35,7,15-26;14]]_3 on https://eaqecc.codetables.de/qutrit.php as re-fetched 2026-10-25T03:52:24Z (HTTP 200, sha256 37bbf731...936c).

pass: true
