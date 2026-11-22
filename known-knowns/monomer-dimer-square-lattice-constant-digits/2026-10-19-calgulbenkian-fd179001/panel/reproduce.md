# reproduce report, md-p1-enclosure-13

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Scope: package folder checked against the contributor's hash list (14 of 14 files OK), copied to a private location, all work done there. No network. My checker (not shipped in this package) was written and run BEFORE I opened verify-it-yourself/ or any author code.

## Definition (quoted from object/PROOF.md section 0, then re-derived by me)
"For m >= 3 let P_m be the 2^m x 2^m matrix indexed by subsets s,t of Z_m (cyclic row of m sites): P_m[s,t] = 0 if s and t intersect, otherwise the number of matchings of the subgraph of the m-cycle induced on the sites outside s u t. beta(m) := rho(P_m)."
Claim: rigorous enclosure 0.6627989728337138109756 <= h2 <= 0.6627989728337490653104 (13 decimals) from Collatz-Wielandt on widths 22 and 24 (Theorem U with M = 22, Theorem L with 2q = 22, p = 2).

## Proof steps re-derived (both inequalities, by hand, from the definitions)
- Torus identity: Tr P_m^L = matchings of C_m x C_L for m, L >= 3 (sum over the sets s_r of vertical edges used between rows; horizontal edges in a row form a matching of the cycle induced on the sites not in s_{r-1} u s_r). Checked numerically from brute-force matchings: (m,L) = (3,3) 370, (3,4) 2764, (4,4) 41025, (3,5) 19874, (4,5) 576287, all equal (output not shipped).
- P_m is real symmetric and nonnegative, so rho = largest eigenvalue and |lambda| <= rho. For even L, Tr B^L = sum lambda^L >= rho^L (S1) and <= 2^m rho^L (S2); Tr B^(p+2q) <= rho^p Tr B^(2q) (S3). All hold.
- Theorem U: for even M >= 4 and any m >= 3, beta(m)^M <= Tr P_m^M = Tr P_M^m <= 2^M beta(M)^m, so ln beta(m)/m <= ln2/m + ln beta(M)/M. Letting m go to infinity uses lim ln beta(m)/m = h2, shown in section 4 of the proof (torus matchings <= 2^(m+L) Z(m,L) <= 2^(m+L) e^(h m L), plus the open-strip lower bound and Fekete). I found no gap. M = 22 is even and >= 4.
- Theorem L: beta(m)^p >= Tr P_m^(p+2q) / Tr P_m^(2q) (S3); both exponents >= 3 so the torus identity applies; for even m, Tr P_(p+2q)^m >= beta(p+2q)^m and Tr P_(2q)^m <= 2^(2q) beta(2q)^m; divide by m and let m go to infinity along even m: p h2 >= ln beta(p+2q) - ln beta(2q). Hypotheses for the used values: q = 11 >= 2, p = 2 >= 1, p + 2q = 24, 2q = 22, all cycle lengths >= 3. Met.
- Collatz-Wielandt (S4): for B >= 0 and x > 0, min (Bx)_i/x_i <= rho(B) <= max (Bx)_i/x_i. Upper via the row sums of D^-1 B D; lower via B symmetric and a nonnegative Perron vector v with v.x > 0. I checked both and the hypotheses (B symmetric nonnegative, x strictly positive; I confirmed every stored entry is positive, no zero entries).
- Orbit shortcut: P_m commutes with the rotations and the reflection of the cycle (P[s,t] depends on s u t and s n t only). I verified by brute force from the definition that P_m is symmetric and dihedral invariant for m = 3 to 8 (self-test output not shipped), and the argument is general (a dihedral map is a graph automorphism of the cycle). An invariant x gives an invariant y = Px, so ratios y_i/x_i are constant on orbits. As belt and braces I ALSO computed y = Px for EVERY state (all 4,194,304 states at m = 22 and all 16,777,216 states at m = 24) and the exact minimum and maximum ratios over all states equal those over the orbit representatives (outputs not shipped).

## My checker (not shipped in this package)
- A C program of mine: builds the number of matchings of the induced cycle by its own dynamic program over edges, canonical dihedral representative by the minimum over all 2m images, expands the published vector (10-byte big-endian entries, orbit representatives in ascending order, width 22 first then width 24, as inferred from the manifest counts), and computes y = P x with unsigned 128-bit integers (entries below 2^80, matching counts below 2^32, at most 2^24 terms: below 2^121, no overflow). I wrote the format reading by myself from the folder description; the tightness of the resulting ratios (agreement to 1e-16 relative) confirms the ordering.
- A self-test script of mine: the C code equals y = Px from a brute-force P built from the definition (all subsets of cycle edges) for all 64 states at m = 6 and all 256 states at m = 8, with random 70-bit invariant vectors.
- A bounds script of mine: exact ratios as integer fractions (cross-multiplied), then interval arithmetic (mpmath iv, 80 digits, directed rounding): upper bound taken as the upper end of ln(max ratio at 22)/22, lower bound as the lower end of (ln(min ratio at 24) - ln(max ratio at 22))/2.

Command: concatenate the five parts into one file (sha256 339d3723...a9c4, equals the MANIFEST whole), then run my C program for width 22 and for width 24 on it, then my bounds script on the results. Real output:
```
m=22 orbits(reps)=96909  min ratio 2151288.2406040465664364457931259770193268143081  max ratio 2151288.2406040469632851141921389153850468691149
m=24 orbits(reps)=352698  min ratio 8098386.0605861547433225503360553991329209825434  max ratio 8098386.0605861609646998513890194302789972770127
U upper bound: ln(max ratio at 22)/22 = 0.66279897283374906531037854463015684138085055709026110720125629443452358...
L lower bound: (ln(min ratio at 24) - ln(max ratio at 22))/2 = 0.66279897283371381097569692093070996657443703009270244490149443581273...
```
and the enclosure printed by my script: lower 0.6627989728337138109756969209307099665744370300927..., upper 0.6627989728337490653103785446301568413808505570902...; width 3.5254334681623699e-14; both end points start 0.6627989728337, so 13 common decimals (floor13 of both = 0.6627989728337, and the outward-rounded published bounds 0.6627989728337138109756 and 0.6627989728337490653104 are valid).
Orbit counts: 96,909 at m = 22 and 352,698 at m = 24, matching the manifest.

## Author's checker, run after mine
Command: sh verify-it-yourself/run_checks.sh (34 s). Output (its output is not shipped separately) ended in "CERTIFIED: 0.6627989728337 < h2 < 0.6627989728338 (13 decimals)" and "PASS". Its min and max ratios at m = 22 and m = 24 are identical, digit for digit (to 28 digits printed), to mine, and its two bounds equal mine to every digit printed (70 digits). No mismatch.

## Remarks
- Both bounds are proved from the definitions; reliance is on exact integer arithmetic, which two independent implementations (mine in C with 128-bit integers, the author's in Python big integers) reproduce.
- The widths 22 and 24 were chosen after seeing wider results; this does not affect validity because each bound is a theorem for any admissible choice.
- Not judged here: novelty, or whether the criterion text is met (other skeptics).

pass: true
