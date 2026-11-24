# Pre-Registration: post-tag-busy-beaver-bbpt

- frozen_utc: 2026-11-15T14:09:16Z
- target_id: post-tag-busy-beaver-bbpt
- status_source: https://wiki.bbchallenge.org/wiki/Post_Tag_System
- status_sha256: 2ac4239d4a7149084325ae0d2e9fc1e7c6eaeece711fc2140a373f5f2fbab123
- null_test: not needed because exact deterministic simulation/enumeration certificate

## Frozen success criterion (verbatim from bank)

Success means (a) a 2-tag system of size S, 8 <= S <= 11 (size and step conventions of https://wiki.bbchallenge.org/wiki/Post_Tag_System), that halts from 00 after STRICTLY more steps than the bound listed for S on that page, re-fetched live before claiming, verified by direct simulation; or (b) an exact value of BB_PT(S) for some S in 8..11 that the page still lists with ' > =': every size-S system either halts (with its step count) or carries a checkable non-halting certificate (cycle, translated cycle, or another proof re-checked by an independent decider or a proof assistant), and the largest halting count is reported.

Partial wins:
- `p1`: Exact `BB_PT(8)`: all size-8 systems classified, the 7 wiki holdouts each with a non-halting certificate (or a new champion).
- `p2`: Exact `BB_PT(9)`, with all size-9 holdouts certified.
- `p3`: A new champion at size 10 or 11 (criterion (a)).

## Frozen verification protocol and acceptance thresholds

1. **Calibration gate**: Any simulator/verifier must first reproduce all five wiki calibration values from initial tape `00`:
   - `0111_1` (size 7) -> halts in `10` steps
   - `111_20_` (size 8) -> halts in `19` steps
   - `11_021_2` (size 9) -> halts in `49` steps
   - `112_1_002` (size 10) -> halts in `779` steps
   - `120221_0_2` (size 11) -> halts in `196,841` steps
2. **Criterion (b) / p1 / p2 exactness gate (`S = 8` or `S = 9`)**:
   - Independently enumerate **every** raw 2-tag system of size `S`, i.e., every `n` in `{1, ..., S}` and every tuple `(w_0, ..., w_{n-1})` in `({0, ..., n-1}^*)^n` with `n + sum_{i=0}^{n-1} |w_i| = S` (exact theoretical count `sum_{n=1}^{S} C(S-1, n-1) * n^(S-n)`: `19,693` for `S = 8`, `136,064` for `S = 9`).
   - Every single raw system must either:
     - Halt by direct deterministic simulation from `00`, recording its exact step count; OR
     - Carry a machine-checked finite non-halting certificate verified from first principles without unproved assumptions:
       - **Certificate Type `CYCLE`**: concrete step `t_1 >= 0` and period `p >= 1` such that `tape[t_1 + p] == tape[t_1]` with all intermediate tapes of length `>= 2`.
       - **Certificate Type `DFA_INVARIANT`**: concrete entry step `t_0 >= 0` and explicit finite DFA `M = (Q, A, delta, q_init, F)` such that (1) `tape[t_0]` (reached from `00` without halting) is accepted by `M`, (2) `M` rejects `epsilon` and rejects every single-symbol string `a` in `A`, and (3) for every word `a b u` accepted by `M`, its 1-step 2-tag successor `u w_a` is also accepted by `M` (checked exhaustively over the finite state-subset product graph of `M`!). Note: every exact cycle and every translated cycler is also representable or directly checkable via exact DFA closure or prefix-depletion translated cycle!
       - **Certificate Type `TRANSLATED_CYCLE`**: concrete step `t_1 >= 0`, period `p >= 1`, such that `|tape[t_1]| = 2*p` (so the entire `tape[t_1]` is consumed in exactly `p` steps while every intermediate step has length `>= 2`), and `tape[t_1 + p]` begins with `tape[t_1]` (`tape[t_1 + p] = tape[t_1] + suffix` with `|suffix| >= 0`), proving by induction that for every `m >= 0`, `tape[t_1 + m*p]` begins with `tape[t_1]` and never halts! (Or general multi-segment translated cycle verified by symbolic prefix consumption.)
       - **Certificate Type `COUNTER_INVARIANT`**: explicit closed-form parametric word family and finite inductive macro-step proof checked symbolically across all residue classes.
   - Report the exact maximum halting step count across all halting systems of size `S`.
3. **Criterion (a) / p3 champion gate (`8 <= S <= 11`)**:
   - Direct deterministic simulation from `00` halts in strictly more than `19` (`S=8`), `49` (`S=9`), `779` (`S=10`), or `196,841` (`S=11`) steps.
4. **Corruption gate**: Modifying one digit of the certificate file in `object/` must cause `verify-it-yourself/run_checks.sh` to exit nonzero and print `FAIL` as its final line.
