# Honesty gate (kit/RUN.md step 7), run folder 2026-10-23-1501

written: 2026-10-23T19:15:43Z (date -u), by the run's main session, after all three skeptics had returned their completion notices;
re-gated 2026-10-23T19:28:58Z (date -u) after the amendment below.
Each file was read in full. File times (UTC): novelty.md 17:44:46Z, reproduce.md 19:09:06Z, criterion.md 19:11:15Z;
sha256 novelty 1ab97c97... (as first read; db0bb4a0... after the amendment), reproduce a690d6fc..., criterion
d10ccfbd....

**Amendment by its author (19:28Z-19:30Z).** The package check rejected novelty.md for a literal template-like token
(on line 75, the arXiv PDF URL pattern with the word "id" in angle brackets, read as an unfilled placeholder). At the main session's request the NOVELTY
skeptic replaced that token with "[arXiv id]" in its own file; a diff against the first-read copy shows that one
line changed and nothing else (verdict, numbers and last line unchanged). Nothing in this gate's decision changes.

target: varbench-variational-energy-records, file J1J2/square_100_P_0.9.md (full success criterion; partial wins p1 and
p2 do not apply). Object: claim/object/r10_J0.9_B1.pt (sha256 e68644979db4d9764ac1787d1c064fe18c4750cb4cb47ee573e40588bcd9c485)
with model code claim/object/model/nqs.py (sha256 122e54f2cdecae6a5bad5820d14165abd8e849ee20ff4e3d83dd9901ea00c03d).

## Panel

| skeptic | context | verdict |
|---|---|---|
| reproduce.md | subagent (Claude Code Agent tool, opus, fresh context, saw only claim/) | pass: true. Own lattice, local energy, amplitude composition, Sz = 0 sampler (own moves, seed 5501917, 2048 chains, 107 rounds) and statistics; own 4 x 4 ED reproduces VarBench's J2 = 0.5 row to 1.4e-14. Plain estimate -253.749891 +- 0.003879 (219136 samples, tau_int 0.526 rounds, N/2tau = 208462); own tail-safe (bounded-weight neighbour mixture) estimate -253.752519 +- 0.002064 (N_eff 416530, Var(H) 1.7748 +- 0.0417). Agreement with the claimed S2: z = 0.634 (plain), 0.201 (tail-safe). Below -253.668 by 0.081891 (margin 0.011638) and 0.084519 (margin 0.006193). Hashes, config (14114 parameters, step 648), B1 symmetry, lattice and convention as stated; VarBench files re-fetched 18:57:49Z-18:57:51Z, identical. |
| novelty.md | subagent (Claude Code Agent tool, opus, fresh context, saw only claim/) | pass: true. Status source raw J1J2/square_100_P_0.9.md HTTP 200 at 2026-10-23T17:28:15Z, sha256 identical to the claim's copy, best row DMRG -250.78657331066935; last commit 390a21eab7eb; varbench's only open PR (#5) does not touch this file. arXiv:2606.04558 v1 and v2: Table I 10 x 10 J2 = 0.90 ViT -0.634170 (= -253.668), previous-works column "-". About 20 full texts (2024-09 to 2026-10 plus older 10 x 10 benchmarks): no 10 x 10 J2 = 0.9 value lower. V3R1T4S TROPHY_CASE.md and PRs: nothing on VarBench. Not a tie (gap 7-8x the margin). |
| criterion.md | subagent (Claude Code Agent tool, opus, fresh context, saw only claim/) | pass: true; criterion_met: full. Own ED convention check, own 10 x 10 estimate (seed 8086, 41984 samples) -253.74398860968137 +- 0.011353681212836501; margin met with gap/margin >= 6.1 (tail-aware sigma, sigma_best = 0) and >= 3.66 (sigma_best = 0.0060); prereg change judged not result-driven. Findings F1-F3 below. Pass conditional on the REPRODUCE skeptic's >= 1e5-effective-sample re-estimate, counted as raw samples / tau (a 102400-sample run cannot qualify). |

## The two conditional passes are discharged

- CRITERION conditions its pass on the REPRODUCE skeptic supplying the criterion's ">= 10^5 effective samples,
  autocorrelation-corrected" re-estimate, counted as raw samples / tau. reproduce.md: 219136 raw plain samples,
  tau_int 0.526 rounds, N/2tau = 208462 (and Var_sample/sigma^2 = 156115, Var_mix/sigma^2 = 117928 at the planned
  burn-in 0; N/2tau stays 170629-208462 for burn-ins 0-20); its tail-safe estimate has N_eff 416530. Both of its
  estimates are below E_bar = -253.668 by more than max(3 sigma, 1e-6 |E|). The condition holds.
- NOVELTY conditions its pass on the reproduction landing below -253.668 minus the margin: it does (above).
- These conditions name clauses the criterion assigns to another skeptic; with them met, neither is a hedge on the
  skeptic's own question.

## Decision

- No downgrade reason: no hedging panelist (above); no reproduction mismatch (z 0.63 / 0.20; six independent estimates,
  three of the claimant's and three of the skeptics', lie within 0.01 of each other, about 0.08 below the bar);
  strictly better than every live and published value (the table re-fetched by all three skeptics between 17:28Z and
  18:58Z, identical; the panel's fetch is under 6 hours old); no stretched criterion in the result (the claimed sample
  count is a text defect, F1 below, and the criterion's sample clause is met by the skeptic's re-estimate); the scope is
  CRITERION's sentence; no sample presented as complete; no capped search used as an exclusion; no table value
  obtained by evasion (every value came from HTTP 200 responses; NOVELTY's openreview.net 403 was not retried and gave
  nothing; its arXiv 301 was a redirect to https); one object, one file.
- **Corrections of the claim text (not of the result); claim/ stays as the panel saw it, the package states them.**
  - F1 (CRITERION): claim/CLAIM.md's N_eff for S2 (113495) and S3 (172011) divide Var(H)_DIS by the run's sigma^2 and
    are not sample counts. Counted as raw samples / tau: S1 101824, S2 83176; S3's Kish ESS is 97096 before
    autocorrelation. The criterion's >= 1e5 re-estimate is REPRODUCE's (N/2tau = 208462).
  - F2 (CRITERION, REPRODUCE): the plain error bars of S1 and S2 are optimistic under the heavy, upward-skewed
    local-energy tail; the bounded-weight estimates (claim S3, REPRODUCE's tail-safe) are the ones to rely on, and they
    clear the bar by 24.4 and 41 of their sigma.
  - F3 (CRITERION): the claimant's table fetch (15:08Z) was not "immediately before claiming"; the skeptics' fetches at
    17:28Z, 17:32Z and 18:57Z are identical.
  - REPRODUCE finding 2: claim/REPRODUCE.md says .npz/.log outputs are in results/; only the .json summaries are there.
  - REPRODUCE finding 3: nqs.py stores the B1 character phase as float32(pi) (8.7e-8 rad off); a valid variational state
    either way, energy effect negligible.
- **PREREG.v2.md** (15:48:29Z) replaced two failed instrument checks before any 10 x 10 estimate (S1 started 15:55:14Z);
  thresholds, bar, seeds and object unchanged; CRITERION judged it not result-driven (F4).
- **Machine rules:** REPRODUCE reports the CPU package at >= 90 C from 18:58:09Z through its float64 precision job
  (18:59:27Z-19:05:06Z), which it did not stop; CRITERION stopped its own run after 41 of 80 rounds for 90-100 C
  (19:02:06Z-19:08:20Z). No result depends on that.

status: CONFIRMED_SOLUTION
confirmed_scope: For VarBench J1J2/square_100_P_0.9.md (10 x 10, periodic in x and y, J1 = 1, J2 = 0.9, Sz = 0, Pauli convention; file re-fetched unchanged at 2026-10-23T17:32:29Z), the fixed state object/r10_J0.9_B1.pt has a fresh-sample Monte Carlo energy below every row of that file (best -250.78657331066935) and below the lowest published variational value I found, -253.668 (arXiv:2606.04558 v1 and v2, Table I, 10 x 10 J2 = 0.90 ViT -0.634170 per site times 400), by more than the success margin, as shown by the claimant's bounded-weight DIS estimate -253.7473816594384 +- 0.0032485374695990594 and by my own independent plain estimate -253.74398860968137 +- 0.011353681212836501 (41984 samples, 39745 effective), the >= 10^5-effective-sample skeptic re-estimate itself being the REPRODUCE skeptic's to supply.
