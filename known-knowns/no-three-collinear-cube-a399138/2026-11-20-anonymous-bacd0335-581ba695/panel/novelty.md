# SKEPTIC 2 — NOVELTY

**pass: true**

No published source gives an upper bound at or below 97 for a(7) (OEIS A399138, the 3D n×n×n no-three-in-line problem). The best published upper bound remains 98 (the elementary a(n) <= 2n^2 bound, = 98 at n=7).

## Sources fetched (fresh, this panel, UTC)

1. **OEIS A399138** — https://oeis.org/A399138 — fetched 2026-11-20T15:05:10Z.
   Data line: 1, 8, 16, 28, 40, 64 (n=1..6). Comments: "Lower bounds for the next terms are a(7) >= 73 ... and a(8) >= 94". Formula: "a(n) = Theta(n^2): the upper bound a(n) <= 2*n^2 is elementary" (= 98 at n=7). No recorded bound below 98. Last edits (Weisstein Oct 27 2026; von Brömssen Oct 03 2026) are all postdating the lower-bound updates — nothing lowers the ceiling.

2. **arXiv 2609.25133 (Kudriashov)** — https://arxiv.org/abs/2609.25133 — fetched 2026-11-20T15:05:10Z.
   Still **v1** (submitted 2026-09-20; submission history shows [v1] only, no revision). Abstract gives only *lower* bounds for the cube: a(7) >= 73, a(8) >= 94, ...; exact values only a(1)..a(6). No upper bound below 98 for a(7).

3. **arXiv API search** — export.arxiv.org, all:"no-three-in-line" AND all:cube — fetched 2026-11-20T15:06:14Z. Only match: 2609.25133v1. No successor.

4. **arXiv API search (broad)** — all:"no-three-in-line", sorted descending — fetched 2026-11-20T15:07:07Z. Every other no-three-in-line paper is the 2D problem or a variant: 2609.12340v2 (checkerboard 2D), 2607.05255 (no-(k+1)-in-line 2D), 2605.09215 (checkerboard 2D), 2605.07000 (extensible 2D), 2603.00215 (Guy-Kelly plane), 2606.26399 (MCTS method, 2D grid). None touches the 3D cube ceiling for a(7).

5. **Wolfram MathWorld "No-Three-in-a-Line Problem"** — https://mathworld.wolfram.com/No-Three-in-a-LineProblem.html — fetched 2026-11-20T15:06:42Z. 3D section: recorded values "begin 1, 8, 16, 28, 40, 64 ... (OEIS A399138; Kudriashov 2026). Larger constructions give lower bounds rather than known exact values." Confirms no upper bound below 98 is recorded.

6. **Web searches** — DuckDuckGo (2026-11-20T15:05:42Z, later queries captcha-blocked) and Bing (2026-11-20T15:06:11Z) for cube/7x7x7/upper-bound-97 and A399138: only the 2D literature and Kudriashov's cube paper (lower bounds) surfaced. No 2025-2026 preprint or announcement claiming an upper bound below 98 for the 7x7x7 grid.

## Conclusion

All independent primary sources agree: exact a(7) is open, the recorded window is 73 <= a(7) <= 98, and the ceiling 98 is the trivial 2n^2 bound. The claim's a(7) <= 97 is a genuine improvement over every published bound and is therefore NOVEL.

context: independent fresh session (separate process, no shared history), model deepseek-v4-pro; given only the claim and the object files, never the attack code beyond what the claim names.

pass: true
