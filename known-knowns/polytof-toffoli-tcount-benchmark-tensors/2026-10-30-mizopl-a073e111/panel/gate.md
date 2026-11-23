status: CONFIRMED_PARTIAL
claim_type: partial_win
partial_win: p2
partial_id: p2
target_id: polytof-toffoli-tcount-benchmark-tensors
reproduce_pass: true
novelty_pass: true
criterion_pass: true
confirmed_scope: Confirmed partial win p2 on polytof-toffoli-tcount-benchmark-tensors for single table row 0725 (GF(2^2) multiplication, n=6, nnz=5, indexed in object/p2_0725_optimality_certificate.json sha256 a073e111c38831bfba3839a47b5bb9a0f2cc2abde8aa9572ee7a528e241dbc8a and recomputed from scratch in 0.21s by verify-it-yourself/verify.py against ZIB-IOL/polytof pinned commit 0dcac107d15adc34dc646242d222f21ae7d32699): (1) certified CP = 3 optimality (CP <= 2 impossible) via exterior-wedge reduction Sym_6(u x v x w) = u ^ v ^ w mod 2 and exhaustive Grassmannian Gr(3, F_2^6) enumeration over all 1,395 3-dimensional subspaces (0/1,395 at R=1, 0/972,315 unordered pairs at R=2, and 120 canonical unordered subspace triples at R=3 including posted 0725-00003.npy) plus exhaustive bilinear check on 0525-00003.npy (0/9 at R=1, 0/36 at R=2, 3/84 at R=3); and (2) certified Waring = 17 optimality (Waring <= 16 impossible) via punctured Reed-Muller RM(3,6)* / RM(2,6)* coset reduction (41 signature equations over 63 nonzero linear forms, rank(H) = 41, dim ker(H) = 22) and exhaustive evaluation of all 2^22 = 4,194,304 valid Waring decompositions in the affine coset e_0 + ker(H) (0/4,194,304 at weight <= 16, and 1,008 optimal weight-17 decompositions including posted 0725-00017.npy).
