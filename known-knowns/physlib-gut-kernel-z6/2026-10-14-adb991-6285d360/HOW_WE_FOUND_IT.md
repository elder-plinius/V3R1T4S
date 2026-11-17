# How we found it (contributor text, unverified)

**Brief.** Physlib's Pati–Salam file lists `GaugeGroupI` (SU(4) × SU(2) × SU(2)), `inclSM` (the map
SU(3) × SU(2) × U(1) → SU(4) × SU(2) × SU(2), (h, g, α) ↦ (blockdiag(αh, α⁻³), g, diag(α³, α⁻³))) and `inclSM_ker`
(its kernel is Physlib's ℤ₃ subgroup) as informal entries: docstrings with tags, no Lean statements. The status page
was fetched once at 2026-10-14T07:02:29Z (HTTP 200). The run first wrote the docstrings out as a frozen Lean statement
(`how-we-built-it/PREREG.md`, frozen before any attempt) and asked the CRITERION skeptic to judge that reading.

**What worked.** The direct route (lens "kernel-first"), first checker PASS on 2026-10-14 against Physlib be0f21e5.
A numerical check came first (`how-we-built-it/code/numeric_check.py`, output in `how-we-built-it/out/`): the map
lands in SU(4) × SU(2) × SU(2), is multiplicative, and its kernel on a 600000-point scan of U(1) is exactly the
three ℤ₃ elements. In Lean the map is built as `hom4.prod (GaugeGroupI.toSU2.prod homR)` from the frozen matrices;
SU(4) membership is block algebra under `reindex` (unitarity from (αh)ᴴ(αh) = 1 and |α⁻³|² = 1, determinant
α³·1·α⁻³ = 1); the kernel is read off from `fromBlocks_inj` and the (0,0) entry of diag(α³, α⁻³): α³ = 1, h = α²·1,
g = 1, which is Physlib's `gaugeGroupℤ₃OfRoot`. Controls (`how-we-built-it/lean/Exp2_controls.lean`): the kernel is
not the ℤ₆ subgroup and not trivial. A second lens ("construct-space") reached a proof independently; it is not part
of this package.

**Timeline.** The 2026-10-14 panel was cut off by the account's session limit before any verdict. On 2026-10-15 the
machine was set up again with Physlib 76245c85; the unchanged object still passed the unchanged checker, and a fresh
three-skeptic panel (all pass) and the honesty gate confirmed it against 76245c85.

**What failed or was not needed.** A one-shot `simp only` for SU(4) unitarity and a `fin_cases <;> simp` for the
diagonal's multiplicativity both stalled on rewrite order; ordered `rw` chains worked. Entrywise normalisation and a
representation-theoretic route were never needed.
