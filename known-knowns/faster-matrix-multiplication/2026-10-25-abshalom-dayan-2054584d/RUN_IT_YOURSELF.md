# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
2054584dc35faa7426d99b2406acb3ea68e7798e12579b1b3d729c65c16cf044 u.txt (matches)
0e8f860801dba7fe48e4828b8611d178741433b3f4e13b195c18500face0ac10 v.txt (matches)
fb6a185d56543f959eda3385e43a469d5d698507fef0c8578f6ada96456c080a w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <24,24,25> (A 24x24, B 24x25), 6820 terms, terms with a zero factor: 0
nonzeros u 268829, v 394150, w 150124; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 90, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 207360000 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 1942056000
random exact evaluation 1 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 600 entries of C differ from AB
rank-6820 scheme for <24,24,25> over Q: all Brent equations hold exactly
PASS
check 1 took 75 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <24,24,25> (A 24x24, B 24x25), 6820 terms, terms with a zero factor: 0
nonzeros u 268829, v 394150, w 150124; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/576, wrong so far 0, 0s
  slab 100/576, wrong so far 0, 1s
  slab 200/576, wrong so far 0, 1s
  slab 300/576, wrong so far 0, 1s
  slab 400/576, wrong so far 0, 1s
  slab 500/576, wrong so far 0, 1s
Brent equations: 207360000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 6929223523914240 (< 2^53)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
rank-6820 scheme for <24,24,25> over Q: all Brent equations hold exactly
PASS
check 2 took 3 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt, v.txt stored as v.part1.txt plus v.part2.txt plus v.part3.txt, and w.txt stored as w.part1.txt plus w.part2.txt): header lines `# factor ...`, `# format 24 24 25` and `# rank 6820`, `# convention` and a format comment, then one line per term k = 0..6819 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*24+j] A[i][j]) * (sum v_k[j*25+l] B[j][l]) for A 24x24 and B 24x25, and C[i][l] = sum_k w_k[i*25+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt > u.txt`, `cat object/v.part1.txt object/v.part2.txt object/v.part3.txt > v.txt`, `cat object/w.part1.txt object/w.part2.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/25x25x25_r7507.npz (sha256 32b251e6933c6652dbbd5ac3037d5afea859c879b2d71c0c1433cadd5e1d5613), convert it, run the two slices with code/rebuild_lita_slices.py (about 922 s wall and 2.2 GB RSS on a shared laptop for this N), export step 2, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
