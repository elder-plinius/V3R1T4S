# Packomania novelty fetches, 2026-10-16 (UTC 02:37-02:41)

curl -sL from the box, HTTP status as shown. Files are byte copies of the responses. Hashes are in EVIDENCE_SHA256SUMS.

| file here | URL | HTTP | Last-Modified |
|---|---|---|---|
| scu_scu.html | https://packomania.com/scu/scu.html | 200 | (no change since 08-Oct-2026, sha256 matches 2026-10-15 snapshot) |
| pending-requests.html | https://packomania.com/pending-requests.html | 200 | page date 08-Oct-2026 (sha256 matches 2026-10-15 snapshot) |
| scu_txt_radius.txt | https://packomania.com/scu/txt/radius.txt | 200 | 15 Oct 2026 12:05:12 GMT |
| scu_txt_author.txt | https://packomania.com/scu/txt/author.txt | 200 | 15 Oct 2026 12:05:12 GMT |
| scu_txt_scu83.txt | https://packomania.com/scu/txt/scu83.txt | 200 | 28 Feb 2012 07:05:00 GMT |
| scu_txt_scu507.txt | https://packomania.com/scu/txt/scu507.txt | 200 | 01 Jun 2012 20:54:00 GMT |
| scu_scu83.html | https://packomania.com/scu/scu83.html | 200 | footer 28-Feb-2012 |
| scu_scu507.html | https://packomania.com/scu/scu507.html | 200 | footer 25-Jun-2013 |
| packomania_index.html | https://packomania.com/ | 200 | 11 Oct 2026 19:00:24 GMT |
| hints.html | https://packomania.com/hints.html | 200 | (format notes only) |

Tried and not found (404): https://packomania.com/scu.html, /history.html, /news.html. The homepage links no errata or news page; scu.html's "History of updates" section is the only history page.

## What the pages say
- scu.html History of updates (08-Feb-2012 .. 08-Oct-2026): no entry mentions an error, a wrong/mismatched file, a correction or a replacement for any N. Entries naming N = 83: 29-Feb-2012 (Liang Yu / Huang group), 25-Jun-2014 (Kolossváry, posted June 2018), 29-Jun-2018 (Bagattini, Schoen, Tigli). Entries naming N = 507: 02-Nov-2012 (Specht, bulk), 25-Jun-2013 (Packntile, "dated from June 2012"). None after 2018 for 83 or after 2013 for 507; the 2026 updates do not list 83 or 507.
- pending-requests.html (08-Oct-2026): 20 rows; no scu row. The only category-unspecified row is 26-Sep-2026 Moki & Julio "*many* 4666 candidates total"; it does not name scu, 83 or 507.
- Live scu83.txt and scu507.txt are byte-identical to the packaged posted copies (sha256 cc08dcaf…1c62, a62939a8…8a04); radius.txt rows 83 and 507 unchanged. Context only: both coordinate files carry a 2012 Last-Modified, older than the history entries that credit their N (2018 for 83; 2013 for 507).
- Searched scu.html text for wrong|error|incorrect|mistake|discrepan|overlap|infeasib|fixed|replac: no hits.

Conclusion: the N = 83 and N = 507 cell/file mismatches are not reported anywhere on Packomania. Not checked: private emails to E. Specht, other websites, papers.
