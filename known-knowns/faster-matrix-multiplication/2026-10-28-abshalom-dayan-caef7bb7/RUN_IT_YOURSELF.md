# Run it yourself

From this folder, in a fresh shell, with only python3 (standard library):

    sh verify-it-yourself/run_checks.sh

Expected output (about 10 s on a laptop; verify-it-yourself/RECEIPTS.md has the real run):

    == exact Brent-equation check (check_scheme.py)
    format <14,15,13>, 1644 terms, every term with three nonzero factors, common denominator 54400, 7452900 Brent equations checked, 0 wrong
    rank 1644 scheme for <14,15,13> over Q verified exactly
    PASS
    == random exact evaluation against AB (check_random_eval.py)
    trial 1: 0 of 182 entries of C differ from AB
    trial 2: 0 of 182 entries of C differ from AB
    trial 3: 0 of 182 entries of C differ from AB
    PASS
    PASS

File format (object/u.txt, v.txt, w.txt): header lines `# format 14 15 13` and `# rank 1644`, then one line per term
k = 0..1643 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention:
m_k = (sum u_k[i*15+j] A[i][j]) * (sum v_k[j*13+l] B[j][l]) for A 14x15, B 15x13, and C[i][l] = sum_k w_k[i*13+l] m_k.
For the sorted format <13,14,15>, rotate the factors cyclically: A'[l][i] = w-factor entry (i,l), B' = the u factor,
C'[l][j] = v-factor entry (j,l); the term count is unchanged.

sha256 of the object files:

    caef7bb7a2974dc44dee7feb61779a52d00b0473b7b416069c7f0e0d11d7e8cd  object/u.txt
    b31e5e77899a5ec44a8922eb49963ccc8babf8e84368a47b2c92d89dd9aa6616  object/v.txt
    79b90daf911f392ccde5cf5abed5400b207ed04980ad392d7c4c9028d20a7da1  object/w.txt

To rebuild the object from LITA's published scheme (needs numpy and python-flint), see how-we-built-it/COMMANDS.md.
