# How we found it (contributor text, unverified)

- Starting point: a target list (2026-11-24) noted that the 32.537 record predates Yang's zero-free constants (51.34) and
  Bellotti's near-unity zero-density estimate. A novelty sweep (arXiv, OEIS, rStation, web) found no rigorous threshold
  below 32.537, and one non-rigorous model (rStation paper 130 §2.3, ~30.07).
- Replay first: a float replay of Cully-Hugill's inequality reproduces 32.892 (Ford c = 57.54) and MTY's 32.76; the thesis
  value 32.536 appears only with Ford's c = 51.82 (stated for T0 = exp(exp(33))), a caution passed on, not a claim.
- Prereg (frozen before any interval computation): Y_cert on the 0.001 grid, certified at prec 128 and 256 and by a second
  implementation; ablation, tamper and float/rigorous controls.
- What worked: replacing the Kadiri-Lumley-Ng bound near sigma = 1 by Bellotti's T^(B(1-sigma)^(3/2)) shape, which needs a
  new integral bound (Lemma 4(c)) and a monotonicity lemma (Lemma 6); with Yang's c = 51.34 this gives 29.735.
- Controls: without Bellotti's density the same code gives 32.892 (Ford c) / 32.505 (Yang c); Y - 0.001 fails; inflating
  Bellotti's C1 by e^50 fails; constants other than I3 and I4 can be inflated by e^100 without effect.
- What did not help: Bellotti's Thm 1.2 (single-term) gives 29.836; Thm 1.3 gives 29.671 but its proof is only sketched,
  so it is not used.
- Panel: three fresh subagent contexts saw only the claim folder; all passed. Their credit fixes (rStation 130, MTY 2024)
  and the journal-variant constant (54.004, not 53.989) are applied as errata (how-we-built-it/CLAIM_CHANGES.md).
