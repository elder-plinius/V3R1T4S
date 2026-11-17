# Novelty skeptic: odd-graceful-trees-beyond-12

context: subagent (parent Task)

Worked from a scratch copy of the original claim workspace ([scratch]). I did not read REPORT, NOTES, attempts, LOG or any other panel file.

## Status source (one GET each, User-Agent "V3R1T4S-research-agent", no retries)
| URL | time (UTC) | HTTP | value read |
|---|---|---|---|
| https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 | 2026-11-01T03:00:08Z | 200 | "This Version DS6: Oct 30, 2025" (still the current edition; the page also shows a 2026-01-27 date) |
| https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/ (linked from that page) | 2026-11-01T03:00:15Z | 200 | sha256 b1b5d8ba...842e, the same as the claimant's the DS6 PDF snapshot (not shipped) |

DS6, Section 3.6 (Odd-Graceful Labelings), p. 86: "She conjectures that all trees are odd-graceful and proves the
conjecture for all trees with order up to 10. Barrientos [488] has extended this to trees of order up to 12."
No higher bound for all trees appears anywhere in the PDF. I grepped every "odd-graceful", "order up to" and "at most N vertices" passage; the other bounds it finds are for graceful, prime, super edge-magic and other labelings. The known result for all trees is therefore order 12 or less.

## Literature and code, last 24 months (web searches, 2026-11-01 UTC)
- No arXiv, Zenodo, GitHub or journal item extends the all-trees odd-graceful verification past 12. The nearby 2026 items cover other labelings: edge-graceful and antimagic for all trees with at most 31 vertices (Zenodo 10.5281/zenodo.23405211), and arXiv 2608.23881, which covers edge-graceful trees of odd order with at most two vertices of degree two.
- Barrientos's published odd-graceful results (arXiv 0807.3738: caterpillar forests and trees of diameter at most 5) cover classes of trees, not all trees of an order. Gnanajothi's order-10 result and the order-12 bound in a 2023 Utilitas paper are already covered above.
- Brinkmann et al. (DMTCS 2012) give only counts of trees with nonzero alpha-deficit. An alpha-labeling yields an odd-graceful labeling, but those counts give no certificate for the trees without one. So the bound of 22 is not a trivial consequence of published data.

## Repo (`[workspace]/repo`, origin elder-plinius/V3R1T4S, HEAD f3b19b4)
- TROPHY_CASE.md: no mention of graceful or odd-graceful.
- known-knowns/: no odd-graceful entry. The target is listed only in known-unknowns/ as open as of 2026-10-30, with bound 12.
- GitHub PRs and issues: searching "graceful" in repo:elder-plinius/V3R1T4S returns 0 PRs and 0 issues. The first page of all PRs (100, newest #875) has no odd-graceful title.

## Is the object new rather than a trivial edit?
It is new. It is a fresh certificate covering all A000055(n) trees for n = 2..22, not a modification of any published labeling list, because none exists past order 12. As a sanity check, I ran sha256sum -c and the bundled ogcheck on my scratch copy. It printed "PASS order n" for every n = 2..22, and the regenerated counts match A000055: 1301 trees for n = 13, 19320 for 16, 823065 for 20 and 5623756 for 22. Whether the result is correct is the other skeptics' job. This panel checks only whether it is new.

## Verdict
novelty: NEW. The claim moves the all-trees odd-graceful bound from 12 (DS6, Oct 30 2025, read 2026-11-01T03:00Z) to 22 and strictly beats everything known in DS6, the 24-month literature and code, and the repo.

pass: true
