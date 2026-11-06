> Publication note (2026-11-06, maintainer-requested path clarification): The reviewer environment and working files named below are not included in this package. This includes `../../../.venv-research/bin/python`, `../review-reproduce/`, and the captured checks, outputs and replay logs there. The historical reproduction command below depends on that unavailable environment and is not a package verification command. The runnable package verifier is `sh verify-it-yourself/run_checks.sh`, executed from the package folder. The original review follows verbatim; its findings and verdict are unchanged.

context: subagent

Evidence was restricted to claim/, plus applicable panel instructions. I wrote ../review-reproduce/independent_check.py from criterion.txt, PREREG.md, the YAML definitions, and references/iea37-aepcalc.py before reading author-code/. No previous run, author notes, or other panel verdict was consulted.

Definition quoted from criterion.txt:
> A feasible 16-turbine layout strictly above 419935.7905 MWh (DPCRO-SL, the best published value by a non-participant) such that, under the minimum-total-distance one-to-one matching, at least 6 of its 16 turbines are more than 50 m from their partner in the participant-12 layout and in every V3R1T4S known-known or open-claim layout.

The supplied fixed-model definition uses the 16-bin rose, 9.8 m/s inflow, 130 m rotor diameter, 3.35 MW rated power, 4/9.8/25 m/s cut-in/rated/cut-out, Gaussian wake expansion 0.0324555 and thrust coefficient 8/9. Geometry is checked with direct double-precision sqrt expressions, radius <=1300 m and each pair >=260 m, with no feasibility tolerance.

Numeric reproduction succeeds for object/layout.json and both supplied references:

| Quantity | Independent result |
|---|---:|
| Candidate scalar AEP, MWh | 421304.60329359624 |
| Candidate official AEP, MWh | 421304.6032935962 |
| Margin above p2 threshold, MWh | 1368.8127935962402 |
| Maximum radius, m | 1299.999900000054 |
| Minimum spacing, m | 580.4318820195579 |
| Participant12 minimum assignment total, m | 5968.153016032979 |
| Participant12 assigned distances >50 m | 16 |
| PR578 minimum assignment total, m | 5604.992303149081 |
| PR578 assigned distances >50 m | 16 |

All three asserted candidate numbers agree exactly with the independent scalar calculation. Official/scalar binned-energy differences are at most 1.4551915228366852e-11 MWh. The supplied reference totals reproduce as 421561.89715066203 MWh and 424131.9502979168 MWh, respectively. Participant12's supplied coordinates are strictly infeasible (maximum radius 1303.5181552724919 m); PR578 is feasible. The candidate does not beat either reference's AEP.

Assignment was exhaustively recomputed by dynamic programming over all 65,536 subsets and cross-checked with SciPy. Both methods select the same pairs. There were no exact floating-point cost ties; the closest selected partner distances are 207.5886458454797 m and 236.26419888974547 m. This is a full assignment computation, not a spot check. Geometry controls with a small radius violation or a coincident pair fail; a strictly interior regular polygon passes. All five reference hashes match reference-hashes.json. A repeat execution produced byte-identical captured output. Later calls of the author's scalar and assignment routines agree with the independent results.

Reproduction command, from claim/:
```sh
../../../.venv-research/bin/python ../review-reproduce/independent_check.py > ../review-reproduce/independent_output.json
```
Captured independent results, the repeat, later author comparison, and input snapshot are in ../review-reproduce/.

Supplemental provenance was added while this review ran: provenance/original-generator-output.json, provenance/generator-log-excerpt.jsonl, and provenance/README.md. I examined those files rather than trusting a description of them. The original output's coordinates match the frozen object exactly; its reported seed 20261102 and restart 80 agree with the log. A fresh replay of the supplied continuation generator completed all 80 restarts, from random/ring starts with seed 20261102. It recovered the same final AEP 421304.6032935965 MWh at restart 80, and its coordinates differ from the frozen object by at most 1.1141310096718371e-10 m. The first 90-second invocation timed out after checkpoint 61; a second invocation resumed that saved RNG/checkpoint state and completed 80. Full replay logs and checkpoint are retained in ../review-reproduce/. This corroborates generation without using reference coordinates as starts. Author-generated records and a current replay cannot independently attest every historical event, such as precisely when code was first adapted; no such historical-attestation conclusion is made.

Packaging observations: the original REPRODUCE.md described a JSON array whereas the actual object wraps coordinates in coordinates_m. The original author-code/verify_layout.py expected omitted review-package/ paths and a recompute module. These defects did not remove any scientific inputs needed by my checker; the command above fully reproduces the numerical certificate from the supplied files. Later packaging edits are not evidence for any scientific conclusion here.

confirmed_scope: The supplied 16-turbine object satisfies strict CS1 geometry, yields 421304.60329359624 MWh under an independent scalar reconstruction of the fixed official model, and has 16 assigned partner distances strictly above 50 m in minimum-total-Euclidean assignments to each of the two supplied comparator layouts.

This review passes numerical eligibility against supplied references and corroborates the stated generation seed/restart. Comparator completeness, exclusion of trivial transformations, non-subsumed novelty, and independent historical attestation are outside this narrow reproduction result. No unresolved numerical condition in this stated scope remains.

pass: true
