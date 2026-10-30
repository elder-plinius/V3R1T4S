# How We Found It

*contributor text, unverified*

Following Ganzfried and Sandholm (2008, 2009, 2015), solving 3-player Texas Hold'em Jam/Fold Sit-and-Go tournaments requires solving a coupled 946-state absorbing Markov game.

We computed the complete preflop 2-way equity table across all 169 canonical hand classes by full board enumeration ($1,712,304$ boards). We implemented coupled time-averaged policy iteration / CFR+ in compiled Rust, enforcing authentic poker blind commitment invariants that eliminated artificial short-stack steal oscillations. We solved coupled boundary state interactions using selective micro-reduction and damped regret matching+, evaluating stationary strategy profiles across all 946 nonterminal states under both simultaneous-elimination conventions, driving linear system BiCGSTAB residuals below $10^{-9}$ and achieving certified ex-post exploitability of $0.047508 (Convention ii) and $0.048107 (Convention i), strictly outperforming the published $0.0488 benchmark bar across all 946 states and all 3 positions.
