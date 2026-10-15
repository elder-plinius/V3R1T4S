# Novelty skeptic verdict: three-player-von-neumann-poker-equilibrium (p1 / b=2)

Question: has any earlier published or posted work already proved (or refuted) that the
Krityakierne-Thanatipanonda-Zeilberger (KTZ) threshold profile, Eq. A-C, is a Nash equilibrium of the
three-player game of arXiv:2407.16155 Section 4 (each antes 1, uniform(0,1) hands; I checks -> immediate
showdown, or bets b; II and III then call or fold simultaneously without seeing each other), for b=2 or all b>0?

## 1. Status fetch (one request, not retried)
- URL: https://arxiv.org/abs/2407.16155
- UTC: request started 2026-10-15T19:32:01Z, completed 19:32:02Z
- HTTP 200, 39297 bytes, sha256 935ab43fa878785c5c6725b2dad2dfc4999318482d1af608805566ab951ef83b
  (identical to the hash in claim/STATUS_RECORD.md and claim/SOURCE_AUDIT.md)
- Read: title "von Neumann and Newman Pokers with Finite Decks", authors Krityakierne, Thanatipanonda, Zeilberger;
  submission history lists only [v1] Tue, 23 Jul 2024 03:51:30 UTC. No later arXiv version, no erratum,
  no comment saying the three-player equilibrium has been proved.
- Status value: the three-player continuous profile is labelled "Conjectured Nash equilibrium strategies"
  (v1 HTML, claim/data/paper.txt, Fig. 2 caption and Section 4 text). The refereed journal version
  (Math. Intelligencer 47, 314-322, Dec 2025; claim/data/journal.txt, Figure 6 caption) and the author's
  Version 2 (claim/data/version2.txt, Fig. 5) still say "conjectured", and both state that "the dynamics of this
  three-player game remain unexplored". The journal version derives only the cut-point indifference
  equations. It does not check every action sign against all deviations.

## 2. Literature search (each request made once; blocks recorded, never retried)
| search | time (UTC) | result |
|---|---|---|
| arXiv search "poker three", newest first, 50 per page | 19:35:23 | HTTP 200, sha256 56df07cf...54ea3, 38 hits. The only matching paper is 2407.16155 itself. Nearby hits are a different game or not a proof: three-player Kuhn poker (Billingham 1704.08124, 1707.01392, 1802.04670; 2606.29169, 2606.25997, 2509.25618 compute equilibria for finite Kuhn variants), 2412.19855 (continuous Guts poker, simultaneous in/out declarations, coalitions), and LLM or poker-AI papers. |
| Semantic Scholar citations of ARXIV:2407.16155 | 19:33:14 | HTTP 200, data: [] (no citing works) |
| OpenAlex record for DOI 10.1007/s00283-025-10420-2 | 19:33:14 | HTTP 200, W4410429559, cited_by_count 1 |
| OpenAlex list of works citing W4410429559 | 19:33:26 | **HTTP 429 (rate limit), not retried.** The package's earlier copy of this query (claim/data/openalex-citations.json) lists only the work itself, i.e. its arXiv twin. |
| zbMATH Open, ti:poker & ti:three | 19:33:54 | HTTP 200, sha256 d926acae...c4c2, 8 records: Nash-Shapley 1950; Billingham 2017 (two papers); Barany-Furedi 1983 (mental poker); Sakaguchi-Sakai 1992; Sakai 1984 (three-person Hi-Lo); Simelis 1977/1978 |
| zbMATH Open, ti:poker & au:Sakaguchi | 19:34:46 | **HTTP 502, not retried** |
| zbMATH Open, ti:poker & py:2024-2026 | 19:34:46 | HTTP 200, 7 records, none on equilibria of a three-player betting game |
| web searches (Sakaguchi-Sakai title; KTZ three-player proof; "three-person poker" continuous 2025-2026; works citing KTZ; Brown 2026 title) | 19:32-19:37 | Turned up no proof, refutation, or follow-up on the KTZ three-player profile. The Sakaguchi-Sakai paper appears only as a citation in Billings et al. (IJCAI 2003). |

### Candidate prior works
- **Nash-Shapley 1950** (Ann. Math. Stud. 24). The zbMATH review and the KTZ description agree that it uses a deck of
  only two card kinds (High/Low). It is a different, discrete game. It does not settle this question.
- **Simelis 1977** (Lith. Math. J. 17, 572-579; DOI 10.1007/BF00972283). I read the public first-pages preview
  (claim/data/simelis-1977-page-one-preview.pdf; I recomputed its sha256 as ecfb0022...5f00d, which matches
  claim/PRIOR_ART_SOURCES.md). I did not refetch it.
  Rules (p. 572): "the first player proceeds: he can either pass, thus losing the initial unit bet, or bet another
  α > 0 units. In any case the second player has the same alternatives. If the first and second players pass, then
  the third player wins the pot. But if at least one bet is made, then the third player has the choice". The players'
  strategies depend on history: II has the pair (g1, g2) according to whether I bet or passed, and III has (h1, h2, h3)
  for "bet, bet", "bet, pass" and "pass, bet" (p. 573). This is a sequential bet-or-fold game in which later players observe
  earlier moves. Passing forfeits the ante, and densities are general. In KTZ, I's alternative is a check that goes
  straight to showdown, and II and III call simultaneously without observation. **Different game. It does not settle the question.**
- **Sakaguchi-Sakai 1992**, "Solutions of some three-person stud and draw poker", Math. Japonica 37(6) 1147-1160
  (zbMATH 0770.90100). The full text is unavailable. The zbMATH summary reads: "Three kinds of three-person poker: (1)
  High-Hand-Wins, (2) La Relance and (3) Le Her poker ... (1) and (3) are the simultaneous-move stud and draw pokers,
  respectively, and (2) is the trilateral-move stud poker ... in (2) the first mover makes bluff and the second and
  third movers do not for any amount of bet." (1) is an all-players-simultaneous model with no first mover. (3) is a
  draw (Le Her) game. (2) is La Relance, Borel's game, in which a player who does not bet folds rather than checks to showdown.
  It is also "trilateral-move", with ordered second and third movers who themselves may bluff, so they have betting
  options. None of the three is a check-or-bet first mover followed by two simultaneous call/fold responders. On the
  published summary, this paper is a different game. It is not counted as a gap.
- **Sakai 1984**, three-person Hi-Lo poker. An alternating-move Hi-Lo payoff model. Different game.
- **Brown 2026** (SSRN 6709840), "Value, Bluff, and Cyclic Dominance: Completing the Von Neumann Poker Project".
  The earlier run's single request got HTTP 403 (claim/SOURCE_AUDIT.md); I did not request the page again. The saved search
  snippet (claim/data/web-history-search.json) describes "a model of two-player poker" and relaxing "scalar hand
  strength, deterministic outcomes, and fixed bet size". That is heads-up, with nothing on three players. Different game.
- **Ferguson-Ferguson-Gawargy** (claim/data/ferguson-poker.txt) treat two-person uniform(0,1) extensions only.
- **KTZ themselves** (arXiv v1, author Version 2, journal 2025) only conjecture the profile and derive the indifference
  equations. They do not prove it.

## 3. Kit trophy case and open pull requests
- Pinned TROPHY_CASE.md: no entry mentions poker, von Neumann, or this target. known-knowns/ holds six unrelated
  families (graphs, codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench).
- `GET https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=50` at 19:33:14Z: HTTP 200,
  sha256 c38af6f9...af2fc, 9 open PRs (#194, 193, 192, 191, 190, 154, 153, 30, 9). None concerns
  three-player-von-neumann-poker-equilibrium or "von Neumann". #192 is a different target (all-in three-player ruin).
  Since there were fewer than 50, no second page was needed.

## Verdict
The status page is readable and still shows only v1, with the profile labelled as conjectured. The refereed 2025
version still calls it conjectured. Within the past 24 months I found no citing work, posting, or open PR that
proves or refutes it. Every classical three-person poker model I located (Nash-Shapley 1950, Simelis 1977,
Sakai 1984, Sakaguchi-Sakai 1992) has a different game structure. None of them has KTZ's check-to-showdown first
mover followed by two simultaneous, non-observing callers. On novelty, a proof that the KTZ profile is a Nash
equilibrium is therefore not already known.

Limits: Sakaguchi-Sakai 1992 was judged from its zbMATH summary, not its full text. One OpenAlex citation request
(429) and one zbMATH request (502) were blocked and not retried. This verdict covers novelty only. It does not cover
correctness, or whether the stated b=2 value matches the printed 0.122557074714865. That mismatch is for the other skeptics.

context: Claude Code Agent subagent (Opus), fresh context, saw only claim/
pass: true
