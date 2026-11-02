# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
94b9f4f822d17940b90b4aa712839b7cacdf0b6012636b885fb4f0ab509a188f u.txt (matches)
dbb972f623641fe34062aa8472a5001a0f9a8979f7e2c5aea9007368edf27a79 v.txt (matches)
831e7d2ebf430b9523457ca0832a5b4d0229ab8832af1846d6208def9e11da04 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; denominators occurring [2, 3, 4, 5, 6, 8, 11, 12, 15, 24, 44, 55, 66, 165, 264, 605, 1815]
least common denominator of each factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 554508304 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 1011985920
random exact evaluation 1 (seed 20261024): 0 of 812 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 812 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 812 entries of C differ from AB
rank-10739 scheme for <28,29,29> over Q: all Brent equations hold exactly
PASS
check 1 took 89 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; LCD per factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/812, wrong so far 0, 1s
  slab 100/812, wrong so far 0, 1s
  slab 200/812, wrong so far 0, 1s
  slab 300/812, wrong so far 0, 2s
  slab 400/812, wrong so far 0, 2s
  slab 500/812, wrong so far 0, 2s
  slab 600/812, wrong so far 0, 3s
  slab 700/812, wrong so far 0, 3s
  slab 800/812, wrong so far 0, 3s
Brent equations: 554508304 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1011985920; max slab bound 2323226025918072 (< 2^52)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
rank-10739 scheme for <28,29,29> over Q: all Brent equations hold exactly
PASS
check 2 took 6 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt plus u.part3.txt plus u.part4.txt plus u.part5.txt plus u.part6.txt, v.txt stored as v.part1.txt plus v.part2.txt plus v.part3.txt, and w.txt stored as w.part1.txt plus w.part2.txt): header lines `# factor ...`, `# format 28 29 29` and `# rank 10739`, `# convention` and a format comment, then one line per term k = 0..10738 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*29+j] A[i][j]) * (sum v_k[j*29+l] B[j][l]) for A 28x29 and B 29x29, and C[i][l] = sum_k w_k[i*29+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt object/u.part3.txt object/u.part4.txt object/u.part5.txt object/u.part6.txt > u.txt`, `cat object/v.part1.txt object/v.part2.txt object/v.part3.txt > v.txt`, `cat object/w.part1.txt object/w.part2.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/29x29x29_r11203.npz (sha256 d54f4f3c63b67dacb3504821fc30d9b5a2b83f3cd45c707683c92b0b7525d1f7), convert it, run the two slices with code/rebuild_lita_slices.py (about 2727 s wall and 4.9 GB RSS on a shared laptop for this N), export step 1, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
