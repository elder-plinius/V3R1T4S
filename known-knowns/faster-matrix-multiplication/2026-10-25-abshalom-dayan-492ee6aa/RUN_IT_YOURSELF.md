# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
492ee6aa98869d87672300fc6bad94738cb8e7905650066d316e3903be92c5be u.txt (matches)
3d78b1a87e5450ac44a77c22aa1b9c406a20c833d804b9f27f044291b98864c4 v.txt (matches)
477a6d278146507c1324b04d8dcd299dc3a92d365d669c0a98dc20e1515f3c00 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <22,22,23> (A 22x22, B 22x23), 5423 terms, terms with a zero factor: 0
nonzeros u 200399, v 290632, w 116087; denominators occurring [2, 3, 4, 6, 9, 11, 12, 16, 18, 22, 36, 48, 144, 176, 352, 2816]
least common denominator of each factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 123921424 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 525533184
random exact evaluation 1 (seed 20261024): 0 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 506 entries of C differ from AB
rank-5423 scheme for <22,22,23> over Q: all Brent equations hold exactly
PASS
check 1 took 43 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <22,22,23> (A 22x22, B 22x23), 5423 terms, terms with a zero factor: 0
nonzeros u 200399, v 290632, w 116087; LCD per factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/484, wrong so far 0, 0s
  slab 100/484, wrong so far 0, 1s
  slab 200/484, wrong so far 0, 1s
  slab 300/484, wrong so far 0, 1s
  slab 400/484, wrong so far 0, 1s
Brent equations: 123921424 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 525533184; max slab bound 1122372292091904 (< 2^50)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
rank-5423 scheme for <22,22,23> over Q: all Brent equations hold exactly
PASS
check 2 took 2 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt, v.txt stored as v.part1.txt plus v.part2.txt plus v.part3.txt, and w.txt): header lines `# factor ...`, `# format 22 22 23` and `# rank 5423`, `# convention` and a format comment, then one line per term k = 0..5422 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*22+j] A[i][j]) * (sum v_k[j*23+l] B[j][l]) for A 22x22 and B 22x23, and C[i][l] = sum_k w_k[i*23+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt > u.txt`, `cat object/v.part1.txt object/v.part2.txt object/v.part3.txt > v.txt`, `cat object/w.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/23x23x23_r6009.npz (sha256 e8741f9d13d65057c56097c65513f724ebd1b3fe007487995865d6a500a674af), convert it, run the two slices with code/rebuild_lita_slices.py (about 452 s wall and 2.0 GB RSS on a shared laptop for this N), export step 2, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
