# Mechanical Template-Closure Proofs of Lychrel Numbers in New Bases b = 50, 98, and 146 (+ Mechanical Audit of Kuitche 2023)

## What

Mechanical template-closure proofs that Lychrel numbers exist in three new bases b = 50 = 2*5^2 (claim/lychrel_base50_certificate.json, sha256 dd093b972a4f7eb7d6d9db4c5809a3332e413868719635bb6d2fdc9e59dacdb2, Period-4 templates T_1(m)..T_4(m) with |L_0|=|R_0|=36, |M_0|=8, and 82-digit start integer n = T_1(1) plus 1-step pre-template seed n_seed), b = 98 = 2*7^2 (claim/lychrel_base98_certificate.json, |L_0|=37, |M_0|=16), and b = 146 = 2*73 (claim/lychrel_base146_certificate.json, |L_0|=80, |M_0|=6), all outside {2^k, 11, 17, 20, 26}, verified by block-by-block symbolic carry computation for all integer parameters m at least 1, symbolic mirrored-block non-palindromicity, brute force over m from 1 to 500, 100,000-step orbit simulation with compiled regex matching to 50,082 digits in base 50, and a complete mechanical audit of Kuitche (2023) across bases 3..10 (claim/kuitche_2023_audit.json).

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same files, with identical bytes, are in `object/` (headlined by `object/lychrel_base50_certificate.json`).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` with `numpy`.
- **Rough laptop time**: about 32 seconds (includes two 100,000-step orbit simulations in Base 50 to 50,082 digits plus negative control).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell / Scope | Listed proven bases | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Wikipedia (`Lychrel_number`) | Proven Lychrel bases | `11, 17, 20, 26, and all powers of 2` | `b = 50 (2*5^2), 98 (2*7^2), 146 (2*73)` (Period-4 all-$m$ symbolic proofs) | https://en.wikipedia.org/wiki/Lychrel_number | 2026-10-19T06:30:18Z |
| MathPages (`dseal.htm`, David Seal 1996) | Sporadic Lychrel bases | `4, 11, 17, 20, 26` | `b = 50, 98, 146` (+ reproduction of Base 26) | https://www.mathpages.com/%68ome/dseal.htm | 2026-10-19T06:30:19Z |
| Kuitche (2023), DOI `10.21203/rs.3.rs-2659802/v1` | Bases `3..10` construction | Base `4` cycle only (`2^2`) | Complete mechanical audit across `b = 3..10` (`object/kuitche_2023_audit.json`) | https://doi.org/10.21203/rs.3.rs-2659802/v1 | 2026-10-19T05:50:12Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Base 10 (`196`) is not proved; our Period-4 Carry-Wire Decoupling theorem requires $b \equiv 2 \pmod{24}$ ($b \equiv 2 \pmod{3}$ for the Period-2 Outer Engine and $b \equiv 2 \pmod{8}$ for the Period-4 Inner Core).
- Not formalized in Lean 4 or Coq; closure for all $m \ge 1$ is reduced to a finite mechanical symbolic run-length block carry computation (`symbolic_rle_rev_add`) plus brute force over $1 \le m \le 500$ and 100,000-step regex-matched orbit simulation, as specified in the target's `success_criterion` and `verification_method`.
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **David Seal** (January 1996 `rec.puzzles` posting archived by **Kevin Brown** at MathPages, https://www.mathpages.com/%68ome/dseal.htm), author of the Period-4 Base-26 template family reproduced as our baseline.
- **Rostand S. Kuitche** (2023), *"On the Construction of Some Lychrel Numbers"*, Research Square preprint `rs-2659802/v1` (https://doi.org/10.21203/rs.3.rs-2659802/v1), audited in `object/kuitche_2023_audit.json`.
- Contributor credit: `mizopl`.
