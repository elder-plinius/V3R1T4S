# Record compared against
No record table exists for this quantity. Checked (see panel/novelty.md): OEIS (both onset conventions and keywords;
no match), arXiv (status page https://arxiv.org/abs/2505.05426 fetched 2026-10-23, HTTP 200, sha256
9d5f01827af97b964dc29f3c2a2c156d203f7395cdfee8277895f022e1db3a76), Jillhewar 2026, Ke's repository and Zenodo records,
LifeWiki/ConwayLife, MathWorld, MSE/MathOverflow, informal sites, and Reddit r/cellular_automata 1emq8r5 (read by hand
2026-10-23: about other rule strings; no seeds or onset table for RL).
Extracted cells compared: g(0)=9977 (A126978); g(4) <= 182 (Ke, different setting); f(0)=11 (Jillhewar).
Ke repository re-checked 2026-10-23 16:24Z (GitHub API, HTTP 200): last push 2026-10-16T05:32:07Z; re-check before any submission.

## Re-check for this package (run 2026-10-24-0139)
- H. Ke repository re-fetched 2026-10-24T01:39:03Z (HTTP 200, page sha256 4749cac7...91d3 in the run's data/): only
  branch main at 22e0c9edcc, last commit 2026-10-16T05:31:52Z. No change since 2026-10-23. No onset table. The
  four_cell_port README says the four-cell result is for the fixed inward boundary pose, and its output times are
  certificate boundaries, not minimal onsets. The user's other repositories have no Langton work.
- The fresh novelty reviewer (panel/novelty.md) also found a 2026-10-15 YouTube clip that shows one black cell below
  the ant giving a road at step 310 (a single example, matching g(1), with no minimality claim and no other k). Ke's
  one-black witness list also has minimum 310. Neither publishes the table or a smaller onset.
