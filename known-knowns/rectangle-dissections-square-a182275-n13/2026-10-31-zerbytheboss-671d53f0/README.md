# Rectangle Dissections of the Square: A182275(13), A182275(14), A182275(15), and A116694(13, 12)

## What

Exact rectangle dissection counts A182275(13) = 44952337678281087149239713571524612859282098351847918617404 (full win), A116694(13, 12) = 1079082161133939350509688342814661590018188105589177004 (partial win p1), A182275(14) = 179633908970647867061644006072082999771595948524857068695476923848566 (partial win p2), and A182275(15) = 3806271642082756769250454934171160217011193243952381412806809441536918416569002, with complete table A116694(m, n) for 0 <= m, n <= 14 verified by independent decompositions.

Summary of new exact terms and digit counts:
- `A182275(13) = 44952337678281087149239713571524612859282098351847918617404` (`59` digits, full win: $13 \times 13$ square)
- `A116694(13, 12) = 1079082161133939350509688342814661590018188105589177004` (`55` digits, partial win `p1`: $13 \times 12$ rectangle and full row `A333476(13, 0..13)`)
- `A182275(14) = 179633908970647867061644006072082999771595948524857068695476923848566` (`69` digits, partial win `p2`: $14 \times 14$ square and full row `A333476(14, 0..14)`)
- `A182275(15) = 3806271642082756769250454934171160217011193243952381412806809441536918416569002` (`79` digits, bonus: $15 \times 15$ square)

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_dissections.py` (Python 3 standard library only, ~2.5 seconds runtime), which recomputes `A116694(m, n)` for $0 \le m \le 15, 0 \le n \le 20$ via three independent algorithms — Method 1 (1-bit broken-profile vertex-degree continuity DP), Method 2 (recursive Kronecker-block divide-and-conquer on $(M_m, B_m)$ without profile sweep + transpose symmetry $A116694(m, n) = A116694(n, m)$), and Method 3 (Fibonacci $F(2m+1)$ vertical-cut open-rectangle transfer matrix for $0 \le m, n \le 6$) — and verifies byte-for-byte reproduction of all 13 entries of `b182275.txt`, all 210 entries of `b116694.txt`, and all 91 entries of `b333476.txt`.

## Compared To

- **Published Record (OEIS A182275, A116694, A333476)**:
  - `A182275` (`https://oeis.org/A182275/b182275.txt`) ends at $n = 12$ (`a(12) = 59647666241586874002530830848160043213559146735474`, computed by Steve Butler via $F(2n+1)$ transfer matrix).
  - `A116694` (`https://oeis.org/A116694/b116694.txt`) lists 210 antidiagonal entries for $d = 1 \dots 20$ ($m + n \le 19$ in 0-based indexing, so `A116694(13, 12)` at $m + n = 25$ was uncomputed).
  - `A333476` (`https://oeis.org/A333476/b333476.txt`) lists rows $0 \le k \le n \le 12$ (91 entries).
- **This Submission**: Extends `A182275` by three new consecutive terms (`a(13)`, `a(14)`, `a(15)`), computes the full $15 \times 15$ array `A116694(0..14, 0..14)` including `A116694(13, 12)`, and extends `A333476` by rows 13 and 14.

## Not Claimed

- No polynomial-time closed-form formula in $n$ is claimed for `A182275(n)`.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - David A. Klarner and Spyros S. Magliveras, "The number of tilings of a block with blocks," *European Journal of Combinatorics* 9 (1988), 317-330 (`https://doi.org/10.1016/S0195-6698(88)80062-3`).
  - Helena Verrill and Joshua Smith (`https://oeis.org/A116694`, 2006).
  - Matthew C. Russell and Steve Butler (`https://oeis.org/A182275`, 2010).
  - Alois P. Heinz (`https://oeis.org/A116694/b116694.txt` and `https://oeis.org/A333476/b333476.txt`, 2012-2020).
  - Peter Kagey (`https://oeis.org/A333476`, 2020).
  - Pablo Blanco, Robert Dougherty-Bliss, Natalya Ter-Saakov, and Doron Zeilberger, "The Amazing World of Framing," `https://arxiv.org/abs/2606.05439` (2026).
