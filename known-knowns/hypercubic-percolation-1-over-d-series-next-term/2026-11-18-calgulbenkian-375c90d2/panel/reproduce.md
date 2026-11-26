context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report, package 375c90d2 (claim p2: closed formula for [binom(d, e-3)] D_e(q))

## Fetch log
- 2026-11-18T17:31:12Z, https://arxiv.org/e-print/1805.02701 (no redirect following), HTTP 301, sha256 5943c7031ac3dcae470119ebdb03712fe4a355c5c9936bdc4bee5a887c2cbb9d (redirect stub, discarded)
- 2026-11-18T17:31:14Z, https://arxiv.org/e-print/1805.02701 (followed to https://arxiv.org/src/1805.02701), HTTP 200, sha256 c2277e76b34fa4cab645e15c949eadae6adfb8aabbd3b68c017eb07c4492a2cf (equals the TeX-source hash the package quotes)

## Conventions fixed from Mertens-Moore (bond-animals.tex, Sec. "From Lattice Animals to Perimeter Polynomials")
- Bond animal = connected set of lattice edges, counted up to translation only (fixed). Size e = number of edges.
- Proper in k dims = edges span a k-dim subspace; G^{(k)}_{e,t,v} = number with e edges, v vertices, perimeter t, where t = edges incident to the animal but not in it, counted inside the k-dim subspace (chords between animal vertices included).
- D_e(q) = sum_k sum_{t,v} binom(d,k) G^{(k)}_{e,t,v} q^{t+2(d-k)v}, so D_e(1) = A_d(e). q is the probability that an edge is absent (they use q = 1-p). "Coefficient of binom(d,e-3)" = the k = e-3 term, with the q^{2(d-k)v} factor kept inside.
- Their anchors: G^{(2)}_{4,12,5}=53, G^{(2)}_{4,11,5}=32, G^{(2)}_{4,8,4}=1; my enumerator reproduces all three, and G^{(2)}_4 = 86.

## My own checker (written before reading any package code)
- a working file (not shipped): Redelmeier-style enumeration of fixed bond animals in Z^k, pruned to those using all k axes, histogram by (v, chords s, t), t computed directly as incident-minus-animal edges. a working file (not shipped) transcribes the six gamma formulas from how-we-built-it/PROOF.md and compares term by term. It also asserts t = 2kv - 2e - s on every animal.
- Results for k = e-3, exact integer equality, all six families (gamma_0..gamma_3 from v=e+1, s=0..3; gamma_2d from v=e, s=0; gamma_{2d+1} from v=e, s=1), and no other (v,s) class occurs:
  - e=4 (Z^1), e=5 (Z^2), e=6 (Z^3), e=7 (Z^4), e=8 (Z^5): ALL OK. For e=8: 104454120, 77177280, 22232640, 2609280, 688640, 192000. The enumeration covers d = 1..5 as its own cases; d enters only through the q exponent, which the identity above fixes.
  - e=9 (Z^6) was not run: I estimate several hours single-threaded (e=7 took 1.3 s, e=8 minutes). Not done, not claimed.
- Independent data from the paper's own enumeration (Appendix A of the TeX source, typed in by me from the source text): D_9, D_10, D_11 binom(d,e-3) coefficient lists: all 6 x 3 = 18 values equal the formula. Sum at q=1 for e=12 gives 6199599459637248, equal to the paper's [binom(d,9)] D_12(1). Total 8 values of e (4..11) compared term by term plus e=12 at q=1. These are a spot check on the formula, not a proof, since the polynomial degrees (up to 9) exceed the number of data points; correctness for general e rests on the proof below.

## Package checks
- Ran verify-it-yourself/run_checks.sh in a copy of this package inside my work folder: 45 s, all four OK lines and final PASS. It checks only e <= 6 by brute force plus Appendix A. My own checker goes further (e=7, 8).
- Determinism: repeated my runs and theirs, same results.

## Proof re-derivation (how-we-built-it/PROOF.md, and the logic of prove_bond_perimeter_e_minus_3.py)
1. Perimeter-chord identity t = 2kv - 2e - s, hence exponent = 2dv - 2e - s: VALID (also asserted on every enumerated animal).
2. Excess bookkeeping e_R = r+3, 1 <= r <= 3, cycles lie in repeated axes, K_{2,3}-free, cyclomatic >= 2 needs >= 7 edges > 6, so v in {e, e+1}: VALID. The disconnected case (two disjoint cycles need 8 edges) is not spelled out in the text, only implied; minor, not a gap in truth. For small e (e=4, 5) the range r <= k restricts the sum; the formula still matched brute force there, but the text claims "all e >= 3" without addressing r > k explicitly: GAP (minor, empirically closed for e=4,5 by my enumeration; e=3 is trivial as the factor (e-3) gives 0).
3. Singleton-bridge separation: chord along a singleton axis needs a simple path P1 + e_a + P2 with Delta(P1)+Delta(P2)=0 and both nonempty, so the bridge joins two different E_R components with extra chords |(V_i-u_i) ∩ (V_j-u_j)| - 1; chords along repeated axes stay inside one component; chords involving external (single-vertex) components are 0: VALID. I checked each sub-claim, including that simple paths use each singleton edge at most once.
4. Core-forest summation: orientation factor 2^{e-e_R}, binomial/falling-factorial choice of R axes (k!/(r!(k-r)!)) times (c0+N-1)! label orderings over N! and prod m_X! symmetry divisors, expansion of the pairwise bridge weights into |V_i||V_j| + W~, and the weighted Prufer identity sum_{T ⊇ F} prod_{T\F} w = (prod S) v^{c'+N-2}: VALID by my reading. I traced each factor to the code (fall_em, p_pref product (N+j), 1<<e_R, the Counter-based W~, forest enumeration). The full symbolic sum over 16,314 cores is machine-executed exact rational arithmetic, which I re-ran, not hand-verified per core. The same code at m=1, 2 reproduces Mertens-Moore Theorems 5-6, a good consistency check. The "PROVED-HERE" label is a computer-assisted derivation; no independent second implementation of step 4 exists in the package (brute force only reaches e=6 there; mine reaches e=8, and the paper's appendix e=11, 12).
Verdict: steps 1, 3, 4 VALID; step 2 VALID with one minor unstated case; no WRONG step found.

## Table 9 ("removes") claim
Their table (tab:estimated_times in the TeX source, called Table 9 by the package) lists, for the classical route, (d,14) with d = 5..11, and for the Pade route (d,12) with d = 7, 8, 9; data for d >= e-2 are said to come from Theorems 4-6. The new formula covers k = e-3, i.e. (9,12) (4.5 years) and (11,14) (133,800 years): the claim is literally correct. It does NOT remove (10,14) (28,526 years), (9,14), (8,14), (7,14), (6,14), (8,12) (387 days), or (7,12) (57 days). Therefore it shrinks but does not make feasible the classical sigma^-7 route, and the Pade route still needs (8,12) at 387 days. The package states this itself under "Not Claimed".

## Result
My independent brute-force counts match the closed formula exactly for e = 4..8 (all six families), and the formula also matches the paper's published enumerations for e = 9, 10, 11 and the e = 12 q=1 sum. The package's own check passes. The proof is a computer-assisted constructive derivation that I find correct; the Table 9 removal claim is accurate. Caveats: e=9 brute force not run (hours); the all-e extension rests on the derivation, which has no second implementation.

pass: true
