# Research charter v2 (2026-11-21), methods only

## Quarries

### Q1 teq-small-counterexample
- question: Is there a tournament on at most 23 alternatives with two distinct inclusion-minimal TEQ-retentive sets (Schwartz's conjecture fails below 24)?
- shape: counterexample
- where defined: bank `schwartz-teq-counterexample-below-24`; Schwartz (1990); Brandt and Seedig, arXiv:1302.5592 (24-vertex example); Yang, arXiv:1611.03991 (none on 14 or fewer).
- status to confirm first: no published counterexample below 24 and no lower bound above 14 since Yang.
- why us: a voting-rule conjecture read as a system to exploit; structured search over tournaments built from the 24-vertex example.
- weight: 5
- wild: no

### Q2 gsp-poa-above-three-slot
- question: Is there a full-information GSP auction instance with a pure Nash equilibrium (no overbidding) whose welfare ratio exceeds the three-slot value 1.259134?
- shape: counterexample (explicit instance, bids and tie-breaking, checked in exact rationals)
- where defined: bank `gsp-pure-nash-poa-conjecture`; Caragiannis et al., JET 2015, arXiv:1201.6429; Lucier and Paes Leme, arXiv:1011.3268.
- status to confirm first: whether Ding, Wu, Qin and Liu (arXiv:1305.5404) has been refereed, extended or refuted.
- why us: worst-case behaviour of ad auctions sits between strategic-agent modelling and attention markets.
- weight: 4
- wild: no

### Q3 selfish-mining-certified-bound
- question: Can the optimal selfish-mining revenue in the untruncated SSZ model (gamma = 0) be certified below 0.70099 at alpha = 0.45 or below 0.90466 at alpha = 0.475?
- shape: bound (machine-checkable certificate from the over-paying finite MDP)
- where defined: bank `bitcoin-selfish-mining-revenue-bounds`; Sapirshtein, Sompolinsky and Zohar, FC 2016, arXiv:1507.06183; Bar-Zur, Eyal and Tamar, arXiv:2007.05614.
- status to confirm first: that no certified upper bound below SSZ Table 2 has appeared (the bank names arXiv:2607.24415 as a different question).
- why us: an attacker's best response in a consensus protocol, where security and game theory are the same question.
- weight: 4
- wild: no

### Q4 aes-linear-layer-circuits
- question: Is there a smaller or shallower XOR circuit for AES MixColumns or InvMixColumns than the live NIST table (or an S-box circuit beating a wish-list cell)?
- shape: record
- where defined: bank `nist-aes-circuit-records`; NIST Circuit Complexity project, csrc.nist.gov/Projects/circuit-complexity, and github.com/usnistgov/Circuits data/slp/aes/README.md.
- status to confirm first: the live README minima (the repository changes often) and its wish list.
- why us: gate-level bit conventions and hardware-style circuits; the linear-layer cells draw fewer attackers than the S-box.
- weight: 3
- wild: no

### Q5 chaocipher-single-message
- question: Can a single Classic Chaocipher message be broken ciphertext-only, at a frozen length, across a frozen 100-message benchmark (or the Extended variant under known plaintext)?
- shape: decipherment benchmark judged by the bank's success criterion
- where defined: bank `chaocipher-single-message-and-extended-kpa`; Rubin, "Chaocipher: current state of research" table (chaocipher.com); Lasry, Rubin, Kopal and Wacker, Cryptologia 40(6), 2016.
- status to confirm first: that the current-state table (last updated January 2023) still lists the single-message ciphertext-only case as open.
- why us: classical cryptanalysis done with honest null baselines, a night-after-night patience problem.
- weight: 3
- wild: no

### Q6 guts-weenie-coalition
- question: Does the Weenie-rule threshold 3^(-1/(n-1)) keep alpha nonnegative against every coalition threshold vector for n = 4 (then 5), or is there an exact negative point?
- shape: counterexample or certified bound for one n (partial win p1 for n = 4)
- where defined: bank `guts-weenie-rule-strong-equilibrium`; Buck, Lee, Platnick, Wheeler and Zumbrun, "Continuous Guts Poker and Numerical Optimization of Generalized Recursive Games", 2022, arXiv:2208.02788, Appendix B.3.
- status to confirm first: no proof or refutation for n >= 4 after arXiv:2208.02788 v3 (also check arXiv:2412.19855).
- why us: bluffing and coalitions in a betting game, small enough to settle exactly.
- weight: 2
- wild: no

### Q7 condorcet-dimension-four
- question: Is there an election in which no three candidates form a Condorcet winning set (Condorcet dimension 4)?
- shape: existence (explicit profile, every 3-committee beaten by a listed candidate)
- where defined: bank `condorcet-dimension-four-profile`; Elkind, Lang and Saffidine (2015); Charikar, Lassota, Ramakrishnan, Vetta and Wang, arXiv:2411.03390; Song, Nguyen and Lin, arXiv:2506.22133; Epoch AI open problem "Condorcet winning sets".
- status to confirm first: the Epoch page still lists it open and the general upper bound is still 5.
- why us: majority-rule paradoxes are home ground; partial wins (refuting Conjecture 1 at k = 2 or 4) are checkable steps.
- weight: 2
- wild: yes

### Reserve-quarry policy
A small but truly first, checkable result on a well-known open mathematical question is welcome, even a simple one:
the next exact term of a sequence attached to a famous problem, a first explicit witness, a first certified small
case. Take a reserve quarry when the weighted quarries are dead or blocked, or when a reserve is clearly closer to a
first result. "First" is judged against the live source at claim time; a tie or a value already posted elsewhere is
not first.

### R1 erdos-773-next-term (reserve)
- question: What is the exact largest Sidon subset size among the first 72 squares, a(72) of OEIS A390813 (or the first index beyond the live sources)?
- shape: record (exact next term: a witness plus an exhaustive non-existence certificate, or a larger witness)
- where defined: bank `erdos-773-sidon-squares-next-term`; Erdős problem #773 (Alon and Erdős); OEIS A390813; Lefmann and Thiele (1995).
- status to confirm first: the live A390813 b-file and the forum or blog posts reporting a(69) to a(71).
- why us: an exact, exhaustive search with a certificate on a famous problem's small cases.
- weight: 2
- wild: no

### R2 erdos-1063-next-term (reserve)
- question: What is n_76, the least n >= 152 such that n - i divides C(n, 76) for all but exactly one i < 76 (Erdős-Selfridge)?
- shape: record (exact next term with a reproducible minimality sweep)
- where defined: bank `erdos-1063-binomial-divisibility-nk-next-terms`; Erdős and Selfridge (1983); Guy, Unsolved Problems in Number Theory, B31; OEIS A389360.
- status to confirm first: the forum thread and the OEIS b-file for terms beyond k = 75.
- why us: a patient, exact sweep whose minimality argument must be audited as carefully as the sweep itself.
- weight: 2
- wild: no

## Lenses

### adversary (skeptic: no)
Treat the conjecture as a system under audit and yourself as the attacker. Spend the first hour on a fast exact
evaluator (rational or interval arithmetic) and test it on the published positive and a known negative. Then fuzz:
mutate the best known object or instance, keep anything that moves the objective toward the bar, and log the margin.
Dead sign: thousands of mutations plateau at a margin that does not shrink, with no structural trend.

### reframe (skeptic: no)
Change the frame until the question looks easy. Restate it as a different object in another field's terms (a
tournament as a majority of linear orders, an auction equilibrium as linear inequalities on bids, an MDP bound as an
LP dual, a cipher as a constraint system) and ask what the new frame forbids or makes cheap. First moves: write the
translation, check it on a solved case, list the tools the new frame unlocks. Dead sign: the reframing yields no new
constraint, symmetry or solver that the original lacked.

### campaign (skeptic: no)
Run the attack as a staged campaign. Scout: solve tiny cases exhaustively and tabulate. Secure: fix symmetry classes
and invariants so no ground is searched twice. Commit: put the night's compute only where the invariants are silent,
with checkpoints and a stated covered space. Dead sign: the small-case table shows the property holding uniformly
with a growing margin, so the counterexample, if any, is far beyond reach.

### solver (skeptic: no)
Recast the question as SAT, SMT, ILP or an exact LP and let a solver argue, keeping the certificate (LRAT proof,
rational dual, exact witness). Encode symmetry breaking first, test the encoding on the known positive, then scale
one parameter at a time. Dead sign: solve time grows by an order of magnitude per step with no certificate in sight.

### oldest-source (skeptic: no)
Read the oldest source on the question and its footnotes, errata and open-question sections. Old papers hold
abandoned constructions and parameter choices that later work dropped. First moves: list every explicit object and
unproved remark in the original, rebuild one with code, and check whether it was ever pushed further. Dead sign:
every idea in the old sources has a later paper that ran it to exhaustion.

### skeptic (skeptic: yes)
Try to show the quarry is settled, trivial or ill-posed before anyone attacks it. Look for a recent result that
closes it, a bar that is mis-stated (a tie dressed as a record, a rounded number, a tie-breaking rule that changes
the answer), or a definition with a loophole that makes a "win" meaningless. Dead sign: the definition is exact,
the bar is current, and no shortcut appears; then hand the quarry to the other lenses.

## Heuristics
1. Build the exact checker before the search; a fast evaluator is the whole edge.
2. Start from the best known object and perturb it; record why each perturbation helped or hurt.
3. Exploit the definition's edge: ties, degenerate parameters, boundary values, smallest legal sizes.
4. One small certified step beats a big uncertified one; partial wins are real results.
5. Impose symmetry to shrink the search, then break it on purpose when it stalls.
6. When two frames disagree about difficulty, trust the one that gives a certificate.
7. Every search keeps a covered-space record precise enough to never repeat it.
8. Prefer quarries with few recent attackers over famous ones.

## Kill criteria
1. A published or posted result already meets the bar (or a strictly better value exists).
2. The bar cannot be reached even under the most favourable relaxation the lens can compute.
3. A week of nights moves the best margin by less than 1% of the remaining gap with no new structure.
4. The definition turns out ambiguous in a way the success criterion does not resolve.
5. The only path forward needs compute far beyond one machine (cluster scale).
6. The reframing or encoding cannot be validated on a known case.
