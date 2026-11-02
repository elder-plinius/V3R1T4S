# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
528be0ed8aa1904d71bc1f59da284b0e3d9f66f4a2e01f01940bcb1ce1c0fb8c u.txt (matches)
da65b90d20b3a1589689d228a71b57910e80d6996174e64f39a848411b020bae v.txt (matches)
c53a02a35df88172c1cb9333c6763d2af9b016609d484d075b6e56bbc54c78aa w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; denominators occurring [2, 4, 7, 13, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 778410000 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 35716681728
random exact evaluation 1 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 930 entries of C differ from AB
rank-12395 scheme for <30,30,31> over Q: all Brent equations hold exactly
PASS
check 1 took 219 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/900, wrong so far 0, 1s
  slab 100/900, wrong so far 0, 1s
  slab 200/900, wrong so far 0, 2s
  slab 300/900, wrong so far 0, 2s
  slab 400/900, wrong so far 0, 3s
  slab 500/900, wrong so far 0, 4s
  slab 600/900, wrong so far 0, 4s
  slab 700/900, wrong so far 0, 5s
  slab 800/900, wrong so far 0, 5s
Brent equations: 778410000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 459266248437295104 (< 2^59)
exact Python-integer path used for 174 term-slab pairs (single contribution >= 2^53) in 29 of 900 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12395 scheme for <30,30,31> over Q: all Brent equations hold exactly
PASS
check 2 took 10 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt plus u.part3.txt plus u.part4.txt plus u.part5.txt, v.txt stored as v.part1.txt plus v.part2.txt plus v.part3.txt plus v.part4.txt plus v.part5.txt plus v.part6.txt plus v.part7.txt, and w.txt stored as w.part1.txt plus w.part2.txt plus w.part3.txt): header lines `# factor ...`, `# format 30 30 31` and `# rank 12395`, `# convention` and a format comment, then one line per term k = 0..12394 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*30+j] A[i][j]) * (sum v_k[j*31+l] B[j][l]) for A 30x30 and B 30x31, and C[i][l] = sum_k w_k[i*31+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt object/u.part3.txt object/u.part4.txt object/u.part5.txt > u.txt`, `cat object/v.part1.txt object/v.part2.txt object/v.part3.txt object/v.part4.txt object/v.part5.txt object/v.part6.txt object/v.part7.txt > v.txt`, `cat object/w.part1.txt object/w.part2.txt object/w.part3.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/31x31x31_r13433.npz (sha256 9effecdc238c8425993e7d73e3cefd45a40e67cd3cc08caf2825493f884e7955), convert it, run the two slices with code/rebuild_lita_slices.py (about 5165 s wall and 5.5 GB RSS on a shared laptop for this N), export step 2, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
