# Potts antiferromagnet colouring entropy: W_sq(5) <= 3.25040520587854968506 (cycle C_14)

## What

Provided the shipped vector satisfies y = C v (reproduce) and the literature search finds nothing as good (novelty), inequality (6) of Lundow and Markstrom with the even circumference 14 (k=7) and the proper 5-colouring cycle transfer matrix gives W_sq(5) <= 3.25040520587854968506, which is smaller than their printed upper bound 3.250407145038276 by about 1.939159726e-6, more than 1e-9.

Notes on that sentence, which is the panel's gate text word for word:
- Citation. The inequality is equation (6) of Lundow and Markstrom (2008), Section 4. The claim folder called it "Theorem 2.2"; that label was
  wrong (the paper has no Theorem 2.2), and this package cites equation (6) throughout. The label is corrected in this README, in RUN_IT_YOURSELF.md
  and in object/BOUND.md. It still appears in the files that are copied unchanged: the panel reports (where the panel notes the error), and the
  snapshot text in how-we-built-it/.
- Rounding. The bound rounded upward at 20 decimals is 3.25040520587854968506. The sentence above and the upward value are the same number.
- Object. The certificate is a pair of vectors (v, y) on the 81433 symmetry orbits (colour permutations and the dihedral group of the cycle) of the
  proper 5-colourings of the cycle C_14; the full transfer matrix has 268435460 states. It is stored as 6 parts under 1 MB
  (object/PARTS.txt gives the sha256 of every part and of the whole 5211716-byte file q5_cyl_14_cert.bin, d225ef1cf4f8f3c335620d5c7e37c5d96afa60cdc47b228acce51b66065a91e1).
- What the panel did that the quick check below does not. The panel's reproduce skeptic recomputed y = C v on the FULL transfer matrix
  (no quotient, no equitable-partition assumption) with its own C program, and matched the shipped y in all 81433 orbits (0 mismatches). That program
  is shipped as an optional second check (verify-it-yourself/full-check/).

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

- Requirements: python3 3.8 or later, standard library only (no numpy).
- Rough laptop time: about 15 seconds.
- Expected last line: `ALL CHECKS PASS`
- Optional second check (the panel reproduce skeptic's independent C checker, about 25 minutes on 28 threads): verify-it-yourself/full-check/FULL_CHECK.md.

The quick check reassembles the parts and checks every sha256 first, then reads the vectors, checks v > 0 and computes the largest ratio
y_i / v_i as an exact integer fraction, the bound C_hi^(1/14) in 80-digit decimals, and, in exact integers, that the stated 20-decimal value
is a valid upper bound and is its upward rounding. It also validates the file format and the orbit numbering on three small certificates,
compares independent small-width eigenvalues with a table, and rejects two corrupted copies. It trusts that y = C v at the claimed width.
That is the gap the optional full check and the panel's reproduce run close.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Lundow and Markstrom (2008), equation (8) | W_sq(5) upper bound | 3.250407145038276 (printed) | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DF3F31D5871C39FDAD818685EDA617B3/S1461157000000498a.pdf/exact-and-approximate-compression-of-transfer-matrices-for-graph-homomorphisms.pdf | 2026-10-18T18:23:42Z |
| same paper, Table 3 | C_12 (largest eigenvalue for the cycle of that length) | 1390763.1270219; its 1/12 power is 3.2504071450382709400, the printed bound | same URL | 2026-10-18T18:23:42Z and 2026-10-18T18:25:57Z |
| Cambridge Core article page | status page for the same paper | no later bound | https://www.cambridge.org/core/journals/lms-journal-of-computation-and-mathematics/article/exact-and-approximate-compression-of-transfer-matrices-for-graph-homomorphisms/DF3F31D5871C39FDAD818685EDA617B3 | 2026-10-18T18:23:02Z |
| V3R1T4S TROPHY_CASE.md, pull requests, known-knowns | this target | none | https://github.com/elder-plinius/V3R1T4S | 2026-10-18T18:23:03Z to 18:23:12Z |
| This package | W_sq(5) upper bound | **3.25040520587854968506** (1.939159726e-6 below the printed bound; the criterion asks for at least 1e-9) | object/q5_cyl_14_cert.bin (in parts) | |

The table is the paper itself; there is no live table for this target. Details, with HTTP status and sha256, are in the-record-we-beat/README.md,
and the panel's novelty report (panel/novelty.md) lists the arXiv queries and what they found. The paper's own tables stop at C_12 (q = 4: C_16,
q = 5: C_12); this cycle is the next even width, so the novelty is the new width, not a new idea.

## Not claimed

- Only this one cell: the upper bound on W_sq(5). Nothing is claimed here for the other colour count, for any lower bound, or for the cubic-lattice
  bounds. (Argon's snapshot also lists improved lower bounds; they are not part of this package and were not panelled.)
- The inequality W_sq(q) <= theta(C_m)^(1/m) for even m is the published equation (6); the paper does not prove it and cites its reference [7]. We did
  not re-derive it. The compression step uses their Theorem 3.1 and Corollary 3.3, and the full check does not depend on it.
- The snapshot's RESULTS.md has one wrong table entry (q = 4, open strip m = 3, a value 16.352349955308334315 where the true value is 16.34846922834953...), as the claim folder
  records. The claim does not depend on it: this package uses only the cycle C_14. The claim folder also called the inequality "Theorem 2.2": wrong label, equation (6) is
  right. The shipped small-width table THETA_TABLE omits that row.
- Google Scholar was not queried (no browser); the literature search was four arXiv API queries and two web searches. A bound in a source those do not index cannot be excluded.
- Not peer reviewed. Checked by a three-skeptic panel (panel/) and by the checkers shipped here. Nothing is said about the exact value of W_sq(5) beyond the bound.
- The object cannot be regenerated byte for byte from the information in the snapshot (how-we-built-it/README.md says why); the bound holds for the shipped file.
- The panel's first criterion run (panel/criterion_run1.md) failed only because the paper was not readable at that time (abstract only); it is kept for the record.
  The second run read the paper and passed.

## Filing history

None. This is a new claim, not a refile of an earlier pull request.

## Credits

- **Per Hakan Lundow and Klas Markstrom**, "Exact and approximate compression of transfer matrices for graph homomorphisms", LMS J. Comput. Math. 11 (2008) 1-14,
  https://www.cambridge.org/core/journals/lms-journal-of-computation-and-mathematics/article/exact-and-approximate-compression-of-transfer-matrices-for-graph-homomorphisms/DF3F31D5871C39FDAD818685EDA617B3 :
  the published bounds this package improves, the method (transfer matrices of cycles and the inequality of equation (6)), and the equitable-partition compression
  (their Theorem 3.1 and Corollary 3.3) that the certificate uses. This package only runs their method one even width further.
- **The panel's reproduce skeptic** (a Claude Code subagent) wrote the independent C checker and the analysis script in verify-it-yourself/full-check/ (mycw.c and analyse.py).
  Please credit it as the panel's own checker.
- **Argon** (an AI search agent, Gemini, working for the contributor) wrote the search code in how-we-built-it/ and produced the certificate.
  The orbit-check, certificate-parsing and small-width scripts in verify-it-yourself/ were written from the definition by the claim folder's builder.
- Contributor credit: `calgulbenkian`.
