# How we found it (contributor text, unverified)

**Brief.** Physlib's Georgi–Glashow file lists `GaugeGroupI` (SU(5)), `inclSM` (the map
SU(3) × SU(2) × U(1) → SU(5), (h, g, α) ↦ blockdiag(α³g, α⁻²h)) and `inclSM_ker` (its kernel is Physlib's ℤ₆
subgroup) as informal entries: docstrings with tags, no Lean statements. The status page was fetched once at
2026-10-14T06:16:29Z (HTTP 200). Because the target is informal, the run first wrote the docstrings out as a frozen
Lean statement (`how-we-built-it/PREREG.md`, frozen before any attempt) and asked the CRITERION skeptic to judge
that reading separately.

**What worked.** The direct route (lens "kernel-first"), first checker PASS at 06:29–06:30 UTC. The map is built
as a monoid hom whose underlying matrix is the frozen `inclSMMatrix` by definition. Membership in SU(5): the
reindexed block matrix times its conjugate transpose is block-diagonal with blocks (αᾱ)³gg* = 1 and (ᾱα)²hh* = 1;
its determinant is (α³)²·(α⁻¹)⁶ = 1. Multiplicativity is one block-multiplication rewrite. Kernel: M = 1 iff
α³g = 1 and α⁻²h = 1; taking the determinant of the first gives α⁶ = 1 (det g = 1), so α is a sixth root of unity
ρ and Physlib's `gaugeGroupℤ₆OfRoot ρ` is the element; the converse is two scalar identities. A numerical check in
Python preceded the Lean work (`how-we-built-it/out/numcheck.txt`). A second lens ("construct-space") reached a
proof independently; it is not part of this package.

**What failed or was not needed.** No SU(5) embedding existed in Physlib to transport. Composing homs, a
*-homomorphism route and an entrywise brute force were never started because the direct route did not stall.
For the bonus `embedSMℤ₆`, a first construction through `kerLift` timed out in `isDefEq` and a `rw` failed on two
definitionally equal but syntactically different group instances; building the map on the quotient with
`QuotientGroup.lift` worked (`how-we-built-it/lean/EmbedZ6.lean`).
