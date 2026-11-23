# Honesty gate (kit/RUN.md step 7)

status: CONFIRMED_PARTIAL
confirmed_scope: The file cert_n23.txt (uncompressed sha256 d25faee17d7c798dbe7f6d4acc882cb82f924a537de4c8620ed61264f79ecf0e; gzip sha256 483c524995e2c184c1f5a7aeda65a69d44a97ac552c3c6177374bc4b13435520; archive odd-graceful-trees-10-23-certificates.tar.xz sha256 f89ddd847de5ea066c05730800a17ac01f9ee694c346638d40d1b1b0dc526713, 271015048 bytes, https://zenodo.org/records/24322888/files/odd-graceful-trees-10-23-certificates.tar.xz?download=1, DOI 10.5281/zenodo.24322888) gives, for every one of the 14828074 unlabeled trees on 23 vertices (A000055(23), matched one-to-one by canonical form against independent regeneration by three fresh-context skeptics), an injective vertex labeling into {0, 1, ..., 43} whose edge differences are exactly {1, 3, ..., 43}.

Read from panel/reproduce.md, panel/novelty.md and panel/criterion.md, each written by a fresh-context
subagent that saw the claim and the certificate only and wrote its own checker, each ending pass: true.
- REPRODUCE: own C checker from the definition; every one of the 14828074 lines is a tree on 23 vertices
  with a valid odd-graceful labeling; AHU forms pairwise distinct; count equals A000055(23). SURVIVES.
- NOVELTY: Gallian DS6, 29th edition (6 November 2026), Section 3.6, fetched 2026-11-17T16:46:26Z, still
  gives the exhaustive bound as order 12 (Barrientos); no published or arXiv census past 12 was found;
  draft PR #1007 claims every tree on at most 22 vertices and does not cover 23. NOVEL for n = 23.
- CRITERION: the paneled object is a complete certificate for the single order n = 23. That is beyond the
  bank target (success criterion (a) stops at 22) and is not one of the named partial wins p1 (16) or p2
  (20). The archive also contains independently derived certificates for n = 10..22; those files were not
  before this three-skeptic panel and are not part of confirmed_scope.
- No downgrade trigger on the n = 23 claim: no hedging on the science, no reproduction mismatch, scope no
  wider than what the three skeptics reproduced, no sample presented as complete, no capped search used as
  exclusion, no evasion, one cell (every tree on 23 vertices).
- Packaging note: the archive is published on Zenodo at https://doi.org/10.5281/zenodo.24322888
  (file https://zenodo.org/records/24322888/files/odd-graceful-trees-10-23-certificates.tar.xz?download=1,
  sha256 f89ddd847de5ea066c05730800a17ac01f9ee694c346638d40d1b1b0dc526713, 271015048 bytes).
