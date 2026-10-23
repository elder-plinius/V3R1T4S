# The record we compared against
- Covering Repository, https://coveringrepository.com/ , (v,k,t)-covering designs (plain, m=t), cell (38,6,3,3).
  - Public plain-text archive https://coveringrepository.com/download_archive_vkt.aspx (all plain (v,k,t) cells):
    one plain curl GET each by two panel skeptics (User-Agent "V3R1T4S-research (honest client)", no cookies, no
    retries) at 2026-10-20T16:35:04Z and 2026-10-20T16:35:40Z, HTTP 200, 171735 bytes, sha256
    3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7. The same bytes were fetched by the lookup tool
    below at 2026-10-20T16:34:06Z. Extracted cell (line 674, tab-separated): `38 06 03 03 510`.
  - Site search form (GET https://coveringrepository.com/systems.aspx at 2026-10-20T16:34:09Z, then one POST of the
    site's own read-only search form with V=38 K=6 T=3 M=3) by a lookup tool with User-Agent
    "V3R1T4S-live_cell/1.0 (record-table check; low volume)", no cookies, no retries, at 2026-10-20T16:34:13Z: response
    30319 bytes, sha256 be283df78172861efedd8a74c45c261049e38136627a5ec5361a263b25f708bc, no challenge page. The tool
    did not log the HTTP status for this read. Extracted row:
    `38 | 06 | 03 | 03 | 510 | 425 | Known design | Creator: Jan de Heer and Steve Muir, Method: Private Tools, Source: Dan Gordon Covering Repository, Repository: https://dmgordo.github.io/ | 05/06/2010`
    The panel ran the same tool once each at 16:35:24Z and 16:35:30Z: 510.
  - Superseded: a first search-form read at 2026-10-20T16:26:03Z (sha256 f1c68e22e8c93602fcce360e336bfa38f59849bd8c078cdb244289add6debb8d)
    used a User-Agent beginning "Mozilla/5.0" and replayed the ASP.NET session cookie from GET to POST. The V3R1T4S
    rules (kit/RULES.md rule 5) forbid both, so it is withdrawn and not relied on. It showed the same 510.
  - Home page: 2026-10-20T12:55:53Z HTTP 200 sha256 e43707d4e5c71e43f5f86143bad1b674e00c1dd54a5efc761769c210d07aaba3; panel 16:35:02Z HTTP 200 sha256 337d7caf92adcd4ef6a9d9f19a2cd610ab0f5ef2f7f6b94ca555fed9e2433652 (no per-cell values).
  - Latest-improvements page https://www.coveringrepository.com/systems.aspx?li=2 : 2026-10-20T12:55:55Z HTTP 200 sha256 1f9d4e1510ea02564e466636d88e14ec5e533b45c5e560923d19808ab62904dd; panel 16:35:05Z HTTP 200 sha256 8585c76298cadc2d022dfdb8b691c8fbae66930c84f007b7156aa833e825fa43. 100 rows dated up to 20/10/2026, no (38,6,3) row.
  - Per-cell query-string pages (systems.aspx?k=..&t=..&m=..) return a Cloudflare challenge for machines and were never requested.
- dmgordo/LJCR, https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json : fetched 2026-10-20T12:55:53Z, and by the panel at 16:35:04Z and 16:35:41Z, HTTP 200, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef. Extracted cell: "C(38,6,3)": size 510, low_bd 425; improvement history 526 (Flavio Perona 2008-11-17), 523 (Michael Dambmann, simulated annealing, 2008-11-29), 513 (Jan de Heer and Steve Muir 2009-09-16), 510 (Jan de Heer and Steve Muir, Private Tools, 2010-06-05).
- Zenodo, La Jolla Coverings Repository v1.2 (record 19735294, 2026-04-24): https://zenodo.org/api/records/19735294/files/coverdata.json/content fetched 2026-10-20T13:13:05Z and by the panel at 16:35:42Z, HTTP 200, sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87: C(38,6,3) size 510, low_bd 425. Version list https://zenodo.org/api/records?q=conceptrecid:10779736&all_versions=true fetched by the panel at 16:35:05Z, HTTP 200: v1.0, 1.1, 1.2; 1.2 newest.
- LJCR site https://dmgordon.org/covering-designs/ : 2026-10-20T12:55:54Z and panel 16:35:06Z / 16:35:42Z, HTTP 200, sha256 a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3, a landing page with no per-cell values. The old per-cell page https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=38 did not connect (2026-10-20T13:09:11Z; panel 16:38:02Z, TLS error), not retried.
No page itself is included.
