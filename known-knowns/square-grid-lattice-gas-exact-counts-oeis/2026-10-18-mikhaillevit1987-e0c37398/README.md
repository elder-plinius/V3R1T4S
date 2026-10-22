# A054759(16) = 2781781827849835218619790131266486746689884618378

## What

Panel gate status: **PROMISING** (not a confirmed partial win; see "Not claimed"). The gate's confirmed_scope, verbatim:

Two runs of claim/checker/ice.rs (left-to-right sweep with full symmetry reduction vs right-to-left sweep with shift-only reduction, on disjoint sets of four primes) saved residues whose CRT values agree for every n = 1..16, reproduce the 14 published A054759 terms exactly, and give 2781781827849835218619790131266486746689884618378 for n = 16; this value is consistent with the finite-size trend, but it is not the first unknown term a(15), so it does not meet p1 as literally worded.

Since the gate, the REPRODUCE skeptic (fresh context, own Rust checker written from the definition, own primes,
modulus 2^64 x four primes > 2^272 >= a(16)) recomputed a(16) twice with two different symmetry reductions and got
the same integer; the author's program on the skeptic's fresh primes agrees as well (`panel/reproduce.md`).

The object is `object/a054759_16.txt`: one decimal integer, the number of Eulerian orientations (square ice
configurations) of the 16 x 16 torus grid graph, OEIS A054759 at n = 16.

## Check it yourself

From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3, standard library). Expected last line: `PASS`.
About 10 seconds on a laptop. It recomputes a(1..9) with an independent exact transfer matrix, checks every prime,
and checks the claimed integer against all five saved runs, two of which have a modulus above the bound 2^272.
It does not recompute a(16) itself; that takes Rust and about 5-25 minutes on 6 cores (`how-we-built-it/COMMANDS.md`).

## Compared to

OEIS A054759, https://oeis.org/A054759 and its b-file https://oeis.org/A054759/b054759.txt: the last known term is
a(14) (Brendan McKay, Apr 18 2024). Fetched 2026-10-18T10:07:50Z by the author and again by the NOVELTY skeptic at
2026-10-18T11:45:20Z (b-file sha256 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada). Open pull
request #366 in this repository claims a(15) only. See `the-record-we-beat/README.md`.

## Not claimed

- Not the next unknown term: a(15) is the first term missing from OEIS, and it is claimed first in open PR #366
  (mizopl). Our a(15) = 4310182149988584261406143524214457416387448 agrees with #366 (also by an independent
  sector-matrix method in `how-we-built-it/sector_trace.py`); priority for a(15) is theirs.
- The CRITERION skeptic failed this claim for that reason (`panel/criterion.md`, pass: false); the gate kept it at
  PROMISING. This package is submitted at the contributor's explicit request despite that.
- Not the main target (the hard-square / lattice-gas constants). No closed form, no asymptotics.
- For information only, not panelled: a(17) = 4251688273930945011485684711076896006927401676575591292 from the same
  program, modes A and B on disjoint primes, equal CRT values (`how-we-built-it/results.jsonl`, n = 17).

## Credits

- Sequence: OEIS A054759; a(14) by Brendan McKay (2024); earlier terms by the authors credited on the OEIS page.
- a(15): first claimed by mizopl, https://github.com/elder-plinius/V3R1T4S/pull/366 .
- Method background: E. H. Lieb, Residual entropy of square ice, Phys. Rev. 162 (1967) 162-172 (six-vertex row
  transfer matrix, W = (4/3)^(3/2)).
- Computed by MikhailLevit1987 with an AI research agent following the V3R1T4S kit.
