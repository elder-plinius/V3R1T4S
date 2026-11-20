# Status and Literature Snapshot (`perfect-cuboid`, Partial Win `p1`)

## Bank status source snapshot
- Target ID: `perfect-cuboid`
- Status source URL: https://en.wikipedia.org/wiki/Euler_brick
- UTC fetch time: `2026-11-19T01:49:44Z`
- HTTP status: `200`
- Selected response headers:
  - `date: Thu, 19 Nov 2026 01:49:44 GMT`
  - `last-modified: Tue, 17 Nov 2026 19:26:30 GMT`
  - `content-type: text/html; charset=UTF-8`
  - `content-length: 205391`
- Fetched page SHA-256: `c9e13da3fa92464a1c28163858afcae7af6aef2e7acda2f492e0102429b6db98`
- Extracted cell / status: `OPEN` ("A perfect cuboid (also called a perfect Euler brick or perfect box) is an Euler brick whose space diagonal also has integer length... no example of a perfect cuboid had been found and no one has proven that none exist.")

## Primary comparison benchmarks and historical lineage for Partial Win `p1`
1. **Aubrey de Grey, Philip Gibbs, and Louie Helm (*Geombinatorics* 33(3), 2024, pp. 107-131):**
   - URL: https://arxiv.org/pdf/2401.06784 (abstract: https://arxiv.org/abs/2401.06784)
   - UTC fetch time: `2026-11-19T01:49:47Z`
   - HTTP status: `200`
   - PDF SHA-256: `8498dd781d31d15d4ccbf06f4429fa41cd49ade051f954578bfc5b741fd123d4`
   - Extracted open problem (Sections 7.2, 7.4, and 10.2): constructs three two-parameter `(p, q)` edge-cuboid fibrations via tangent steps on cuboid elliptic curves; proves Theorem 3 (Section 7.2) excluding the face-ratio family, derives explicit `(p, q)` parametrizations of the two internal-ratio edge-cuboid families in Section 7.4 (Theorem 5), and poses as an explicit open problem in Section 10.2 proving that members of the two internal-ratio families can never be perfect cuboids.
2. **Ronald van Luijk (Doctoraalscriptie, Mathematisch Instituut, Universiteit Utrecht, June 2000, pp. 4-5) and John Leech (*Amer. Math. Monthly* 84(7), 1977, pp. 518-533):**
   - URL: https://pub.math.leidenuniv.nl/~luijkrmvan/ps/cuboids.pdf
   - UTC fetch time: `2026-11-19T04:19:25Z`
   - HTTP status: `200` (`930207` bytes)
   - PDF SHA-256: `2ab7703333e6d8e37698aeb6428a90f9fabe7491648732cd8422a78e8999174c`
   - Historical lineage: John Leech (https://doi.org/10.1080/00029890.1977.11994405, building on W. G. Spohn, *Amer. Math. Monthly* 79(1), 1972, pp. 57-59, https://doi.org/10.1080/00029890.1972.11992984, and followed by W. J. A. Colman, *Fibonacci Quart.* 26, 1988, pp. 54-57 and pp. 338-343, https://doi.org/10.1080/00150517.1988.12429617) introduced the elliptic cycle-of-four framework for edge cuboids and proved non-existence on the `2 Q` face-ratio family. On pp. 4-5 of his 2000 Utrecht thesis, Ronald van Luijk first constructed the two internal-ratio edge-cuboid families from the `(Q, 2 Q)` cycle of four on Leech's curve without proving that their squared third edge is never a nonzero rational square.
3. **René Peschmann (2026-04-30) and Ricky Cipollini (2026-09-13):**
   - Peschmann URL: https://arxiv.org/pdf/2604.28072 (abstract: https://arxiv.org/abs/2604.28072), fetched `2026-11-19T01:49:45Z`, HTTP `200`, PDF SHA-256 `1b91c4ad8a8449a9a6b8a3811360d4ff44c4532b6461cc3e801a188f7064a05e`.
   - Cipollini URL: https://arxiv.org/e-print/2609.14526 (abstract: https://arxiv.org/abs/2609.14526), fetched `2026-11-19T01:51:34Z`, HTTP `200`, e-print SHA-256 `9cc67b1fea9a12bb6faf2f1354361a3364c03b287482a46ed5797c38a5093286`.
   - Extracted baseline: Peschmann excludes `1,072` explicit bounded master-tuple fibers `(m, n)` with `max(m, n) ≤ 100`, and Cipollini excludes the complementary `968` bounded fibers up to `m ≤ 100`; unbounded regimes `max(m, n) ≥ 101` and the two open internal-ratio edge-cuboid fibrations remained open.
