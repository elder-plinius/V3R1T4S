# A006821(15): connected 5-regular graphs on 30 vertices

## What
A006821(15) = 1690586697346784893842479211750187 (with U_5(30) = 1690586697369281612308192667831589) is computed by two separately coded exact methods that agree on U_5(30), and method D reproduces all b-file terms of A006821 (n=1..14) and A165626 (n=0..14) through the inverse Euler transform.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library and gcc). Expected last line: `PASS`. Rough laptop time: about 5 minutes on one core (method A recomputes U(30); 272 s measured).

## Compared to
OEIS A006821 b-file, https://oeis.org/A006821/b006821.txt, fetched 2026-11-24T02:19:45Z (HTTP 200): it ends at n=14 (322040154704144697047052726990); there is no n=15 entry. Details in the-record-we-beat/RECORD.md.

## Not claimed
- Nothing about A006821(16) or later terms, nor about any other degree.
- The two methods share the Burnside/cycle-type frame and the inverse Euler transform; they differ in how Fix(lambda) or U(N) is computed (histogram recurrence vs vertex DP plus count-vector DP). The shared frame is exercised by reproducing every published A165626 and A006821 term.
- The per-type values in object/F_N30.txt are method D's; check (3) of verify-it-yourself recomputes U(30) with method A.
- A first panel (2026-11-22) left this claim at PROMISING because its novelty skeptic could not read some sources; the human checked those by hand on 2026-11-23, and a fresh three-skeptic panel on 2026-11-24 passed it (panel/).

## Credits
- M. Meringer, Tables of Regular Graphs (http://www.mathe2.uni-bayreuth.de/markus/reggraphs.html), and GENREG; the contributors credited on OEIS A006821 (https://oeis.org/A006821) and A165626 (https://oeis.org/A165626) for the published terms to 28 vertices that this result extends.
- Cheng and Xu, arXiv:2609.31407 (https://arxiv.org/abs/2609.31407): the histogram recurrence used by method A (they apply it to quartic graphs).
- Andrew Howroyd's programs on OEIS for counting regular graphs over cycle types.
- The OEIS Foundation for the b-files.
