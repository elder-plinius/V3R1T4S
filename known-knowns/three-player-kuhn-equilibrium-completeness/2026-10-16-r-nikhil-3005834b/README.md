# 2026-10-16-r-nikhil-3005834b: three-player Kuhn poker: every Nash equilibrium agrees on its path of play with the Szafron–Gibson–Sturtevant family

> **Status: PROMISING, submitted by the human's decision. This is not a kit-confirmed claim.** REPRODUCE and CRITERION
> passed in fresh contexts, and the status source was checked by hand by the human. NOVELTY returned pass: false
> because it could not read one source, E. Prisner, *Game Theory Through Examples* (MAA, 2014), chapter "Example: VNM
> POKER and KUHN POKER", pp. 185–192, doi:10.5948/9781614441151.026. The submitter could not access it either. The
> submitter judges that chapter to treat two-player (heads-up) Kuhn poker models only, as the book's other Kuhn chapter
> does, and therefore not to contain this three-player result, but has not read it. For that reason
> `kit/check_run.py --package` does not pass on this folder: its gate.md honestly says PROMISING. The research lane and
> all three skeptics ran on OpenAI Codex (gpt-6-astra), so no second model family has reviewed it.

## What

Every behavioral Nash equilibrium of the three-player Kuhn poker game defined in Section 2 of Szafron, Gibson and Sturtevant (2013) agrees at every information set it reaches with positive probability with some member of their Tables 2–3 family.

## Check it yourself

`sh verify-it-yourself/run_checks.sh` (from this folder). Expected last line: `PASS`, after `FULL_GAME_COMPLETENESS: PASS`.
Under a second on a laptop, Python 3.9+ standard library only, no network, no solver, no floating point. Do not run
Python with `-O`: the checkers reject disabled assertions. Details: `RUN_IT_YOURSELF.md`.

## Compared to

| source | statement | fetched / checked |
|---|---|---|
| Szafron, Gibson, Sturtevant, "A Parameterized Family of Equilibrium Profiles for Three-Player Kuhn Poker", AAMAS 2013 | the Tables 2–3 family; whether it contains every Nash equilibrium is left open | the paper (copy not included) |
| https://en.wikipedia.org/wiki/Kuhn_poker (status source; last edited 10 July 2026) | "It is not known if this equilibrium family covers all Nash equilibria for the game." | checked by hand by the human on 2026-10-15 after the skeptic's fetch returned HTTP 403 (`panel/status_by_hand.md`) |
| Crossref, OpenAIRE, arXiv searches (last 24 months), this repository's TROPHY_CASE.md and open PRs | no earlier proof found | `panel/novelty.md` |

## What the proof is

Five exact certificates in `object/`: no initial bet by player 1 in any Nash equilibrium (`no_initial_bet_certificate.json`);
normalisation preconditions and dominance identities that reduce the game's 48 behavioural probabilities to a
32-coordinate normal form (`normalization_preconditions.json`, `normalization_dominance.json`); the 18-coordinate
restricted family (`restricted_family_certificate.json`); and the terminal-history law over all 24 ordered deals and 13
terminal histories (`terminal_family_certificate.json`). The checker in `verify-it-yourself/` reads only these files and
verifies every rational polynomial identity and every sign premise. Proof notes: `how-we-built-it/NORMALIZATION_PROOF.md`,
`how-we-built-it/TERMINAL_LAW.md`.

## Not claimed

- Not a statement about off-path behaviour: equilibria are compared at information sets reached with positive probability.
- Not a proof-assistant formalisation and not peer reviewed.
- Not kit-confirmed: see the status box above.

## Credits

Harold W. Kuhn (the game); Nick Abou Risk and Duane Szafron (the three-player variant); Duane Szafron, Richard Gibson and
Nathan Sturtevant (the equilibrium family and the open question). Proof and checkers written by a V3R1T4S research lane
on OpenAI Codex (gpt-6-astra).
