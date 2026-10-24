# Three-player von Neumann poker (Krityakierne–Thanatipanonda–Zeilberger): the conjectured threshold profile is a Nash equilibrium for every bet b > 0

## What

For every real b>0, the paper's Eq. A-C have exactly one solution with 0<A<C<B<1, and in the arXiv:2407.16155 Section 4 three-player continuous game where II and III decide simultaneously, seeing only their own hand and I's bet, the threshold profile (I bets iff x<A or x>B; II and III call iff y>=C) is a Nash equilibrium against all measurable, possibly randomized, unilateral deviations, each prescribed action being a best response at every hand value in (0,1) (and at 0 and 1 only under the continuity-extended endpoint actions), which settles partial win p1 but not main branch (A), because the exact b=2 value 0.1225570747148686867... does not match the printed digits 0.122557074714865.

(Panel status: CONFIRMED_PARTIAL, partial win p1 of the bank target `three-player-von-neumann-poker-equilibrium`;
`panel/gate.md`. The main criterion's case (A) is NOT claimed: it also requires the exact b = 2 value to match the
paper's printed 0.122557074714865 "to the digits given", and the exact value is 0.12255707471486868673777879827615…,
which rounds to 0.122557074714869.)

In words: in the game of Section 4 of arXiv:2407.16155 (antes 1, independent uniform(0,1) hands; Player I checks to a
three-way showdown or bets b; II and III then call or fold, each seeing only their own hand), the paper's
"conjectured Nash equilibrium" (I bets iff x < A or x > B; II and III call iff their hand exceeds C, with A, B, C from
the paper's three indifference equations Eq. A–C) is a genuine Nash equilibrium for every real b > 0, and Eq. A–C have
exactly one ordered solution 0 < A < C < B < 1 for every b > 0. The proof is in `object/all_b_proof.md` (with
`object/proof.md`); exact polynomial identities are in `object/universal.json`, the independently generated raw
payoff table in `object/raw_payoffs.txt`, and the b = 2 specialisation (defining polynomials and rational isolating
intervals of A, B, C and the value) in `object/equilibrium.json`. PROVED-HERE (computer-checked identities plus
elementary analytic steps: monotonicity, the intermediate value theorem, pointwise optimality; not formalised in a
proof assistant).

At b = 2: A = 0.137058194328368924134…, B = 0.829422249795390707454…, C = 0.641304115985178878622…, value to I
0.122557074714868686737778798276… (degree-8 algebraic numbers).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. About 10 seconds on a laptop; needs only `sh` and Python 3 (standard library); nothing is
downloaded or written. It runs four exact checkers of the original certificate and one independently written checker
(an exact terminal-utility integrator compared with the closed-form payoffs, every polynomial identity over Q, and the
b = 2 thresholds and value). Details: `RUN_IT_YOURSELF.md`; real output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| cell | published status | source | URL | fetched (UTC) |
|---|---|---|---|---|
| three-player continuous game, Section 4, threshold profile from Eq. A–C | **conjectured** ("conjectured Nash equilibrium strategies"; only the three indifference conditions are derived) | Krityakierne, Thanatipanonda, Zeilberger, arXiv:2407.16155 v1 (23 Jul 2024); the 2025 journal version also calls it conjectured | https://arxiv.org/abs/2407.16155 | 2026-10-15T13:12:53Z and (panel) 2026-10-15T19:32:01Z, HTTP 200 |
| this package | **proved for every b > 0** (partial win p1) | `object/` | — | — |

Full snapshot with hashes: `the-record-we-beat/RECORD.md`. The panel's own fetches and searches: `panel/novelty.md`.

## Not claimed

- Not the main criterion's case (A): the paper's printed b = 2 value 0.122557074714865 (and its printed A and C) are
  wrong in the 15th decimal; the exact value cannot match "the digits given". Printed B matches.
- Nothing about other equilibria (uniqueness), the optimal bet size, the sequential variant in which III sees II's
  action, or games with more players. (Work on these exists in the producing workspace but has not been panelled.)
- Endpoints: on the closed interval [0, 1], the paper's literal "otherwise" actions at the single hands x = 0, x = 1
  (check) and y = 0 (call) are not best responses; the certificate uses the continuity-extended actions there. These
  are probability-zero hands and change no payoff.
- Not formalised in a proof assistant; the analytic steps are written out and were re-derived by the panel.
- The paper's other statement "b* ≈ 2.07, value 0.122590664136184" is not part of this claim (an unpanelled
  computation in the producing workspace suggests 0.122590664136184 is the value at b = 2.07 exactly, not at the
  maximiser b* ≈ 2.0723786).
- Not submitted anywhere; the authors were not contacted.

## Credits

- Tipaluck Krityakierne, Thotsaporn "Aek" Thanatipanonda and Doron Zeilberger, "von Neumann and Newman Pokers with
  Finite Decks", arXiv:2407.16155 (https://arxiv.org/abs/2407.16155), Mathematical Intelligencer (2025): the game,
  the conjectured profile and Eq. A–C. This package verifies their proposed profile; it does not introduce it.
- John von Neumann and Oskar Morgenstern (two-player model); C. Ferguson and T. S. Ferguson, "On the Borel and von
  Neumann poker models" (https://www.math.ucla.edu/~tom/papers/poker1.pdf), used for the two-player calibration.
- Prior work checked and found to concern different games: J. Nash and L. Shapley (1950); Č. P. Šimelis, Lithuanian
  Math. J. 17 (1977) 572–579 (https://doi.org/10.1007/BF00972283); M. Sakaguchi and S. Sakai, Math. Japonica 37
  (1992) 1147–1160.
- Produced in a V3R1T4S workspace by a Codex-based agent run (the certificate and proof) and a Claude-based run
  (independent re-derivation, prior-art search and the three-skeptic panel); credit name r-nikhil.
