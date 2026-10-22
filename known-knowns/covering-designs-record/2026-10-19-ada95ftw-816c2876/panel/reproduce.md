# REPRODUCE skeptic: C(29,5,3) <= 399

context: subagent (fresh executor, saw only claim/)

Claim: claim/C29_5_3_399blocks.txt is a (29,5,3) covering design with 399 blocks (sha256 816c2876...b94a56bbb).

## Definition (quoted from claim/criterion.md)
> "Success means b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively) ... b must be at least the Schonheim bound L(v,k,t); going below it means a bug. Same-day claim only if C(v,t) <= 5e9, so the exhaustive coverage check runs on a laptop"

C(29,3) = 3654, far below 5e9, so a full exhaustive check is possible and was done.

## My own checker (written before opening claim/checker.py): work/mycheck.py
It reads the raw bytes and computes the sha256. Then it checks that the file has exactly 399 lines, that each line has 5 integers, that no point repeats within a block, that every point is in 1..29, and that no block repeats. It enumerates all 3654 3-subsets of {1..29} with itertools.combinations and fails if any is not contained in some block. Finally it computes Schonheim L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)) recursively and fails if b < L.

```
$ python3 mycheck.py claim/C29_5_3_399blocks.txt
sha256 816c287640bc50f50a87d27707aaae2c77ff99c1580a07336a594d3b94a56bbb
lines 399
triples total 3654 covered 3654 uncovered 0
Schonheim L(29,5,3) = 366
RESULT VALID
exit=0
```
Determinism: I ran it twice, saving the output to r1.txt and r2.txt. `diff r1.txt r2.txt` printed nothing, and the script then printed `deterministic`.

Schonheim by hand: L(27,3,1) = ceil(27/3) = 9; L(28,4,2) = ceil(28*9/4) = 63; L(29,5,3) = ceil(29*63/5) = ceil(365.4) = 366. Since 399 >= 366, the claim is consistent with the bound.

sha256 matches CLAIM.md: `816c287640bc50f50a87d27707aaae2c77ff99c1580a07336a594d3b94a56bbb  C29_5_3_399blocks.txt`. There are no CR characters (`grep -c $'\r'` returns 0).

Additional (my code): coverage-multiplicity histogram `[(1, 3528), (2, 56), (3, 56), (13, 14)] sum 3990 399*10= 3990`, point degrees min 68 max 91 over all 29 points. Removing any single block uncovers some triple: `blocks whose removal keeps coverage: 0`.

## Negative controls (mine)
```
drop last block (398 lines):  RESULT INVALID: expected 399 lines, got 398; uncovered triples, first: [(15, 22, 27), (15, 22, 28), (15, 22, 29)]  exit=1
line 1 point 2 := point 1:    RESULT INVALID: line 1: repeated point; uncovered triples, first: [(1, 4, 5), (1, 4, 8), (1, 4, 15)]  exit=1
line 7 point 5 := 30:         RESULT INVALID: line 7: point out of range; uncovered triples, first: [(1, 3, 16), (1, 5, 16), (1, 10, 16)]  exit=1
last block replaced by copy of block 1: RESULT INVALID: repeated blocks: 1; uncovered triples, first: [(15, 22, 27), (15, 22, 28), (15, 22, 29)]  exit=1
claim/data/neg_minus_last_block.txt: RESULT INVALID: expected 399 lines, got 398; uncovered triples, first: [(15, 22, 27), (15, 22, 28), (15, 22, 29)]
claim/data/neg_repeated_point.txt:   RESULT INVALID: line 1: repeated point; uncovered triples, first: [(1, 4, 5), (1, 4, 8), (1, 4, 15)]
```
I confirmed that neg_minus_last_block.txt is exactly the first 398 lines (`diff` empty), and that neg_repeated_point.txt differs only on line 1 (`1 4 5 8 15` -> `1 1 5 8 15`).

## Author's checker, claim/checker.py, run per claim/REPRODUCE.md (after mine)
```
$ python3 checker.py 29 5 3 C29_5_3_399blocks.txt   (run twice, identical)
VALID C(29,5,3) blocks=399 distinct=399 t_subsets=3654 uncovered=0 schonheim=366
point degrees min=68 max=91 points_used=29; coverage multiplicity histogram=[(1, 3528), (2, 56), (3, 56), (13, 14)]
exit=0
$ python3 checker.py 7 5 3 data/pos_C7_5_3_all.txt
VALID C(7,5,3) blocks=21 distinct=21 t_subsets=35 uncovered=0 schonheim=5
exit=0
$ python3 checker.py 29 5 3 data/neg_minus_last_block.txt
INVALID C(29,5,3) blocks=398 distinct=398 t_subsets=3654 uncovered=8 schonheim=366
exit=1
$ python3 checker.py 29 5 3 data/neg_repeated_point.txt
INVALID C(29,5,3) blocks=399 distinct=399 t_subsets=3654 uncovered=6 schonheim=366
problem: line 1: repeated point
exit=1
my controls through checker.py:
INVALID C(29,5,3) blocks=398 distinct=398 t_subsets=3654 uncovered=8 schonheim=366
INVALID C(29,5,3) blocks=399 distinct=399 t_subsets=3654 uncovered=6 schonheim=366
INVALID C(29,5,3) blocks=399 distinct=399 t_subsets=3654 uncovered=6 schonheim=366
INVALID C(29,5,3) blocks=399 distinct=398 t_subsets=3654 uncovered=8 schonheim=366
```
Comparison, line by line: the two checkers agree on block count (399), triples (3654), uncovered (0), Schonheim (366), point degrees (68/91, 29 points), and the full multiplicity histogram. Every control gets the same verdict and the same uncovered count from both checkers (8, 6, 6, 8 for my four controls; 8 and 6 for the packaged ones). I found no mismatch, no missing object and no non-determinism.

## Proof steps
Beyond the exhaustive coverage check and the Schonheim sanity bound, there is no proof step to re-derive. I agree.

## Scope note
This verdict covers only the mathematical validity of the object and the claimed value b = 399. I did not re-fetch the comparison tables. Whether 399 beats every live table value (413 in claim/data/*.json and the operator's hand read recorded in claim/CLAIM.md) is for the novelty and criterion skeptics. The two data excerpts in claim/data/ both state size 413, low_bd 366.

## Scratch code (work/mycheck.py)
```python
import sys, itertools, hashlib, math
def check(path, v=29, k=5, t=3, b=399):
    raw = open(path,'rb').read()
    print("sha256", hashlib.sha256(raw).hexdigest())
    lines = raw.decode('ascii').split('\n')
    if lines and lines[-1]=='': lines=lines[:-1]
    errs=[]
    blocks=[]
    for i,l in enumerate(lines,1):
        toks=l.split()
        try: pts=[int(x) for x in toks]
        except ValueError: errs.append(f"line {i}: non-integer"); continue
        if len(pts)!=k: errs.append(f"line {i}: {len(pts)} points")
        if len(set(pts))!=len(pts): errs.append(f"line {i}: repeated point")
        if any(p<1 or p>v for p in pts): errs.append(f"line {i}: point out of range")
        blocks.append(frozenset(pts))
    print("lines", len(lines))
    if len(lines)!=b: errs.append(f"expected {b} lines, got {len(lines)}")
    if len(set(blocks))!=len(blocks): errs.append(f"repeated blocks: {len(blocks)-len(set(blocks))}")
    covered=set()
    for B in blocks:
        for T in itertools.combinations(sorted(B),t): covered.add(T)
    alltr=list(itertools.combinations(range(1,v+1),t))
    unc=[T for T in alltr if T not in covered]
    print("triples total", len(alltr), "covered", len(alltr)-len(unc), "uncovered", len(unc))
    if unc: errs.append(f"uncovered triples, first: {unc[:3]}")
    # Schonheim
    def L(v,k,t):
        if t==0: return 1
        return -(-v*L(v-1,k-1,t-1)//k)
    print("Schonheim L(%d,%d,%d) ="%(v,k,t), L(v,k,t))
    if len(blocks)<L(v,k,t): errs.append("below Schonheim bound: bug")
    print("RESULT", "VALID" if not errs else "INVALID: "+"; ".join(errs[:5]))
    return not errs
ok=check(sys.argv[1])
sys.exit(0 if ok else 1)
```

pass: true
