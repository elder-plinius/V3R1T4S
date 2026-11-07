# Honesty gate: physlib-restricted-lorentz-connected (run 2026-10-14-0608)

status: CONFIRMED_SOLUTION
confirmed_scope: Against the local Physlib build at commit be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1, object/RestrictedIsConnected.lean kernel-checks `V3R1T4S.claim : V3R1T4S.spec` using only the axioms propext, Classical.choice and Quot.sound, where `V3R1T4S.spec` is `∀ {d : ℕ}, IsConnected (LorentzGroup.restricted d : Set (LorentzGroup d))` and is structurally identical to the statement of Physlib's `semiformal_result "FXNL5" restricted_isConnected` re-elaborated in its own source context (Physlib's subspace topology on `LorentzGroup d`).

Read by the run's main session at 2026-10-14T07:29Z: reproduce.md, novelty.md and criterion.md, each from a fresh
subagent context that saw only claim/, each ending `pass: true`.

Downgrade checks (kit/RUN.md step 7), none triggered:
- Hedging: none. NOVELTY says its pass covers novelty only and leaves correctness to the other two, which both
  confirm it; its stated limits (no GitHub API, Zulip only through web search, two sites unreachable) are scope
  notes, not conditions.
- Reproduction: REPRODUCE wrote its own statement before opening the object (including the textbook matrix form
  Mᵀ η M = η, det M = 1, M₀₀ ≥ 0), derived it from `V3R1T4S.claim`, ran the checker twice with byte-identical
  output (PASS), replayed the modules with leanchecker, and re-derived every proof step.
- Strictly better than the live record: the status page (fetched again by NOVELTY at 2026-10-14T07:00:56Z, HTTP 200,
  same sha256 e41850ba01879f3a9a6c3934efd85aab5b4a1a48c8d8a4621da63f7c5296f1c9) still has FXNL5 as a
  `semiformal_result`, also at the newer master 5f2136528e887a222a6be6ee5d04a3899450b255; no proof in any of the
  1642 pull request heads, in Mathlib (pinned or master), in TauCeti or in the literature searched. The fetch is
  less than 6 hours old.
- Stretched criterion or hidden quantifier: CRITERION and REPRODUCE each showed the frozen statement is
  structurally identical (Expr equality) to FXNL5 re-elaborated in its own source context, for every d.
- Scope: the confirmed_scope sentence above is CRITERION's, verbatim, and no wider than what REPRODUCE reproduced.
- One object, one statement; no sampling; no evasion.

Process note (not affecting the result): all three noted that CLAIM.md names the source copy's folder as data/ on
one line while it is in source/ (same sha256).
