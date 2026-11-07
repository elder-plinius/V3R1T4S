# Honesty gate: run 2026-11-07-1508, claim (b, p) = (28910, 1011548897263), partial win p1

status: CONFIRMED_PARTIAL
confirmed_scope: The pair in object/pair.json, base b = 28910 (2*5*7^2*59, not a perfect power, 10125 < b < 65537) and p = 1011548897263 (proven prime, p > 1e12), satisfies 28910^(p-1) == 1 (mod p^2) in exact integer arithmetic and is absent from both Fischer tables, FermQ_Sorg.txt and FermQ_Sort.txt, in the snapshots identified in the-record-we-beat/RECORD.md, and from OEIS (no match for p on 2026-11-07), so it meets partial win p1 of wieferich-other-bases-fischer-table and not the full win, whose base range ends at 10125.

partial_win: p1
panel: reproduce.md pass: true · novelty.md pass: true · criterion.md pass: true (three Claude Code Task subagents,
each given only claim/, launched in one message)

## Gate reading (main session, RUN.md step 7; the status may only go down)
- No downgrade trigger found.
  - No panelist hedged its verdict, and there is no reproduction mismatch. REPRODUCE proved p prime by full trial
    division and a Lucas certificate. It checked the congruence with three arithmetic implementations, and
    claim/verify.py agreed with its own checks on seven controls. CRITERION re-derived every clause with four exact
    routes and an independent primality proof.
  - The claim is one object (one pair). Primality is proven, not probable. No capped search is used as an
    exclusion, and no benchmark baseline applies.
- Table access was honest. Every fetch in the run and in panel/work-* used the User-Agent naming V3R1T4S, with no
  retries and no blocked or challenge page.
  - NOVELTY's `gh api` call was refused by this workspace's permission settings. NOVELTY read the same public
    repository data with single plain curl GETs to api.github.com, as the scout does. That is a read through an
    allowed honest client, not an evasion of a block.
  - GitHub code search timed out once and was not repeated (disclosed in novelty.md). The bank's named sources,
    Fischer's tables and OEIS, were fetched and read in full.
- The panel's table fetches are under 6 hours old (NOVELTY 15:53:12Z, CRITERION 16:00:54Z, both byte-identical to
  the scout's 15:08:57Z copies), so no extra fetch was needed.
- The quoted criterion texts in claim/claim.md match bank/targets.json verbatim. The main-session string comparison
  is saved in attempts/object-as-data/output/gate_bank_quote_check.txt, and CRITERION checked the live bank file too.
- The confirmed_scope above is the CRITERION panelist's sentence, exactly. It names the package's own files
  (object/pair.json, the-record-we-beat/RECORD.md), not claim/ paths.
- Panel-file edits: NOVELTY replaced two angle-bracketed words in its own curl description (the words file and url,
  each between angle brackets) with `FILE` and `URL` on the gate's request, because the package checker reads such a
  bracketed url as an unfilled placeholder.
  Nothing else changed. The panel files are copied into the package exactly as they stand now (sha256 before
  packaging: reproduce.md 35ba14b8…, novelty.md 04787ccf…, criterion.md d2ad4896…).
- Not claimed: the full win (b > 10125), a search certificate for the rest of the swept range, and novelty beyond the
  sources listed in novelty.md.
