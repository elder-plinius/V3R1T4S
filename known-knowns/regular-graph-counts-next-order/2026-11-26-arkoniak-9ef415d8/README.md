# Connected quartic graphs on 51 vertices: C_4(51), beyond Cheng and Xu's table (orders to 50)

## What
Two separately implemented Burnside-over-cycle-type computations (method D per-type extraction mod 2^521-1, and method A C histogram recurrence mod 62-bit primes with CRT) agree exactly on U_4(N) for every N up to 51, and their inverse Euler transform gives C_4(51) = 152556958807091391617335751728584931970607218791861386 connected 4-regular graphs on 51 vertices; the method-D code reproduces every term of the A033301 and A006820 b-files (n<=28) and Cheng-Xu Tables 4-5 (orders 29-50).

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library and gcc). Expected last line: `PASS`. Rough laptop time: about 2 minutes on one core (method A recomputes U(5..36); 98 s measured). Check (6) compares U(51) with method A's stored U_A(51); recomputing method A to N=51 (`--nmax 51`) takes longer.

## Compared to
Cheng and Xu, arXiv:2609.31407 (https://arxiv.org/abs/2609.31407): Tables 4 and 5 end at order 50 (v1 only, abstract page fetched 2026-11-26T02:07:40Z, HTTP 200). OEIS A006820 (https://oeis.org/A006820, b-file https://oeis.org/A006820/b006820.txt fetched 2026-11-26T02:07:39Z, HTTP 200) ends at n=28. No published value at order 51 was found (panel/novelty.md). Details: the-record-we-beat/RECORD.md.

## Not claimed
- Only order 51 (one cell). Order 52 and later are not claimed here.
- Per-type agreement between the two methods (F_D(lambda) == F_A(lambda) per cycle type) was checked only at N=30; at N=51 the two methods agree on the total U_4(51), from which C_4(51) follows by the inverse Euler transform with U_4(0..50).
- Method A uses the histogram recurrence that Cheng and Xu describe; method D is a separately coded per-cycle-type count. Both share the Burnside frame and the inverse Euler transform.
- object/F_N29.txt holds method D's per-type values at N=29 only; the N=51 per-type files (two files of about 7 MB each) are not in this package.

## Credits
- Cheng and Xu, arXiv:2609.31407 (https://arxiv.org/abs/2609.31407): the published table recomputed here and the histogram recurrence used by method A.
- M. Meringer, Tables of Regular Graphs (http://www.mathe2.uni-bayreuth.de/markus/reggraphs.html), and GENREG; the contributors credited on OEIS A006820 (https://oeis.org/A006820) and A033301 (https://oeis.org/A033301).
- Andrew Howroyd's programs on OEIS for counting regular graphs over cycle types.
- The OEIS Foundation for the b-files.
