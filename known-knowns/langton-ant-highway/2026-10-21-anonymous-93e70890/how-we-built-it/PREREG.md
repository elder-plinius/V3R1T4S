# PREREG — run 2026-10-20-2306, langton-ant-highway (frozen 2026-10-20 23:11 UTC, before any experiment of this run)

Criterion (verbatim, bank partial win p1): Exhaustive verification of all initial configurations in a 6x6 (or larger) box under a stated symmetry reduction, each with a highway-capture certificate (window at t equals window at t+104 shifted by (+-2,+-2), ant beyond all black cells, and no initial black cell anywhere in the future sweep of the highway) re-checked by an independent simulator on a random 1% sample plus all hard cases.

This run supplies only the "re-checked by an independent simulator on a random 1% sample plus all hard cases" part, for the user's existing exhaustive 6x6 run (data-user/langton6x6-out6/).

## Checker (frozen)
- New program indep/code/lantx.c, written from the spec in BRIEF.md without opening lant.c, lant2, lant4 or ref sources.
- Simulation: exact, byte grid, convention of BRIEF.md (6x6: bit b -> (b%6-2, b//6-2); 4x4/5x5: o=(k-1)//2, bit b -> (b%k-o, b//k-o)).
- Certificate X (sufficient, rigorous): let s0 be the start of a stretch over which h(u)=h(u-104) for every step u (h = heading after u steps), with 104-step displacement v in {(+-2,+-2)}. Let B0 = bbox of the initial box and of every cell visited before s0 (so all black cells at s0 lie in B0), V0 = cells visited in period 0 of the stretch, M = floor(min(span_x(V0), span_y(V0))/2). Choose the least K >= M such that bbox(V0)+K*v is strictly beyond B0 in a coordinate in which v moves away. If the stretch is verified by simulation through period K, then every period p >= K sees the same environment (no black cell of time s0 in V0+p*v, and the XOR of earlier periods' parity patterns on V0+p*v is constant for p >= M), so the motion is 104-periodic forever. T_cap(X) = the first s with h(u)=h(u-104) for all u >= s+104 (the intrinsic start of periodic motion), output with vx vy and dir = h(T_cap).
- Expected relation to lant's T_cap: lant's C(s) is claimed exact, and the first s with C(s) should equal the intrinsic start of periodicity; then T_cap, vx, vy, dir must be identical. The validation decides whether the certificates are equivalent in effect; if validation shows a systematic, explained offset, agreement is judged on "captured" plus the explained relation, and the report says so.
- Cap: a mask counts as captured iff T_cap(X) <= 2,000,000 and the certificate completes within 4,000,000 simulated steps; grid window 8192x8192 (edge -> OOB, never counted as captured).

## Validation (must pass before 6x6 work counts)
- V1: all 65536 4x4 masks vs enum4_lant2.txt; V2: all 2^25 5x5 masks vs enum5/chunk_*.gz (lant.c). Pass = every line equal in (mask, tcap, vx, vy, dir) (or the explained relation above) and every mask captured.
- Negative tests: N1 cap smaller than a known tcap -> not captured; N2 a planted black cell in the future sweep of the empty-grid highway -> no certificate before the ant has passed it (T_cap with the plant must differ from or exceed the unplanted run's plant-encounter time).

## Hard cases (frozen)
- H: the 4096 per-chunk maxtcap_mask values from data-user/langton6x6-out6/chunk_*.sum. Pass = every one captured by lantx with T_cap equal to the summary's maxtcap (if V1/V2 show equivalence).
- Also: a contiguous 6x6 subset rerun with box lant4 (/workspace/langton6x6-package/lant4) and lantx, per-mask lines compared on (mask, tcap, vx, vy, dir): masks [0, 2^20) and [40920836116-2^19, 40920836116+2^19) (around the global max), plus [2^35, 2^35+2^20).

## Random sample (frozen)
- Seed SEED = 0x5EED20261020. For each mask m in [0, 2^36): z = splitmix64(m + SEED) (standard splitmix64: z+=0x9E3779B97F4A7C15; z=(z^(z>>30))*0xBF58476D1CE4E5B9; z=(z^(z>>27))*0x94D049BB133111EB; z^=z>>31), r = z mod 10000. m is in the sample iff r < 100 (1%, expected 687,194,767 masks). Pass index q = r div 25 in {0,1,2,3}; each pass alone is a uniform 0.25% Bernoulli sample.
- Order: pass 0 over all 4096 chunks, then pass 1, 2, 3. Each (pass, chunk) unit is checkpointed. If the deadline (02:40 ET 2026-10-21, 06:40 UTC) arrives first, the checked sample is the completed passes plus completed chunks of the partial pass; the report states the exact count and that it is below 1% and why. A partial pass's completed chunks are reported separately (not uniform over the whole space).
- Pass = every sampled mask captured (CAP) by lantx. lant4 per-mask lines are not available for the sample (not kept), so for the sample the comparison is: captured by both (the user's summaries show every mask CAP) and per-chunk max T_cap(sample) <= that chunk's summary maxtcap (with equality impossible to require).

## What counts as failure
- Any mask (validation, hard case, sample) not captured by lantx, OOB, or a per-mask mismatch with lant output where equivalence was established, or a sampled mask with T_cap above its chunk's maxtcap. Each such mask is rerun with /workspace/langton6x6-package/ref/lant_ref enumr 6 6 M M+1 with cap 20,000,000 and reported exactly. No claim beyond what was checked.

null_test: not needed because this is a deterministic re-check of explicit masks by an exact simulator against stored per-mask and per-chunk values, not a search or "beats chance" statistic.

Resources: nice -n 19, at most 5 worker processes, < 8 GB RAM, each shell command < 8 min, long job as a resumable background job with a STOP file and checkpoints; done or stopped by 02:50 ET.
