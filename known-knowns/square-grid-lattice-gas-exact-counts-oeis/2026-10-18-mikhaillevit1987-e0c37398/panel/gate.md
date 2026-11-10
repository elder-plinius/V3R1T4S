# Honesty gate — square-grid-lattice-gas-exact-counts-oeis, A054759(16)

status: PROMISING
confirmed_scope: Two runs of claim/checker/ice.rs (left-to-right sweep with full symmetry reduction vs right-to-left sweep with shift-only reduction, on disjoint sets of four primes) saved residues whose CRT values agree for every n = 1..16, reproduce the 14 published A054759 terms exactly, and give 2781781827849835218619790131266486746689884618378 for n = 16; this value is consistent with the finite-size trend, but it is not the first unknown term a(15), so it does not meet p1 as literally worded.

Read by the main session on 2026-10-18T11:47Z (UTC).

- novelty.md: pass. Single fetches 2026-10-18 11:45-11:46Z, all HTTP 200; OEIS A054759 DATA/b-file end at a(14); no pending edit; only competing claim is open PR #366 for a(15), which disclaims n >= 16.
- criterion.md: pass: false. p1 reads "the next unknown term(s)"; with OEIS ending at 14, the next unknown term is a(15). Claiming a(16) alone because a(15) sits in an unmerged PR stretches the definition. The gate accepts this: downgrade, never upgrade.
- reproduce.md: pass (run later, 2026-10-18 21:30-22:24 local, at the user's request). Own Rust checker written from the definition, brute force for n=1..3, own primes; two reductions agree on n=1..14 (b-file) and on n=15, 16; a(16) equals the claim; author's ice.rs on fresh primes also agrees. Caveat accepted: the skeptic's sweep is the same broken-profile family as the author's (independent code, not an independent method). The growth-gap remark (6.5e-3 vs the main target's 1e-3) does not apply to p1. Status unchanged: the CRITERION failure stands.
- Path forward recorded for the human: a(16) becomes the literal next unknown term once a(15) is accepted (PR #366 merged or OEIS updated); then rerun CRITERION and REPRODUCE. a(15) is mizopl's by priority (our run is an independent confirmation).
- 2026-10-18 21:48 local: at the user's request, claim/CLAIM.md got a section 'Not claimed' with the a(17) value (two runs, no panel). The skeptics' copies of claim/ predate it; the claimed object is unchanged.
