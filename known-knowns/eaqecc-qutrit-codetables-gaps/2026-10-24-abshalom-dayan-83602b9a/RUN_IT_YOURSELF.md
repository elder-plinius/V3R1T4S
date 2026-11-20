# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc):

    sh verify-it-yourself/run_checks.sh

Expected output (about 1 minute on a laptop with 3 free cores, about 2 CPU-minutes):

    {"n": 28, "s": 34, "c": 11, "k": 5, "dim_perp": 22, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    d=15 count=26676 enumerated=10460353203
    d=15 count=22302 enumerated=10460353203
    d=15 count=22302 enumerated=10460353203
    computed n=28 k=5 c=11 d=15 (71280 words of weight d; enumerated 31381059609 vectors, 3^22 = 31381059609); claimed n=28 k=5 c=11 d=15
    D9 Hermitian-orthogonal to G9: True; rowspace(S) = phi(D9): True
    PASS

What it does: check_eaqecc.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis
of span(S)^perp with the isotropic part span(S) ∩ span(S)^perp first, and checks the GF(9) description (D9 ⊥_H G9,
rowspace(S) = phi(D9)); enum_min.c visits every one of the 3^22 vectors of span(S)^perp once (ternary Gray code)
and takes the minimum symplectic weight over those outside the isotropic part.

Rebuild the object from scratch: see how-we-built-it/README.md (`python3 how-we-built-it/build_claim.py 13
rebuilt.json 15` gives a byte-identical file).
