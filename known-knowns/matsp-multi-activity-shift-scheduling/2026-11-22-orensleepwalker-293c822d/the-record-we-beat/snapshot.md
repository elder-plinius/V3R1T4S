# What these results are compared against

Table: https://www.schedulingbenchmarks.org/matsp/ fetched 2026-11-22T08:26:45Z, HTTP 200, page sha256 f14664f5e33d0a99e1bf19d97f6e7eedfad344fbd45b744dbfdb1bbbb17ee984; it lists 225 'Best known' values (all TRA26) and no lower bounds. The best known value of each certified instance is copied into object/certificates.csv (column best_known); every one matched the table (how-we-built-it/code/check_table.py) and was re-checked live by the NOVELTY reviewer at 2026-11-22T08:56Z.
Changes page: https://www.schedulingbenchmarks.org/changes.html, same time, sha256 6eb567e75bfe9a5615fc79a58a6210c980764d2fb1d2a900706bbaff41cfef3b; no multi-activity entry after 7 Oct 2026.
Published lower bounds: Trautsch and Kovari, Journal of Scheduling 2026 (doi 10.1007/s10951-026-00886-z), prove instances 1, 3, 4, 5, 77 and 78 optimal (not claimed here); their CP/IP lower bounds for other instances are much weaker (e.g. 9: 93, 50: 2, 89: 73).
Instances: https://www.schedulingbenchmarks.org/matsp/data/instances1_225.zip, sha256 202ddbc48da844a404298f24edecc00f717c21e334e1dfe510e9b20d081cd556.
