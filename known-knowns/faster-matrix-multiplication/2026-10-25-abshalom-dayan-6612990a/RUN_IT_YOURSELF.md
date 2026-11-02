# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (python3, standard library; numpy for the second checker)

    sh verify-it-yourself/run_checks.sh

Expected output (real output, see verify-it-yourself/RECEIPTS.md for the date, wall time and memory):

```
6612990a836a5164f4909364a1f967014a90964ce86081f363b67c1763107fc2 u.txt (matches)
b4ff0e7c1a5cf27e75f1e5332a9521378b23da3c57e5d2a8aad1be15d63d14cc v.txt (matches)
5157c4f9f94610e1b0d3a1c2160e8358eb96261bbe03ea373cc21af6fb544e89 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <22,23,23> (A 22x23, B 23x23), 5710 terms, terms with a zero factor: 0
nonzeros u 294407, v 130320, w 118015; denominators occurring [2, 3, 4, 6, 9, 11, 12, 16, 18, 22, 36, 48, 144, 176, 352, 2816]
least common denominator of each factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 135443044 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 525533184
random exact evaluation 1 (seed 20261024): 0 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 506 entries of C differ from AB
rank-5710 scheme for <22,23,23> over Q: all Brent equations hold exactly
PASS
check 1 took 30 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <22,23,23> (A 22x23, B 23x23), 5710 terms, terms with a zero factor: 0
nonzeros u 294407, v 130320, w 118015; LCD per factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/506, wrong so far 0, 0s
  slab 100/506, wrong so far 0, 1s
  slab 200/506, wrong so far 0, 1s
  slab 300/506, wrong so far 0, 1s
  slab 400/506, wrong so far 0, 1s
  slab 500/506, wrong so far 0, 1s
Brent equations: 135443044 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 525533184; max slab bound 372537744924672 (< 2^49)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
rank-5710 scheme for <22,23,23> over Q: all Brent equations hold exactly
PASS
check 2 took 3 s
PASS
```

File format (the joined object/u.txt, object/v.txt and object/w.txt; each is stored as u.txt stored as u.part1.txt plus u.part2.txt plus u.part3.txt, v.txt, and w.txt): header lines `# factor ...`, `# format 22 23 23` and `# rank 5710`, `# convention` and a format comment, then one line per term k = 0..5709 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention: m_k = (sum u_k[i*23+j] A[i][j]) * (sum v_k[j*23+l] B[j][l]) for A 22x23 and B 23x23, and C[i][l] = sum_k w_k[i*23+l] m_k.

To join a factor by hand: for this package: `cat object/u.part1.txt object/u.part2.txt object/u.part3.txt > u.txt`, `cat object/v.txt > v.txt`, `cat object/w.txt > w.txt`.

## 2. Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/23x23x23_r6009.npz (sha256 e8741f9d13d65057c56097c65513f724ebd1b3fe007487995865d6a500a674af), convert it, run the two slices with code/rebuild_lita_slices.py (about 452 s wall and 2.0 GB RSS on a shared laptop for this N), export step 1, and compare with object/ (the compare loop prints nothing but `compared` when identical). code/slice_accounting.py replays the counting and prints how many terms each slice kills.

## 3. Negative controls (optional)

`python3 verify-it-yourself/make_negative_controls.py <joined folder> <out folder>` writes a copy with one term deleted and a copy with one coefficient changed; both checkers must print FAIL on both (RECEIPTS.md shows it).
