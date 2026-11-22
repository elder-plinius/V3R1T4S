# The record we compared against

No third-party page or file is copied here. Each row records one GET (Python urllib, default User-Agent, no retries).

| URL | fetched (UTC) | HTTP | bytes | Last-Modified | sha256 |
|---|---|---|---|---|---|
| https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html | 2026-10-19T03:57:05Z | 200 | 40715 | Mon, 26 Feb 2018 16:57:00 GMT | `b1033b4142e8db518d0e9ef448c5e9d9e7fe651bc2088a0d54aad671eec030ef` |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/points.tgz | 2026-10-19T03:57:08Z | 200 | 276791 | Sun, 16 Oct 2005 03:56:11 GMT | `bd568d308fc3944501e97fae1eb64d536769b59f0677f0e080246416c3c5f561` |
| https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/Co.zip | 2026-10-19T03:57:10Z | 200 | 25979 | Mon, 30 Aug 2010 11:30:10 GMT | `28141c13e9658f901e6fa49228b38f3eca69a206f904a34043280f2ecebde9ca` |

Extracted cells: the 199 posted (N, point group, energy) rows of cobalt.html are the columns N, point_group and
E_table_posted of ../object/ccd_cobalt_audit.csv; the ten Co/Energy.txt values are its column E_coZip_posted.
The page states no potential parameters; it cites Zhan, Chen, Liu, Lai, J. Chem. Phys. 122, 244707 (2005),
doi:10.1063/1.1940028, and credits the Co.zip minima to Lai Xiangjing, Huang Wenqi and Ni Hanwen.
