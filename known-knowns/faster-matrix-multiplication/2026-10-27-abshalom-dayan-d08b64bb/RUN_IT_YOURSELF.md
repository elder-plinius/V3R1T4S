# Run it yourself

From this folder, in a fresh shell, with only python3 (standard library):

    sh verify-it-yourself/run_checks.sh

Expected output (seconds on a laptop; verify-it-yourself/RECEIPTS.md has the real run):

    == exact Brent-equation check (check_scheme.py)
    format <12,13,13>, 1270 terms, every term with three nonzero factors, common denominator 59904, 4112784 Brent equations checked, 0 wrong
    rank 1270 scheme for <12,13,13> over Q verified exactly
    PASS
    == random exact evaluation against AB (check_random_eval.py)
    trial 1: 0 of 156 entries of C differ from AB
    trial 2: 0 of 156 entries of C differ from AB
    trial 3: 0 of 156 entries of C differ from AB
    PASS
    PASS

File format (object/u.txt, v.txt, w.txt): header lines `# format 12 13 13` and `# rank 1270`, then one line per term
k = 0..1269 listing the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention:
m_k = (sum u_k[i*13+j] A[i][j]) * (sum v_k[j*13+l] B[j][l]) for A 12x13, B 13x13, and C[i][l] = sum_k w_k[i*13+l] m_k.
Coefficients are rationals; 59904 is the common denominator the checker uses (the least common denominator of the
coefficients is 3744).

sha256:

    d08b64bbd70b1059b87528ba8e988f57a7f20293d181168a2083380b810d4690  object/u.txt
    a1c142447b30847fe70f7f0dc7aa638665c313efdab236f9ede41b10c04eadaf  object/v.txt
    8180074e608df407ce136e21ed42797fb7071b28691182e034dab6bb84feaf58  object/w.txt

To rebuild the object from LITA's published 13x13x13 rank-1379 scheme (needs numpy and python-flint 0.9.0), follow
how-we-built-it/COMMANDS.md: about 7 s, ends with `identical`.
