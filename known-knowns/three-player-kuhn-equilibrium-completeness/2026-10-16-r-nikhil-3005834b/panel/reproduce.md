# Independent REPRODUCE verdict

context: codex exec (fresh context via codex-fresh)

Confirmed direction B. Every Nash equilibrium of the specified game agrees
at all reached information sets with a member of Tables 2–3. I found no
mathematical mismatch, missing proof object, or nondeterministic mathematical
output. All file names below are relative to `claim/`.

I read `target.md`, `CLAIM.md`, and the saved definition in
`data/original.txt` before reading author code. Section 2 states:
“Three-player Kuhn poker [1] is played with a deck of 4 cards, denoted 1, 2, 3
and 4. To begin, each player must ante one chip into the pot so that the
players have incentive to play.” It further states: “The final case is where
neither P1 nor P2 bet, but P3 bet. In this case, both P1 and P2 can fold or
call in order and then the showdown takes place.” The remaining rules are
quoted and implemented in `independent_reproduce.py`, which I wrote before
inspecting author code.

The independent tree enumerates all 24 deals and 13 terminal histories per
deal. Exact symbolic checks verify probability conservation, zero-sum utility,
and the 48 information sets. The three rational family calibrations exhaust
each player's pure best responses by factoring 65,536 strategies into four
independent sets of 16 card-specific plans. Those calibrations are only spot
checks; the passing verdict rests on the universal certificate below.

`independent_certificate.py` imports no author code. It reconstructs the
realization game from the independent behavioral tree and verifies equality
of all 312 leaf polynomials under coordinate conversion. It checks every
certificate event with exact rational polynomial arithmetic and independently
justified feasible-deviation rules:

| Saved certificate in `attempts/solver/output/` | Events checked |
| --- | ---: |
| `no_initial_bet_certificate.json` | 759 |
| `normalization_preconditions.json` | 733 |
| `normalization_dominance.json` | 75 |
| `restricted_family_certificate.json` | 634 |
| `terminal_family_certificate.json` | 40 |
| Total | 2,241 |

The full-game proof closes the positive-opening branch and proves all four
P1 opening probabilities zero on the complementary branch. The normalization
maps preserve feasibility and act only on their owner's coordinates. Its
three dominance polynomials use domain facts for arbitrary deviations, with
certified opponent equalities. Zero-sum Nash inequalities then prove that the
normalized profile remains a restricted equilibrium with identical payoffs.

The restricted certificate proves beta=max(b11,b21) in [0,1/4] and the exact
payoff vector

    (-(1+2*beta)/48, -1/48, (1+beta)/24).

The three family cases are exhaustive: c11=0, c11=1/2, or 0<c11<1/2.
I re-derived their bounds from Tables 2–3, including the positive denominator
1-b21>=3/4 in the behavioral conversion. The explicit 48-coordinate symbolic
family representative is saved in `independent_family_map.json`.

All 312 joint deal/history identities are checked against a complete expected
key set. No terminal leaf is sampled or omitted. Another 96 symbolic
identities establish that each information set's action-cylinder mass equals
its action probability times its reach. Dividing at positive reach proves
the claimed on-path agreement. The full proof, including the justification
of every inference-rule type and each composition step, is in
`independent_proof.md`.

Evidence: `independent_game.json`, `independent_output.json`,
`independent_certificate_output.json`, `independent_proof_trace.json`, and
`independent_certificate_run.log`. The definition-only output deliberately
does not claim universal completeness; the certificate output supplies that
conclusion. Input hashes are recorded in the certificate output.

`independent_validation.py` rejects eight damaged certificates, including a
missing or duplicate terminal, omitted cases, a changed coefficient, an
invalid domain sign, an unclosed branch, and a Nash premise improperly added
to arbitrary-deviation dominance. Results are saved in
`independent_validation_output.json`.

`independent_determinism.py` runs the complete checker sequentially with hash
seeds 0 and 9137. Mathematical stdout, certificate output, proof trace, and
family map are byte-identical; hashes are in
`independent_determinism_output.json`. The certificate-output SHA-256 is
`b63093ec234fabeac534a0557fef3a6107117c7a75f493ee6887f54ce0e12908`.

No delegation, installations, external messaging, or other reviewers' material
was used. Computation uses one Python thread, with numerical-library thread
limits set to one. The complete deterministic runs peaked at 31,571,968 and
28,655,616 resident bytes. The operating system rejected hard memory-limit
changes; the checker monitors resident usage during polynomial operations,
and observed usage remained far below 1.5 GB. Resource measurements are
recorded separately from deterministic mathematical output.

pass: true
