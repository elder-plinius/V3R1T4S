# Pre-Registration: Attack on Constant-Weight Code Bounds (`Andw.html`)

> Note added 2026-11-05, not contributor text: this is the contributor's working record. Paths such as `results/...` name files in the contributor's own workspace and are not shipped. The shipped object is `object/A27_8_10_1740.txt`, and the shipped checkers are in `verify-it-yourself/`.

## 1. Target & Baseline Snapshot

- **Target Table**: Andries E. Brouwer's *Bounds for binary constant weight codes* (`https://aeb.win.tue.nl/codes/Andw.html`).
- **Frozen Local Snapshot**: a copy of https://aeb.win.tue.nl/codes/Andw.html saved by the contributor at the start of the work (not shipped)
  - **SHA-256**: `bc8822714c5d0f6414f158e6f0dad6529b9253aaf33b6b4a4c620105ee7e3653`
  - **Size**: `261,806` bytes (`6,999` lines)
- **Prior-Art Cross-Check Corpora**:
  1. `bigger-codes` (`[Pl]` in `Andw.html`): 30 lower-bound codes and 5 Delsarte LP upper-bound certificates already merged into the contributor's frozen Andw.html snapshot.
  2. Lysenstoen (`arXiv:2607.19550v1`): 45 cells with improved lower bounds (44 already merged into the frozen Andw.html snapshot as `Ly`, 1 superseded by `Pl`).
  3. Echols (`arXiv:2608.13906v1`): 124 cells with improved lower bounds on `n <= 28`.
  4. Draft PR `#351` (`A(31, 10, 7) <= 106` / `108`): explicitly excluded from Goal A (`p2`).

---

## 2. Three Pre-Registered Goals & Acceptance Criteria

### Goal A — Partial Win `p2`: Exact Rational Delsarte LP Upper-Bound Certificates Beating `Andw.html`
- **Exclusion List**: Exclude `(31, 10, 7)` (draft PR `#351`) and the 5 `bigger-codes` cells already merged as `L` in `Andw.html` (`(31,12,10)`, `(31,12,11)`, `(32,12,10)`, `(32,12,15)`, `(32,12,16)`).
- **Success Criterion**: Certify in 100% exact rational arithmetic (`fractions.Fraction`, zero floating-point reliance) at least 5–10 cells $(n, d, w)$ where $A(n, d, w) \le U < U_{\text{table}}$ (mirror-aware across $(n, d, w)$ and $(n, d, n-w)$).
- **Two Pre-Registered Families**:
  - **Family A1 (Extended Delsarte LP on Printed `lo-hi` Ranges)**: Combines the Johnson scheme Delsarte inequalities ($D_k$: $-\sum_{x=\delta}^w a_x Q_k(x) \le Q_k(0) = m_k$), the per-distance support-split bound ($R_x$: $a_x \le \binom{w}{x} A(n-w, d, x)$), and the $(t, s)$-shortening moment inequality ($M_{t,s}$: $\sum_{x=\delta}^w \binom{w-x}{s}\binom{n-w-x}{t-s} a_x \le \binom{w}{s}\binom{n-w}{t-s}(A(n-t, d, w-s)-1)$), using **only** explicitly printed `lo-hi` upper bounds from the frozen Andw.html snapshot.
  - **Family A2 (Pure Delsarte LP on Unmarked `n > 28` Cells)**: Uses **only** $D_1, \dots, D_w$ (zero table inputs!) to strictly beat the iterated Johnson upper bound on cells with $n > 28$ where the frozen Andw.html snapshot omits an upper bound (`lo-...` or secondary table entries).

### Goal B — Partial Win `p1`: Explicit Constant-Weight Code Certificates for Unlinked 1990 `[BSSS]` Citations
- **Success Criterion**: Identify at least 3–5 cells $(n, d, w)$ in the frozen Andw.html snapshot whose lower bound $M = L_{\text{table}}$ is an unlinked 1990-era citation (neither $(n, d, w)$ nor $(n, d, n-w)$ has an `href="cwc/..."` link in the frozen Andw.html snapshot, and the cell is not in `arXiv:2607.19550` or `arXiv:2608.13906`), and construct + verify an explicit binary constant-weight code of length $n$, weight $w$, minimum Hamming distance $\ge d$, and size $M = L_{\text{table}}$.

### Goal C — Full Win: Explicit Constant-Weight Codes Strictly Beating Live `Andw.html` Lower Bounds ($M > L_{\text{table}}$)
- **Success Criterion**: Construct and verify explicit constant-weight codes with $M > \max(L_{\text{table}}(n, d, w), L_{\text{table}}(n, d, n-w))$ strictly beating today's live Andw.html (including all merged `Pl` and `Ly` records) AND strictly exceeding both `arXiv:2608.13906` and `arXiv:2607.19550`.
- **Search Architecture (`cwc_search.c`)**:
  - **Degree-Sorted Coordinate Relabeling**: Sorts coordinates $0 \dots n-1$ in descending order of ones-frequency in the seed code before colexicographic ranking. Because the co-blocking cluster extractor and maximum independent set (`mis_exact_g`) branch in colexicographic order under a node cap, degree-sorted coordinate relabeling breaks colexicographic tie-breaking traps and exposes new augmenting configurations on previously plateaued `[Pl]` and LNS codes.
  - **Co-Blocking Cluster LNS + Bit-Parallel Exact MIS**: Maintains an exact $(w - d/2 + 1)$-subset owner table over $\binom{n}{t}$ and conflict counter over $\binom{n}{w}$, extracts connected removal clusters of size up to $r_{\max}$ on the co-blocking graph of $1..K_B$-blocked candidate words, solves the local maximum independent set exactly via bit-parallel branch-and-bound, and applies greedy maximal disjoint sets of improving ($+1, +2$) or plateau ($+0$) swaps.

---

## 3. Standalone Verification Protocol

Every artifact the contributor produced had to pass the contributor's own exact verifier (not shipped). For this package, the shipped checkers in `verify-it-yourself/` play that role; see `RUN_IT_YOURSELF.md`.
