# Brun's constant under GRH: B < 2.156967 (previous conditional record 2.1594, Dunn)

This is a **conditional** result: it assumes the Generalized Riemann Hypothesis for Dirichlet L-functions
(including RH). It is a small improvement of Dunn's GRH bound B < 2.1594, obtained by feeding a known
modulus-dependent explicit GRH error term (Grenié–Molteni) into Dunn's published method. It is not
unconditional, it is not the bank's main win, and it says nothing about whether GRH holds.
Submission id: `2026-11-23-blocksavvy-a26bba47`. Bank target: `brun-constant-unconditional-upper-bound`, partial win p1.

## What

Assuming GRH for Dirichlet L-functions (including RH), Brun's constant satisfies B < 2.156967, by Dunn's (arXiv:2504.15658) sieve framework with Grenie-Molteni Cor. 1.2 applied per modulus q <= z^2 and a proved V(z) lower bound, evaluated in arb ball arithmetic (claim/code/replay.py, sup 2.1569669355 at 128 and 256 bits), which meets bank partial win p1 (strictly below Dunn's 2.1594) and the PREREG.v2 bar (U <= R - 1e-4, R = 2.1593210324) but is conditional and not the main win.

In short: B = sum over twin primes (p, p+2) of 1/p + 1/(p+2). Dunn (Bull. Aust. Math. Soc. 113 (2026) 293-303,
arXiv:2504.15658v2 Theorem 3.1) bounds B by B(4e18) plus a Selberg-sieve sum over 9906 intervals [m_i, m_{i+1}]
up to 10^2000 plus a tail. In that sum he uses one GRH constant for every modulus up to sqrt(x). We change three
inputs (object/proof.md):
- (B) Grenié–Molteni, J. Number Theory 2019, Cor. 1.2 applied per modulus q = [d1, d2] <= z_i^2, which gives a
  smaller constant because log q <= 2 log z_i is much less than (1/2) log x;
- (L) li(x) evaluated directly in ball arithmetic, in place of the Dusart/Schoenfeld bounds;
- (V) our own proved lower bound for V(z) when z > 1e10, in place of Klyve's c3 lemma, with exact fixed-point
  tables of V(z) up to 1e10.
We also add the inherited pi_2(z) term that Dunn's Theorem 2.1 leaves out (<= 1.03e-15).
Everything is evaluated in arb ball arithmetic, and the total is B <= 2.15696693552995885 (the sup of the ball)
< 2.156967. Replaying Dunn's own inputs rigorously gives 2.1593210324, which reproduces his 2.1594. Change (B)
alone, with all of Dunn's other inputs, gives 2.1569562895; that figure is noted, not claimed.

## Check it yourself

From this folder (python3 >= 3.9, a C compiler, and pip access once to install python-flint==0.9.0 into
verify-it-yourself/.venv):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: about 20 seconds on 6 cores (about 1-2 minutes on a 4-core laptop, plus
the one-time pip install). It recomputes V(z) and M(z) exactly from the definition with its own sieve
(verify-it-yourself/vcount.c, cross-checked against pure Python for n <= 20000), checks that every z_i in
object/a_bound_certificate.json is admissible, re-evaluates every one of the 9906 interval terms in arb and
requires the stated value to match, recomputes the V-lemma constant A(1e10), and checks the total < 2.156967.
The checker trusts the cited published inputs listed under "Not claimed" and the proof in object/proof.md, which
it evaluates but does not prove.

## Compared to

| table | cell | our value | table value | source | fetched (UTC) | HTTP | sha256 of fetched page |
|---|---|---|---|---|---|---|---|
| Tao et al., optimizationproblems | constant 81a (Brun's constant), upper bound under GRH | 2.156967 | 2.1594 (Dunn 2025) | https://teorth.github.io/optimizationproblems/constants/81a.html | 2026-11-23T18:21:53Z (gate re-fetch; also NOVELTY 17:11:43Z, ours 16:18:57Z and 16:57:58Z) | 200 | f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9 |

The best unconditional upper bound on the same page is not affected. See the-record-we-beat/ and panel/novelty.md
(no open pull request touches constants/81a; no published or posted GRH bound <= 2.156967 was found).
Re-fetched immediately before submission: 2026-11-24T01:56:00Z, HTTP 200, same sha256 f8344f6a... (raw 81a.md also
unchanged, sha256 62848e9a...), still 2.1594; no open pull request touches constant 81a (GitHub API, 01:56:07Z).

## Not claimed

- Not unconditional: the bound assumes GRH for the Dedekind zeta functions of Q(zeta_q), which factor into Dirichlet
  L-functions. It is not the bank's main (unconditional) win.
- Inherited inputs that were not re-proved here and are trusted as published: Dunn's framework (Theorems 2.1, 2.2,
  3.1; Prop. 2.1 / Lemma 2.2 for M(z) above 1e7); Grenié–Molteni Cor. 1.2; Platt–Trudgian Lemma 6
  (B(4e18) <= 1.840518, checked in arXiv:1803.01925); pi_2(4e18) = 3023463123235320 (checked in
  Bayless–Klyve–Oliveira e Silva, Integers 13 (2013) #A43); and Klyve's thesis Theorem 5.7 (the Selberg sieve form
  used by Dunn). Theorem 5.7 was checked against the primary source after the gate: the thesis PDF
  (https://collections.dartmouth.edu/xcdas-derivative/dcdis/pdf/dcdis-klyve2007.pdf, doi:10.1349/ddlp.153, fetched
  2026-11-24T01:54:42Z, HTTP 200, sha256 5f3e0034a542745dd6ce7b6cdfa199bd669e3c9c9086815cff4b556cac11a03b), p. 128:
  "Theorem 5.7. Let x > 0 be a real number. Then for any number z, pi_2(x) <= li(x) (sum_{d<=z, d|P_z} 1/f_1(d))^(-1)
  + sum_{d1,d2<=z, d1,d2|P_z} |E(x; [d1,d2], -2)|", with f_1(p) = p - 2, E(x; d, -2) = pi(x; d, -2) - li(x)/phi(d) and
  li truncated at 2. It is unconditional (Selberg's sieve, Theorem 5.4) and matches Dunn's Theorem 2.1. Klyve's
  derivation, (5.27), has pi_2(x) - pi_2(z) <= S(A, P, z); the displayed theorem drops the pi_2(z) term, which is the
  omission we already correct for (object/proof.md A).
- The margin below 2.156967 is 6.4e-8 at the chosen z_i. The z_i come from a float optimiser, and other admissible
  choices give other valid bounds; the first REPRODUCE skeptic's own optimisation gave 2.1569642936
  (panel/superseded/reproduce_v1.md). The headline is rounded up
  and was not tuned.
- Not new mathematics beyond the bound itself: the ingredients are published; the contribution is combining them,
  proving the V(z) lemma, and certifying the evaluation.

## Credits

- **Contributor:** [BlockSavvy](https://github.com/BlockSavvy). Found with a V3R1T4S agent run, checked by a
  three-skeptic panel of fresh subagent contexts (REPRODUCE was rerun in a fresh context; the first
  REPRODUCE verdict, also pass: true, is kept in panel/superseded/).
- **Lachlan Dunn**: the GRH bound 2.1594 and the framework reused here. Bull. Aust. Math. Soc. 113 (2026) 293-303,
  doi:10.1017/s0004972725100233; https://arxiv.org/abs/2504.15658 ; code https://github.com/LachlanJDunn/B_Under_GRH
- **Loïc Grenié and Giuseppe Molteni**: explicit Chebotarev under GRH, https://arxiv.org/abs/1709.07609
- **Daniel R. Johnston and Valeriia Starichkova**: the GRH constant Dunn used, https://arxiv.org/abs/2208.01229
- **Dave Platt and Tim Trudgian**: B(4e18) and the unconditional framework, https://arxiv.org/abs/1803.01925
- **Jonathan Bayless, Dominic Klyve and Tomás Oliveira e Silva**: pi_2(4e18), Integers 13 (2013) #A43,
  https://math.colgate.edu/~integers/n43/n43.pdf ; **Dominic Klyve**: thesis (Dartmouth 2007), Theorem 5.7.
- **Pierre Dusart**: Ramanujan J. 45 (2018), Theorem 5.1, used by Dunn and checked here, though the headline no
  longer needs it.
- **Terence Tao and contributors**: the optimizationproblems constants table,
  https://teorth.github.io/optimizationproblems/constants/81a.html
- **FLINT/Arb** and python-flint, used for the ball arithmetic.
