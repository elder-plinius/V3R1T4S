# Fetch notes (novelty seat)
- fetch_log.tsv: one live session 2026-10-17T04:27:56Z..04:30:01Z UTC (06:27-06:30 Berlin, UTC+2); curl -L, HTTP code and sha256 of the bytes AS FETCHED.
- raw/ssp.html.redacted and raw/pending-requests.html.redacted: email addresses replaced with [email-redacted]; their sha256 therefore differs from the log, which records the unredacted as-fetched bytes.
- raw/radius_root.txt in the log was saved as raw/radius_root_404.html (404 page for /ssp/radius.txt).
- raw/ssp20000.txt (1130016 bytes, > 1 MB) was not kept; its hash is in the log. spotcheck_novelty.py needs it re-fetched to rerun N=20000.
- hydra.nat.uni-magdeburg.de mirror: both requests timed out after 120 s (HTTP 000, curl error 28); nothing saved. Tarball not fetched (per-N files used instead).
