novelty: CONFIRMED NEW (novelty axis only; correctness of the certificate was not examined)
context: subagent

Claim (CLAIM.md): gamma_2 >= 833267/1048576 = 0.794665336609, from a window-N=17 adaptive-strip certificate (object/c17.counts, c17.states, c17.V; PROOF.md; PREREG.md).

## Sources (UTC time, HTTP status, value, from command output)
1. Status page https://teorth.github.io/optimizationproblems/constants/31a.html
   - Read once, 2026-11-01T19:17:18Z, HTTP 200, 5816 bytes, last-modified 28 Oct 2026 04:16:30 GMT.
   - Rigorous lower bar: 0.792665992 [H2024], Heineman et al., arXiv:2407.10925.
   - The row 0.79970 [AA2026] is labeled Monte Carlo with a Hoeffding margin and "not a deterministic lower bound", so it is not a bar.
   - Upper bars: 0.825101 and 0.824120 [J2026].
2. Tomar's Zenodo record https://zenodo.org/api/records/23610945
   - 2026-11-01T19:17:26Z, HTTP 200. Version 5, published 2026-10-24, gamma_2 <= 0.821963 (h=13).
   - Upper bounds only; no lower bound in it.
3. teorth/optimizationproblems open pulls, pulls list API.
   - 2026-11-01T19:17:30Z, HTTP 200, 43 open PRs (a single page).
   - Relevant to the Chvátal–Sankoff cells: #249 (replay of the upper bounds), #272 (31b, four-letter alphabet), #273 (C_91, edit distance).
   - None is a binary lower bound.
4. teorth/optimizationproblems closed pulls, pages 1-3: 100 + 100 + 46 = 246 PRs, all HTTP 200. Page 3 was short, so the list is complete.
   - Sankoff hits: #18, #19 (original page), #45 (0.79970 Monte Carlo), #231 (upper 0.824120), #265 (note that 0.79970 is Monte Carlo/Hoeffding), #255 (C_89, not a hit on the topic).
   - No rigorous binary lower bound.
5. elder-plinius/V3R1T4S open pulls, pages 1-4, all HTTP 200.
   - Pages 1-3 returned 100 PRs each. Page 4 (2026-11-01T19:21:37Z) returned 99, so it is the last page.
   - Pages 1-4 therefore cover all 399 open PRs (399 distinct numbers), not just part of them.
   - No title or body mentions Chvátal, Sankoff, LCS or common subsequence.
6. elder-plinius/V3R1T4S closed pulls, pages 1-5, all HTTP 200, 2026-11-01T19:22:04Z to 19:22:21Z.
   - 100 + 100 + 100 + 100 + 51 = 451 PRs. Page 5 was short, so the list is complete.
   - No hit for Chvátal, Sankoff, LCS or common subsequence.
7. This repo's own files.
   - TROPHY_CASE.md (31,306 bytes): grep for chv, sankoff, subsequence, LCS, gamma_2, lueker and teorth found nothing on this topic.
   - known-knowns/: 26 result folders, none on Chvátal–Sankoff or LCS. The only mention of teorth is a URL for another problem (eaqecc-qutrit-codetables-gaps charter).
   - The repo's bank page known-unknowns/erdos-and-proofs/chvatal-sankoff-binary-lcs-constant-bounds.md states the same bars (lower 0.792665992 [Heineman], upper 0.821963 [Tomar]).
   - Its "ideas" for the lower side are Lueker's method with the Heineman memory scheme plus symmetry reduction. It does not mention an adaptive-strip, ROW/SHIFT or potential-vector method.
8. Heineman et al. PDF https://arxiv.org/pdf/2407.10925, 2026-11-01T19:18:51Z, HTTP 200.
   - Method: Lueker / Kiwi–Soto over pairs of binary prefixes of length l (4^l states).
   - Table 2: l=15 gives 0.788071, l=17 gives 0.789882, l=21 gives 0.792665. The increment per l is 0.00061 at l=21 and shrinking.
9. GitHub Statistics-of-Subsequences/PaperMaterials (Heineman code), 2026-11-01T19:20:17Z. The releases list is empty (HTTP 200, `[]`). The last commit is 2024-07-31. There is no release-asset lag.
10. arXiv API (this answers the direct-listing point).
    - The first request, 2026-11-01T19:22:26Z, returned HTTP 301 and 0 bytes.
    - That 301 is a redirect and not a 401/403/429 block. I repeated the same URL once with `-L`, which followed the redirect.
    - 2026-11-01T19:22:32Z, HTTP 200: abs "longest common subsequence" AND "lower bound", newest first. The newest on-topic entry is arXiv:2407.10925 (2024-07-15). The newer entries (2026-10-12 Fréchet, 2026-04-08 deletion channel, 2026-03-31 edit-distance approximation, and so on) are algorithmic or unrelated.
    - 2026-11-01T19:22:43Z, HTTP 200: all "Chvátal-Sankoff", newest first. The newest are 2025-04-14 (2504.10425, multiple strings, asymptotics) and 2024-07-15 (2407.10925). No entry is a newer binary lower bound.
11. Zenodo records list, q="Chvátal-Sankoff", 2026-11-01T19:22:47Z, HTTP 200, 4 hits.
    - 23735681 (2026-10-28, upper bounds, alphabets 3 to 15 and binary h=9/10 certificates).
    - 23610945 and 23610946 (2026-10-24, upper bounds, Tomar).
    - 22051390 (2025-07-10, Portuguese, an empirical simulation with n up to 1000, no bound).
    - No lower bound.
12. Web searches, English, Chinese and Zenodo/Tomar, run earlier. They found no newer rigorous binary lower bound.

## Comparison with the published objects
- The claim exceeds the rigorous bar 0.792665992 by about 0.0020. The 1e-6 margin and the prereg threshold 0.7939155565 are both cleared by a wide margin.
- Heineman/Lueker at l=17 uses 4^17 states and gives 0.789882. The claim at N=17 uses 242M states and gives 0.794665.
- Small certificates in the claim's own format are below the Lueker family at N=3 to 5 (0.7347, 0.7523, 0.7615 against 0.7479, 0.7586, 0.7654). The claim passes it only at larger N, so it is not a trivial edit of the Lueker family.
- Reaching 0.7947 inside the Heineman family would need l far beyond 21.
- The claim is not a deletion, restriction, relabelling, symmetry or numerical polish of a published object. It is not the same method at a higher window.
  - The state is increments h plus a b-window, the policy chooses ROW or SHIFT, and the certificate is a potential V.
  - Nothing is seeded from a published object as far as CLAIM.md and PROOF.md state.
  - Dančík's 1994 increment automaton (0.77391) and Lueker/Kiwi–Soto are conceptual neighbours with far lower numbers.
- I found no publication of this adaptive-strip method at any window.
- The novelty skeptic's notes (not shipped) list 10 hypotheses on how this could fail to be new. They include 2 imported from other fields (average-reward MDP/Lyapunov duals, PushTASEP/seaweed strips) and 1 strange (the Tartu 2026 Markov-model thesis). None was confirmed.

## Not read, not done, blocks
- No block occurred (no 401, 403 or 429 on any request). The single arXiv 301 redirect is the only non-200 response.
- The Tartu thesis, Bukh–Cox, Tiskin and the Archivara repository were seen only as search-result summaries, not opened. Archivara is a Monte Carlo bound, excluded by the criterion.
- The leandrejack repository and the Zenodo 23735681 archive were not downloaded. Their metadata describe upper bounds only.
- I ran no checker and did not examine the certificate's correctness.
- Bars must be re-fetched at the gate. The status page was last modified 2026-10-28.
- Work files (notes, fetch commands, saved pages) are not shipped.

pass: true
