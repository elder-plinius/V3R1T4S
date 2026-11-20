context: subagent (fresh isolated OpenClaw subagent, given only claim/)

# REPRODUCE skeptic panel (Voynich B-panel: outcome (B) — Naibbe H1 falsification)

## Definition I re-derived from (quoted from the task policy)
H1 = observed # adjacent token pairs within Levenshtein edit distance 1,
divided by the expected count under the within-line shuffle null computed by the
exact unbiased expectation per line = m/n where m = #{(i,j): i!=j, lev1(line[i],line[j])}
(ordered pairs) and n = line length; H1 = sum over lines of obs_line / sum over
lines of (m_line/n_line). Tokens are first passed through the SUBS glyph->letter
collapse table (IVTFF): cth->T, ckh->K, cph->P, cfh->F, ch->C, sh->S, iin->N, in->I, ee->E.
Pooled files' line breaks are the template-wrap boundaries.

I wrote my own independent checker (panel/repro_skeptic_check.py, stdlib only,
lru_cache lev1). My lev1 (two-pointer) was cross-validated against a naive DP
Levenshtein on 200,000 random string pairs: 0 mismatches. Proof step re-derived:
for a uniform random permutation of the line's n tokens, a fixed adjacent slot is
occupied by a given ordered token-index pair (i,j) with prob 1/(n*(n-1)); with
(n-1) slots, E[adjacent lev1 count] = (n-1)*m/(n*(n-1)) = m/n — matching the
documented exact-unbiased null. SUBS applied after lowercasing, in listed order.

## Exact numbers I re-derived (from my command output, not memory)
- pooled A: sum(obs_line)=45007, sum(m_line/n_line)=56391.163336,
  RE-DERIVED pooled A H1 = 0.7981215023387158 (my checker printed 0.798122)
- pooled B: sum(obs_line)=44644, sum(m_line/n_line)=56392.297368,
  RE-DERIVED pooled B H1 = 0.791668403014533 (my checker printed 0.791668)
- Both runs (initial + determinism re-run) returned bit-identical H1 values →
  no non-determinism in the re-derivation. lev1 cache ~6.5M/~10.3M entries,
  each file ~12s (well under the 1000s naive bound).

## Agreement with stored values
- objects/naibbe_batch.json pooled A stats.H1 = 0.7981215023387158 (diff 0.0, within 0.005)
- objects/naibbe_batch.json pooled B stats.H1 = 0.791668403014533 (diff 0.0, within 0.005)
- README claims 0.7981 / 0.7917 → consistent (rounded).

## Envelope / null properties (from saved files only)
- env_H1_A_ZL3b.json envelope_999[0]=1.0689697211194191 ; pooled A 0.798122 < it → OUTSIDE
- env_H1_A_IT2a.json envelope_999[0]=1.027068780639737 ; pooled A 0.798122 < it → OUTSIDE
- env_H1_B_ZL3b.json envelope_999[0]=0.905272706055239 ; pooled B 0.791668 < it → OUTSIDE
- env_H1_B_IT2a.json envelope_999[0]=0.9011753804716054 ; pooled B 0.791668 < it → OUTSIDE
- null_H1_bootstraps.json per-cell 'min' (16,000 controls):
  A_ZL3b=1.065032987747408, A_IT2a=1.0254637631063488,
  B_ZL3b=0.9037196956660043, B_IT2a=0.8989687544145788.
  pooled A 0.798122 < both A minima → True; pooled B 0.791668 < both B minima → True.
- Per-plaintext secondary (per_ptext_H1 in objects/naibbe_batch.json): 20/20 means
  below the 99.9% lower bound on BOTH transliterations (ZL3b and IT2a) for their
  dialect; failures: none.
- Cross-consistency: env envelope_999 lower bounds agree with null p005
  (e.g. A_ZL3b env 1.0689697 vs null p005 1.0689706), and null min < p005 < p999 as expected.

## Object non-triviality / self-consistency
- objects/pooled_A.wrapped.txt: 404168 lines, 3,049,184 tokens (~3.05M, matches "3.05M")
- objects/pooled_B.wrapped.txt: 404938 lines, 3,057,184 tokens (~3.05M, matches "3.05M")
- objects/naibbe_batch.json: 'seeds' has 10 entries (2026111601..2026111610, equal to
  distinct run seeds); 'runs' has 200 entries, every run has a 16-hex 'sha' field,
  200 distinct shas; 20 distinct ptexts, 100 runs/mode; per-plaintext means exactly
  match the per-run H1 means (0 mismatches); pooled n_tokens == sum of per-run n_tokens.
- objects/naibbe_tables.json: non-trivial Naibbe homophone tables — 3 states
  (unigram/prefix/suffix) x 6 tables x 23 letters = 414 cells, 356 distinct glyph
  strings; carries _source/_citation (greshko/naibbe-cipher, Cryptologia 2025).

## Author checker
`python3 checker.py` (from claim/) ended in PASS, as expected. My pass/fail decision
is from my own re-derivation above, which independently reproduces every stored value.

## Mismatches found
- MINOR (non-blocking): token count. objects/naibbe_batch.json pooled A n_tokens =
  3,049,192 (== sum of per-run n_tokens) but objects/pooled_A.wrapped.txt contains
  3,049,184 tokens (diff 8). Pooled B: stored 3,057,200 vs 3,057,184 in the file
  (diff 16). This is 0.00026% (A) / 0.00052% (B) and does not affect the H1
  statistics: the stored pooled H1 (0.7981215023387158 / 0.791668403014533) is
  exactly the value re-derived from the saved pooled files, so the falsification
  statistic is consistent with its own source object. Likely a tiny artifact of the
  template-wrap/dump step (e.g. a few tokens dropped or re-joined at wrap
  boundaries). Recorded as a minor internal inconsistency; not a blocker for the
  claimed falsification property (H1 outside 99.9% envelope and below all controls).
- No other mismatches: no missing objects, no non-determinism (bit-identical
  re-run), all envelope/null/per-ptext/structure checks pass.

## Verdict
Every falsification property in the claim package is confirmed from the saved
files by my independent re-derivation: pooled H1 A=0.7981 and B=0.7917 are below
the 99.9% Voynich envelope lower bound on both dialects and both transliterations
and below the minimum of all 16,000 bootstrap controls; all 20 per-plaintext
means are outside on both transliterations. One minor token-count inconsistency
(8/16 tokens) is noted but does not change the H1 values.

pass: true
