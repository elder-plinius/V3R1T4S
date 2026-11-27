# Primes between consecutive cubes for n >= exp(exp(29.735)) (previous record exp(exp(32.537)), Cully-Hugill)

This is a **conditional threshold** result: it uses two inputs that are not refereed journal papers, Yang's 2025 UNSW
PhD thesis (Theorem 1.3, zero-free region c = 51.34) and Bellotti's unrefereed preprint arXiv:2311.05136v1 (Theorem 1.1,
zero density near sigma = 1). It does not settle the problem for all n >= 1.
Submission id: `2026-11-24-blocksavvy-7742deed`. Target: `primes-between-cubes-explicit-threshold` (outside the bank; family folder = target id).

## What

Conditional on Yang's 2025 UNSW PhD thesis Theorem 1.3 (zero-free region, c = 51.34) and Bellotti's unrefereed preprint arXiv:2311.05136v1 Theorem 1.1 (zero density near sigma = 1), plus published results, for every integer n >= exp(exp(29.735)) there is a prime in (n^3 + 1/2, n^3 + 3n^2 + 1/2], and so between n^3 and (n+1)^3; this is a threshold result, and the claim for all n >= 1 stays open.

In short: Ingham's argument as made explicit by Cully-Hugill (J. Number Theory 247 (2023)), with x = n^3 + 1/2,
y = n^3 + 3n^2 + 1/2 and T = x^(1/3 + 1e-9). The prime exists if Phi(log x) < 1 (object/proof.md, Lemmas 1-5); Phi is
non-increasing for log x >= X0 = 3 e^Y (Lemma 6). The gain over 32.537 comes from using Bellotti's density shape
T^(B(1-sigma)^(3/2)) near sigma = 1 (new integral bound, Lemma 4(c)) together with Yang's zero-free constant.
object/certificate.json lists every constant; at Y = 29.735, Phi(X0) = 0.9342533444881... < 1 (interval arithmetic),
and at Y = 29.734 it is 1.0445 > 1, so the certificate is tight to the 0.001 grid.
Variants (how-we-built-it/out/scan_out.txt): 29.907 with Bellotti's zero-free region c = 54.004 (arXiv:2306.10680v1,
published J. Math. Anal. Appl. 536 (2024)) instead of Yang's thesis; 32.677 with no thesis or preprint input at all.

## Check it yourself

From this folder (python3 >= 3.8; pip access once to install mpmath==1.3.0 into verify-it-yourself/.venv unless python3
already has mpmath):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: under 1 second (plus the one-time pip install). It checks that every constant
in object/certificate.json equals the value in the cited statement, recomputes Phi(X0) and the monotonicity and validity
conditions (M1)-(M4), (V1)-(V4) in mpmath interval arithmetic at 200 and 300 bits, requires the stated upper bound to be
>= the recomputed one (and within 1e-9 of it) and < 1, and checks that Y - 0.001 fails. It evaluates, but does not prove,
the formulas in object/proof.md, and it trusts the cited inputs listed under "Not claimed".

## Compared to

| table | cell | our value | table value | source | fetched (UTC) | HTTP | sha256 of fetched page |
|---|---|---|---|---|---|---|---|
| OEIS A060199 (comments) | explicit n0 with a prime in (n^3,(n+1)^3) for n > n0, as log log n0 | 29.735 | 32.76 (Mossinghoff-Trudgian-Yang 2024) | https://oeis.org/search?fmt=json&q=id:A060199 | 2026-11-24T08:03:19Z (pre-package; NOVELTY 07:53:27Z; scout 07:34:04Z) | 200 | d132575bbd4f0fd0d1bf0eb86ef09a0239b5c60ac8817d7becab7dc7fca6cc5e |
| literature (no table) | best rigorous prior value | 29.735 | 32.537 (Cully-Hugill PhD thesis 2021, Thm 4.3) | https://doi.org/10.1017/S0004972723000588 (thesis abstract) | 2026-11-24T07:34:05Z | 200 | 7b2af7afd5b622dc5148030d6e7f49614a63542f80b9dfdb4703ea775ef26713 |

32.537 is quoted as the best value by Johnston-Sorenson-Thomas-Webster (arXiv:2601.15564v2, 2026). Caution, not
established: a replay of the thesis inequality reproduces 32.536 only with Ford's constant c = 51.82, which the thesis
states for T0 = exp(exp(33)) (see how-we-built-it/CLAIM.md). This does not affect the comparison, which uses the smaller value.
Prior non-rigorous anticipation: rStation paper 130 §2.3 (u/span_of_dilates, 08 Nov 2026) gives about 30.07 as a
"model, not a theorem". See the-record-we-beat/snapshot.md and panel/novelty.md.

## Not claimed

- Not for all n >= 1: below exp(exp(29.735)) the question stays open (computations reach n^3 <= 1.649e40, arXiv:2601.15564).
- Not unconditional on refereed work: I3 (Yang, PhD thesis 2025) and I4 (Bellotti, arXiv:2311.05136v1, unrefereed) are
  trusted as stated. I4's constant is load-bearing (C1 x 1.2 already breaks 29.735). Without both, the method gives 32.677.
- Inputs trusted as published: Cully-Hugill JNT 2023 Theorem 2 and Table 2 (K = 2.4798); the Kadiri-Lumley-Ng density
  bound as restated there (C1 = 17.418, C2 = 5.272); Hasanalizade-Shen-Wong (N(T)); theta(t) < t log 4. All except I3
  and I4 enter with slack above e^100 (how-we-built-it/out/mutation_out.txt).
- Not a new idea: inserting Bellotti's near-unity density into Cully-Hugill's argument was proposed non-rigorously in
  rStation paper 130. What is new is the rigorous chain (Lemma 4(c), Lemma 6), the interval certificate, and the value.
- Not the lowest the method may reach: Bellotti arXiv:2508.02041 (2025) and JNT 269 (2025) were not used.

## Credits

- **Contributor:** [BlockSavvy](https://github.com/BlockSavvy). Found with a V3R1T4S agent run, checked by a
  three-skeptic panel of fresh subagent contexts.
- **Michaela Cully-Hugill**: the explicit Ingham argument and error term, J. Number Theory 247 (2023) 100-117,
  https://arxiv.org/abs/2107.14468 ; PhD thesis (UNSW 2021), Thm 4.3 (32.537), abstract Bull. Aust. Math. Soc.,
  https://doi.org/10.1017/S0004972723000588
- **Andrew Yang**: zero-free region c = 51.34, PhD thesis (UNSW 2025), doi:10.26190/unsworks/31825
- **Chiara Bellotti**: zero density near unity, https://arxiv.org/abs/2311.05136 ; zero-free region, J. Math. Anal. Appl.
  536 (2024), https://arxiv.org/abs/2306.10680
- **Michael J. Mossinghoff, Timothy S. Trudgian and Andrew Yang**: 32.76, Res. Number Theory 10 (2024),
  https://doi.org/10.1007/s40993-023-00498-y
- **Adrian W. Dudek**: the first explicit cube threshold (exp(exp(33.217))).
- **A. E. Ingham** (1937): primes between consecutive cubes for large n.
- **Habiba Kadiri, Allysa Lumley and Nathan Ng**: the explicit zero-density estimate. **Elchin Hasanalizade, Quanli Shen
  and Peng-Jie Wong**: explicit N(T). **Kevin Ford**: explicit Korobov-Vinogradov zero-free region.
- **Daniel R. Johnston, Jonathan P. Sorenson, Andrew Thomas and Jonathan Webster**: the current computational range and
  record survey, https://arxiv.org/abs/2601.15564
- **u/span_of_dilates (rStation paper 130)**: the non-rigorous ~30.07 model that anticipates the idea,
  https://rstation.ai/problems/riemann_hypothesis/papers/130
- **Charles R. Greathouse IV and OEIS contributors**: A060199, https://oeis.org/A060199
- **FLINT/Arb**, python-flint and **mpmath**: interval arithmetic.
