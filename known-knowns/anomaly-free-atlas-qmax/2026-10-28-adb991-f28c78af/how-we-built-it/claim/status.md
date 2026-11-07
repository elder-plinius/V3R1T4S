# Status source record

status_source: B. C. Allanach, J. Davighi, S. Melville, "An anomaly-free atlas: charting the space of
flavour-dependent gauged U(1) extensions of the Standard Model", arXiv:1812.04602 (v5), JHEP 02 (2019) 082,
erratum JHEP 08 (2019) 064. arXiv record: https://arxiv.org/abs/1812.04602

- arXiv record, fetched by this run's scout: https://export.arxiv.org/abs/1812.04602, 2026-10-28T08:21:07Z, HTTP 200,
  sha256 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93 (source/atlas/arxiv_1812.04602_abs.html);
  versions v1..v5 (no v6).
- The v5 PDF and the JHEP erratum PDF were supplied by the workspace owner on 2026-10-23 (the container could not
  reach arXiv PDFs or Springer then); their text extractions (pdftotext -layout) are in source/atlas/ with the PDFs'
  sha256 in source/atlas/SHA256SUMS.
- The paper states the atlas is "for Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR" (line 784) (source/atlas/arXiv-1812.04602v5.txt),
  i.e. the largest published Q_max is 10 for both contents.
- source/atlas/table_comparison.txt: all 40 published values (Tables 2 and 3: solutions and symmetric solutions, SM
  and SMnuR, Q_max 1..10) equal this workspace's counts in the convention of CLAIM.md.
