# CHANGES to this claim package

## 2026-10-20 (after the first panel; claim sentence and all numbers unchanged)
- METHOD.md section 2: the SKETCH for lant4's certificate C(s) is replaced by a full, self-contained proof (PROVED-HERE, modelled on section 1: E_k for all k, telescoping to D_k, period lemma, induction on periods). The argument was also checked by a panel reviewer.
- METHOD.md section 2: corrected a factual error. The old text said checkC compares the grid "at the detection step t". In fact lant_run rewinds the grid to time s before calling checkC(s), so the comparison uses G_s; only the bounding box is taken at step t (which only makes the check longer).
- METHOD.md section 2 remark: the list of where lant's and lantx2's T_cap agree now separates per-mask comparisons from the full-chunk and sample-unit consistency checks.
- CLAIM.md, "What is NOT claimed": the bullet saying C(s) is only sketched now says both certificates have full proofs in METHOD.md.
- Added this file.
