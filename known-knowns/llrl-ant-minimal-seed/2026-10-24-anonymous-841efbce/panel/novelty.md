# NOVELTY skeptic verdict: LLRL ant g(k) table k=0..5 and K0=12, target llrl-ant-minimal-seed (partial win p1)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## What I read
- claim/CLAIM.md: LLRL (colours 0,1,3 left; 2 right; write c+1 mod 4). g(k) = least H384 onset over starts with at most k non-zero cells. Table k=0..5: 256241, 555, 318, 245, 195, 174. K0=12 (fewest non-zero cells giving onset 0; 10 such 12-cell seeds). Blank onset 256241; GLR's "256100" treated as rounded and allowed.
- claim/NOVELTY_RECORD.md (prior-run notes; not trusted; used only as a list of places to re-check).
- claim/TARGET_CRITERION.md (p1 scope: g(k) for k=1..5 plus g(0) and K0=12).
- claim/data/minimisers.txt (the actual cell lists, so I could search for those seeds, not only the numbers).

I did not read anything outside claim/ except public web pages.

## What I ran (commands and key output lines)

OEIS JSON (curl, fmt=json):
- `https://oeis.org/search?q=555,318,245,195&fmt=json` → `null`
- `https://oeis.org/search?q=554,317,244,194&fmt=json` → `null`
- `https://oeis.org/search?q=256241,555,318&fmt=json` → `null`
- `https://oeis.org/search?q=555,318,245&fmt=json` → `null`
- `https://oeis.org/search?q=318,245,195,174&fmt=json` → `null`
- `https://oeis.org/search?q=LLRL&fmt=json` → `null`
- `https://oeis.org/search?q=256241&fmt=json` → A256241 only: "Numbers n whose Euler's totient function phi(n), divided by two, plus one, ... is a divisor of n." Unrelated.

arXiv / journal (fetched HTML/PDF text):
- https://arxiv.org/abs/2409.10124 and https://ar5iv.labs.arxiv.org/html/2409.10124 : grep hit for 256100 is the blank-grid sentence; no 256241, 555, 318, 245, 195 as onsets; the only "174" is TCS volume 174 in the bibliography.
  Quote: "from the initial 0-uniform grid, the ant reaches the dominant 384 period highway after 256100 steps."
- Springer Natural Computing 24:497–509 (2025), DOI 10.1007/s11047-025-10018-9 : same paper; abstract/snippets and notes point at lutfalla.fr/ant/highway.html?antword=LLRL ; "174 Accesses" is a download counter, not g(5).
- https://ar5iv.labs.arxiv.org/html/2506.10482 (Lutfalla, LLLR): "minimal seed pattern that starts the highway" is for LLLR P52/P156, a different rule. LLRL is mentioned only as GLR's period-384 + rare 308/380/388/928 highways.
- https://arxiv.org/html/2505.05426 (Lutfalla, Sideways): LLRRRL and LLRLRLL, not LLRL.

Lutfalla simulator / GitLab:
- https://lutfalla.fr/ant/js/highway.js : `llrl_highway384 = {..., "grid":[[0,2,2,0,0,1],[0,3,2,0,0,1],[0,3,3,0,1,3],[1,0,0,2,3,0]]}` — 13 non-zero cells, ant at [2,2]. This is a period-384 highway snapshot (onset 0 for that finite grid), not a g(k) table and not fewer than 12 cells.
- Same grids in GitLab commit b8ca1b75 (2024-09-04) "added the highways for LLRL": https://plmlab.math.cnrs.fr/vlutfall/generalized_langtons_ants_js/-/commit/b8ca1b7566ed4da0c00000da7b14c824f3d095a7
- Simulator UI https://lutfalla.fr/ant/gl_ant.html loads those presets; no onset table.

Other public pages (search + page fetch):
- Wikipedia Langton's ant: classic RL highway ~9977, multi-colour examples; no LLRL g(k).
- MathWorld Langton's Ant: classic only.
- LifeWiki OCA:Langton's ant: classic only.
- ConwayLife forums (Langton's Ant Challenge, resolved-collection, Society): long blank-grid times for other rules; no LLRL onset-by-k table.
- Reddit r/cellular_automata: highway-period hunts (MrCamoga et al.); no LLRL sparse-seed table. One comment that classic RL needs "12 blocks or so" is a different rule.
- GitHub MrCamoga/Langton-s-Ant and langtonsant.es: rule-space highway census from blank/random soups, not LLRL g(k).
- YouTube https://www.youtube.com/watch?v=22dfYC_q_ho (2026-10-15): transcript "256,241 steps of chaos. Then: a road." among a gallery of 2–12 colour rules. This is the blank-grid onset (allowed). No k=1..5 table.
- MathOverflow / Math.SE: classic highway conjecture; no LLRL table.
- Semantic Scholar page for GLR: citing follow-ups are Lutfalla's 2505.05426 and 2506.10482 (already read).
- Queries for the literal seed `1,0,1` with LLRL/555, and for "least onset" / g(k) / "fewest" cells LLRL, returned the GLR/Lutfalla pages above and nothing else matching the table.

## Findings
The table (and an equivalent 0-indexed list 554,317,244,194,…) is not on OEIS. It is not in GLR 2409.10124 / the 2025 Natural Computing article. Those sources give the H384 fact and a rounded blank onset of 256100, which the claim already treats as known.

Lutfalla's public simulator publishes an H384 *snapshot* with 13 non-zero cells. That shows some 13-cell finite grid already sits on the highway at t=0. It does not publish minimality, does not list g(1)..g(5), and does not beat K0=12.

arXiv 2506.10482 publishes *minimal seeds for LLLR* highways (onset 0). That is a different rule and a different table.

I did not find a published smaller onset for any k in 1..5, nor a published onset-0 LLRL seed with fewer than 12 non-zero cells, nor a public list of fastest-highway LLRL seeds indexed by number of non-zero cells.

Blank onset 256241 itself is public (YouTube 22dfYC_q_ho; GLR's 256100 is the rounded form). That is allowed.

## Caveats
- The Springer full PDF is paywalled; I used arXiv HTML/PDF (v1, 16 Sep 2024), Springer abstract/snippets, and ResearchGate preview. I saw no extra seed table in those.
- Semantic Scholar / arXiv APIs rate-limited; citing papers were recovered from the Semantic Scholar HTML snippet and from Lutfalla's later arXiv notes. I may have missed an unindexed preprint, a private gist, or a forum attachment.
- I did not re-simulate the ant; this is a novelty check, not a correctness check of the numbers.

scope: Verified that the LLRL g(k) list 256241,555,318,245,195,174 (and 0-indexed 554,317,244,194) and the claim K0=12 are absent from OEIS, GLR 2409.10124 / Nat. Comput. 2025, Lutfalla simulator/GitLab, arXiv 2506.10482 and 2505.05426, Wikipedia, MathWorld, LifeWiki, ConwayLife, Reddit, GitHub highway-search projects, MathOverflow/Math.SE, and the YouTube description that already states the blank onset; did not audit completeness of the exhaustive searches inside claim/code.
pass: true
