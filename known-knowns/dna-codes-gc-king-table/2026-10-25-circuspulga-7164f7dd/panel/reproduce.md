# Panel: REPRODUCE
context: subagent (fresh context, knowledgeWork subagent, local box only; inputs limited to claim/)
date: 2026-10-25 (Europe/Madrid)

## Definition checked (written before reading the author's code)
"A_4^GC(n,d,w) code: a set of distinct words of length n over {A,C,G,T}, each with exactly w letters in {G,C}, with pairwise Hamming distance >= d." Claim: claim/objects/A4GC_15_11_7_M42.txt is such a code for n=15, d=11, w=7 with 42 words; table entry 34.

## 1. Own checker (independent Python, all 861 pairs, no sampling) on claim/objects/A4GC_15_11_7_M42.txt
```
sha256 7164f7dd9a56e376779fb30fc4d61a3dc7b6c9508cce1b4c1247f89d484b5089
lines_total 42 nonempty 42 distinct 42
lengths [15]
alphabet ['A', 'C', 'G', 'T']
gc_counts [7]
pairs 861 min_dist 11 violations(<d) 0
VALID True size 42
```
sha256sum agrees with the expected value 7164f7dd9a56e376779fb30fc4d61a3dc7b6c9508cce1b4c1247f89d484b5089. Plain ASCII, one word per line, LF endings, no blank lines.

## 2. Table cell (own HTML parser) on claim/data/dnacodes.html
sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5 (matches CLAIM.md). 2 tables; table 0 is under the heading "Lower bounds for A4^GC(n,d,w)" (table 1 is GC,RC, not claimed).
```
hdr   ['n\\d', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ...]
row15 ['15', '6589440c', '1647360c', '103680x', '27840x', '6960v', '1920x', '240x', '124x', '34v', '15v', '6.m', '4.m', '3.p', '-', ...]
```
Raw HTML for the cell: `<td>  34<sup>v </sup></td>`. Value 34, superscript v (VNS, [MS]/[MS2]), not followed by '.' or ':' (so not marked optimal). 42 > 34.
Note: this copy of the page does not state w in its text; w = floor(15/2) = 7 comes from the claim and the King 2003 reference (for the CRITERION skeptic to judge).

## 3. Author's checker (run after mine, matches)
```
n=15 d=11 w=7 size=42 min_distance=11
table cell A4GC(15,11,7) = 34 marker=''
VERDICT: VALID, beats_table=True
```

## 4. Rebuilding the chain per REPRODUCE.md (in a scratch copy, nothing written to claim/)
- `python3 code/gf4slice.py 15 2 3000 s40.txt`: 40 words, about 26 s, byte-identical to objects/intermediate_slice40.txt (cmp OK)
- `./gcmc 15 11 41 401 60 ...`: c41.txt has 41 words, byte-identical to objects/intermediate_code41_s401.txt (cmp OK)
- `./gcmc 15 11 42 5042 600 ...`: c42.txt has 42 words, byte-identical to objects/A4GC_15_11_7_M42.txt (cmp OK), sha256 7164f7dd9a56e376779fb30fc4d61a3dc7b6c9508cce1b4c1247f89d484b5089; my own checker on c42.txt gives VALID True size 42 min_dist 11
Deterministic: one run of each step reproduced the saved files exactly.

## 5. Table-access audit
`grep -rniE 'user-agent|cookie|requests|urllib|curl|wget|403|429' code/` gives no hits.

## Scope of this pass
This reproduces the object's validity (42 distinct words, n=15, GC=7, d_min=11) and the value 34 in the saved html copy. It does not check that 34 is still the live value, and it does not check the literature (that is NOVELTY's job).

pass: true
