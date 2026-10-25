# Lychrel New Base: Base-98 Template-Closure Certificate (`2026-10-19-mizopl-6ec98e27`)

## What

Mechanical template-closure proof that Lychrel numbers exist in base $b = 98 = 2 \cdot 7^2 \notin \{2^k, 11, 17, 20, 26\}$ (`object/lychrel_base98_certificate.json`, `38,310` bytes, `sha256: 6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256`, Period-4 templates $T_1(m)\dots T_4(m)$ with $|L_0|=|R_0|=37$, $|M_0|=16$, and `92`-digit start integer $n = T_1(1)$ plus 1-step pre-template seed $n_{\text{seed}}$), verified by block-by-block symbolic carry computation for all integer parameters $m \ge 1$, symbolic mirrored-block non-palindromicity, brute force over $m$ from $1$ to $500$, and a 2,000-step concrete orbit simulation with compiled regex matching.

*(Split from PR #517 per maintainer request so each package contains a single object.)*

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` with `numpy`.
- **Rough laptop time**: `< 2` seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell / Scope | Listed proven bases | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Wikipedia (`Lychrel_number`) | Proven Lychrel bases | `11, 17, 20, 26, and all powers of 2` | `b = 98 (2*7^2)` (Period-4 all-$m$ symbolic proof) | https://en.wikipedia.org/wiki/Lychrel_number | 2026-10-19T06:30:18Z |
| MathPages (`dseal.htm`, David Seal 1996) | Sporadic Lychrel bases | `4, 11, 17, 20, 26` | `b = 98` (+ baseline reproduction of Base 26) | https://www.mathpages.com/%68ome/dseal.htm | 2026-10-19T06:30:19Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Base 10 (`196`) is not proved; our Period-4 Carry-Wire Decoupling theorem requires $b \equiv 2 \pmod{24}$.
- Not formalized in Lean 4 or Coq; closure for all $m \ge 1$ is reduced to a finite mechanical symbolic run-length block carry computation (`symbolic_rle_rev_add`) plus brute force over $1 \le m \le 500$ and concrete regex-matched orbit simulation.
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **David Seal** (January 1996 `rec.puzzles` posting archived by **Kevin Brown** at MathPages, https://www.mathpages.com/%68ome/dseal.htm), author of the Period-4 Base-26 template family reproduced as our baseline.
- Contributor credit: `mizopl`.
