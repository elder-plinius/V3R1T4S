# NOVELTY verdict: hsp4-N216

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:21Z

## Value computed here
- Claim object `claim/hsp4_N216.txt`: sha256 bacd6f0e…e968 (matches CLAIM.md); 216 centres, 4 coordinates each (comment lines ignored).
- r* (mpmath, 50 digits, own code `work/common.py`, `work/c12.py`) = 0.20362333097990599275220577366244339625411531997264
  (binding term: 1 - max|c_i| = 0.2036233309799059927522…; half min distance = 0.2036233309799060304522…).
- Live table row (evidence/hsp4_radius_live.txt, line 215): `216 0.203582040585`. r* - table = 4.1290394906e-5.
- The evidence files were fetched by the repository owner from an unrestricted machine on 2026-11-01T14:32Z; I treat them as the live re-fetch for this panel. I recomputed sha256 of every file listed in FETCHED.md and all match. The copy of hsp4-216.txt extracted from hsp4_coords.tar.gz is byte-identical (sha256 f3969495…a410) to evidence/posted/hsp4-216.txt.
- No injection_suspected: the claim file's comment lines state values, which I ignored and recomputed (they agree with mine).

## Clauses checked
- 1 Value: r* = 0.203623330979905992752205773662…; r* - 0.203582040585 = 4.129e-5 >= 1e-10. PASS.
- 2 Parser sanity: posted hsp4-216.txt recomputed the same way = 0.2035820405845065555764600748; header 0.203582040585 (= table row); difference -4.93e-13, within 1e-11. Clauses 3 and 4 apply. PASS.
- 3 Non-isometry: 23220 pairwise distances each; max |sorted claim - sorted posted| = 7.89e-3 > 1e-8. (Info: sorted centre norms differ by up to 0.246.) PASS.
- 4 Polish floor: my own sequential-LP polisher (`work/polish.py`, HiGHS; near-active pairs within 2r+margin+2Δ and centres with |c|>1-r-margin-Δ; maximize linearized radius under box trust region Δ on every coordinate; accept only if the exactly recomputed radius increases, else shrink Δ), started from the posted coordinates. Final radii recomputed at 50 digits from the polished coordinates:
  - s2: Δmax 1e-2, margin 1e-2, shrink 0.5: 0.2035820564527032840, gain over header +1.58677e-8, 94 iters, stop: no gain >1e-15 over 20 iters (Δ<1e-9).
  - s3: Δmax 1e-3, margin 1e-3, shrink 0.5: 0.2035820564526811230, gain +1.58677e-8, 83 iters, same stop.
  - s3b: Δmax 1e-3, margin 5e-3, shrink 0.3: 0.2035820563984392831, gain +1.58134e-8, 104 iters, stop: trust region < 1e-13.
  - s4: Δmax 1e-4, margin 1e-3, shrink 0.5: 0.2035820564526262270, gain +1.58676e-8, 79 iters, no-gain stop.
  - s5: Δmax 1e-5, margin 1e-4, shrink 0.7: 0.2035820564527321696, gain +1.58677e-8, 158 iters, no-gain stop.
  Highest polished = 0.20358205645273217; r* - highest = 4.1275e-5 >= 1e-9. (The polish gain ~1.6e-8 is an errata-scale note for the table keeper only.) PASS.
- 5 Not a relaxed copy: claimant states lane hsp4-b never had posted coordinates; seeds random / two-shell / D4-lattice cuts, N=214..217 grown from its own N-1 packing plus one inserted ball; names no posted packing as a start. I do not have the claimant's search code and cannot verify the narrative directly. My own evidence: contact graphs differ (claim at tol 1e-9: 666 ball-ball contacts, 188 boundary centres, 28 interior, degree histogram [1,0,0,0,2,18,56,60,51,23,4,1]; posted: 663 contacts, 185 boundary, degree histogram [2,0,0,0,1,24,42,76,42,23,6]); sorted distance multisets differ by 7.9e-3 and sorted norms by 0.246; all five polishes of the posted file plateau at ~0.2035820565, 4.1e-5 below r*, and the polished posted packing still differs from the claim by 7.9e-3 in sorted distances. Nothing indicates derivation from a posted packing. PASS.
- 6 History of updates: hsp4.html "Last update: 06-Jul-2025"; History entries 04-Jul-2025 (N=2-100), 05-Jul-2025 (to N=200), 06-Jul-2025 (extension to N=300, covers N=216); no entry newer than the table snapshot (whose row 216 = 0.203582040585 matches radius.txt). PASS.
- 7 Queue rule: pending.html (30-Oct-2026) lists ranges only for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp; no hsp4 range, and none labelled hsp/hyperspheres; N=216 lies in no hsp4 range. CAVEAT (required): the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; N=216 must be re-checked against the live hsp4 table once that bundle disappears from the pending list. PASS (subject to that caveat).
- 8 Moki & Julio MANIFEST: row `hsp4,216,0.203582040585,0.2035821276819616514336772,4.278224e-07,REFINEMENT,dp`; published_radius 0.203582040585, new_radius 0.20358212768196165; r* - new_radius = 4.1203e-5 >= 1e-10. Only one hsp4 row has N=216; no other row has a radius in 0.2035-0.2037 except hsp4 N=215 (new_radius 0.20368299878, which is for N=215, a different cell); other N=216 rows are other shelves (ccq, crc_*, crt, csc, hsp5, hsp6, ssp) with unrelated radii. PASS.
- 9 Other prior work: claims list for packomania-hyperspheres-hsp4-hsp6 has hsp4 claims for N = 30,35,42,48,54,62,63,64,66,67,69,74,75,79,80,81,83,88,89,91,94,104,111,119,170,301 — none for N=216 (open, closed or merged); spherical-codes claims list has no hsp4 N=216 entry; TROPHY_CASE.md has no hsp4 N=216 entry. Spherical-code constructions from spherical_plain_live.txt: (4,216) c = 0.880886649220 gives s/(2+s) = 0.196168853249 (r* exceeds by 7.45e-3); (4,215) c = 0.880272662054 with centre ball gives min(1/3, 0.196574535420) = 0.196574535420 (r* exceeds by 7.05e-3). Both below r*. PASS.

## Decision
All nine clauses pass on numbers computed here. On prior work specifically: Packomania's hsp4 page has had no update since 06-Jul-2025 and no History entry newer than the table snapshot names N=216; the pending-requests list has no hsp4 range (with the unresolvable 'Moki & Julio *many* 4666 candidates' caveat stated above); the Moki & Julio manifest's hsp4 N=216 refinement (0.2035821277) is 4.12e-5 below r*; no claim PR or trophy entry covers hsp4 N=216; and the spherical-code constructions fall ~7e-3 short. The claimed packing (r* = 0.2036233310) is structurally distinct from the posted one and beats every polish of the posted file I ran by 4.13e-5. I accept the claim as novel, subject to re-checking N=216 against the live table once the Moki & Julio 4666-candidate bundle leaves the pending list.

pass: true
