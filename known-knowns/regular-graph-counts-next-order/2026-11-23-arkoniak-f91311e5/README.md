# A006822(25): connected 6-regular graphs on 25 vertices

## What
A006822(25), the number of connected 6-regular simple graphs on 25 vertices, equals 1058090189356372623457538781723, obtained from U_6(25)=1058090189356373578845816711343 computed by a histogram-recurrence method and by a separate per-cycle-type vertex-DP method (both Burnside-based) that agree exactly, with the second method's code reproducing A165627 n=0..24 and, via inverse Euler, A006822 n=0..24 with no mismatch.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library). Expected last line: `PASS`. Rough laptop time: about 10 minutes on one core (method A recomputes all 1958 cycle-type values; 574.5 s measured).

## Compared to
OEIS A006822 b-file, https://oeis.org/A006822/b006822.txt, fetched 2026-11-23T01:50:31Z (HTTP 200): it ends at n=24 (5782740798229825207562109439); there is no n=25 entry. Details in the-record-we-beat/RECORD.md.

## Not claimed
- Nothing about A006822(26) or later terms, nor about any other degree.
- The two methods share the Burnside/cycle-type frame and the inverse Euler transform; they differ in how Fix(lambda) is computed (histogram recurrence vs vertex DP plus count-vector DP). The shared frame is exercised by reproducing every published A165627 and A006822 term.
- The per-type values in object/F_N25.txt are method D's; check (2) of verify-it-yourself recomputes each with method A.

## Credits
- M. Meringer, Tables of Regular Graphs (http://www.mathe2.uni-bayreuth.de/markus/reggraphs.html), and GENREG; J. Kimberley's extensions, as credited on OEIS A006822 (https://oeis.org/A006822) and A165627 (https://oeis.org/A165627): the published terms to 24 vertices that this result extends.
- Cheng and Xu, arXiv:2609.31407 (https://arxiv.org/abs/2609.31407): the histogram recurrence used by method A (they apply it to quartic graphs).
- Andrew Howroyd's programs on OEIS for counting regular graphs over cycle types.
- The OEIS Foundation for the b-files.
