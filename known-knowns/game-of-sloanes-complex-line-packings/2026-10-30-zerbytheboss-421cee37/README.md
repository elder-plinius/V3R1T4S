# Game of Sloanes: Complex Line Packing Record for d=5, n=49

## What
Explicit complex line packing of 49 unit vectors in C^5 with coherence mu = 0.5414603056425635777656004045456828234216 computed in mpmath at 40 digits after normalization, strictly lowering the Game of Sloanes live leaderboard record 0.54164128 by 0.000180974357 >= 1e-8.

## Check it yourself
Run the standalone checker from this package directory in a fresh shell:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output:
```text
Object: object/5x49_v3r1t4s.txt
Dimension d=5, Lines n=49
Computed Coherence mu (40 digits): 0.5414603056425635743462895172126666579322
Leaderboard Record Coherence    : 0.54164128
Theoretical Lower Bound         : 0.50751922
Strict Lowering Margin          : 0.000180974357436425653710482787333342067819
VERIFIED: mu = 0.5414603056425635743462895172126666579322 strictly beats 0.54164128 by 0.000180974357436425653710482787333342067819 >= 1e-8
PASS
```
Verification takes approximately 10 seconds.

## Compared to
| Parameter | Live Leaderboard Value | Source | V3R1T4S Certified Value | Improvement Margin |
|---|---|---|---|---|
| Dimension $d$ | 5 | Game of Sloanes Table | 5 | Match |
| Line Count $n$ | 49 | Game of Sloanes Table | 49 | Match |
| Best Coherence $\mu$ | 0.54164128 | `CurrentBestPackings/5x49_oai.txt` | **0.5414603056...** | **$-0.000180974357$** |
| Lower Bound | 0.50751922 | Welch / Bukh-Cox Bound | 0.50751922 | Satisfied ($\mu > \text{LB}$) |

## Not claimed
- We do not claim to have proved optimality for $(5, 49)$; row $(5, 49)$ remains open with theoretical lower bound $0.50751922$.
- We do not claim to have improved provably optimal rows ($\circ$).

## Credits
- John Jasper, Emily J. King, and Dustin G. Mixon for maintaining the Game of Sloanes repository and leaderboard (arXiv:1907.07848, `https://github.com/gnikylime/GameofSloanes`).
- Dustin G. Mixon (`oai`) for the baseline packing `5x49_oai.txt`.
