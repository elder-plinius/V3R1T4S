# Commands (python-flint 0.9.0, sympy 1.14.0)
    python3 lemmas.py                                    # symbolic lemmas, all True
    nice python3 certify.py 2 55 0 448 96 384 72         # the certificate (about 20 min)
Arguments: ROW, box half-width exponent, vx shift, centre precision bits, centre Taylor order, box precision bits, box
Taylor order. PROOF.md explains each check; PREREG.md, PREREG.v2.md, PREREG.v3.md are the frozen rules (v2 fixed C2,
v3 added the reduced-monodromy route C3', both before any certificate was scored).
