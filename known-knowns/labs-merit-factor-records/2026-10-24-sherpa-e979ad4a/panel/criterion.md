# CRITERION skeptic: claim_v6, target labs-merit-factor-records, cell L = 401

context: subagent (fresh context, Claude Code Agent tool)

I read only the claim package and worked on a scratch copy outside it. Every number below is copied from my own
command output. File names are relative to the claim folder.

**Verdict.** The cell meets the full success criterion, read literally. Its energy, E = 10776, is strictly below the
named-source bar of 11888. It is also below the lowest published L = 401 value anywhere in the package, which is 11000
(ERK'2025, Figure 2). It is not a trivial derivation of any published sequence.

## 1. Length, explicit sequence, exact integer energy

- `sequence_L401.txt` holds 401 symbols over {0,1} ('1' = +1, '0' = -1). Energy does not change under negation, so the
  mapping cannot matter.
- I wrote my own integer checker before running the package's. Two independent methods (direct sums, and a polynomial
  product) both give `E = 10776` with `C0 = 401` and `max|C_k| = 27`, so `F = 160801/21552 = 7.461071`.
- 67 <= 401 <= 600 holds.
- The sequence is skew-symmetric, s[200+j] = (-1)^j s[200-j] (True). All odd-lag C_k are 0, as skew symmetry requires
  (True). E mod 8 = 0.
- To test my code: Barker 13 gives E = 6. As a null, 200 random length-401 sequences gave a minimum E of 61828 and a mean
  of 79044 (theory: 80200). The package's `check_labs.py` agrees with my result (PASS).

## 2. The named sources, one by one: what each lists at L = 401

I checked every archive's sha256 against `table_record.md`, and all match.

- **arXiv:2607.09688** (`bar/data/criterion_repair/arxiv_2607.09688v1_eprint.bin`). The TeX source has three tables.
  - `TAB_RECORDS` is a longtable with 35 rows: L = 450-452, 455-465, 475-484, 490, 491, 494-498, 516-518 and 573.
  - `TAB_TOPPAR` lists partitions for p = 81, q = 7.
  - `TAB_PARTITIONS` lists partitions for L = 461.

  No number from 400 to 449 appears in any of its .tex files. Its records figure also covers only 450..527 and 573. The
  abs page (`bar/data/eprints/arxiv_abs_2607.09688.html`) shows only [v1], dated 17 Jun 2026, and the API returns it as
  2607.09688v1. **It has no value at L = 401.**
- **arXiv:2504.00987** (`bar/data/criterion_repair/arxiv_2504.00987v2_eprint.bin`) has three tables.
  - `tab:labs_results` covers 16 lengths: even 92, 98, 104-120 in steps of 2, and odd 99, 107, 109, 113, 119.
  - `tab:fit` is a runtime fit for N_min^fit = 20..70.
  - `combinedTable` is an illustrative 5-element matrix.

  **It has no value at L = 401.**
- **"The Bošković et al. LABS records repository cited there."** Of the two named papers, only arXiv:2504.00987 cites a
  repository. Its bibliography entry `OPUS2-git_labs-Boskovic` reads "A GitHub Archive for Solvers and Solutions of the
  labs problem. For updates, see https://github.com/borkob/git_labs", dated January 2016. arXiv:2607.09688 cites no
  repository; its only records URL is the Bauke-Mertens open.dat.
  - The tree listing `bar/data/criterion_repair/borkob_tree_1aa1234.json` is for commit
    sha 1aa123407636e48630174e0bf122037e369c1d68, with truncated false and 146 entries.
  - Its result files are `results-2016/2004-Knauer-original.{txt,html}`, `results-2016/2016-labs-skew.txt` and
    `results-2018/2018-labs-skew.txt`. All four copies in `bar/data/borkob_git_labs/` match the tree's git blob sha1 and
    sizes (227908, 34446, 22419 and 22501 bytes).
  - Both skew tables contain the row `401 6.7632 11888 <sequence>`. I recomputed the witness and got E = 11888. It is
    the only row between 391 and 411.
  - The Knauer list has no 401 anywhere: the text file's largest length is 222, and the HTML table runs from 4 to 304
    (270 rows).

  **This source gives 11888.**
- **Any newer arXiv result** (`bar/data/criterion_repair/arxiv_api_newer_search.xml`).
  - The feed was updated 2026-10-24T19:23:25Z and reports totalResults 966.
  - Its 100 entries are in non-increasing submission-date order, from 2026-10-19 back to 2026-03-26T17:09:42Z. The window
    therefore covers everything since arXiv:2607.09688.
  - 66 entries are dated on or after 2026-06-17. Three of them are about LABS:
    - 2610.27329: complexity of LABS variants.
    - 2610.14361v2: time-to-solution scaling for N = 27..60.
    - 2609.05771: moments of crosscorrelation demerit factors.

  None of these abstracts reports an L = 401 value. **No newer arXiv result gives a value.**

**Minimum over the named sources at L = 401: 11888.**

## 3. Every other published L = 401 value in the package

- **Dimitrov, arXiv:2206.12070.** The row reads `$401$ & B_401^{27,13,9} & <hex, with a typeset space> & 7.0084 &
  7.01820006983` (columns: Old MF, New MF). I decoded it myself, stripping the leading zeros to get 401 bits:
  E = 11456, F = 7.01820006983, an exact match.
- **Brest and Bošković, arXiv:2011.00068v1.** In `tb_best.tex` ("length 301 up to 401") the row reads `401 & 7.0084 &
  <101 hex digits, with a typeset space>`. Dropping 3 leading pad bits gives E = 11472 and F = 7.0084. Dropping trailing
  pad bits instead gives 13388, which does not match. v2 (201..303) has no 401.
- **ERK'2025, Pšeničnik, Bošković and Brest** (`bar/data/erk2025/psenicnik_integer_partitions_erk2025.pdf`). The paper
  "improved the merit factor values for all fifty sequences in the interval 400 ≤ L ≤ 450". Its Table 3 prints only
  L = 405, 422, 433, 441 and 450. Its reference [6] is Dimitrov's arXiv:2206.12070.
  - **The figure.** Figure 2 is Form XObject Im2 on page 4. It holds 51 blue markers (legend "Dimitrov"), 51 red markers
    ("Our work") and 51 dashed segments.
  - **My calibration.**
    - x axis: I used the axes box (60.23..445.68) with matplotlib's 5% margins. L = 400 lands at x = 77.7505, and the
      largest |L - round(L)| is 1.4e-10.
    - y axis: I fitted the 51 blue markers against the 51 MFs Dimitrov prints in his TeX. The slope is 312.551216 pt per
      unit F, the same as the tick-label spacing (312.55121629350003), and the largest residual is 0.00000 pt.
    - Check: all five Table 3 rows read back to their printed "Our F" and "Previous F".
  - **The L = 401 reading.**
    - The blue marker reads 7.018200, which is Dimitrov's value.
    - The red marker reads 7.309100, which gives E = 11000.055.
    - The red values sit on 4-decimal numbers (largest deviation 2.16e-12). F = 7.3091 allows only integer energies in
      (10999.979, 11000.130], so E = 11000.
    - E = 10776 would need the marker 47.50 pt higher.

  **ERK'2025 gives 11000.**
- **No value at 401:** arXiv:2409.07222v1 (tables cover 450..527, plus a Legendre table at 450, 471, 491 and 526) and
  arXiv:2210.15962 (171..247).

Including all of these, **the minimum published value is 11000.** It does not change the verdict.

## 4. Decision arithmetic (my own small checker, integer comparison only)

```
claimed E = 10776 | min over named sources = 11888 | strictly below: True | margin 1112
min over all published values in package = 11000 | strictly below: True | margin 224
lowest trivial derivation = 11200 | strictly below: True
```

## 5. Not a trivial derivation, not subsumed

- **Witness pool.** I decoded 707 published witnesses from the primary sources, each reproducing its printed F:
  - Dimitrov: 275
  - archive 2016: 118
  - archive 2018: 99
  - arXiv:2409.07222v1: 75
  - arXiv:2011.00068v1: 51
  - arXiv:2011.00068v2: 50
  - arXiv:2607.09688v1: 35
  - ERK Table 3: 4

  Two rows needed extra handling:
  - ERK Table 3, L = 450: it decodes to E = 13761 and F = 7.35775016. The paper prints 7.3577, which is a truncation in
    the 4th decimal.
  - Dimitrov, L = 409: the paper prints the L = 408 hex here. I rebuilt it from its stated class B_407∘η2∘η6 as
    -1‖W408, which gives E = 11548 and matches the printed F of 7.24285590578.
- **Closest published sequence.** I compared against 386 witnesses of length 300 or more, under all 8 symmetries and
  every shift with an overlap of at least 200. The best agreement is 211/328 = 0.643 (Dimitrov L = 328), then
  245/382 = 0.641 (Dimitrov L = 385 and 386). Minimum Hamming distances to the L = 401 witnesses, over the 8 symmetries:
  Dimitrov 160, Brest-Bošković 173, archive 188 (of 401).
- **Trim-and-extend derivations to L = 401.** These start from every verified witness of length 389..413 (34 distinct,
  including the rebuilt L = 409).
  - Any truncation followed by exhaustive addition of up to 8 end symbols: 1,056,246 candidates.
  - Up to 10 end symbols: 6,435,318 candidates.

  Both searches give a lowest E of 11200: ERK's L = 405 sequence (E = 10906) trimmed by 2 at each end. I rechecked that
  value with exact integers: 11200. 10776 < 11200.
- **The win is genuine.** This is a full-criterion win for one cell, not an enumerated partial win. The bar is not empty:
  a real archive row sets it, and the sequence also beats the strongest published value in the package.

## Limits of what I confirmed

- **Archive.** The package shows the archive's content at commit 1aa1234, fetched 2026-10-24. It does not show that this
  commit was the default-branch HEAD at that time.
- **arXiv:2504.00987.** I read v2; the package does not show that it is the latest version.
- **Newer arXiv results.** I checked them from their abstracts only.
- **Sources outside the package.** I did not read published sources outside the package, which the criterion does not
  name. Examples are journal versions and Dimitrov's DSP 2025 paper on skew-symmetric sequences. ERK'2025 cites that
  paper as [12] but still takes arXiv:2206.12070 as the previous best for 400..450.

confirmed_scope: The sequence in sequence_L401.txt is an explicit +-1 sequence of length 401 whose exactly computed integer energy E = 10776 is strictly below the minimum L = 401 energy over the criterion's named sources as archived in this package (11888, from the borkob/git_labs skew tables at commit 1aa1234, with the arXiv:2607.09688v1 and arXiv:2504.00987v2 tables and the 2026-10-24 arXiv search listing no L = 401 value), below every other published L = 401 value in the package (ERK'2025 Figure 2: 11000; arXiv:2206.12070: 11456; arXiv:2011.00068v1: 11472), and below every truncate-then-extend (up to 10 symbols) derivation of a verified package witness (lowest 11200).

pass: true
