# Repair round 1 (kit/RUN.md step 5: FLAWED with a repair hint, budget allows one repair round)

Found by the round-1 REPRODUCE skeptic (panel/round1/reproduce.md): attempts/leakage-knn/code/p2_knn.py computed the
fraction of negatives scoring at or above a candidate threshold as `1.0 - searchsorted(...)/len(neg)`, which gives
0.05000000000000004 instead of 0.05 when exactly 5% of negatives are at or above it, so the frozen "<= 0.05" rule of
PREREG.md acted as "< 0.05" at that boundary. The skeptic found the sensitivity changes in one control only (seed 333:
0.584375 written, 0.5875 by the frozen definition); the split-v2 value is not at the boundary.

Fix (no rule change; the code now implements PREREG.md's rule exactly): count the negatives with score >= t as an
integer and test 20 * count <= number of negatives. Same fix in export_p2_artifacts.py. Nothing else changed:
same model, drug, filter, metric, seeds, splits and pass rule. The full ETH run (400 random + 100 alternative splits)
was re-run with the fixed code in this folder, and the claim package (claim/) was rebuilt from these outputs.
