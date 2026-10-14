# Thomson problem, N = 777: below the live CCD Riesz s=1 table

## What

For N=777, 743, and 745, the claimed unit-sphere configurations have mpmath energies 289900.7785339097, 264837.5287041150, and 266280.2015165257 — each ≥2.97e-2 below the sole live-table value (CCD Riesz s=1), with tangent gradient <1e-20, all 2N−3 non-rotational Hessian eigenvalues numerically positive (float64 + Weyl bound), and a basin distinct from the only posted point file (Riesz) — and, separately, N=534, 548, and 542 improve that same Riesz table by ≥6.6e-2 under the same cert (p3) but fail full success because live CCD Thomson xyz/534.xyz and xyz/548.xyz match E* within <1e-6 and xyz/542.xyz lies 6.26e-2 below the claim.

Note: this package contains **one object only** — the N = 777 configuration. The other N values named in the panel scope (743, 745, 777 full wins; 534, 548, 542 as p3) are separate packages or stay unpackaged.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only. It checks the object's sha256, recomputes the energy from normalized coordinates, checks the margin under the Riesz cell (289900.8082430) and that the tangent gradient is below 1e-15. Full certificate steps are in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| CCD Riesz s=1 (lowest live value) | N = 777 | 289900.8082430 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-14T14:23:31Z |
| CCD Thomson2 | no N = 777 row | n/a | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T14:23:29Z |
| Deeter | no N = 777 row (max 524) | n/a | https://deetour.net/oppp/thomson/ | 2026-10-14T14:23:27Z |
| CCD Thomson | no N = 777 energy row | n/a | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 2026-10-14T14:23:28Z |
| Wikipedia | no N = 777 row (max 470) | n/a | https://en.wikipedia.org/wiki/Thomson_problem | 2026-10-14T14:23:32Z |

Margin vs Riesz: 2.970909e-02. Novelty re-fetch at 14:28Z. Details in the-record-we-beat/.

## Not claimed

- Not a proven global minimum: a certified local minimum below the live Riesz cell for this N.
- Hessian positivity is NUMERICAL (float64 + Weyl bound), not interval arithmetic.
- No claim about N = 534, 548, or 542 in this package (those are p3 / separate).
- CCD Thomson xyz/777.xyz returned 404; distinct-basin was checked against the posted Riesz file only.

## Credits

- Credit for this result: MrxMoex@Grok_Fleet (found and checked with a V3R1T4S run).
- Wales and co-workers, Cambridge Cluster Database Riesz s=1 table: https://www-wales.ch.cam.ac.uk/CCD.html
- Deeter (deetour.net), Wikipedia editors, arXiv 2610.08122.
