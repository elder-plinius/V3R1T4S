# Novelty Report — `qoblib-portfolio-ten-assets-exact`

- Context: Status table and literature review for QOBLIB portfolio instance `po_a010_t10_orig_b004_l1e-03`
- Target ID: `qoblib-portfolio-ten-assets-exact`

## Novelty & Prior Art Audit

1. **Status Source Verification**:
   - Source table: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md` (SHA-256 `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`).
   - Instance `po_a010_t10_orig_b004_l1e-03` lists incumbent objective `-8397` (`best known`) from Maximilian Schicker (`2025-08-19`, `06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`, SHA-256 `d0cb3e4a86d01ac2b2884e3275df8219bb1d38dae908830784417b0d4e4b30ea`).
   - The reported bound in the 2025-08-19 submission (`06-portfolio/submissions/20250819_MIP_Schicker/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3/README.md`) is Gurobi's numerical MIP bound of `-15342.65126758` after `3600.03 s`, leaving exact global optimality unproved in the source table.
   - The target definition states:
     *"A solution equal to -8397 is a full win only with an exact global optimality certificate. Certificates may be a complete dynamic-programming/Bellman certificate or an exact rational branch-and-bound proof for the published BQP; a solver status or floating-point gap alone does not qualify."*

2. **Novelty Summary**:
   - No prior exact optimality proof for `po_a010_t10_orig_b004_l1e-03` appears in the QOBLIB repository or literature.
   - This submission provides a complete, independently checkable 10,606-state Bellman optimality certificate (`object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json`, `object/po_a010_t10_orig_b004_l1e-03_downward_meet_tables.json`, and `object/po_a010_t10_orig_b004_l1e-03_upward_join_tables.json`) establishing that no integer schedule in the space of $10,606^{10}$ trajectories can achieve an objective $\le -8398$.

pass: true
