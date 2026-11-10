# Honesty gate: run 2026-11-07-1751, claim (b, p) = (17766, 1016845912283), partial win p1

status: CONFIRMED_PARTIAL
confirmed_scope: The pair in object/pair.json, base b = 17766 (2 × 3^3 × 7 × 47, not a perfect power, strictly between 10125 and 65537) and p = 1016845912283 (proven prime by trial division up to its square root and by a Lucas certificate, above 1e12), satisfies b^(p-1) == 1 (mod p^2) in exact integer arithmetic and is absent from both Fischer tables, FermQ_Sorg.txt and FermQ_Sort.txt, in the 2026-11-07 snapshots identified in the-record-we-beat/RECORD.md (sha256 beginning 35273a26 and bda97784 respectively), and from OEIS (no match for p on 2026-11-07), so it meets partial win p1 of wieferich-other-bases-fischer-table and not the full win, whose base range ends at 10125.

partial_win: p1
panel: reproduce.md pass: true · novelty.md pass: true · criterion.md pass: true (three hermes delegations, one
delegate_task call with three tasks, each given only claim/)

## Gate reading (main session, RUN.md step 7; the status may only go down)
- No downgrade trigger found.
  - No panelist hedged its verdict, and there is no reproduction mismatch. REPRODUCE wrote its checker before reading
    claim/verify.py, proved p prime by full trial division up to isqrt(p) = 1008387 and by a Lucas certificate
    (p - 1 = 2 * 487 * 1043989643, witness 2), checked the congruence four ways plus a Node BigInt run, and ran
    positive and negative controls. CRITERION re-derived every clause of p1 literally with its own primality proofs
    and showed that verify.py fails each altered clause. NOVELTY found the pair in no Fischer file (the two tables,
    the two first-bases files and six others), not in OEIS, not in the repository (main tree, TROPHY_CASE.md,
    known-knowns/, 200 pull requests, releases, issue search) and not in the literature or code it searched.
  - The claim is one object (one pair). Primality is proven, not probable. No capped search is used as an
    exclusion, and no benchmark baseline applies. 17766 is the only base in 2..65537 for this p (NOVELTY, CRITERION
    and the main session's own check), so no published pair propagates to it.
- Table access was honest. Every fetch in the run and in panel/work-* used the User-Agent naming V3R1T4S, with one
  request per resource, no retries and no blocked or challenge page (the OEIS pages carry the usual embedded
  Cloudflare script path; they are ordinary result pages).
- The panel's table fetches are under 6 hours old (NOVELTY 18:34:23Z, REPRODUCE 18:40:34Z, both byte-identical to the
  scout's 17:53:48Z copies), so no extra fetch was needed.
- The quoted criterion texts in claim/claim.md and target.md match bank/targets.json verbatim
  (attempts/frontier-archivist/output/gate_bank_quote_check.txt).
- The confirmed_scope above is the CRITERION panelist's sentence, exactly. It names the package's own files
  (object/pair.json, the-record-we-beat/RECORD.md) and pins the two table snapshots by their sha256 prefixes, which
  RECORD.md must state in full.
- Placeholder, leak and e-mail scan of the three panel files with check_run's own PLACEHOLDER_RE, LEAK_RES and
  EMAIL_RE: none found. No panel file was edited. sha256 before packaging: reproduce.md c8e6afa3..., novelty.md
  2ef7eff3..., criterion.md 70eab7b2....
- OEIS response bodies differ between fetches only by a per-request token, so their sha256 values cannot match each
  other; every fetch shows the same no-match sentence (REPRODUCE, NOVELTY, CRITERION and the scout).
- Not claimed: the full win (b > 10125); the second exact pair of this run, (28860, 1017279755641), which stays
  PROMISING until its own panel; a search certificate beyond the stated coverage; novelty beyond the sources listed
  in novelty.md.
