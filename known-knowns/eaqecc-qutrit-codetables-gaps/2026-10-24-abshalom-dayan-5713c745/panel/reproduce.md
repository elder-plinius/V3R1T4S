# REPRODUCE skeptic verdict: [[33,7,15;12]]_3 (object/eaqecc_33_7_15_12.json)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

**Pass.** From the matrix S alone, by my own exact method (a Brouwer-Zimmermann search I wrote for the GF(3)-linear
symplectic dual, checked against brute force), the object has s = 38, c = 12, k = 7 and minimum distance d = 15
exactly: no nonzero vector of span(S)^perp has symplectic weight 14 or less, and weight-15 vectors outside the
isotropic part exist (9946 supports). All five of the author's offline steps (REPRODUCE.md steps 1-5) ran and printed
exactly the values REPRODUCE.md states, and their counts agree with my independent ones (9946). No mismatch, no
missing object, no non-determinism. Not covered here: the live table cell and novelty (step 6, other skeptics).

## The definition (quoted from claim/CLAIM.md, success criterion)

> "with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic
> commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in
> the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used
> by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper."

Conventions used (from the object's `S_convention` field): S rows are (x|z) over GF(3), 2n columns,
<(x|z),(x'|z')> = x.z' - z.x'; the weight of a vector of GF(3)^{2n} is its symplectic weight
#{i : (x_i, z_i) != (0,0)}.

## What I computed, and how (my own code, written before reading claim/checkers/ or claim/rebuild/)

Files in my work folder, `mine/`:

| file | role | sha256 |
|---|---|---|
| mine/gf3lib.py | exact GF(3) elimination; s, rank(S J S^T), c, k, a basis of N = span(S)^perp, dim of I = span(S) ∩ N | 03717233c0d2810102ec95625a0f50eb95162aa506e939a4608fade59f2d403e |
| mine/bz3.c | exact minimum symplectic weight of N \ I (Brouwer-Zimmermann written for GF(3)-additive codes; uses no GF(9) structure) | 8ad848f71157ff786690e31d314318797942fa6a7cc7ac66dacf9858667a0c4a |
| mine/prep.py | runs gf3lib on the object's S, writes the C input, checks the JSON's other fields | 15b8352d11b4992eec84cc38c252746a6aa75a36ef43799bed8d738629d11069 |
| mine/dedupe.py | distinct weight-15 words and supports from bz3's log, each re-checked in Python | ab2a964c060821bf88eabaced4e124879a1ba583ba72072becf26470d35e438f |
| mine/test_small.py | brute-force tests, n = 3..6 | 3cbf150d552c8a8b264169277e64e8d5a76855f1bec73e07a515c55de2b825d2 |
| mine/test_small2.py | brute-force tests, n = 6, 7, several disjoint full sets | cf9a500c60a5c14bcbc82a34c63ab9117294f07f5ce07fbe5e27c44eec07821d |
| mine/seeded_negative.py | seeded negatives at full size | 535bf48f5f822bd5abee6f48c257630100101a08a3bd243299bec60a3018d41c |

Object hash checked first: `shasum -a 256 claim/object/eaqecc_33_7_15_12.json` =
5713c745e8e837dc41e1883a120488fb38dce3b4254292335ca98f99a1787256 (as stated in CLAIM.md).

### Parameters from S alone (mine/prep.py)

| quantity | my value | claimed |
|---|---|---|
| n | 33 | 33 |
| rows of S / s = rank(S) over GF(3) | 38 / 38 (rows independent) | |
| rank(S J S^T) (matrix antisymmetric: True) | 24 | |
| c = rank/2 | 12 | 12 |
| k = n - s + c | 7 | 7 |
| dim N = dim span(S)^perp | 28 (= 2n - s) | |
| dim I = dim(span(S) ∩ span(S)^perp) | 14 (= s - 2c) | |

Checks of the JSON's other fields (not needed for the distance, done for completeness): S equals phi(D9) with rows
r, w*r interleaved (True); G9 . conj(D9)^T = 0 (True); GF(9) ranks G9 = 14, D9 = 19; the GF(3) span of phi(G9) and
phi(w G9) equals my N (True).

### Minimum distance, exactly (mine/bz3.c)

Method. N is treated only as a GF(3)-linear code of length 2n with symplectic (block) weight. A "full set" P is a set
of positions whose columns of N's generator contain dim N = 28 independent columns (free coordinates, chosen
greedily). In systematic form each codeword is determined by its free values; a block with a nonzero free value is a
nonzero block, so enumerating every free assignment with at most w nonzero blocks (one of each +-pair) covers every
codeword with block weight <= w on P, and any codeword not reached has block weight >= w+1 on P. With disjoint full
sets P_1, P_2 enumerated to levels w_1, w_2, every codeword reached by neither has weight >= (w_1+1) + (w_2+1). Every
reached word is weighed exactly and tested for membership in span(S) by elimination against the RREF of S. Before
the search the program re-checks that its N basis is symplectically orthogonal to all 38 rows of S, and self-tests
its bit-sliced GF(3) addition on all 9 pairs.

Real run (`nice ./bz3 16 15 0 < real_input.txt`; 15.76 s, peak memory 1196344 bytes): two disjoint full sets of 14
positions each (positions {0..10,12,13,15} and {11,14,16..27}; 5 positions left over), both enumerated to level 7,
8054538032 words in total (per level C(14,i)*4*8^(i-1), e.g. 3598712832 at level 7, matching the formula). The bound
on words not reached is 16, so every vector of N of weight <= 15 was reached. Result:

- no nonzero vector of N (inside or outside I) has symplectic weight <= 14;
- weight-15 vectors outside I exist: 39784 distinct ones up to sign, on 9946 distinct 15-position supports (exactly 4
  per support), every one re-checked in Python as orthogonal to all rows of S and not in span(S);
- smallest nonzero weight found inside I: 34 (that is, none of weight <= 15);
- **d = 15 exactly.** Witness (x|z) printed by bz3:
  `100000000001002201002101122200000000000000002000201122120210200000`, re-checked in Python: symplectic weight 15,
  orthogonal to all 38 rows of S, not in span(S), support {0,11,14,15,17,...,27}.

Robustness: a second run with the same arguments gave a byte-identical output (sha256
f70a4b0043f9289a43a55bd57caa9b23e899033967598fb2819ac60955714fcd both times). A run with shuffled position order
(seed 11, different information sets) gave d = 15 exact and the same 9946 supports / 39784 words; an automatic-stop
run with seed 5 stopped at bound 15 with d = 15 exact.

## Tests of my checker

| test | runs | result |
|---|---|---|
| brute force, random S (n = 3..6, 1..2n rows, some with forced dependent rows) and phi(random GF(9) matrices); s, rank(SJS^T), c, k, dim N, dim I and d each obtained by full enumeration of GF(3)^{2n} and of span(S) | 756 (each case in 2 position orders x 2 stopping modes) | 0 mismatches |
| brute force, n = 6, 7 with s >= n so that 1 to 7 disjoint full sets are used (chunked enumeration of up to 3^14 vectors) | 90 | 0 mismatches; d ranged 2..7, plus 6 cases with no vector outside I |
| seeded negative 1: S' = basis of {r in span(S) : <r,u> = 0} for a random u of weight 14, so u is in span(S')^perp and not in span(S') | 1 | checker reports d = 11 exact (an even lighter word exists), witness re-checked in Python; the claimed d = 15 is rejected |
| seeded negative 2: same with a planted u of weight 10 | 1 | checker reports d = 10 exact, witness re-checked; rejected |

Peak memory of the largest test batch: 764806176 bytes (under the 1 GB limit).

## The author's REPRODUCE.md steps 1-5 (run on a copy of claim/ in author_run/)

I read claim/checkers/ and claim/rebuild/ only after my numbers above existed; they are plain computation (file writes
only to the paths given on the command line, no network or process calls). Step 6 (live table) was not run: it is
another skeptic's role.

| step | command (from REPRODUCE.md) | printed | REPRODUCE.md expects | match |
|---|---|---|---|---|
| 1 | build_x_lead.py ... rebuilt.json 15; shasum | `X code [33,14] hull=7 -> [[33,7,?;12]]  S 38x66  D9 19x33`; both hashes 5713c745e8e837dc41e1883a120488fb38dce3b4254292335ca98f99a1787256 (files byte-identical by cmp) | same line and hash | yes |
| 2 prep | gf9info.py prep | `n=33 s=38 c=12 k=7 dim_N=28 dim_I=14 N_closed_under_w=True`, `kappa=14` | same | yes |
| 2, m=19 | infoset 19 p 3, p = 0,1,2 | subsets = 507629004, 219864219, 91315977 (sum 818809200 = C(33,19)); deficient = 0, 0, 0 | same | yes |
| 2, m=18 | infoset 18 p 3 | deficient = 5445, 2942, 1559 (sum 9946); subsets sum 1037158320 = C(33,18) | 5445, 2942, 1559 | yes |
| 3a | gf9info.py witness ... (18 zero positions) | `weight=15 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False` | same | yes |
| 3b | witness.py ... 0,11,14,15,17,...,27 | `symplectic_weight=15 orthogonal_to_all_rows_of_S=True in_span_S=False` | same | yes |
| 4 prep | gf3prep.py | `n=33 s=38 c=12 k=7 dim_isotropic=14 dim_dual=28` | same | yes |
| 4, W=14 | subset_ea64 14 p 3 | examined = 272936400 in each part (3 x 272936400 = 818809200 = C(33,14)); with_vector_outside_isotropic = 0, 0, 0 (285.13 s, 286.38 s, 286.62 s) | examined=272936400, 0 | yes |
| 4, W=15 | subset_ea64 15 p 3 | examined = 345719440 each (total 1037158320 = C(33,15)); with_vector_outside_isotropic = 3362, 3252, 3332 (sum 9946); 393.40 s, 388.88 s, 389.05 s | 3362, 3252, 3332 | yes |
| 5 | bz64 < G9.txt | `K=14 n=33 d=15 sets=14,14,3,2 maxw=7 words=4027269016` and a weight-15 witness word (11.14 s) | same | yes |

Cross-checks between the author's outputs and mine: the three `first=` 15-subsets printed by step 4 and the support of
the step-3 GF(9) witness are all among my 9946 weight-15 supports; my count of supports (9946) equals step 4's W = 15
total and step 2's deficient 18-subsets. Step 3b's witness support {0,11,14,15,17,...,27} is the support of my bz3
witness.

Determinism: step 5 rerun twice more gave byte-identical output (sha256
696942e92ea59b9d3b87a01dea4f2af2c10dd20bbeee6e30c2dc3414b0b62a00 both times); step 2 m = 18 rerun gave the same
5445, 2942, 1559. My bz3 run was repeated with a byte-identical result (above).

I also read the logic of the author's checkers after running mine: subset_ea64.c tests, for each W-subset T, whether a
non-I basis row becomes dependent after restricting to the complement of T with the I rows eliminated first, which is
exactly dim N_T > dim I_T, that is, a vector of N \ I supported in T; infoset.c and bz64.c are standard exact
methods on the GF(9) code, which applies because N is closed under w (which I confirmed independently: phi(C) = N).

Run log: started 20:26:03 UTC, finished 21:11:09 UTC. Step 4 ran one part at a time until the coordinator raised the
limit to 2 heavy processes mid-run; I then stopped only my own step-4 driver shell (the PID I had recorded), let the
running W = 15 part 1 finish, and ran W = 15 part 2 in parallel. Peak memory of everything I ran stayed under 1 GB
(largest: 764806176 bytes, my n = 7 brute-force batch).

## Notes

- The code is pure: d(C) of the whole symplectic dual is 15, so the minimum over N \ I is the plain minimum of N.
- I did not check the table cell (d_lower = 14, d_upper = 23) or novelty; d = 15 satisfies 14 < 15 <= 23 against the
  values the claim quotes.

pass: true
