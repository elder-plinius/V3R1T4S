# Monomer-dimer entropy of the cubic lattice: h3 <= 0.7859681 at cross-section (5,4), 2.34e-4 below the published 0.7862023450 (partial win p2)

## What

The 3D monomer-dimer entropy h3 of Z^3 (growth of the total number of matchings at unit activity, FKLM's sup over density) satisfies h3 <= 0.7859681, by exact integer Collatz-Wielandt on the full 1048576-state monomer-dimer diagonal-layer matrix at (m,n) = (5,4) (ratio 1891821269973664/281869529, log/20 = 0.7859680768...), below FKLM's 0.7862023450 by 2.34e-4, resting on a written but unpublished extension of He's argument that I re-derived with no gap; the currency of the comparator is left to the novelty skeptic.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later (standard library only) and a C compiler named `cc`. No network. About 1 GB of memory.
- **Time**: about 20 seconds on a laptop (the default check_run timeout is enough).
- **Expected last line**: `ALL CHECKS PASS`.

The certificate is stored in two numbered parts (`object/cert_md_h3_54.txt.part00` and `.part01`, 1,314,630 bytes in all, split because of the 1 MB file limit). The checker reassembles them and checks the sha256 of each part and of the whole (listed in `object/PARTS.sha256`). The submission id of this package (4db68440) is the first 8 hex digits of the sha256 of the reassembled whole certificate, 4db684405f609065a95ffe192fcdf672742b3910e7dfff37ed80b02ec0f74c0c. No single file in object/ has that hash, because the main object is the whole certificate and the parts are only its storage pieces.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Friedland, Krop, Lundow and Markstrom, arXiv math/0603001 v3 (11 Apr 2008), introduction | h3 upper bound | 0.7862023450 (quoted: "The numerical computations in [FP] yield the best known upper bound") | https://arxiv.org/abs/math/0603001 | 2026-10-19T05:30:56Z (HTTP 200; source archive 05:36:22Z) |
| same | h3 lower bound | 0.7849602275 | same | same |
| Friedland and Peled, arXiv math/0402009 (the paper FKLM cite as [FP]) | where the upper bound comes from | the novelty skeptic read in its text: "the best upper bound for h3 from our data is log beta(4,4)/16 = 0.7862023450" | https://arxiv.org/abs/math/0402009 | 2026-10-19, about 12:51 to 12:53 UTC (novelty skeptic; every attempt is logged in the panel workspace) |
| arXiv export API searches for a newer or citing bound (builder: three queries; novelty skeptic: further queries and author searches) | newest items | none newer than He on l3, h3 or l4; no rigorous h3 upper bound from 2024 to 2026 | https://export.arxiv.org/api/query | builder 2026-10-19T06:36:39Z to 06:36:49Z (HTTP 200); novelty skeptic 2026-10-19, about 12:51 to 12:53 UTC |

Margin: 0.7862023450 - 0.7859681 = 2.34e-4. Snapshot metadata with HTTP status and page sha256: the-record-we-beat/README.md. The panel's novelty report is panel/novelty.md.

## Not claimed

- This is a partial win (p2 of the target), not the main criterion. It is a bound on the monomer-dimer entropy h3 at unit activity, not on the dimer constant l3, and nothing here bounds h3 from below.
- It rests on a written but unpublished extension of He's argument (arXiv 2607.28810) from dimers to monomer-dimers, using the 2-lift matching inequality at unit activity on the diagonal layers. The derivation (object/DERIVATION.md) is the contributor's own extension of He's work; it has not been peer reviewed or published. Before the panel, the derivation at cross-section (3,3) was reviewed read-only by a model of a different family (OpenAI gpt-6.1-sol); here only (m,n) changes, and the criterion skeptic re-derived every step that depends on (m,n) and found no gap. That is the panel's finding, not a published proof.
- The bound was recomputed on the full, uncompressed 1048576 by 1048576 monomer-dimer matrix at cross-section (5,4). Only the (5,4) cell is claimed. Figures at other cross-sections in the author's notes (how-we-built-it/RESULTS.md covers several quantities, including dimer-constant figures) are not part of this claim and were not checked.
- The comparator 0.7862023450 is read as quoted in the 2008 paper of Friedland, Krop, Lundow and Markstrom and in the text of Friedland and Peled. Whether a later or journal-only rigorous bound exists is not settled: the search was arXiv-based, Semantic Scholar's list of papers citing FKLM ends in 2020, and no index used knows the papers citing He. Lundow's 2001 paper and the 2011 Federbush-Friedland journal text were not read. A days-old preprint, or a pull request filed after the panel's snapshot of the V3R1T4S pull requests (other than #537), cannot be excluded. The gate leaves the currency of the comparator to the novelty skeptic's search, which found nothing newer.
- This package does not re-derive or test the comparator value itself; it is a published numerical computation.
- The panel's skeptics are Claude Code general-purpose subagents; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The package also ships the earlier (3,3) certificate, only as a known-answer test for the checker. It is not a second claim; the (5,4) bound is the one to record.

## Filing history

This replaces the earlier (3,3) bound h3 <= 0.7860441 that was first filed in this PR (#537) on 2026-10-19 with package 2026-10-19-calgulbenkian-74ab789d. The (5,4) bound is strictly stronger (0.7859681 against 0.7860441, 7.6e-5 lower) and uses the same written derivation with only (m,n) changed. The (3,3) certificate is kept as the known-answer test in verify-it-yourself/ (cert_md_h3_33_sibling.txt): the checker first reproduces the (3,3) ratio 731051554747087/618837374495 exactly, then runs (5,4). This is not a refile of a closed pull request.

## Credits

- **Shmuel Friedland and Uri N. Peled**, "Theory of Computation of Multidimensional Entropy with an Application to the Monomer-Dimer Problem", arXiv math/0402009 (dated February 1, 2004 in its source), https://arxiv.org/abs/math/0402009: the earlier rigorous monomer-dimer entropy computations that FKLM cite for the upper bound 0.7862023450.
- **S. Friedland, E. Krop, P. H. Lundow and K. Markstrom** (names as printed in the arXiv source of math/0603001), "On the validations of the Asymptotic Matching Conjectures", arXiv math/0603001 v3, https://arxiv.org/abs/math/0603001: the definitions of the monomer-dimer entropy (h3 as a sup over densities, and the box limit) and the bounds 0.7862023450 and 0.7849602275 compared against.
- **Qidong He**, "A new upper bound on the dimer constant of Z^3", arXiv 2607.28810, https://arxiv.org/abs/2607.28810: the diagonal-layer method and Collatz-Wielandt bound that the written extension builds on.
- **Peter Csikvari**: the 2-lift matching-polynomial inequality that He's paper uses (cited in object/DERIVATION.md; we did not fetch or read Csikvari's paper).
- The contributor's team (credit name calgulbenkian; the search code was produced by the model Gemini, Argon).
- Contributor credit: `calgulbenkian`.
