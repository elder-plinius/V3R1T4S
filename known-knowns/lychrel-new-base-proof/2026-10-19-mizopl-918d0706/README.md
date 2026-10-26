# Lychrel New Base (`p2`): Mechanical Audit of Kuitché (2023) Across Bases $3\dots 10$ (`2026-10-19-mizopl-918d0706`)

## What

Complete mechanical audit of Rostand S. Kuitché (2023), *"On the Construction of Some Lychrel Numbers"* (Research Square preprint `rs-2659802/v1`, DOI `10.21203/rs.3.rs-2659802/v1`) across all bases $b \in \{3, 4, 5, 6, 7, 8, 9, 10\}$ (`object/kuitche_2023_audit.json`, `14,637` bytes, `sha256: 918d070676a95905173766663baef89c576b2f22d135cc7eacc7dd691f596736`), certifying that only $b = 4 = 2^2$ and $b = 8 = 2^3$ (powers of 2) close under the paper's construction while every non-power-of-2 base $b \in \{3, 5, 6, 7, 9, 10\}$ fails template closure with explicit counterexamples at $p = 2$.

*(Split from PR #517 per maintainer request so each package contains a single object.)*

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` with `numpy`.
- **Rough laptop time**: `< 1` second.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell / Scope | Listed proven bases | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Wikipedia (`Lychrel_number`) | Proven Lychrel bases | `11, 17, 20, 26, and all powers of 2` | Mechanical audit of Kuitché (2023) across `b = 3..10` (`p2`) | https://en.wikipedia.org/wiki/Lychrel_number | 2026-10-19T06:30:18Z |
| Kuitché (2023), DOI `10.21203/rs.3.rs-2659802/v1` | Bases `3..10` construction | Base `4` cycle (`2^2`) | Complete mechanical audit across `b = 3..10` (`object/kuitche_2023_audit.json`) | https://doi.org/10.21203/rs.3.rs-2659802/v1 | 2026-10-19T05:50:12Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- No non-power-of-2 base in $3\dots 10$ closes under Kuitché's construction; new proven Lychrel bases $b = 50, 98, 146$ are submitted in separate single-object packages (`#517` for base 50, plus separate PRs for base 98 and base 146).

## Credits

- **Rostand S. Kuitché** (2023), *"On the Construction of Some Lychrel Numbers"*, Research Square preprint `rs-2659802/v1` (https://doi.org/10.21203/rs.3.rs-2659802/v1), audited in `object/kuitche_2023_audit.json`.
- Contributor credit: `mizopl`.
