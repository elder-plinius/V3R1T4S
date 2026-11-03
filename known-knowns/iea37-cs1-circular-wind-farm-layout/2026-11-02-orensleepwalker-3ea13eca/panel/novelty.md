# NOVELTY skeptic verdict: iea37-cs1-circular-wind-farm-layout, partial win p1 (36 turbines)

context: subagent (Claude Code Agent tool, fresh context, saw only claim/ and the public web)

Scope judged: the claim is enumerated partial win p1 only. It is not a total-energy record, because participant 12 posted 882383.3040 MWh. The question here is whether any known feasible 36-turbine CS1 layout, or published value, from someone other than participant 12 reaches or exceeds the object's AEP, and whether the object is only a trivial edit of a published layout.

## Status source (fetched once, plain curl, User-Agent "V3R1T4S-novelty-skeptic/1.0", no retries)

- URL: https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2/iea37-cs1-results
- Fetch time (UTC, from `date -u`): 2026-11-02T23:35:00Z. HTTP 200, 273616 bytes.
- What the page shows: a directory listing with iea37-par{1..12}-opt{16,36,64}.yaml (12 participants), the ex16/ex36/ex64 example layouts, iea37-aepcalc.py, iea37-335mw.yaml and iea37-windrose.yaml. Nothing else has been added.
- The values come from the posted files. I fetched each raw file once at 2026-11-02T23:35:05Z (HTTP 200):
  - https://raw.githubusercontent.com/IEAWindSystems/iea37-wflo-casestudies/master/cs1-2/iea37-cs1-results/iea37-par12-opt36.yaml shows `default: 882383.3040320875`.
  - https://raw.githubusercontent.com/IEAWindSystems/iea37-wflo-casestudies/master/cs1-2/iea37-cs1-results/iea37-par4-opt36.yaml (SNOPT+WEC) shows `default: 863676.2993158966`.
  - Both files are byte-identical to claim/references/iea37-par12-opt36.yaml and claim/references/iea37-par4-opt36.yaml.
- Commit history of the results folder, from the GitHub API at 2026-11-02T23:39:21Z: the only commit is 1b2062b64b5d, dated 2019-07-29 ("addition of participant results for publication"). The byuflowlab copy has the same single commit. Neither repo has any releases, so no release assets can lag the tree.
- Official repo PRs and issues (API, state=all, 2026-11-02T23:39:27Z):
  - IEAWindSystems has #1 "byu updates" (closed, 2020) and #2 "Update wind resource reference in YAML file" (open, 2026-02-24).
  - byuflowlab has #1 (closed, 2018).
  - None of them adds a 36-turbine result.

## My own computation (code/check.py and check_output.txt in panel/work-novelty/; official evaluator from claim/references, unmodified)

- Object, claim/object/layout.json:
  - 36 hubs.
  - Max radius 1999.999900001902 m, which is ≤ 2000.
  - Min pair distance 260.259001345249 m, which is ≥ 260.
  - Feasible with no tolerance.
  - AEP = **869713.9496471485 MWh**.
- AEP and feasibility of every posted opt36 file, all reproduced by me. The only strictly feasible posted 36-turbine file is par10 (851631.93). Of the non-participant-12 files, par4 / SNOPT+WEC has the highest AEP (863676.2993), and its maximum radius is 4e-11 m over the boundary.
- Rigid-transform comparison:
  - For each posted opt36 layout (and the author's own starting layout), I scanned rotations about the origin at 0.5° steps, refined at 0.01°, with and without a mirror, and used a minimum-total-Euclidean (Hungarian) matching.
  - Best-fit results, counting turbines more than 50 m from their partner:

    | Layout | Turbines >50 m | Median distance | Max distance |
    |---|---|---|---|
    | par12 | 34/36 (36/36 in the untransformed matching; mean 353.8 m) | 242.6 m | — |
    | par4, SNOPT+WEC (mirror + 293.11°) | 27/36 | 133.8 m | 1185 m |
    | par1, 2, 3, 5, 6, 7, 8, 9, 10, 11 | 29 to 36 of 36 | 180 to 271 m | — |

  - No published layout comes within local-polish distance of the object under rotation, mirror or relabelling. Also, AEP is not invariant under rotation or mirroring with this 16-bin rose, so those edits could not produce a higher-AEP copy anyway.
- Neighbouring cell, restriction or deletion check:
  - The 64-turbine layouts of participants 4 and 12 have only 19 and 26 hubs within 2000 m (fetched raw at 2026-11-02T23:41:29Z, HTTP 200).
  - So deleting turbines from them cannot give 36 hubs inside R = 2000.
  - The 16-turbine cell has too few turbines to produce a 36-turbine layout by deletion.
- Seeding: by the author's own logs, the starting layout was claim/provenance/starting-own-best.json (859452.80 MWh, feasible). Its best rigid match to the object has 23/36 turbines more than 50 m away. Its best rigid match to every posted layout also has 23 or more turbines more than 50 m away (not tabulated). I did not assess the author logs beyond that, because they are not external attestation.

## Sources checked (all opened once, honest default client; no bypass)

1. The status page and raw opt36 / opt64 files above: HTTP 200, values as quoted.
2. Baker et al., NREL/TP 72935, "Best Practices for Wake Model and Optimization Algorithm Selection".
   - docs.nrel.gov did not resolve (DNS ENOTFOUND). docs.nlr.gov/docs/fy19osti/72935.pdf opened through WebFetch, and I extracted the text myself.
   - Table 3 (36 turbines) is topped by "SNOPT + WEC 4 G 863676.2993 17.05%". The rows below it are 851631.9310, 849369.7863, 846357.8142, 844281.1609 and so on.
   - Participant 12 is not in the table.
3. Perez-Rua, Stolpe and Cutululis, WES 8, 1453 (2023), https://wes.copernicus.org/articles/8/1453/2023/.
   - Case II (36 turbines): "the final solution of 865 GW h (increment of 0.61 %)".
   - The comparison table is an image. Even read generously as up to 865.5 GWh, it is about 4.2 GWh below the object.
4. da Silva et al. 2025, IEEE Access, "Genetic Algorithm-Based Optimization Framework for Offshore Wind Farm Layout Design", doi 10.1109/ACCESS.2025.3614516.
   - **Not opened.** ResearchGate returned HTTP 403, and both IEEE Xplore (doc 11179964) and zendy.io returned empty, JS-rendered pages. I did not retry.
   - Search-engine snippets only, so not a source I opened: the GA reports a +17.06% increase at 36 turbines against SNOPT+WEC's +17.05%. That implies about 863.75 to 863.77 GWh, consistent with the claim's "about 863.8 GWh", and below the object.
5. Ojeda-style DPCRO-SL, arXiv 2212.00742 (HTML version): 16 turbines only (best 419935.7905). No 36-turbine result.
6. Quaeghebeur, "Wind farm layout optimization using pseudo-gradients", WES 6, 815 (2021): 36-turbine results are given only as wake-loss figures, with no absolute AEP in the text. It is also older than the 24-month window.
7. Offshore wind farm layout optimization with alignment constraints, WES 10, 1611 (2025): Borssele CS3/4, 10 MW turbines, 81 to 250 turbines. Not CS1, so no 36-turbine value.
8. Valotta Rodrigues et al., WES 9, 321 (2024): appeared only in search results (360 directions, normalised values; not opened). It is not comparable to CS1 and was already noted in the bank.
9. arXiv 2610.35975 (Graph-informed Kriging BO, Oct 2026): an IEA37 benchmark at 16 turbines plus a 48-turbine farm. No 36-turbine AEP.
10. arXiv 2610.07844 (GPU WFLO with EndoWake) and arXiv 2609.40157 (EndoWake MILP): Lillgrund and square grids, with no IEA37 CS1 36-turbine case in the text read.
11. arXiv 2608.26613 (AI benchmarking study): no IEA37 AEP values.
12. arXiv 2502.00476 (Perez, Minguez, Guanche): Alpha Ventus only.
13. Shin and Yun, "Wind Farm Layout Optimization with Diffusion Models", KDD 2025, dl.acm.org/doi/10.1145/3711896.3737181.
    - **HTTP 403**, not retried.
    - Its code repo README (github.com/dbsxodud-11/layopt, API HTTP 200) does not mention IEA37 or 36 turbines.
14. Hexaly WFLOP template (hexaly.com): uses the IEA37 16/36/64 instances but reports no AEP values.
15. GitHub repository search via the API:
    - "iea37" returns 6 repos. The newest was pushed 2024-10-01, and none posts a 36-turbine optimum.
    - "wind farm layout optimization" pushed after 2024-11-01 returns 40 repos.
    - I checked the READMEs of 8 candidates (CSRPSO-data, TheZeta/wflop, WFLOP-HGPSO, isaigm/wflo, layopt, PIBO, ElDeriuos/WFLOP, IEA37_Surrogates). None reports an IEA37 CS1 36-turbine AEP.
    - Unauthenticated code search is not available, so code files were not exhaustively searched.
16. V3R1T4S repo (github.com/elder-plinius/V3R1T4S):
    - TROPHY_CASE.md (raw, HTTP 200, 2026-11-02T23:37:54Z): no IEA, wind or turbine entry.
    - known-knowns/ (API listing, HTTP 200): 27 entries, none IEA37 or wind.
    - Issue/PR search (open and closed) for "iea37", "wind", "AEP", "turbines", "wflo" and "36 turbine" finds only:
      - #578, an open 16-turbine claim. Its body says "nothing about the 36- or 64-turbine scenarios".
      - #900, an open 16-turbine p2 claim.
      - #866, an open data-quality issue about participant 7's binned values: par7-opt36 binned sum 756896.63 against default 777475.78. That is far below the object.
      - #36, an unrelated matrix-multiplication PR.
    - Releases: none.
    - This agrees with claim/status/pr-search.json.

injection_suspected: none observed in any page read.

## Comparison and conclusion

- Strongest known 36-turbine CS1 value that is not participant 12:
  - Perez-Rua et al., WES 2023: about 865 GWh (rounded in the source).
  - Strongest exact posted value: SNOPT+WEC (participant 4), 863676.2993 MWh, file 4e-11 m outside the boundary.
  - da Silva et al. 2025: about 863.76 GWh, inferred only from search snippets.
- Object: 869713.9496 MWh, strictly feasible.
  - About 6037.65 MWh above SNOPT+WEC, so it clears the p1 threshold of 863677.2993.
  - About 4.2 GWh or more above Perez-Rua's rounded 865 GWh.
- It is not a rotation, mirror, relabelling, restriction or local polish of any published layout. In the best rigid fit, at least 27/36 turbines are more than 50 m from their partners in every published opt36 layout.
- Against participant 12, 36/36 turbines are more than 50 m away under the minimum-total-Euclidean matching (34/36 even after best rotation). So the topology is independent of participant 12, as p1 requires.
- No V3R1T4S known-known, trophy entry, or open or closed PR covers the 36-turbine cell.
- Residual gaps:
  - The da Silva 2025 full text and the KDD 2025 diffusion paper could not be opened (403 or empty pages). Snippet evidence and the diffusion paper's code repo give no sign of a value at or above the object's.
  - Unauthenticated GitHub code search was not possible.
- For the claimed scope (p1 only, explicitly not a record against participant 12), the object strictly beats every known non-participant-12 value and is not a trivial edit of a published layout.

novelty: PASS for p1 scope (not a total-energy record; participant 12's 882383.3040 remains higher)
pass: true
