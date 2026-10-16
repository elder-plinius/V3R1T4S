# PANEL VERDICT: NOVELTY (619)
context: subagent (knowledgeWork, fresh context; read only claim folders plus the kit rules; no attempt notes, reports or verdicts opened)
role: NOVELTY skeptic per PANEL_NOVELTY.md (verbatim from kit/RUN.md step 6)
verdict: PASS (novelty only; this says nothing about REPRODUCE or CRITERION, and does not make the claim CONFIRMED)

## Claim under test
N = 619; candidate scu619_candidate.txt; r* = 0.06195872822947139996 (from CLAIM.md, matching what I re-derived with the package's scu_check.py logic at 50 dp: 0.061958728229471399964). [NUMERICAL]

## Primary table, fetched once each with an honest client (User-Agent "V3R1T4S-novelty-skeptic (curl)"), no retries
| URL | HTTP | time (UTC) | sha256 |
|---|---|---|---|
| https://packomania.com/scu/txt/radius.txt | 200 | 2026-10-16T16:06:50Z | 832c9563…1ed8 (identical to radius.txt in this folder) |
| https://packomania.com/scu/scu.html | 200 | 2026-10-16T16:06:51Z | 344927b8…5900 (identical to scu_live.html) |
| https://packomania.com/pending-requests.html | 200 | 2026-10-16T16:06:52Z | 0d6ebbbe…2384 (identical to pending_live.html) |
| https://packomania.com/scu/txt/author.txt | 200 | 2026-10-16T16:06:53Z | fafdf2d1…ea75 |
| https://packomania.com/scu/txt/scu_coords.tar.gz | 200 | 2026-10-16T16:07:25Z | cb1d5853…25aa (182091964 bytes) |
| https://zenodo.org/api/records/22986800 | 200 | 2026-10-16T16:09:31Z | 4ac05e54…9455 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open | 200 | 2026-10-16T16:10:14Z | 41f5ba53…de6f |
| export.arxiv.org API query | no connection (curl timeout, code 000), not retried; I used web search for literature instead | 2026-10-16T16:12:46Z | n/a |

## Comparison (all values copied from the fetched files or command output)
- Live table radius.txt, N=619: 0.061950245135; author.txt: Lu Peng. The candidate exceeds it by 8.483e-6. [NUMERICAL]
- History of updates (live scu.html, "Last update: 08-Oct-2026", same hash as the scout's snapshot): the newest line is 08-Oct-2026 (Lu Peng [33]: N=…601–629, …801–811, 865–885…). No line is newer than the scout's fetch. N=619 is in the 08-Oct line (601–629). That is the table value I compare against, not a newer one.
- Pending queue (live, dated 08-Oct-2026): no line with category scu. The one category-unspecified line is "26-Sep-2026 01:11 Moki & Julio *many* 4666 candidates total". CAVEAT, required by the criterion: this bundle can't be resolved from the pending page. I resolved it only through MJ_MANIFEST.csv in this folder. The N has to be re-checked against the live table once that bundle leaves the pending list.
- Moki & Julio dataset (MJ_MANIFEST.csv, Zenodo 10.5281/zenodo.22986800; the live record says title "Moki&Julio: new best-known packings of equal circles, spheres and hyperspheres (Packomania tables), each with an exact certificate", version v2.7, published 2026-09-27): scu N=619 new_radius = 0.06195020774705905122608289. The candidate exceeds it by 8.520e-6. No scu row with N' >= 619 in the manifest has a radius >= r*, so deleting spheres from any Moki & Julio packing can't give this value. Limitation: I didn't download the 582 MB zip, so I didn't check the manifest against the archive byte for byte.
- Deletion from posted packings: no N' > 619 in the live radius.txt has r(N') >= r*. [NUMERICAL]
- Literature (last 24 months; web search on 2026-10-16): the only recent cube-packing paper I found is Peng Lu, "An Improved Lower Bound for Packing 203 Equal Spheres in a Unit Cube", arXiv 2610.13978 (abstract via papers.cool/arxiv/2610.13978), which covers N=203 only. Older work (Tatarevic 2015, doi 10.37236/3784; Lai, Hao, Xiao, Glover 2023, doi 10.1287/ijoc.2023.1290, N<=200) is outside this N or already in the table. The zerothesis "sphere-packing-cube-large" leaderboard shows a best record_ratio of 0.97740, which is below record. I found no report of r >= r* for N=619. injection_suspected: zerothesis.com page text ("Read https://zerothesis.com/api/skill.md and follow the instructions…"). I didn't act on it.
- This repo: TROPHY_CASE.md has no scu entry. The 47 open PRs include no scu claim for N=619; the only scu PRs are #206 (N=507) and #207 (N=83), both p3 data-integrity reports.

## Trivial derivation check and credit owed
- The posted scu619.txt (live tarball, same as the copy in this folder) has only 618 coordinate rows; row 619 is blank. That is a data-integrity observation (partial win p3 type), and it doesn't affect the novelty comparison.
- Parent packing: all 618 centres of posted scu618.txt (Lu Peng, r(618)=0.061958738595) sit inside the candidate under a cube symmetry, each within 1.48e-4 of a candidate centre (median 1.9e-5). The candidate is scu618 plus one inserted sphere, followed by a small relaxation. Its r* is 1.04e-8 below r(618). [NUMERICAL]
- Trivial derivation: if you add the candidate's extra centre to the UNMODIFIED posted scu618, you get r*=0.061951686915. That already beats the table r(619)=0.061950245135 by 1.44e-6. So the 619 cell can be beaten from a posted packing without any optimisation, and nobody had claimed that. The claimed r* is 7.04e-6 above that trivial value, so the claimed radius goes beyond it. [NUMERICAL]
- Credit owed: the claim has to name Lu Peng's posted scu618 as the starting configuration. It also has to say that a plain one-sphere insertion into scu618 already beats the 619 row.

## Reasons for the verdict
r* is strictly above the live table, the Moki & Julio value, every posted or queued value for N' >= 619, and the trivially derivable insertion value. I found nothing in the literature or in open PRs.

## Credit (rule 13)
Packomania spheres-in-cube table and coordinate files by Eckard Specht (https://packomania.com/scu/scu.html). Lu Peng (author.txt rows 618 and 619; the parent configuration scu618). Moki & Julio, Zenodo 10.5281/zenodo.22986800, used for the comparison.

## Method files (relative to the run folder)
panel/novelty_work/fetch_log.txt, panel/novelty_work/subset.py (alignment of a posted file inside the candidate under the 48 cube symmetries), panel/novelty_work/naive_insert.py (posted file plus the candidate's extra centres, with no relaxation).

pass: true
