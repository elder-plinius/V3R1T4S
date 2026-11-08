# Novelty skeptic: VarBench J1J2/square_100_P_0.9.md

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Claim under test (claim/CLAIM.md): object/r10_J0.9_B1.pt (sha256 e68644979db4d9764ac1787d1c064fe18c4750cb4cb47ee573e40588bcd9c485,
re-hashed here, matches; object/model/nqs.py 122e54f2cdecae6a5bad5820d14165abd8e849ee20ff4e3d83dd9901ea00c03d, matches)
with claimed E = -253.75342431118173 +- 0.0039992310644334774 (claim/results/S2_plain_4242.json), DIS cross-check
E = -253.7473816594384 +- 0.0032485374695990594 (claim/results/S3_dis_2718.json), S1 E = -253.748446817066 +- 0.003746765388504872
(claim/results/S1_plain_31337.json). Pauli convention, E = 400 e.

## 1. Status source (one GET each, curl, User-Agent "V3R1T4S-research-run (curl)")

| UTC | HTTP | URL | sha256 / result |
|---|---|---|---|
| 2026-10-23T17:28:15Z | 200 | https://raw.githubusercontent.com/varbench/varbench/main/J1J2/square_100_P_0.9.md | 0d0e85250570199179a9696a8ab8e71292b99993788ab492f64039b5d8c5a34d (796 bytes) |
| 2026-10-23T17:28:22Z | 200 | https://api.github.com/repos/varbench/varbench/pulls?state=open&per_page=100 | bcc48863d3b4c1c4afbecf8b16a7f64da3b50a5c6789f7499495f2287d8f09d4; 1 open PR |
| 2026-10-23T17:28:25Z | 200 | https://api.github.com/repos/varbench/varbench/commits?per_page=5 | 3a54755e6bafba6f1e023dd7d7c0f3a8c84c5a6e06e9a243501407c58c35be00 |
| 2026-10-23T17:28:39Z | 200 | https://api.github.com/repos/varbench/varbench/pulls/5/files?per_page=100 | c1b8e5133c6468993f36aa0c056abadab3310c8200e952a1a6514ec3c4448841 |

- The live table file is byte-identical to the claim's copy claim/inputs/varbench/square_100_P_0.9.md (same sha256 0d0e8525...).
  Rows (values as fetched): DMRG (bond dimension = 1024) -250.78657331066935; RBM (alpha = 1) -238.966 (0.013);
  Jastrow baseline -235.905 (0.010). Best row: DMRG -250.78657331066935.
- Last commit 390a21eab7eb, 2024-10-22T08:50:50Z ("Merge pull request #38 from varbench/badge"), same as the claim states.
- varbench/varbench open PRs: one, #5 (external contributor, created 2023-04-02T21:26:22Z, "Add results for symmetry projected RBM and
  Lanczos"). Its files touch J1J2/square_100_P_0.2, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8 and _1 (and 36-site files), but NOT
  J1J2/square_100_P_0.9.md. No pending row for this file.

## 2. This repo (V3R1T4S)

| UTC | HTTP | URL | result |
|---|---|---|---|
| 2026-10-23T17:28:48Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S | default_branch main, pushed_at 2026-10-22T12:58:37Z |
| 2026-10-23T17:28:57Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | sha256 fe08d1550543a39a7f91211ef3bb3bf2125f65a2bebcfe115a194d23012c290e; page 1 of 4 (PRs 631..522), regex varbench/J1J2/Heisenberg/square_100/variational/NQS/spin: 0 hits |
| 2026-10-23T17:29:02Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1, 31235 bytes |
| 2026-10-23T17:29:21Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+varbench+OR+J1J2+OR+Heisenberg+OR+variational | total_count 0 (all PR states) |
| 2026-10-23T17:29:31Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+is:open | total_count 305 (sanity check that the search covers this repo's PRs) |

- TROPHY_CASE.md lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer,
  VNN-COMP, RobustBench) plus cipher commitments; grep for varbench|J1J2|Heisenberg|square_100|variational|NQS|neural: no match.
  No VarBench record exists in the repo, and no PR (open or closed) mentions VarBench, J1J2, Heisenberg or variational.

## 3. The bar (lowest published variational energy for the identical system)

- arXiv:2606.04558 (P. S. Golubev, I. A. Iakovlev, V. V. Mazurenko, "Extremely slow scaling of minimal Hamming distance in
  quantum sampling data"), Table I, J2 = 0.90, column "10 x 10, ViT (this work)": -0.634170 per site; column
  "10 x 10 (previous works)": "-".
  - https://arxiv.org/pdf/2606.04558v2, 2026-10-23T17:33:17Z, HTTP 200, sha256 9064b3c7893c4e6692524eb19fc2ef73b82e04096b5c4431664c5030da414f19
    (identical to the hash recorded in claim/inputs/bar/arxiv_2606.04558v2_tableI.txt).
  - https://arxiv.org/pdf/2606.04558v1, 2026-10-23T17:38:05Z, HTTP 200, sha256 341be5e085635203a9b9d8d9b47634bdc454f983d2078adc953b8e0182286ee9:
    same J2 = 0.90 row (-0.634170). arXiv API lists v2 (updated 2026-09-15) as the latest version.
  - Same system: the text states "square lattice with periodic boundary conditions and N = 36, 64 and 100 spins"; the Table I
    caption calls the values "variational NQS approach utilizing vision transformer wave function (ViT)" (not extrapolated).
    Convention: their J2 = 0 10 x 10 value -0.671476 sits just above the QMC -0.67155266 they cite, i.e. S.S per-site units,
    so E_Pauli = 400 x (-0.634170) = -253.668 (computed). No error bar is printed.
  - Golubev's own "previous works" column is "-" at J2 = 0.90 for 10 x 10: independent support that no earlier 10 x 10 value
    exists at this coupling.

## 4. Literature search (last 24 months and older 10 x 10 sources)

arXiv API (https://export.arxiv.org/api/query, sorted by submittedDate desc, one request at a time, >= 3 s apart; a first
attempt over http at 2026-10-23T17:30:10Z returned HTTP 301 (redirect to https, not a block) and was re-issued over https):
- 17:30:18Z HTTP 200: abs:"J1-J2" AND abs:square AND (neural OR transformer OR network) - 9 results, nothing new.
- 17:30:30Z HTTP 200: abs:"neural quantum states" AND (frustrated OR J2 OR J_2) - 27 results.
- 17:30:43Z HTTP 200: abs:Heisenberg AND abs:square AND (J2 OR J_2 OR frustrated OR J1J2) AND (neural OR transformer OR variational) - 70 results.
- 17:30:55Z HTTP 200: (ti/abs J1-J2 or J_1-J_2) AND (Heisenberg OR spin), 300 newest (back to 2024-09).
- 17:31:41Z, 17:34:20Z, 17:39:38Z HTTP 200: id_list abstract lookups of the candidates below.
- one broad query (transformer/convolutional/NQS/foundation AND Heisenberg/antiferromagnet/frustrated; time not captured,
  its printed output was filtered away; results parsed afterwards from the saved file).
- 17:32:36Z HTTP 200: abs:stripe AND (neural OR transformer OR variational) AND (Heisenberg OR J2) - 22 results.
- 17:38:37Z HTTP 200: ti:Lanczos AND ti:"neural network quantum states" (to locate Chen et al. on arXiv).
- 17:39:12Z HTTP 200: abs:"V-score" OR abs:VarBench OR "variational benchmark".
- 17:39:25Z HTTP 200: title query neural/transformer/"quantum states" AND Heisenberg/frustrated/spin/magnets/antiferromagnet.
Date screen used: submitted >= 2024-09-01 (wider than 24 months), plus older 10 x 10 benchmark papers.

Full texts read (each one GET from https://arxiv.org/pdf/[arXiv id], all HTTP 200, between 2026-10-23T17:33:17Z and 17:38:48Z;
grepped for J2 values, 10 x 10, and energies near -0.63 / -253):

| arXiv | paper | 10 x 10 at J2 = 0.9? |
|---|---|---|
| 1903.06713 | Choo, Neupert, Carleo (CNN) | Table I 10 x 10: J2 = 0, 0.2, 0.4, 0.45, 0.5, 0.55, 0.6, 0.8, 1.0; no 0.9 |
| 2206.14307 | Chen et al. (symmetrized RBM + Lanczos; NeurIPS 2022) | Table 5 10 x 10: J2 = 0, 0.2, 0.4, 0.6, 0.7, 0.8, 1.0, 1.2, 1.5; no 0.9 |
| 2002.04613 | Szabo, Castelnovo | 10 x 10 at J2 = 0.5 only |
| 2211.05504 | Viteritti, Rende, Becca (ViT) | J2/J1 = 0, 0.4, 0.8 mentions; no 10 x 10 J2 = 0.9 |
| 2211.07749 | Roth, Szabo, MacDonald (GCNN) | 10 x 10 at J2 = 0.5, 0.55 |
| 2403.07795 | Rende et al., fine-tuning NQS | J2 = 0.1-0.6 |
| 2502.09488 | Rende et al., Foundation NQS | 10 x 10 J2 in [0, 1] but order parameters only; energies compared at J2 = 0, 0.5 |
| 2502.01264 | Generalized Lanczos for NQS | J2 = 0.5, 0.55, 0.6 |
| 2503.17140 | Adiabatic fine-tuning of NQS | no 10 x 10 |
| 2505.03466 | Nutakki, Shokry, Vicentini (ConvNext) | J1-J2 at 0.5 (0.8/1 are Shastry-Sutherland couplings) |
| 2506.01891 | KAN NQS | J2 <= 0.6, no 10 x 10 |
| 2507.20510, 2509.02658, 2510.02051, 2510.08430 | sampling / degenerate states / sign structure / QGT blocks | J2 = 0 or 0.5 only |
| 2602.03031 | physics-inspired transformer QS | J2 = 0.5 |
| 2603.11189 | DysonNet | no 10 x 10 |
| 2606.02794 | Rende et al., Scaling laws for NQS | J2/J1 = 0, 0.125, 0.5 |
| 2606.07825 | Projected inverse iteration | J2 = 0, 0.5 |
| 2606.30464 | NQS-Agent | J2 = 0.50, 0.55 |
| 2607.02292 | NQS / reinforcement learning | J2 = 0, 0.5 |
| 2607.18865 | annealed gradient descent NQS | J2 = 0.5, 0.6, 0.8 mentions; no 10 x 10 |
| 2609.23334 | SR as statistical filtering | J2 = 0.5 |

Abstracts only (not about 10 x 10 J2 = 0.9 energies): 2607.00398 (HQT; 8 x 8 and 10 x 10 at J2 = 0.5), 2602.02665 (20 x 20,
triangular and square), 2609.40209 and 2609.05556 (foundation-NQS phase design / Kibble-Zurek), 2602.21468 (VAE on ED/DMRG,
L <= 8), 2511.17957, 2411.14114, 2411.17452, 2603.02316, 2604.27738, 2606.17045.
Web search (4 queries, incl. "J2/J1 = 0.9" 10 x 10 and the VarBench filename): no 10 x 10 PBC J2 = 0.9 variational energy found.
Blocked: https://openreview.net/pdf?id=qZUHvvtbzy returned HTTP 403 at 2026-10-23T17:38:27Z (stopped with that host, no
retry); the same paper was read from arXiv:2206.14307 instead.

Lowest known variational energy for the identical system: -253.668 (Golubev et al., ViT). Best VarBench row: -250.78657331066935.
Nothing lower was found.

## 5. Margin (criterion: max(3 sqrt(sigma_new^2 + sigma_best^2), 1e-6 |E|), sigma_best = 0 as none is stated)

| run | E - bar gap | required margin | gap / margin | gap to DMRG row |
|---|---|---|---|---|
| S2 (headline) | 0.085424 | 0.011998 | 7.12 | 2.966851 |
| S3 (DIS) | 0.079382 | 0.009746 | 8.15 | 2.960808 |
| S1 | 0.080447 | 0.01124 | 7.16 | 2.961874 |

- Robustness to the unprinted error on the bar: the gap would only fall to the margin if sigma_bar were 0.028192 (S2),
  0.026261 (S3), 0.026553 (S1) in Pauli units, i.e. about 7.048e-05 / 6.565e-05 / 6.638e-05 per site. A table printed to six
  decimals is not consistent with an error that large, so this does not block. Rounding of -0.634170 (half of 1e-6 per site) is at most 0.0002 Pauli.
- Not a tie: all three estimates are strictly below every known value by 7-8 times the margin.

## 6. Scope and caveats

- Novelty is judged on the claimed E. I did not re-measure the energy. If the reproduction skeptic's own Monte Carlo
  estimate (>= 1e5 effective samples) lands above -253.668 minus the margin, this pass does not carry over.
- Plausibility only (not a correctness check): claim e = -0.63438356 per site is 0.00021356 per site below the ViT value; the
  6 x 6 ED (-0.649048) to 10 x 10 rise it implies, 0.014664, sits between the rises at J2 = 0.8 (0.012447) and J2 = 1.0
  (0.01766) computed from the 6 x 6 ED and 10 x 10 RBM values of 2206.14307; nothing looks unphysical.
- injection_suspected: none (no fetched page, PR body, or claim file told the agent to do anything).

novelty: PASS - strictly below the best VarBench row and the lowest published variational energy for this system
(-253.668, arXiv:2606.04558 v1/v2), with nothing lower found in the file, its open PR, V3R1T4S TROPHY_CASE.md / PRs, or the
2024-09 to 2026-10 literature.
pass: true
