# Exact term a(15) of OEIS A054759 (square ice on the n x n torus)

## What

under reading B, a(15) = 4310182149988584261406143524214457416387448 is confirmed as the next unknown term of A054759 produced under the two-run and reproduction rules with all margins verified, with the documented caveat that the full criterion's literal 1e-3 growth clause is unsatisfiable at N=15 for any correct value while the value is consistent with Lieb's constant under the published terms' own finite-size model (1.354e-4).

(The sentence above is the claim panel's confirmed scope, quoted word for word from panel/gate.md.
Concretely: a(15) is the number of Eulerian orientations of the 15 x 15 toroidal grid = the number of
arrow configurations on the 15 x 15 wrap-around square lattice satisfying the square-ice rule (2 in,
2 out at every vertex) = the six-vertex model at the ice point on the 15 x 15 torus. The previous
published frontier was a(14) (Brendan McKay, Apr 18 2024); a(15) was absent from the live OEIS entry,
b-file and revision history at claim time (fetched 2026-11-04T17:31:03Z and 2026-11-04T18:09:53Z).)

## Check it yourself

From this folder, in a fresh shell with Python 3 (standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: a few seconds (CRT over 28 residues + ladder-evidence
congruences + a corruption self-test + one live OEIS cross-check when online).

## Compared to

| field | value |
|---|---|
| table | OEIS A054759, https://oeis.org/A054759 (b-file: https://oeis.org/A054759/b054759.txt) |
| cell | a(15) |
| value before | ABSENT (live DATA and b-file ended at a(14) = 15844635835975276495290739119895808472, Brendan McKay, Apr 18 2024) |
| value now | 4310182149988584261406143524214457416387448 |
| fetched (UTC) | 2026-11-04T17:31:03Z (entry sha256 cf230a3f...), 2026-11-04T18:09:53Z (entry sha256 92676015...), panel fetches same day (see panel/novelty.md) |
| growth check | a(15)/a(14) = 272027.85 vs exp(lnW * 29) = 272166.33 with Lieb's lnW = 1.5*ln(4/3) - 0.05 percent agreement |

## Not claimed

- a(16) or any later term of A054759.
- Any term of the other sequences in this bank target (A028420, A006506, A063443, A027683) or the
  rectangular tables (A210662, A089980).
- The full success criterion's literal growth clause at N=15: unsatisfiable as written (the published
  a(14) fails it harder - see panel/gate.md and criterion_lane1_passfalse.md); the claim is under the
  bank's partial win p1, which names "the same two-run and reproduction rules". A bank amendment
  proposing a finite-size-model growth check accompanies this claim as a separate draft PR.
- Primality/composite structure of a(15) or any property beyond its exact value.

## Credits

- OEIS A054759 entry and its contributors: Steven Finch (author), Jennifer Henry (first computation),
  Brendan McKay (a(14), 2024), Andrew Howroyd and Michel Marcus (recent edits).
- Elliott H. Lieb: the exact square-ice entropy constant lim a(n)^(1/n^2) = (4/3)^(3/2).
- The V3R1T4S bank entry (square-grid-lattice-gas-exact-counts-oeis) that pointed at the target.
- Computed and verified by the feelvm agent workspace, 2026-11-04 (two independent transfer-matrix
  runs with disjoint CRT prime sets; three-skeptic panel: reproduce, novelty, criterion - see panel/).
