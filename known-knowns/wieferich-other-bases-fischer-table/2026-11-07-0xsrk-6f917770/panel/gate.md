# Honesty gate: run 2026-11-07-2010, claim (b, p) = (28860, 1017279755641), partial win p1

status: CONFIRMED_PARTIAL
confirmed_scope: The single pair in object/pair.json, b = 28860 = 2^2*3*5*13*37 (not a perfect power, an integer from 10126 to 65536) with p = 1017279755641 (above 1e12, proven prime by exhaustive trial division up to isqrt(p)), satisfies b^(p-1) == 1 mod p^2 in exact integer arithmetic and is absent from both Fischer tables identified by URL and sha256 in the-record-we-beat/RECORD.md (neither FermQ_Sorg.txt nor FermQ_Sort.txt has a row for base 28860 or contains p) and from OEIS (a search for p on 2026-11-07 matched no sequence), so it is one new pair meeting partial win p1 of wieferich-other-bases-fischer-table, and not the full win, which requires b at most 10125.

partial_win: p1
panel: reproduce.md pass: true · novelty.md pass: true · criterion.md pass: true. These are the run's second panel
(PREREG.v2.md): three Claude Code Task subagents, launched in one message at 2026-11-07T21:06:10Z, each given only
claim/.

## Why this is the second panel
- The run's first claim/ was assembled at 20:12:22Z-20:12:53Z, 29 to 60 s before PREREG.md was frozen (20:13:22Z),
  because RUN.md step 0 makes a carried-over claim's panel the first job. The first panel (launched 20:14:50Z) passed
  3/3, and its gate was written before the full workspace check had been run.
- That check then rejected the order ("PREREG.md was written after the claim was built"). RUN.md step 7 lets a
  confirmed status stand only on a full CHECK_RUN PASS, so the first gate could not stand.
- PREREG.v2.md (frozen 21:04:28Z) changed the claim path before any of it ran:
  - the first panel and gate stay unchanged in panel/first-panel/;
  - claim/ was rebuilt byte for byte at 21:05:07Z (attempts/skeptic-settled/output/claim_rebuild.txt: 9 files, every
    sha256 equal before and after, CLAIM_REBUILD IDENTICAL);
  - the three role files were reset to a one-line reservation stub, so no second-panel skeptic could read a
    first-panel verdict;
  - a fresh panel received the first panel's instructions word for word, with new scratch folders.
- PREREG.v2.md fixed in advance that the second panel's verdicts govern, whatever they are.

## Gate reading (main session, RUN.md step 7; the status may only go down)
- **No downgrade trigger found.**
  - No skeptic hedged its verdict, and there is no reproduction mismatch. REPRODUCE leaves the OEIS clause to
    NOVELTY by role, because it makes no network requests.
  - REPRODUCE and CRITERION each proved p prime by exhaustive trial division up to isqrt(p) = 1008602, and each
    also gave a Lucas certificate (p - 1 = 2^3 * 3^2 * 5 * 47^2 * 1279211, witness 11).
  - Each checked the congruence by at least three exact routes. claim/verify.py agreed and rejected five mutated
    objects (REPRODUCE and CRITERION).
  - The claim is one object; primality is proven, not probable; no capped search is used as an exclusion; and no
    benchmark baseline applies.
- **Table access was honest.** Every fetch used the User-Agent naming V3R1T4S, with one request per source, no
  retries, and no blocked or challenge page.
  - NOVELTY fetched Fischer's index and his ten Fermat-quotient files, two OEIS searches, and the repository's tree,
    trophy case, releases, target page, bank and news. It also made 28 raw-file reads at the heads of the three
    Wieferich pull requests, all HTTP 200.
  - CRITERION fetched both tables, the index, News.txt, one OEIS search, the live bank entry and one GitHub search.
- **The panel's table fetches are under 6 hours old:** NOVELTY 21:08:48Z (FermQ_Sorg.txt) and 21:08:54Z
  (FermQ_Sort.txt); CRITERION 21:15:55Z and 21:16:01Z. All are byte-identical to the scout's copies of 20:11:24Z.
- **The quoted criterion texts match the bank verbatim.** CRITERION checked them against the live bank entry
  (its F4), and the main-session string comparison is in attempts/skeptic-settled/output/gate_bank_quote_check.txt.
- **confirmed_scope** above is the CRITERION panelist's sentence, exactly, and it names the package's own files
  (object/pair.json, the-record-we-beat/RECORD.md).
- **One verdict line read narrowly.** CRITERION's closing paragraph says p appears in no V3R1T4S issue or pull
  request. That rests on GitHub's issue search, which indexes titles, bodies and comments, not files.
  - NOVELTY read the files of the three Wieferich pull requests and found the one mention, line 37 of #999's
    panel/gate.md, which lists this pair under "Not claimed".
  - Partial win p1 asks for absence from the two Fischer tables and from OEIS, and both hold. The scope sentence
    claims nothing about the repository, so no downgrade follows.
- **Priority condition: met.**
  - The pair's only earlier public mention is that disclosure in #999, by the same contributor, which leaves it
    explicitly unclaimed until its own panel.
  - No pull request claims it (NOVELTY: 959 pull requests read).
  - This package's id carries the same credit as #999's branch, and its README cites the mention.
- **Panel contexts: disclosed and recorded.**
  - The Claude Code harness preloads the workspace's project-instruction file, with the hand-off notes it imports,
    into every session, subagents included. Each skeptic's context therefore held the hand-off notes' one-line
    summary of this pair. All three disclosed it.
  - Each skeptic read its own one-line reservation stub, which the Write tool requires before replacing a file.
    REPRODUCE also listed the panel folder's file names to find its scratch folder, and opened no other panel file.
  - None opened any other workspace file outside claim/ and its scratch folder.
  - Each verdict rests on claim/ and on the panelist's own code, fetches and pasted outputs. The kit accepts
    subagents as fresh contexts, and run 2026-11-07-1158's gate recorded a similar disclosure without downgrading.
    This gate does not downgrade either, and records the deviation.
- The panel files are copied into the package exactly as written.
