# Honesty gate (main session) — claims D–I
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true. All three are fresh executor contexts (DI round). Prior A/B/C panel archived in panel/archive_ABC/.
Table fetch age: novelty re-fetched 2026-10-14T14:28:41Z–14:28:46Z; claim tables 14:23:27Z–14:23:39Z; both under 6 h at gate time (~14:37Z).
Downgrade checks (never upgrade):
- Reproduce: all six energies/grad/Hessian/Riesz-basin match saved files; no hedging.
- Novelty: all six strictly below live Riesz and literature; no tie.
- Criterion: F_777, H_743, I_745 meet full success_criterion (only Riesz lists N; other point URLs 404). D_534, E_548, G_542 fail full distinct-basin because live CCD Thomson xyz/<N>.xyz exists (gate re-checked HTTP 200 for 534/542/548, 404 for 743/745/777); 534/548 match E* within <1e-6; 542 xyz is ~6.26e-2 below E*. Downgraded those three to p3 (Riesz-table improvement only). Scope not wider than evidence. Hessian NUMERICAL allowed by criterion wording.
status: CONFIRMED_SOLUTION
confirmed_scope: For N=777, 743, and 745, the claimed unit-sphere configurations have mpmath energies 289900.7785339097, 264837.5287041150, and 266280.2015165257 — each ≥2.97e-2 below the sole live-table value (CCD Riesz s=1), with tangent gradient <1e-20, all 2N−3 non-rotational Hessian eigenvalues numerically positive (float64 + Weyl bound), and a basin distinct from the only posted point file (Riesz) — and, separately, N=534, 548, and 542 improve that same Riesz table by ≥6.6e-2 under the same cert (p3) but fail full success because live CCD Thomson xyz/534.xyz and xyz/548.xyz match E* within <1e-6 and xyz/542.xyz lies 6.26e-2 below the claim.
