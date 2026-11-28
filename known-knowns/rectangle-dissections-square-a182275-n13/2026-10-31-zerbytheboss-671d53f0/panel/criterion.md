# Skeptic 3: Success Criterion & Pitfall Audit

context: independent clean-room specification audit comparing package artifacts against bank/targets.json

## Audit Summary

1. Compared the package against `bank/targets.json` entry `rectangle-dissections-square-a182275-n13`:
   - Full win criterion requires the exact integer `A182275(13)` computed by two independent implementations that agree with each other, reproduce `a(0)..a(12)` and all 210 entries of `b116694.txt`, and satisfy `A116694(m, n) = A116694(n, m)`. Verified: `A182275(13) = 44952337678281087149239713571524612859282098351847918617404` (`59` digits).
   - Partial win `p1` (`A116694(13, 12)`) is included and verified: `1079082161133939350509688342814661590018188105589177004` (`55` digits), along with the full row `A333476(13, 0..13)`.
   - Partial win `p2` (`A182275(14)`) is included and verified: `179633908970647867061644006072082999771595948524857068695476923848566` (`69` digits), along with `A182275(15) = 3806271642082756769250454934171160217011193243952381412806809441536918416569002` (`79` digits).
2. Checked all listed pitfalls in `bank/targets.json`:
   - Confirmed grid-subgraph dissections are counted (including guillotine and non-guillotine configurations; $a(2) = 8$, $a(3) = 322$).
   - Confirmed raw labeled dissections are counted without $D_4$ symmetry reduction.

pass: true
