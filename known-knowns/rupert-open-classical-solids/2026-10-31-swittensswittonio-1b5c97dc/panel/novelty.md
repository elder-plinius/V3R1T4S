# NOVELTY panel (partial win p3, rupert-open-classical-solids)

context: subagent (NOVELTY skeptic, fresh, read-only on the claim package and repo clone)
injection_suspected: none

## Status source (fetched once, no retry)
- URL: https://en.wikipedia.org/wiki/Prince_Rupert%27s_cube
- Fetched 2026-10-31 12:25:36 UTC (`date -u`), HTTP 200, 242061 bytes, sha256 df13564bc42baaf790b88dcef12d1038603ecc2bc6f9c89ca79c10803e67b475 (identical to scout_record.md); "last edited on 29 September 2026, at 00:29 (UTC)".
- Value: page lists J72-J75, J77, deltoidal and pentagonal hexecontahedra (and snubs) as Rupert-unknown; it never mentions Hervay or the rhombicosidodecahedron certificate. So the status table says nothing for or against p3 itself; p3 is a verification task on Hervay's certificate, not a table cell.
- (A first fetch at 12:23:20 UTC returned the same HTTP 200/242061 bytes; I discarded its file because /tmp is shared with other agents and had been overwritten, then refetched to a private file.)

## Primary object and errata
- Zenodo https://zenodo.org/records/23013945 (fetched 12:24 UTC): "Non-Rupertness of the Rhombicosidodecahedron", published September 28, 2026, Version v1, status `published`, one version, no erratum/withdrawal/related notice (API `related_identifiers` empty, updated 2026-09-28T14:17Z).
- GitHub bence-hervay/nopert-rid: 2 commits (1efe1501 v1 proof 2026-09-28T14:13Z; 802a3ded arXiv format 2026-09-28T16:43Z = the pinned commit, latest), 0 issues, 0 PRs, 0 tags/releases, 0 forks (API, 12:24 UTC). README says Rust prover + Python audit, records 192,696, sha256 df1f8dbab68b561f22fa9daeca48153d71bde7b6fba3345d9f6b7b8077df4b5f.
- arXiv API query (rhombicosidodecahedron AND Rupert; author Hervay): no entries (the audit README also says "arXiv article: pending"). Nothing to retract.

## Prior re-verifications / audits found (last 24 months, GitHub search, gh code search, web search)
1. davidryan59/rid-nopert-audit (created 2026-10-08, last push 2026-10-09; Python; https://github.com/davidryan59/rid-nopert-audit). What it does: runs Hervay's own Rust `rid check` and Hervay's own Python audit on commit 802a3ded (all 192,696 records accepted by THOSE tools), regenerates the certificate byte-for-byte with Hervay's Rust search, and adds `clean-room-v2/checker.py`: a stdlib-Python, spec-mediated checker of the 38 serialized cover files only (11,231 terminal leaves: 11,183 witness + 48 delegated; 357,856 corner evaluations). Its README: "A specification-mediated clean-room verification independently passed all 38 serialized cover files." The independent code is Python (not allowed by p3's "neither Rust nor Python"), and it does not independently re-check the 192,696 records; the record check there is Hervay's Rust+Python. => does not preempt p3. It also provides a neutral `rid-cover/1` spec "for a second clean-room checker" (the claim's C# was written from Hervay's article and data, per CLAIM.md; the claim's independence from this spec is for the reproduce skeptic).
2. oscardssmith/Nopert.jl (created 2026-09-26, before Hervay; Julia search + Lean 4 `native_decide` proof `rhombicosidodecahedron_nonRupert`; https://github.com/oscardssmith/Nopert.jl). Own, different certificate: 91,845 leaves in four trees + 18 blow-up certificates, Lean/Mathlib checker (`checkMain`). Does not read or verify Hervay's search.cert / 192,696 records. It is a rival proof, not a re-verification of this certificate. => does not preempt p3. Caveat for the record: a Lean-checked proof of the same theorem exists, so the theorem is not novel; p3 asks only for re-verification of Hervay's certificate.
3. tom7/noperts (Lean + C++, 2026-10-09; https://github.com/tom7/noperts): formal Lean verifications for snub dodecahedron, pentagonal/deltoidal hexecontahedron, snub cube, nopert231, Septopert; its README only cites Nopert.jl and nopert-rid for the RID ("claimed proofs or verifications"). No RID re-verification. Other hits (dwrensha/NopertTriakisTetrahedron, badly-drawn-wizards/noperthedron, ejgallego/verso-noperthedron, tomhannen) are about other solids.
4. GitHub repo search ("nopert", "noperthedron", "rupert", "rhombicosidodecahedron nopert", "192696") and code search ("nopert-rid", "search.cert rhombicosidodecahedron"): only the above plus this V3R1T4S repo's own known-unknowns pages. Web search (two queries, after 2026-09-28): Zenodo, MathWorld (Hervay cited), tom7/noperts, no C#/Java/JS/Go/Julia/C++/Haskell verifier of this certificate. Absence in search is not proof of absence, but nothing preempting was found.

## This repo (V3R1T4S, read-only)
- TROPHY_CASE.md: no match for rupert/nopert/hervay/rhombicos. known-knowns/: no match. Only matches: bank/targets.json and known-unknowns/recreational-math/{rupert-open-classical-solids,fewest-vertex-non-rupert-polyhedron,README}.md (the target itself; p3 wording identical to CLAIM.md).
- `gh pr list -R elder-plinius/V3R1T4S --state all --search` for rupert, nopert, Hervay, rhombicosidodecahedron, RID, re-verif: all `[]`. (C# search returned unrelated PRs only.) No open/closed PR for this target.

## Triviality check
p3 is a verification deliverable, so "trivial edits of a published object" does not bite as for a record; the question is whether a published artifact already does exactly this. The closest ones (rid-nopert-audit Python cover checker; Nopert.jl Lean with its own cert) differ on language (Python), scope (cover only; no independent record check), or object (different certificate). Nothing published re-checks all 192,696 of Hervay's records with independent non-Rust/non-Python exact code, so a correct C# result would be the first.

## Caveats (not blockers for novelty)
- Novelty only; correctness, independence of the C# author from Hervay's code and from the audit's spec, and the actual 192,696/11,231/711 numbers belong to the Reproduce and Criterion panels.
- Possible later preemption after 2026-10-31 is not excluded; searches were run 12:23-12:25 UTC.

pass: true
