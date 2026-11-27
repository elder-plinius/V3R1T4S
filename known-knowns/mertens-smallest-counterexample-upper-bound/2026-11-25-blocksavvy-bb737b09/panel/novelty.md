# NOVELTY skeptic: p4 (independent K_2 sum at the bzyzz point over all zeros below 1.3e6)

context: fresh-context knowledgeWork skeptic, sandbox panel-0045-novelty

Inputs read: claim/ (CLAIM.md, status_source.md, inputs/, result/, code/k2_chunks.py) and RULES.md of the sandbox only.
No private/ files, no credentials, no outward actions (only read-only GET requests).
Searches ran 2026-11-25 between 04:39Z and 04:43Z (from `date -u`).

## 1. Status source (fetched once, plain curl, UA "V3R1T4S-panel/1.0 (novelty skeptic)", no retries)

- URL: https://en.wikipedia.org/wiki/Mertens_conjecture
- Time: 2026-11-25T04:39:06Z (`date -u` just before and just after the request)
- HTTP 200, 175,526 bytes, sha256 d3a6e043fb17c35c1d7d092c64163df06e847198d55b570de5bb1168faeb05ef
  (this differs from the claim's 00:47Z sha256 63a12542...; the article text is unchanged, so the difference is likely
  dynamic page markup. Revision id 1343658435, "This page was last edited on 15 March 2026".)
- Value (quote): "In 2024, Seungki Kim and Phong Nguyen lowered the bound to e^(1.96×10^19) ≈ 10^(8.512×10^18), but no
  explicit counterexample is known." No mention of the 3.485e18 claims (bzyzz, Gallego). This matches claim/status_source.md.
  Label: KNOWN.

## 2. Searches (window: 2024-11 .. 2026-11-25)

1. **arXiv** (export API, sorted by submission date): `all:"Mertens conjecture"` (17 hits), `abs:Mertens AND abs:counterexample` (4),
   `abs:Mertens AND abs:Pintz` (2), `all:bzyzz` (0), `abs:Mertens AND abs:zeros AND abs:lattice` (1), `au:Pintz` (10),
   id 2608.24878. In the window: only arXiv:2502.21021 (Kim-Nguyen, 2025-02-28), 2608.24878 (Pintz, "Oscillation of partial
   sums of the Möbius function...", about the average order of |M(x)|, not about the bzyzz point) and an unrelated 2610.07741.
   **No arXiv paper checks the bzyzz K_2 sum.**
2. **HAL hal-05838582** (API + PDF Mertens.pdf, HTTP 200): Bi and Hou, v1, submitted 2026-10-26, modified 2026-10-27. It is
   the authors' own computation. §(d) "Tail. For 6·10^5 < n ≤ N(T0) we worked at 20 digits ... The resulting tail enclosure
   is [±9.43·10^-12]". This matches the claim's description (certificate bounds the tail, does not evaluate it). The only
   "independent" wording in the paper refers to Table 1 vs Saouter-te Riele ("rather than an independent confirmation") and to
   Lean. HAL search `title_t:Mertens`, submitted since 2024-11: 4 hits (hal-05016898 Kim-Nguyen; hal-05838582; hal-05675375
   Yarman et al. "Revisiting the Mertens Conjecture Disproof of 1985"; an unrelated halshs). **None is an independent K_2 check.**
3. **Zenodo 10.5281/zenodo.23700211** (record 23700212, the only version, v1.0, 2026-10-27; English PDF read): Gallego's
   own proof. It uses k = 5.7e-12, y = 3484971332733132396.538348536063730810969705971170 (differs from the bzyzz v by
   1.4387e-5), 16,622,627 zeros up to T0 = 7,999,035.172, S(y) = 1.002069993625 ± 4.96e-7, B < exp(3484971332733141310.42338180385).
   Its "Control" sections recompute Kim-Nguyen's point, not the bzyzz one; the PDF never mentions bzyzz, Bi or Hou.
   **This is a different kernel, point and cutoff, so it is not a K_2 recomputation at (v, k = 1.5e-10, T0 = 1.3e6).**
   Zenodo search `title:Mertens` (newest, 2 pages): nothing else relevant (Tomov "first sign change in Mertens' first
   theorem", Rusiashvili, Pavesi, and biology records). `"mertens_bound" OR bzyzz OR "3484971332733"`: 0 hits.
4. **GitHub bzyzz/mertens_bound** (API): head a0b267c2 (2026-10-22T14:26:15Z), 0 forks, 0 releases (so no release assets),
   issues and PRs #1-#3, all by bzyzz, all closed on 2026-10-18 (Lean verification; "Review fixes", which addresses "the
   internal review of 2026-10-18", i.e. the authors' own review; Lean merge), 0 comments. Tree at a0b267c2: certification/,
   lean/, legacy/, kim_nguyen_ref/, search/; no third-party verification file. **No independent check.**
   GitHub repository search `mertens_bound` (9 hits: bzyzz, wbeni95/mertens-function-bounds (lim sup/inf, not this),
   luchesart and leecrossley repos about other Mertens problems), `bzyzz` (2, no other relevant), `mertens counterexample`
   (only bzyzz). **None is an independent check.**
5. **V3R1T4S TROPHY_CASE.md** (main, HTTP 200, 100 lines): no line matches mertens/bzyzz/K2. **Nothing.**
6. **V3R1T4S known-knowns/** (main head 989ddf5f, 2026-11-23T18:25:27Z; full tree, 8,798 paths, not truncated): no path
   contains "mertens" or "bzyzz" under known-knowns/. The only mertens files are the three known-unknowns/number-hunts/
   target pages. **Nothing.**
7. **V3R1T4S pull requests**, all 1,189 (574 open + 615 closed), titles and bodies grepped for mertens / bzyzz / 3484971 /
   mertens-smallest / Pintz / Saouter / Kim-Nguyen / zeta zeros / 1.3e6: on this target only **#1234** (open, 2026-11-24T15:02:30Z).
   #1218 is a different target (A084235 Mertens values). Every other hit is an unrelated "counterexample" title.
8. **Web search** (3 queries: bzyzz independent verification K2; exp(3484971332733178124) Bi Hou check; 3.485e18 Gallego
   verification): only the HAL and Zenodo deposits themselves, Kim-Nguyen (ANTS slides/paper, Zenodo 10775723/11550925),
   and Weisz Zenodo 10.5281/zenodo.23651459 (lim sup/inf M(x)/sqrt(x), unrelated). **No independent K_2 check.**

### PR #1234 overlap (same author's earlier p1)
#1234 re-evaluates Kim-Nguyen's 19 printed rows: h_P (k = 1.5e-6, γ < 14,000) and h_StR (k = 3e-9, γ < 74,000) at
Kim-Nguyen's y values. Its CLAIM.md never evaluates K_2 at the bzyzz v with k = 1.5e-10 and T0 = 1.3e6. It cites Bi-Hou
only for their re-evaluation of the Kim-Nguyen record cell. So the two share a method (python-flint zeros), not an object,
and they are different partial wins (p1 vs p4). **No overlap that affects novelty.** The claim's own "Not claimed" section
correctly keeps Kim-Nguyen's tables out of scope.

**Novelty result:** I found no public, independent, full ball-arithmetic recomputation of the bzyzz K_2 sum over all
2,325,572 zeros below 1.3e6 (in particular none evaluates the tail 600,000 < n ≤ N(T0), which the certificate only bounds).
Label: KNOWN (search result; absence cannot be proved, but every requested source was checked).

## 3. Credits check

- Zhenyu Bi and Enze Hou: correct. The HAL authors are Bi and Hou; the HAL paper's data statement points to github.com/bzyzz/mertens_bound.
- Leandro Hector Gallego, 10.5281/zenodo.23700211: correctly attributed, and the concept DOI resolves to the only version.
  **Wording nit (non-blocking):** "independent claim of the same exponent" is accurate only to 3.485e18. Gallego's exact
  bound exp(3484971332733141310.42...) is 36,813.58 below bzyzz's exp(3484971332733178124) in the exponent, and it uses a
  different k, point and T0. Suggested wording: "independent claim, also about exp(3.485e18), at a different (k, y, T0)".
- Kim and Nguyen, arXiv:2502.21021, exp(1.96e19) peer-reviewed record: correct (Wikipedia and ANTS XVI confirm it).
- Pintz (1987), Saouter and te Riele (2014): correct attributions for the criterion (Astérisque 147-148; Math. Comp. 83).
  No links are given (RULES 13 asks for links). Suggested links: Numdam AST_1987__147-148__325_0, and the Math. Comp. DOI.
- FLINT/Arb (Fredrik Johansson et al.) and python-flint: correct, and the code uses `flint.acb.zeta_zeros` and `acb_series(...).zeta()`.
- Nothing is missing that the claim builds on (Odlyzko and Platt zeros are not used).
- **Independence caveat (non-blocking, should be stated):** the code is separately written (meeting p4's "separately written
  code"), but the zeros come from the same FLINT routine (`acb.zeta_zeros`) that the bzyzz certificate used (python-flint
  0.9.0 / FLINT 3.6.0 per its versions field). So this is an independent computation, not an independent zero source or
  method. PR #1234 states the same caveat; this claim should too.

## 4. Side notes for the human (not part of this verdict)
- Gallego's bound (2026-10-27) is smaller than bzyzz's exp(3484971332733178124), which the bank calls "the smallest public
  claim on 2026-10-30". The bank target text may need updating. This does not affect p4.
- chunks_tail/ is labelled n = 600,001..2,325,573, one past N(T0) = 2,325,572. aggregate_claim.json reports
  gamma_2325573 > T0 and boundary_ok = true. Whether n = 2,325,573 is excluded from the sum is for the REPRODUCE skeptic to confirm.

## Verdict
No equivalent independent check exists in any searched source. PR #1234 does not overlap. The credits are present and
correctly attributed, with three non-blocking fixes: Gallego wording, missing links for Pintz/StR/FLINT, and the
same-library caveat.

pass: true
