# Criterion skeptic verdict, L = 328

context: subagent (same VM)

confirmed_scope: The explicit +-1 sequence of length 328 in sequence.txt has exactly recomputed integer energy E = 7148 (F = 7.525), which is strictly below 7444 (F = 7.22622246104), the only published L=328 value found in the ten sources actually read (arXiv:2206.12070 table row, whose printed hex sequence also recomputes to 7444; arXiv:2607.09688 and arXiv:2504.00987 were read and have no L=328 row, and 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222 and Knauer 2004 have none either), while the Boskovic records repository (git_labs tree and Merit_Factor_Records even/odd pages), newer arXiv results and journal-only versions were NOT readable, so "best published" is established only over the sources read.

## Reasoning

Element-by-element check against the verbatim criterion:
- Explicit +-1 sequence: sequence.txt is one line of 328 characters, all in {0,1} (0=+1, 1=-1). Yes.
- 67 <= L <= 600: L = 328. Yes.
- Exact integer energy: I recomputed E = sum_k C_k^2 with Python integers, independently of check_energy.py: E = 7148 (also for the reversed sequence). I also confirmed seq == parent + '1' and that the parent (L=327) recomputes to 6883, matching the printed F 7.76761586518 (327^2/(2*6883) = 7.7676158...). Of the four single end edits of the parent, appending '1' or prepending '1' gives 7148, and appending '0' or prepending '0' gives 7272, so the object is the best of the four one-element edits and the edit is reproducible.
- Baseline: the 2206.12070 row for L=328 prints F = 7.22622246104 and no energy. 328^2/(2F) = 7444.0 exactly. Decoding the printed 82-hex-digit string as a 328-bit sequence (leading zero bits kept) gives E = 7444, so printed F, implied E and sequence agree. The same decoding of the L=327 row reproduces 6883, which validates the decoder. The baseline value 7444 is correct as a table value.
- Strictly smaller, integer comparison: 7148 < 7444 (difference 296, about 4 percent). No merit-factor rounding is involved. One table cell (L=328).

Null models and stretched definitions:
- No hidden quantifier found: the claim is for a single L, one sequence, one comparison. The construction (one end element appended to a published L=327 skew-symmetric record) does not need to be novel in method; the criterion asks only for an explicit sequence with lower exact energy than the best published for that L, and imposes no restriction on how it was obtained. The parent is a published object at a different length, so the L=328 sequence is not itself published (the 328 row is a different, worse sequence). I do not treat it as subsumed: no read source lists any L=328 sequence at or below 7148.
- Why the published 328 value is weak: the 2206.12070 row for 328 is built from a longer chain of operators on B_323 (F 7.226), whereas the L=327 record is a separate skew-symmetric search result (F 7.768). Neighbouring even rows in the same table are also modest (326: 7.506, 330: 7.228, 332: 7.212, 334: 7.069, 336: 7.274), so even lengths in that table are derived afterthoughts, not search results. The 7.525 here would be above every even-length row in the printed window L-3..L+8, which is what one expects if nobody optimised 328 directly.
- Parity: 328 is even, so the skew-symmetric solvers (2206.12070 searches, 2011.00068 up to 303, 2210.15962 up to 247, Brest/Boskovic odd-length work) do not target it. Non-skew general-purpose records at this length would need to be above F = 7.525, which is far beyond the 7.0 floor stated in 2607.09688 ("exceeding 7.0 for 172 <= L <= 527") and beyond what is printed anywhere I could read. 1406.5301 (the 2017 Boskovic et al. paper, 16 lengths in 181..401) has no 328 row. This makes an unread better value unlikely but not excluded.

Residual gap (why the scope sentence is limited): the criterion literally names the Boskovic et al. records repository and "any newer arXiv result" in the minimum. Both were unreadable or unsearched (github 403, even.html 404, arXiv listing 429). So the minimum over all named sources is not fully established; it is established over the ten sources read, with a plausible but unverified expectation that the repository holds no 328 value below 7148 (its pages were Knauer-era and 2013 records, and the tabulated range of the readable Knauer copy ends at 304). A reviewer with access should check the repository for L=328 and for newer arXiv items before making any claim broader than the scope sentence.

Decision: the result meets the full criterion as far as it can be checked with the sources read, by a large margin and with a reproducible exact recomputation; the claim is a genuine win at one length, not a general result, and it is scoped to the sources read.

pass: true
