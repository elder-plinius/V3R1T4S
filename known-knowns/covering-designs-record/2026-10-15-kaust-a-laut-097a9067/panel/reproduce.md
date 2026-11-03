# REPRODUCE skeptic verdict

role: REPRODUCE
context: subagent (Claude Code Agent tool, fresh context that saw only claim/)

Claim under test (from `CLAIM.md`): "The file C61_25_3_27blocks.txt is a (61,25,3) covering design with 27 blocks,
one fewer than the best known value 28 listed for C(61,25,3)."

## Definition (quoted from `CLAIM.md`)

> A (v,k,t)-covering design is a collection of k-element subsets (blocks) of {1,...,v} such that every t-element subset
> is contained in at least one block. C(v,k,t) is the minimum number of blocks.

## Method

Before opening `REPRODUCE.md`, I wrote my own checker from the definition alone (`work/reproduce/check_cover.py`,
Python standard library only). It:

- parses the block file strictly (ASCII only, every token must be a decimal integer, reports any CR bytes);
- checks the block count against the claimed b, that each block has exactly k tokens, no repeated point, all points
  in 1..v, and that the blocks are pairwise distinct as sets;
- checks coverage EXHAUSTIVELY in two independent ways: (A) enumerates every one of the C(v,t) t-subsets of {1..v}
  and tests containment in some block via bitmasks; (B) takes the union of all t-subsets of every block and compares
  its size with C(v,t). No sampling;
- computes the Schonheim bound L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)), L(v,k,1) = ceil(v/k), in exact integer
  arithmetic, and checks b >= L;
- checks C(v,t) <= 5e9;
- computes the sha256 of the input file with hashlib and compares it with the expected value.

## Checker self-test (known positive and negatives I built)

Fano plane (blocks {i, i+1, i+3} mod 7, relabelled 1..7) as a (7,3,2) covering, plus broken variants
(`work/reproduce/tests_output.txt`):

| case | result | reason reported |
|---|---|---|
| Fano plane, 7 blocks | ALL CHECKS PASS: True (exit 0) | checked 21, uncovered 0; L(7,3,2) = 7 |
| one block removed (b=6) | False (exit 1) | uncovered 3 [(1,3),(1,7),(3,7)]; b >= L False |
| one point changed in block 1 | False (exit 1) | uncovered 2 [(1,4),(2,4)] |
| block 2 duplicated over block 1 | False (exit 1) | distinct blocks 6 of 7; uncovered 3 |
| block with a repeated point | False (exit 1) | blocks with repeated points: 1 [3]; uncovered 2 |
| point 8 > v | False (exit 1) | blocks with a point outside 1..v: 1 [4]; uncovered 2 |
| Fano with claimed b=6 | False (exit 1) | block count equals claimed b: False |
| Fano with wrong expected sha256 | False (exit 1) | sha256 match: False |

The checker accepts the valid design and rejects every broken one for the right reason.

## Result on the claimed object

Command: `python check_cover.py claim/C61_25_3_27blocks.txt 61 25 3 27 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e`
(output saved as `work/reproduce/claim_check_run1.txt`; exit code 0). Exact output:

```
input file: C61_25_3_27blocks.txt
input bytes: 1928
input sha256: 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e
expected sha256: 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e
sha256 match: True
carriage returns present: False
blank lines (ignored): 1
parse problems: 0
parameters: v=61 k=25 t=3 claimed b=27
number of blocks: 27
block count equals claimed b: True
blocks with token count != k: 0 []
blocks with repeated points: 0 []
blocks with a point outside 1..v: 0 []
distinct block sizes: [25]
min point: 1, max point: 61
points of 1..v appearing in some block: 61 of 61
distinct blocks (as sets): 27 of 27
C(v,t) = C(61,3) = 35990
C(v,t) <= 5e9: True
method A (enumerate all t-subsets of 1..v): checked 35990, uncovered 0, first uncovered []
method B (union of t-subsets of blocks): distinct covered 35990 of 35990
methods A and B agree: True
Schonheim bound L(61,25,3) = 20
b >= L: True
ALL CHECKS PASS: True
```

("blank lines (ignored): 1" is the empty segment after the file's final trailing newline; `wc -l` gives 27 lines.)

Schonheim recursion steps (`work/reproduce/schonheim_steps.txt`): L(59,23,1) = 3, L(60,24,2) = 8, L(61,25,3) = 20.
b = 27 >= 20. It is also >= the LJCR lower bound low_bd = 22 in the Zenodo excerpt, so there is no conflict with
any known lower bound in the saved files.

Determinism: I ran the check a second time (`work/reproduce/claim_check_run2.txt`), exit 0. The two output files are
byte-identical (`cmp` reports no difference). Both have sha256
915861933970ee0917396d0eab68de56045db8ed3751bc37c76305ba3baff4df.

Object hash: the hashlib sha256 of `C61_25_3_27blocks.txt` is 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e,
which equals the sha256 stated in `CLAIM.md`.

## Author's `REPRODUCE.md` commands (run after my own check)

I ran steps 1 to 3 exactly as written, from inside claim/ (it has no .py files). Output
(`work/reproduce/reproduce_md_output.txt`):

```
== REPRODUCE step 1 ==
097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e
== REPRODUCE step 2 ==
blocks 27 missing 0
exit: 0
== REPRODUCE step 3 (formula as written) ==
20
```

These agree with my checker on hash, block count, distinctness, block size, range, zero uncovered 3-subsets and the
bound. Step 4 is a live fetch. That is outside this role (no web access), so I checked the saved copy instead (below).

## Saved table record

`table_record/coveringrepository_download_archive_vkt.html`: 171741 bytes, sha256
85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17. Both match `CLAIM.md`. The content is tab-separated
rows "v k t m (empty) blocks" with CRLF endings. 9490 rows parse as data and every one has m = t. The other 140
lines are blank separators.

Lookup (`work/reproduce/table_lookup.py`, output in `work/reproduce/table_lookup_output.txt`):

```
rows matching (v,k,t,m)=(61, 25, 3, 3): 1
  line 9245 raw: b'61\t25\t03\t03\t\t28\r'
  value field(s): ['28']
```

So the saved table's single row for v=61, k=25, t=3, m=3 reads 28, as `CLAIM.md` says. The other v=61, k=25 rows are
t=2: 9, t=4: 90, t=5: 285, t=6: 1329, t=7: 5104, t=8: 20255.

`table_record/ljcr_zenodo_v1.2_C61_25_3.json` reads `"C(61,25,3)": {"size": 28, "low_bd": 22, ...}`. Its best entry is
"28, Simple construction from (60,24,3), LJCR, 2009-01-21". This matches `CLAIM.md` (size 28, low_bd 22).

27 < 28, so the claimed comparison holds against both saved records.

## Mismatches and concerns

- No mismatch found. Every property, the hash, the block count, the exhaustive coverage and the bound check out.
  Both runs are deterministic, and the author's commands agree with my checker.
- Scope limit: I checked the saved files only, not live sources. The success criterion requires re-fetching
  coveringrepository.com, LJCR and the Zenodo/GitHub values at verification time and grepping GitHub/arXiv for
  recent claims. That is outside this role and must be covered elsewhere on the panel.
- The Zenodo JSON is an excerpt prepared by the claimant, not the original coverdata.json. I can confirm what it
  says, but I cannot check its stated coverdata.json sha256 from claim/ alone. No file was saved for the "dmgordo/LJCR
  GitHub has no k = 25 entry" statement, so I could not check it.

pass: true
