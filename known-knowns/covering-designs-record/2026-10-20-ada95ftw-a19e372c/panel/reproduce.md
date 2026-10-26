# REPRODUCE skeptic: C(35,5,3) <= 713

context: subagent (fresh executor, saw only claim/)

## Definition used (quoted from claim/criterion.md)
> "Success means b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively) ... b must be at least the Schonheim bound L(v,k,t); going below it means a bug."

Here (v,k,t) = (35,5,3), claimed b = 713.

## 1. Own checker, written before opening claim/checker.py
work/mycheck.py (Python 3 stdlib): parses each line, requires exactly k integers, all distinct, all in 1..v; counts lines and distinct blocks; builds the set of all t-subsets contained in some block and compares it against ALL itertools.combinations(range(1,v+1), t) (exhaustive, not sampled); computes Schonheim L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)), L(.,.,0) = 1. VALID only if no bad lines, no duplicate blocks, zero uncovered, b >= L.

```
$ python3 mycheck.py 35 5 3 claim/C35_5_3_713blocks.txt
VALID lines=713 distinct=713 badlines=0 triples=6545 uncovered=0 schonheim=658
$ sha256sum claim/C35_5_3_713blocks.txt
a19e372c3611962126c615fd73a79e8c023e2f7369b38aa29f12ca00e2181149  claim/C35_5_3_713blocks.txt
$ wc -l claim/C35_5_3_713blocks.txt
713
$ awk 'NF!=5' claim/C35_5_3_713blocks.txt | wc -l
0
```
The sha256 matches claim/CLAIM.md exactly.

Schonheim by hand: L(33,3,1) = ceil(33/3) = 11; L(34,4,2) = ceil(34/4 * 11) = ceil(93.5) = 94; L(35,5,3) = ceil(35/5 * 94) = 658. 713 >= 658, so no sub-bound bug signal.

Determinism (two runs, output hashed):
```
69d9acb2cb5c20d8b4669dbb6e865789  -
69d9acb2cb5c20d8b4669dbb6e865789  -
```

Extra: coverage-multiplicity and redundancy (own script):
```
max multiplicity 10 triples covered 6545
redundant blocks (all triples covered elsewhere): 0
uncovered if last block dropped: 10
```
Consistency: 6320*1 + 180*2 + 45*10 = 7130 = 713 * C(5,3), as required.

## 2. Negative and positive controls (own checker)
```
drop last block      -> INVALID lines=712 distinct=712 badlines=0 triples=6545 uncovered=10 schonheim=658  first_uncovered=[(31, 32, 33), (31, 32, 34), (31, 32, 35)]
repeated point (l.1) -> INVALID lines=713 distinct=713 badlines=1 triples=6545 uncovered=6 schonheim=658 first_bad=[(1, 'repeated point')] first_uncovered=[(1, 2, 7), (1, 2, 8), (1, 2, 10)]
point 36 (l.5)       -> INVALID lines=713 distinct=713 badlines=1 triples=6545 uncovered=6 schonheim=658 first_bad=[(5, 'out of range')] first_uncovered=[(6, 11, 13), (6, 13, 14), (6, 13, 18)]
duplicate block      -> INVALID lines=714 distinct=713 badlines=0 triples=6545 uncovered=0 schonheim=658
all 21 5-subsets of 7 -> VALID lines=21 distinct=21 badlines=0 triples=35 uncovered=0 schonheim=5
```
Own checker on the package's control files:
```
data/pos_C7_5_3_all.txt      -> VALID lines=21 distinct=21 badlines=0 triples=35 uncovered=0 schonheim=5
data/neg_minus_last_block.txt -> INVALID lines=712 distinct=712 badlines=0 triples=6545 uncovered=10 schonheim=658  first_uncovered=[(31, 32, 33), (31, 32, 34), (31, 32, 35)]
data/neg_repeated_point.txt  -> INVALID lines=713 distinct=713 badlines=1 triples=6545 uncovered=6 schonheim=658 first_bad=[(1, 'repeated point')] first_uncovered=[(1, 2, 7), (1, 2, 8), (1, 2, 10)]
```

## 3. Author's claim/checker.py per claim/REPRODUCE.md (run only after the above)
Run twice on the claim file, identical output:
```
VALID C(35,5,3) blocks=713 distinct=713 t_subsets=6545 uncovered=0 schonheim=658
point degrees min=101 max=107 points_used=35; coverage multiplicity histogram=[(1, 6320), (2, 180), (10, 45)]
```
This matches the expected line in claim/REPRODUCE.md and my checker's counts (713 / 713 / 6545 / 0 / 658).
Controls:
```
python3 checker.py 7 5 3 data/pos_C7_5_3_all.txt
VALID C(7,5,3) blocks=21 distinct=21 t_subsets=35 uncovered=0 schonheim=5
python3 checker.py 35 5 3 data/neg_minus_last_block.txt
INVALID C(35,5,3) blocks=712 distinct=712 t_subsets=6545 uncovered=10 schonheim=658
python3 checker.py 35 5 3 data/neg_repeated_point.txt
INVALID C(35,5,3) blocks=713 distinct=713 t_subsets=6545 uncovered=6 schonheim=658
problem: line 1: repeated point
```
Author's checker on my own corrupted files (agrees with mine on every one):
```
drop last  -> INVALID ... blocks=712 ... uncovered=10
rep point  -> INVALID ... uncovered=6 / problem: line 1: repeated point
point 36   -> INVALID ... uncovered=6 / problem: line 5: point out of range 1..35
dup block  -> INVALID ... blocks=714 distinct=713 ... uncovered=0 / problem: 1 duplicate block(s)
```
Line-by-line comparison: blocks, distinct, t-subset count, uncovered count and Schonheim value agree between the two checkers on the claim file and on all 7 control files. No mismatch.

## 4. Optional rebuild
Not run: `import ortools` fails (ModuleNotFoundError: No module named 'ortools'). Not required; the claim is the block file alone.

## 5. Notes
- Minor doc nit: claim/REPRODUCE.md says `cd claim/C35_5_3_713`, but the files are directly in claim/. Commands work from claim/. This doesn't affect the result.
- There is no proof step beyond the exhaustive coverage check. I agree: the claim is a finite object, fully verified over all 6545 triples.
- Scope: this review covers reproduction/validity only. It does not judge novelty against the live tables (that is the novelty skeptic's job).

pass: true
