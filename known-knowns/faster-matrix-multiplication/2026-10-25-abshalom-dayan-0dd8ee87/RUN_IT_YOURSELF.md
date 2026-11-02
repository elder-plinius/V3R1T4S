# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
0dd8ee872815374dbea1c5ad46d2fa3d66b5513d5daf7e3deb924a7d11e146dc u.txt (matches)
2fa3c110aee729212f67c643abcb3ea16e7ace02aa005b5ea9078c9ebc8455dd v.txt (matches)
23207f290da58bb771cd3a713cf030e3916bb262c1fbd5db863eb04af2b7f42c w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <24,25,25> (A 24x25, B 25x25), 7157 terms, terms with a zero factor: 0
nonzeros u 398652, v 167772, w 152419; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 225000000 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 1942056000
random exact evaluation 1 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 600 entries of C differ from AB
rank-7157 scheme for <24,25,25> over Q: all Brent equations hold exactly
PASS
check 1 took 47 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <24,25,25> (A 24x25, B 25x25), 7157 terms, terms with a zero factor: 0
nonzeros u 398652, v 167772, w 152419; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/600, wrong so far 0, 0s
  slab 100/600, wrong so far 0, 1s
  slab 200/600, wrong so far 0, 1s
  slab 300/600, wrong so far 0, 1s
  slab 400/600, wrong so far 0, 1s
  slab 500/600, wrong so far 0, 1s
Brent equations: 225000000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 2118902173790580 (< 2^51)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
rank-7157 scheme for <24,25,25> over Q: all Brent equations hold exactly
PASS
check 2 took 3 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt plus u.part3.txt, v.txt stored as v.part1.txt plus v.part2.txt, and w.txt stored as w.part1.txt plus w.part2.txt): header lines `# factor ...`, `# format 24 25 25` and `# rank 7157`, `# convention` and a format comment, then one line per term k = 0..7156 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*25+j] A[i][j]) * (sum v_k[j*25+l] B[j][l]) for A 24x25 and B 25x25, and C[i][l] = sum_k w_k[i*25+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt object/u.part3.txt > u.txt`, `cat object/v.part1.txt object/v.part2.txt > v.txt`, `cat object/w.part1.txt object/w.part2.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/25x25x25_r7507.npz (sha256 32b251e6933c6652dbbd5ac3037d5afea859c879b2d71c0c1433cadd5e1d5613), convert it, run the two slices with code/rebuild_lita_slices.py (about 922 s wall and 2.2 GB RSS on a shared laptop for this N), export step 1, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
