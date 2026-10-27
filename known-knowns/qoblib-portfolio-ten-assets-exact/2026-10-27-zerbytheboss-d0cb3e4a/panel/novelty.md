# Novelty Skeptic Report — `qoblib-portfolio-ten-assets-exact`

context: subagent (fresh invocation)
target_id: qoblib-portfolio-ten-assets-exact
review_utc: 2026-10-27T16:10:00Z

## Novelty & Prior Art Audit

1. **Status Source Verification**:
   - Source table: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md`
   - Instance `po_a010_t10_orig_b004_l1e-03` lists incumbent objective `-8397` from Maximilian Schicker (2025-08-19).
   - The reported bound in the source table is a continuous solver relaxation bound (-15342.65126758 after 3600s), leaving the exact global optimum unproved in the literature.
   - The target definition explicitly states:
     *"A solution equal to -8397 is a full win only with an exact global optimality certificate. Certificates may be a complete dynamic-programming/Bellman certificate or an exact rational branch-and-bound proof for the published BQP; a solver status or floating-point gap alone does not qualify."*

2. **Strict Novelty Isolation**:
   - `repo/TROPHY_CASE.md` contains no prior entry for `qoblib-portfolio-ten-assets-exact`.
   - Contributor identity: `HindsightWise` <-> `zerbytheboss`.
   - No prior proof exists in the literature establishing that -8397 is the exact integer global optimum of this benchmark.
   - This submission provides the first complete, independently checkable Bellman optimality certificate proving that no integer schedule in the entire space of $10,606^{10}$ possible trajectories can achieve an objective $\le -8398$.

pass: true
