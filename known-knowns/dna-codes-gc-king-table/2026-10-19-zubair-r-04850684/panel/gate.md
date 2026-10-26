# Honesty gate: run 2026-10-19-1601, claim A_4^GC(10,7,5) >= 44
status: CONFIRMED_SOLUTION
confirmed_scope: The 44 words in object/gc_n10_d7_m44.txt form a length-10 quaternary code with exactly 5 G/C per word, all words distinct, and minimum plain Hamming distance 7, which strictly exceeds the unmarked entry 34^v for A_4^GC(10,7,5) in the GC (non-RC) table of the re-fetched King page [not included in this package; its URL, fetch time and sha256 are recorded in the-record-we-beat/RECORD.md] (re-fetched 2026-10-19T16:38:28Z); post-2010 novelty is not covered.
reasons: REPRODUCE pass, NOVELTY pass, CRITERION pass, each in a fresh subagent context that saw only claim/ (the review folder, not included in this package).
gate checks (downgrade-only):
- Table access audit: the NOVELTY skeptic read the Aboluion 2011 thesis from the repository's portal link (https://pure.southwales.ac.uk/ws/portalfiles/portal/991721/PhD_thesis_Niema.pdf, one plain request, HTTP 200). An earlier skeptic in another claim got HTTP 403 on a different URL (/files/991721/...). No browser user agent, cookie replay or same-URL retry appears in panel/novelty.md. Disclosed here for the human to judge.
- Residual hedge resolved: arXiv 1902.04419v3 (conflict-free DNA codes), fetched by the gate at 2026-10-19T17:05:25Z (HTTP 200, sha256 b8439b99...). Tables I-II (GC plus reverse, reverse-complement and conflict-free constraints, so subsets of GC codes) give 16 at (10,7), below 44. No downgrade.
- Panel table fetch 2026-10-19T16:59:33Z (HTTP 200) is < 6 h old at the gate.
- Documentation defect, not a downgrade: W_CONVENTION_AND_REFETCH.md [not included in this package] section 1 was copied from the (11,8) claim. For n=10, w = n/2 is stated directly by King 2003 Table 2 (checked by CRITERION).

Paths edited after review at the owner's request; verdict unchanged.
