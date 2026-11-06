# Timeline (UTC; every value is from a command)
$ cat runs/*/start_utc.txt
2026-10-25-0955: 2026-10-25T08:51:32Z
2026-10-25-0948: 2026-10-25T09:48:30Z
2026-10-25-1015: 2026-10-25T10:15:55Z
2026-10-25-1017: 2026-10-25T10:17:04Z
$ date -u -r <file> +%FT%TZ
2026-10-25T08:53:07Z ../2026-10-25-0955/PREREG.md
2026-10-25T09:48:30Z ../2026-10-25-0948/PREREG.md
2026-10-25T10:17:04Z PREREG.md
2026-10-25T10:17:04Z PREREG.sha256
2026-10-25T10:17:08Z data/dnacodes.html
2026-10-25T10:17:48Z attempts/regenerate/A4GC_19_14_object.txt
2026-10-25T10:27:12Z null_test.md
data fetch (curl, written by date -u): 2026-10-25T10:17:08Z
Note: the folder name 0955 was typed by hand. That sweep really started 08:51:32Z. Folders 0948, 1015 and 1017 are named with date -u. 1015 was aborted with no measurement (ABORTED.md).
