# Reproduction of the frozen Hornsea One capacity-6 object

The explicit object satisfies the frozen release-r26.10-v4 reproduction criterion. This report concerns deterministic identity, feasibility and length comparison only; it makes no novelty or optimality finding.

The examination began in a fresh subagent context. Scientific inputs were confined to `claim-ho6/` and installed public OptiWindNet definitions. No other panel, prior result, author search code or author reproduction code was read. The independently written checker was saved before inspecting OptiWindNet's storage/encoding implementation; its initial SHA-256 was `8f03a063b0d8a12d7279cba33cba3fe1eae2c794562248110f0d0aae8deacffc`, unchanged at completion. Its scratch implementation is explicitly excluded from any future public claim package. All writes were confined to `panel-ho6/`, with code and intermediate data confined to `panel-ho6/work-reproduce/`; the claim was read only.

## Definition applied

The complete operative success criterion in `claim-ho6/criterion.txt` is:

> For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!', and topology X (radial or branched), a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared.

The independent graph check requires a forest, exactly one root in each connected component, all release turbines present, and at most six turbines in each component after removing roots. It counts each root's incident cables and sums Euclidean length for every cable, including separate coincident cables. Whole-segment containment uses the closed border polygon's `covers` predicate with no buffering or tolerance. Obstacle interiors are excluded. Every unordered segment pair is inspected for proper crossings, overlaps and contacts. OptiWindNet's additional full-polyline, shared-corridor and branch-split semantics are tested by its official validator with unchanged defaults; no tolerance was widened.

## Identity and reconstruction

`claim-ho6/references/optiwindnet-routesets-r26.10-v4.sqlite.xz` hashes to the criterion's exact SHA-256:

`c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a`.

The release contains exactly one nodeset named `Hornsea One.1_OSS`: T=174, R=1, B=25, VertexC shape (200,2), constraint groups `[25]`, and no obstacles. Its name has no `!` prefix. Every coordinate, including all turbine, substation and border vertices, is exactly array-equal and byte-equal between the pickle's VertexC array and the independently loaded release blob. Border indices are exactly equal; obstacle lists are both empty. The release border polygon is valid.

The packed JSON was rebuilt against this release geometry by an independent parent-slot decoder: source is slot for slots below T, otherwise slot+B; targets come from `edges`; clone coordinates come from `clone2prime`. This did not use the author or official decoder. A separate rebuild using public `TerseLinks.to_routeset` agreed. Both rebuilds, the pickle, and `segments.json` have precisely identical node-indexed edges and endpoint coordinates, including every clone/detour. No geometric matching tolerance was needed.

Frozen object SHA-256 values:

| File relative to claim | SHA-256 |
|---|---|
| `object/G.pickle` | `830846712933194587af3a23234781c9a77423a881ec25f520ed97bd21de9e41` |
| `object/routeset-packed.json` | `38e89fe442554d209a8e5d4d17bdd0546dc8e19294c60e30707101f76b8b4b44` |
| `object/segments.json` | `b06859d806e341c850264459f1f0f8bb0fa7c2039b253da4e3b803f1273f6395` |

## Exhaustive feasibility and length

The pickle and independent rebuild each have 202 nodes and 201 edges, one connected acyclic component and one root. Removing that root gives 30 feeders with turbine counts `[1,5]` followed by 28 six-turbine feeders. Thus every one of the 174 turbines reaches the root, capacity is respected, and the root uses exactly the allowed 30 feeders. Maximum turbine degree is 3, so the submitted branched description is appropriate. An independent reverse root traversal reproduces every stored edge load and root total 174. Every segment has positive length. Maximum discrepancy between a stored per-edge length and direct Euclidean computation is 9.095e-13 m.

All 201 complete segments lie in the closed site polygon. There are no obstacles. All 20,100 unordered segment pairs were inspected: zero proper transverse crossings, 45 coincident segment pairs and 142 contacts between edges with distinct graph-node identifiers. These latter counts disclose clone/corridor co-location rather than silently discarding it. Public OptiWindNet definitions permit shared corridor traversals unless they swap sides at both ends; the official full-route checks return no crossings, overlap-crossings, self-intersections or branch splits.

`optiwindnet.validating.validate_routeset` returns exactly `[]` for the original pickle, the independently rebuilt packed graph and the additional official packed rebuild.

The sum over all 201 cable segments, including detours and each coincident cable separately, is **449188.82031142124 m**, exactly the submitted packed total at the printed binary64 precision.

The SQLite query selected every row for the exact nodeset digest and capacity 6, without filtering by creator or topology. It returned four rows, all radial or branched. Every stored graph was also independently decoded against the release coordinates and its Euclidean length recomputed:

| Routeset | Topology | Release length (m) | Recomputed length (m) | Feeders |
|---:|---|---:|---:|---|
| 45811 | radial | 450092.351727352 | 450092.351727352 | [30] |
| 2799 | branched | 451220.99185956945 | 451220.99185956956 | [30] |
| 9634 | radial | 452600.50812744885 | 452600.50812744873 | [29] |
| 8922 | radial | 464173.546237935 | 464173.546237935 | [30] |

The candidate is shorter than `(1-1e-6)` times every release and independently recomputed comparator length. The binding threshold is 450091.90163500025 m, derived from row 45811. The improvement over that row is 903.5314159307745 m, or 0.2007435612854177%. Its [30] feeder count supplies the criterion's per-root cap. No straight-line solver objective or reported restricted-solve bound is used in this comparison.

## Invalid controls

All deliberate failures were detected:

- Capacity reduced to 5: independent capacity failure; official `κ = 5, max_load = 6`.
- One root feeder removed: independent component-root failure; official 168 reachable terminals versus 174, with six disconnected turbine IDs identified.
- Feeder allowance reduced to 29: independent feeder-cap failure.
- Synthetic segment leaving the site: independent exact containment failure.
- Synthetic segment entering an obstacle: independent obstacle-interior failure.
- Synthetic crossing: independent crossing failure and official self-cross at `POINT (0 0)`.
- One submitted edge load increased by one: official `link 0–218 states load 7, carries 6`.

## Execution record

Environment: OptiWindNet 0.3.2, NumPy 2.5.4, NetworkX 3.7, Shapely 2.2.0. No solver was run. Python bytecode writes were disabled and OpenBLAS, OMP, MKL and NumExpr threads were set to one. Commands below were executed from the run directory; all listed paths are relative to that directory:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 ../../.venv-optiwindnet/bin/python panel-ho6/work-reproduce/run.py > panel-ho6/work-reproduce/output.txt
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 ../../.venv-optiwindnet/bin/python panel-ho6/work-reproduce/supplement.py > panel-ho6/work-reproduce/supplement-output.txt
```

Both exited 0. The first run's release setup used Python `lzma.open` and `shutil.copyfileobj` to decompress the pinned release into `panel-ho6/work-reproduce/release.sqlite`. Full row-level comparator data and exhaustive intersection findings are retained in scratch, not proposed as public-package artifacts.

| Scratch artifact relative to `panel-ho6/work-reproduce/` | SHA-256 |
|---|---|
| `checker.py` | `8f03a063b0d8a12d7279cba33cba3fe1eae2c794562248110f0d0aae8deacffc` |
| `run.py` | `d862b320740f1e53810aa60d4eaf39d37134af312408a6e27ceb20dcc2e16266` |
| `supplement.py` | `60ab0fd0939c16cf668facb4d8b5c01bd39729fe448a76c0ad0d88250af78208` |
| `output.txt` | `1672d05774e1947be260d2196afd887be6b6effee1913e945e2b30495a226a5f` |
| `supplement-output.txt` | `41b64b786f832188fc5eb5a668b9e50aad1be792483cf7afaafd74bdf710c8b1` |
| `results.json` | `58b30361206ac1ed494e4ee9678c00a2dd1ba767903a6cf3ad4d377fb2796c98` |
| `supplement.json` | `50c17932be452ebddcd2d217e80aadd81a5dad16c543dd18c04afc6221420087` |
| `comparators.json` | `64801c1034cecb7a8ecd4de6ce5b35a34f5f9d2859553f4895985169be5f7633` |

The installed public `optiwindnet.validating` source hashes to `ef522fd8a89761757229662a7c310c217fc26da6ca3035a151f3e8598730bafa`; `optiwindnet.crossings` hashes to `a56f622720d259a111d1c2e2398149dc1aabc6c70fb611faa67ad43a79206c61`. This pass is scoped to the frozen release and objects identified above.

context: fresh subagent (claim-ho6 only)

pass: true
