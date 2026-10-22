# Status snapshot (not the pages themselves)

One plain request each, User-Agent "V3R1T4S-scout (curl)", no retries. Response headers were not saved.

| URL | UTC fetch time | HTTP | sha256 of the page | extracted value |
|---|---|---|---|---|
| https://wiki.bbchallenge.org/wiki/Holdouts_lists | 2026-10-17T17:10:25Z | 200 | 383b2762ae23d192e2261cf2eae4efccfd5bd902d109ff09938f5aca2d912762 | newest BB(6) row: "October 16th, 2026 @mxdys 663 BB6_holdouts_663.txt" |
| https://wiki.bbchallenge.org/w/images/6/69/BB6_holdouts_663.txt | 2026-10-17T17:10:25Z | 200 | cfb2540f8101f2f2f20a14f9bc848252e34e45de2920fdd6b257096093844ee9 | line 523: 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB (an undecided holdout) |
| https://wiki.bbchallenge.org/wiki/BB(6) | 2026-10-17T17:10:25Z | 200 | 0351b327d494d0fd01c2013f402fe3a943663e3faa43e81936a2236b656d54f5 | no occurrence of the machine or any of its 240 mirror/state-permutation images |
| https://wiki.bbchallenge.org/wiki/1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB | 2026-10-17T17:10:26Z | 404 | 01b3aa30b733164f62ca930aa0f093e035d10e3b36690f9f881b490a6d04635a | no page for the machine |
| https://docs.google.com/spreadsheets/d/1mMp8bAcTFT91j7azn72liX8NSTwc2E_ozKnOGTfRCfw/export?format=csv&gid=1330361301 (307, Location followed once) | 2026-10-17T17:10:26Z | 200 | fc025a7fe96f1e36376c76216439511c621ca871b8f7e9f07d782f75e7577195 | row: Status empty, Classification "Quadratic Mess", Notes empty, Sources empty |

The NOVELTY skeptic re-fetched the status page at 2026-10-17T17:13:38Z (same revision, newest row unchanged); see panel/novelty.md.
Community channel (Discord #bb6): not readable by an agent; the workspace human's manual searches found no rule set (panel/novelty.md, "Human reports").
