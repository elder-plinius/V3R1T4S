context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/

# REPRODUCE verdict

## Definition quoted (CLAIM.md, success criterion, verbatim)
"a set S of distinct vectors in {0,1,2}^n ... such that for every pair of distinct x,y in S, the third point -(x+y) mod 3 is not in S, verified exhaustively"
Claim: cap_1104_n9.txt is such a set in F_3^9 with 1104 elements, larger than 1082 (the largest 9-dimensional cap the listed sources report).

## My checker (written before reading checker/capcheck.py or inputs/verify_structure.py)
mychk/my_check.py: reads the file as bytes, prints sha256; requires every line to be exactly 9 chars from {0,1,2} (no CR, final newline noted);
checks distinctness; loops over ALL 608856 unordered pairs (C(1104,2)) and tests whether z = -(x+y) mod 3 is in S; second route loops over all
ordered pairs x != y and counts z in S with z not in {x,y}. Negative control (mychk/neg.txt = 000000000, 111111111, 222222222) correctly reports NOT A CAP (3 violations).

mychk/my_struct.py: independent re-derivation of REPRODUCE.md section 3 (slices by first digit; C = inputs/record_512_n8.txt; D = diag(2,2,2,2,2,1,1,1);
form set {-(c + D c')}; K = F_3^8 minus form set; exhaustive cap test of C and of slice 0).

## Commands and exact outputs
`python3 -I mychk/my_check.py cap_1104_n9.txt 9 > mychk/out1.txt` (run twice, out1.txt and out2.txt, `cmp` -> identical), contents:
```
sha256 26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e
ends with newline: True CR present: False
lines 1104 valid vectors 1104
distinct 1104 all distinct: True
pairs checked 608856 expected 608856 violations 0
ordered-pair violations (route 2): 0
RESULT CAP size 1104 n 9 claimed 1104: True
```
`shasum -a 256 cap_1104_n9.txt` -> `26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e  cap_1104_n9.txt` (matches expected).

`python3 -I mychk/my_struct.py` (run twice, outputs identical, mychk/struct_out1.txt, struct_out2.txt):
```
|C| 512 distinct 512 all len8 True
C is cap: True
slice sizes {0: 80, 1: 512, 2: 512}
slice1 == C: True  slice2 == D C: True | |DC| 512
|form| 6469 |K| 92
slice0 subset of K: True  slice0 cap: True
C & DC overlap 128
```
Author's commands (REPRODUCE.md), run after my checker:
```
$ python3 checker/capcheck.py cap_1104_n9.txt 9; echo "exit $?"
checker A: CAP - cap of size 1104 (pairs checked: 608856)
checker B: CAP - 0 lines inside S (lines meeting S twice or more: 608856)
VERDICT: CAP size 1104 n 9
exit 0
$ python3 inputs/verify_structure.py
slice sizes {'0': 80, '1': 512, '2': 512}
slice1 == C: True  slice2 == D C: True
|K| = 92  slice0 subset of K: True
slice0 is a cap: True
```
Author output identical to the expected block in REPRODUCE.md; two further runs of capcheck.py gave byte-identical output (mychk/author1.txt, author2.txt).
Hashes checked: inputs/record_512_n8.txt and checker/capcheck.py: both match CLAIM.md (record file 15f918afc3f5fc39bb300447e18929f980e51feea47f5113c3238ef80ad24860; capcheck.py 0d162d448d862f6ae35910ae000bb7a2f49e2564207a065b7d61fb8586e0f2dd);
sources/funsearch-cap_set.ipynb sha256 f97f6f6ec331e5809ca4d40205224d2c5c613687d4f65316ecc2dd04a1724203 matches, and contains "largest known cap set for `n = 9` has size `1082`".

## Mismatches
None. Deterministic across repeated runs.

## Limits of this check (not mismatches)
- "Larger than the best known" is confirmed only against the sources in the package (FunSearch notebook states 1082); I could not verify Edel's tables or the arXiv search (no network, and the package says Edel's tables were not read). 1104 > 1082 itself is verified.
- Provenance of inputs/record_512_n8.txt (conversion from the FunSearch file) was not re-fetched; it is a valid 512-cap by my check and is only needed for the optional structure claims.

pass: true
