# gamma_2 >= 833267/1048576 = 0.7946653...: a lower bound on the binary Chvatal-Sankoff constant

## What

gamma_2 >= 13332272/2^24 = 833267/1048576 = 0.794665336609..., a deterministic lower bound from the unrefereed proof in object/PROOF.md and an exact-integer certificate at window N = 17 with 242,084,334 states (object/CERTIFICATE.md). The three certificate files total 1.7 GB and are not shipped. There is no public download of them yet; RUN_IT_YOURSELF.md rebuilds them in about 15 minutes, and a rebuild on 2026-11-07 matched the sha256 values in object/CERTIFICATE.md byte for byte. The three shipped checkers (check_a17, check_d, check_e) accept them over all states, as did a fourth, unshipped checker. As of 2026-11-07 the best rigorous binary lower bound on the status page is 0.792665992 (Heineman et al. 2024), unchanged since 2026-11-01; this value is above it by 0.00199934 (records in the-record-we-beat/record.md).

The method: read both random strings one character at a time, keep a window of 17 cells of the LCS dynamic-programming table as increment bits together with the 17 characters of B in the window, and let a fixed policy decide from that state whether to read the next character of A (update the row) or of B (shift the window). What leaves the window at the left is a value of a real common subsequence. The bound follows from an integer potential on the 242,084,334 reachable states. object/PROOF.md has the proof.

All three checkers ran over all states and accepted, including check_a17; m + 1 is refused, and three states attain the lowest value. verify-it-yourself/RECEIPTS.md has the output.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. A few seconds on a laptop. This checks the N = 3, 4, 5, 8 certificates with all three checkers and exact tests of the proof steps. The check of the N = 17 certificate needs the large files and is in RUN_IT_YOURSELF.md: about 15 minutes to rebuild with about 2.54 GB of memory, under a minute per checker.

## Compared to

| table | cell | value | fetched |
|---|---|---|---|
| https://teorth.github.io/optimizationproblems/constants/31a.html | best rigorous lower bound, [H2024] | 0.792665992 | 2026-11-01T19:17:18Z, HTTP 200 |

The value here, 0.794665336609..., is above that bar by 0.00199934. That is the best rigorous binary lower bound across the page, its open pull requests, Tomar's record and the arXiv and Zenodo listings. The same page lists 0.79970 [AA2026] and labels it Monte Carlo with a Hoeffding margin, "not a deterministic lower bound"; the target's criterion excludes such bounds ("Probabilistic (Monte Carlo/Hoeffding) bounds never count as bars or as wins."), and the value here is below that number. Open pull requests of teorth/optimizationproblems, Tomar's Zenodo record (upper bounds only), and arXiv and Zenodo listings read 2026-11-01 change no binary lower bound. Details in the-record-we-beat/record.md.

## Not claimed

No optimality and no formal verification; the proof is unrefereed. Fekete's lemma and McDiarmid's inequality are cited, not re-proved. We do not claim this is the limit of the method: window 18 did not fit the 3 GB used here, and at window 17 the one wider near-tie width tried, 0.005,0.005, stopped at a 2600 MB guard; widths under 3 GB between the two are untried. The upper bound is not touched. Lueker's journal paper was not opened; his preprint of 22 July 2005 (32 pages, Internet Archive copy of his UCI page, read 2026-11-07, sha256 eafa7611c163971f871251bcb4f09629a690b488e0e4e675a724a9764def5a4b) was read, and its Figure 1 gives 0.788071 at k = 15 as its best binary lower bound. The Tartu 2026 thesis, Bukh-Cox, Tiskin and the Archivara repository were seen only as search-result summaries; the Jack repository and Zenodo 23735681 were not downloaded, and their metadata describe upper bounds only. Monte Carlo rates in verify-it-yourself/sim_rate17.c carry no weight in the bound.

## Credits

- V. Chvatal and D. Sankoff (1975, J. Appl. Probab. 12(2), 306-315) defined the constant.
- V. Dancik, PhD thesis, Warwick 1994 (https://wrap.warwick.ac.uk/id/eprint/107547/1/WRAP_Theses_Dancik_1994.pdf), chapter 3 and Theorem 2.2: finite-state machines with a tape switch chosen by the state, an output counter, Markov-chain analysis and the |u|+|v| = 2n conversion, giving 0.773911. This is the closest earlier method.
- J. G. Deken (1979, 1983), alternating-pointer matching, as described in Dancik's thesis.
- G. S. Lueker, JACM 56(3), 2009 (https://doi.org/10.1145/1516512.1516519): the certificate T(v, v - r) >= v + r (his Observation 1) with a maximum over which string to discard a character from, 0.788071; the journal version was not opened, but the preprint of 22 July 2005 (https://web.archive.org/web/20070119065823/http://www.ics.uci.edu/~lueker/papers/lcs/lcs.pdf) was read and states the same method (Observation 1, a max over which string to discard) and value (Figure 1).
- M. Kiwi and J. Soto (2009, https://arxiv.org/abs/0810.1066) and G. T. Heineman, C. Miller, D. Reichman, A. Salls, G. Sarkozy, D. Soiffer (https://arxiv.org/abs/2407.10925): the same operator, and the record compared against, 0.792665992.
- L. Jack (https://github.com/leandrejack-afk/chvatal-sankoff-bound) and T. S. Tomar (https://zenodo.org/records/23610945): recent work on the same constant, checked for the bars as stated under Not claimed.
- Maintainers and contributors of https://github.com/teorth/optimizationproblems for the status page.
- The same contributor's earlier unpublished window-16 run: the same method and proof, 0.793914556503.

Different here: window 17 in place of 16, a certificate format that goes past window 16, and a producer that fits window 17 in about 2.54 GB. Against the published work, the state holds the dynamic-programming frontier increments plus a window of B, in place of a single pointer pair, so that the process keeps hindsight across alignments inside the window. The adaptive read and the potential certificate are earlier ideas. We found no published bound using this state space.
