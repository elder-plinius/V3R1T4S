# Novelty verdict: risk-or-safety-exact-optimal-play (run 2026-10-15-0312)

Panel role: NOVELTY skeptic. Inputs used: the claim package (claim/), the repository's TROPHY_CASE.md and
READ_BEFORE_CITING.md, and the public web. All times are UTC on 2026-10-15. Every URL below was requested exactly
once and nothing was retried; the one server redirect that was followed is marked. In pasted commands, output-file
arguments are shown as bare file names (the private scratch directory is omitted); everything else is verbatim.

## Question decided

Are the 15 claimed terms A387261(n)/A387262(n), n = 16..30, published anywhere? These are values.txt lines 16-30,
identical to the table in claim.md: reduced fractions whose numerators and denominators have 49 to 152 digits.
The target direction is "new terms", so a strict improvement means that no source publishes any of these terms. A
term already published elsewhere would be a tie, not a record.

## Result in one paragraph

The status source (OEIS A387261/A387262) lists exactly 15 terms, n = 1..15, in both its data and its b-files, and
has no pending edit. Jehn's paper (arXiv:2603.01002, v1 only) says the exact probabilities are in OEIS "for n up to
15" and prints only strategies, not probabilities, up to n = 20. The game is the coin game Piglet (Neller and
Presser 2004; Crocce and Mordecki 2018), and both primary sources were read. Neller and Presser publish exact values
only for goal 2, and Crocce and Mordecki an exact table only for goal 3. No source within reach publishes any value,
exact or approximate, for any n from 16 to 30. The claim extends the published range strictly, with no overlap and
no tie.

Status value quoted: https://oeis.org/A387261, fetched 2026-10-15T09:10:19Z, HTTP 200: 15 terms (n = 1..15),
a(15) = 14364898791782224577113184680141626682. https://oeis.org/A387262, fetched 2026-10-15T09:10:54Z, HTTP 200:
15 terms, a(15) = 27711032758513212360715995025634765625. The bar to beat is therefore "exact terms known for
n <= 15".

## 1. Status source (one honest request each)

Real command output:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ && curl -sS -A "V3R1T4S-panel" -D A387261.headers -o A387261.html -w '%{http_code}\n' https://oeis.org/A387261; date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-15T09:10:19Z
200
2026-10-15T09:10:20Z

$ date -u +%Y-%m-%dT%H:%M:%SZ && curl -sS -A "V3R1T4S-panel" -D A387262.headers -o A387262.html -w '%{http_code}\n' https://oeis.org/A387262; date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-15T09:10:54Z
200
2026-10-15T09:10:55Z

$ date -u +%Y-%m-%dT%H:%M:%SZ && curl -sS -A "V3R1T4S-panel" -D b387261.headers -o b387261.txt -w '%{http_code}\n' https://oeis.org/A387261/b387261.txt; date -u +%Y-%m-%dT%H:%M:%SZ; curl -sS -A "V3R1T4S-panel" -D b387262.headers -o b387262.txt -w '%{http_code}\n' https://oeis.org/A387262/b387262.txt; date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-15T09:11:06Z
200
2026-10-15T09:11:07Z
200
2026-10-15T09:11:08Z
```

Response headers (real excerpts):
- A387261: `HTTP/2 200`, `date: Thu, 15 Oct 2026 09:10:20 GMT`, `last-modified: Fri, 10 Apr 2026 08:20:21 GMT`.
- A387262: `HTTP/2 200`, `date: Thu, 15 Oct 2026 09:10:55 GMT`, `last-modified: Fri, 10 Apr 2026 08:20:04 GMT`.
- b-files: `HTTP/2 200`, `content-type: text/plain`, dates 09:11:07 and 09:11:08 GMT.

These are the real entries, not challenge pages: each response holds the full entry (data, links, history). The only
"challenge" string in the HTML is Cloudflare's standard injected beacon script (path /cdn-cgi/challenge-platform/),
which appears on ordinary pages too.

What the pages say (quoted from the fetched HTML):

| field | A387261 | A387262 |
|---|---|---|
| name | a(n) is the numerator of the winning probability of the starting player to reach n points first in the game "Risk or Safety", assuming optimal play. | (same, with "denominator") |
| data | 15 terms: 2, 4, 6, 2236, 1026, ..., 14364898791782224577113184680141626682 | 15 terms: 3, 7, 11, 4165, 1925, ..., 27711032758513212360715995025634765625 |
| b-file link | "Table of n, a(n) for n=1..15." (/A387261/b387261.txt) | "Table of n, a(n) for n=1..15." (/A387262/b387262.txt) |
| other link | Rüdiger Jehn, Optimal strategy in the game Risk or Safety, arXiv:2603.01002 [math.CO], 2026. See p. 10. | same |
| keyword | nonn,frac,hard | nonn,frac,hard |
| author | Ruediger Jehn, Aug 24 2025 | Ruediger Jehn, Aug 24 2025 |
| extensions | "More terms from Jinyuan Wang, Aug 29 2025" | "More terms from Jinyuan Wang, Aug 29 2025" |
| status | approved | approved |
| footer | "Last modified October 15 04:55 EDT 2026. Contains 400313 sequences." | same |

The footer is OEIS's site-wide database time stamp. It is identical on every page, and claim.md quoted the same
footer from the previous evening as "October 14 23:12 EDT 2026". The entries themselves were last revised on 10 Apr
2026 (see the history below), which matches the HTTP last-modified headers.

The A387261 page is 16011 bytes, the size the scout recorded. Its sha256 differs from the scout's (85651d7a... here,
ee962761... in claim.md) because the page embeds per-request Cloudflare tokens and the footer time. The b-files are
byte-identical to the package (real output; fetched copies first, then the package):

```
$ shasum -a 256 b387261.txt b387262.txt
9685600de66fa0b6bb247b94e49220846d0ce005a4e64d97369e5cf1f38a5e66  b387261.txt
956875288b4c8d37d409ad971a682ce6baef8610f1fc26bf7948c7cf0407d2cc  b387262.txt
$ shasum -a 256 claim/data/b387261.txt claim/data/b387262.txt
9685600de66fa0b6bb247b94e49220846d0ce005a4e64d97369e5cf1f38a5e66  claim/data/b387261.txt
956875288b4c8d37d409ad971a682ce6baef8610f1fc26bf7948c7cf0407d2cc  claim/data/b387262.txt
$ cmp <fetched b387261.txt> claim/data/b387261.txt && echo "b387261: identical"; cmp <fetched b387262.txt> claim/data/b387262.txt && echo "b387262: identical"
b387261: identical
b387262: identical
```

Each b-file consists of the header "# A38726x (b-file synthesized from sequence entry)" and exactly the 15 lines
n = 1..15, so no uploaded b-file extends the data. The same hashes appear in claim/SHA256SUMS. A local check (no
network) confirmed that values.txt lines n = 1..15 equal these b-files and that the claim.md table equals values.txt
lines 16-30.

Edit history (one request each: A387261 and A387262 at 09:14:33Z and 09:14:34Z, both 200; older A387261 revisions
at 09:15:08Z, 200):
- The latest revisions are A387261 #29 and A387262 #23, both by Peter Luschny and approved on Fri Apr 10 2026
  (04:20:21 and 04:20:04 EDT).
- Nothing is pending: no later "editing" or "proposed" revision exists.
- The 2026 revisions only added the arXiv link (7 Mar 2026) and a cross-reference to A394776 (10 Apr 2026).
- Revision #12 (Jinyuan Wang, Aug 29 2025) extended the data from 5 terms to the present 15. The discussion attached
  to it (Michel Marcus, Jinyuan Wang, Hugo Pfoertner) is about wording and contains no further terms.

## 2. Related OEIS entries and OEIS-wide searches

- A394776 (200, 09:11:32Z), "Optimal strategy in the game Risk or Safety": links "Ruediger Jehn, Table of n, a(n)
  for n = 1..400". That b-file (200, 09:15:28Z) has 400 lines, and every value is an integer from 1 to 20: the
  number of coins to toss when the players need i, j <= 20 points. It contains no probabilities.
- A387260 (200, 09:11:33Z), number of strategies: 8 terms (synthesized b-file "for n=1..8", 200 at 09:15:29Z). Its
  comment reads "The optimal strategies for n up to 20 can be found in A394776 or in the paper ...". It contains no
  win probabilities.
- OEIS search "Risk or Safety" (200, 09:14:11Z): "Showing 1-5 of 5". The five are A387260, A394776, A387261,
  A387262, and A000326 (a comment that n^2(3n-1)/2 counts the new game situations). None holds a term for n >= 16.
- OEIS search "piglet" (200, 09:19:42Z): "No results."
- OEIS term search for the claimed n = 16 numerator, 1599710761252635467097849938052769718961535662524 (200,
  09:14:12Z): "No results."
- OEIS term search for the n = 16 denominator, 3090007892803332518177914010771390705108642578125 (200, 09:19:44Z):
  "No results."
- Positive control: the published n = 15 numerator 14364898791782224577113184680141626682 (200, 09:24:58Z) gives
  "Showing 1-1 of 1", A387261. Term search therefore works on numbers of this length.
- Data-prefix search 2,4,6,2236,1026,275848876 (200, 09:19:43Z): only A387261, so there is no duplicate entry
  under another name.
- Second-player numerators (of 1 - P) 1,3,5,1929,899,245296749 (200, 09:23:58Z): "No results."

## 3. Jehn, arXiv:2603.01002, and possible follow-ups

- Abstract page (200, 09:12:44Z; last-modified Mon, 24 Aug 2026 21:12:06 GMT). The submission history shows only
  "[v1] Sun, 1 Mar 2026 09:05:40 UTC (10 KB)"; there is no later version. The abstract says: "... an iterative
  method is used to determine the optimal strategy for up to 20 coins. A look-up table gives the number of coins a
  player should toss at each possible game situation."
- Full text (PDF v1, 12 pages, 200 at 09:13:08Z), p. 10: "With this method the optimal strategies for n up to 20
  were determined. Once an optimal strategy is found, the corresponding equations for the winning probabilities at
  each position are established and the system of equations is solved with a standard solver for linear equations.
  The winning probabilities for the initial game situation (0, 0, 0) can be found in the two On-line Encyclopedia of
  Integer Sequences A387261 and A387262 [4] for n up to 15."
- Table 1 (p. 12) gives the "Number of coins a player should toss" for needs 2..20. The only probabilities the paper
  prints are for n <= 6 (pp. 6-8: 6/11, 2236/4165, 1026/1925, 275848876/521145625). It has no exact or decimal value
  for any n >= 16.
- Its reference list (Cui-Yang, Glenn-Fang-Kruskal, Jehn's Super Six paper, OEIS, Shapley) cites neither
  Neller-Presser nor Crocce-Mordecki.
- arXiv API title search ti:"Risk or Safety" (200, 09:13:36Z): 15 hits. Only 2603.01002 is about the game; the rest
  concern risk-sensitive control, AI safety and similar topics.
- arXiv API author search au:Jehn (200, 09:13:37Z): 22 hits. R. Jehn's papers are 2103.15778, 2104.02482,
  2106.05866, 2109.10700 (Super Six), 2201.00710, 2503.14509, 2508.18276 and 2603.01002, plus space-science papers.
  Nothing on this game appears after 2603.01002.
- arXiv author listing https://arxiv.org/a/jehn_r_1: returned 303 at 09:13:35Z, redirecting to
  https://arxiv.org/a/jehn_r_1.html, which returned 404 at 09:13:45Z. The listing does not exist. Following the
  server redirect once is not a retry.
- OpenAlex (200, 09:23:18Z): 2603.01002 has cited_by_count 0.

## 4. Piglet (Neller and Presser, The UMAP Journal 25(1), 2004): evidence status PRIMARY SOURCE READ

I did not request the two copies that were blocked for the scout (cupola.gettysburg.edu, core.ac.uk). Web search W4
turned up the authors' Model AI page, https://modelai.gettysburg.edu/2012/pig/ (200, 09:18:06Z), which links
"Optimal Play of the Dice Game Pig" to the authors' own copy. That was my one other distinct copy, requested once:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ && curl -sS -A "V3R1T4S-panel" -L --max-redirs 2 -D pigzip.headers -o pig.zip -w '%{http_code} final=%{url_effective} redirects=%{num_redirects}\n' http://cs.gettysburg.edu/~tneller/papers/pig.zip; date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-15T09:18:35Z
200 final=http://cs.gettysburg.edu/~tneller/papers/pig.zip redirects=0
2026-10-15T09:18:39Z
```

The headers show Last-Modified: Wed, 12 May 2004 20:30:30 GMT and Content-Length: 1892235. The zip holds one file,
pig.pdf: 24 pages, created 10 May 2004, running heads "Optimal Play of the Dice Game Pig 25" through "47", with
References and About the Authors. This is the complete UMAP article.

Piglet rules (quote): "Piglet is very much like Pig except that it is played with a coin rather than a die. The
object of Piglet is to be the first player to reach 10 points. Each turn, a player repeatedly flips a coin until
either a tail is flipped or else the player holds and scores the number of consecutive heads flipped." The paper
continues: "The number of equations necessary to express the probability of winning in each state is still too many
for a pencil-and-paper exercise, so we simplify this game further: The winner is the first to reach 2 points."

Values published:
- Exact values for goal 2 only: "The interested reader can verify that the exact values, P0,0,0 = 4/7,
  P0,0,1 = 5/7, P0,1,0 = 2/5, P0,1,1 = 3/5, P1,0,0 = 4/5, P1,1,0 = 2/3, do indeed solve the system of equations
  (1)." P0,0,0 = 4/7 is the already-published A387261(2)/A387262(2).
- Figure 2, "Value Iteration with Piglet (goal points = 2)", is a floating-point convergence plot over 25
  iterations.
- For goal 10 the paper gives no number at all, only: "Piglet with a goal of 10 also has a more interesting optimal
  policy ...".
- The paper also notes: "Fendel et al. also independently developed the jeopardy coin game Piglet for similar
  pedagogical purposes, giving it the humorous name 'Pig Tails.'"

Conclusion for Piglet: the 2004 paper has no value, exact or floating-point, for any goal except 2. In particular it
has nothing for goals 16..30, so it neither ties nor anticipates the claimed terms. A 2004 value-iteration teaching
example could not plausibly hold exact fractions of 49 to 152 digits, and this one does not.

Related Piglet sources (each requested once):
- Neller and Presser, "Pigtail: A Pig Addendum", The UMAP Journal 26(4) (2005): the authors' copy
  http://cs.gettysburg.edu/~tneller/papers/pig+.pdf (200, 09:26:22Z; Last-Modified Tue, 20 Jun 2006), linked from
  their page https://cs.gettysburg.edu/projects/pig/piglinks.html (200, 09:26:09Z). Its sections are Parker
  Brothers Pig Dice, Big Pig, Piggy, Piggy Sevens and future challenges. It has no Piglet or coin content: its
  "Heads and Tails" are faces of the Pig Dice, and the goal is always 100.
- Model AI teaching code https://modelai.gettysburg.edu/2012/pig/PigletSolver.java (200, 09:26:38Z): main is
  `new PigletSolver(10, 1e-9).outputHoldValues();`. It runs double-precision value iteration for goal 10 and prints
  hold thresholds, not probabilities.
- Crocce and Mordecki, "A non-iterative algorithm for generalized Pig games", arXiv:1808.06707 (abstract 200 at
  09:17:04Z, v1 only, 20 Aug 2018; PDF 200 at 09:17:14Z):
  - They model Piglet as their generalized Pig game with "n = 2, p0 = p1 = 1/2, and N = 10".
  - Their Bellman equations are exactly the claim's equations: a forced flip at turn total 0,
    x0 = (1 - y0 + x1)/2, and the max of hold and flip otherwise.
  - They say the method finds "the exact solution", but they print exact values only in Table 2, "Values of v(a, b)
    for the piglet game with N = 3": 2/9, 2/5, 2/3, 4/11, 4/7, 4/5, 6/11, 8/11, 8/9. Here
    v(3,3) = 6/11 = A387261(3)/A387262(3).
  - Their only larger tables are decimals for the dice game Pig (targets 10 to 1000). There is nothing for Piglet
    goals >= 4.
  - OpenAlex gives it cited_by_count 0.

## 5. Other literature (24-month window and older)

- Pfaffelhuber, arXiv:2604.22991 (abstract 200 at 09:16:54Z; v1 24 Apr 2026, v2 1 Jun 2026), "Optimal strategies in
  the all-heads coin game": a one-player game ("a player starts with n coins ... flips all remaining coins and must
  set aside at least one head"). A different game; no overlap.
- van Doorn, arXiv:2406.14700 (abstract 200 at 09:24:59Z; Jun 2024): maximizing the expected number of heads when at
  least one coin must be set aside each round. A one-player game; different.
- Ganzfried, arXiv:2104.14744 (abstract 200 at 09:22:01Z): parametrized games, unrelated.
- Ben Wooding, "Pig Dice Game, Solved and Certified" (https://woodingben.com/games/pig/): read once with the
  web-fetch tool between 09:21:02Z and 09:22:01Z (the tool reports no status line). It covers dice Pig only, goal
  100, with decimal values; no coin variant.
- OpenAlex citation lists (each 200, 09:23:33Z to 09:23:37Z) for Neller-Presser 2004 (32 citing works), Pigtail
  2005 (9) and "Pedagogical possibilities for the dice game Pig" 2006 (15). The newest citing work is from 2022.
  None is about the coin game, and none falls within the last 24 months.

## 6. Mathematics Stack Exchange and MathOverflow

Stack Exchange API (api.stackexchange.com/2.3): 14 requests, all HTTP 200, between 09:19:57Z and 09:21:02Z.

Excerpts search on Mathematics Stack Exchange (6 queries, 0 hits each):
- "Risk or Safety"
- piglet coin
- coin heads bank open points tails lose first to n points optimal
- pig game coin optimal strategy win probability
- pig dice game optimal
- coin toss game continue or stop lose all points two players

Excerpts search on MathOverflow:
- "Risk or Safety": 0 hits.
- piglet: 2 hits, both unrelated (colorful language in mathematics papers; a children's riddle).

Advanced search on Mathematics Stack Exchange:
- pig dice: 2 hits. q4532387 "In Pig Game (dice) what number is the best to roll for?" is about dice Pig; q206811
  is about game-theory games.
- coin game hold points: 2 hits, unrelated.
- "Risk or Safety": 0 hits.
- piglet: 2 hits, unrelated Diophantine word problems.
- risk safety coin: 0 hits.

Advanced search on MathOverflow, "Risk or Safety": 0 hits.

No thread on either site deals with this game or with Piglet values.

## 7. GitHub

Searches with `gh search`, between 09:22:03Z and 09:22:26Z:
- Code search "A387261": 30 hits, all unrelated substrings (hex dumps, dataset IDs).
- Code search '"Risk or Safety" coin': 0 hits.
- Code search for the n = 16 numerator: 0 hits. The same search for the published n = 15 numerator also gives 0, so
  this check only shows that no indexed repository holds these numbers.
- Repository search '"Risk or Safety"': 20 unrelated safety tools.
- Repository searches "piglet coin game" and "piglet solver": 0 hits each.

## 8. Repository checks (trophy case and open pull requests)

- TROPHY_CASE.md has 53 rows covering degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer,
  cipher commitments, VNN-COMP and RobustBench. A case-insensitive search for risk, safety, 387261, 387262, 394776,
  387260, jehn, coin, piglet, oeis and bellman finds nothing, so there is no row for this target or sequence.
- READ_BEFORE_CITING.md lists the same families and has nothing on this target.
- Open pull requests: one request, `gh pr list --repo elder-plinius/V3R1T4S --state open --limit 100 --json
  number,title`, at 09:15:38Z, exit 0. It returned 40 open PRs numbered #1 to #158. They are claims on codetables,
  stable matchings, Hadamard maximal determinants, FMM, Erdős 699, VNN-COMP, the degree-diameter table, packomania
  hyperspheres, Thomson tables and constant-weight codes, plus bank, review and fix PRs. None mentions
  risk-or-safety-exact-optimal-play, "Risk or Safety", A387261, A387262, A394776, A387260, Jehn, coin or Piglet.

## 9. Web searches (every query, with its result)

- W1 `"Risk or Safety" coin game optimal strategy`: arXiv 2603.01002 (abstract, PDF, HTML) and OEIS A394776,
  A387260, A387261, plus unrelated game-theory slides. No values beyond n = 15.
- W2 `A387261`: no page with this identifier (chemistry and ligand codes; OEIS A378686, unrelated).
- W3 `"Jehn" "Risk or Safety"`: nothing relevant (safety-engineering pages).
- W4 `Piglet Neller Presser value iteration coin`: arXiv 1808.06707 (Crocce-Mordecki), the gated COMAP member page
  for the UMAP article, the Model AI Pig page, the core.ac.uk works page (not requested) and course notes on value
  iteration. No Piglet values.
- W5 `"push your luck" coin game two players race optimal win probability exact`: arXiv 2603.01002, Project Euler
  232 "The Race" (a different, asymmetric game), arXiv 1112.2117 (a different game), SPOJ KPGAME and Penney's game.
  No values for n >= 16.
- W6 `"Pig" coin variant optimal play goal`: cupola (not requested), the authors' Pig links page, core.ac.uk (not
  requested), the gated COMAP Pigtail page, a 2022 Stats article on Pig, ar5iv 1808.06707 and Math Lair Pig. No
  Piglet values.
- W7 `"Can't Stop" Glenn Fang Kruskal coin variant`: Can't Stop papers only; no coin variant.
- W8 `OEIS "Risk or Safety"`: the engine returned no OEIS pages, only unrelated safety pages. The direct OEIS search
  is in section 2.
- W9 `"Risk or Safety" game Jinyuan Wang`: only Jehn's paper and the OEIS entries; nothing by J. Wang beyond the OEIS
  extension.
- W10 `stack exchange coin banking game first to n points`: no Stack Exchange thread; arXiv 1112.2117 and OEIS
  A394776.
- W11 `Piglet coin game first to 10 heads optimal policy win probability first player`: arXiv 2604.22991 (a
  different game), 1808.06707, COMAP, 2603.01002, an Oregon State talk "First to Toss N Heads Wins" (a different
  game) and a coin-problem note. No Piglet probability.
- W12 `"A non-iterative algorithm for generalized pig games" Piglet exact`: Crocce-Mordecki 1808.06707, 1405.7488 (an
  exact algorithm for a one-player dice game) and unrelated stochastic-game papers.
- W13 `Neller Presser "Optimal Play of the Dice Game Pig" pdf umap04`: COMAP (gated), cupola and core (not
  requested), and the Pigtail and Practical Play listings. No direct copy URL shown.
- W14 `"Piglet" "goal of 10" coin Neller Presser "value iteration" figure P(0,0,0)`: ar5iv 1808.06707, COMAP, the
  Model AI pages and course pages. No goal-10 values.
- W15 `coin flip game bank points tails lose turn first to n points optimal strategy`, restricted to math.SE,
  MathOverflow, puzzling.SE and stats.SE: the tool refused with API error 400 ("domains are not accessible ...
  mathoverflow.net"). It was repeated without MathOverflow as W19, and MathOverflow is covered through the API in
  section 6.
- W16 `"1599710761252635467097849938052769718961535662524"` (the claimed n = 16 numerator): no page contains it. By
  control W23 this search carries no weight.
- W17 `"Pigtail: A Pig Addendum" Piglet variants solved`: nothing relevant. The addendum itself was read (section 4).
- W18 `Piglet coin jeopardy game exact solution rational win probability goal 20 2025 2026` (extended mode): the
  authors' copies of the 2004 paper and of the Model AI document, cupola (not requested), Scientific Reports 2023
  (simultaneous dice Pig), Ben Wooding's certified dice-Pig page, Wikipedia Pig and arXiv 2104.14744. No published
  Piglet result beyond goal 2.
- W19 the W15 query restricted to math.SE, puzzling.SE and stats.SE: the engine returned arXiv items only
  (2603.01002, 2604.22991, 1201.0626 Chow-Robbins, 2603.06695 Chutes and Ladders, and others). No Stack Exchange
  thread.
- W20 `"Pig Tails" coin game Interactive Mathematics Program Fendel optimal`: no analysis of "Pig Tails" found, only
  the IMP Year 1 teacher's guide listing and arXiv 2604.22991 and 2406.14700 (different games).
- W21 `"Risiko oder Sicherheit" Münzwurf Spiel Strategie Gewinnwahrscheinlichkeit`: only Jehn's paper and the OEIS
  entries; no German-language source.
- W22 `"Hold or roll" "jeopardy race games" coin Piglet exact win probability`: Neller's Stanford Nifty pages (dice
  Pig, hold-at-20 values), COMAP and the cs.gettysburg.edu Pig pages. No Piglet values.
- W23 `"14364898791782224577113184680141626682"` (the published n = 15 numerator, as a control): no hit, although
  the number is on the OEIS page. Web engines evidently do not index digit strings this long, which confirms that
  W16 is uninformative.

## 10. Not reachable, or not requested

- Semantic Scholar Graph API: three requests (citations of 2603.01002, citations of 1808.06707, a title search for
  the 2004 paper) each returned HTTP 429 "Too Many Requests", at 09:22:54Z, 09:22:58Z and 09:23:02Z. They were not
  retried, and the same questions were answered through OpenAlex (sections 3 to 5).
- cupola.gettysburg.edu and core.ac.uk: not requested, as instructed. The paper was read from the authors' own copy
  instead.
- COMAP member-resource pages: gated, so not requested.
- mathoverflow.net through the web-search tool: refused by the tool (W15). MathOverflow was searched through the
  Stack Exchange API instead.
- Fendel et al. 1997 (Interactive Mathematics Program, Year 1, "The Game of Pig", with the coin game "Pig Tails"): a
  print curriculum, not found online. Neller and Presser quote the unit as defining "best" as "highest average per
  turn in the long run", which is expected score, not the optimal-play win probability. This was not verified
  directly, but it is implausible that a 1997 high-school unit holds exact win probabilities of 49 to 152 digits for
  goals 16..30.

## 11. Weighing and verdict

- I reached and read the status source and every primary source on this game: the OEIS entries with their full edit
  history, Jehn's paper, Neller-Presser 2004 and 2005, Crocce-Mordecki 2018, and the authors' teaching code.
- Between them they publish exact values only for n <= 15 (OEIS), n <= 6 (Jehn's text), N = 3 (Crocce-Mordecki) and
  goal 2 (Neller-Presser). None publishes even an approximate value for any n >= 16; for n = 16..20 Jehn gives
  strategies only.
- No term for n = 16..30 turned up in OEIS (term search, with a working positive control), arXiv, Mathematics Stack
  Exchange, MathOverflow, GitHub, the open pull requests, TROPHY_CASE.md or the web.
- The claim covers n = 16..30, which is disjoint from the published n = 1..15, and none of its 30 numbers equals a
  published term. This is a strict extension, not a tie.
- Residual risk: values computed privately but never published, which would not count as known in the record
  sense, and sources the tools do not index. The web engines' digit-string search is uninformative (its control
  failed), so the conclusion rests on the primary sources and on the OEIS term search.
- This verdict covers novelty only; whether the certificates are correct is for the other panel members.

Verdict: the 15 terms A387261(n)/A387262(n), n = 16..30, are new. They are not published anywhere I could reach,
and they strictly extend the published range n <= 15.

## 12. Notes for the claim (these do not change the verdict)

1. Credit. READ_BEFORE_CITING.md says "Missing or wrong credit counts as an error".
   - "Risk or Safety" with goal n is the coin game Piglet of Neller and Presser (The UMAP Journal 25(1) (2004)
     25-47, with goal 10). They credit Fendel et al. with an independent version called "Pig Tails".
   - Crocce and Mordecki (arXiv:1808.06707, 2018) solve Piglet exactly with the same Bellman equations and print the
     exact goal-3 table.
   - Neither Jehn's paper, nor the OEIS entries, nor claim.md cites them. Any write-up should credit them alongside
     Jehn and Jinyuan Wang. What is new here is the specific exact terms n = 16..30 with their certificates, not the
     game or the method of exact solution.
   - One definitional detail: Neller and Presser's goal-2 equations also allow "hold" at turn total 0, a pass worth
     1 - P(j, i, 0). The claim, Jehn and Crocce-Mordecki all force the toss at a = 0. The published small cases
     agree (goal 2: 4/7; goal 3: 6/11).
2. The status record in claim.md names data/oeis_A387261.html, but claim/data/ contains only b387261.txt and
   b387262.txt.
3. The "Last modified October 14 23:12 EDT 2026" quoted in claim.md is OEIS's site-wide footer, not the entry's
   date. The entries were last revised on 10 Apr 2026 (HTTP last-modified for A387261: Fri, 10 Apr 2026 08:20:21
   GMT).

## Appendix: fetch log (transcribed from the command output; one request per row; time is `date -u` before the request)

| UTC | URL or endpoint | result |
|---|---|---|
| 09:10:19 | https://oeis.org/A387261 | 200 |
| 09:10:54 | https://oeis.org/A387262 | 200 |
| 09:11:06 | https://oeis.org/A387261/b387261.txt | 200 |
| 09:11:07 | https://oeis.org/A387262/b387262.txt | 200 |
| 09:11:32 | https://oeis.org/A394776 | 200 |
| 09:11:33 | https://oeis.org/A387260 | 200 |
| 09:12:44 | https://arxiv.org/abs/2603.01002 | 200 |
| 09:13:08 | https://arxiv.org/pdf/2603.01002v1 | 200 |
| 09:13:35 | https://arxiv.org/a/jehn_r_1 | 303, redirect to .html |
| 09:13:36 | https://export.arxiv.org/api/query?search_query=ti:%22Risk%20or%20Safety%22&max_results=50 | 200 |
| 09:13:37 | https://export.arxiv.org/api/query?search_query=au:Jehn&max_results=50 | 200 |
| 09:13:45 | https://arxiv.org/a/jehn_r_1.html (the redirect target) | 404 |
| 09:14:11 | https://oeis.org/search?q=%22Risk+or+Safety%22&fmt=text | 200 |
| 09:14:12 | https://oeis.org/search?q=1599710761252635467097849938052769718961535662524&fmt=text | 200 |
| 09:14:33 | https://oeis.org/history?seq=A387261 | 200 |
| 09:14:34 | https://oeis.org/history?seq=A387262 | 200 |
| 09:15:08 | https://oeis.org/history?seq=A387261&start=10 | 200 |
| 09:15:28 | https://oeis.org/A394776/b394776.txt | 200 |
| 09:15:29 | https://oeis.org/A387260/b387260.txt | 200 |
| 09:15:38 | gh pr list (open PRs of the repository) | exit 0 |
| 09:16:54 | https://arxiv.org/abs/2604.22991 | 200 |
| 09:17:04 | https://arxiv.org/abs/1808.06707 | 200 |
| 09:17:14 | https://arxiv.org/pdf/1808.06707v1 | 200 |
| 09:18:06 | https://modelai.gettysburg.edu/2012/pig/ | 200 |
| 09:18:35 | http://cs.gettysburg.edu/~tneller/papers/pig.zip | 200 |
| 09:19:42 | https://oeis.org/search?q=piglet&fmt=text | 200 |
| 09:19:43 | https://oeis.org/search?q=2%2C4%2C6%2C2236%2C1026%2C275848876&fmt=text | 200 |
| 09:19:44 | https://oeis.org/search?q=3090007892803332518177914010771390705108642578125&fmt=text | 200 |
| 09:19:57 to 09:21:02 | api.stackexchange.com/2.3 search, 14 queries (section 6) | 200 each |
| 09:21:02 to 09:22:01 | https://woodingben.com/games/pig/ (web-fetch tool) | page returned |
| 09:22:01 | https://arxiv.org/abs/2104.14744 | 200 |
| 09:22:03 to 09:22:26 | gh search code / gh search repos, 7 queries (section 7) | completed |
| 09:22:54, 09:22:58, 09:23:02 | api.semanticscholar.org, 3 queries | 429 each, not retried |
| 09:23:18 to 09:23:37 | api.openalex.org, 6 queries | 200 each |
| 09:23:58 | https://oeis.org/search?q=1%2C3%2C5%2C1929%2C899%2C245296749&fmt=text | 200 |
| 09:24:58 | https://oeis.org/search?q=14364898791782224577113184680141626682&fmt=text | 200 |
| 09:24:59 | https://arxiv.org/abs/2406.14700 | 200 |
| 09:26:09 | https://cs.gettysburg.edu/projects/pig/piglinks.html | 200 |
| 09:26:22 | http://cs.gettysburg.edu/~tneller/papers/pig+.pdf | 200 |
| 09:26:38 | https://modelai.gettysburg.edu/2012/pig/PigletSolver.java | 200 |

context: subagent
pass: true
