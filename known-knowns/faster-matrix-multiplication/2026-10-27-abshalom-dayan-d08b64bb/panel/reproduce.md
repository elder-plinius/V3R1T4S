context: subagent (fresh Claude Code Agent context, Sonnet 5.5, saw only claim/)

# REPRODUCE skeptic report

## Definition used (my own checker, written before reading the author's code)
Quoted from claim/CLAIM.md and the file-format paragraph of claim/REPRODUCE.md: "m_k = (sum u_k[i*13+j] A[i][j]) * (sum v_k[j*13+l] B[j][l]) for A 12x13, B 13x13, and C[i][l] = sum_k w_k[i*13+l] m_k".
Hence the scheme computes AB iff for all index triples (i,j), (j',l), (i',l'):
  sum_k u_k[i,j] v_k[j',l] w_k[i',l'] = [i=i'][j=j'][l=l']   (Brent equations; 156*169*156 = 4,112,784 of them).
My checker (stdlib Python, exact Fractions, then scaled to integers by the lcm of all denominators; accumulates every triple product term by term, so it tests every one of the 4,112,784 equations, both the 2028 target entries =1 and all other entries =0) also reports: term count, terms with an empty factor or explicit zero coefficient, terms whose U, V and W factors are all proportional to an earlier term's (duplicates), and pairs of terms with two proportional factors (mergeable).

## Result on claim/object/
```
terms 1270
terms with empty factor or explicit zero coefficient: 0
terms whose U,V,W factors are each proportional to an earlier term's: 0
pairs of terms with UV both proportional: 0
pairs of terms with UW both proportional: 0
pairs of terms with VW both proportional: 0
lcm denominators 3744
equations total 4112784 | nonzero-target hits 2028 | nonzero off-target/wrong entries 0 | target entries not equal 1 0
RESULT PASS
```

## Planted negatives (mutated copies outside claim/), so the checker can fail
- one coefficient of one w term changed: `off-target/wrong entries 304 | target entries not equal 1 2` -> FAIL
- one term deleted (rank 1269): `wrong entries 1243 | target entries not equal 1 7` -> FAIL
- last term replaced by a copy of the first (duplicate term, rank still 1270): `UW pairs 1, VW pairs 1 ... wrong entries 12787 | not equal 1 12` -> FAIL

## Hashes (claim/REPRODUCE.md section 1)
```
d08b64bb...4690  object/u.txt   (matches)
a1c14244...adaf  object/v.txt   (matches)
8180074e...8f58  object/w.txt   (matches)
9df0b464793e3c9584c9e95e48dc748a4774afa07bd1b7aa7e6d4421570b40eb  rebuild/13x13x13_r1379.npz (matches the stated value)
```
(full values compared against REPRODUCE.md; all four equal.)

## Author's checks (run after mine)
`sh verify-it-yourself/run_checks.sh`: exit 0, printed "format <12,13,13>, 1270 terms, every term with three nonzero factors, common denominator 59904, 4112784 Brent equations checked, 0 wrong", "rank 1270 scheme for <12,13,13> over Q verified exactly", PASS; and 3 random exact evaluations "0 of 156 entries of C differ from AB", PASS. Agrees with mine.

## Rebuild (section 2), run in a copy, python-flint 0.9.0 venv, -I
```
parent <13,13,13> rank 1379
slice axis 0 with e=1,1,1,1,1,1,-4,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1 -> (12, 13, 13) rank 1295
flat absorption removed 25 -> rank 1270
wrote 1270 terms to rebuilt/
same u
same v
same w
```
`cmp` of the rebuilt u/v/w against claim/object/ was byte-identical (one rebuild run; the seed is fixed in the command).

## Caveats / not verified
- The comparison to the four published tables (1274 minimum) rests on claim/TABLE_RECORD.md; I had no network and did not re-fetch, so "strictly below 1274" is taken from the record, not reproduced. The mathematical part of the claim (exact rank-1270 scheme for <12,13,13> over Q, no zero factors, no duplicate or mergeable terms) is fully reproduced.
- Minor: the claim states a "common denominator 59904"; the lcm of all denominators in the files is 3744 (59904 = 16 * 3744). Not a correctness issue (the Brent check is exact either way), only a description difference.
- I did not independently re-verify the parent LITA scheme or the provenance statement; the rebuild is deterministic and byte-identical, and the output is checked on its own by the exhaustive Brent check.

pass: true
