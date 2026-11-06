# HSP4 N=119 explicit packing

## What

For HSP4 N=119, candidate.txt has mpmath-50 feasible radius 0.23606892889364886505664445893098935298010907228947, exceeding the freshly verified Packomania row and supplied Moki & Julio certificate with the specified non-isometry, history and category-queue conditions satisfied; the category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle remains unresolved, and N=119 must be re-checked against the live table when that bundle disappears.

The referenced candidate.txt is object/candidate.txt. The full 50-digit feasible radius is 0.2360689288936488650566444589309893529801090722894663. The distributed exact-rational checker certifies the conservative radius 0.23606892889364886505.

## Check it yourself

Run `python verify-it-yourself/check.py` (standard library only), or `sh verify-it-yourself/run_checks.sh`. Expected last line: `PASS`. It checks the pinned file, every pair and wall inequality, the dated table improvement and a certified non-isometry witness. It does not contact live sources.

## Compared to

Packomania, Eckard Specht, [HSP4 radius table](https://packomania.com/hsp4/txt/radius.txt), N=119: 0.236068068183. Latest verification fetch: 2026-10-17T01:24:13.400712+00:00; HTTP 200. SHA256 and exact comparison receipt are in the-record-we-beat/record.json. The gain is 0.000000860710648865056644458930989353.

The unresolved Moki & Julio 4666-candidate bundle remains a caveat. Recheck N=119 against the live table when that bundle disappears from [the pending list](https://packomania.com/pending-requests.html).

## Not claimed

No optimality, accepted table entry, global priority, improvement for another N, or absence from the unspecified pending bundle is claimed. Nothing has been submitted to Packomania or GitHub.

## Credits

Eckard Specht and [Packomania](https://packomania.com/hsp4/hsp4.html) supplied the baseline table and configuration. The success criterion is the V3R1T4S bank target packomania-hyperspheres-hsp4-hsp6. Sequential linear programming was implemented locally using SciPy/HiGHS; original search source and pinned package versions are included.

Moki & Julio receive credit for the stronger public [HSP4 certificate](https://github.com/Hashirama1337s/moki-julio-circle-packing): its recomputed N119 radius is 0.2360686959792902894654488326491620389779247149658949, which this object improves by 0.000000232914358575591195626281827314. The exact checker proves the comparison against a dated upper-bound witness; it does not assume the published certificate header is exact. The full source-object recheck below can independently regenerate those witnesses.

Typical offline geometry check time: a few seconds on a laptop.
