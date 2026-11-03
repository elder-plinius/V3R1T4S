# REPRODUCE skeptic: covering-designs-record, C(38,6,3) <= 469

context: subagent (fresh executor, saw only claim/)

Scope: I read only the isolated claim folder. I made no web requests, because the reproduce role needs none. Scratch files are in work/.

## Definition (quoted from claim/criterion.md)
> "Success means b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively) ... b must be at least the Schonheim bound L(v,k,t); going below it means a bug."

Here (v,k,t) = (38,6,3) and b = 469.

## 1. Own checker, written before opening claim/checker.py
work/mycheck.py is standard-library Python. It:
- parses claim/C38_6_3_469blocks.txt;
- requires exactly 469 lines, each holding 6 distinct integers in 1..38;
- rejects repeated blocks;
- builds the set of every 3-subset contained in some block;
- enumerates all C(38,3) triples with itertools.combinations, so the check is exhaustive and not sampled;
- computes the Schonheim bound recursively as L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)).

```
$ python3 mycheck.py ../claim/C38_6_3_469blocks.txt
file=../claim/C38_6_3_469blocks.txt sha256=09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b
blocks=469 distinct=469 triples_total=8436 covered=8436 missing=0
schonheim L(38,6,3)= 425 C(38,3)= 8436
errors: none
VALID
exit=0
```

**Determinism.** I ran it twice more and diffed the outputs: `diff r1.txt r2.txt && echo deterministic` printed `deterministic`.

**Schonheim bound by hand:**
- ceil(36/4) = 9
- ceil(37/5 * 9) = ceil(66.6) = 67
- ceil(38/6 * 67) = ceil(424.33) = 425

So 469 >= 425. The claim is consistent with the bound, and there is no sign of a bug.

**sha256.** The file hashes to 09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b, which matches claim/CLAIM.md.

**Independent multiplicity cross-check.** Each block contains 20 triples, so the coverage counts must sum to 469 * 20.
```
[(1, 8148), (3, 168), (5, 84), (7, 8), (9, 28)] sum 9380 =469*20= 9380
deg min 70 max 81 points 38
```

## 2. Negative controls for my own checker
I built four corrupted copies of the block file. My checker rejected all four:

| Control | How it was made | Result |
|---|---|---|
| neg_drop | first 468 lines only | `errors: ['468 blocks, expected 469', '8 uncovered triples, e.g. [(26, 29, 37), (26, 29, 38), (26, 35, 37)]']` INVALID exit=1 |
| neg_rep | block 1, point 6 set equal to point 1 | `errors: ['line 1: repeated point', '10 uncovered triples, ...']` INVALID exit=1 |
| neg_range | block 2, point 1 set to 39 | `errors: ['line 2: point out of range', '10 uncovered triples, ...']` INVALID exit=1 |
| neg_dup | line 3 duplicated, then truncated to 469 lines | `errors: ['1 repeated blocks', '8 uncovered triples, ...']` INVALID exit=1 |

My checker also rejects the package's own controls:
- claim/data/neg_minus_last_block.txt gives INVALID, with 8 missing triples.
- claim/data/neg_repeated_point.txt gives INVALID, with a repeated point on line 1 and 10 missing triples.

## 3. claim/checker.py, run per claim/REPRODUCE.md (opened only after steps 1 and 2)
```
$ python3 checker.py 38 6 3 C38_6_3_469blocks.txt
VALID C(38,6,3) blocks=469 distinct=469 t_subsets=8436 uncovered=0 schonheim=425
point degrees min=70 max=81 points_used=38; coverage multiplicity histogram=[(1, 8148), (3, 168), (5, 84), (7, 8), (9, 28)]
exit=0
$ python3 checker.py 38 6 3 C38_6_3_469blocks.txt   (second run, identical)
VALID C(38,6,3) blocks=469 distinct=469 t_subsets=8436 uncovered=0 schonheim=425
point degrees min=70 max=81 points_used=38; coverage multiplicity histogram=[(1, 8148), (3, 168), (5, 84), (7, 8), (9, 28)]
exit=0
$ python3 checker.py 7 5 3 data/pos_C7_5_3_all.txt
VALID C(7,5,3) blocks=21 distinct=21 t_subsets=35 uncovered=0 schonheim=5
exit=0
$ python3 checker.py 38 6 3 data/neg_minus_last_block.txt
INVALID C(38,6,3) blocks=468 distinct=468 t_subsets=8436 uncovered=8 schonheim=425
exit=1
$ python3 checker.py 38 6 3 data/neg_repeated_point.txt
INVALID C(38,6,3) blocks=469 distinct=469 t_subsets=8436 uncovered=10 schonheim=425
problem: line 1: repeated point
exit=1
$ python3 checker.py 38 6 3 ../work/neg_dup.txt
INVALID C(38,6,3) blocks=469 distinct=468 t_subsets=8436 uncovered=8 schonheim=425
problem: 1 duplicate block(s)
exit=1
$ python3 checker.py 38 6 3 ../work/neg_range.txt
INVALID C(38,6,3) blocks=469 distinct=469 t_subsets=8436 uncovered=10 schonheim=425
problem: line 2: point out of range 1..38
exit=1
```

**Line-by-line comparison with my checker:**
- Block count: 469 in both.
- Distinct blocks: 469 in both.
- Triples: 8436 total in both.
- Uncovered triples: 0 in both.
- Schonheim bound: 425 in both.
- Multiplicity histogram: identical.
- Point degrees: min 70, max 81 in both.
- Controls: each one is rejected by both checkers with the same uncovered counts (8, 10, 8, 10).

There are no mismatches.

One minor note: claim/checker.py does not itself assert that the block count equals the claimed b. It prints `blocks=469`, and my checker asserts the count explicitly.

## 4. Optional rebuild
claim/rebuild/ was not run. numpy 2.5.4 is present, but `import ortools` fails with `ModuleNotFoundError: No module named 'ortools'`. The claim rests on the block file alone, so the rebuild is not required.

## 5. Proof steps
I agree there is no proof step to re-derive beyond the exhaustive coverage check. The claim is an explicit object, and both checkers verified it exhaustively over all 8436 triples. This verdict covers reproducibility and validity only. Novelty against the live tables is outside the reproduce role.

pass: true
