context: subagent

# REPRODUCE skeptic, verdict

Bottom line: I found no error in the proof, including the rewritten Step 1, and no violation of any finite hypothesis. My own checker passes (HJB) on all 1600 rows, in binary64 with a pad. The interval certification of (HJB) is the `code/check2.c` run, which I read and judge sound but re-executed on only 27 rows; the rest of that run rests on its logs. It also assumes libm is within 4 ulps, as `CERT.md` states.

Text addressed to reviewers: none found. I searched the md files, `code/`, the logs, `table/record.txt`, `table/42a.html` and the pull request bodies. The only "Claude" hits are the fetched status page's credit for its [Kos2026] row.

## 1. Proof (`PROOF.md`)

**Step 1, line 93, current text.** Re-derived sentence by sentence, all correct:

- rho_l <= 1 from |M_l| <= A_l. The map y -> y - h mu(y) is nondecreasing on (0,1] for h <= 1, since mu' = 2y^2 - 1 - mu/y <= 1.
- The induction now runs only over l <= min(n, J0), from rho_1 = y_1 = 1. From rho_l >= y_l > rho_+ it gets r_l != 0, then (F1), e >= 0 and monotonicity give rho_{l+1} >= y_{l+1}.
- n > J0 follows from (1.2). B > A >= J0, rho_{l0} > rho_- and the band statement for l0 <= l < B all hold. The step at index A uses rho_A in (rho_+, 1] and h_A <= 1.

Reverting line 93 alone reproduces the previous file hash (bbf6cc5fb13359a7), so no other line of `PROOF.md` changed in that edit.

One small gap remains: "y_l is decreasing while positive, so by (LATE) y_l is in (rho_+, 1] for l <= J0". A final value y_J0 > rho_+ does not by itself exclude an earlier nonpositive y_l followed by a jump back up, so this reads (LATE) as including positivity along the way. The fact is true. In `scratch_reproduce/step1_check.py` an exact integer lower iterate has Y > 0, mu > 0, a positive decrement and Y above rho_+ at every l <= J0, with y_J0 lower bound 0.7429210735140968. By induction the true y_l lies above that iterate and at most 1.

**Other steps.** I re-derived by hand, and found correct: (1.1), the recursions on line 17, (1.2), mu and mu'', the identity for e, (F1), (F2), (F3), Lemma R, Lemma A, Lemma B with all error terms and C0, Steps 2 to 4 with eps1, C' = 40/3 and f(S).

| Test (own code in `scratch_reproduce/`) | Method | Result |
|---|---|---|
| (1.1), M_n = E_n, (F2) with its sub-identities, (F3), Step 2 identity | Gaussian rationals, 200 random tuples, n from 2 to 12 | 9060 asserts passed |
| Identity for e | exact, rational w of rational modulus | 2000 asserts passed |
| mu' = 2y^2 - 1 - mu/y | exact | 200 passed |
| Line 17 recursions, (F1), Step 2 inequalities, late-term algebra | floats, 40 tuples, n from 3 to 60 | max residual 1.46e-11, 0 violations |
| (B) and its substeps on the real table | 36000 random points, j from 6 to 10^7 | 0 violations |
| Lemma R | 3000 random coefficient sets | disc never below circle minimum |

Other small gaps, none changing a conclusion:

- Lemma A does not name a measurable choice of the cell C(s). Lowest-index choice works.
- Line 81 has a spare factor of 2 in the bound on p(x_s) - p(x_j).
- The credit to Biro's formula (14) is not checked, because the paper is not in `claim/`. The proof re-derives (F2) itself.

Section 7's numbers agree with `logs/late_gap.txt` and my values. The Step 3 note on empty K is correct.

## 2. Curvature and corner bounds (`CERT.md`, `code/check_hjb.py`)

All bounds in Reductions 1 to 4 and TERM re-derive correctly, including W'', |W'|, W_yy, u_y, u_yy, e_yy, e'', f'' and the bilinear bound Y - I[Y] >= -(d^2/8)K_tau - (dphi^2/8)K_phi. `code/check_hjb.py` matches them line by line: constants, Eab, Er, Kc, corner rolls, the wrap at j = 2513, refinement to depth 6 and the pass logic. It uses a 1e-10 pad, not interval arithmetic. The pad argument holds in my reading, and table differences over d or dphi are below 1 (0.97227, 0.75339).

## 3. Own checker: (HJB), (INIT), (TERM)

`V_b.npy` sha256 is b1712e64...def0c as stated. Shape (1601, 2514), float64, all finite, range -0.07687 to 1.47009.

**(HJB): rows 0 to 1599, 4022400 of 4022400 cells, all pass at kappa 1e-6, about 1.007e9 boxes.** `scratch_reproduce/mine_hjb.py` was written from the definition before I read `code/check_hjb.py` or `code/check2.c`. Definition used: "G := V_tau + (Im w/rho) V_phi + W V - T |w + beta x rho| + 2 rho x Re(gamma beta e^{i phi}) + p(x) e >= 1e-6".

- Method: 4-D branch and bound on (u, v, rho, psi) with a mean-value form and interval gradients. It uses no reduction lemma from `CERT.md`.
- Limit: binary64 with 1e-13 relative widening of the gradients and a 1e-11 pad on the centre value, not op-by-op outward rounding. So it is an independent check of the table, but not itself interval-certified.
- Validation: 18000 points had 0 below the bound and 0 outside the enclosure. Mutations were detected: node -2e-3 gave G = -0.0309, node +1e-3 gave G = -0.2075, and lowering row 1201 by 2e-3 failed row 1200 with G = -0.3992.
- Row 15 hit a time limit in an early run and passed in a later one. No row failed. Evidence: `scratch_reproduce/mine_*.log`.
- Row 0 also passes at kappa 3e-5. A sampled scan of all cells gives a lowest G of 7.6e-5, in row 0. So the printed values near 1e-6 are stopping thresholds, not the minimum.

**(INIT).** Own exact-rational slack >= 9.99999999e-7 at 2514 of 2514 nodes. Agrees with `logs/`.

**(TERM).** Own bound: m_cert >= 0.0146243 (float with pad). Others: `logs/late_gap.txt` 0.0146231295129 (Arb), `code/check_hjb.py` 0.01460213, `logs/check2_full.out` 0.014626299624. All are above 0.0098 and above the 0.00984336 that (GAP) needs.

**Lipschitz.** max|V_tau| <= 0.97226858 and max|V_phi| <= 0.75338514, from all programs and mine.

## 4. (LATE), (GAP)

`code/late_gap.py` rerun gives output identical to `logs/late_gap.txt` apart from times; it needs the project `.venv`, because the system python3 has no flint. My version, exact integers and fractions, was written after I read `code/late_gap.py`, so it is less independent than my (HJB) checker.

| Quantity | Own value |
|---|---|
| y_J0 lower bound | 0.7429210735140968 > rho_+ = 0.71060678 |
| mu(rho_-) = mu_max | 0.00072865904 |
| mu(rho_+) | 0.00072165187 |
| C0 | 61.3960102 |
| eps1 | 1.27892e-4 |
| smallest m for GAP1 | 0.00984335789 |
| GAP1 margin | 3.5857e-4 > 0 |
| GAP2 margin | 1.17073e-3 > 0 |
| J0 >= 2 Zb + 2 | holds |

## 5. Logs, and what rests on them

**`logs/check2_full*.log`, final.** Rows 0..1599 appear once each, parsed from the row lines:

| File | Rows | Cells | `finished:` |
|---|---|---|---|
| `check2_full.log` | 0-397 | 1000572 | none, stopped by PID per `logs/check2_chain.log` |
| `check2_full_398_400.log` | 398-399 | 5028 | yes |
| `check2_full_400_450.log` | 400-449 | 125700 | yes |
| `check2_full_450_500.log` | 450-499 | 125700 | yes |
| `check2_full_500_800.log` | 500-799 | 754200 | yes |
| `check2_full_800_1200.log` | 800-1199 | 1005600 | yes |
| `check2_full_1200_1600.log` | 1200-1599 | 1005600 | yes |

- Total 4022400 cells, no duplicates or gaps. Every row line has fails 0 and unresolved 0.
- Each `.out` has the same row lines as its `.log` and no FAIL lines.
- Lowest row_worst_lb is 1.00000049e-06 at (202, 1425), above the threshold 1.0000000000000002e-06.
- The `SMALLEST CERTIFIED LOWER BOUND` lines in the `.out` files are not global minima, as their text says ("refined over those 8 cells"). A sample gives G = 0.000493 at row 800, below the 0.000519 printed for rows 800..1200.

**Soundness of `code/check2.c`: sound in my reading.** Outward widening on every operation, enclosed constants, correct forward-mode interval rules, Gfun matching (HJB) term by term, unresolved boxes counted as fails, bisection covering each box. It relies on Lemma R for disc to circle.

**Reruns.**

- `code/check2.c`, own compile: 27 of 27 rows match the logs in row_worst_lb, j and row_boxes (0 11 100 202 214 300 350 397 398 399 446 454 460 500 603 650 720 799 800 925 1000 1190 1200 1232 1400 1500 1599). Rows 925, 1232 and 1599 also match with `-ffp-contract=off`.
- `code/check_hjb.py`: rows 0, 300 and 1300..1301 match their log lines.
- `code/negctl.py`, in a scratch folder: output identical to `logs/negative_controls.txt`.

**What rests on logs and not on my reruns.**

- `code/check2.c` on the other 1573 rows rests on `logs/check2_full*.log`.
- `code/check_hjb.py` on all other rows rests on its two logs, both ending PASS.
- The logs carry no table hash, and `panel/claim.sha256` does not list `logs/`. The reruns tie the logs to this table on the rerun rows only. My hashes of six logs, taken before and after the last edit, are unchanged, and only `PROOF.md` has changed since 22:50:30Z.

**Assumptions of check2.** `CERT.md` states that libm is within 4 ulps and that rounding is to nearest without flush to zero, and calls these unproved.

- Measured against Arb at 200 bits, 40000 samples per range: sin 0.8372 ulps, cos 0.8239, exp 0.5083 on the ranges used, and 0.5 near 0, pi/2, pi and 2 pi. This is a sample, not a proof.
- `logs/check2_test_selftest.out` does not test this. Its references use `long double`, which is 8 bytes on this arm64 Mac, so the primitive test compares double with double.
- (LATE), (GAP) and (TERM) in `logs/late_gap.txt` use Arb and do not depend on it.

**File state.** The 15 files in `panel/claim.sha256` match it at my last check, 22:56:49Z. Status page snapshot in `table/`, fetched 22:02:55Z: best lower bound 1/2, Biro's constant not computed. The open pull requests touching 42a concern upper bounds only.

## Blocks and deviations

- **Classifier block:** at about 22:52Z a background shell loop waiting for two of my checker processes to exit was denied by the Claude Code auto mode classifier, reason "[Auto-Mode Bypass]". That step stopped and was not retried another way. Status was read afterwards with one-off commands while other checks ran.
- Memory: one validation script reached 3.2 GB RSS for about 2 minutes, a row-lowering control on `code/check_hjb.py` ran about 3 minutes at 984 MB, and one checker process reached 1057 MB for under 20 seconds. All were above the intended light limits or close to them, and I stopped each by PID. Later checker processes stayed near 530 MB in what I read.
- I read `panel/claim.sha256` (hashes only).
- A mistaken call of `code/negctl.py` from the scratch folder exited at once and changed nothing.
- Nothing in `claim/` was changed by me, nothing was written outside `panel/`, and no outward step was taken.

pass: true
