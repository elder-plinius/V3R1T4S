# OEIS A089980 Antidiagonal d = 79 (`square-grid-lattice-gas-exact-counts-oeis` Partial Win `p2`)

## What

The complete 80-entry antidiagonal d = 79 (b-file indices 3160..3239, canonical widths w = 0..39 peaking at the 279-digit T(39, 40) = 254735682081189541344081503360736788844774937958504869716096214590338245178492823863429255507628678700444558564935870046594368781174025731139175661159108554557238150761113808065611962133371021250718485742976243397588856426972383225337965855119190243350002187880478598136326595377) of OEIS A089980 in claim/a089980_antidiag79.txt (sha256 918a1787709ce8d30985fe62d7cf067072f66d3edf34e5c99718541f3b7f0ed6) is confirmed under partial win p2's two-run rule (40/40 widths agreed between MSB-first boustrophedon broken-profile DP modulo 37 primes in (2^30, 2^31) and LSB-first butterfly column-transfer DP modulo 38 disjoint primes in (0, 2^30), plus exact big-integer column transfer on w = 0..16, all 40/40 held-out check primes passing) and reproduction rule (0 mismatches across all published cells d <= 78 in claim/b089980.txt); at (39, 40), T(39, 40)^(1/1560) = 1.5082225930 vs Baxter's hard-square constant 1.5030480825 (open-boundary finite-size gap +0.005175, monotonically decreasing from +0.005241 at (39, 39) and +0.005311 at (38, 39)).

OEIS `A089980` tabulates $T(w, m)$, the number of independent vertex sets (hard-square lattice-gas configurations) on the $w \times m$ rectangular grid graph $P_w \times P_m$, read by rising antidiagonals $d = w + m \ge 0$. The published OEIS b-file `b089980.txt` (`n = 0..3159`) ends at antidiagonal $d = 78$. This package supplies `object/a089980_antidiag79.txt` (`15,242` bytes, `sha256: 918a1787709ce8d30985fe62d7cf067072f66d3edf34e5c99718541f3b7f0ed6`), containing all `80` exact entries (`n = 3160..3239`) of antidiagonal $d = 79$, along with the complete two-decomposition modular residue tables `object/residues_hs_mod.tsv` and `object/residues_far.tsv` and exact big-integer table `object/antidiag79_indep_bigint.tsv`.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `ALL CHECKS PASS` (~2 seconds). See `RUN_IT_YOURSELF.md` for full details.

## Compared to

| sequence | row / cell | our value (at central peak $T(39, 40)$, `n = 3199`, `279` digits) | previous published row ($d = 78$, central peak $T(39, 39)$, `n = 3120`, `272` digits) | source | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A089980 | Antidiagonal $d = 79$ (`n = 3160..3239`, `80` entries) | `254735682081189541344081503360736788844774937958504869716096...326595377` (`279` digits) | `298556124475442741590313898130272393354970149904914940364871...330411607` (`272` digits) | `https://oeis.org/A089980/b089980.txt` | `2026-10-18T19:47:12Z` |

## Not claimed

- This is **enumerated partial win `p2`** ("A new row of an associated rectangular table (A210662 monomer-dimer m x n, A089980 hard squares m x n) extending the largest published m by one for all n up to the published range, same rules"), not the main diagonal target (`A028420`, `A006506`, or `A063443`).
- On open-boundary $w \times m$ grids at $w \le 40$, the perimeter $2(w+m)$ contributes a positive $O(1/w)$ finite-size excess to $T(w, m)^{1/(wm)}$ (`1.5082225930` vs Baxter's bulk constant $\kappa = 1.5030480825$, gap `+0.005175`, monotonically decreasing from `+0.005241` at $(39, 39)$ and `+0.005311` at $(38, 39)$).
- No claim is made for antidiagonal $d \ge 80$.

## Credits

- **Contributor:** [mizopl](https://github.com/mizopl). Computed and verified in V3R1T4S runs `2026-10-17-1708`, `2026-10-17-1754`, `2026-10-17-1913`, and `2026-10-17-2208`, audited by a 3-skeptic panel (`REPRODUCE`, `NOVELTY`, `CRITERION`).
- **Prior OEIS A089980 authors and contributors:** Alois P. Heinz, Andrew Howroyd, and Kai Liang (`arXiv:2505.12776`, `arXiv:2507.04007`, antidiagonals $d = 0..78$).
- **Rodney J. Baxter:** Hard-square lattice-gas transfer-matrix theory and bulk entropy constant $\kappa$.
