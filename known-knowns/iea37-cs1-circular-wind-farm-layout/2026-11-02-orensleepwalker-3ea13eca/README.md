# IEA37 CS1: a distinct feasible 36-turbine layout (partial win p1)

## What
The single 36-turbine layout in object/layout.json is strictly feasible for IEA37 case study 1 (all hubs within 2000 m and all pairs at least 260 m apart in exact double precision), has AEP 869713.9496471485 MWh under the unmodified references/iea37-aepcalc.py model, which is 6037.65 MWh above the SNOPT+WEC 863676.2993 MWh threshold, and has all 36 of its turbines more than 50 m from their partners under the minimum-total-Euclidean one-to-one matching to participant 12's posted layout, so it meets enumerated partial win p1 for the 36-turbine cell (not the full criterion, and with prior-art novelty left to the novelty skeptic).

Status: CONFIRMED_PARTIAL, enumerated bank partial win p1 (36-turbine cell). Three fresh AI-agent contexts passed (panel/). This is a computational partial result; no independent human or benchmark-maintainer review has occurred.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; about a second with internet access on the first run. One comparator file (participant 12's posted 36-turbine layout) is downloaded from a pinned public commit, checked by SHA256 and cached in the OS temporary directory. No downloaded code is executed. See RUN_IT_YOURSELF.md for an offline option.

## Compared to
| Comparator | Official AEP (MWh) | Role |
|---|---:|---|
| SNOPT+WEC (participant 4), p1 threshold | 863676.2993 | p1 requires at least 1 MWh more |
| Perez-Rua, Stolpe and Cutululis, WES 2023 | about 865000 (rounded in source) | Strongest published non-participant-12 value found |
| This explicit object | 869713.9496471485 | Strictly feasible, 36/36 hubs > 50 m from matched participant-12 hubs |
| Participant 12 | 882383.3040320875 | Posted record, 4.9 mm outside the boundary; not beaten |

Table: https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2/iea37-cs1-results, fetched 2026-11-02T23:30:04Z (HTTP 200); see the-record-we-beat/record.md.

## Not claimed
No energy record (participant 12's posted 882383.3040 MWh is higher), optimality, field-performance prediction, new optimization method, global firstness, or exhaustive literature coverage. Novelty coverage limits: the full text of da Silva et al. 2025 (IEEE Access, doi 10.1109/ACCESS.2025.3614516) and Shin and Yun, KDD 2025 (doi 10.1145/3711896.3737181) could not be opened (HTTP 403 or empty pages; no bypass attempted); unauthenticated GitHub code search was unavailable. Search snippets put da Silva et al. at about 863.76 GWh.

## Credits
- Nicholas F. Baker, Andrew P. J. Stanley, Jared J. Thomas, Andrew Ning and Katherine Dykes: IEA Wind Task 37 case studies, evaluator, parameters and submitted layouts; https://github.com/IEAWindSystems/iea37-wflo-casestudies and https://doi.org/10.2514/6.2019-0540.
- Majid Bastankhah and Fernando Porte-Agel: Gaussian wake-model foundations.
- IEA37 participant 12: posted comparison layout; credited through the official benchmark, without asserting identity.
- Jared J. Thomas and Andrew Ning (SNOPT+WEC, participant 4): p1 energy threshold.
- Juan-Andres Perez-Rua, Mathias Stolpe and Nicolaos A. Cutululis: published 36-turbine comparison, https://wes.copernicus.org/articles/8/1453/2023/.
- OrenSleepwalker, with Codex generation (search code) and Claude Code verification and three separately started AI review contexts. No external timestamp attestation is claimed.
