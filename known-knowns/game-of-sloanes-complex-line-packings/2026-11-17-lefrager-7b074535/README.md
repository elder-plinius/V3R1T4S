# Game of Sloanes — New Best `(3, 34)` Complex Line Packing

## What

`34 unit vectors in C^3 (d=3, n=34) achieving 60-digit Decimal coherence mu = 0.756494798182271705164224601239675096749550724764985832115081 (strictly lower by +0.000340001817728294835775398760324903250449275235014167884919 than the live GameofSloanes README table Best Coherence 0.75683480 and by +0.000339999071356500933599184538472857625193835021833167888572 than upstream CurrentBestPackings/3x34_jrr.txt 0.756834797253628206097823785778147954374744559786819000003653, >= 1e-8 threshold satisfied by 34,000x, above lower bound 0.67202151, on an unclaimed open row absent from all 10 open pull requests, formatted to >= 20 significant digits per coordinate).`

Packaged at `object/3x34_new.txt` (`sha256: 7b0745355c9f502a7eb731c0ec7541db1d21edfabe543f6274eacda06f2b0597`, `204` floats: `102` real parts vector-by-vector followed by `102` imaginary parts vector-by-vector), with `min |coord| >= 0.017`, `>= 20` significant digits per coordinate, unit norm error `7.695e-20`, and all `129 = DOF + 1` active pairs equilibrated to `< 1e-10`.

## Check It Yourself

From the root of this package directory (`< 1 second`, Python 3 standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line of output:

```text
PASS
```

To rediscover and polish the packing from random seeds (`~10 seconds` with `g++` OpenMP):

```sh
sh how-we-built-it/reproduce.sh
```

## Compared To

- **Live `gnikylime/GameofSloanes` `README.md` (`https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md`, fetched `2026-11-17T00:12:14.359235+00:00`, `SHA-256: 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d`):** `(3, 34)` listed `Best Coherence = 0.75683480` (`CurrentBestPackings/3x34_jrr.txt`, author `jrr`, lower bound `0.67202151`), `IS_PROVABLY_OPTIMAL: False`, `IS_CONJECTURALLY_OPTIMAL: False`.
- **All 10 Open Pull Requests (`https://api.github.com/repos/gnikylime/GameofSloanes/pulls?state=open&per_page=100`, checked live `2026-11-17T00:12:14Z`):** `71` claimed cells total; `(3, 34) IS_CLAIMED_IN_OPEN_PR: False`.
- **Upstream Beaten File [`CurrentBestPackings/3x34_jrr.txt`](https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x34_jrr.txt) (`SHA-256: 159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e`, `60-digit` `Decimal` coherence):** `0.756834797253628206097823785778147954374744559786819000003653` (`129` active pairs).
- **Our Result (`object/3x34_new.txt`, `60-digit` `Decimal` coherence):** `0.756494798182271705164224601239675096749550724764985832115081`, improving on the table by **`+0.000340001817728294835775398760324903250449275235014167884919`** (`34,000x` the `1e-8` threshold) and on the exact upstream baseline by **`+0.000339999071356500933599184538472857625193835021833167888572`**.

## Not Claimed

- We do not claim global optimality for `(3, 34)` (`mu = 0.75649479818227170516... > 0.67202151` lower bound).
- We do not submit directly to `gnikylime/GameofSloanes` without human confirmation.
- No other `(d, n)` rows are claimed in this single-object submission package.

## Credits

Contributed by `lefrager`. Compared against [`gnikylime/GameofSloanes`](https://github.com/gnikylime/GameofSloanes) and prior `(3, 34)` record contributor `jrr` ([`CurrentBestPackings/3x34_jrr.txt`](https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x34_jrr.txt), `SHA-256: 159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e`).
