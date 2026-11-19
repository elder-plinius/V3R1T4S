# Skeptic verdict

Context: fresh headless agent CLI. Read `claim/TARGET_CRITERION.md` and `claim/CLAIM.md` first. Wrote a stdlib-only B3/S23 checker (`checker.py`) before reading `claim/code/` or the original result JSON. Public Wechsler/apgcode rules and glider kinematics were taken from LifeWiki-style extended Wechsler (bit `i` of a 0–31 digit is row offset `i` in a 5-row strip; `w`/`x`/`y*` skips; `z` starts the next strip). No GitHub login, installs, proxies, or live-table novelty job.

## Claim judged

Main criterion only: a 7-glider all-glider B3/S23 synthesis of the still life `xs28_69a4owgzxol5d1d96`. Assigned scope is numerical verification. A published predecessor `xs25_0ml1u8z643032ak8` (6 gliders) plus a 1-glider converter is disclosed; the construction is that seeded converter route.

## Method

1. Parse the claimed RLE. Require rule B3/S23.
2. Split generation 0 into 8-connected components. Require exactly 7 components, each 5 cells, each one of the 16 glider shapes obtained from `xq4_153` by 4 phases and 4 rotations, with diagonal period-4 velocity in `{±1}×{±1}`.
3. Inclusive bounding box `w×h`; Euclidean diagonal `hypot(w,h)`; rewind `T = 4 * ceil(diagonal)` generations (a multiple of 4, so phase is unchanged). Translate each glider by `-(T/4) * (vx,vy)`.
4. From that rewound state, evolve the combined pattern and the seven gliders separately. At every generation `0..T` require combined cells equal the union of the separate gliders. At generation `T` require recovery of the original generation-0 pattern.
5. Evolve forward until a state equals its successor (exact period 1). Require population 28 and exact match to the cells decoded from the target apgcode under D8 plus translation, with no leftover cells.
6. Decode-time still-life check on the apgcode, plus a strictness test: 2-neighbor forced union-find, then exhaustive partition of the remaining groups.
7. Built-in positive and negative controls must all pass before the claim is judged. Two Life step implementations (neighbor Counter vs padded grid) must agree on controls and on an 8-step prefix of the claim.
8. Run the checker twice with `PYTHONHASHSEED=0` and compare a SHA-256 digest of the claim payload.

## Exact commands (relative)

```
PYTHONHASHSEED=0 nice -n 19 python3 checker.py --rle claim/result/xs28_69a4owgzxol5d1d96.rle --target xs28_69a4owgzxol5d1d96 --out checker_out --tag run1
PYTHONHASHSEED=0 nice -n 19 python3 checker.py --rle claim/result/xs28_69a4owgzxol5d1d96.rle --target xs28_69a4owgzxol5d1d96 --out checker_out --tag run2
nice -n 19 python3 claim/code/life_check.py --rle claim/result/xs28_69a4owgzxol5d1d96.rle --target xs28_69a4owgzxol5d1d96
```

Saved: `checker.py`, `checker_out/run1.json`, `checker_out/run1.log`, `checker_out/run1_controls.json`, `checker_out/run2.json`, `checker_out/run2.log`, `checker_out/run2_controls.json`, `checker_out/summary.txt`.

## Measured output

Controls: 44/44 pass on both runs. Including: blinker period 2; block/tub/beehive/boat still lifes; `xq4_153` glider identification and 16 shapes; LWSS 2c/4; `xs31_0ca178b96z69d1d96` (z-strip) still life of 31 cells; target decode population 28 and itself a still life; R-pentomino rejected as a glider; two far gliders rewind cleanly; a 2-glider block recipe rewinds and settles to a block; receding same-lane gliders fail rewind; a block plus gliders fails the all-glider test; blinker fails the period-1 still-life test; bi-block admits a still-life partition; a single block is strict.

Claim RLE: rule B3/S23, header 204×213, generation-0 population 35.

Gliders: 7 eight-connected components, sizes 5,5,5,5,5,5,5. Velocities in min-(y,x) component order: (1,1), (-1,1), (-1,1), (-1,1), (1,1), (-1,-1), (-1,-1).

Rewind: `w=204`, `h=213`, diagonal `294.93219559756443`, `ceil=295`, `T=1180`. Mismatch generations: none. Recovered original generation 0: true.

Forward: exact period 1 from generation 759, population 28, bounding box 11×10, D8+translation match to decoded `xs28_69a4owgzxol5d1d96`: true, no other cells.

Target strictness: true (6 forced groups; every bipartition leaves an unstable piece).

Determinism: both runs `ok=true`, digest `383c6c54ba4ac9c117fa6cd0f2dd2f862ad8840eb2155a16171b613eb0354c6d`.

Author `claim/code/life_check.py` (stdlib, after the independent result): `PASS`, 7 gliders, rewind `T=852` and `T=1180` ok, exact repeat from generation 759, period 1, population 28, final object matches the apgcode. The original result JSON marks `ok: false` with a missing live `#CSYNTH` line, and records `structurally_valid: true`, `n_gliders: 7`, `rewind_ok: true`, `period: 1`, `final_apgcode` equal to the target. Those structural fields agree with the numerical checks.

## Limitations

Assigned scope is numerical verification. Live Catagolue unlisted/first-synthesis table status was not judged here. The disclosed predecessor route is accepted as given. Long rewind/forward loops used the Counter engine after the two engines agreed on controls and a short prefix. Strictness is the union-find/partition test above, not a census classifier. Inclusive bounding-box diagonal was used for `T`.

Numerical synthesis of the stated still life by 7 inbound gliders holds.

pass: true
