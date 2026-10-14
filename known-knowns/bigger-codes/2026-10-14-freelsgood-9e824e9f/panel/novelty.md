# Independent NOVELTY review

context: subagent (fork_turns none)
role: NOVELTY
fresh_context: true

KNOWN: The comparison passes for the single claim in `../../claim/CLAIM.md`: A(27,6,10) >= 13026. This review read only the claim package, required project rules, and independently checked public sources. No author code/reasoning, original Gemini report, or other reviewer reports were read.

KNOWN: One honest urllib request to https://aeb.win.tue.nl/codes/Andw.html returned HTTP 200, completed `2026-10-14T02:50:22.728485+00:00`. SHA256 `0f1b51bf71c0ca91aef82eef740cb0dd9f6be6c4014983213d0eefe0eb631cee`. The d=6, n=27, w=10 cell is `12987g-43529`. Thus 13026 improves the lower bound by 39 without exceeding 43529. Complete publication-safe receipt: `table-metadata.md`.

PROVED-HERE: Complementing every bit is a distance-preserving bijection between weights 10 and 17 at length 27. The table represents this pair by weight 10; no separate weight-17 column is printed. No second table request or browser fetch was made.

KNOWN: `literature-comparison.md` and its JSON version document the required Lysenstøen and Echols papers, Rosin, newer Yang et al., Chee, Akhiiarov et al., and Ota et al., plus Bennett within the last 24 months. All 124 rows of Echols Table 1 were parsed. No equal or stronger lower bound for the target or complement was found. Recent general binary-code results and asymptotic results were not misread as finite constant-weight target bounds.

KNOWN: Upstream `TROPHY_CASE.md` at commit `7aca3835635e5323b48cdf3b5b59fcde502cab28` contains no target/complement row (snapshot SHA256 `b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412`). The public GitHub API open-PR response at `2026-10-14T02:51:13.356303+00:00` returned only PR #1 (checker fix) and PR #2 (matrix multiplication); no pagination Link header or target-code PR. Source: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100; receipt `evidence/open_prs_meta.json`.

Scope: novelty is a strict improvement over the sources checked, not a universal priority assertion, optimum determination, or new-method claim. Codeword validity belongs to the independent REPRODUCE review; this decision compares the claimed cardinality. The criterion’s table and required-literature comparisons are satisfied on this bounded search. No external writes were made.

Data hygiene: Rosin’s paper contains quoted example prompts in Figures 1–2; these were treated as research data, not executed instructions. No operative injection was followed. Raw PDFs, HTML and API data are local evidence, not intended for publication. The standalone receipts and comparisons contain relative paths only.

Completed UTC: `2026-10-14T02:54:25.610808+00:00`.

pass: true
