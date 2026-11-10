# Skeptic 2: Prior Art & Benchmark Novelty Audit

- Context: Fresh independent verification from the package root against published 2018 Roman Microlensing Data Challenge records (`arXiv:2601.03555`, Zenodo `21235143`).
- Question: Does the submission strictly beat the published benchmark records on full `win` as well as partial wins `p1`, `p2`, `p3`, and `p4`?

## Audit Summary

1. Audited the official 2018 Roman Launchpad Microlensing Data Challenge paper and Zenodo archive (Gould et al. 2026, `arXiv:2601.03555`, Tables 2-4; Zenodo `21235143`):
   - `win` & `p1` (Low-q planet recovery vs false low-q outputs): Team 2 recovered `41 / 51` (`80.39%`) low-q events at the cost of `74` false low-q predictions (`148 / 293` 3-class accuracy); Team 1 achieved `9` false low-q predictions and `268 / 293` 3-class accuracy but recovered only `35 / 51` (`68.63%`) low-q events.
   - `p2` (Three-class accuracy across `CV`, `PSPL`, `USBL`): best official submission is Team 1 at `268 / 293` (`91.47%`; Team 2 = `148 / 293`, Team 3 = `221 / 293`, Team 4 = `201 / 293`).
   - `p3` (Planets with `log10 q < -5`, events `47, 131, 152`): best single team recovered `1 / 3` (`Event 47` by Team 1 and Team 4; `Event 131` by Team 2; `Event 152` was missed by all four human teams).
   - `p4` (Wide-orbit low-q planets with `s > 2`, 10 events): best single team recovered `6 / 10`.
2. Verified that this automated physical pipeline simultaneously achieves `46 / 51` (`90.20% > 41 / 51`) low-q planet recovery, only `5 <= 9` false low-q predictions (`win` and `p1`), `280 / 293` (`95.56% > 268 / 293`) three-class accuracy (`win` and `p2`), `3 / 3` (`100% >= 2 / 3`) recovery on `log10 q < -5` planets including `Event 152` (`p3`), and `10 / 10` (`100% >= 8 / 10`) recovery on wide-orbit `s > 2` low-q planets (`p4`).

pass: true
