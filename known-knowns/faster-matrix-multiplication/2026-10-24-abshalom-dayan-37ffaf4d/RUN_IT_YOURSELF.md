# Run it yourself

All commands run from this folder in a fresh shell.

## Check the object (python3, standard library only, no network)

    sh verify-it-yourself/run_checks.sh

Expected output (real output from 2026-10-24T19:15:13Z, 74 s on a laptop):

```
37ffaf4dc24686ccb944605fd965f8b981088a74cf5246a54d6bcf5a2b665eca u.txt (matches)
5d15717baf763e44e9fb2808ff92335e66ec76f0940c0f75839a79a33ea4c5be v.txt (matches)
0f0a3d5cffe4ba63b5aa9a464c87abe0c17a501028c2d7f0d02cc128ea4fd93a w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py)
format <18,18,19> (A 18x18, B 18x19), 3225 terms, terms with a zero factor: 0
nonzeros u 102579, v 145368, w 64253; denominators occurring [2, 4, 5, 7, 10, 12, 14, 25, 28, 50, 84, 300, 600, 1200]
least common denominator of each factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 37896336 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 59270400
random exact evaluation 1 (seed 20261024): 0 of 342 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 342 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 342 entries of C differ from AB
rank-3225 scheme for <18,18,19> over Q: all Brent equations hold exactly
PASS
== check 2: second exact Brent-equation checker (check_scheme_second.py)
format <18,18,19>, 3225 terms, every term with three nonzero factors, common denominator 352800, 37896336 Brent equations checked, 0 wrong
rank 3225 scheme for <18,18,19> over Q verified exactly
PASS
PASS
```

File format (object/u.txt, object/v.txt = object/v.part1.txt followed by object/v.part2.txt, object/w.txt): header
lines `# format 18 18 19` and `# rank 3225`, then one line per term k = 0..3224 with the nonzero entries
`index:coefficient` (integer or p/q) of that term's factor. Convention:
m_k = (sum u_k[i*18+j] A[i][j]) * (sum v_k[j*19+l] B[j][l]) for A 18x18 and B 18x19, and
C[i][l] = sum_k w_k[i*19+l] m_k.

"common denominator 352800" in check 2's output is that checker's scaling factor; the least common denominators
are U 8400, V 84 and W 84.

To join v.txt by hand: `cat object/v.part1.txt object/v.part2.txt > v.txt`.

## Rebuild the object (optional; numpy 2.5.4 and python-flint 0.9.0, network for one download)

how-we-built-it/COMMANDS.md: download LITA's schemes/19x19x19_r3633.npz (sha256
72633df65c1da7195d1a3284845cf82bf70c5e11c969895a33b7167bd978889b), convert it, run the two slices with
code/rebuild_lita_slices.py (about 2.5 minutes, under 0.7 GB), export, and compare with object/ (prints SAME).
code/drop_accounting.py replays the two steps and prints how many terms each slice kills.

The rebuild code is the same code PR #708 published in its how-we-built-it/ (see README.md, "Not claimed").
