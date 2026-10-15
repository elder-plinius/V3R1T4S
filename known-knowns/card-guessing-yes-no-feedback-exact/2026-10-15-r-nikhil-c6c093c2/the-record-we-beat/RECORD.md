# The record we compared against

No exact value of P+_{2,n} for any n >= 11 is published. The bank's status source was fetched once, honestly:

- URL: https://arxiv.org/search/?query=card+guessing+feedback&searchtype=all&abstracts=show&order=-announced_date_first&size=25
- fetched: 2026-10-15T13:16:53Z, HTTP status 200, client: curl with User-Agent "V3R1T4S-scout/1.0 (research status check)"
- sha256 of the page as fetched: b457009a53b9c7f9ccf724ce8f7c247446977de8a5eb819340e5d339e80ed6fd
- extracted: 19 results; newest arXiv:2610.17479 (12 Oct 2026, complete feedback), 2609.25063 (14 Sep 2026, complete
  feedback, shelf shuffles), 2609.25062 (14 Sep 2026, Luo, partial feedback: bounds and the recursion, no values for
  n >= 11), 2607.10418, 2602.12928, 2602.07920, 2601.16607 (shelf and riffle shuffles), then 2023 and older. None
  reports an exact or numerical value of P+_{2,n} for n >= 11.

Published values used for calibration (the cells below the claim):
- Diaconis-Graham-Spiro, arXiv:2012.04019 (PDF fetched 2026-10-15T13:18:46Z, HTTP 200, sha256
  13e0772a4305aaa7feb4ac3e3cad12174ce276ed3d2728f2d0c08e011a6facf2), Table 2 (n = 2..5) and Table 3 (n = 6..10),
  m = 2, "rounded to four decimal places": 2.8333, 3.0111, 3.0452, 3.0467, 3.0376, 3.0323, 3.0260, 3.0219, 3.0186.
- Diaconis-Graham, Ann. Statist. 9 (1981), Section 3: E(3,3,3;0) = 4.26, E(4,4,4,4;0) = 5.47, E(5,5,5,5,5;0) = 6.63
  (scan fetched 2026-10-15T13:36:19Z, HTTP 200, sha256 7935155102a74847f404ae27ccc27b1c178d4470b418f7f54c4d6feb4db87677).
