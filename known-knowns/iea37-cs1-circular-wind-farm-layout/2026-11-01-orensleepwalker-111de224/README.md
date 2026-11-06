# IEA37 CS1: a distinct feasible 16-turbine alternative

## What
The fixed 16-turbine layout in object/layout.json satisfies p2 against the complete live V3R1T4S comparator inventory checked on 2026-11-01, with strict feasibility, fixed-model AEP 421304.60329359624 MWh, and all 16 matched displacements above 50 m versus participant 12 and the sole relevant open claim PR #578.

Status: CONFIRMED_PARTIAL, enumerated bank partial win p2. Three fresh AI-agent contexts passed. At initial packaging, no independent human or benchmark-maintainer review had occurred.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; a few seconds with internet access on the first run. Two comparator files are downloaded from pinned public commits, checked by SHA256, and cached in the operating system temporary directory. No downloaded code is executed. Subsequent runs can use that cache. See RUN_IT_YOURSELF.md for an explicit local-reference option.

## Compared to
| Comparator | Official AEP (MWh) | Role |
|---|---:|---|
| DPCRO-SL Table 4 / p2 threshold | 419935.7905 | Energy threshold for this partial win |
| This explicit object | 421304.60329359624 | Strictly feasible alternative |
| Participant 12 | 421561.89715066203 | Posted comparator, boundary-infeasible |
| Open draft PR #578 | 424131.9502979168 | Stronger feasible energy, different arrangement |

All 16 minimum-total-Euclidean assigned partner distances exceed 50 m against each required comparator; p2 requires at least 6. Independent global origin-rotation/reflection screens also exclude a mere transformed copy. The live comparator inventory was checked on 2026-11-01; see the panel reports for evidence, scope and times. Their original review text is preserved verbatim below publication notes identifying local reviewer paths and commands that are not included in this package.

## Not claimed
No energy record, optimality, field-performance prediction, new optimization method, global firstness, or exhaustive literature coverage. The candidate is below PR #578 in official AEP. One relevant 2026 multimodal-layout paper could not be read in full because its publisher returned 403; no bypass was attempted. General layout-diversity methods predate this certificate. Separate robustness experiments and 36-turbine searches from the original research session are excluded from this package.

## Credits
- Nicholas F. Baker, Andrew P. J. Stanley, Jared J. Thomas, Andrew Ning and Katherine Dykes: IEA Wind Task 37 case studies, evaluator, parameters and submitted layouts; https://github.com/IEAWindSystems/iea37-wflo-casestudies and https://doi.org/10.2514/6.2019-0540.
- Majid Bastankhah and Fernando Porte-Agel: Gaussian wake-model foundations.
- IEA37 participant 12: posted comparison layout; authorship is credited through the official benchmark, without asserting identity.
- Perez-Aracil et al.: DPCRO-SL comparison threshold, https://arxiv.org/abs/2212.00742.
- Contributor of PR #578: stronger comparison object, https://github.com/elder-plinius/V3R1T4S/pull/578. Its coordinates were not used as generator starts for this candidate.
- OrenSleepwalker, with Codex generation and three separately started AI review contexts. No historical timestamp attestation by an external party is claimed.
