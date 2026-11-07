# NOVELTY skeptic: anomaly-free-atlas-qmax

Target: anomaly-free-atlas-qmax (charter quarry 5). Claimed new rows: SMnuR Q_max 12..16, SM Q_max 12..31
(e.g. SMnuR Q_max 12: 95067546; SM Q_max 12: 67968, 31: 13425699). Inputs read: claim/CLAIM.md, claim/status.md,
claim/object/counts.txt, and the repo's TROPHY_CASE.md. Nothing else in the run was read.

## Status-source fetches (one request each, plain curl, no retries, no user-agent changes)

| UTC time | URL | result |
|---|---|---|
| 2026-10-18T09:53:09Z | https://zenodo.org/records/3345889 | http_code 000, "curl: (56) CONNECT tunnel failed, response 403" (proxy refused; no page bytes) |
| 2026-10-18T09:53:10Z | https://arxiv.org/html/1812.04602v5 | http_code 000, "curl: (56) CONNECT tunnel failed, response 403" (proxy refused; no page bytes) |
| 2026-10-18T09:53:10Z | https://link.springer.com/article/10.1007/JHEP08(2019)064 | http_code 000, "curl: (56) CONNECT tunnel failed, response 403" (proxy refused; no page bytes) |

No status-source page was read, so no published value can be quoted with a URL and a time. Per the instruction (a
block means fail) none of these was retried, and WebFetch was not used as a second attempt on them. This matches the
run's own record in status.md: the scout's fetches at 05:54 UTC were refused the same way ("PENDING TABLE CHECK").
So the largest published Q_max (10 for both SM and SMnuR, per status.md) and the published counts are known here
only from search-engine text, not from a byte-exact table.

## Literature search (WebSearch, last 24 months targeted), 2026-10-18 between 09:53 and 09:54 UTC

1. "anomaly-free U(1) charge assignments Standard Model family-dependent count Qmax atlas extension" (extended):
   returned the ADM atlas (JHEP 02 (2019) 082, arXiv:1812.04602v5), its erratum (adds SMnuR 7 <= Q_max <= 10), the
   Zenodo record 3345889, the SUSY atlas (Allanach, Madigan, Tooby-Smith, JHEP 02 (2022) 144; MSSM + up to 3 singlets,
   Q_max <= 10), and unrelated U(1)' model papers (e.g. arXiv:2511.05976, a leptophilic U(1)'). No count with
   Q_max >= 11.
2. "Allanach Davighi Melville anomaly-free atlas right-handed neutrinos Qmax 10 solutions extended 2025 2026":
   same atlas and SUSY-atlas papers; no 2025 or 2026 extension found.
3. "\"anomaly-free\" \"flavour-dependent\" U(1) charges enumeration larger Qmax arXiv 2025": atlas paper, Zenodo
   records 3345889 and 5062066/5062067 (SUSY atlas data, Q_max <= 10), Cambridge repository copy; no Q_max >= 11.
   (The tool's snippet attributed 21546920 at Q_max 10 to the SM content; status.md attributes it to SMnuR. Snippets
   are not a table; this inconsistency is one more reason the table itself must be read.)
4. "number of anomaly-free U(1) charge assignments SM three right-handed neutrinos Qmax 11 12 census": NSF PAR and
   Cambridge copies of the SUSY atlas, Zenodo records, DOAJ entry; the tool reported no published count at
   Q_max = 11 or 12.

Finding: the searches surfaced nothing with Q_max >= 11 for SM or SMnuR, and no extension of the ADM table in the
last 24 months. A search engine is not exhaustive (e.g. no INSPIRE citation crawl of 1812.04602 could be made), and
the SUSY atlas is a different field content, so it does not compete with these rows.

## TROPHY_CASE.md and open pull requests

- TROPHY_CASE.md (repo copy): no match for anomal, U(1), Q_max/qmax, Allanach, Davighi, atlas, "charge assign",
  neutrino. Families listed: degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP,
  RobustBench, cipher commitments. No entry for this target.
- Open PRs, https://github.com/elder-plinius/V3R1T4S/pulls (WebFetch, all 4 pages of the 89 open PRs read by title):
  no title on anomaly-free U(1) charges, the ADM atlas, Q_max or right-handed neutrinos. GitHub search
  "is:pr is:open anomaly" returned one PR, #311 (a Packomania spheres-in-cube erratum), which is unrelated.
  Only titles were visible, not PR bodies.

## Assessment

Nothing found beats or ties the claimed rows, and the claimed Q_max values (12..16 SMnuR, 12..31 SM) are above the
reported published maximum (10). But the record condition, "strictly beats everything known", needs the primary
table to be read to confirm that 10 really is the largest published Q_max, and that table could not be read: all
three status-source URLs were refused by the proxy. Side note: the claim skips Q_max = 11 for both contents. That
does not affect novelty for Q_max >= 12, but the census is not contiguous past the published range.

novelty: PENDING STATUS CHECK
context: subagent (fresh, saw only claim/)
pass: false
