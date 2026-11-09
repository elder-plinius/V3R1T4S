# Novelty skeptic: tsasm-a005164-order-51-exact

context: subagent (parent Task)

Worked only from a scratch copy of `claim/` ([scratch]/claim). I did not read REPORT, NOTES, attempts, LOG or other panel files.

## Object under test
A005164(25) = 30533896243799704017627552102998416 (TSASMs of order 51), from exact enumeration (claim.md).

## Status source: one GET per URL, User-Agent "V3R1T4S-research-agent", no retries
| URL | time (UTC) | time (America/New_York) | HTTP | what it shows |
|---|---|---|---|---|
| https://oeis.org/A005164 | 2026-11-01T03:00:03Z | 2026-10-31 23:00 EDT | 200 | DATA ends at a(24) = 52893528399758443649956432899616; "a(20)-a(24) from Jean Liénardy, Sep 21 2022"; keyword `more` |
| https://oeis.org/A005164/b005164.txt | 2026-11-01T03:00:03Z | 2026-10-31 23:00 EDT | 200 | last line `24 52893528399758443649956432899616`; sha256 prefix b93ec1418f1bf5b8, identical to the claimant's copy |
| https://oeis.org/draft/A005164 | 2026-11-01T03:00:03Z | 2026-10-31 23:00 EDT | 200 | "(No pending changes for A005164.)" |

The claimed value (and the substring 30533896) does not appear in any of the three pages.

## Search, last 24 months and older
- Web search for the exact 35-digit value: no hits.
- GitHub code search for the exact value: 0 results. Code search for "A005164": only joeis (a brute-force search the author calls "too slow for more than a few terms", with no stored terms), the V3R1T4S target files, OEIS mirror/spider data (a(24) at most), and guillochon/oeis-results/A005162 (a different class). guillochon/oeis-results has no A005164 directory and no releases or release assets.
- Literature:
  - Liénardy & Walmsley Hagendorf, arXiv:2509.09209 (v1 Sep 2025, v2 Nov 2025; fetched once, 200, 2026-11-01T03:01:09Z). It proves a multiple-contour-integral formula for |TSASM(2N+1)| (Cor. 4.3) and cites OEIS A005164. It gives no numeric table and contains no term beyond the OEIS data.
  - Behrend–Fischer–Koutschan, arXiv:2309.08446 (fetched once, 200, 2026-11-01T03:01:22Z). It cites Liénardy's thesis Tab. A.1 for TSASM data and gives asymptotics only. It contains no new terms.
  - Richards, Cardiff PhD thesis (Feb 2026), covers HTSASM, OOSASM and QTSASM, not TSASM.
  - Liénardy's PhD thesis (2020, hdl 2078.1/240624): the handle GET returned HTTP 500 (2026-11-01T03:01:38Z), so I did not retry and could not read it. It predates his own Sep 2022 OEIS extension to a(24), so it almost certainly stops at or before a(24).
- Repo [workspace]/repo (HEAD f3b19b4, 2026-10-30): TROPHY_CASE.md has no TSASM or A005164 entry. known-knowns/ has no TSASM or A005164 folder. The only "30533896" hit is a coincidental substring inside a long integer in codetables-qubit cert_164_1_54_sh.json, which is unrelated. No local branch or commit mentions tsasm or A005164.
- V3R1T4S pull requests, open and closed (GitHub API, state=all, #771–#875, created 2026-10-26 to 2026-10-31T20:15Z, which covers everything since the target opened on 2026-10-30), plus PR search for "A005164" and "tsasm": none mention TSASM, A005164, alternating sign matrices or the value.

## Comparison
The largest published index is n = 24 (OEIS DATA, b-file, draft queue; unchanged since Sep 21 2022). The claim adds a new term at n = 25, so it strictly extends the known record and is not a tie. It is also not a trivial edit of a published object, because no published source has a(25) in any form. As a sanity check, the successive ratio a(25)/a(24) ≈ 577.3 continues the alternating second-ratio pattern (≈1.37 and ≈1.23) seen from a(15) to a(24). That does not prove correctness; correctness is for the other skeptics.

Side note for the panel (does not affect novelty): arXiv:2509.09209 turns the Hagendorf–Liénardy formula from a conjecture into a theorem. The bank still asks for exact enumeration rather than evaluating that formula, and the claim says it used enumeration.

pass: true
