# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
3dbe67c0fd5688bd563efe6b78a457f6f91111868199e5e3307a3dbc3d6b8604 u.txt (matches)
75acbc4537f71d57179eb8f296fc13016f3f9cc2d58aefdc63d6026c3aa9463b v.txt (matches)
d9fdcfe51666bc6023b62f4bcb158d34ad74b1710a15e6f0e2f3e69b8c87df95 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <20,21,21> (A 20x21, B 21x21), 4471 terms, terms with a zero factor: 0
nonzeros u 211890, v 98908, w 89223; denominators occurring [2, 4, 7, 8, 14, 16, 29, 56, 112, 203, 1421]
least common denominator of each factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 77792400 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 285200384
random exact evaluation 1 (seed 20261024): 0 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 420 entries of C differ from AB
rank-4471 scheme for <20,21,21> over Q: all Brent equations hold exactly
PASS
check 1 took 18 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <20,21,21> (A 20x21, B 21x21), 4471 terms, terms with a zero factor: 0
nonzeros u 211890, v 98908, w 89223; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/420, wrong so far 0, 0s
  slab 100/420, wrong so far 0, 0s
  slab 200/420, wrong so far 0, 0s
  slab 300/420, wrong so far 0, 1s
  slab 400/420, wrong so far 0, 1s
Brent equations: 77792400 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 285200384; max slab bound 124678617281232 (< 2^47)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
rank-4471 scheme for <20,21,21> over Q: all Brent equations hold exactly
PASS
check 2 took 2 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt, v.txt, and w.txt): header lines `# factor ...`, `# format 20 21 21` and `# rank 4471`, `# convention` and a format comment, then one line per term k = 0..4470 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*21+j] A[i][j]) * (sum v_k[j*21+l] B[j][l]) for A 20x21 and B 21x21, and C[i][l] = sum_k w_k[i*21+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt > u.txt`, `cat object/v.txt > v.txt`, `cat object/w.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/21x21x21_r4723.npz (sha256 9d8389744035a57e63a5eb13cd766ddbd695e2bc71e6b25f9ce5eacdbd0d6397), convert it, run the two slices with code/rebuild_lita_slices.py (about 244 s wall and 1.2 GB RSS on a shared laptop for this N), export step 1, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
