# Verification Receipts

## Automated package check suite (ISO C99 + Python 3 stdlib + Core Lean 4 compiler)

The proof uses no rank or descent computation; it is the self-contained Lean file.

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Captured verbatim output:

```text
C99_VERIFIER: unified_parametrizations=1 excluded_fibrations=2 lean_theorems=12 PASS
PROVED_SUMMARY: unified_parametrizations=1 excluded_fibrations=2 lean_theorems=12 placeholder_count=0 reflection_count=0
PROVED_DEGREES: unified_edge_deg=5 unified_csq_deg=10
PROVED_FIBERS_CHECKED: total=500 family_a=250 family_b=250 min_k_a=1 min_k_b=2 perfect_cuboids_found=0
PROVED_WITNESS_A: p=101 q=100 e1=33469138819712441001 e2=666068993744360400 c_sq=11313570376135558875577698408157896183880000
PROVED_WITNESS_B: p=100 q=1 e1=2000000280000000200 e2=80007999199920000 c_sq=9997996498160289986002899815996499980001
PYTHON_VERIFIER: PASS
'PerfectCuboidDGH.no_euler_quartic_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'PerfectCuboidDGH.no_dgh_unified_square' depends on axioms: [propext, Classical.choice, Quot.sound]
'PerfectCuboidDGH.dghInternalFamilyA_infinite_positive_edge_cuboids' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
'PerfectCuboidDGH.dghInternalFamilyB_infinite_positive_edge_cuboids' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
'PerfectCuboidDGH.dghInternalFamilyA_cSq_not_square' depends on axioms: [propext, Classical.choice, Quot.sound]
'PerfectCuboidDGH.dghInternalFamilyB_cSq_not_square' depends on axioms: [propext, Classical.choice, Quot.sound]
'PerfectCuboidDGH.dghInternalFamilyA_no_scaled_perfect_cuboid' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
'PerfectCuboidDGH.dghInternalFamilyB_no_scaled_perfect_cuboid' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
'PerfectCuboidDGH.dgh_quartic_to_15a8_bridge' depends on axioms: [propext, Classical.choice, Quot.sound]
'PerfectCuboidDGH.edgh_15a8_phi_neg_obstruction' depends on axioms: [propext, Classical.choice, Quot.sound]
'PerfectCuboidDGH.edgh_15a8_phi_torsor2_mod5' depends on axioms: [propext, Classical.choice, Quot.sound]
'PerfectCuboidDGH.edgh_15a3_dual_torsors_mod16' depends on axioms: [propext, Classical.choice, Quot.sound]
PASS
```

Negative control: with one digit of `object/certificate.json` changed in a temporary copy (once in a witness decimal, once in `lean_proof_sha`), the same command prints a `*_REJECT` line and ends with `FAIL` (exit status `1`).
