# Brun's constant under GRH: B < 2.126988 (previous conditional record 2.1594, Dunn)

This is a **conditional** result: it assumes the Generalized Riemann Hypothesis for Dirichlet L-functions
(including RH). It is not unconditional, it is not the bank's main win, and it says nothing about whether GRH holds.
Submission id: `2026-11-24-blocksavvy-e6b84d42`. Bank target: `brun-constant-unconditional-upper-bound`, partial win p1.

**Supersedes** the same contributor's conditional submission `2026-11-23-blocksavvy-a26bba47` (B < 2.156967, draft
PR #1231), which is left as it is: this is a separate, new submission, and nothing in #1231 was changed. The
2.156967 package's proof is reused here and one step is replaced, so this package contains the earlier bound as its
weights-off control (2.15696693552995885).

## What

Assuming the Generalized Riemann Hypothesis for Dirichlet L-functions, the written proof in PROOF.md together with its arb-certified computation shows Brun's constant satisfies B < 2.126988 (sup 2.1269871669853558245), strictly below Dunn's conditional 2.1594, which meets partial win p1 and not the main (unconditional) win.

In short: Dunn (Bull. Aust. Math. Soc. 113 (2026) 293-303, arXiv:2504.15658v2 Theorem 3.1) bounds B by B(4e18) plus
a Selberg-sieve sum over 9906 intervals up to 10^2000 plus a tail. His sieve error term uses |lambda_d| <= 1 for
the Selberg weights, so it carries r(z)^2 with r(z) = #{odd squarefree d <= z} ~ 0.405 z. The weights are explicit
(Klyve, PhD thesis 2007, (5.24)-(5.26)), and summing them gives exactly
    sum_{d<=z} |lambda_d| = W(z)/V(z),   W(z) = sum_{n<=z, n odd squarefree} prod_{p|n} p/(p-2)   (~ z/log z),
(object/proof.md section S, proved there and checked in exact rationals). With this in place of r(z), on top of the
earlier package's changes (Grenié–Molteni per-modulus GRH constant, direct li, own V(z) lemma, pi_2(z) correction),
the arb evaluation gives B <= 2.1269871669853558245 (standalone checker, 128 and 256 bits) < 2.126988.
Ablations (how-we-built-it/out/): weights off gives 2.1569669355; the weights on Dunn's original inputs alone give
2.1282623, so the gain comes from the weights.

## Check it yourself

From this folder (python3 >= 3.9, a C compiler, and pip access once to install python-flint==0.9.0 into
verify-it-yourself/.venv unless python3 already has it):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: about 70 seconds on 8 cores for both precisions (a few minutes on a
4-core laptop, plus the one-time pip install). It recomputes V(n), M(n) and W(n) exactly from the definition with
its own sieve (verify-it-yourself/wvcount.c, cross-checked against pure Python for n <= 20000), checks every z_i in
object/a_bound_certificate.json is admissible, recomputes every one of the 9906 interval terms in arb (including
Lambda(z) <= W/V, the W bound beyond 1e10 with S'(s) recomputed, and 2 z_i/m_i), requires each stated term to be
at least the recomputed sup (to 1e-15 relative) and at most 1e-5 above it, recomputes A(1e10), and checks the total of its own recomputed sups
< 2.126988, at 128 and at 256 bits. It trusts the cited inputs under "Not claimed" and evaluates, but does not prove,
the formulas in object/proof.md.

## Compared to

| table | cell | our value | table value | source | fetched (UTC) | HTTP | sha256 of fetched page |
|---|---|---|---|---|---|---|---|
| Tao et al., optimizationproblems | constant 81a (Brun's constant), upper bound under GRH | 2.126988 | 2.1594 (Dunn 2025) | https://teorth.github.io/optimizationproblems/constants/81a.html | 2026-11-24T06:16:12Z (pre-package re-fetch; NOVELTY 06:01:30Z; scout 05:32:04Z) | 200 | f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9 |

The unconditional row (2.288513, Platt–Trudgian) is not affected. No open pull request in teorth/optimizationproblems
matches "81a" (GitHub search API, 2026-11-24T06:16:12Z). See the-record-we-beat/ and panel/novelty.md.
Unconditional neighbours (panel/novelty.md): 2.288513 (Platt–Trudgian), and unrefereed Zenodo preprints at 2.281721
(Sergaev, 2026-11-22) and 2.27428 (Daniyarov, 2026-10-09); none uses GRH and none is below 2.126988.
Re-fetch the page immediately before submitting.

## Not claimed

- Not unconditional: the bound assumes GRH for the Dedekind zeta functions of Q(zeta_q), which factor into Dirichlet
  L-functions. It is not the bank's main (unconditional) win.
- Not a new sieve technique: bounding the Selberg remainder through the explicit weights instead of |lambda_d| <= 1 is
  classical (e.g. Vaughan's notes on Selberg's sieve, sum |lambda_m| << D/log D; see panel/novelty.md). The exact
  identity W(z)/V(z) in this twin-prime setting is a two-line rearrangement and may well be folklore. What is new is
  applying it to Brun's constant and the certified bound.
- Inherited inputs trusted as published: Dunn's framework (Theorems 2.1, 2.2, 3.1; Lemma 3.2 tail); Klyve's thesis
  (Theorem 5.4 proof (5.16), (5.24)-(5.26), (5.27); Klyve prints "|lambda_delta| = 1" on p.125 where only "<= 1" holds,
  harmless to all uses); Grenié–Molteni Cor. 1.2; Platt–Trudgian Lemma 6 (B(4e18) <= 1.840518); pi_2(4e18) =
  3023463123235320 (Bayless–Klyve–Oliveira e Silva); pi(x) < 1.25506 x/log x (Rosser–Schoenfeld). Dunn's Lemma 2.2
  (r(z) above 1e7) is used only by the weights-off control.
- The certificate's field names `B_upper_without_pi2z` and `note` are labels inherited from the earlier code and are
  wrong for this certificate: its stated terms include 2 z_i/m_i (how-we-built-it/CLAIM_CHANGES.md (d)). The checker
  ignores both fields.
- The z_i come from a float optimiser; any admissible choice gives a valid bound. The headline is rounded up and was not tuned.
- Residual novelty risk (panel/novelty.md): Google Scholar (403) and Semantic Scholar (429) citation checks were blocked
  and not retried; Halberstam–Richert, Opera de Cribro, Greaves and Montgomery–Vaughan were not opened (paywalled).
- A further lead (combining weights per modulus, about 2.12574) is not part of this package.

## Credits

- **Contributor:** [BlockSavvy](https://github.com/BlockSavvy). Found with a V3R1T4S agent run, checked by a
  three-skeptic panel of fresh subagent contexts.
- **Lachlan Dunn**: the GRH bound 2.1594 and the framework reused here. Bull. Aust. Math. Soc. 113 (2026) 293-303,
  doi:10.1017/s0004972725100233; https://arxiv.org/abs/2504.15658 ; code https://github.com/LachlanJDunn/B_Under_GRH
- **Dominic Klyve**: PhD thesis (Dartmouth 2007), the explicit Selberg sieve and its weights,
  https://collections.dartmouth.edu/xcdas-derivative/dcdis/pdf/dcdis-klyve2007.pdf (doi:10.1349/ddlp.153)
- **Atle Selberg**: the Lambda^2 sieve. **Robert C. Vaughan**: notes on Selberg's sieve,
  https://personal.science.psu.edu/rcv4/Selberg.pdf
- **Loïc Grenié and Giuseppe Molteni**: explicit Chebotarev under GRH, https://arxiv.org/abs/1709.07609
- **Daniel R. Johnston and Valeriia Starichkova**: the GRH constant Dunn used, https://arxiv.org/abs/2208.01229
- **Dave Platt and Tim Trudgian**: B(4e18) and the unconditional record 2.288513, https://arxiv.org/abs/1803.01925
- **Jonathan Bayless, Dominic Klyve and Tomás Oliveira e Silva**: pi_2(4e18), Integers 13 (2013) #A43,
  https://math.colgate.edu/~integers/n43/n43.pdf
- **J. Barkley Rosser and Lowell Schoenfeld**: pi(x) bounds (1962). **Pierre Dusart**: Ramanujan J. 45 (2018), checked
  but no longer needed by the headline.
- **Terence Tao and contributors**: the optimizationproblems constants table,
  https://teorth.github.io/optimizationproblems/constants/81a.html
- **FLINT/Arb** and python-flint, used for the ball arithmetic.
