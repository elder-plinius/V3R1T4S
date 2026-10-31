Real output of `sh verify-it-yourself/run_checks.sh plain.csv index.html` run from the package folder on 2026-10-27 (Python standard library only), against the two pages fetched at 2026-10-27T13:31:11Z (`/plain`, sha256 2e6502fa3d86…) and 2026-10-27T13:31:13Z (index, sha256 189e750e70f8…):

```
sha256 ok object/29x60.txt
== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the table pages given
(29,60) c*=0.032282689322403249986 table=0.032282791684 gain=1.02362e-7 star=False needs_opt=False ref=Ilmari Vahteristo, New spherical codes by tuning an annealing solver, preprint,  index_cos=0.032282791684 OK
rows checked: 1 (expected 1); smallest gain 1.02e-07; largest gain 1.02e-07
assertions: PASS (every row OK, no star, label absent)
ALL CHECKS PASS
```
