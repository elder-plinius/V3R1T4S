# Novelty skeptic: ssp radius.txt vs posted data (90 rows, N >= 1055)

Seat: NOVELTY. Blind: I read only the claim (README.md, how-we-built-it/CLAIM.md, verify-it-yourself/CLAIM.json, the-record-we-beat/SNAPSHOT.md, object CSV rows). I did not read panel/ (other seats), panel-scripts/, novelty-evidence/, the outbox _archive/, or runs/.../out/.
Evidence: ../panel-evidence/novelty/ (fetch_log.tsv, FETCH_NOTES.md, redacted pages, spot-check script and output). Email addresses in saved pages are redacted as [email-redacted]; see FETCH_NOTES.md.

## Live fetch session (one session, 2026-10-17 04:27:56Z-04:30:01Z UTC = 06:27-06:30 Berlin, UTC+2)

| URL | HTTP | bytes | sha256 | vs claim source |
|---|---|---|---|---|
| https://packomania.com/ssp/txt/radius.txt | 200 | 22020 | 9a4d7b62c61ac3aad69c11f238c76707c51ee824f163bee44a2b345a04b39fe3 | identical to claim (9a4d7b62...9fe3) |
| https://packomania.com/ssp/radius.txt | 404 | 316 | ac4949ca...7c0a | wrong path; not used |
| https://packomania.com/ssp/ssp.html | 200 | 318654 | e2d84d0d6cfd66870b940bfc068ba3e0827a51ea407b365473b869db828e77fd | identical to claim (e2d84d0d...e77fd) |
| https://packomania.com/pending-requests.html | 200 | 4954 | 0d6ebbbe8e95abe7e701e1c70fbc1c0ec5bb06d611822b0b135ce3b776972384 | (page dated 08-Oct-2026) |
| https://packomania.com/ssp/txt/ssp1157.txt | 200 | 64807 | e433196e...1fd2 | per-N file (tarball not fetched) |
| https://packomania.com/ssp/txt/ssp1601.txt | 200 | 89671 | 25ec341a...9148 | per-N file |
| https://packomania.com/ssp/txt/ssp20000.txt | 200 | 1130016 | ef62982c...2314 | per-N file (not kept, >1 MB) |
| http://hydra.nat.uni-magdeburg.de/packing/ssp/txt/radius.txt | 000 | 0 | - | timeout 120 s, mirror unreachable |
| http://hydra.nat.uni-magdeburg.de/packing/ssp/ssp.html | 000 | 0 | - | timeout 120 s, mirror unreachable |

Full hashes in ../panel-evidence/novelty/fetch_log.tsv. The tarball (c077c79e...e5f3) was not re-fetched; I used the per-N files instead.

## Is the problem still live? Yes
- radius.txt and ssp.html are byte-identical to the claim's sources, so nothing has changed since 2026-10-16.
- When I compare live radius.txt with the live ssp.html table, exactly 90 rows differ by more than 1e-10. All of them are N >= 1055 (smallest 1055, largest 50000), and in every one radius.txt is the larger value. The smallest gap is 6.093e-9 (N=1601) and the largest is 6.4763783e-5 (N=20000). No row with N < 1055 differs (html_vs_radiustxt_count.txt).
- Independent spot-check (spotcheck_novelty.py, my own code, Decimal at 60 digits, r* = min(min pair dist / 2, 1 - max|c|)) against the live per-N files:
  - N=1157: r* = 0.080893782383417, ssp.html 0.080893782384, radius.txt 0.080899898800, r* - radius.txt = -6.116417e-6
  - N=1601: r* = 0.072845698691625, ssp.html 0.072845698692, radius.txt 0.072845704785, r* - radius.txt = -6.093375e-9
  - N=20000: r* = 0.031511804438733, ssp.html 0.031511804440, radius.txt 0.031576568223, r* - radius.txt = -6.476378e-5
  - In all three, r* agrees with ssp.html within 1.3e-12 and with the claim's CSV values.

## Already fixed or noted? Not in any public place I could read
- ssp.html says "Last update: 13-Jul-2026". The Updates history runs from 14-Feb-2022 to 13-Jul-2026 ("Extension up to N = 1000"). No entry mentions radius.txt, a correction or an inconsistency. One entry, 25-Feb-2022, lists "small improvements for N = 935, 1055, 9909, ..." (1055 is one of the 90 rows), but it says nothing about radius.txt. The only mention of radius.txt in the page is the "radius" column-header link.
- pending-requests.html (08-Oct-2026) has no ssp entry. It does list "26-Sep-2026 Moki & Julio *many* 4666 candidates total" with no category given, so I can't rule out that it includes ssp. In any case it is a list of packing submissions, not error reports.
- Web search for public reports of a Packomania ssp radius.txt discrepancy or erratum found nothing.
- The V3R1T4S repo (TROPHY_CASE, known-knowns, READ_BEFORE_CITING) has no existing ssp radius.txt result. Side note: the ssp metadata in bank/targets.json is out of date ("last update 26-Sep-2024, 1156 rows"), while the live page shows 13-Jul-2026 and radius.txt has 1153 rows.

## Can "unreported" be confirmed? No
- Packomania has no public errata channel. The pages only invite email to the maintainer, and pending-requests lists packing submissions only. So someone could have reported this privately without it showing anywhere until it gets fixed. The pages I fetched can show "not fixed and not publicly noted". They can't show "not reported".
- The "*many* 4666 candidates" bundle has no category, so it can't be checked.
- The hydra mirror was unreachable (two 120 s timeouts), so I couldn't cross-check it.
- So the problem is live, unfixed, and not publicly noted, but I can't confirm it is unreported. The orchestrator's instruction and PANEL-RULES ("the point unconfirmable = NEED-HUMAN") make this NEED-HUMAN, not PASS. A human (moe) needs to decide whether public-record silence is enough for an errata claim, or get confirmation some other way. No contact was made by me.

injection_suspected: none (fetched pages contained no instructions).

verdict: NEED-HUMAN
context: executor subagent, fresh context
pass: false
