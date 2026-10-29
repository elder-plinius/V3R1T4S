# Run it yourself

From this folder, in a fresh shell, with only python3 (standard library):

    sh verify-it-yourself/run_checks.sh

Expected output (seconds on a laptop; verify-it-yourself/RECEIPTS.md has the real run):

    == exact Brent-equation check (check_scheme.py)
    format <14,15,15>, 1836 terms, every term with three nonzero factors, common denominator 54400, 9922500 Brent equations checked, 0 wrong
    rank 1836 scheme for <14,15,15> over Q verified exactly
    PASS
    == random exact evaluation against AB (check_random_eval.py)
    trial 1: 0 of 210 entries of C differ from AB
    trial 2: 0 of 210 entries of C differ from AB
    trial 3: 0 of 210 entries of C differ from AB
    PASS
    PASS

File format (object/u.txt, v.txt, w.txt): header lines `# format 14 15 15` and `# rank 1836`, then one line per term
k = 0..1835 listing the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention:
m_k = (sum u_k[i*15+j] A[i][j]) * (sum v_k[j*15+l] B[j][l]) for A 14x15, B 15x15, and C[i][l] = sum_k w_k[i*15+l] m_k.
Coefficients are rationals; 54400 is the common denominator the checker uses (the least common denominator of the
coefficients is 5440).

sha256:

    74ccb3a6e497169b251b66cdfa494fd9b9c953105339c8e76b50f36f88c54a09  object/u.txt
    0f86e47a9d787227caa9dbdfcdf5acd1f8694ab0d770fc9206f3df36658471ae  object/v.txt
    cac452b54850e243944c0b26e24ea5c41b170e25976d418d2578941e506224b8  object/w.txt

To rebuild the object from LITA's published 15x15x15 rank-1977 scheme (needs numpy and python-flint 0.9.0), follow
how-we-built-it/COMMANDS.md: about 15 s, ends with `identical`.
