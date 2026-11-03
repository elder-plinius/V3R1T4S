# How we found it (contributor text, unverified)

Target: llrl-ant-minimal-seed (Langton’s ant LLRL, H384 onset g(k)).
Claim: g(6) = 139 with unique minimiser under the fixed frame
(ant at origin facing north, y down): cells (0,1,3)(0,2,2)(1,2,3)(1,4,3)(2,1,3)(3,0,1).

Method (two independent exhaustive searches + certificate):

1. Checker A (hsearch, first-read DFS). Home machine ran 84 pieces at TMAX=140;
   the merged result is unique onset 139. Box scout pieces at TMAX=174 returned
   NONE / best ≥ 173, so no onset-139 seed exists above the home TMAX either.
2. Checker B (lcb_fast, light-cone). Full partition into 400 pieces at T=139
   (LCB_SPLITD=60). Merged: 5_011_329_083 leaves, 0 VIOLATION, 1 MIN — the same
   unique seed. Digests A=bc8fc1f6719817ee, B=cbd7913df3b309c1.
3. Checker C: ccheck/ant plus an independent Python simulator (sim_llrl.py) with
   no shared code. Both certify onset 139 for the seed; blank 256241 and the
   k=5 seed 174 also match.

Panel: criterion, novelty, reproduce all pass:true; an extra reproduce2 skeptic
re-ran all 400 B pieces byte-identical and spot-checked A. Gate: CONFIRMED_PARTIAL
with confirmed_scope covering g(6)=139 unique + A/B exhaustiveness + C certificate.
