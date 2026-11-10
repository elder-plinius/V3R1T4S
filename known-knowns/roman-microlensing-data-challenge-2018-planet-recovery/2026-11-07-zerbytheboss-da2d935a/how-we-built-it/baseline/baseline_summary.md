# Baseline Reproduction Summary

Audited the 4 official human team submissions in the Zenodo `21235143` archive (`entries/ entry1..entry4`, Gould et al. 2026 `arXiv:2601.03555`, Tables 2-4):
- **Low-q planet recovery & False low-q (`win`, `p1`)**: Team 2 = `41 / 51` (`80.39%`) with `74` false low-q outputs; Team 1 = `35 / 51` (`68.63%`) with `9` false low-q outputs.
- **Three-class accuracy (`p2`)**: Team 1 = `268 / 293` (`91.47%`), Team 3 = `221 / 293` (`75.43%`), Team 4 = `201 / 293` (`68.60%`), Team 2 = `148 / 293` (`50.51%`).
- **Ultra-low-q planets (`log10 q < -5`, `p3`, events `47, 131, 152`)**: Team 1 = `1 / 3` (`Event 47`), Team 2 = `1 / 3` (`Event 131`), Team 3 = `0 / 3`, Team 4 = `1 / 3` (`Event 47`); `Event 152` (`log10 q = -5.78`) was missed by all 4 teams.
- **Wide-orbit low-q planets (`s > 2`, `p4`, 10 events)**: Best single team recovered `6 / 10`.
