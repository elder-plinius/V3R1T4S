# The record we extend

| field | value |
|---|---|
| URL | https://oeis.org/A210662/b210662.txt |
| fetched (UTC) | 2026-11-03T08:34:08Z (also 2026-11-01T08:35:26Z, 2026-11-02T08:36:53Z, and the NOVELTY panel's own 2026-11-03T08:38:42Z — all byte-identical) |
| HTTP | 200 |
| sha256 | 05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d |
| bytes | 22774 |
| content | 378 terms, the triangular table rows n = 1..27; T(n,k) = monomer-dimer tilings of the k x n board |

The extracted baseline: the LAST PUBLISHED ROW (n = 27) and the corner cell
T(27,27) = 10246…0347 (207 digits) — the largest published value; every claimed
T(28,k) exceeds it. The snapshot copy is b210662_snapshot.txt (as fetched;
compare sha256). The diagonal equals A028420 through n = 27 (cross-checked
against that sequence's b-file). a28_anchor.txt is our own open PR #849 object
(the 28th diagonal cell), used as the CRT anchor: every T(28,k) counts
matchings of a subgraph of the 28x28 grid, so T(28,k) <= a(28) < 2^737 < the
794-bit products of either run's primes.
