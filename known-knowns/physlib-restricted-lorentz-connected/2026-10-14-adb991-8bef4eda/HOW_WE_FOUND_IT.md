# How we found it (contributor text, unverified)

**Brief.** Physlib states `restricted_isConnected` (tag FXNL5) as a `semiformal_result`, a statement with no
proof. The status page was fetched once at 2026-10-14T06:07:15Z (HTTP 200) and the run's Physlib build was
moved to the master commit of that moment, be0f21e5002d6d73b87f2055530c1e8bf7151546. The statement was frozen in
`how-we-built-it/PREREG.md` before any attempt. Physlib already had the boost–rotation homeomorphism
`LorentzGroup.toBoostRotation : restricted d ≃ₜ Velocity d × SO(d)` and path-connectedness of the velocity space,
so the missing piece was the connectedness of SO(d), which the pinned Mathlib does not contain.

**What worked.** Three independent attempts (V3R1T4S "lenses") each produced a proof that the frozen checker
passed:
- The object in this package (lens "construct-space": its first proof passed the checker at 06:22 UTC; this explicit-path version passed at 06:55 UTC):
  Householder reflections `hh w = 1 - (2/(w·w)) w wᵀ`; every element of SO(n) is reduced to the identity by an
  explicit elimination, two reflections per column; each product of two reflections is joined to the identity
  by the explicit path `t ↦ hh u * hh ((1 - t) u + t v)` inside SO(n). So SO(n) is path-connected for every n,
  and the boost–rotation homeomorphism carries this to the restricted Lorentz group. It imports only Physlib.
- Two other proofs (lenses "kernel-first" and "same-object") used Mathlib's Cartan–Dieudonné theorem
  (`LinearIsometryEquiv.reflections_generate_dim`) moved to matrices, then the connected component of the
  identity. They are not part of this package.

**What failed or was not needed.** Mathlib's connectedness of unitary groups is for complex C*-algebras and does
not give real SO(n). Givens rotations, the Cayley transform, the exponential map and a sphere fibration were
planned but never run once the Householder argument compiled. One tactic dead end (rewriting `hh u` into
`1 + replicateCol * replicateRow`) was replaced by `ext; simp; ring`.

**Upstreaming.** `how-we-built-it/upstream/RestrictedConnected.lean` is a draft in Physlib's module style that
proves the statement under its upstream name `LorentzGroup.restricted_isConnected`, plus
`restricted_eq_connectedComponent_one`. It was not reviewed by the panel and was not submitted.
