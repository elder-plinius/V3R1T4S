# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
1570401161925e32961aa2ad3cb58ac6c66b38b3e804fac3e9d7a195405da245 u.txt (matches)
ccae23a2fc6350bf299bfbf6b5df8ebab898741535a56a983e2285f681efcb3d v.txt (matches)
cfb52c03a37acf0d7c85b66db919ec6dcd32ef47203ac183c59a577426eabb42 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; denominators occurring [2, 4, 7, 13, 14, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 831168900 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 35716681728
random exact evaluation 1 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 930 entries of C differ from AB
rank-12906 scheme for <30,31,31> over Q: all Brent equations hold exactly
PASS
check 1 took 148 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/930, wrong so far 0, 1s
  slab 100/930, wrong so far 0, 1s
  slab 200/930, wrong so far 0, 2s
  slab 300/930, wrong so far 0, 2s
  slab 400/930, wrong so far 0, 2s
  slab 500/930, wrong so far 0, 3s
  slab 600/930, wrong so far 0, 4s
  slab 700/930, wrong so far 0, 4s
  slab 800/930, wrong so far 0, 5s
  slab 900/930, wrong so far 0, 5s
Brent equations: 831168900 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 113569216608466944 (< 2^57)
exact Python-integer path used for 178 term-slab pairs (single contribution >= 2^53) in 30 of 930 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12906 scheme for <30,31,31> over Q: all Brent equations hold exactly
PASS
check 2 took 10 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt plus u.part3.txt plus u.part4.txt plus u.part5.txt plus u.part6.txt plus u.part7.txt, v.txt stored as v.part1.txt plus v.part2.txt plus v.part3.txt, and w.txt stored as w.part1.txt plus w.part2.txt plus w.part3.txt): header lines `# factor ...`, `# format 30 31 31` and `# rank 12906`, `# convention` and a format comment, then one line per term k = 0..12905 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*31+j] A[i][j]) * (sum v_k[j*31+l] B[j][l]) for A 30x31 and B 31x31, and C[i][l] = sum_k w_k[i*31+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt object/u.part3.txt object/u.part4.txt object/u.part5.txt object/u.part6.txt object/u.part7.txt > u.txt`, `cat object/v.part1.txt object/v.part2.txt object/v.part3.txt > v.txt`, `cat object/w.part1.txt object/w.part2.txt object/w.part3.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/31x31x31_r13433.npz (sha256 9effecdc238c8425993e7d73e3cefd45a40e67cd3cc08caf2825493f884e7955), convert it, run the two slices with code/rebuild_lita_slices.py (about 5165 s wall and 5.5 GB RSS on a shared laptop for this N), export step 1, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
