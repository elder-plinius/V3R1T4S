# Panel copies: redactions

The four panel files are byte copies of the run's panel/ files, made after the gate. No change was needed: they
contain no machine-local absolute paths (the skeptics wrote their scratch locations as relative names such as
panel0423-reproduce/ and rep0423/), so kit/check_run.py's leak scan passes on them as written.

| file | replaced | sha256 of the run's original (= this copy) |
|---|---|---|
| reproduce.md | nothing | e6efe13284e3ea0e04d7fa1e4bf444b324284264431fa5a1deb0a84ae61c7a1d |
| novelty.md | nothing | 48174ad4e15a8cb218fb47f6ac22ad5a65b2cb2dc05b7fd93ea306ef77d4be2b |
| criterion.md | nothing | 5abac499bcdfcf49f26ab9e11fb0f11bbc0ead4753269b01424e5e37a3ca1b8c |
| gate.md | nothing | f4bcabff873694daaf4c5deabf910af5d685e5507fba3e31b368e3a457738955 |

In the panel text, claim/code/ and claim/result/ are the run's names for the files shipped here as object/code/
and object/evidence/ (same bytes; object/VALUE.txt pins them, and code/A/totF.c, code/B/main.go keep their
subfolders). claim/data/ (the fetched OEIS pages) is not shipped (third-party content);
the-record-we-beat/TABLE_SNAPSHOT.md records its URLs, times and sha256. claim/tools/geng is pinned, not shipped.
