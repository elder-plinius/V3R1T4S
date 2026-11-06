# NOVELTY skeptic: claim_v6, target labs-merit-factor-records, cell L = 401

context: subagent (fresh context, Claude Code Agent tool)

Verdict: the claimed E = 10776 at L = 401 is strictly below every L = 401 value I could find. The lowest published value
is E = 11000 (ERK'2025, Figure 2 only). The lowest trivial derivation of a published neighbouring sequence is E = 11200.
The status page and the archive table were each fetched once and returned HTTP 200. Neither was blocked.

All times are UTC on 2026-10-24. File names are relative to the claim folder. My own scripts are not part of the package.

## 0. The object

Before running anything in the package, I wrote my own standard-library checker. On `sequence_L401.txt` it gives
L = 401, E = 10776, F = 160801/21552 = 7.461071. The sequence is skew-symmetric (s[200+j] = (-1)^j s[200-j]).
This matches `CLAIM.md`.

## 1. Status source, fetched once

- URL: https://arxiv.org/abs/2607.09688
- Client: plain `curl/7.81.0` with its default user agent. One request, no retry.
- Time: 21:02:28Z. The server `Date` header was `Sat, 24 Oct 2026 21:02:30 GMT` and `Last-Modified` was `Mon, 24 Aug 2026 20:58:48 GMT`.
- Response: HTTP 200, 43984 bytes. This was a normal abstract page, not a challenge page.
- Title: "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem".
- Authors: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest.
- Versions: only [v1], dated "Wed, 17 Jun 2026 09:17:04 UTC".
- Coverage, quoted from the abstract: "improves the previously best-known results for 35 sequence lengths in the range
  $450 \le L \le 527$ and for $L=573$". The page gives no value at L = 401.
- I also fetched the paper's source once, at 21:15:20Z. Its sha256 is `738c297c53b58cbd7ed4cddd7a05f25e379604427d201e2354471bebe47b43a0`,
  identical to `bar/data/criterion_repair/arxiv_2607.09688v1_eprint.bin`.
  - `TAB_RECORDS.tex` has 35 rows (450..518 and 573), and all 35 sequences reproduce their printed F.
  - No length from 390 to 409 appears in any of its .tex files.
  - The records figure covers "$450 \le L \le 527$ and for $L=573$".
  - The paper does not cite ERK'2025.

## 2. Bošković et al. archive table, fetched once

- Request: one GitHub CLI call, `GET https://api.github.com/repos/borkob/git_labs/contents/results-2018/2018-labs-skew.txt` (raw media type).
- Time: 21:02:51Z.
- Response: HTTP 200, 22501 bytes.
  - The ETag `fffadcb7f9184df5235a5a07ba3890644613d398` equals the git blob hash.
  - sha256 is `1719cd1cf2544f197a621353795c6eef1600479124714682a06eecf14bedd4c1`, identical to `bar/data/borkob_git_labs/2018-labs-skew.txt`.
- Repository state: the default branch `master` is at `1aa123407636e48630174e0bf122037e369c1d68`, last commit 2020-09-15T12:57:12Z ("results 2018").
  The repository's `pushed_at` is 2020-09-15T12:57:25Z. There is one branch. Its two PRs date from 2017 and 2018.
- The L = 401 row, verbatim (sequence cut short here):
  `401	6.7632	11888	110000100111101111101001001011000001111110011110000010110001100111101100...`
- I recomputed E = 11888 for that row. All 104 rows of the file reproduce their E column.
- Other files in the archive:
  - `results-2016/2016-labs-skew.txt` (blob `906e43aa…` matches the tree) has the same L = 401 row.
  - The two Knauer 2004 files (blobs `ca0e6869…` and `ab23f31e…` match the tree) contain no 401.

## 3. Published values at L = 401

| source | E at L = 401 | F | how I obtained it |
|---|---|---|---|
| Pšeničnik, Bošković, Brest, "Integer Partitions and the Merit Factor Problem", ERK'2025, pp. 587-590, https://erk.fe.uni-lj.si/2025/papers/psenicnik(integer_partitions).pdf (fetched 21:07:33Z, HTTP 200, sha256 `72574b63061ac62707b26b77c02698ef20ac8d0bcde1956e9f7060a443149605`, same as `bar/data/erk2025/psenicnik_integer_partitions_erk2025.pdf`) | **11000** | 7.3091 | Figure 2 only; no sequence is printed (details below) |
| Dimitrov, arXiv:2206.12070 (2022), class B_401^{27,13,9} (source fetched 21:16:48Z, sha256 `79806b61…f13a`, same as the package copy) | 11456 | 7.01820006983 | I decoded the hex myself and recomputed E. 310 of 332 rows reproduce their printed F to 1e-8; every row in 389..413 does. |
| Brest & Bošković, arXiv:2011.00068v1 (2020), table "Merit factors and sequences of length 301 up to 401" (sha256 `7ee37bda…4deb4`) | 11472 | 7.0084 | I decoded it myself after removing the typeset space in `...DB2 77EDF`. 51 of 51 rows verify. v2 (MENDEL 2022, sha256 `886de15b…f79b`) covers 201..303 only. |
| Bošković et al. archive, 2016 and 2018 tables | 11888 | 6.7632 | Section 2 |

How I read ERK'2025 Figure 2:
- The figure is a matplotlib Form XObject (`./img/records.pdf`).
- It has 51 blue "Dimitrov" markers and 51 red "Our work" markers at x = 77.7504545455 + 7.0081818182·(L − 400), for L = 400..450.
- I fitted y = a + b·F to the blue markers using Dimitrov's exact F values from my own decode.
  The fit is y = −2120.412296309 + 312.551216294·F, with maximum residual 1.5e-9 pt (5e-12 in F).
  The slope matches the tick-label spacing, 31.2551216293 pt per 0.1.
- The red marker at L = 401 is at y = 164.05579871. That gives F = 7.3091000 and 401²/(2F) = 11000.05.
  E = 11000 is the only integer consistent with F rounded or truncated to 4 decimals.
- Cross-check: the red values at L = 405, 422, 433, 441 and 450 equal Table 3's printed F (7.5199, 7.5981, 7.8016, 7.4823, 7.3577).
  I decoded the Table 3 sequence for L = 405 myself: E = 10906, F = 7.519943, skew-symmetric.
- A small inaccuracy, unrelated to L = 401: the printed 7.3577 at L = 450 is truncated. The sequence gives E = 13761 and
  F = 7.357750, which rounds to 7.3578. So `CLAIM.md` is not quite right to say all five reproduce "to 4 decimals".
- The paper says it improved "all fifty sequences in the interval 400 ≤ L ≤ 450" and that these "currently represent the
  best-known results in the literature".

Literature I checked that has no value at L = 401. Each item was read unless marked otherwise.
- arXiv:2409.07222v1: sha256 `09b0825c…69b76d`; 77 rows verify; lengths 450..527.
- arXiv:2504.00987v2: sha256 `bc0b444f…72f5cd`; table rows cover 20..70 and 92..120.
- arXiv:2210.15962: sha256 `7217b1d4…af179`; table rows cover 171..247.
- arXiv:2106.03377 (Dimitrov 2021): its only record is L = 449, F = 6.5319. It mentions 401 only as the end of Brest–Bošković's range.
- Pšeničnik's master's thesis, "Dvofazna optimizacija daljših binarnih zaporedij z nizkimi avtokorelacijami", DKUM 2025:
  MD5 `8976b09ef872923632ccb302a161b00d` matches the repository's listing. Its results cover 450..527 and 573.
- Brest et al., Elektrotehniški vestnik 92(3):97-103 (2025): lengths up to 225.
- ERK programmes:
  - 2026 (24-25 Sep 2026; fetched 21:12:15Z) lists no LABS or merit-factor paper.
  - 2024 (fetched 21:12:43Z) lists no LABS paper.
  - 2025 lists the paper above and an unrelated paper on the asymmetric TSP.
- arXiv API, two date-sorted queries at 21:23:16Z and 21:23:29Z. LABS-related papers since 2024-09:
  - 2610.27329: complexity.
  - 2610.14361: N = 27..60.
  - 2609.05771: crosscorrelation moments.
  - 2511.05778: TOPSIS. "401.16" there is a mean energy at a small length, not a length.
  - 2511.04553: N = 27..37.
  - 2506.17391: NISQ solver.
  - None has a value at L = 401.
- OpenAlex title search since 2024-09-01 (21:32:01Z):
  - Zhang & Melnikov, Cybernetics and Physics 15(1):112-117 (2026): N = 64, 100, 128 (read).
  - Elloumi & Palagi, ROADEF 2026, hal-05534981: n ≤ 60 (read).
  - Liu et al., ISCEIC 2024: "length 150–300" (abstract only).
  - Brest et al., IEEE Access 2024: PSL, N up to 2^20−1 (abstract only).
  - Popič et al., MELECON 2024: L = 31 and 41 (abstract only).
  - Bošković & Brest, ESWA 2024: PSL, L = 2^m−1 (abstract only).
- GitHub, read-only, 21:09-21:30Z:
  - mdayan8/labs-continuation: lengths 450..1100, nothing at 401.
  - thakrarsagar/labs and its upstream discoveryathome/labs: at N = 401, only the archive's E = 11888 (`data/published.json`).
  - J-Brest/LABS: PSL files only.
  - The Endless Exam's LABS instances (copy of its published index): N = 240, 280, 281, 357, 375.
  - jobssteve164dev/proofwild: baselines at 451, 518, 573 only.
  - Repository search for other LABS repositories: none with long-length tables.
  - Code search for the claimed sequence's four symmetry-distinct hex encodings and a binary substring: no hits.
    As a sanity check, the same search finds the archive's L = 401 row in borkob/git_labs.

## 4. Trivial derivations (my own code)

I computed integer energies with an FFT and re-checked each minimum with direct correlation.
1. Pool: 34 verified sequences of length 389..413 (25 from Dimitrov, 7 from Brest & Bošković v1, ERK'2025 L = 405,
   and the archive's L = 401). For each, I removed up to 24 symbols at each end and then exhaustively added up to
   10 end symbols (12 for L = 389 and 390, which need at least 11).
   That is 6,566,390 candidates. The minimum is **11200**, from ERK'2025 L = 405 with 2 symbols removed at each end (F = 7.1786).
   The best results for the other families: Dimitrov's B_407 family gives 11464, B_399 gives 11512, and the B_401 row is
   itself 11456.
2. Trimming only, from all 235 verified longer sequences (Dimitrov 402..527, ERK 405..450, arXiv:2409.07222 and
   arXiv:2607.09688 at 450..573): the minimum is again 11200.
3. Skew-preserving insertions and deletions of free variables (sources of length 397, 399, 403 and 405), plus one
   delete-and-insert move on the 401 sources: the minimum is 11200.
4. This agrees with `bar/data/deep_derivations_401_v5.json` (11200). Every derived sequence has E ≥ 11200 > 10776,
   so the claimed sequence is not one of them.

## 5. This repository

- `TROPHY_CASE.md`: the local copy (repo HEAD `99d7b99d`, 2026-10-21) is byte-identical to the remote file I fetched at
  21:30:08Z, whose last change was 2026-10-17. Neither has any LABS or merit-factor entry, and "401" does not appear.
- PR search: at 21:04:17Z, `gh pr list -R elder-plinius/V3R1T4S --state all --search "labs-merit-factor-records in:title"`
  returned 11 PRs, all CLOSED: #255 (L = 463), #283 (232), #284 (242), #285 (328), #288 (464), #290 (380), #291 (338),
  #292 (377), #293 (384), #294 (391), #295 (252).
  - None is at L = 401. The nearest is L = 391 (#294), which the submitter withdrew: "the sequence is a published
    neighbouring sequence with end symbols trimmed or added".
  - Full PR list: 689 PRs in all, 341 open, newest 2026-10-24T21:14:11Z. No other PR has a LABS title, and no LABS PR is open.
- What counts, in the maintainer's own words:
  - #290: "It is the published L = 383 sequence from that same paper, verbatim, with one symbol trimmed from the start
    and two from the end ... The repo does not count trivial derivations of published instances as new records, so I
    recommend REJECT."
  - #255: "Appending or removing end symbols is exactly the sequence-operator step ... a trivial derivation of a published
    instance is not a new record".
  - Section 4 covers exactly these operations.

## 6. What I could not read

- Brest, Pšeničnik, Popič, A. Brest, Bošković, "Binary Sequences with Low Aperiodic Autocorrelations: Small Peak Sidelobe
  Levels", Preprints.org 202605.0907 (v2 dated 2026-07-28).
  - Landing page: HTTP 403 (curl at 21:13:45Z, and the web tool). Direct download: HTTP 403 at 21:35:07Z.
  - Its OpenAlex abstract says the best-known-PSL sequences "have merit factor ≈ 5.0", which means E ≈ 16,000 at L = 401.
  - Not plausible as an L = 401 value at or below 10776.
- Dimitrov, "On the skew-symmetric binary sequences and the merit factor problem", Digital Signal Processing 156:104793 (2025).
  - ScienceDirect: HTTP 403. SSRN 4939906: HTTP 403. OpenAlex marks it closed access, with no open PDF.
  - Semantic Scholar maps the DOI to arXiv:2106.03377 with the same abstract ("merit factor greater than 5" for long lengths).
    I read that arXiv paper; its only record is L = 449.
  - ERK'2025 cites this journal paper as [12], yet compares 400..450 only against Dimitrov 2022.
  - Low plausibility of an L = 401 value at or below 10776, but not read.
- Full texts of the IEEE Access 2024, MELECON 2024 and ISCEIC 2024 papers: abstracts only (see section 3). Not plausible.

## Conclusion

- Under the bank's own criterion, the comparison set is arXiv:2607.09688, arXiv:2504.00987, the archive and newer
  arXiv work. Its minimum at L = 401 is 11888.
- Against everything I found, the minimum is 11000 (ERK'2025). E = 10776 is 224 lower (F 7.4611 against 7.3091).
- It is also 424 below the best trivial derivation (11200).
- This is not a tie. Nothing at L = 401 is at or below 10776.

pass: true
