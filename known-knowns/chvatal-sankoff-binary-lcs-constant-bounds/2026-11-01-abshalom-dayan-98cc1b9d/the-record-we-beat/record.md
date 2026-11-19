# The record compared against

Fetches (URL, UTC time, HTTP status, sha256). Response headers not saved.

https://teorth.github.io/optimizationproblems/constants/31a.html 2026-11-01T18:05:51Z HTTP 200 177aa953ac6c70a5d4b48c9d9d2bd26262428947195ee959c92b5ec7931fd8bc
https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/31a.md 2026-11-01T18:05:51Z HTTP 200 80b53e18cafa5100b72d3fb02e5e564d05bb93b882f55a190c22c0fc5df4b599
https://zenodo.org/api/records/23610945 2026-11-01T18:05:52Z HTTP 200 a8974e98a7500e32b66ca3332059c2d5b4b7a451e116157c23b500de160b24b1, version 5, upper bounds only.
https://api.github.com/repos/teorth/optimizationproblems/pulls?state=open&per_page=100 2026-11-01T18:05:52Z HTTP 200 a33983d91329db17ed66bb3c01ff06b06bc04d1d70a96382a2ef414cba10956a
https://teorth.github.io/optimizationproblems/constants/31a.html read again 2026-11-01T19:17:18Z HTTP 200, same bar, hash not saved; read again 2026-11-01T20:16Z HTTP 200, same sha256 as the first read above.
arXiv API, abstract search "longest common subsequence" and "lower bound", and all-fields search "Chvatal-Sankoff", newest first, 2026-11-01T19:22:32Z and 19:22:43Z, HTTP 200. The newest entry on this bound is arXiv:2407.10925 (2024-07-15).
Zenodo records search, q = Chvatal-Sankoff, 2026-11-01T19:22:47Z, HTTP 200, 4 hits, none a lower bound.

Extracted cell (Known lower bounds, page text): 0.773911 [D1994]; 0.788071 [L2009]; 0.792665992 [H2024], computer assisted; 0.79970 [AA2026], "AI and computer assisted (unverified)", Monte Carlo with a Hoeffding margin, "It is not a deterministic lower bound".

Open pull requests touching 31a, 31b or 91, from the pulls list API at 2026-11-01T19:17:30Z, HTTP 200, 43 open on a single page: #249 (upper-bound replay), #272 (four letters), #273 (edit distance). None changes the binary lower bound.

Re-read 2026-11-07: https://teorth.github.io/optimizationproblems/constants/31a.html at 2026-11-07T20:07:37Z, HTTP 200, 5816 bytes, same sha256 as the first read (177aa953...), last-modified 28 Oct 2026; raw 31a.md same sha256 (80b53e18...). Open pull requests of teorth/optimizationproblems at 2026-11-07T20:07:47Z, HTTP 200: 75 open; those whose files touch constants/31a, 31b or 91a are #249 (upper-bound replay), #272 (31b, four letters), #273 and #306 (91a, edit distance). None changes the binary lower bound. Zenodo 23610945 latest is still version 5 (2026-11-07T20:08:52Z, HTTP 200). arXiv API and Zenodo searches at 2026-11-07T20:09:05Z, HTTP 200: no binary lower bound newer than arXiv:2407.10925.

Lueker preprint: https://web.archive.org/web/20070119065823/http://www.ics.uci.edu/~lueker/papers/lcs/lcs.pdf, 2026-11-07T20:10:02Z, HTTP 200, 255,969 bytes, sha256 eafa7611c163971f871251bcb4f09629a690b488e0e4e675a724a9764def5a4b, dated July 22, 2005, 32 pages; Figure 1 last row k = 15, 0.788071.

Certificate archive: https://zenodo.org/api/records/24051334 read 2026-11-08, HTTP 200, published 2026-11-08, DOI 10.5281/zenodo.24051334, files c17.counts 262,144 bytes md5 970ef8d6581996f271ce65e1850063da, c17.states 726,253,002 bytes md5 e16ff4fe34e50079f8901f3c9a27ad74, c17.V 968,337,336 bytes md5 a4ddcc41a198ad048ff40cd18b6bb5e1; uploaded from files whose sha256 match object/CERTIFICATE.md.
