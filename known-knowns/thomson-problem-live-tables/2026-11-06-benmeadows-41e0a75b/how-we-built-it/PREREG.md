# PREREG: thomson-problem-live-tables, N = 436

written_utc: 2026-11-06T19:33Z

## Timing, stated plainly

The configuration was found by a search lane on 2026-11-04/05 and refined (L-BFGS plus a float64 tangent-Hessian
check) on 2026-11-05. This file was written after that, and after the certification run below was started but before
its output was read. It is not a pre-registration of the search; it freezes the judging. The criterion is quoted from
the public bank, `bank/targets.json` at https://github.com/elder-plinius/V3R1T4S (main, read 2026-11-06). No
threshold or margin below was chosen by us.

## Criterion: thomson-problem-live-tables

Quoted verbatim from the bank:

> Success means N points on the unit sphere (coordinates to >= 20 digits) for some N <= 1500 listed in at least one live table, such that E* computed in mpmath at 30 digits from the normalized coordinates is STRICTLY LOWER (direction: min) than the minimum energy for that N over ALL of: Deeter's table (https://deetour.net/oppp/thomson/, N = 4..524), CCD Thomson/table.html, CCD Thomson2/table.html, the CCD Riesz s=1 table (site/s_1/index.html), the Wikipedia table and (for N = 282) EinsteinArena, each re-fetched live immediately before claiming, by at least 1e-6 in absolute energy, AND the configuration is a certified strict local minimum (mpmath tangent-space Newton to gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0), AND it is a different basin from every posted table configuration for that N: polishing each table's own point file (Deeter e.<N>.txt, CCD xyz/<N>.xyz, Riesz dat/points_<N>_1.dat) with the same routine must give an energy higher than E* by >= 1e-6. N > 1500 (Riesz rows up to 9913) cannot be Hessian-certified in under an hour and is partial win p3 only.

Cell: N = 436.

## Tables for N = 436 (fetched 2026-11-06T19:30:58Z; URLs and sha256 in the-record-we-beat/RECORD.md)

- Deeter, https://deetour.net/oppp/thomson/: N = 436 listed, 90020.71608562, point file e.436.txt.
- CCD Thomson/table.html and Thomson2/table.html: no N = 436 row. CCD posts xyz/436.xyz; it is polished as a table
  point file anyway.
- CCD Riesz s = 1 table: starts at N = 512, so no N = 436 row.
- Wikipedia Thomson_problem: no N = 436 row. EinsteinArena: N = 282 only.

## Statistic and thresholds

- E* in mpmath (30 digits or more) from normalised coordinates; pass iff 90020.71608562 - E* >= 1e-6.
- Tangent-space Newton in mpmath to tangent gradient norm < 1e-20, E* change < 1e-12; float64 tangent Hessian with
  the three rotation modes excluded has 2N - 3 = 869 positive eigenvalues.
- Deeter e.436.txt and CCD xyz/436.xyz, each polished to a local minimum by the same routine, end >= 1e-6 above E*.
- Null test: not applicable. A deterministic construction checked against a definition, not a search or statistical
  claim.

## Panel

Three fresh skeptics (REPRODUCE, NOVELTY, CRITERION), new subagents, each seeing only the claim folder and writing its
own code; none sees the search code or our checker. The cell is dropped unless all three write `pass: true`.
