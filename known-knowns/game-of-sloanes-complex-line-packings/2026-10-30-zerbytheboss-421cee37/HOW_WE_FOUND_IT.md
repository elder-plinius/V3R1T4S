# How We Found It

contributor text, unverified

## Overview
We targeted the Game of Sloanes complex line packing challenge (Jasper, King, and Mixon, arXiv:1907.07848; `gnikylime/GameofSloanes`). The challenge seeks configurations of $n$ unit vectors in $\mathbb{C}^d$ minimizing the maximum overlap (coherence) $\mu = \max_{j < k} |\langle \phi_j, \phi_k \rangle|$.

## Investigation and Discovery
An audit of the live leaderboard repository revealed that several recent rows—notably those produced by heuristic solvers or LLM-prompted searches (`oai`)—had small residual slacks between the maximum overlap and the subsequent active pairs. Specifically, on row $(d=5, n=49)$, the published incumbent packing `5x49_oai.txt` (`https://raw.githubusercontent.com/gnikylime/GameofSloanes/master/CurrentBestPackings/5x49_oai.txt`, SHA-256 `bb50766d16ea892dad8645f2993ca38edd04c2f2fe5af895b8909b2819ef8280`) with coherence `0.54164128` had only a single pair attaining the peak overlap, with adjacent contacts lagging by $2.18 \times 10^{-7}$ and the 10th pair by $6.16 \times 10^{-6}$.

Starting from the published `5x49_oai.txt`, we SQP-polished the configuration using an active-set Sequential Quadratic Programming (SQP) equalizer on the horizontal tangent bundle $T_{[\phi]} (\mathbb{C}P^{d-1})^n$ that linearizes the active pairwise overlaps and solves a linear/quadratic minimax direction finding problem subject to strict quotient tangency constraints $\langle \phi_j, \xi_j \rangle = 0$. Each step was retracted to the manifold via Euclidean vector normalization.

Over 120 SQP iterations, the contact network equalized across 100+ active pairs, driving the global maximum coherence monotonically down from `0.54164128` to `0.5414603056425635743462895172126666579322`. Independent high-precision verification in `mpmath` at 40 decimal digits precision confirmed that the SQP-polished candidate `object/5x49_v3r1t4s.txt` achieves $\mu = 0.5414603056425635743462895172126666579322$, strictly lowering the live leaderboard record by $0.000180974357436425653710482787333342067819 \ge 10^{-8}$ (over 18,000 times the acceptance resolution).
