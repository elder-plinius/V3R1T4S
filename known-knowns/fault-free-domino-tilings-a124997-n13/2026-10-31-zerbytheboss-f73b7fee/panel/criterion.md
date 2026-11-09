# Skeptic 3: Success Criterion & Pitfall Audit

context: independent clean-room specification audit comparing package artifacts against bank/targets.json

## Audit Summary

1. Compared the package against `bank/targets.json` entry `fault-free-domino-tilings-a124997-n13`:
   - Full win criterion requires the exact integer `A124997(13)` from two independent runs/methods that agree exactly and reproduce `a(1)..a(12)`. Verified: `6247544447707621227323332397746698905631862234864529357713987234906581365476497906` (82 digits), with `a(1)..a(12)` reproduced to the last digit.
   - Partial win `p1` (`A124997(14)`) is included and verified by both methods: `199616955472645465045650566203466781313162448998311240985347793453943630517044514139601504958394` (96 digits).
   - Partial win `p2` (`24 x 26` rectangle) is included and verified by both methods: `1917746391484128020631543300994138189551214236354867955795097459933023415049` (76 digits).
2. Checked all listed pitfalls in `bank/targets.json`:
   - Confirmed $a(1) = a(2) = a(3) = 0$ (the $6 \times 6$ square has no fault-free domino tiling) and $a(4) = 25,506$.
   - Confirmed raw labeled orientations are counted without dihedral symmetry reduction, and $0 < \text{A124997}(n) < \text{A004003}(n)$ holds for all $4 \le n \le 15$.

pass: true
