# Receipts: real output of sh verify-it-yourself/run_checks.sh

started: Sun Nov  1 03:26:00 UTC 2026, finished Sun Nov  1 03:53:24 UTC 2026 (27 min 24 s wall, 12 threads for the replay, on a desktop PC that was at 100% load from other jobs during the run; the replay alone is 3,291 thread-seconds in the original run). Lines longer than 400 characters are cut.

```
[03:26:01] step 1: sha256 of every file in object/
object/: 66 files, all sha256 match
[03:26:04] step 2: fetch the pinned public certificate (md5 + sha256 checked) and unpack it
using cached copy, md5 and sha256 verified
[03:26:27] step 3: sample-point tables: independent 90-digit membership re-check; far-field constants with exact radii
sets 21 points 5584 enclosure violations 0
R3 vertex radius [0.5773502691896257645091487805019574556476017512701268760186012629, 0.5773502691896257645091487805019574556476017512701268760186031298]
R5 vertex radius [0.5257311121191336060256690848478766072854979322433417815289348288, 0.5257311121191336060256690848478766072854979322433417815289360734]
d3(b3) = [0.6926763455379395057412052189669942153047704058948436118199870098, 0.6926763455379395057412052189669942153047704058948436118199907436]
d5(b5) = [0.6926761504535408451668527183743574275893911605749197260914501232, 0.6926761504535408451668527183743574275893911605749197260914532347]
G(d3(b3)) - 0.834 = [0.0000002139441454410094467857059216840329782699865521966977525817307906, 0.000000213944145441009446785705921684032978269986552196697760049349124]   >0 : True   (paper: [2.13944145452936,2.13944145452937]e-7)
G(d5(b5)) - 0.834 = [0.0000001464388840437641856899081057431564944386844239722139919036929202, 0.0000001464388840437641856899081057431564944386844239722139981267081981]   >0 : True   (paper: [1.46438884041707,1.46438884041708]e-7)
d3(b3) > 1/2: True  d5(b5) > 1/2: True
smallest b3 for which G(d3(b3))>0.834 (bisection upper): [0.1906991066111426516328786195941802361630834639072418212890634011, 0.1906991066111426516328786195941802361630834639072418212890634011]
smallest b5 for which G(d5(b5))>0.834 (bisection upper): [0.1946005271409877341895729510601320555451820837333798408508311781, 0.1946005271409877341895729510601320555451820837333798408508311781]
pi/5 float 0.6283185307179586 float-true = [-0.00000000000000002449293598294706354452131864550002116419498976684382819331968479, -0.00000000000000002449293598294706354452131864550002116419498852224077262109134336]
pi/3 float 1.0471975511965976 float-true = [-0.0000000000000001148364282799222086024443089485547227736583164855068895842375316, -0.0000000000000001148364282799222086024443089485547227736583139963007784397808487]
[03:26:36] step 4: build the checker
[03:26:52] step 5: interval type self-test (random operations against exact Fractions / mpmath)
checked 200000 violations 0 {'add': 20000, 'sub': 20000, 'mul': 20000, 'sqr': 20000, 'div': 20000, 'sqrt': 20000, 'sin': 20000, 'cos': 20000, 'sinI': 20000, 'cosI': 20000}
[03:27:08] step 6: replay ALL leaves of the certificate (2,374 + 1,029 collar leaves, 6,742,989 core leaves) on 12 threads
PART r3_collar: shards=256/256 leaves=2374 checked=2374 failing=0 min_slack=5.848039E-005 (leaf r3_collar:frontier:00000049:leaf:00000042) cover_and_frontier_partition=EXACT kinds=onebody_inner_polygon:2324,onebody_inner_polygon_pruned:50
PART r5_collar: shards=256/256 leaves=1029 checked=1029 failing=0 min_slack=4.895557E-005 (leaf r5_collar:frontier:00000225:leaf:00000004) cover_and_frontier_partition=EXACT kinds=onebody_inner_polygon:1014,onebody_inner_polygon_pruned:15
PART core5d: shards=256/256 leaves=6742989 checked=6742989 failing=0 min_slack=1.551089E-009 (leaf core5d:frontier:00000099:leaf:f3f063e37aab2285c295) cover_and_frontier_partition=EXACT kinds=template_simple_meanvalue:6317602,template_convex_meanvalue:423033,template_simple_meanvalue+altset:2354
TOTAL leaves=6746392 failing=0 worst_slack_over_0.834=1.551089E-009
VERDICT: ACCEPT (all leaf proofs pass with interval lower bound > 0.834; exact box partitions; counts equal shipped summaries)
[03:52:04] step 7: negative controls (tampered one-frontier mini certificates; each must be rejected)
c2_truncate            tau=0.834     REJECT  core5d readErr: JsonReaderException: '4' is an invalid end of a number. Expected a del; core5d failing leaves=1; core5d cover: None
c1_bitflip             tau=0.834     REJECT  core5d readErr: JsonReaderException: ',' is invalid after a property name. Expected a ; core5d failing leaves=1; core5d cover: None
c3_drop100             tau=0.834     REJECT  core5d cover: summary leaf_count 8200 != 8100
c0_baseline            tau=0.834     ACCEPT  min_slack=4.201e-07
c3b_drop100_countfixed tau=0.834     REJECT  core5d cover: volume mismatch sum!=root
c4b_dup1_countfixed    tau=0.834     REJECT  core5d cover: volume mismatch sum!=root
c4_dup1                tau=0.834     REJECT  core5d cover: summary leaf_count 8200 != 8201
c5_shrink              tau=0.834     REJECT  core5d cover: volume mismatch sum!=root
c8_samples32           tau=0.834     REJECT  core5d failing leaves=87
c6_grow                tau=0.834     REJECT  core5d cover: volume mismatch sum!=root
c12_swap_lohi          tau=0.834     REJECT  core5d cover: leaf 200 non-positive width axis 3
c9_psi07               tau=0.834     REJECT  core5d failing leaves=1
c14_shift              tau=0.834     REJECT  core5d cover: no separating plane (overlap or irregular cell)
c7a_tau_0.8340004      tau=0.8340004 ACCEPT  min_slack=4.201e-07
c15_countlie           tau=0.834     REJECT  core5d cover: summary leaf_count 8201 != 8200
c7b_tau_0.8340005      tau=0.8340005 ACCEPT  min_slack=1.984e-06
c7d_tau_0.8348         tau=0.8348    ACCEPT  min_slack=8.010e-04
c7c_tau_0.84           tau=0.84      REJECT  core5d failing leaves=237
controls: 14 tampers rejected, baseline accepted
PASS
```
