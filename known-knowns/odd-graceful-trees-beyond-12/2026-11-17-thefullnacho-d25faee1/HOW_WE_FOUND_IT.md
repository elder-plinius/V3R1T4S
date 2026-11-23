# How we found it (contributor text, unverified)

The brief: Gnanajothi conjectured that every tree is odd-graceful and proved it up to 10 vertices;
Barrientos extended the exhaustive check to 12, and Gallian's survey (29th ed., 6 November 2026,
Section 3.6) still gives 12. The bank's success criterion (a) asks for a certificate up to 22. Draft
pull request #1007 later claimed that target; we did not take files from it.

A direct odd-graceful backtracker (og_direct: force the largest odd difference 2q-1 onto an edge as
labels 0 and 2q-1, then assign unused odd differences largest-first, with a node cap and a restart
search on the leftovers) labelled every tree on 10..22 vertices in a first run (2026-11-02). The same
hybrid search, streamed in 1,000,000-tree chunks with five low-priority workers, then labelled all
14,828,074 trees on 23 vertices in about 16 minutes (2026-11-17). A first pass with a 1e5-node cap
left only 208 trees unlabeled; the restart search labelled all 208. The fourth field on each line is
a search-cost counter from that run, not a graph parameter.

What failed: treating the fourth field as q (a checker bug, not a certificate bug); expecting order 23
to need a C port of the coverage verifier (the author's Python coverage check finished in about 10
minutes). No tree on 10..23 vertices was found that resisted the hybrid search.

An independent re-check (a checker written from the definition, plus a leaf-extension regeneration of
all 23-vertex trees from the n = 22 certificate) matched the n = 23 file one-to-one before the
three-skeptic panel ran.
