context: subagent (Claude Sonnet 5.5, fresh context, given only a copy of claim/)

# Reproduce report: <14,14,15> rank 1709 over Q

## Definition used (written before reading any author code)

Matrix multiplication <n,m,p>: C = A B with A n x m, B m x p, C[i][l] = sum_j A[i][j] B[j][l]. The matrix multiplication tensor is
T = sum_{i,j,l} a_{ij} (x) b_{jl} (x) c_{il}. A rank-r bilinear scheme is r triples (u_t, v_t, w_t) with
m_t = (u_t . vec A)(v_t . vec B) and C[i][l] = sum_t w_t[i*p+l] m_t. Index convention (stated in the object file headers and
CLAIM/REPRODUCE.md, and re-derived by me): u index a = i*m+j, v index c = j*p+l, w index e = i*p+l. Brent equations: for every
a=(i,j) in n*m, c=(j',l) in m*p, e=(i',l') in n*p,
  sum_t u_t[a] v_t[c] w_t[e] = [i == i'] [j == j'] [l == l'].
For <14,14,15>: 196 * 210 * 210 = 8,643,600 equations, of which 14*14*15 = 2940 have right-hand side 1 and the rest 0.

## What I checked, and how

- sha256 of object/u.txt, v.txt, w.txt: all three equal the values in CLAIM.md/REPRODUCE.md (recomputed with shasum -a 256).
- Each file has 5 header lines plus exactly 1709 term lines; headers say format 14 14 15, rank 1709. My parser raised on any
  count mismatch, duplicate index or out-of-range index; none occurred.
- Number of terms: exactly 1709 in each of u, v, w. Zero factors: 0 in u, 0 in v, 0 in w (every term has three nonzero factors).
  nnz: u 220889, v 166143, w 35817.
- My own checker (standard-library Python, run with -I, work/mycheck.py, not part of claim/): parses coefficients with
  fractions.Fraction (exact), scales each term to an integer triple with a per-term denominator, multiplies each term by
  LCD/denominator (global scale LCD has 7 digits; equal to the 2121600 the author prints), accumulates exact Python integers for
  every (u index, v index, w index) triple, and compares ALL 8,643,600 entries with L * [target] (entries not produced by any term
  must be 0). Not a sample. No floats are used.
- Checker validation before the real run: Strassen <2,2,2> rank 7 (my own transcription): 64 equations, 0 wrong; Strassen with
  one w coefficient changed: 2 wrong (rejected); a fractional-coefficient naive <2,3,2> rank-12 scheme: 144 equations, 0 wrong,
  and a corrupted copy of it rejected.
- Corrupted real object (w.txt, term 100, first coefficient -1 changed to 0, other files unchanged): my checker reports
  8,643,600 equations, 2968 wrong, FAIL (rejected, as it must).
- Real object: 8,643,600 equations checked, 0 wrong, 1709 terms. RESULT PASS.
- Resources: real-object run 83.5 s wall (single process, nice -n 10), peak RSS 114 MB. The corrupted run ran in parallel
  (2 processes in total): 83 s, 115 MB.
- Determinism: my checker and the author's checker are deterministic code (no randomness); two independent implementations
  gave the same 0-wrong verdict on the same bytes. I did not run my checker twice; the author's checker and mine each ran once and agreed.

## Result vs the claim

Claim: the object is an exact rank-1709 scheme for <14,14,15> over Q. My result: confirmed, 0 of 8,643,600 Brent equations
violated, exactly 1709 terms, no zero factors, sha256 match. The denominator set I extracted from the files equals the list in
CLAIM.md (plus denominator 1 for integers). Not checked by me: the comparison of 1709 to the four external tables (1789, 1798,
1790, 1798, none for Merlijn) and TABLE_RECORD.md, since no network is allowed and those are external fetches; I do not
vouch for those numbers. Provenance ("derived from the LITA 15x15x15 r1977 scheme") is not needed for the validity of the
object and was not independently verified.

## Author's results (run in a copy of claim/, sh verify-it-yourself/run_checks.sh)

check_scheme.py: "format <14,14,15>, 1709 terms, every term with three nonzero factors, common denominator 2121600,
8643600 Brent equations checked, 0 wrong ... verified exactly ... PASS". check_random_eval.py: 3 trials, 0 of 210 entries of C
differ from AB each, PASS. Overall PASS. Wall 337 s, peak RSS 1.2 GB (slower than the "about 4 minutes" stated while the
machine was shared; output otherwise identical to the expected output in REPRODUCE.md).

Rebuild (claim/rebuild/, optional): NOT run. rebuild/engine.py imports python-flint, which is not installed here
(ModuleNotFoundError: flint) and I was told to install nothing. I did confirm the sha256 of rebuild/15x15x15_r1977.npz equals
94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33 as stated. The rebuild is not needed for the verdict,
which rests on the saved object.

## Mismatches

None found in the object or in the author's printed results.
The only gap: the rebuild step could not be executed (missing python-flint).

pass: true
