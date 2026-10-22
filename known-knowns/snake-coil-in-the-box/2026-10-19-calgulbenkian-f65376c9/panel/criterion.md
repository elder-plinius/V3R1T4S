# Criterion report: snake-q12-symcoil-1454

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Method and fetches. I read the package and wrote my own checker: transition sequence decoded in base 36 from vertex 0; vertices distinct; every pair of non-consecutive vertices at Hamming distance at least 2 (exhaustive O(L^2) with numpy), consecutive vertices at distance 1, and for coils the closing edge included. Length convention (edges; for a coil also the vertex count) was calibrated on downloaded records: all 15 sample sequences on the live minortriad page for n = 9..13 (snake, coil, symmetric coil) reproduce their table lengths exactly (my calibration output, not shipped in this package), and Caltech record_coils.csv n = 10 row 374 and record_symmetric_coils.csv n = 11 row 734. Live fetches, each once, private copies not shipped in this package: the minortriad page (https://www.minortriad.com/snake/, 2026-10-19T05:30:11Z, HTTP 200, sha256 af45d6499dcae6cb6d3e1942c5ccd0ab8159c7755dec1667e097a1859dfcebb2, same as the hash in the-record-we-beat/README.md); Caltech README.md (2026-10-19T05:30:11Z, 200, b56bf45b4a8bbbb2c5df625ccdaa47693d3832397333c683f691f00daec14a77); record_coils (200, e2c4a5b92a394f85cacccc4cc33ddb1ec31d6319d96680aa8718cebdc172cae0); record_symmetric_coils (200, b5bac7da71f94aa13896e74cbb14259ab9d0596f90b8284ad7d3962fcb920160); record_snakes archive (2026-10-19T05:30:35Z, 200, 7bd8ca971a52e6534670b6802d885f53bad0c31a6ba7117f2ba84ee458acb58e); arXiv 2607.15270v3 HTML (2026-10-19T05:50:46Z, 200, 06d59a9d75cf810e590bf76040bb48730f546a751d5e39bb9aa7b9e354a40d50). Live minortriad table values (read from the page): snake 191/379/750/1480/2946, coil 192/374/740/1468/2930, symmetric coil 186/370/730/1434/2830 for n = 9..13. Not fetched: the Caltech Snakepits folder, EinsteinArena, Zenodo and other later sources.

Win text, literally. Target snake-coil-in-the-box, partial win p1: 'A symmetric-coil record: a coil in Q_n (9 <= n <= 13) that is invariant under the symmetry required by the minortriad symmetric-coil table, verified exhaustively, whose length strictly exceeds the live minortriad symmetric-coil value for that n (context: Q9 186, Q10 370, Q11 730, Q12 1434, Q13 2830).'

Clauses:
1. Coil in Q12 with 9 <= n <= 13: MET (n = 12).
2. Valid induced cycle, exhaustively: MET. 1454 transitions, all coordinates below 12, 1454 distinct vertices, every non-consecutive pair at distance at least 2, closing edge returns to vertex 0 and is induced. Checker output: 0 violating pairs.
3. Invariant under the symmetry the minortriad table requires: MET. The page's own analyzer (quoted in the-record-we-beat/) calls a coil symmetric when its length is 2h and transition i equals transition i + h for all i below h. I tested this directly: the length 1454 is even and the first 727 transitions equal the last 727. (The Caltech notion, v_{i+h} = sigma(v_i) with a coordinate swap P and translation t, is more general; the repository's own symmetric file uses P = identity, which is this same test. Either way the object satisfies the stated, narrower test, so it satisfies p1 as written.)
4. Strictly exceeds the live minortriad symmetric-coil value: MET. 1454 > 1434.
5. Length convention calibration: MET (see Method).
6. No symmetric-coil record exists in the Caltech repository for Q12 (its symmetric file covers n = 10 and 11 only), and the live minortriad value is 1434, so there is no published symmetric coil of equal length among the files I read.

Hidden quantifiers and null models. p1 compares only with the minortriad symmetric-coil column, and the object beats that. It is NOT claimed to beat the main-criterion records (coil records are larger than symmetric ones), and it is not offered as such. The column is symmetric coils only, so nothing in the p1 text asks for more.

Open questions in the claim record (not shipped) that concern this role.
- Which symmetry is intended? Answer: the minortriad analyzer's test (first half equals second half); the object satisfies it.

confirmed_scope: A coil of length 1454 in Q12, valid and induced, whose first half of transitions equals its second half (the minortriad page's own symmetry test), which strictly exceeds the live minortriad symmetric-coil value 1434 for Q12; it is a partial win p1 only and is not claimed to exceed any ordinary coil or snake record.

pass: true
