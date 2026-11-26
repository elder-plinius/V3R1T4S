context: Claude Code subagent, fresh context [Sonnet 5.5]

novelty: the case A1 = 11 is not published as proved in anything I could find. Limits are listed at the end.

Status source (read once, honestly, no retries)
- 2026-11-17T03:54:14Z, GET https://library.slmath.org/books/Book71/files/GONC6-04.pdf, HTTP 200, sha256 cc1b985ef7fa16d79877677a49b59eb65924a6d082341ae53348544c22cde1f1. This is the same hash the package's the-record-we-beat/SNAPSHOT.md records (fetched 2026-11-16T19:42:23Z).
- Problem A4(53), N-heap Wythoff game, pp. 61-62 of Nowakowski's column. It states Conjectures 1 and 2. It says Fraenkel and Krieger proved that Conjecture 1 implies Conjecture 2. It says of Sun and Zeilberger [139]: "the conjectures are true for the case N = 3, where the first heap has up to 10 tokens. For those 10 cases, the parameter values m, M, a, T were listed in a table." It then mentions Sun [138], who proved similar results, with a method to compute a. Nothing in it records a proof for A1 = 11 or any larger value, or for all A1.

Literature and code search (web search tool or curl; each curl fetch is recorded in a fetches log in my scratch folder)
- Web search: "Fraenkel three-heap Wythoff conjecture proved smallest heap A_1 = 11 Sun Zeilberger". Result: only the Sun-Zeilberger paper (A1 <= 10), Sun's Discrete Math 2005 paper, and an unrelated 2026 arXiv "A Proof of Fraenkel's Conjecture" about Beatty-sequence partitions (a different conjecture).
- Web search: "N-heap Wythoff game Fraenkel conjectures 3-heap proof first heap 11 OR 12 OR all A1 arXiv 2025 2026". Result: nothing beyond A1 = 10. It also surfaced the Klein-Fraenkel K-Pile Wythoff papers and Wythoff's Game with a Pass (arXiv 1711.04960, July 2025 revision); neither appears to prove the A1 = 11 case, going by titles and snippets. I did not read their full text.
- Web search: "Sun and Zeilberger Wythoff three heaps P-positions sufficient condition extended computer proof github". Result: no code repository and no extension of the proof; only the Rutgers pages and the Games of No Chance 4 survey, which repeats the A1 <= 10 result.
- 2026-11-17, GET https://oeis.org/search?q=wythoff+three+heap&fmt=json, HTTP 200. It returned only generic Wythoff sequences (for example A000201); I saw no 3-heap P-position entry proving anything. I read only the head of the output.
- 2026-11-17, GET http://export.arxiv.org/api/query (two queries: Wythoff with heap; Fraenkel with conjectures and Wythoff). HTTP 200 but an empty feed, which is not evidence either way. Not retried.
- Semantic Scholar API query "N-heap Wythoff conjectures": HTTP 429, not retried. No Semantic Scholar evidence.
- Repository check, read-only gh, elder-plinius/V3R1T4S: searches for pull requests matching "wythoff", "three-heap-wythoff-fraenkel-a1-11" and "Fraenkel" returned no open or closed pull requests. Code search for "wythoff" found only the target's own entry, the target's own page in the repository's known-unknowns folder, and the folder README. That entry says the problem is open as of 2026-10-30, with the same criterion as the claim. TROPHY_CASE.md has no line mentioning wythoff. The known-knowns folder (35 entries listed) has no Wythoff or Fraenkel entry by name.

Judgment
Fraenkel's own later papers and the Klein-Fraenkel pages appear in search, but none showed a proof for A1 = 11 or any larger value. The status column still lists only A1 <= 10. No competing pull request exists. So the A1 = 11 case is not published as proved, and a correct result for it would strictly extend the known frontier.

Limits
- Google Scholar and journal sites were reached only through the web search tool, not directly. The arXiv API returned an empty feed and Semantic Scholar rate-limited, so those two checks are weak.
- I did not read the full text of Fraenkel's later papers; I judged them from titles and search snippets.
- This panel checked novelty only, not whether the certificate is correct.

pass: true
