# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
1d6c9f89e17717b7236f9bbbf46d6903e95f66a3965445cd8194bc23bd065d58 u.txt (matches)
bdcfa626ff98644b132c75ac00deebb2b9cb922116b7b44e00e63d2238f5da5a v.txt (matches)
9192310639d1141ba525574fac6735b5ce0507711ac0c8989a1f049b221aa48e w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <26,26,27> (A 26x26, B 26x27), 8437 terms, terms with a zero factor: 0
nonzeros u 352891, v 522808, w 190241; denominators occurring [2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400]
least common denominator of each factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 333135504 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 8731360000
random exact evaluation 1 (seed 20261024): 0 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 702 entries of C differ from AB
rank-8437 scheme for <26,26,27> over Q: all Brent equations hold exactly
PASS
check 1 took 115 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <26,26,27> (A 26x26, B 26x27), 8437 terms, terms with a zero factor: 0
nonzeros u 352891, v 522808, w 190241; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/676, wrong so far 0, 1s
  slab 100/676, wrong so far 0, 1s
  slab 200/676, wrong so far 0, 1s
  slab 300/676, wrong so far 0, 1s
  slab 400/676, wrong so far 0, 1s
  slab 500/676, wrong so far 0, 1s
  slab 600/676, wrong so far 0, 2s
Brent equations: 333135504 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 49600548524296000 (< 2^56)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
rank-8437 scheme for <26,26,27> over Q: all Brent equations hold exactly
PASS
check 2 took 5 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt plus u.part3.txt, v.txt stored as v.part1.txt plus v.part2.txt plus v.part3.txt plus v.part4.txt, and w.txt stored as w.part1.txt plus w.part2.txt): header lines `# factor ...`, `# format 26 26 27` and `# rank 8437`, `# convention` and a format comment, then one line per term k = 0..8436 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*26+j] A[i][j]) * (sum v_k[j*27+l] B[j][l]) for A 26x26 and B 26x27, and C[i][l] = sum_k w_k[i*27+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt object/u.part3.txt > u.txt`, `cat object/v.part1.txt object/v.part2.txt object/v.part3.txt object/v.part4.txt > v.txt`, `cat object/w.part1.txt object/w.part2.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/27x27x27_r9233.npz (sha256 f62e6272e1fbcfcb02b57b8ffc7afc1896143e22f707e5f1791d9a6174a1132d), convert it, run the two slices with code/rebuild_lita_slices.py (about 1653 s wall and 2.4 GB RSS on a shared laptop for this N), export step 2, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
