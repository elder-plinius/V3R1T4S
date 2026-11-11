# Novelty review: Hornsea One.1_OSS, capacity 2

context: novelty skeptic of a three-person panel, fresh context; read only the claim folder `claim-ho2/` (frozen, not modified) and public web sources; scratch work in `panel-ho2/work-novelty/`; official validator environment optiwindnet 0.3.2.

## Verdict

The object is strictly shorter than every route set I could find for this instance (1030454.2878 m against 1031350.3996 m, 896.1118 m or 0.087% shorter). It is a very small edit of the named seed (5 of 174 links), but the edit is a combinatorial re-pairing that none of the listed trivial edits reproduces. Pass.

## Status source (fetched once)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Time: 2026-11-10T14:57:13Z, HTTP 200, resolved to record 23537067 (no retry).
- Value: latest version is still record 23537067, "OptiWindNet RouteSets", publication date 2026-10-21, modified 2026-10-21T15:29:56Z, flagged `is_last: true`; single file `optiwindnet-routesets-r26.10-v4.sqlite.xz`, 28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7.
- `references/optiwindnet-routesets-r26.10-v4.sqlite.xz` has the same md5 and the sha256 stated in `CLAIM.md` (c78c8f3c...e3a). `status/zenodo-latest.json` agrees with the live answer. The table has not changed since the claim was built.

## Stored sets for the instance (release r26.10-v4, recomputed)

| id | creator | topology | feeders | length (m) |
|---|---|---|---|---|
| 42234 | MILP.pyomo.cplex | radial | [87] | 1031350.3996 |
| 9595 | baselines.hgs | radial | [87] | 1031350.3996 |
| 8881 | baselines.lkh | radial | [87] | 1032129.6496 |
| 2782 | MILP.pyomo.cplex | branched | [88] | 1032792.2112 |

Lengths recomputed from the stored links match the stored `length` column. The object (`object/routeset-packed.json`, `object/segments.json`, `object/G.pickle`) recomputes to 1030454.2878 m with 87 feeders, maximum turbine degree 2, and `validate_routeset` returns no violations. The stored MILP bounds (1026484.83 radial, 1026124.42 branched, straight-line objective) are below the object's straight-line length 1026786.07 m, so nothing contradicts a bound.

## Comparison with the seed (id 42234) and the other stored sets

Turbine-level links (detour nodes collapsed), object against each stored set:

| stored id | links in common (of 174) | differing links | turbines touched |
|---|---|---|---|
| 42234 (seed) and 9595 | 169 | 5 | 6, one cluster |
| 8881 | 111 | 63 | 72, four clusters |
| 2782 | 102 | 72 | 86, four clusters |

The whole difference from the seed is one local move. Three strings {168,171}, {166,169}, {172,173} become {166,168}, {169,172}, {171,173}; two feeder attachments move (168 and 172 to 169 and 171). All other 169 links have identical routed geometry in both sets, so the full 896.1118 m gain comes from these five links (585.26 m of it straight-line, the rest from shorter detours on the re-paired strings).

Test of the listed trivial edits on the stored sets:

- Local numerical polish: re-routing each stored topology with optiwindnet's PathFinder, default limits and raised limits (200000 iterations, 10 traversals), under both radial and branched re-hooking rules, returns exactly the stored lengths (1031350.3996 for 42234 and 9595; 1032129.6496; 1032792.2112). No gain.
- Deletion and restriction do not apply (all 174 turbines must be connected). Relabelling and symmetry do not change length.
- Neighbouring cells: capacity 3 of the same nodeset uses three-turbine strings (58 feeders), not feasible at capacity 2; "Hornsea One" (3 substations) is a different nodeset. No stored set there yields this object by a trivial edit.

So the seed is named in `CLAIM.md`, and the object beats what those edits alone give (1031350.3996 m) by 896.11 m. The edit is small: readers should understand the result as one 3-string exchange on a solution that CPLEX and HGS both left at the same value, not a new solution structure.

## Prior art searched

- github.com/elder-plinius/V3R1T4S pull requests, open and closed, all 1000 listed on 2026-11-10T23:00Z (titles and bodies): 18 concern this benchmark; for Hornsea One.1_OSS they cover capacities 5 to 12 only (#967, #968, #977 to #982). None for capacity 2. Issue search for "Hornsea" gives the same set.
- `TROPHY_CASE.md` (main): no mention of Hornsea, OptiWindNet or cable routing. `known-knowns/`: no folder for this target.
- Zenodo 20053479 (RouteSets r26.05-v4, the only other version of the record): same four capacity-2 rows, same lengths.
- Zenodo 18864643 and 19798734 (`paperdb.v3`, `paperdb.v4`, `MILP_model_comparison.v3/v4`): nodeset "Hornsea One.1_OSS" with identical coordinates; capacity 2 holds ids 9595 (1031350.3996) and 2782 (1032792.2112). No other nodeset with 174 turbines is congruent to it (pairwise-distance signature, so rotation and renaming are covered).
- Zenodo 20140812 (thesis artifacts): notebooks and figures only, no route sets, no mention of Hornsea.
- DTUWindEnergy/OptiWindNet: tree holds only site definitions (`Hornsea One.yaml`); releases v0.1.6 to v0.3.2 carry only wheel and source assets.
- Preprint wes-2026-124 (abstract page, 2026-07-28, in review): describes the dataset; no separate values. Two web searches found no other publication of a shorter set for this instance.

Not checked: the full text of the preprint PDF (no PDF text tool available) and its discussion comments; web search was limited to two queries.

## Conclusion

Best known before the claim: 1031350.3996 m (ids 42234 and 9595, also in the 2025 datasets). Object: 1030454.2878 m, same feeder count [87], relative improvement 8.7e-4, above the 1e-6 threshold. Not a tie; not reproduced by trivial edits of any published set.

pass: true
