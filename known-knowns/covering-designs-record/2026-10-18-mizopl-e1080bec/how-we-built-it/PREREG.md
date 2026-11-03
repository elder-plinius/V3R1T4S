# PREREG (frozen 2026-10-18T03:12:16Z, before any attack output of this run)

criterion: verbatim in target.md (bank success_criterion for covering-designs-record; partial wins p1, p2). This run
targets the main criterion only, one (v,k,t) cell per claim.

checker (frozen, deterministic, exhaustive):
- tools/cover_check.py V K T FILE (sha256 dcf6f867fa3ea9d0e823640581f48d52d0a033a3a12bc1412085032f6abd82ac, the
  frozen checker of run 2328), used when C(v,t) <= 3e8 (its 1-byte-per-subset array must stay under the 1.5 GB/process cap);
- tools/cover_check_bits V K T FILE (source tools/cover_check_bits.c sha256
  f2461aec972520c7ebf57d3de8000c6feccbfc0ed2d4f702c2f6867006ba1378; x86_64 binary sha256
  ce5d224e0589dbd4dcaea7466320315749c3fa3ffdab18d5f9127397dee388e0), the same definition with a 1-bit-per-subset
  bitmap, used for every cell (and the only one for C(v,t) > 3e8). Both pass/fail identically on the positive and negative
  tests in tools/test_cover_check_out.txt and commander/checker_crosscheck.txt.
A candidate counts only if the applicable checker's last line is "COVER_CHECK: PASS" and C(v,t) <= 5e9.

statistic: b = number of blocks. live_value = min over: the CR (v,k,t) archive re-fetched by one plain GET at
verification time (data/cr_archive_vkt.txt is the 03:10:29Z copy), the LJCR snapshot value (Zenodo coverdata.json
v1.1 / GitHub dmgordo/LJCR), and any value for that (v,k,t) found on GitHub/arXiv/Zenodo in the last 6 months.

thresholds: strict b < live_value; a tie is NOTHING. b < Schonheim L(v,k,t) = bug, never a result. Cells with
C(v,t) > 5e9 ((77,25,8), (86,23,7)) are at most "PENDING chunked exhaustive check" this run.

ratchet (autoresearch section 1, optimizer lens only): metric = b of a design that passes the checker (lower is better);
ratchet_budget: 10 min per experiment; ratchet_patience: 8.

null_test: not needed because a candidate is an explicit object judged by a deterministic exhaustive checker against a table value (no statistical claim).
