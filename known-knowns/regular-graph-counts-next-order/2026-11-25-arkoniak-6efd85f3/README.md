# Quartic graph counts, orders 29..50: an independent recomputation of Cheng and Xu's Tables 4 and 5 (partial win p1)

## What
For every order N=29..50, an independent Burnside sum over all p(N) cycle types (method D, exact mod 2^521-1) gives unlabeled quartic totals equal to the C implementation of the histogram recurrence (method A) and to Cheng-Xu's Table 4, and the inverse-Euler connected counts equal Table 5 (MISMATCH 0), with per-type D vs A agreement shown only at N=30; nothing at order 51 or above.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library and gcc). Expected last line: `PASS`. Rough laptop time: about 2 minutes on one core (method A recomputes U(5..36); 98 s measured).

## Compared to
Cheng and Xu, "Exact counting of unlabeled quartic graphs by permutation-cycle aggregation", arXiv:2609.31407 (https://arxiv.org/abs/2609.31407), Table 4 (all quartic graphs, n=29..50) and Table 5 (connected, n=29..50); abstract page fetched 2026-11-25T01:49:20Z (HTTP 200). All 22 orders of both tables agree. The OEIS b-files of A033301 and A006820 (fetched 2026-11-25T01:49:20Z, HTTP 200) end at n=28 and agree with our values for n<=28. Details in the-record-we-beat/RECORD.md.

## Not claimed
- No value at order 51 or above, and no new OEIS term: these are Cheng and Xu's published values, recomputed.
- Per-type agreement between the two methods (F_D(lambda) == F_A(lambda) for every cycle type) was checked only at N=30; for the other orders the two methods agree on the totals U_4(N).
- Method A uses the same histogram recurrence that Cheng and Xu describe, so independence from their computation rests on method D (a separately coded per-cycle-type count). Both methods share the Burnside frame and the inverse Euler transform.
- object/F_N29.txt holds method D's per-type values at N=29 only; the per-type files for N=30..50 (up to about 20 MB per order) are not in this package.

## Credits
- Cheng and Xu, arXiv:2609.31407 (https://arxiv.org/abs/2609.31407): the published table recomputed here and the histogram recurrence used by method A.
- M. Meringer, Tables of Regular Graphs (http://www.mathe2.uni-bayreuth.de/markus/reggraphs.html), and GENREG; the contributors credited on OEIS A006820 (https://oeis.org/A006820) and A033301 (https://oeis.org/A033301).
- Andrew Howroyd's programs on OEIS for counting regular graphs over cycle types.
- The OEIS Foundation for the b-files.
