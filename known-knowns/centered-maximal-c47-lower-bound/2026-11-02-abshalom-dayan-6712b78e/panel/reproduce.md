# REPRODUCE

context: subagent

## Definition, quoted

PROOF.md: "For f in L^1(R^2) put M f(z) = sup_{r>0} (1/|Q(z,r)|) int_{Q(z,r)} |f|, with Q(z,r) the closed square with centre z and side 2r. The constant c_2 is the least C with alpha |{M f >= alpha}| <= C ||f||_1 for all f in L^1 and alpha > 0."

CLAIM.md: "c_2 >= 5422547985449268449657817/3169205443485515833671680 = 1.711011823672...", object in object/measure.json, sha256 6712b78e...921891.

## Method

I read CLAIM.md, PROOF.md, REPRODUCE.md, table/record.md and object/measure.json, then wrote my own programs before opening checkers/. This means I knew the certificate shape and the 2^-40 rho grid from PROOF.md, so my checker is separately written but not blind to the method.

- **Property checks (Python integers):** sha256, types, ranges, duplicates, mass, the fraction, and the tail bound in exact Fractions.
- **Own checker (C, 128-bit integers):**
  - It uses a 2D prefix mass table over periodic images.
  - It enumerates every box with x1, y1 in the cell and x2, y2 on image coordinates, and tests side^2 <= m 2^30 exactly.
  - It takes rho = k 2^-40 with k = isqrt(m 2^48), exact, or the ceiling for an outer set.
  - It clips with all period translates.
  - It computes the union by a sweep along x.
- **Second union implementation:** Python big integers, sweep along y, run on the same pieces.
- **Own pointwise evaluator from the definition (C):** exact test of M mu(z) >= 1 at any point, over images with distance up to 5, which covers every side below S*.

The verdict rests on the exhaustive enumeration, the exact unions and the proof review. The samples below are spot checks only.

## Own checker output

```
sha256 6712b78eb07a4accab668a351347f9ccab05f3564034baa99e3dfb27ea921891
bits 30 Lx 3521728552 Ly 2941646574 atoms 344
duplicate positions 0
atom(0,0) [[0, 0, 1073741824]] is 2^30 1073741824
mass_num 5629639765 M= 5.243010600097477
distinct x 116 distinct y 13
smallest [509376] 0.000474393367767334 second largest non-frame 1451960 0.0013522431254386902 largest 4281796557 3.9877337934449315
frame atom [[1760864276, 0, 4281796557]] Lx/2? 1760864276.0
fraction 5422547985449268449657817/3169205443485515833671680 True
decimal 1.7110118236719642
f(10) 0.9871526409009421 True
S* in 9.726890934546645 9.726890934554831

reach=4 rects=186110 pieces=282779 maxside_real=3.991827 area_num=10844998364959256391267914  value 1.710996424553633
reach=5 rects=187868 pieces=286295 maxside_real=4.295045 area_num=10844998364959256391267914  value 1.710996424553633
reach=6 rects=188898 pieces=288355 maxside_real=5.554326 area_num=10845095970898536899315634  value 1.711011823671964
reach=8 rects=188902 pieces=288359 maxside_real=6.559731 area_num=10845095970898536899315634  value 1.711011823671964
reach=10 rects=188902 pieces=288359 maxside_real=6.559731 area_num=10845095970898536899315634  value 1.711011823671964
reach=12 rects=188902 pieces=288359 maxside_real=6.559731 area_num=10845095970898536899315634  value 1.711011823671964
ceil rho, reach 6/10/12: area_num=10845095970927508751909818 value 1.711011823676535
grid 2^-46, reach 12, floor: 1.711011823674691   ceil: 1.711011823674763

ysweep_python area_num 10845095970898536899315634 pieces 288355

random=200000 M_ge_1=199669 in_lower=199669 in_upper=199669 lower_but_not_M=0 M_but_not_upper=0
corner probes: pieces=100000 corners=400000 corners_with_M_lt_1=0
```

My checker on the calibration files, grid 2^-50:
- tests/lin40.json: rects=11 pieces=20, value 1.6855099933553
- tests/tomar40.json: rects=3362 pieces=5129, value 1.7027237336031

The first own version of the second union program was too slow and hit my own 500 s alarm (exit 142). I replaced it with the segment tree above. This was my code, not a block.

## The author's programs, run on a copy of claim/

`sh checkers/run_checks.sh`, 1:47 total:

```
atoms=344 rectangles=188898 pieces=288355 area_num=10845095970898536899315634 (over 2^80) mass_num=5629639765 (over 2^30)
value=1.711011823672
strictly_above_bar True margin 0.008288090071964177
pieces=270257 area_num=10845095970898536899315634 (over 2^80) mass_num=5629639765 (over 2^30)
value=1.711011823672
SWEEP V_lower 1.71101182367469 V_upper 1.71101182367477 width 0.00000000000008  area_lower 8.97085312841852 V*mass_lower 8.97085312841852
      trivial cap area/mass 1.71382271903463
PASS
```

A second run was byte-identical (`cmp` silent). A recursive diff of the copy against claim/ afterwards showed no differences.

Calibration:

```
atoms=2 rectangles=11 pieces=20 area_num=10134321765464081975785980 (over 2^80) mass_num=5468440998922 (over 2^40)
value=1.685509993354
atoms=50 rectangles=3362 pieces=5129 area_num=10857451761599542030224416 (over 2^80) mass_num=5799411059506 (over 2^40)
value=1.702723733601
value=1.000000000000
value=1.000000000000
value=1.085786437626
PASS
```

Family regeneration:

```
formula_atoms=344 cert_atoms=344 merged=0 mass=5.2430106587 ceiling=1.7138226997
cmp with object/measure.json: identical; sha256 6712b78eb07a4accab668a351347f9ccab05f3564034baa99e3dfb27ea921891
second generation: identical
```

family/famgen.py reads only family/L3.par, not the object.

Pointwise tests in REPRODUCE.md, which match its stated lines:

```
samples=1000000 M_ge_1=998365 in_S=998365 violations=0 missed=0
N=64 samples=1000000 hits=876530 ratio=1.695862 se=0.000636
```

Rounding spot check in family/FAMILY.md:
- 24 bits: value=1.711011732550, rectangles=188898
- 34 bits: value=1.711011822549, rectangles=188898

Both match.

## Agreement

| item | own | author | match |
|---|---|---|---|
| area_num, reach 6 | 10845095970898536899315634, in two own unions | check_a and check_b, same | exact |
| mass_num | 5629639765 | same | exact |
| rectangles, pieces, reach 6 | 188898, 288355 | check_a same | exact |
| reach 4, 5, 6, 8 (PROOF.md) | .710996424554 twice, .711011823672 twice | stated values | yes |
| true ratio | [1.711011823674691, 1.711011823674763] at grid 2^-46 | vsweep [1.71101182367469, 1.71101182367477] | yes |
| f(10) | 0.98715264 | 0.98715 | yes |
| Lin formula 1.68550999335553 | 1.6855099933553 | 1.685509993354 | yes, within rounding |

The margins in CLAIM.md follow by subtraction from the values as read: 0.00828809 above 1.7027237336 and 0.02550183 above 1.6855099933.

## Proof, step by step

- **Step 1:** ||f||_1 = (2K)^2 M holds. Bumps may extend outside the block without changing the norm.
- **Step 2:** the inner block has margin c min(Lx,Ly) >= D + min(Lx,Ly) > D on each side, in both axes. So S lies in P_K, including with half-open blocks. The set S is translated by a period, and that keeps it in the extension.
- **Step 3:** Q(p,eta) lies in Q(z,rho+eta) when |z-p|_inf <= rho. Since f >= 0 is a sum, the integral is at least mu(S). The average is at least rho^2/(rho+eta)^2, and t -> (t/(t+eta))^2 is increasing. Correct.
- **Steps 4 and 5:** V is periodic, so the inner block has (2K-2c)^2 full cells. c does not depend on K or eta. The limits are valid for K > c.
- **Strict level sets and open squares:** both correct.
- **Rho rounding:** k^2 <= m 2^48 is exactly 4 rho^2 <= mu(S), exact in my code and in the author's. Rounding down only shrinks rectangles. The rounded-up run gives a true outer set.
- **Closed squares and atoms at the boundary:** an atom on the boundary of Q counts because Q is closed. The closed-box mass includes atoms on the box sides. Every rectangle is valid, because every z in it has the box inside Q(z,rho). All 400000 sampled piece corners have M mu >= 1 by the exact evaluator, including corners of pieces clipped to the cell.
- **Wrap-around:** my checker uses explicit translates for all k, and the author's check_a uses a split with a full-cover case. Rectangle and piece counts and area are identical. A box wider than a period counts all its images. Rectangles wider than a period cover the whole axis. Every box has a translate with x1, y1 in the cell, and no negative images can lie in such a box.
- **Tail bound:** a closed interval of length S holds at most floor(S/L)+1 images, so mu(Q) <= M(S/Lx+1)(S/Ly+1) = S^2 f(S). f is strictly decreasing, and the exact S* lies in 9.72689093455 +- 1e-11.
- **Reach:** the sup over r of a right-continuous step mass over 4r^2 is reached at a jump radius, and the tight box of that witness is enumerated. So a reach of at least S* captures the whole level set. Reach 10 and 12 change nothing, and the largest useful side is 6.559731. The lower bound does not depend on any of this.
- **Normalisation:** scaling positions by t and masses by t^2 leaves the ratio unchanged. Correct.

## Mismatches

None in any number, property or proof step.

One notation remark. The exact fraction is 1.71101182367196..., so "1.711011823672..." in CLAIM.md is rounded up, not truncated. The fraction is what is claimed. The decimal is also a valid bound, since my grid 2^-46 lower end 1.711011823674691 exceeds it.

## Not done here

- **Comparators not re-fetched:** the page value, the open pull requests and Tomar's value were not re-fetched. I took them as recorded in table/record.md, so "strictly above the live page and open pull requests" is verified only against those recorded values.
- **Programs not run:** checkers/third/vtree.c, checkers/third/vsample.c and the float search in rebuild/.
- **Family tables:** the tables in family/FAMILY.md were not reproduced, except the 24, 30 and 34 bit rows.
- **Independence from Tomar:** the file contents support it only partly. The object shares one position with tests/tomar40.json at 4 decimals, namely (0,0). Tomar's small masses run 0.00497 to 0.00612, against 0.00047 to 0.00135 here. The provenance statement itself cannot be checked from these files.

## Text addressed to reviewers

None found, by reading the files I opened and by searching all files for "reviewer", "ignore previous" and "pass: true". The only hit is the line in table/record.md saying none was found.

## Blocks

None.

pass: true
