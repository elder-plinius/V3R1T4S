# REPRODUCE skeptic: verdict on claim_v6 (labs-merit-factor-records, L = 401)

context: subagent (fresh context, Claude Code Agent tool)

Scope and order of work. I read only files inside the claim folder, and every file named below is relative to it. When I checked whether this output folder existed I saw the names of the entries in the run folder, but I opened nothing outside the claim folder. I wrote my own energy checker, hex decoders and PDF vector readers before reading `check_labs.py`, `bar/read_erk2025_fig2.py` or `bar/deep_derivations.py`. I ran the package's scripts last, on a scratch copy. I used at most 4 CPU cores and no GPU. All numbers below are copied from my command output.

## Definition used (quoted from CLAIM.md, "Target statement (verbatim from the bank)")

"For a +-1 sequence s of length L, the aperiodic autocorrelations are C_k = sum_i s_i s_{i+k}, the energy is E = sum_{k=1}^{L-1} C_k^2, and the merit factor is F = L^2/(2E)."

## 1. The sequence and its energy

- `sequence_L401.txt` is 402 bytes: 401 symbols and one trailing newline. Byte histogram: '1' = 213, '0' = 188, newline = 1. Only the symbols {0,1} occur. sha256 e979ad4ab8b2de33a68d6700b89b83c9e227cc2a616c041f1ce4fb6969e1f8da.
- My checker uses two independent exact-integer algorithms: a direct double loop, and a big-integer polynomial product (Kronecker substitution). I self-tested it on Barker 11 and 13 and on 200 random sequences. Output: `L = 401 E_direct = 10776 E_kronecker = 10776 F = 160801/21552 = 7.461070898292502`. Claimed E = 10776 and F = 7.4611: **reproduced**.
- Provenance properties also hold. Skew-symmetry s[200+j] = (-1)^j s[200-j] has 0 violations. The minimum Hamming distance to Dimitrov's L = 401 witness over the 8 energy-preserving symmetries is 160 (identity, and reversal plus alternation). Claimed: 160.

## 2. Published values at L = 401, re-derived from the primary files

| source (file) | my result at L = 401 | CLAIM.md |
|---|---|---|
| Archive, `bar/data/borkob_git_labs/2016-labs-skew.txt` and `2018-labs-skew.txt` | row `401 6.7632 11888 <401 symbols>`. Recomputed E = 11888, F = 6.763164535666218, in both files. All 124 rows of each file reproduce their printed E (0 mismatches). | 11888 (match) |
| Dimitrov, `bar/data/eprints/arxiv_2206.12070_eprint.bin` (`bare_jrnl.tex`, byte-identical to `bar/data/dimitrov_2206.12070/src/bare_jrnl.tex`) | class B_401^{27,13,9}, 101 hex digits (space removed), printed New MF 7.01820006983. Recomputed E = 11456, F = 160801/22912 = 7.018200069832402. All 62 rows in 389..450 reproduce their printed New MF. | 11456 (match) |
| Brest & Bošković v1, `bar/data/eprints/arxiv_2011.00068v1_eprint.bin` (`tb_best.tex`, identical to `bar/data/brest_boskovic_2011.00068/v1/tb_best.tex`) | printed F 7.0084. The hex has one internal typeset space; with it removed, 101 digits give E = 11472, F = 7.008412. All 51 typeset rows reproduce their printed F. A LaTeX-commented (not typeset) row gives E = 11496. | 11472 (match) |
| ERK'2025, `bar/data/erk2025/psenicnik_integer_partitions_erk2025.pdf`, Figure 2 (my own reader, section 3) | F_new = 7.309100000000. The only integer energy consistent with 7.3091 (rounded or truncated) is E = 11000 (F = 7.309136363636363). | 11000 (match) |
| arXiv:2607.09688v1, `bar/data/criterion_repair/arxiv_2607.09688v1_eprint.bin` | `TAB_RECORDS.tex` (third table input in main.tex, after `TAB_TOPPAR` and `TAB_PARTITIONS`) has 35 rows: 450, 451, 452, 455-465, 475-484, 490, 491, 494-498, 516-518 and 573. All 35 printed F reproduce. The other two tables list partitions. No 401 anywhere in the TeX. | no value (match) |
| arXiv:2504.00987v2, `bar/data/criterion_repair/arxiv_2504.00987v2_eprint.bin` | `tab:labs_results` has 16 lengths: 92, 98, 104, 106, 108, 110, 112, 114, 116, 118, 120, 99, 107, 109, 113, 119. `tab:fit` and `combinedTable` hold no sequences. It cites github.com/borkob/git_labs (Bošković, Brglez, Brest, 2016). | no value (match) |
| arXiv:2409.07222v1, `bar/data/criterion_repair/arxiv_2409.07222v1_eprint.bin` | `table.tex` has 77 result rows covering 450..527 with 518 absent. 76 reproduce their printed F within 5e-5; L = 451 gives E = 14065, F = 7.23075 against a printed 7.2307. Its Figure fig:oldmf plots L = 401 at F = 7.01815, i.e. E about 11456.09 (Dimitrov's value; see note 1). | no value in the result rows (match; see note 1) |
| arXiv:2210.15962, `bar/data/eprints/arxiv_2210.15962_eprint.bin` | 17 table rows, odd lengths 171..247. Its MF figures stop at L = 250 and L = 240. | no value (match) |
| Knauer 2004, `bar/data/borkob_git_labs/2004-Knauer-original.txt` / `.html` | no L = 401. Largest length: 222 in the .txt (200 rows), 304 in the .html (270 rows). | matches |

I also read the figures of arXiv:2011.00068v1 that reach L = 401. `fg_MF_201-401` and `fg_MF-L301-401` show F = 7.0084 (E about 11472), and `fg_MF` and `fg_MF-allL` show 6.9939 (E about 11496). arXiv:2011.00068v2 never mentions 401.

## 3. ERK'2025 Figure 2, read with my own reader

- The figure is Form XObject /Im2 on page 4. It contains 51 red dashed vertical segments, 51 "Dimitrov" circle markers (/M0) and 51 "Our work" markers (/M1). The x step is a constant 7.0081818182 pt per unit L, starting at L = 400. Segment endpoints coincide with the markers to within 4.95e-07 pt.
- I calibrated independently of the package: a least-squares fit of the 51 Dimitrov markers against Dimitrov's exact F for L = 400..450, decoded from his TeX. The result is c = 312.551216294 pt per unit F, with max residual 1.547e-09 pt. The y tick-label spacing implies c = 312.551216293. The fit is this exact, so both the L assignment and the scale are confirmed.
- L = 401 reads F_old = 7.018200 (Dimitrov, E = 11456) and F_new = 7.309100000000, so E = 401^2/(2F) = 11000.0547. All 51 "Our work" values are exact 4-decimal numbers, and at the five Table 3 lengths they equal the printed values.
- Comparison with the package: `bar/data/erk2025/fig2_values.json` agrees with my reading. Max |F_new difference| = 1.0e-05 and max |F_old difference| = 1.15e-05 (the package rounds to 5 decimals). The nearest-integer E_new agrees at all 51 lengths. Rerunning `bar/read_erk2025_fig2.py` on a copy reproduced `fig2_values.json` identically. Its log shows a calibration residual of 1.074e-02 pt (CLAIM.md says 0.011 pt).
- Table 3, decoded by me. L = 405 gives E = 10906 (F 7.519943, printed 7.5199). L = 422 gives E = 11719 (7.598089, printed 7.5981). L = 433 gives E = 12016 (7.801639, printed 7.8016). L = 441 gives E = 12996 (7.482341, printed 7.4823). L = 450 gives E = 13761 (7.357750, printed 7.3577; see note 2). These equal `bar/data/erk2025/table3_verified.json`.

## 4. Hashes

All 13 sha256 values in `table_record.md` match the saved files ("all sha256 match: True"). The git blob SHA-1 of all four archive files match `bar/data/criterion_repair/borkob_tree_1aa1234.json`:

- 2004-Knauer-original.txt: ca0e6869a97177496462d567357047a503d2c359 (this is also the value stated in table_record.md)
- 2004-Knauer-original.html: ab23f31e868e9f8de998c5a55684307244fd8999
- 2016-labs-skew.txt: 906e43aa7d15a7044cb800969ac3934c41470eac
- 2018-labs-skew.txt: fffadcb7f9184df5235a5a07ba3890644613d398

The tree listing has 146 entries and truncated: false. Its only results files are the four named in CLAIM.md; the other blobs are solver code and solver test-run output.

## 5. Trivial derivations, with a bounded check of my own design

- Pool: 1668 sequences, all decoded by me. 330 Dimitrov, 51 Brest & Bošković v1 plus the 1 commented row, 45 v2, 124 + 124 archive, 5 ERK'2025 Table 3, 77 arXiv:2409.07222, 35 arXiv:2607.09688, and 225 + 651 mdayan8 from the package TSVs.
- T1: every length-401 window of every pool sequence. 299,313 windows; minimum E = 11200, from the ERK L = 405 sequence starting at offset 2. Minimum per source: ERK 11200, Dimitrov 11456, Brest v1 11472, archive 11888, mdayan8 15328, arXiv:2409.07222 17416, arXiv:2607.09688 17448.
- T2: any truncation, then exhaustive addition of every ±1 pattern at every left/right split. Up to 12 added symbols for the 23 sources of length 389..401, up to 10 for the 13 of length 402..413, up to 8 for the 95 of length 414..460, and up to 4 for the 1015 longer sources. 79,134,757 candidates (FFT energies, exact after integer rounding). Minimum E = 11200 (ERK L = 405, 2 symbols removed from each end, 0 added). The best from any other source is 11456 (Dimitrov L = 401 unchanged).
- Exact integer check of that derivation: E = 11200 by both of my algorithms.
- Package: `bar/data/deep_derivations_401_v5.json` gives deep_bar 11200, "ERK2025 L=405 remove 2/2 add 0", F 7.1786, the same result. Rerunning `bar/deep_derivations.py 401` on a copy produced an identical JSON. The superseded files give 11456 at L = 401, as CLAIM.md states: `bar/data/bar_395_407.json`, `bar/data/deep_derivations_401_v3.json`, `bar/data/bar_351_449.json` and `bar/data/deep_derivations_401.json`.
- No derivation in either search reaches 10776 or below.

## 6. The package's checker, run last

`check_labs.py sequence_L401.txt --L 401 --E 10776 --below 11000` printed `L = 401`, `E = 10776`, `F = L^2/(2E) = 160801/21552 = 7.461071`, `bar = 11000; strictly below: True` and `PASS`, with exit code 0. This agrees with my checker. Two reruns gave byte-identical output (md5 461b102a0d87b9ceef9a5032e0d972e7). A negative control (`--E 10775 --below 10776`) printed FAIL. I saw no non-determinism anywhere.

## 7. Accuracy of CLAIM.md's statements about the sources

Every statement the record comparison depends on is accurate. The newer-arXiv search also checks out: 100 entries in descending date order spanning 2026-03-26 to 2026-10-19, so the window from 2026-06-17 onward is fully covered. 66 entries fall on or after 2026-06-17, including arXiv:2607.09688 itself. The three LABS-related abstracts match CLAIM.md's descriptions. I found these inaccuracies; **none affects the record comparison**:

1. Table row for arXiv:2409.07222v1, "no value at L = 401". This is true of its result rows. However, its Figure fig:oldmf (file `plots/old_mf.pdf` inside `bar/data/criterion_repair/arxiv_2409.07222v1_eprint.bin`, captioned "Largest known merit factors (F) for L ≤ 527") plots L = 401 at F = 7.01815, E about 11456. That is Dimitrov's value, already in the comparison, so the comparison is unaffected.
2. Trivial-derivations bullet, "all five reproduce their printed F to 4 decimals". For L = 450, E = 13761 gives F = 202500/27522 = 7.3577502, which rounds to 7.3578, not the printed 7.3577. It matches only under truncation, and `bar/parse_erk2025.py` uses a 1e-4 tolerance with a comment saying so. The same boundary effect occurs at arXiv:2409.07222v1 L = 451. This is peripheral: L = 450 lies outside the derivation window, and L = 405, which sets the derivation bar, matches exactly.
3. "Primary-source archives" section, "Their sha256 are in table_record.md". There is no sha256 row for `bar/data/eprints/arxiv_abs_2607.09688.html` (my sha256: 5710c1bdbadba480cbb819984dec6f19ddb7a456fd6d226bca68cac38c100c92). Peripheral.
4. Table row for arXiv:2504.00987v2, "`tab:fit` (a runtime fit over N = 20..70)". The rows are fits with lower limit N_min^fit = 20, 25, ..., 70. Loose wording; peripheral.

There is also a quirk in a source file, not an error in CLAIM.md: one `\allowbreak` in arXiv:2409.07222v1 `table.tex` (row L = 459) is split across a line break. I rejoined it to decode the row. It is irrelevant to L = 401.

Limits of this check (not mismatches):
- Not checkable offline from the package: that the ERK'2025 paper is "not on arXiv", the URLs, and the fetch times.
- For the three newer LABS-related arXiv papers, the package holds only their abstracts. Those abstracts show scopes unrelated to L = 401: complexity theory, N = [27, 60], and crosscorrelation moments.
- Dimitrov's DSP 2025 paper ("On the skew-symmetric binary sequences and the merit factor problem", DSP 156:104793) is cited by arXiv:2607.09688 and by ERK'2025 (as [12]). It is neither in the package nor discussed in CLAIM.md. Indirect evidence suggests it holds nothing below 11000 at L = 401. ERK'2025 cites it and still says its own 400..450 values "currently represent the best-known results in the literature". arXiv:2409.07222v1's largest-known figure shows 11456 at L = 401. The paper is also outside the bank's criterion set (arXiv:2607.09688, arXiv:2504.00987, the archive, and newer arXiv results).

## Verdict

E = 10776 reproduces exactly: my two algorithms and the package checker agree, and the run is deterministic. It is strictly below every published value I could find for L = 401: 11000 (ERK'2025 Figure 2), 11456 (Dimitrov), 11472 (Brest & Bošković v1), 11496 (their commented-out row) and 11888 (archive). It is also strictly below every trivial derivation I computed, whose minimum is 11200. The margin to the lowest published value is 224 in energy (F = 7.4611 against 7.3091). The inaccuracies in section 7 are peripheral and do not change the comparison.

pass: true
