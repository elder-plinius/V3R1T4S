# A002851(21): connected cubic graphs on 42 vertices

## What
A002851(21)=264592224929900091377 (connected cubic graphs on 42 vertices, one order beyond a saved b-file ending at n=20) is obtained by two separately coded Burnside-type methods that agree on all 53174 cycle types and on U(42)=264928974203634896907, with the method-D code reproducing A002851(1..20) and A005638(1..20) exactly through the inverse Euler transform.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (Python 3, standard library only; about 20 s on a laptop). Expected last line: `PASS`.
It recomputes every one of the 53174 per-cycle-type values F(lambda) with method A, compares them with the method-D values in `object/`, sums the Burnside formula to U(42) = 264928974203634896907, and applies the inverse Euler transform with the published A005638(1..20) to get C(42) = A002851(21).

## Compared to
OEIS A002851 b-file, https://oeis.org/A002851/b002851.txt, fetched 2026-11-19T01:52:53Z (HTTP 200): last term n=20 (40 vertices), 8832736318937756165; no n=21. A005638 (all cubic graphs) also ends at n=20 (https://oeis.org/A005638, fetched by the novelty panelist 2026-11-19T01:57:27Z, HTTP 200).

## Not claimed
- A005638(21) = U(42) = 264928974203634896907 is an intermediate of the same computation, not a separate claim here.
- No claim about A002851(22) or later terms, or about any other degree.
- The two methods were written within this project; they share the definition of F (labeled cubic graphs fixed by a permutation of a given cycle type) and nothing else (method A: histogram recurrence of Cheng and Xu; method D: closed configuration-model formula for fixed points and 2-cycles plus a residual-degree DP for longer cycles).

## Credits
- R. W. Robinson and N. C. Wormald (1983), as credited on OEIS A002851 (https://oeis.org/A002851) and A005638 (https://oeis.org/A005638): the published terms to 40 vertices that this result extends.
- Cheng and Xu, arXiv:2609.31407 (https://arxiv.org/abs/2609.31407): the histogram recurrence used by method A (they apply it to quartic graphs).
- OEIS A002829 (https://oeis.org/A002829), labeled cubic graphs: the identity term used as a gate.
- Andrew Howroyd's programs on OEIS A005638 (https://oeis.org/A005638) for counting regular graphs over cycle types.
- The OEIS Foundation for the b-files.
