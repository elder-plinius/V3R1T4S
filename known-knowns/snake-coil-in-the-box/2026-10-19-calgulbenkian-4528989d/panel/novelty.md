context: Claude Code subagent, fresh context [Sonnet 5.5]

# novelty report: snake-q12-snake-1480-p3

Claim: an induced snake of length 1480 in Q12. Target snake-coil-in-the-box, enumerated partial win p3 (equal-record witness that is inequivalent to every published record file). I judge p3 against its own text: under the kit's general rule a tie is not a record, but p3 defines the win as an equal-length witness in a new class, so the question is whether the length equals the live record and the class is new.

Read from the package: README.md, INDEX.csv, the-record-we-beat/README.md and published.json.

## Common sources (fetched once for the whole review group; each source is given with its fetch time, HTTP status and sha256)

- Fetch method: plain curl with the honest client string, one request per URL, no retries. Times are UTC. Where a fetch needed a deviation it is stated under unresolved.
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-19T05:27:03Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments. No row for snake-in-the-box.
- known-knowns listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-19T05:27:03Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty directories. There is no directory for snake-coil-in-the-box.
- Pull requests: I used a snapshot of all V3R1T4S pull requests (titles and bodies), 473 entries, fetched 2026-10-19T04:30:31Z, instead of the api.github.com pulls pages, which I did not fetch. I read every title and searched every body for the target ids and keywords (snake-coil).
- The contributor's review ruling R1: closed pull requests from the 2026-10-14 bulk close by the same contributor (#65-#120) are the author's own earlier filings, not competing values. They are reported, not counted against a cell.

## Primary sources (snake-in-the-box)

- minortriad table: https://www.minortriad.com/snake/, fetched 2026-10-19T05:26:55Z, HTTP 200, sha256 af45d6499dcae6cb6d3e1942c5ccd0ab8159c7755dec1667e097a1859dfcebb2 (identical to the triage fetch). Change log, last entry in the page source: "updated 11-oct-2026 with snake (13-d,len=2946)". Table rows (snake / coil / symmetric coil): dimension 10: 379 / 374 / 370; dimension 11: 750 / 740 / 730; dimension 12: 1480 / 1468 / 1434; dimension 13: 2946 / 2930 / 2830. The table has no dimension 14. As calibration I re-verified all 15 sample sequences for dimensions 9 to 13 in the page with my own induced-path checker (no chords, distinct vertices, closing edge for coils); every sample has exactly the table length.
- Math-AI-Caltech Snake-in-the-Box README: https://raw.githubusercontent.com/Math-AI-Caltech/Snake-in-the-Box/main/README.md, 2026-10-19T05:26:56Z, HTTP 200, sha256 b56bf45b4a8bbbb2c5df625ccdaa47693d3832397333c683f691f00daec14a77. Quoted (contributor names omitted): "Subsequent bounds by others: 750 in Q11, 1480 in Q12 and 2934 in Q13 (names omitted)"; "Subsequent coil bounds by others: 740, 1468 and 2930 in dimensions 11-13"; its own records: snakes 191, 379, 746, 1476, 2924; coils 192, 374, 734, 1466, 2916; symmetric coils: 10: 370, 11: 734, and nothing for 12 or 13. Its pulls page (https://github.com/Math-AI-Caltech/Snake-in-the-Box/pulls, 2026-10-19T05:26:56Z, HTTP 200, sha256 8fe9a04136415f465b35a9af0998270a5e8bf7172e5efd3b4dd053689e4cc975) shows openCount 0 and closedCount 0.
- Caltech data files (one request each, 2026-10-19T05:34:07Z to 05:34:08Z, all HTTP 200): record_coils sha256 e2c4a5b92a394f85cacccc4cc33ddb1ec31d6319d96680aa8718cebdc172cae0 (coil classes: Q10 length 374: 12; Q11 length 734: 11; Q12 length 1466: 5; Q13 length 2916: 1; sigma-symmetric flag true only for Q9 192 and two Q11 734 coils); record_symmetric_coils sha256 b5bac7da71f94aa13896e74cbb14259ab9d0596f90b8284ad7d3962fcb920160 (Q10 370: 2 classes; Q11 734: 1 class); record_snakes archive sha256 7bd8ca971a52e6534670b6802d885f53bad0c31a6ba7117f2ba84ee458acb58e (I streamed record_snakes; longest per dimension: 191, 379, 746, 1476, 2924, so it has no file at the live snake lengths 750, 1480 or 2946).
- Literature: arXiv:2607.15270 v3 abstract page (2026-10-19T05:32:40Z, HTTP 200, sha256 23c86ec0a6552e8cdbf4cf2fbc59b86a7b176a33e817bae459a85e6218427731) and full html (https://arxiv.org/html/2607.15270v3, 2026-10-19T05:35:53Z, HTTP 200, sha256 06d59a9d75cf810e590bf76040bb48730f546a751d5e39bb9aa7b9e354a40d50): no dimension 14 value anywhere in the text; symmetric coils only for n = 10, 11. arXiv API query 1 of 4 (snake-in-the-box, newest first, 2026-10-19T05:32:37Z, HTTP 200, sha256 ab20b320f862e066e137af9b86324e96c8b42e95f6d98eb488a3c6ce5aad8dcb): newest are 2607.15270 (July 2026) and 2409.04476 (Sept 2024, a QUBO formulation); nothing else in the last 24 months. Wikipedia Snake-in-the-box (2026-10-19T05:32:39Z, HTTP 200, sha256 500fe2fca60a64db36a65bd1002938496efc3ad9fbdf7e040f23026e19a9ca9e): no dimension 14 value. EinsteinArena home page (2026-10-19T05:40:57Z, HTTP 200, sha256 f5c8fff10812b9c529aec39e0f9922c564c7bb3a1cbfb872ec5ef72a87258094): "Snake-in-the-Box (13-dimensional hypercube)", baseline 2,934, a reported 2,938-edge snake; no dimension 14.
- Pull requests in this repository on this target (snapshot of all pull requests): the contributor's closed #88 (R1, own earlier filing): #88 (Q12 snake 1480). Another contributor's open #393 updates the bank text only ("Facts only"). No other contributor has a value on this target; no merged package exists for it.

## My own class comparison

Script: my own comparison scripts (not shipped in this package). I read the object (one base-36 digit per step from vertex 0), verified it is induced with my own check (every vertex has exactly 2 path neighbours, 1 for snake endpoints, none further away along the path; coil closes at the origin) and got the exact length stated in the cell. I computed a canonical class under coordinate permutation (relabel by first appearance), translation (automatic, sequences start at 0), reversal, and for coils every cyclic rotation, taking the lexicographic minimum, and compared with (a) every Caltech record file of the same dimension and type at the same length and (b) the minortriad page sample of the same dimension and type.

## This cell

Object length by my own check: 1480 (matches the claim). Live comparison value: 1480 (minortriad snake column, dimension 12; Caltech README: "1480 in Q12"). Published sequences or values: Caltech has no snake file of length 1480 (longest Q12 snake there is 1476); the only published record sequence is the minortriad sample.
Class comparison: The object is not in the class of the minortriad sample.
The contributor's earlier filing on this cell: #88 (Q12 snake 1480) (R1: own earlier filing, reported, not competing).

Coverage of the p3 comparison set: the Caltech data holds no file at this length for snakes, and for coils it holds the classes counted above; I compared with all of them where they exist and with the minortriad sample (a published record sequence). The object is in a new class under the canonical comparison p3 prescribes, and its length equals the live record, so the p3 text is met. An open question asks whether a sample on the minortriad page is a published record file; I compared with it anyway, so the answer does not change the result. The "drifted copy" question: p3 defines inequivalence by the canonical comparison, which the object passes; whether a neutral-walk neighbour of an earlier witness is interesting is not part of that text.
Propagation (PR #350 rule): an equal-length witness is not a value that follows from the tables; no propagation applies.

unresolved: Google Scholar and private communication were not searched (the minortriad table is updated from personal emails, so a longer value could exist before it is posted). arXiv API budget: four queries for the whole group.

novelty verdict: the length equals the live record and the class is new against every Caltech record file of that dimension and type and against the live page sample; no other pull request has a witness for this cell.

pass: true
