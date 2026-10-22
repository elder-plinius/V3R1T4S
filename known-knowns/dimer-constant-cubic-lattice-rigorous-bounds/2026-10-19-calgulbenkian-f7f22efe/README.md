# Four-dimensional dimer constant: l4 <= 0.5840147694 (0.584015 rounded up) against the cited table value 0.66278769 (partial win p3)

## What

A certified Z^4 dimer-constant bound l4 <= 0.5840147694 (0.584015 rounded up) from the four-dimensional diagonal-layer matrix at (3,3,2), against the cited Butera-Federbush-Pernici table value ln(8!)/16 = 0.66278769, resting on a written but unpublished extension of He's argument that I re-derived with no gap; whether a better published Z^4 upper bound exists is not settled by this report.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later, standard library only. No network.
- **Time**: about 6 minutes (about 5 minutes alone and 11 min 5 s on a loaded machine, as measured by the contributor; CW_QUICK=1 skips the all-sector iteration and takes about 40 seconds).
- **Expected last line**: `ALL CHECKS PASS`.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Butera, Federbush and Pernici, arXiv 1305.7028 (Phys. Rev. E 88, 032113), table of rigorous bounds (label tab3 in the source; the author calls it Table III) | lambda_4(1) upper bound | 0.66278769 = ln(8!)/16 (caption: (1/2) ln(2d) - 1/2 <= lambda_d(1) <= ln((2d)!)/4d) | https://arxiv.org/abs/1305.7028 | 2026-10-19T05:30:57Z (HTTP 200; source archive 05:39:44Z) |
| same | lambda_4(1) lower bound | 0.53972077 | same | same |
| arXiv 1502.06734 (virial coefficients and upper bounds on matchings), abstract page only | any Z^4 bound | not read beyond the abstract; whether it yields a Z^4 constant bound is not settled | https://arxiv.org/abs/1502.06734 | 2026-10-19T06:49:22Z (HTTP 200) |
| arXiv export API searches for a newer or citing bound (three queries) | newest items | none newer than He on l3, h3 or l4 | https://export.arxiv.org/api/query | 2026-10-19T06:36:39Z to 06:36:49Z (HTTP 200); the novelty skeptic repeated the search about 07:12 to 07:28Z |

Margin: 0.66278769 - 0.584015 = 0.0788. The bound is compared against the cited table value, not against a search of everything published on Z^4. Snapshot metadata with HTTP status and page sha256: the-record-we-beat/README.md. The panel's novelty report is panel/novelty.md.

## Not claimed

- ROUNDING NOTE. The author printed the bound as 0.5840147693. That figure is rounded down, so it is not an upper bound. The exact value of the Collatz-Wielandt ratio's logarithm divided by 36 is 0.584014769338, so the correct ten-decimal upper figure, rounded up, is 0.5840147694. The claim here is l4 <= 0.5840147694 (0.584015 rounded up to six places). The shipped object file, object/cert_4d_332.txt, is byte for byte the author's file, and its own header still shows the author's figure 0.5840147693; the headers and some of the earlier recorded output in verify-it-yourself/RECEIPTS.md also show it. The shipped checker prints the rounded-up figure. The six-decimal value 0.584015 is the same either way.
- This is a partial win (p3 of the target), not the main criterion. The comparator is the table value ln(8!)/16 = 0.66278769 cited by Butera, Federbush and Pernici. Whether a better published upper bound on the four-dimensional dimer constant exists is not settled by this package: the searches were arXiv-based, one possibly relevant paper (arXiv 1502.06734) was read only at abstract level, and journal-only results were not searched.
- It rests on a written but unpublished extension of He's argument from three to four dimensions (diagonal layers and the symmetry reduction by the group of order 36 at cross-section (3,3,2)). The extension is the contributor's own. The cross-family reviewer, the criterion skeptic and the reproduce skeptic checked the written derivation step by step and found no gap, but it has not been peer reviewed or published. The reproduce skeptic checked the certificate in sector 9 and the all-ones iteration in every sector; only (3,3,2) is claimed.
- The author's pre-registration quotes a four-dimensional lower bound 0.55808612 attributed to Schrijver and this table; the table of Butera, Federbush and Pernici lists 0.53972077. This package makes no claim about lower bounds.
- The cross-family reviewer saw the written derivations only, not the certificates. The three panel skeptics and the object's builder (Gemini, Argon) are different model families, but none of this is peer review.

## Credits

- **P. Butera, P. Federbush and M. Pernici**, arXiv 1305.7028 (Phys. Rev. E 88, 032113, 2013), https://arxiv.org/abs/1305.7028: the table of rigorous bounds whose upper bound 0.66278769 for lambda_4(1) is compared against. (The arXiv listing names Paolo Butera as submitter; the other first names were not seen in the sources we fetched.)
- **Qidong He**, arXiv 2607.28810, https://arxiv.org/abs/2607.28810: the diagonal-layer method (Theorem 2.1, Corollary 3.4) that the four-dimensional extension builds on.
- **Csikvari**, as cited by He: the inequality that links the layer matrix to the dimer constant. We did not read Csikvari's paper itself.
- The contributor's team (credit name calgulbenkian; the search code was produced by the model Gemini, Argon).
- Contributor credit: `calgulbenkian`.
