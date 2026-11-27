# Honesty gate (kit/RUN.md step 7): run 2026-11-25-0045-mertens, Mertens target, bank partial win p4 (claim/)

gated: Wed Nov 25 08:01:55 UTC 2026 (date -u) by the run's executor, after reading all three panel files in full (not edited).
panel files read (sha256): reproduce.md b7af7ce69f388d444b517f15e520d379704f7302774c827636cdb40e9f5b852b, novelty.md ae5c9dfdd1c5f81ccca53b4e0c1119b4cef34da7461bbdc2b4fe287ab0a42740, criterion.md 483627d0c835aee5ea4e317f06d333899b983435c753edb8845761dee08509c1
panel: REPRODUCE pass: true, NOVELTY pass: true, CRITERION pass: true (with confirmed_scope). Three fresh-context knowledgeWork skeptics (sandboxes panel-0045-reproduce, panel-0045-novelty, panel-0045-criterion), launched by the parent session; each saw only a copy of claim/ and kit/RULES.md. Panel files kept exactly as written.
prereg: sha256sum -c PREREG.sha256: PREREG.md OK (unchanged). PREREG outcome class: CONFIRMS-NUMERICS.

## Why p4 is confirmed (from the panel files, judged literally)
- REPRODUCE wrote its own checker before reading the author's code and computed all 2,325,573 zeros itself (acb.zeta_zeros, 160/128/96 bits, exact rational k and v), summed all 2,325,572 terms (no sampling), and got K2 = [1.00030525038651186516826 +/- 3.73e-24], contained in the author's ball [1.00030525038651 +/- 5.07e-15] and in the certificate's [1.0003052504 +/- 2.30e-11]; independent count arb(1300000).zeta_nzeros() = 2325572; 0 of 1,163 block comparisons fail to overlap; determinism checks pass. Caveat (stated by all three panelists): the zeros come from the same Arb routine the certificate uses, so this is an independent computation with separately written code, not an independent zero source.
- NOVELTY fetched the status source once (2026-11-25T04:39:06Z, HTTP 200; still Kim-Nguyen exp(1.96e19)) and found no public independent full K_2 recomputation at the bzyzz point (arXiv, HAL, Zenodo, GitHub, this repo's TROPHY_CASE, known-knowns and all 1,189 PRs); PR #1234 is a different partial win (p1) with no overlap. Non-blocking fixes: Gallego wording, links for Pintz / Saouter-te Riele / FLINT, the same-Arb caveat.
- CRITERION: p4's first option is met (separately written code; all zeros below 1.3e6 with count and boundary; ball arithmetic; comparison with the certificate; "confirms it"). E = 2.391e-11 is the certificate's own value and is unchecked here; Pintz Theorem A / Corollary A as used, Lemmas 4-5, J1..J6 and M remain unchecked. Required wording fixes 1-5 (and optional 6) were applied to claim/ after this gate without changing any number (claim/CHANGES.md).

## Downgrade checks (kit/RUN.md step 7), each judged literally
- hedging panelist: none; all three verdicts are unconditional passes. The listed fixes are wording, not hedges on the verdict.
- reproduction mismatch: none (REPRODUCE's 3.7e-24 ball lies inside the claim's ball).
- value not strictly better than the live table: p4 is a verification partial, not a tighter bound; the status source still cites Kim-Nguyen. NOVELTY's fetch (04:39:06Z) is 3.4 h old at gating (under 6 h); no refetch.
- stretched criterion / hidden quantifier: no; only p4's first option is claimed, at the certificate's stated E, with the rest of the bzyzz proof explicitly unchecked.
- scope wider than reproduced: no; confirmed_scope below is the CRITERION sentence verbatim.
- sample presented as complete: no; the sum covers every zero below 1.3e6, reproduced in full by REPRODUCE.
- table value by evasion: none (single plain fetches).
- several objects bundled: no; one K_2 enclosure at one point.
- same-cell overlap: no prior trophy or PR on p4; #1234 is p1.

status: CONFIRMED_PARTIAL
partial_win: p4 (independent ball-arithmetic K_2 sum of the bzyzz/mertens_bound certificate over all zeros below 1.3e6; outcome CONFIRMS-NUMERICS)
confirmed_scope: With separately written python-flint/Arb ball-arithmetic code, the K_2 sum of the bzyzz/mertens_bound certificate at v = 3484971332733132396.5383341489440461, k = 1.5e-10, over all 2,325,572 zeta zeros with 0 < gamma < 1.3e6 (zeros from Arb's acb_dirichlet_zeta_zeros, which the certificate also uses) is enclosed in [1.00030525038651 +- 5.07e-15]; this ball lies inside the certificate's K2 ball [1.0003052504 +- 2.30e-11] and exceeds 1 + E by 3.0525e-4 at the certificate's own, here unchecked, E = 2.391e-11, which confirms the certificate's K_2 inequality and finds no error in it, while Pintz Theorem A/Corollary A as used, Pintz Lemmas 4-5, J1..J6 (hence E) and the 1/zeta constant M remain unchecked.
stands_only_if: python3 repo/kit/check_run.py prints CHECK_RUN: PASS for the run and for the package; otherwise the status is PROMISING.
