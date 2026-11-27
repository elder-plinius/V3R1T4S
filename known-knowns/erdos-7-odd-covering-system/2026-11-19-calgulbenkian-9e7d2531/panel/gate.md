# Honesty gate (erdos-7-odd-covering-system)

status: CONFIRMED_PARTIAL
confirmed_scope: Assuming the prose proof's Lemmas 1-5 are sound (I found no error), no covering of Z by distinct odd moduli greater than 1 has lcm L at most 168,131,152,814,624, so L is at least 168,131,152,814,625, which is strictly above 11,486,475. All 7036 band profiles are refuted by exact rational certificates that two package verifiers and my own re-implementation reproduce.

## Gate notes
- Object: object/lcm_lower_bound_certificate.tsv, sha256 9e7d2531a58c0a8bd865aca01cc3b511e4d26941708a1e0a4f4db717298d67be.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- The REPRODUCE skeptic re-derived the proof chain and wrote its own exact checker before reading the package: 30,147 abundant profiles, 7,036 band profiles, 2,519 refuted by pure deletion and the remaining 4,517 matching the certificate rows exactly, all below 1; a null model (the covering of Z/12 with moduli 2, 3, 4, 6, 12) is not ruled out.
- Novelty history, in full: the first NOVELTY review failed only because its single fetch of the status page was refused (HTTP 403); the operator then read erdosproblems.com/7 and its forum thread in his own browser (record: panel/status_check_by_hand.md); a second review did not pass because it had not read Schroeder's preprint or the Lean repository in full; a third review read both in full and passed (novelty.md).
- The novelty reviewer's caveat: every lemma here has a counterpart in Schroeder (Zenodo 10.5281/zenodo.22759614) or the Lean repository rw762-sketch/Open-Math-problem; the new part is their combination and the exhaustive per-profile certificate up to the bound, which neither source's method reaches (each says where it stops). The proof is a written argument checked by two skeptics, not machine-checked.
- Added 2026-11-19 after filing: a Lean 4 formalisation of the whole result (`lean/`, Lean v4.36.0, Mathlib v4.36.0). Built from clean by the orchestrating session in a separate copy: the build succeeds, and `#print axioms` on `odd_covering_lcm_lower_bound` shows only propext, Classical.choice and Quot.sound. The sources were scanned for `sorry`, `native_decide`, `axiom`, `extern` and `implemented_by`, with none found. The panel reports above predate this addition and review the prose proof and the certificates.
