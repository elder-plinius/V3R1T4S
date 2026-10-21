# Kissing number lower bounds in dimensions 25-48 (beat the max over ALL sources, not Cohn's table)

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Find K nonzero vectors of equal norm in R^d, 25 <= d <= 48, with every pairwise angle >= 60 degrees, so that K exceeds the best known kissing configuration for that d. Cohn's table https://cohn.mit.edu/kissing-numbers was updated after 2026-10-08 and on 2026-10-20 meets or exceeds the 2026-10-08 vetter snapshot below in every d in 25..48; still re-derive B(d) from ALL sources. Cohn 2026-10-20 (orientation only): d25 197583, d26 199868, d27 201589 (Takhanov-Yun, github.com/k-nic/kissing_d25-31); d28 205172, d29 210495, d30 222073, d31 241079 (K. Li, github.com/Felpix-Studios/kissing-number); d33 364736, d34 384836 (the V3R1T4S codes A(33,8,8) >= 1809 and A(34,8,8) >= 1965 with Edel-Rains-Sloane); d32 and d35..48 equal the snapshot. The records are spread over arXiv papers AND public GitHub repositories. Vetter's snapshot on 2026-10-08 (orientation only; NEVER use these as the bar, re-derive live): d25 197580 (Yang); d26 199806, d28 204896, d29 209968, d30 221012, d31 238662 (Kravatskiy repo RESULTS.md); d27 201567 (Yang); d32 347584, d33 363968, d34 384196, d35 409676, d36 484760, d37 498024, d38 591900, d39 763668, d43 2553792, d45 7380090 (Yang, arXiv:2609.35051 Table 1); d40 1092000, d41 1324472, d42 1792386, d44 4153600, d46 12309600, d47 23766960 (Dorofeev-Sun-Wang arXiv:2607.20359 / wcgbg sphere-packing repo / Boyvalenkov-Cherkashin arXiv:2312.05121); d48 52416000 (P48). Takhanov-Yun arXiv:2609.21591 (d25-31) and Echols arXiv:2608.13906 (d32-34, d37) are below these. For d=32..35 Yang's values equal exactly the modified Edel-Rains-Sloane bound tau_d >= 2^17 + 2^7*A(d,8,8) + 2d(d-1) with A = 1676/1803/1960/2158 (Brouwer's live Andw.html cells are lower: 1674/1800/1949/2157). For d36 the same bound needs A(36,8,8) >= 2744 to pass 484760. Yang's d36-39 values do not follow from his listed codes, so other constructions are involved there. The machine-verified V3R1T4S codes A(33,8,8) >= 1809 and A(34,8,8) >= 1965 (constant-weight-codes/ in this repository) would give tau33 >= 364736 and tau34 >= 384836 by the formula; Cohn's table now lists exactly these values for d33 and d34, citing those codes. Our own success criterion still requires explicit vectors.

## What counts as a win

Success means K vectors in R^d (25 <= d <= 48), given EXACTLY with integer coordinates (or rational coordinates scaled to integers). All vectors must have identical squared norm Nsq, every pair must satisfy <x,y> <= Nsq/2, and no two vectors may coincide, all verified in exact integer arithmetic. K must be STRICTLY GREATER (direction: max) than B(d) = the maximum, over every dimension d' <= d (a configuration in R^{d'} embeds in R^d), of ALL of the following, each read LIVE at verification time: (i) the lower bound at https://cohn.mit.edu/kissing-numbers; (ii) every value in arXiv:2609.35051 (Yang et al., including its Table 1 'comparison' column and any later version), arXiv:2609.21591, arXiv:2608.13906, arXiv:2607.20359, arXiv:2511.13391, arXiv:2312.05121; (iii) every value in the public repositories https://github.com/alexlegeartis/KissingNumbers (RESULTS.md and contributed/), https://github.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research, https://github.com/wcgbg/sphere-packing, and https://github.com/CDM1619/PackingStar; (iv) every value in any other arXiv paper, journal article, public repository or public catalogue found by a FRESH web + arXiv search at verification time, REGARDLESS of its date; (v) for d = 32..39, the value 2^17 + 2^7*L + 2d(d-1), where L is the largest A(d,8,8) lower bound in Brouwer's live https://aeb.win.tue.nl/codes/Andw.html or in any published source. If any source in (i)-(iv) cannot be read with an honest client (no spoofed User-Agent, no retry through 403/429, no CAPTCHA/JS-challenge bypass), the result is PENDING TABLE CHECK and NOT a success. K must not exceed the smallest published upper bound for d (Cohn's table or newer); exceeding it means a bug. A count from a formula alone is NOT a certificate: the vectors must be listed and checked. Beating Cohn's table alone is NOT a success.

## Partial wins

- **p2:** An improved upper bound: an SDP/LP certificate, verified in exact rational or interval arithmetic, proving a kissing-number upper bound strictly below the smallest published upper bound for some d in 25..48 (Cohn's live table, de Laat-Leijenhorst 2024, and anything newer found by a fresh search at verification time).

## How a win is checked

Use an independent script.
- Load the vectors as integer arrays and assert every squared norm equals Nsq.
- Compute all Gram entries in blocks. A float32/float64 matmul is exact when |entries| * d * max|coord|^2 < 2^24 or 2^53; otherwise use int64 with overflow checks. Assert that every off-diagonal entry is <= Nsq/2.
- Sort the rows to assert that no two are equal.
- K ~ 3.6e5 in d=33 means about 6.5e10 pairs, a few minutes of blocked matmul on a laptop.
- If an Edel-Rains-Sloane-type construction is claimed, regenerate the vector set from the stated code and construction, assert it equals the submitted set, and check the code with an independent constant-weight checker (all popcounts w, pairwise distance >= 8).
- Compute B(d) live: re-fetch Cohn's page, the listed arXiv papers (latest versions), the four listed GitHub repos (RESULTS.md / README / constructions/), the Brouwer A(d,8,8) cells, and run a fresh web + arXiv search for any other source; take the max over all d' <= d. Quote URL, value and fetch time for every input. Any unreadable source => PENDING TABLE CHECK.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://cohn.mit.edu/kissing-numbers/>

## Sources

- <https://cohn.mit.edu/kissing-numbers>
- <https://arxiv.org/abs/2609.35051>
- <https://arxiv.org/abs/2609.21591>
- <https://arxiv.org/abs/2608.13906>
- <https://arxiv.org/abs/2607.20359>
- <https://arxiv.org/abs/2511.13391>
- <https://arxiv.org/abs/2312.05121>
- <https://github.com/alexlegeartis/KissingNumbers>
- <https://github.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research>
- <https://github.com/wcgbg/sphere-packing>
- <https://github.com/CDM1619/PackingStar>
- <https://aeb.win.tue.nl/codes/Andw.html>
- <https://github.com/k-nic/kissing_d25-31>
- <https://github.com/Felpix-Studios/kissing-number>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Build the explicit configuration via the code link, tau_d >= 2^17 + 2^7*A(d,8,8) + 2d(d-1) (Edel-Rains-Sloane as modified in Echols eq. (2) / Yang Sec. 5), from the machine-verified V3R1T4S A(33,8,8) >= 1809 and A(34,8,8) >= 1965 codes. Check it exactly and compare against Yang's Table 1.
- Push A(32,8,8) above 1676 and A(35,8,8) above 2158 (Yang's implied codes), and A(36,8,8) to >= 2744 (live Brouwer 2742), with the constant-weight-codes plateau-walk LNS engines (lb_lns_fast3). Each extra codeword adds +128 to tau_d. For d37-39, first find out which construction gives Yang's values.
- d = 25..31: start from the Kravatskiy repo / Yang configurations (they are above Takhanov-Yun) if they are published as coordinates, and look for insertions via exact local search: a free spherical cap of angular radius 60 degrees found by LP or SAT over a lattice shell.
- d = 40..47: the records are Conway-Sloane / P48p cross-section and antipode packings (Dorofeev-Sun-Wang, wcgbg repo), far above Cohn's entries; start from those, not from Cohn's Barnes-Wall/laminated values.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Cohn's table is stale for almost every d in 25..47 (e.g. d46/d47 by a factor of 2+). Beating it alone is NOT novel. Many records live only in GitHub repositories (Kravatskiy, Oxelra/Qiushi, wcgbg), not on arXiv; the bar is the max over ALL sources and all d' <= d.
- Overlap: bank target kissing-number-low-dim has partial win p1 (d >= 24 vs Cohn's table only). That p1 is now dangerously loose; this entry's all-sources bar must govern any d in 25..48.
- Yang's Table 1 comparison column (e.g. d25 197579, d43 2545056, d45 7379838) shows the previous bests came from repositories, not Cohn; read it.
- Kravatskiy's repo lists d32-37 and d40-43 as exactly at the Edel-Rains-Sloane value; reproducing a known ERS configuration is not a win.
- The construction's validity conditions (the shell components and their mutual inner products) must be checked in the explicit vector set, not assumed from the formula.
- Floating-point near-feasible configurations do not count unless they are exactified.
- Yang et al. and Kravatskiy update fast (commits within days); re-read repos and re-search arXiv at verification time.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/kissing-number-dims-25-48.md
```

Already set up? Say `run V3R1T4S on kissing-number-dims-25-48`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `kissing-number-dims-25-48`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
