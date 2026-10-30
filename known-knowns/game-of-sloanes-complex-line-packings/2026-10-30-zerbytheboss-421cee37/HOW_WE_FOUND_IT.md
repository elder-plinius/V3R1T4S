# How We Found It

contributor text, unverified

## Overview
We targeted the Game of Sloanes complex line packing challenge (Jasper, King, and Mixon, arXiv:1907.07848; `gnikylime/GameofSloanes`). The challenge seeks configurations of $n$ unit vectors in $\mathbb{C}^d$ minimizing the maximum overlap (coherence) $\mu = \max_{j < k} |\langle \phi_j, \phi_k \rangle|$.

## Investigation and Discovery
An audit of the live leaderboard repository revealed that several recent rows—notably those produced by heuristic solvers or LLM-prompted searches (`oai`)—had small residual slacks between the maximum overlap and the subsequent active pairs. Specifically, on row $(d=5, n=49)$, the incumbent record of `0.54164128` had only a single pair attaining the peak overlap, with adjacent contacts lagging by $2.18 \times 10^{-7}$ and the 10th pair by $6.16 \times 10^{-6}$.

We constructed an active-set Sequential Quadratic Programming (SQP) equalizer on the horizontal tangent bundle $T_{[\phi]} (\mathbb{C}P^{d-1})^n$ that linearizes the active pairwise overlaps and solves a linear/quadratic minimax direction finding problem subject to strict quotient tangency constraints $\langle \phi_j, \xi_j \rangle = 0$. Each step was retracted to the manifold via Euclidean vector normalization.

Over 120 SQP iterations, the contact network equalized across 100+ active pairs, driving the global maximum coherence monotonically down from `0.54164128` to `0.5414603056...`. Independent high-precision verification in `mpmath` at 40 decimal digits precision confirmed that the candidate achieves $\mu \approx 0.54146031$, strictly lowering the live leaderboard record by $0.000180974357... \ge 10^{-8}$ (over 18,000 times the acceptance resolution).
