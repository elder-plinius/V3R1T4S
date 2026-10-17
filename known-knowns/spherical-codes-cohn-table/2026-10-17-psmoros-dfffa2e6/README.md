# spherical-codes-cohn-table: the (6,526) code now on the table, against the pre-upload table value

This package replaces PR #231 (closed as superseded), as the V3R1T4S maintainer asked there: it carries the code whose value
the live table now lists for (6,526) (the live coordinates were not fetched; see below), compares it with the table value from before any of our uploads, and says
plainly who uploaded what and when.

## What

The 526-point code object/d6_N526.txt (sha256 dfffa2e6...) has 26-digit coordinates and c* = 0.786427532330074152872057, which is 2.0887e-4 below the cosine 0.786636400242 that spherical-codes.org listed for the unstarred, unlabelled (6,526) row before any upload (/plain 2026-10-16T05:12:04Z, index 05:12:06Z), with d = 6 outside the kissing exclusion; the live table's value 0.786427532331 equals this c* rounded up at the 12th decimal, and that the live table holds this exact file is inferred, not shown.

## Check it yourself

From this folder, with only Python 3 (standard library):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (a few seconds on a laptop; every one of the 138,075 pairs in decimal arithmetic at
70 digits, plus the object's sha256). Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | value compared | ours | gain | URL | fetched (UTC) |
|---|---|---|---|---|---|---|
| Henry Cohn, Table of spherical codes, before our uploads | (d, N) = (6, 526), no star, no "needs more optimization", held by Vahteristo (arXiv:2610.19988) | 0.786636400242 | 0.786427532330074 | 2.0887e-4 | https://spherical-codes.org/plain | 2026-10-16T05:12:04Z |
| the same table, live (context) | (6, 526) | 0.786427532331, "Pavlos Moros, 2026." | 0.786427532330074 | equal at 12 decimals (ours rounded up) | https://spherical-codes.org/ | 2026-10-17T21:47:47Z |

Smaller is better: the table lists the cosine of the minimal angle. Minimal angle of this code: 38.14710 degrees.

## Who uploaded it, and when (plainly)

- 2026-10-16T06:21:20Z: a first code for this row (c* 0.786430618545, sha256 9ab80210..., the object of PR #231) was
  uploaded to spherical-codes.org/upload-code by Claude, an AI agent working for Pavlos Moros, with one curl POST
  (User-Agent: curl). Pavlos Moros had explicitly asked for this upload in chat about half an hour earlier.
- 2026-10-16T07:26Z (about): Pavlos Moros gave Claude standing permission to upload verified codes to the table
  without asking each time. Claude then set up an upload script that ran at the end of each tables-lane run (run 0758's PREREG calls it "the
  human's upload script": Claude wrote it at Pavlos Moros's request).
- 2026-10-16, 14:41:11Z to 15:26:01Z: this code was uploaded by that script, as one of 331 rows sent in 28 requests
  (User-Agent: curl; times from the script's own log, which does not record which request carried which file). It is an
  in-place re-polish of the first code, made in run 2026-10-16-0758.
- robots.txt: the site's robots.txt allows generic agents only "/", /robots.txt and /static/; /plain, /data/* and
  /upload-code are allowed only to the ChatGPT-User and Claude-User agents. Claude did not read robots.txt before the
  first upload or before setting up the script. Run 2026-10-16-0758 read it at 08:03:29Z, stopped its own /plain and
  /data requests and flagged the script under "Needs you" in its report; the script still ran automatically when that
  run ended (14:41Z to 15:26Z), before anyone had read the flag. Claude switched the script off at about 16:05Z, and Pavlos Moros
  apologised to Henry Cohn by email the same morning. The pre-upload comparison value above also comes from scripted
  /plain fetches (2026-10-16T00:28Z to 05:12Z, User-Agent naming V3R1T4S) made before robots.txt had been read; we do
  not know whether robots.txt read the same then.
- After the first upload, Pavlos Moros saw the row labelled "Uploaded by anonymous internet user" (2026-10-16, about
  07:58Z, in a browser). An index fetch at 2026-10-16T19:49Z (sha256 9f3dc0684b7be6bebaef171a2e39f689c0019074aeb785018a1f1785b0ff1c0e)
  and the live index of 2026-10-17T21:47:47Z both list 0.786427532331, "Pavlos Moros, 2026" (the table's upload page
  says credits are added when the maintainer reviews uploads). Our upload ledger has: 2026-10-16T15:26:32Z, 6, 526,
  c* 0.786427532330074, sha256 dfffa2e676f24cbecc11657a119d33fd2169f06963446dbde15c10e6455c8eb8, HTTP 302. The live coordinates at /data/6/526 were not fetched (robots.txt), so that the table holds this exact file
  is inferred from the matching value, not shown.
- PR #231's README said "Nothing was uploaded to spherical-codes.org". That was true when its package was built and
  stopped being true about an hour later; its PR body noted the upload.

## Not claimed

- Not a claim that the live table is beaten: the live table lists this code. The comparison is with the pre-upload
  value, as the maintainer asked in PR #231.
- Only the row (6, 526). No optimality, no exact (algebraic) value, nothing about other rows.
- The search code is randomised; a rerun gives a code of similar quality, not this file byte for byte.

## Credits

- Henry Cohn, Table of spherical codes, https://spherical-codes.org/ (data set https://hdl.handle.net/1721.1/153543):
  the table compared against, and the posted (6,527) code ("needs more optimization") that was the starting point of the first version; this version is an in-place re-polish of that first code (run 2026-10-16-0758, how-we-built-it/repolish-run0758/).
- Ilmari Vahteristo, "New spherical codes by tuning an annealing solver", arXiv:2610.19988,
  https://arxiv.org/abs/2610.19988; codes on Zenodo https://doi.org/10.5281/zenodo.23270586: the code that holds the
  (6,526) row, and the LogSumExp-annealing idea used in the polish.
- A. Jay, M. Poberznik, M. Brut, A. Hemeryck, L.-H. Hoang, M. Gunde, N. Salles, G. Cruchon and M. Roux,
  "Equidistribution of points on the hypersphere including symmetries" (SSRN 6427919): earlier holders of the row.
- Methods: monotonic basin hopping (R. H. Leary 2000; A. Grosso, M. Locatelli, F. Schoen 2007); the penalty-threshold
  polish follows soft-sphere jamming (Lubachevsky-Stillinger).
- Submission credit: psmoros. Built and reviewed with the V3R1T4S protocol, https://github.com/elder-plinius/V3R1T4S;
  panel: REPRODUCE (fable), NOVELTY and CRITERION (opus) subagents, each seeing only the claim.
