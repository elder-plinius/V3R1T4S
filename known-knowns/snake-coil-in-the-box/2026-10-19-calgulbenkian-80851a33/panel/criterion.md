# Criterion report: snake-q10-coil-374-p3

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Method and fetches. I read the package and wrote my own checker: transition sequence decoded in base 36 from vertex 0; vertices distinct; every pair of non-consecutive vertices at Hamming distance at least 2 (exhaustive O(L^2) with numpy), consecutive vertices at distance 1, and for coils the closing edge included. Length convention (edges; for a coil also the vertex count) was calibrated on downloaded records: all 15 sample sequences on the live minortriad page for n = 9..13 (snake, coil, symmetric coil) reproduce their table lengths exactly (my calibration output, not shipped in this package), and Caltech record_coils.csv n = 10 row 374 and record_symmetric_coils.csv n = 11 row 734. Live fetches, each once, private copies not shipped in this package: the minortriad page (https://www.minortriad.com/snake/, 2026-10-19T05:30:11Z, HTTP 200, sha256 af45d6499dcae6cb6d3e1942c5ccd0ab8159c7755dec1667e097a1859dfcebb2, same as the hash in the-record-we-beat/README.md); Caltech README.md (2026-10-19T05:30:11Z, 200, b56bf45b4a8bbbb2c5df625ccdaa47693d3832397333c683f691f00daec14a77); record_coils (200, e2c4a5b92a394f85cacccc4cc33ddb1ec31d6319d96680aa8718cebdc172cae0); record_symmetric_coils (200, b5bac7da71f94aa13896e74cbb14259ab9d0596f90b8284ad7d3962fcb920160); record_snakes archive (2026-10-19T05:30:35Z, 200, 7bd8ca971a52e6534670b6802d885f53bad0c31a6ba7117f2ba84ee458acb58e); arXiv 2607.15270v3 HTML (2026-10-19T05:50:46Z, 200, 06d59a9d75cf810e590bf76040bb48730f546a751d5e39bb9aa7b9e354a40d50). Live minortriad table values (read from the page): snake 191/379/750/1480/2946, coil 192/374/740/1468/2930, symmetric coil 186/370/730/1434/2830 for n = 9..13. Not fetched: the Caltech Snakepits folder, EinsteinArena, Zenodo and other later sources.

Win text, literally. Target snake-coil-in-the-box, partial win p3: 'An equal-record snake or coil: length equal to the live record (as defined in the success criterion) for that n and type, 9 <= n <= 13, verified exhaustively, and inequivalent under hypercube automorphisms (coordinate permutations and translations) and reversal (plus cyclic rotation for coils) to every record file published in the Math-AI-Caltech repository and the arXiv:2607.15270 data at verification time, checked by comparing canonical relabelled transition sequences.' This is judged against p3's own text; it is not a strict-record claim and does not need to beat the live length.

Clauses:
1. Coil in Q10, 9 <= n <= 13: MET.
2. Valid and induced, exhaustively: MET. 374 transitions, distinct vertices, all non-consecutive pairs at distance at least 2, closing edge induced; checker output 0 violating pairs.
3. Length equals the live record for that n and type: MET. The live minortriad coil value for Q10 is 374; the Caltech coil table also lists 374.
4. Inequivalent to every published record file of the same n and type that I could read, by canonical relabelled transition sequence: MET for what I read. My canonical form relabels coordinates by order of first appearance and takes the minimum over all L rotations and the reversal of the cyclic sequence (this is a complete invariant of the equivalence in p3). Comparison set, with length equal to 374:
   - Caltech record_coils, 12 classes of length 374: all different from the object.
   - Caltech record_symmetric_coils, n = 10, length 370: other length.
   - minortriad page sample co10 (length 374): different.
5. Calibration of the length convention on a downloaded record of the same n and type: MET (the minortriad page sample for this cell reproduces its table length; Caltech coil and symmetric files for n = 10, 11).


Hidden quantifiers and null models. 'Every record file published in the Math-AI-Caltech repository and the arXiv data' is a closed set that I could read except the repository's Snakepits folder (a different table, not fetched); I therefore state the inequivalence only for the files I read. The minortriad page sample for this cell is a published record sequence of the live length and is included in the comparison. A negative result of this test depends on the object not being merely a relabelling, rotation or reversal of a published sequence; a nearby sequence that differs by a local rewrite counts as inequivalent under the p3 definition, and I take p3 literally. The object is described by the author as a drifted copy of an earlier witness; p3 says nothing about that.

Open questions in the claim record (not shipped) that concern this role.
- Does the canonical-hash comparison cover the repository files? Answer: I re-did it from the CSV sequences themselves with my own canonical form, not from the author's hashes, so the answer does not depend on their function.
- Is a minortriad page sample also a published record file for this purpose? Answer: p3 names the Caltech repository and the arXiv data, but the sample is the live record itself, so I included it; the object is inequivalent to it.
- Does a drifted copy count as a new class? Answer: p3 defines inequivalence by canonical relabelled sequence only, and this object differs from every published sequence of that length that I compared with; so under p3's text yes.

confirmed_scope: A valid induced coil of length 374 in Q10, equal to the live record length 374 for this dimension and type and inequivalent (canonical relabelled transition sequence, with reversal and rotation) to every same-length record sequence in the Caltech files and the minortriad page that I read; this is an enumerated partial win p3 only, not a strict record.

pass: true
