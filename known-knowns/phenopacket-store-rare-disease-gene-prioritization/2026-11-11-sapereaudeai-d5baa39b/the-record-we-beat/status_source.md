# The status source (no record table exists for p3)

p3 is an audit of the reference tool, not a record value, so there is no table cell to beat. This file records the
bank's status source as read by this run.

- URL: https://github.com/monarch-initiative/phenopacket-store/releases, read through
  https://api.github.com/repos/monarch-initiative/phenopacket-store/releases?per_page=5
- fetched (UTC): 2026-11-11T10:34:08Z, HTTP 200, one request, User-Agent naming V3R1T4S
- sha256 of the saved API response: 943ff00717cfa392acf9e0f1cf6641f0ae8c76868b528d7376ac5b2d241ef2e4 (the page itself is not copied here)
- extracted: latest release 0.1.27, published 2026-06-09T16:47:04Z; all_phenopackets.zip 19431098 bytes, digest
  sha256:d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a (the corpus this audit pins)
- related published work, for comparison of design only (not a table): arXiv 2609.02473 reports LIRICAL 2.4.1 on
  phenopacket-store 0.1.27 under exact leave-one-publication-out removal, Recall@1 0.4868 -> 0.1724 on its 2,227 cases.
